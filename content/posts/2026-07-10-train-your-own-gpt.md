---
title: "Train Your Own GPT"
date: 2026-07-10
category: Deep Learning
tags: GPT, transformer, training, PyTorch, gradient descent, language model, loss curves, hands-on exercise, deep learning
level: Intermediate–Advanced
read_time: 35 min
summary: "Lesson 5 of Learning With Dr Neal. Stop reading and train one: take the TinyGPT from Lesson 4, feed it a corpus small enough for a laptop, write the training loop with your own hands, and watch generated text condense out of randomness — from noise, to word-shaped noise, to sentences."
featured: false
---

<style>
.lesson-banner {
  font-size: 0.85em;
  background: linear-gradient(135deg, #1a237e 0%, #283593 100%);
  color: white;
  padding: 1.2em 1.6em;
  border-radius: 8px;
  margin: 1.5em 0;
  line-height: 1.6;
}
.lesson-banner a { color: #90caf9; font-weight: bold; }
.audio-section {
  font-size: 0.8em;
  background: #1a1f2e;
  border-left: 4px solid #1a237e;
  padding: 1em 1.4em;
  border-radius: 0 6px 6px 0;
  margin: 1.5em 0;
}
.callout {
  font-size: 0.85em;
  background: #1e1a0e;
  border-left: 4px solid #f9a825;
  padding: 0.8em 1.2em;
  margin: 1.2em 0;
  border-radius: 0 4px 4px 0;
}
.keyidea {
  font-size: 0.85em;
  background: #0e1e1a;
  border-left: 4px solid #10b981;
  padding: 0.8em 1.2em;
  margin: 1.2em 0;
  border-radius: 0 4px 4px 0;
}
.sample-box {
  font-size: 0.82em;
  background: #0d1117;
  border: 1px solid #1e2d45;
  border-radius: 6px;
  padding: 0.9em 1.2em;
  margin: 1em 0;
  font-family: 'JetBrains Mono', monospace;
  color: #c9d6e8;
  line-height: 1.55;
}
.sample-box .label { color: #f59e0b; font-weight: bold; }
figure.diagram {
  margin: 2em 0;
  text-align: center;
}
figure.diagram svg {
  max-width: 100%;
  height: auto;
}
figure.diagram figcaption {
  font-size: 0.8em;
  color: #6b82a0;
  margin-top: 0.6em;
  text-align: left;
}
</style>

<div class="lesson-banner">
📚 <strong>Lessons series — #5.</strong> This is the hands-on payoff of <a href="/post/2026-07-10-inside-the-transformer">Lesson 4</a>, and it leans on the gradient-descent foundations of <a href="/post/2026-06-19-how-deep-neural-networks-really-work">Lesson 1</a> and <a href="/post/2026-06-26-deep-learning-spreadsheet-exercise">Lesson 2</a>. You'll want a laptop with Python and PyTorch installed. The full curriculum lives on the <a href="/lessons">Lessons page</a>.
</div>

# Train Your Own GPT

Lesson 4 ended with a promise: stop reading and *train one*. Today we keep it.

By the end of this lesson you will have taken the `TinyGPT` we built last time, pointed it at a text corpus small enough for a laptop, written the training loop with your own hands, and — this is the part I want you to actually watch, in real time, rather than take on faith — seen its output evolve from random characters, to word-shaped gibberish, to grammatical sentences in the voice of your corpus. Nothing I know of calibrates your intuitions about what these models *are* better than watching one condense out of randomness in front of you. It takes about an hour, most of which is the computer's time rather than yours.

<div class="audio-section">
  🎧 <strong>Listen to this post:</strong> Coding your own self-supervised GPT — the audio companion to this lesson.<br/><br/>
  <audio controls style="width:100%; margin-top:0.4em;">
    <source src="/static/audio/Coding_Your_Own_Self-Supervised_GPT.mp3" type="audio/mpeg">
    <a href="/static/audio/Coding_Your_Own_Self-Supervised_GPT.mp3">Download the audio</a>
  </audio>
</div>

## What "training" actually means here

Let's assemble the pieces we already own. From Lessons 1–2: a neural network is a parameterised function, a **loss** measures how wrong it is on data, and **gradient descent** nudges every parameter slightly downhill on that loss, over and over. From Lesson 4: the transformer is such a function — it reads a token sequence and outputs, at *every position*, a probability distribution over the next token.

Training a GPT is nothing more than the marriage of the two:

<figure class="diagram">
<svg viewBox="0 0 720 400" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The training loop cycle">
  <defs>
    <marker id="larrC" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L8,4.5 L0,9 z" fill="#00d4f5"/>
    </marker>
  </defs>
  <rect x="0" y="0" width="720" height="400" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="34" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">ONE TRAINING STEP — REPEATED THOUSANDS OF TIMES</text>

  <!-- 1 batch -->
  <rect x="40" y="80" width="180" height="76" rx="10" fill="#2e1e5e" stroke="#a78bfa" stroke-width="1.5"/>
  <text x="130" y="108" text-anchor="middle" fill="#e8e3fa" font-family="sans-serif" font-size="13" font-weight="bold">① Grab a batch</text>
  <text x="130" y="128" text-anchor="middle" fill="#bdaef0" font-family="sans-serif" font-size="10.5">random snippets of corpus,</text>
  <text x="130" y="144" text-anchor="middle" fill="#bdaef0" font-family="sans-serif" font-size="10.5">targets = same text shifted by 1</text>

  <!-- 2 forward -->
  <rect x="270" y="80" width="180" height="76" rx="10" fill="#0a4a5c" stroke="#00d4f5" stroke-width="1.5"/>
  <text x="360" y="108" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="13" font-weight="bold">② Forward pass</text>
  <text x="360" y="128" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="10.5">model predicts next-token</text>
  <text x="360" y="144" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="10.5">probabilities at every position</text>

  <!-- 3 loss -->
  <rect x="500" y="80" width="180" height="76" rx="10" fill="#4a3000" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="590" y="108" text-anchor="middle" fill="#fdeccd" font-family="sans-serif" font-size="13" font-weight="bold">③ Score it</text>
  <text x="590" y="128" text-anchor="middle" fill="#f0c987" font-family="sans-serif" font-size="10.5">cross-entropy: how surprised</text>
  <text x="590" y="144" text-anchor="middle" fill="#f0c987" font-family="sans-serif" font-size="10.5">was it by the real next char?</text>

  <!-- 4 backward -->
  <rect x="500" y="230" width="180" height="76" rx="10" fill="#3d0f0f" stroke="#f87171" stroke-width="1.5"/>
  <text x="590" y="258" text-anchor="middle" fill="#fde2e2" font-family="sans-serif" font-size="13" font-weight="bold">④ Backward pass</text>
  <text x="590" y="278" text-anchor="middle" fill="#e2a0a0" font-family="sans-serif" font-size="10.5">gradient of loss w.r.t. every</text>
  <text x="590" y="294" text-anchor="middle" fill="#e2a0a0" font-family="sans-serif" font-size="10.5">one of the ~800k parameters</text>

  <!-- 5 step -->
  <rect x="270" y="230" width="180" height="76" rx="10" fill="#053d28" stroke="#10b981" stroke-width="1.5"/>
  <text x="360" y="258" text-anchor="middle" fill="#d3f5e6" font-family="sans-serif" font-size="13" font-weight="bold">⑤ Optimizer step</text>
  <text x="360" y="278" text-anchor="middle" fill="#8fd8b8" font-family="sans-serif" font-size="10.5">every parameter nudged a</text>
  <text x="360" y="294" text-anchor="middle" fill="#8fd8b8" font-family="sans-serif" font-size="10.5">tiny distance downhill</text>

  <!-- arrows -->
  <path d="M220,118 L262,118" stroke="#00d4f5" stroke-width="2" marker-end="url(#larrC)"/>
  <path d="M450,118 L492,118" stroke="#00d4f5" stroke-width="2" marker-end="url(#larrC)"/>
  <path d="M590,156 L590,222" stroke="#00d4f5" stroke-width="2" marker-end="url(#larrC)"/>
  <path d="M500,268 L458,268" stroke="#00d4f5" stroke-width="2" marker-end="url(#larrC)"/>
  <path d="M270,268 Q130,268 130,164" stroke="#00d4f5" stroke-width="2" fill="none" marker-end="url(#larrC)"/>
  <text x="150" y="240" fill="#00d4f5" font-family="monospace" font-size="12">repeat ~5,000×</text>

  <text x="360" y="372" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11.5">This is Lessons 1–2's gradient descent, applied to Lesson 4's architecture. There is no additional idea.</text>
</svg>
<figcaption><strong>Figure 1.</strong> The whole training loop. Note what's absent: no labels, no annotation effort, no human grading. The text itself is the supervision — every character is the "correct answer" for the characters before it. This is why language models can train on essentially unlimited data.</figcaption>
</figure>

<div class="keyidea">
💡 <strong>Key idea.</strong> Language modelling is <em>self-supervised</em>: the training signal is manufactured from raw text by shifting it one position. That single trick — no labelling bottleneck — is arguably as responsible for the LLM era as the transformer itself. Compare the labelled-data famine in medical imaging, where every training example costs radiologist-hours.
</div>

## The corpus

Frontier models train on trillions of tokens. We need something a laptop can chew through in minutes, which means roughly a **few megabytes of plain text** — and at this scale, the honest choice is **character-level** modelling: our vocabulary will be the set of distinct characters in the file (typically 60–100), not the 50,000-piece token vocabularies of Lesson 4. Every concept transfers unchanged; only the granularity differs.

Any plain-text file works — collected essays, public-domain novels, your own writing. Being who I am, I trained mine on a public-domain classic of medical literature: the 1918 edition of *Gray's Anatomy*, freely available from Project Gutenberg (about 5 MB of glorious Edwardian anatomical prose). Watching a neural network learn to hallucinate confident anatomy is an instructive experience for any clinician — more on that below. Save whatever you choose as `corpus.txt` next to your script.

## The data pipeline

Ten lines. We build the character vocabulary, encode the whole corpus as integers, hold out the last 10% for validation, and write a function that serves random training snippets:

```python
import torch

text = open("corpus.txt", encoding="utf-8").read()
chars = sorted(set(text))
vocab_size = len(chars)                      # typically 60–100 characters
stoi = {c: i for i, c in enumerate(chars)}
itos = {i: c for c, i in stoi.items()}
encode = lambda s: [stoi[c] for c in s]
decode = lambda t: "".join(itos[i] for i in t)

data = torch.tensor(encode(text), dtype=torch.long)
n = int(0.9 * len(data))
train_data, val_data = data[:n], data[n:]    # last 10% never trained on

ctx, batch_size = 256, 64

def get_batch(split):
    d = train_data if split == "train" else val_data
    ix = torch.randint(len(d) - ctx - 1, (batch_size,))
    x = torch.stack([d[i     : i+ctx    ] for i in ix])   # inputs
    y = torch.stack([d[i + 1 : i+ctx + 1] for i in ix])   # same text, shifted by 1
    return x.to(device), y.to(device)
```

Look hard at `get_batch` — it is Figure 1's step ① and the heart of self-supervision. The target `y` is literally the input `x` shifted one character. Because of the causal mask from Lesson 4, position *t* in the model's output only ever saw characters up to *t*, so predicting `y[t]` — the character at *t+1* — is a fair exam, at all 256 positions of all 64 snippets simultaneously. One batch therefore contains 16,384 individual next-character exams.

The held-out 10% deserves emphasis. The model will never take a gradient step on it, which makes it our **external validation cohort**: performance there tells us the model is learning *the language*, not memorising *the file*. Every clinician who has watched a risk score validated only on its derivation cohort knows exactly why this split is non-negotiable.

## The training loop

Bring in the `TinyGPT` from Lesson 4 unchanged, then:

```python
import torch.nn.functional as F

device = ("mps" if torch.backends.mps.is_available()      # Apple Silicon
          else "cuda" if torch.cuda.is_available()        # NVIDIA
          else "cpu")

model = TinyGPT(vocab_size).to(device)     # ~800k parameters at default size
opt = torch.optim.AdamW(model.parameters(), lr=3e-4)

@torch.no_grad()
def estimate_loss(split, iters=50):
    model.eval()
    losses = []
    for _ in range(iters):
        x, y = get_batch(split)
        logits = model(x)
        losses.append(F.cross_entropy(
            logits.view(-1, vocab_size), y.view(-1)).item())
    model.train()
    return sum(losses) / len(losses)

for step in range(5001):
    if step % 500 == 0:
        tr, va = estimate_loss("train"), estimate_loss("val")
        print(f"step {step:5d}   train {tr:.3f}   val {va:.3f}")

    x, y = get_batch("train")
    logits = model(x)                                          # ② forward
    loss = F.cross_entropy(logits.view(-1, vocab_size),        # ③ score
                           y.view(-1))
    opt.zero_grad()
    loss.backward()                                            # ④ gradients
    opt.step()                                                 # ⑤ nudge
```

That's the entire loop — compare it line by line against Figure 1. Two notes for the practitioners:

**The optimizer is AdamW, not raw gradient descent.** It's the same "step downhill" idea from Lesson 2, with two refinements earned by a decade of practice: each parameter gets an adaptive step size based on its recent gradient history, and a slight pull toward zero (weight decay) discourages overfitting. You could train with plain SGD; it would just take longer and land somewhere slightly worse.

**The loss number is interpretable — use that.** Cross-entropy here is the model's average surprise, in units of *nats*, at each true next character. Before training, with ~85 characters all equally likely, expect ln(85) ≈ **4.4**. A model that has learned English character statistics lands around **2.0**; a well-trained one on this corpus reaches **1.4–1.5** on validation. When your step-0 print shows ≈4.4, that's your first sanity check passing: the untrained model is exactly as ignorant as theory predicts.

## Sampling: watching it think out loud

To generate text we run Lesson 4's Figure 1 literally — predict, sample, append, repeat:

```python
@torch.no_grad()
def generate(model, prompt, max_new_tokens=400, temperature=1.0):
    idx = torch.tensor([encode(prompt)], device=device)
    model.eval()
    for _ in range(max_new_tokens):
        logits = model(idx[:, -ctx:])            # crop to context window
        logits = logits[:, -1, :] / temperature  # last position only
        probs = F.softmax(logits, dim=-1)
        nxt = torch.multinomial(probs, num_samples=1)
        idx = torch.cat([idx, nxt], dim=1)
    model.train()
    return decode(idx[0].tolist())
```

Now add `print(generate(model, "The "))` inside the every-500-steps block, run the script, and watch. This is the part I promised. Roughly — your exact output will differ — here is what my Gray's Anatomy run produced:

<div class="sample-box">
<span class="label">step 0 — loss 4.43 — pure noise:</span><br/>
The q)Kf;öJ2và]x9Yt(Q…7zR&amp;fB[wp0ûNnV,ceT!SkAé§m8—D5W&amp;)Hq;;ô
</div>

<div class="sample-box">
<span class="label">step 500 — loss 2.31 — word-shaped noise:</span><br/>
The pertion of the mecle is ativery of the sof the brone and lation, and the extremity of the moth whith the ceparatirs of the
</div>

<div class="sample-box">
<span class="label">step 2000 — loss 1.72 — the corpus's voice emerges:</span><br/>
The muscle is inserted into the outer surface of the humerus, and is supplied by the anterior branches of the artery which descend behind the tendon
</div>

<div class="sample-box">
<span class="label">step 5000 — loss 1.46 — fluent, confident, and frequently wrong:</span><br/>
The internal carotid artery ascends in front of the transverse process of the axis, and divides into two branches, which supply the deep surface of the deltoid and the integument of the back of the neck.
</div>

Sit with that progression for a moment, because it compresses the entire deep-learning story into four snippets. At step 0: uniform randomness. By 500 the model has learned *the statistics of English spelling* — letter frequencies, vowel placement, word lengths — with no idea what a word means. By 2000 it produces real anatomical vocabulary in grammatical arrangements. By 5000 it writes fluent Edwardian anatomical prose that is *anatomically wrong* — that final sample is confident nonsense; the internal carotid does no such thing.

<div class="callout">
⚕️ <strong>And there it is: your first hallucination, bred in captivity.</strong> Nobody "programmed" it to make things up. The model learned to produce text that is <em>statistically shaped like</em> its corpus, and at 800k parameters, statistical shape is all it can afford. Fluency arrives long before fidelity — and fluency is what human readers instinctively use as a proxy for fidelity. Every clinical warning I've written about trusting LLM output traces back to this exact asymmetry, and now you've watched it form from scratch on your own laptop.
</div>

## Reading the loss curves

While samples give you the qualitative story, the two loss numbers you're printing tell the quantitative one:

<figure class="diagram">
<svg viewBox="0 0 720 430" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Training and validation loss curves over training steps">
  <rect x="0" y="0" width="720" height="430" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="34" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">WHAT THE TWO LOSSES TELL YOU</text>

  <!-- axes -->
  <line x1="80" y1="70" x2="80" y2="350" stroke="#2a3f5f" stroke-width="2"/>
  <line x1="80" y1="350" x2="670" y2="350" stroke="#2a3f5f" stroke-width="2"/>
  <text x="52" y="80" fill="#6b82a0" font-family="monospace" font-size="11">4.4</text>
  <text x="52" y="216" fill="#6b82a0" font-family="monospace" font-size="11">2.9</text>
  <text x="52" y="345" fill="#6b82a0" font-family="monospace" font-size="11">1.4</text>
  <text x="375" y="376" text-anchor="middle" fill="#6b82a0" font-family="monospace" font-size="11">training steps →</text>
  <text x="30" y="215" fill="#6b82a0" font-family="monospace" font-size="11" transform="rotate(-90 30 215)">loss (nats)</text>

  <!-- train curve -->
  <path d="M85,78 C160,180 240,280 360,318 C480,344 580,352 665,356" stroke="#00d4f5" stroke-width="2.5" fill="none"/>
  <!-- val curve: follows then flattens/diverges -->
  <path d="M85,78 C160,182 240,285 360,325 C450,340 540,338 665,330" stroke="#f59e0b" stroke-width="2.5" fill="none" stroke-dasharray="7,4"/>

  <!-- annotations -->
  <text x="150" y="150" fill="#c9d6e8" font-family="sans-serif" font-size="11.5">steep early drop:</text>
  <text x="150" y="166" fill="#6b82a0" font-family="sans-serif" font-size="11">spelling statistics are cheap to learn</text>

  <text x="392" y="266" fill="#c9d6e8" font-family="sans-serif" font-size="11.5">long slow middle:</text>
  <text x="392" y="282" fill="#6b82a0" font-family="sans-serif" font-size="11">grammar, vocabulary, style</text>

  <circle cx="560" cy="337" r="5" fill="#f87171"/>
  <text x="470" y="405" fill="#f87171" font-family="sans-serif" font-size="11.5">⚠ curves part company: memorisation begins —</text>
  <text x="470" y="421" fill="#e2a0a0" font-family="sans-serif" font-size="11">train keeps falling, val stalls. Stop here.</text>
  <line x1="560" y1="342" x2="540" y2="396" stroke="#f87171" stroke-width="1.5"/>

  <!-- legend -->
  <rect x="480" y="80" width="200" height="58" rx="8" fill="#111827" stroke="#2a3f5f"/>
  <line x1="495" y1="100" x2="530" y2="100" stroke="#00d4f5" stroke-width="2.5"/>
  <text x="540" y="104" fill="#d8f6fd" font-family="sans-serif" font-size="11.5">train loss (seen data)</text>
  <line x1="495" y1="122" x2="530" y2="122" stroke="#f59e0b" stroke-width="2.5" stroke-dasharray="7,4"/>
  <text x="540" y="126" fill="#fdeccd" font-family="sans-serif" font-size="11.5">val loss (held-out data)</text>
</svg>
<figcaption><strong>Figure 2.</strong> The characteristic shape of a small-model training run. The validation curve is the only one you should ever brag about: it measures generalisation to text the model has never seen. The moment it stops falling while train loss continues down, further training is teaching the model your file, not your language.</figcaption>
</figure>

That divergence point is **overfitting**, and our 800k-parameter model on a 5 MB corpus will hit it eventually — the model is small relative to the data, so it holds off for a while, but it comes. The remedies are the classics: more data, a smaller model, more weight decay, or simply stopping when validation loss bottoms out. If this sounds exactly like the derivation-cohort-versus-validation-cohort discipline of clinical prediction models: yes. It is the same statistics wearing different clothes.

## Practical notes for your run

On timing: with the default settings (4 layers, 128-wide, context 256), a 5,000-step run takes roughly 10–20 minutes on an Apple Silicon Mac (the script auto-selects the `mps` backend) or a modest NVIDIA GPU, and an hour or two on pure CPU. If CPU is all you have, drop `ctx` to 128 and the model to 3 layers — the qualitative arc from noise to sentences survives entirely intact.

On knobs worth turning once it works, in rough order of instructional value: `temperature` in `generate()` (0.5 is cautious and repetitive; 1.5 is creative and unhinged — an intuition worth having, since it's the same parameter you set in every LLM API); the learning rate (try 3e-3 and watch training destabilise — the divergence you'll see is Lesson 2's "overshooting the valley" made vivid); model width and depth (double both and watch validation loss improve — a miniature scaling law on your own hardware); and the corpus itself (swap in a different author; the model's entire personality follows the data — nothing else changed).

The complete script — data pipeline, Lesson 4's model, training loop, sampling, all assembled and commented — is here: **[train_tinygpt.py](/static/train_tinygpt.py)**. Read it top to bottom before running it; it's ~130 lines and there is nothing in it you haven't now met.

## What scaling changes — and what it doesn't

It's worth saying plainly what separates your afternoon's model from a frontier one, because the list is shorter than most people assume: more data (megabytes → tens of trillions of tokens), more parameters (800k → hundreds of billions), subword tokens instead of characters (Lesson 4), longer context, and a few architectural refinements per year of engineering. The training loop you just wrote — batch, forward, cross-entropy, backward, step — is, to a first approximation, *what the big labs run*, distributed across thousands of GPUs for months. The loss-versus-compute curves you sketched by doubling your model's width become, at industrial scale, the **scaling laws** that let labs forecast a model's loss before spending the money to train it.

And one thing scaling does *not* change: the model that comes out of this loop — at any size — is a raw next-token predictor with exactly the confident-fluency-without-fidelity property you bred in your own laptop run. It answers questions by continuing them, sometimes with more questions. Turning that raw material into something that reliably *helps* — that answers, follows instructions, declines gracefully, cites honestly — is a separate act of shaping, performed after pretraining.

## What's next

That shaping is Lesson 6 — [now live](/post/2026-07-11-from-predictor-to-assistant): **post-training** — how a base model becomes an assistant. Instruction tuning, feedback-based refinement, why the same weights can host such different behaviours, and what that pipeline means for the failure modes you'll meet in deployed clinical tools. The raw predictor you trained today is the "before" picture; next time we look at the "after," and at exactly what happens in between.

Until then: run the script. Change the corpus. Break the learning rate on purpose. The point of this lesson was never the 8 MB of weights you'll end up with — it's that "GPT" now names a process you have personally executed, end to end, rather than a product you consume.

*— Neal*

<div class="lesson-banner">
📚 <strong>Continue the series:</strong> all lessons, in order, on the <a href="/lessons">Lessons page</a>.
</div>
