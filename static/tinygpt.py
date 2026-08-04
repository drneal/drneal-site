"""
tinygpt.py — a decoder-only transformer in NumPy, with hand-written backprop.

A faithful Python/NumPy port of the model CJ builds in TypeScript in
"I Built an LLM from Scratch" (https://github.com/w3cj/how-llms-work).

No autograd, no ML framework. Every gradient is derived by hand and checked
against finite differences.

    python tinygpt.py check     # numerical gradient check
    python tinygpt.py train     # train on a toy corpus and sample text

Reference: Vaswani et al. (2017); Radford et al. (2018); Ba et al. (2016);
Kingma & Ba (2014); Glorot & Bengio (2010); Holtzman et al. (2019).
"""
from __future__ import annotations

import sys
from collections import Counter
from dataclasses import dataclass

import numpy as np

DTYPE = np.float64
EPS_LN = 1e-5


# --------------------------------------------------------------------------
# 1. Tokenizer: Byte-Pair Encoding
# --------------------------------------------------------------------------
import re

PRE_TOKEN_RE = re.compile(r"\s\w+|[^\w\s]")     # GPT-2 style: space glued to word


def count_words(text, regex=PRE_TOKEN_RE):
    return Counter(regex.findall(text))


def merge_tokens(tokens, pair, merged):
    out, i = [], 0
    while i < len(tokens):
        if i < len(tokens) - 1 and tokens[i] == pair[0] and tokens[i + 1] == pair[1]:
            out.append(merged)
            i += 2
        else:
            out.append(tokens[i])
            i += 1
    return out


def train_bpe(word_freqs, max_merges=1000):
    splits = {w: list(w) for w in word_freqs}
    merges = []
    for _ in range(max_merges):
        pair_freq = Counter()
        for w, toks in splits.items():
            weight = word_freqs[w]
            for a, b in zip(toks, toks[1:]):
                pair_freq[(a, b)] += weight
        if not pair_freq:
            break
        (a, b), count = pair_freq.most_common(1)[0]
        merged = a + b
        splits = {w: merge_tokens(t, (a, b), merged) for w, t in splits.items()}
        merges.append(((a, b), merged, count))
    return merges


def apply_merges(text, merges, regex=PRE_TOKEN_RE):
    out = []
    for pre in regex.findall(text):
        toks = list(pre)
        for pair, merged, _ in merges:
            toks = merge_tokens(toks, pair, merged)
        out.extend(toks)
    return out


# --------------------------------------------------------------------------
# 2. Config and parameter initialisation
# --------------------------------------------------------------------------
@dataclass
class Config:
    vocab_size: int
    context_len: int = 32
    emb_dim: int = 32
    num_heads: int = 2
    ff_dim: int = 128
    num_layers: int = 2

    @property
    def head_dim(self):
        assert self.emb_dim % self.num_heads == 0
        return self.emb_dim // self.num_heads


def xavier(rng, shape, fan_in, fan_out):
    limit = np.sqrt(6.0 / (fan_in + fan_out))
    return rng.uniform(-limit, limit, size=shape).astype(DTYPE)


def init_weights(cfg: Config, seed=42):
    rng = np.random.default_rng(seed)
    V, C, D, F, N = (cfg.vocab_size, cfg.context_len, cfg.emb_dim,
                     cfg.ff_dim, cfg.num_layers)
    w = {
        "tok_emb": xavier(rng, (V, D), V, D),
        "pos_emb": xavier(rng, (C, D), C, D),
        "lnf_g": np.ones(D, DTYPE),
        "lnf_b": np.zeros(D, DTYPE),
        "head_W": xavier(rng, (D, V), D, V),
        "head_b": np.zeros(V, DTYPE),
    }
    for i in range(N):
        p = f"b{i}."
        w[p + "ln1_g"] = np.ones(D, DTYPE)
        w[p + "ln1_b"] = np.zeros(D, DTYPE)
        for nm in ("Wq", "Wk", "Wv", "Wo"):
            w[p + nm] = xavier(rng, (D, D), D, D)
        for nm in ("bq", "bk", "bv", "bo"):
            w[p + nm] = np.zeros(D, DTYPE)
        w[p + "ln2_g"] = np.ones(D, DTYPE)
        w[p + "ln2_b"] = np.zeros(D, DTYPE)
        w[p + "W1"] = xavier(rng, (D, F), D, F)
        w[p + "b1"] = np.zeros(F, DTYPE)
        w[p + "W2"] = xavier(rng, (F, D), F, D)
        w[p + "b2"] = np.zeros(D, DTYPE)
    return w


def zeros_like_weights(w):
    return {k: np.zeros_like(v) for k, v in w.items()}


def count_params(w):
    return sum(v.size for v in w.values())


# --------------------------------------------------------------------------
# 3. Primitive layers
# --------------------------------------------------------------------------
def layernorm_forward(x, g, b):
    mu = x.mean(axis=-1, keepdims=True)
    var = x.var(axis=-1, keepdims=True)
    inv = 1.0 / np.sqrt(var + EPS_LN)
    xhat = (x - mu) * inv
    return g * xhat + b, (xhat, inv, g)


def layernorm_backward(dout, cache):
    xhat, inv, g = cache
    D = xhat.shape[-1]
    dg = (dout * xhat).sum(axis=tuple(range(dout.ndim - 1)))
    db = dout.sum(axis=tuple(range(dout.ndim - 1)))
    gh = dout * g
    dx = inv * (gh
                - gh.mean(axis=-1, keepdims=True)
                - xhat * (gh * xhat).mean(axis=-1, keepdims=True))
    return dx, dg, db


def softmax(z, axis=-1):
    z = z - z.max(axis=axis, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=axis, keepdims=True)


def softmax_backward(dout, out, axis=-1):
    """Jacobian-vector product: a * (g - sum(g*a))."""
    return out * (dout - (dout * out).sum(axis=axis, keepdims=True))


# --------------------------------------------------------------------------
# 4. Forward pass
# --------------------------------------------------------------------------
def forward(ids, w, cfg: Config):
    S = len(ids)
    D, H, hd, N = cfg.emb_dim, cfg.num_heads, cfg.head_dim, cfg.num_layers
    scale = 1.0 / np.sqrt(hd)

    ids = np.asarray(ids, dtype=np.int64)
    x = w["tok_emb"][ids] + w["pos_emb"][:S]           # (S, D)

    mask = np.triu(np.ones((S, S), dtype=bool), k=1)   # True where j > i
    blocks = []

    for i in range(N):
        p = f"b{i}."
        h, ln1c = layernorm_forward(x, w[p + "ln1_g"], w[p + "ln1_b"])

        Q = h @ w[p + "Wq"] + w[p + "bq"]
        K = h @ w[p + "Wk"] + w[p + "bk"]
        V = h @ w[p + "Wv"] + w[p + "bv"]

        # (S, D) -> (H, S, hd)
        Qh = Q.reshape(S, H, hd).transpose(1, 0, 2)
        Kh = K.reshape(S, H, hd).transpose(1, 0, 2)
        Vh = V.reshape(S, H, hd).transpose(1, 0, 2)

        scores = (Qh @ Kh.transpose(0, 2, 1)) * scale          # (H, S, S)
        scores = np.where(mask[None], -np.inf, scores)
        A = softmax(scores, axis=-1)                            # (H, S, S)
        ctx = A @ Vh                                            # (H, S, hd)
        ctx_flat = ctx.transpose(1, 0, 2).reshape(S, D)

        attn_out = ctx_flat @ w[p + "Wo"] + w[p + "bo"]
        x1 = x + attn_out

        h2, ln2c = layernorm_forward(x1, w[p + "ln2_g"], w[p + "ln2_b"])
        f1 = h2 @ w[p + "W1"] + w[p + "b1"]
        r = np.maximum(f1, 0.0)
        f2 = r @ w[p + "W2"] + w[p + "b2"]
        out = x1 + f2

        blocks.append(dict(x=x, ln1c=ln1c, h=h, Qh=Qh, Kh=Kh, Vh=Vh, A=A,
                           ctx_flat=ctx_flat, x1=x1, ln2c=ln2c, h2=h2,
                           f1=f1, r=r))
        x = out

    hf, lnfc = layernorm_forward(x, w["lnf_g"], w["lnf_b"])
    logits = hf @ w["head_W"] + w["head_b"]                     # (S, V)
    probs = softmax(logits, axis=-1)

    cache = dict(ids=ids, blocks=blocks, hf=hf, lnfc=lnfc,
                 logits=logits, probs=probs, S=S, mask=mask)
    return cache


def cross_entropy(probs, targets):
    S = len(targets)
    return float(-np.log(probs[np.arange(S), targets] + 1e-12).sum() / S)


# --------------------------------------------------------------------------
# 5. Backward pass
# --------------------------------------------------------------------------
def backward(cache, targets, w, cfg: Config, grads):
    S = cache["S"]
    D, H, hd, N = cfg.emb_dim, cfg.num_heads, cfg.head_dim, cfg.num_layers
    scale = 1.0 / np.sqrt(hd)
    targets = np.asarray(targets, dtype=np.int64)

    # --- cross-entropy + softmax fused: dL/dz = (p - onehot) / S ----------
    dlogits = cache["probs"].copy() / S
    dlogits[np.arange(S), targets] -= 1.0 / S

    grads["head_b"] += dlogits.sum(axis=0)
    grads["head_W"] += cache["hf"].T @ dlogits
    dx = dlogits @ w["head_W"].T

    dx, dg, db = layernorm_backward(dx, cache["lnfc"])
    grads["lnf_g"] += dg
    grads["lnf_b"] += db

    for i in reversed(range(N)):
        p = f"b{i}."
        bc = cache["blocks"][i]

        # residual 2: out = x1 + f2
        dx1 = dx.copy()
        df2 = dx

        grads[p + "b2"] += df2.sum(axis=0)
        grads[p + "W2"] += bc["r"].T @ df2
        dr = df2 @ w[p + "W2"].T
        df1 = np.where(bc["f1"] > 0, dr, 0.0)

        grads[p + "b1"] += df1.sum(axis=0)
        grads[p + "W1"] += bc["h2"].T @ df1
        dh2 = df1 @ w[p + "W1"].T

        dln2, dg2, db2 = layernorm_backward(dh2, bc["ln2c"])
        grads[p + "ln2_g"] += dg2
        grads[p + "ln2_b"] += db2

        # residual 1: x1 = x + attn_out
        dx1 = dx1 + dln2
        dattn = dx1
        dx_in = dx1.copy()

        grads[p + "bo"] += dattn.sum(axis=0)
        grads[p + "Wo"] += bc["ctx_flat"].T @ dattn
        dctx_flat = dattn @ w[p + "Wo"].T
        dctx = dctx_flat.reshape(S, H, hd).transpose(1, 0, 2)   # (H, S, hd)

        # ctx = A @ Vh
        dA = dctx @ bc["Vh"].transpose(0, 2, 1)                 # (H, S, S)
        dVh = bc["A"].transpose(0, 2, 1) @ dctx                 # (H, S, hd)

        dscores = softmax_backward(dA, bc["A"], axis=-1)
        dscores = np.where(cache["mask"][None], 0.0, dscores) * scale

        dQh = dscores @ bc["Kh"]                                # (H, S, hd)
        dKh = dscores.transpose(0, 2, 1) @ bc["Qh"]             # (H, S, hd)

        dQ = dQh.transpose(1, 0, 2).reshape(S, D)
        dK = dKh.transpose(1, 0, 2).reshape(S, D)
        dV = dVh.transpose(1, 0, 2).reshape(S, D)

        h = bc["h"]
        grads[p + "bq"] += dQ.sum(axis=0); grads[p + "Wq"] += h.T @ dQ
        grads[p + "bk"] += dK.sum(axis=0); grads[p + "Wk"] += h.T @ dK
        grads[p + "bv"] += dV.sum(axis=0); grads[p + "Wv"] += h.T @ dV

        dh = dQ @ w[p + "Wq"].T + dK @ w[p + "Wk"].T + dV @ w[p + "Wv"].T

        dln1, dg1, db1 = layernorm_backward(dh, bc["ln1c"])
        grads[p + "ln1_g"] += dg1
        grads[p + "ln1_b"] += db1

        dx = dx_in + dln1

    # --- embeddings: scatter-add ------------------------------------------
    np.add.at(grads["tok_emb"], cache["ids"], dx)
    grads["pos_emb"][:S] += dx
    return grads


# --------------------------------------------------------------------------
# 6. Adam
# --------------------------------------------------------------------------
def init_adam(w):
    return {k: [np.zeros_like(v), np.zeros_like(v)] for k, v in w.items()}


def adam_step(w, grads, state, t, lr=1e-3, b1=0.9, b2=0.999, eps=1e-8):
    bc1 = 1.0 - b1 ** t
    bc2 = 1.0 - b2 ** t
    for k in w:
        m, v = state[k]
        g = grads[k]
        m *= b1; m += (1 - b1) * g
        v *= b2; v += (1 - b2) * g * g
        w[k] -= lr * (m / bc1) / (np.sqrt(v / bc2) + eps)


# --------------------------------------------------------------------------
# 7. Generation
# --------------------------------------------------------------------------
def sample_next(logits, temperature=0.8, top_p=0.9, rng=None):
    rng = rng or np.random.default_rng()
    z = np.asarray(logits, DTYPE) / max(temperature, 1e-8)
    p = softmax(z)
    order = np.argsort(-p)
    csum = np.cumsum(p[order])
    keep = int(np.searchsorted(csum, top_p) + 1)
    idx = order[:keep]
    q = p[idx] / p[idx].sum()
    return int(rng.choice(idx, p=q))


def generate(w, cfg, seed_ids, max_new=40, idx_to_token=None,
             temperature=0.8, top_p=0.9, rng=None, seq_len=None):
    window = seq_len or cfg.context_len
    ids = list(seed_ids)
    for _ in range(max_new):
        ctx = ids[-window:]
        cache = forward(ctx, w, cfg)
        ids.append(sample_next(cache["logits"][-1], temperature, top_p, rng))
    if idx_to_token is None:
        return ids
    return "".join(idx_to_token[i] for i in ids)


# --------------------------------------------------------------------------
# 8. Gradient check
# --------------------------------------------------------------------------
def gradient_check(n_probe=4, seed=0):
    rng = np.random.default_rng(seed)
    cfg = Config(vocab_size=11, context_len=8, emb_dim=8,
                 num_heads=2, ff_dim=16, num_layers=2)
    w = init_weights(cfg, seed=1)
    ids = rng.integers(0, cfg.vocab_size, size=6).tolist()
    tgt = rng.integers(0, cfg.vocab_size, size=6).tolist()

    grads = zeros_like_weights(w)
    cache = forward(ids, w, cfg)
    backward(cache, tgt, w, cfg, grads)

    def loss_of(w):
        return cross_entropy(forward(ids, w, cfg)["probs"], tgt)

    worst, worst_key = 0.0, None
    eps = 1e-5
    for key in w:
        flat = w[key].ravel()
        gflat = grads[key].ravel()
        probes = rng.choice(flat.size, size=min(n_probe, flat.size), replace=False)
        for i in probes:
            old = flat[i]
            flat[i] = old + eps; lp = loss_of(w)
            flat[i] = old - eps; lm = loss_of(w)
            flat[i] = old
            num = (lp - lm) / (2 * eps)
            # Skip probes where both values are numerical noise. Note that
            # grads for `bk` are exactly zero: adding a constant to every key
            # shifts a whole softmax row uniformly, and softmax is
            # shift-invariant, so bK cannot affect the output at all.
            if max(abs(num), abs(gflat[i])) < 1e-9:
                continue
            den = max(1e-12, abs(num) + abs(gflat[i]))
            rel = abs(num - gflat[i]) / den
            if rel > worst:
                worst, worst_key = rel, f"{key}[{i}]"
    return worst, worst_key


# --------------------------------------------------------------------------
# 9. Train on a toy corpus
# --------------------------------------------------------------------------
STORIES = [
    "the cat sat on the mat and the cat was happy",
    "the dog ran to the park and the dog was happy",
    "a boy saw the cat and the boy smiled at the cat",
    "a girl saw the dog and the girl smiled at the dog",
    "the cat and the dog sat on the mat together",
    "the boy and the girl ran to the park together",
    "the king saw the queen and the king smiled",
    "the queen saw the king and the queen smiled",
]


def build_corpus(max_merges=120):
    text = "".join(" " + s for s in STORIES).lower()
    merges = train_bpe(count_words(text), max_merges=max_merges)
    freq = Counter()
    for s in STORIES:
        for t in apply_merges(" " + s.lower(), merges):
            freq[t] += 1
    idx_to_token = [t for t, _ in freq.most_common()]
    token_to_idx = {t: i for i, t in enumerate(idx_to_token)}
    all_ids = []
    for s in STORIES:
        for t in apply_merges(" " + s.lower(), merges):
            all_ids.append(token_to_idx[t])
    return merges, idx_to_token, token_to_idx, all_ids


def train(epochs=300, num_layers=2, seq_len=16, lr=3e-3, seed=42, verbose=True):
    merges, idx_to_token, token_to_idx, all_ids = build_corpus()
    V = len(idx_to_token)
    cfg = Config(vocab_size=V, context_len=32, emb_dim=32,
                 num_heads=2, ff_dim=128, num_layers=num_layers)
    seq_len = min(seq_len, cfg.context_len)

    seqs = [(all_ids[i:i + seq_len], all_ids[i + 1:i + seq_len + 1])
            for i in range(len(all_ids) - seq_len - 1)]

    w = init_weights(cfg, seed=seed)
    state = init_adam(w)
    rng = np.random.default_rng(seed)

    if verbose:
        print(f"vocab={V}  sequences={len(seqs)}  params={count_params(w):,}")
        print(f"uniform-baseline loss = ln(V) = {np.log(V):.3f}\n")

    for epoch in range(1, epochs + 1):
        grads = zeros_like_weights(w)
        total = 0.0
        for x, y in seqs:
            cache = forward(x, w, cfg)
            total += cross_entropy(cache["probs"], y)
            backward(cache, y, w, cfg, grads)
        for k in grads:
            grads[k] /= len(seqs)
        adam_step(w, grads, state, epoch, lr=lr)

        if verbose and (epoch % 50 == 0 or epoch == 1):
            loss = total / len(seqs)
            sample = generate(w, cfg, all_ids[:3], max_new=25,
                              idx_to_token=idx_to_token, rng=rng, seq_len=seq_len)
            print(f"epoch {epoch:4d}  loss {loss:.4f}  ppl {np.exp(loss):6.1f}"
                  f"  | {sample.strip()!r}")
    return w, cfg, idx_to_token, all_ids


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "check":
        worst, key = gradient_check()
        print(f"worst relative gradient error: {worst:.3e}  (at {key})")
        print("PASS" if worst < 1e-5 else "FAIL")
    elif cmd == "train":
        train(epochs=int(sys.argv[2]) if len(sys.argv) > 2 else 300)
