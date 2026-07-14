"""
train_tinygpt.py — companion script to Lesson 5, "Train Your Own GPT"
https://drnealaggarwal.info/post/2026-07-10-train-your-own-gpt

Trains a small character-level GPT (from Lesson 4, "Inside the Transformer")
on any plain-text file. Put your corpus at ./corpus.txt and run:

    python train_tinygpt.py

Requires: torch (pip install torch). Runs on Apple Silicon (mps),
NVIDIA (cuda), or CPU. ~10-20 min on a GPU/Apple Silicon at defaults.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(1337)

# ── hyperparameters ──────────────────────────────────────────────────────────
CTX        = 256    # context window (characters). CPU-only? Try 128.
BATCH      = 64     # snippets per training step
D_MODEL    = 128    # embedding width
N_HEADS    = 4      # attention heads per block
N_LAYERS   = 4      # transformer blocks. CPU-only? Try 3.
LR         = 3e-4   # AdamW learning rate
STEPS      = 5000   # training steps
EVAL_EVERY = 500    # evaluate + sample this often

device = ("mps" if torch.backends.mps.is_available()
          else "cuda" if torch.cuda.is_available() else "cpu")
print(f"device: {device}")

# ── data pipeline (Lesson 5, "The data pipeline") ────────────────────────────
text = open("corpus.txt", encoding="utf-8").read()
chars = sorted(set(text))
vocab_size = len(chars)
print(f"corpus: {len(text):,} chars, vocab: {vocab_size}")

stoi = {c: i for i, c in enumerate(chars)}
itos = {i: c for c, i in stoi.items()}
encode = lambda s: [stoi[c] for c in s]
decode = lambda t: "".join(itos[i] for i in t)

data = torch.tensor(encode(text), dtype=torch.long)
n = int(0.9 * len(data))
train_data, val_data = data[:n], data[n:]   # last 10% = validation, never trained on


def get_batch(split):
    d = train_data if split == "train" else val_data
    ix = torch.randint(len(d) - CTX - 1, (BATCH,))
    x = torch.stack([d[i     : i + CTX    ] for i in ix])  # inputs
    y = torch.stack([d[i + 1 : i + CTX + 1] for i in ix])  # shifted by one = targets
    return x.to(device), y.to(device)


# ── model (Lesson 4, "A complete tiny GPT") ──────────────────────────────────
class Block(nn.Module):
    """Communicate (attention), then compute (MLP) — with residual adds."""
    def __init__(self, d_model, n_heads):
        super().__init__()
        self.ln1  = nn.LayerNorm(d_model)
        self.attn = nn.MultiheadAttention(d_model, n_heads, batch_first=True)
        self.ln2  = nn.LayerNorm(d_model)
        self.mlp  = nn.Sequential(
            nn.Linear(d_model, 4 * d_model),
            nn.GELU(),
            nn.Linear(4 * d_model, d_model),
        )

    def forward(self, x):
        T = x.shape[1]
        causal = torch.triu(torch.ones(T, T, device=x.device), 1).bool()
        h = self.ln1(x)
        attn_out, _ = self.attn(h, h, h, attn_mask=causal)  # no peeking ahead
        x = x + attn_out                 # write attention result onto the stream
        x = x + self.mlp(self.ln2(x))    # write MLP result onto the stream
        return x


class TinyGPT(nn.Module):
    def __init__(self, vocab_size, d_model=D_MODEL, n_heads=N_HEADS,
                 n_layers=N_LAYERS, ctx=CTX):
        super().__init__()
        self.tok_emb = nn.Embedding(vocab_size, d_model)  # what each token means
        self.pos_emb = nn.Embedding(ctx, d_model)         # where each token sits
        self.blocks  = nn.Sequential(*[Block(d_model, n_heads)
                                       for _ in range(n_layers)])
        self.ln_out  = nn.LayerNorm(d_model)
        self.head    = nn.Linear(d_model, vocab_size)     # scores over vocabulary

    def forward(self, idx):
        B, T = idx.shape
        pos = torch.arange(T, device=idx.device)
        x = self.tok_emb(idx) + self.pos_emb(pos)
        x = self.blocks(x)
        return self.head(self.ln_out(x))                  # logits: (B, T, vocab)


# ── evaluation and sampling (Lesson 5) ───────────────────────────────────────
@torch.no_grad()
def estimate_loss(model, split, iters=50):
    model.eval()
    losses = []
    for _ in range(iters):
        x, y = get_batch(split)
        logits = model(x)
        losses.append(F.cross_entropy(
            logits.view(-1, vocab_size), y.view(-1)).item())
    model.train()
    return sum(losses) / len(losses)


@torch.no_grad()
def generate(model, prompt, max_new_tokens=400, temperature=1.0):
    idx = torch.tensor([encode(prompt)], device=device)
    model.eval()
    for _ in range(max_new_tokens):
        logits = model(idx[:, -CTX:])             # crop to context window
        logits = logits[:, -1, :] / temperature   # last position only
        probs = F.softmax(logits, dim=-1)
        nxt = torch.multinomial(probs, num_samples=1)
        idx = torch.cat([idx, nxt], dim=1)
    model.train()
    return decode(idx[0].tolist())


# ── the training loop (Lesson 5, Figure 1) ───────────────────────────────────
if __name__ == "__main__":
    model = TinyGPT(vocab_size).to(device)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"parameters: {n_params:,}")

    opt = torch.optim.AdamW(model.parameters(), lr=LR)

    for step in range(STEPS + 1):
        if step % EVAL_EVERY == 0:
            tr = estimate_loss(model, "train")
            va = estimate_loss(model, "val")
            print(f"\nstep {step:5d}   train {tr:.3f}   val {va:.3f}")
            print("sample:", generate(model, "The ", 200).replace("\n", " "))

        x, y = get_batch("train")                            # ① batch
        logits = model(x)                                    # ② forward
        loss = F.cross_entropy(logits.view(-1, vocab_size),  # ③ score
                               y.view(-1))
        opt.zero_grad()
        loss.backward()                                      # ④ gradients
        opt.step()                                           # ⑤ nudge

    torch.save(model.state_dict(), "tinygpt.pt")
    print("\ndone — weights saved to tinygpt.pt")
    print(generate(model, "The ", 800))
