---
title: "Inside the Transformer"
date: 2026-07-10
category: Deep Learning
tags: transformer, attention, GPT, LLM, embeddings, tokens, context window, PyTorch, deep learning
level: Intermediate–Advanced
read_time: 35 min
summary: "Lesson 4 of Learning With Dr Neal. How a language model actually turns a transcript into the next token: tokens and embeddings, why attention was the breakthrough, what a context window physically is — and a complete tiny GPT in PyTorch, small enough to read in one sitting and train on your laptop."
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
📚 <strong>Lessons series — #4.</strong> This lesson sits between <a href="/post/2026-06-19-how-deep-neural-networks-really-work">Lesson 1</a> (what a neural network computes) and <a href="/post/2026-07-10-anatomy-of-an-ai-coding-agent">Lesson 3</a> (what's wrapped around the model to make an agent). Today we open the model itself. The full curriculum lives on the <a href="/lessons">Lessons page</a>.
</div>

# Inside the Transformer

At the end of the last lesson I promised we'd close the gap in the middle of our stack. At the bottom (Lessons 1–2): neurons, weights, gradient descent. At the top (Lesson 3): the agent loop, tools, permissions. Between them sits the machine that does the actual thinking — the thing that receives a transcript and produces, of all the words it could say next, the right one.

That machine is the **transformer**, and it has been the architecture behind essentially every frontier language model since 2017. This lesson explains it the way I wish someone had explained it to me: not as a wall of matrix algebra, but as a small number of design decisions, each solving a specific problem — ending with working PyTorch code for a complete miniature GPT that you can read in one sitting.

<div class="audio-section">
  🎧 <strong>Listen to this post:</strong> How transformers predict the next token — the audio companion to this lesson.<br/><br/>
  <audio controls style="width:100%; margin-top:0.4em;">
    <source src="/static/How_Transformers_predict_the_next_token.m4a" type="audio/mp4">
    <a href="/static/How_Transformers_predict_the_next_token.m4a">Download the audio</a>
  </audio>
</div>

<div class="audio-section">
  🎬 <strong>Watch the video overview:</strong> Inside the Transformer in nine minutes — the visual companion to this lesson.<br/><br/>
  <video controls preload="metadata" style="width:100%; margin-top:0.4em; border-radius:6px;">
    <source src="/static/Inside_the_Transformer.mp4" type="video/mp4">
    <a href="/static/Inside_the_Transformer.mp4">Download the video</a>
  </video>
</div>

## One job: the next token

Strip away the chat interface and an LLM has exactly one skill. Given a sequence of tokens, it outputs a probability for *every token in its vocabulary* being the next one. That's it. That's the whole job.

Everything else is repetition. To generate a paragraph, the system samples one token from that probability distribution, appends it to the sequence, and asks again. And again. A thousand-word answer is a thousand spins of this wheel:

<figure class="diagram">
<svg viewBox="0 0 720 400" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The autoregressive generation loop">
  <defs>
    <marker id="tarrC" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L8,4.5 L0,9 z" fill="#00d4f5"/>
    </marker>
    <marker id="tarrA" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L8,4.5 L0,9 z" fill="#f59e0b"/>
    </marker>
  </defs>
  <rect x="0" y="0" width="720" height="400" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="34" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">ONE TOKEN AT A TIME</text>

  <!-- transcript -->
  <rect x="30" y="80" width="230" height="70" rx="10" fill="#111827" stroke="#a78bfa" stroke-width="1.5"/>
  <text x="145" y="107" text-anchor="middle" fill="#e8e3fa" font-family="sans-serif" font-size="13" font-weight="bold">The sequence so far</text>
  <text x="145" y="130" text-anchor="middle" fill="#9f8fd0" font-family="monospace" font-size="11">"The patient was given"</text>

  <!-- transformer -->
  <rect x="310" y="72" width="150" height="86" rx="10" fill="#0a4a5c" stroke="#00d4f5" stroke-width="2"/>
  <text x="385" y="105" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="14" font-weight="bold">Transformer</text>
  <text x="385" y="126" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="10.5">one forward pass</text>

  <!-- probability bars -->
  <rect x="510" y="60" width="180" height="150" rx="10" fill="#111827" stroke="#2a3f5f" stroke-width="1.5"/>
  <text x="600" y="82" text-anchor="middle" fill="#c9d6e8" font-family="sans-serif" font-size="11.5" font-weight="bold">P(next token)</text>
  <rect x="525" y="94"  width="118" height="13" rx="3" fill="#10b981"/>
  <text x="648" y="105" fill="#d3f5e6" font-family="monospace" font-size="10">aspirin .38</text>
  <rect x="525" y="114" width="66" height="13" rx="3" fill="#00d4f5"/>
  <text x="596" y="125" fill="#d8f6fd" font-family="monospace" font-size="10">a .21</text>
  <rect x="525" y="134" width="44" height="13" rx="3" fill="#f59e0b"/>
  <text x="574" y="145" fill="#fdeccd" font-family="monospace" font-size="10">two .14</text>
  <rect x="525" y="154" width="28" height="13" rx="3" fill="#a78bfa"/>
  <text x="558" y="165" fill="#e8e3fa" font-family="monospace" font-size="10">iv .09</text>
  <rect x="525" y="174" width="14" height="13" rx="3" fill="#6b82a0"/>
  <text x="544" y="185" fill="#c9d6e8" font-family="monospace" font-size="10">… the rest</text>

  <!-- arrows -->
  <path d="M260,115 L302,115" stroke="#00d4f5" stroke-width="2" marker-end="url(#tarrC)"/>
  <path d="M460,115 L502,115" stroke="#00d4f5" stroke-width="2" marker-end="url(#tarrC)"/>

  <!-- sample + append loop -->
  <rect x="470" y="250" width="180" height="56" rx="10" fill="#4a3000" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="560" y="273" text-anchor="middle" fill="#fdeccd" font-family="sans-serif" font-size="12.5" font-weight="bold">Sample one token</text>
  <text x="560" y="292" text-anchor="middle" fill="#f0c987" font-family="monospace" font-size="11">→ "aspirin"</text>

  <path d="M600,210 L565,242" stroke="#f59e0b" stroke-width="2" marker-end="url(#tarrA)"/>
  <path d="M470,278 Q145,278 145,158" stroke="#f59e0b" stroke-width="2" fill="none" marker-end="url(#tarrA)"/>
  <text x="255" y="266" fill="#f59e0b" font-family="sans-serif" font-size="11">append &amp; repeat — every single word, forever</text>

  <text x="360" y="374" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11.5">"Generating text" is this loop. Nothing more. The intelligence lives inside the blue box.</text>
</svg>
<figcaption><strong>Figure 1.</strong> Autoregressive generation. The model never plans a paragraph; it emits one probability distribution, a token is drawn from it, and the extended sequence goes straight back in. (How <em>randomly</em> the draw is made is the "temperature" knob you may have met in API settings.)</figcaption>
</figure>

Hold on to this framing, because it demystifies half the folklore about LLMs. The model has no plan, no draft, no lookahead buffer. Any apparent long-range structure in its output — an argument that builds, code that compiles, a differential that narrows — must somehow be computed *fresh at every step*, from nothing but the transcript so far. The rest of this lesson is about the machinery that makes that possible.

## From text to numbers

Neural networks eat vectors, not words. So before anything interesting happens, text goes through two conversions.

**Tokenisation.** The raw string is chopped into *tokens* — chunks from a fixed vocabulary, typically 50,000–200,000 entries learned from data. Common words get their own token; rarer words are assembled from pieces (`hyponatraemia` might become `hypo|nat|ra|emia`). This is why LLMs are notoriously shaky at counting letters: the model never sees letters, only chunk IDs.

**Embedding.** Each token ID indexes into a big lookup table and retrieves a learned vector — several hundred to several thousand numbers. These *embeddings* are learned during training, and they end up encoding meaning as geometry: tokens used in similar contexts drift toward each other in the vector space. You met this idea in Lesson 1; here it's the front door of the whole model.

One more ingredient: the model needs to know *where* each token sits, because "dog bites man" and "man bites dog" contain the same tokens. So a **position signal** is mixed into each embedding — in the simplest scheme, a second lookup table indexed by position 0, 1, 2, …

<figure class="diagram">
<svg viewBox="0 0 720 470" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Pipeline from text to next-token probabilities">
  <defs>
    <marker id="parr" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L8,4.5 L0,9 z" fill="#6b82a0"/>
    </marker>
  </defs>
  <rect x="0" y="0" width="720" height="470" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="34" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">THE JOURNEY OF A PROMPT</text>

  <!-- 1 text -->
  <rect x="60" y="58" width="600" height="44" rx="8" fill="#111827" stroke="#a78bfa" stroke-width="1.5"/>
  <text x="80" y="85" fill="#e8e3fa" font-family="sans-serif" font-size="12.5"><tspan font-weight="bold">Text</tspan>   "the drug lowered blood pressure"</text>

  <path d="M360,102 L360,118" stroke="#6b82a0" stroke-width="2" marker-end="url(#parr)"/>
  <text x="380" y="116" fill="#6b82a0" font-family="sans-serif" font-size="10.5">tokenise</text>

  <!-- 2 tokens -->
  <rect x="60" y="122" width="600" height="44" rx="8" fill="#111827" stroke="#00d4f5" stroke-width="1.5"/>
  <text x="80" y="149" fill="#d8f6fd" font-family="sans-serif" font-size="12.5"><tspan font-weight="bold">Token IDs</tspan>   [464, 2563, 17788, 2910, 3833]</text>

  <path d="M360,166 L360,182" stroke="#6b82a0" stroke-width="2" marker-end="url(#parr)"/>
  <text x="380" y="180" fill="#6b82a0" font-family="sans-serif" font-size="10.5">embed + add position</text>

  <!-- 3 vectors -->
  <rect x="60" y="186" width="600" height="44" rx="8" fill="#111827" stroke="#10b981" stroke-width="1.5"/>
  <text x="80" y="213" fill="#d3f5e6" font-family="sans-serif" font-size="12.5"><tspan font-weight="bold">Vectors</tspan>   5 tokens × d numbers each — meaning as geometry</text>

  <path d="M360,230 L360,246" stroke="#6b82a0" stroke-width="2" marker-end="url(#parr)"/>

  <!-- 4 blocks -->
  <rect x="60" y="250" width="600" height="98" rx="8" fill="#0a4a5c" stroke="#00d4f5" stroke-width="2"/>
  <text x="80" y="277" fill="#d8f6fd" font-family="sans-serif" font-size="12.5" font-weight="bold">A stack of identical transformer blocks (×N)</text>
  <text x="80" y="298" fill="#9fdcec" font-family="sans-serif" font-size="11.5">Each block: every token gathers context from earlier tokens (attention),</text>
  <text x="80" y="316" fill="#9fdcec" font-family="sans-serif" font-size="11.5">then each token thinks on its own (a small MLP). Repeat N times —</text>
  <text x="80" y="334" fill="#9fdcec" font-family="sans-serif" font-size="11.5">GPT-2 sized models: N≈12–48. Frontier models: N in the dozens-to-hundreds.</text>

  <path d="M360,348 L360,364" stroke="#6b82a0" stroke-width="2" marker-end="url(#parr)"/>
  <text x="380" y="362" fill="#6b82a0" font-family="sans-serif" font-size="10.5">project to vocabulary</text>

  <!-- 5 logits -->
  <rect x="60" y="368" width="600" height="44" rx="8" fill="#111827" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="80" y="395" fill="#fdeccd" font-family="sans-serif" font-size="12.5"><tspan font-weight="bold">Scores → softmax → probabilities</tspan>   one number per vocabulary entry</text>

  <text x="360" y="444" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11.5">Every stage is differentiable — so the gradient descent of Lessons 1–2 trains the whole pipe end to end.</text>
</svg>
<figcaption><strong>Figure 2.</strong> The full forward pass. Note there is nothing exotic at either end — lookup tables at the entrance, one linear layer plus a softmax at the exit. The novelty is entirely in the middle stack.</figcaption>
</figure>

## The breakthrough: attention

Here's the problem the middle stack has to solve. Consider the sequence:

> *"the drug lowered blood pressure because **it** …"*

To predict what follows "it", the model must know what "it" refers to — and that information lives four tokens back, in "drug". Meaning in language is *relational*: a token's true significance depends on other tokens, sometimes hundreds of words away, in patterns that change from sentence to sentence.

Older architectures handled this badly. Recurrent networks read left to right, compressing everything seen so far into one fixed-size summary vector — by the time you're 500 tokens in, the details of token 12 have been squeezed to mush. The field needed a mechanism where any token could consult *any* earlier token directly, with the relevance decided dynamically by content.

That mechanism is **attention**, and the cleanest way to understand it is as a soft database lookup that every token performs simultaneously.

Each token's vector is projected into three roles:

- a **query** — "here's what I'm looking for"
- a **key** — "here's what I contain, as an advertisement"
- a **value** — "here's what I'll hand over if you pick me"

Every token's query is compared (dot product) against every earlier token's key. Good matches score high. The scores pass through a softmax to become weights summing to 1, and each token receives the weighted average of the earlier tokens' *values*. The token "it" emits a query shaped roughly like "recent singular noun, thing that can act"; the key of "drug" matches it far better than the key of "because"; so the value flowing back to "it" is dominated by drug-ness.

<figure class="diagram">
<svg viewBox="0 0 720 430" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Attention as a content-based lookup">
  <rect x="0" y="0" width="720" height="430" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="34" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">ATTENTION: "it" ASKS THE SENTENCE A QUESTION</text>

  <!-- token row -->
  <g font-family="monospace" font-size="13">
    <rect x="38"  y="300" width="64" height="40" rx="8" fill="#111827" stroke="#2a3f5f"/><text x="70"  y="325" text-anchor="middle" fill="#c9d6e8">the</text>
    <rect x="112" y="300" width="64" height="40" rx="8" fill="#053d28" stroke="#10b981" stroke-width="2"/><text x="144" y="325" text-anchor="middle" fill="#d3f5e6" font-weight="bold">drug</text>
    <rect x="186" y="300" width="84" height="40" rx="8" fill="#111827" stroke="#2a3f5f"/><text x="228" y="325" text-anchor="middle" fill="#c9d6e8">lowered</text>
    <rect x="280" y="300" width="64" height="40" rx="8" fill="#111827" stroke="#2a3f5f"/><text x="312" y="325" text-anchor="middle" fill="#c9d6e8">blood</text>
    <rect x="354" y="300" width="94" height="40" rx="8" fill="#111827" stroke="#2a3f5f"/><text x="401" y="325" text-anchor="middle" fill="#c9d6e8">pressure</text>
    <rect x="458" y="300" width="84" height="40" rx="8" fill="#111827" stroke="#2a3f5f"/><text x="500" y="325" text-anchor="middle" fill="#c9d6e8">because</text>
    <rect x="552" y="300" width="54" height="40" rx="8" fill="#4a3000" stroke="#f59e0b" stroke-width="2"/><text x="579" y="325" text-anchor="middle" fill="#fdeccd" font-weight="bold">it</text>
  </g>

  <!-- attention arcs from "it" -->
  <path d="M579,300 Q360,90 144,300"  stroke="#10b981" stroke-width="6" fill="none" opacity="0.9"/>
  <path d="M579,300 Q400,170 228,300" stroke="#00d4f5" stroke-width="2.5" fill="none" opacity="0.6"/>
  <path d="M579,300 Q470,220 401,300" stroke="#00d4f5" stroke-width="1.5" fill="none" opacity="0.45"/>
  <path d="M579,300 Q545,255 500,300" stroke="#00d4f5" stroke-width="1" fill="none" opacity="0.35"/>

  <!-- weights labels -->
  <text x="330" y="120" text-anchor="middle" fill="#10b981" font-family="monospace" font-size="13" font-weight="bold">weight 0.71 → "drug"</text>
  <text x="352" y="185" text-anchor="middle" fill="#00d4f5" font-family="monospace" font-size="11.5">0.14 → "lowered"</text>
  <text x="460" y="238" text-anchor="middle" fill="#00d4f5" font-family="monospace" font-size="11">0.08 → "pressure"</text>
  <text x="548" y="272" text-anchor="middle" fill="#00d4f5" font-family="monospace" font-size="10.5">0.04</text>

  <!-- QKV legend -->
  <rect x="38" y="366" width="644" height="44" rx="8" fill="#111827" stroke="#2a3f5f"/>
  <text x="360" y="384" text-anchor="middle" fill="#c9d6e8" font-family="sans-serif" font-size="11.5"><tspan fill="#f59e0b" font-weight="bold">query</tspan> — what "it" is looking for · <tspan fill="#10b981" font-weight="bold">key</tspan> — what each token advertises · <tspan fill="#a78bfa" font-weight="bold">value</tspan> — what a chosen token hands over</text>
  <text x="360" y="402" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11">Weights come from query·key matches, softmaxed to sum to 1. "it" receives 0.71 × value(drug) + 0.14 × value(lowered) + …</text>
</svg>
<figcaption><strong>Figure 3.</strong> One attention operation, seen from the token "it". Arc thickness = attention weight. Crucially, these weights are not stored anywhere — they are recomputed from the actual content of the sentence, every pass. Swap "drug" for "diet" and the arcs redraw themselves.</figcaption>
</figure>

Two properties make this the breakthrough it was.

**It's content-addressed, not position-addressed.** The lookup asks "who *matches* this query?", not "who is 4 slots back?". The same weights machinery handles pronoun resolution, subject–verb agreement, matching a closing bracket in code, and retrieving a fact stated three paragraphs ago — without being told which of those tasks it's doing.

**It's completely parallel.** Every token computes its lookup simultaneously — one big matrix multiplication, no left-to-right crawl. This is what let transformers train on orders of magnitude more data than recurrent networks: the architecture finally matched what GPUs are good at.

In code, the whole mechanism is about a dozen lines. This runs as written:

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class AttentionHead(nn.Module):
    def __init__(self, d_model, d_head):
        super().__init__()
        self.q = nn.Linear(d_model, d_head, bias=False)
        self.k = nn.Linear(d_model, d_head, bias=False)
        self.v = nn.Linear(d_model, d_head, bias=False)

    def forward(self, x):                       # x: (batch, tokens, d_model)
        B, T, _ = x.shape
        q, k, v = self.q(x), self.k(x), self.v(x)
        scores = q @ k.transpose(-2, -1) / k.shape[-1] ** 0.5   # (B, T, T)
        mask = torch.tril(torch.ones(T, T, device=x.device)).bool()
        scores = scores.masked_fill(~mask, float("-inf"))       # no peeking ahead
        weights = F.softmax(scores, dim=-1)     # each row sums to 1
        return weights @ v                      # weighted mix of values
```

That `masked_fill` line deserves a highlight: it blanks out the upper triangle of the score matrix so that no token can attend to tokens *after* itself. During training the model predicts every position's next token simultaneously, and the mask is what stops it cheating by reading the answer. This is the **causal mask**, and it's why this family of models is called *autoregressive*.

<div class="callout">
⚕️ <strong>The consult analogy.</strong> Attention is a ward round where every patient simultaneously broadcasts a question ("query"), every chart on the ward advertises its contents ("key"), and each patient receives a summary weighted by relevance ("value"). No one reads every chart cover to cover; relevance is negotiated by content. And like any triage system, it can misfire — when a model confidently attributes a statement to the wrong antecedent, you are often watching an attention head pick the wrong chart.
</div>

## Heads, MLPs, and the residual stream

A real transformer block adds three refinements to the bare mechanism above.

**Multiple heads.** Instead of one attention operation with big vectors, run 8–100 smaller ones in parallel — each with its own Q/K/V projections — and concatenate the results. Each *head* is free to specialise: trained models reliably develop heads for syntax, heads that track quoted speech, heads that find the previous occurrence of the current token, heads for bracket matching in code. Interpretability research — the field that dissects trained models — finds these specialisations without being told to look for them, the way histology reveals cell types.

**A per-token MLP.** Attention moves information *between* tokens, but does little computation on it. So each block follows attention with a small two-layer network — the plain feed-forward kind from Lesson 1 — applied to each token independently. The rhythm of a block is: *communicate, then compute*. Gather what you need from the ward, then go away and think about it. Notably, the MLP is where most of a model's parameters live — roughly two-thirds — and current evidence suggests it acts substantially as the model's learned key-value store of facts.

**The residual stream.** Each sub-layer's output is *added* to its input, never substituted for it. You can picture each token as owning a running vector — a chart, if you like — that flows up through the stack, with every attention head and MLP reading from it and writing small annotations back onto it:

<figure class="diagram">
<svg viewBox="0 0 720 480" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="One transformer block with the residual stream">
  <defs>
    <marker id="rarr" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L8,4.5 L0,9 z" fill="#a78bfa"/>
    </marker>
    <marker id="rarrG" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L8,4.5 L0,9 z" fill="#10b981"/>
    </marker>
  </defs>
  <rect x="0" y="0" width="720" height="480" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="34" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">ONE BLOCK: COMMUNICATE, THEN COMPUTE</text>

  <!-- residual stream: broad vertical highway -->
  <rect x="120" y="60" width="90" height="380" rx="14" fill="#2e1e5e" opacity="0.55"/>
  <text x="165" y="86" text-anchor="middle" fill="#c9b8f5" font-family="sans-serif" font-size="11" font-weight="bold">residual</text>
  <text x="165" y="102" text-anchor="middle" fill="#c9b8f5" font-family="sans-serif" font-size="11" font-weight="bold">stream</text>
  <path d="M165,115 L165,425" stroke="#a78bfa" stroke-width="3" marker-end="url(#rarr)"/>

  <!-- attention module -->
  <rect x="330" y="120" width="330" height="96" rx="10" fill="#0a4a5c" stroke="#00d4f5" stroke-width="2"/>
  <text x="495" y="148" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="13.5" font-weight="bold">Multi-head attention</text>
  <text x="495" y="170" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="11.5">each head: its own Q/K/V lookup</text>
  <text x="495" y="188" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="11.5">moves information <tspan font-style="italic">between</tspan> tokens</text>

  <!-- mlp module -->
  <rect x="330" y="290" width="330" height="96" rx="10" fill="#053d28" stroke="#10b981" stroke-width="2"/>
  <text x="495" y="318" text-anchor="middle" fill="#d3f5e6" font-family="sans-serif" font-size="13.5" font-weight="bold">MLP (feed-forward)</text>
  <text x="495" y="340" text-anchor="middle" fill="#8fd8b8" font-family="sans-serif" font-size="11.5">two linear layers, applied per token</text>
  <text x="495" y="358" text-anchor="middle" fill="#8fd8b8" font-family="sans-serif" font-size="11.5">computes <tspan font-style="italic">within</tspan> each token · most parameters live here</text>

  <!-- read / write arrows: attention -->
  <path d="M210,140 Q270,140 322,150" stroke="#00d4f5" stroke-width="2" fill="none" marker-end="url(#rarr)"/>
  <text x="262" y="130" fill="#00d4f5" font-family="sans-serif" font-size="10.5">read (normalised)</text>
  <path d="M330,196 Q260,206 214,206" stroke="#00d4f5" stroke-width="2" fill="none" marker-end="url(#rarr)"/>
  <text x="268" y="228" fill="#00d4f5" font-family="sans-serif" font-size="10.5">write: add result back</text>

  <!-- read / write arrows: mlp -->
  <path d="M210,310 Q270,310 322,320" stroke="#10b981" stroke-width="2" fill="none" marker-end="url(#rarrG)"/>
  <text x="262" y="300" fill="#10b981" font-family="sans-serif" font-size="10.5">read (normalised)</text>
  <path d="M330,366 Q260,376 214,376" stroke="#10b981" stroke-width="2" fill="none" marker-end="url(#rarrG)"/>
  <text x="268" y="398" fill="#10b981" font-family="sans-serif" font-size="10.5">write: add result back</text>

  <text x="440" y="446" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11.5">Nothing overwrites the stream — modules only add to it. Stack N of these blocks and the</text>
  <text x="440" y="464" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11.5">chart accumulates progressively richer annotations before the final prediction is read off.</text>
</svg>
<figcaption><strong>Figure 4.</strong> The residual view of a transformer block. Each module reads a normalised copy of the stream and adds its contribution back. Because addition is order-of-magnitude gentle, gradients flow cleanly through even 100-block stacks — the same trick that made very deep vision networks trainable.</figcaption>
</figure>

(The "normalised" in Figure 4 is **layer normalisation** — each read is rescaled to a standard spread before use. It's the same statistical hygiene as standardising lab values before feeding them to a risk model, and it matters for training stability, not for understanding.)

<div class="keyidea">
💡 <strong>Key idea.</strong> A transformer is just this block, photocopied N times, between an embedding table and an output projection. There is no other structural idea in it. GPT-2 and the largest frontier models differ in width, depth, data, and training refinement — not in kind.
</div>

## What a context window physically is

Now we can give a concrete answer to a question I promised in Lesson 3, where we saw the agent loop "compact" its transcript when it grew too long.

The **context window** is the maximum number of tokens the model can process in one forward pass. It is a physical quantity, set by two things. First, the position signal: the model has only learned to represent positions up to some maximum. Second — and this is the one that costs money — the attention score matrix in every head of every block has one entry per *pair* of tokens. Double the sequence length and you quadruple the attention computation, and quadruple the memory holding those keys and values.

That quadratic term is why context windows are a headline specification, why long conversations get slow and expensive, and why the agent loop from Lesson 3 summarises old turns rather than keeping everything verbatim. When your coding agent "compacts" the transcript, it is managing exactly this budget.

It also explains something subtler: within its window, the model's recall is *direct* — attention can reach token 12 from token 5,000 in one hop, with no degradation by distance. Nothing like human memory decay applies inside the window; everything is equally available if some attention head chooses to look at it. Outside the window, recall is exactly zero. The cliff is absolute — which is why agents need the memory files we met in Lesson 3.

## A complete tiny GPT

Time to keep the promise: a full GPT-style model, small enough to read in one sitting. This is a real, runnable PyTorch module — embeddings, blocks, the lot:

```python
import torch
import torch.nn as nn

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
        x = x + attn_out                # write attention result onto the stream
        x = x + self.mlp(self.ln2(x))   # write MLP result onto the stream
        return x

class TinyGPT(nn.Module):
    def __init__(self, vocab_size, d_model=128, n_heads=4, n_layers=4, ctx=256):
        super().__init__()
        self.tok_emb = nn.Embedding(vocab_size, d_model)   # what each token means
        self.pos_emb = nn.Embedding(ctx, d_model)          # where each token sits
        self.blocks  = nn.Sequential(*[Block(d_model, n_heads)
                                       for _ in range(n_layers)])
        self.ln_out  = nn.LayerNorm(d_model)
        self.head    = nn.Linear(d_model, vocab_size)      # scores over vocabulary

    def forward(self, idx):             # idx: (batch, tokens) of integer IDs
        B, T = idx.shape
        pos = torch.arange(T, device=idx.device)
        x = self.tok_emb(idx) + self.pos_emb(pos)          # Figure 2, stages 2–3
        x = self.blocks(x)                                 # Figure 2, stage 4
        return self.head(self.ln_out(x))                   # logits: (B, T, vocab)
```

Sixty lines, and it is not a toy in any structural sense. Scale `d_model` to 12,288, `n_heads` to 96, `n_layers` to 96, `ctx` into the hundreds of thousands, train it on a large slice of the internet, and you have sketched a frontier base model. The recipe you'd use to train it is the one you already own: cross-entropy loss on next-token prediction, backpropagation, gradient descent — Lessons 1 and 2, at industrial scale.

Line up the pieces against Figure 2 and notice how little is left unexplained: `tok_emb` and `pos_emb` are the lookup tables; each `Block` is Figure 4; the causal mask is Figure 3's "earlier tokens only" rule; `head` produces the scores that softmax turns into Figure 1's probability bars.

<div class="callout">
⚠️ <strong>One honest caveat.</strong> Knowing the architecture is not the same as knowing <em>what the trained model computes</em>. The blueprint above tells you where information <em>can</em> flow; which circuits actually form when you train it on a trillion tokens is an open research question — the province of interpretability work, which is still closer to anatomy-by-dissection than to physiology. Keep that humility; it will serve you when someone claims to know exactly "what the model is thinking."
</div>

## From next-token predictor to assistant

A short bridge, because the gap puzzles many newcomers: how does "predict the next token of internet text" become the helpful assistant in your terminal?

In stages. **Pretraining** produces the raw predictor above — call it a base model. Prompt a base model with a question and it may answer, or may continue with *nine more questions*, because that's a plausible continuation of text containing a question. **Post-training** then reshapes the distribution: the model is further trained on demonstration conversations, and refined against feedback signals, until "continue the transcript" and "respond helpfully" become the same thing. The architecture never changes — same blocks, same attention — only the weights move. The chat format itself is just more tokens: special markers delimiting who said what, exactly like the transcript the agent loop of Lesson 3 maintains.

That's the full stack, connected: gradient descent (Lessons 1–2) trains the transformer (this lesson), whose next-token interface is wrapped by the agent loop (Lesson 3) — turtles all the way down, except every turtle is now one you've met.

## What's next

The obvious move — and the next lesson — is to stop reading and *train one*. We'll take the `TinyGPT` above, feed it a corpus small enough for a laptop, write the training loop with our own hands, and watch generated text evolve from noise, to word-shaped noise, to sentences. There is no better calibration for your intuitions about what these models are than watching one condense out of randomness in front of you.

Until then, a self-test: next time you use an LLM, watch the streamed reply and try to see it as Figure 1 — thousands of forward passes, each one Figure 2, each block Figure 4, every token consulting the transcript by Figure 3. Once you can hold that picture, the word "transformer" stops being a brand name and becomes a machine you could sketch on a napkin.

*— Neal*

<div class="lesson-banner">
📚 <strong>Continue the series:</strong> all lessons, in order, on the <a href="/lessons">Lessons page</a>.
</div>
