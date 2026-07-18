---
title: "Reading the Room: The Idea at the Heart of Every Language Model"
date: 2026-07-19
category: Deep Learning
tags: attention, self-attention, query key value, transformers, context, LLM, softmax, causal mask, foundations
level: Intermediate
read_time: 40 min
summary: "Chapter Three of a ground-up account of how large language models work. In the last chapter we left every token stranded — rich with meaning but frozen, wearing the same face in every sentence. This chapter builds the single mechanism that lets a token turn its head, look at the words around it, and become a different thing in every context. It is called attention, it is the beating heart of every modern language model, and we are going to derive it from nothing."
featured: false
---

<style>
.chapter-banner {
  font-size: 0.85em;
  background: linear-gradient(135deg, #1a237e 0%, #283593 100%);
  color: white;
  padding: 1.2em 1.6em;
  border-radius: 8px;
  margin: 1.5em 0;
  line-height: 1.6;
}
.chapter-banner a { color: #90caf9; font-weight: bold; }
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
.tokrow {
  font-size: 0.82em;
  background: #0d1117;
  border: 1px solid #1e2d45;
  border-radius: 6px;
  padding: 0.9em 1.2em;
  margin: 1em 0;
  font-family: 'JetBrains Mono', monospace;
  color: #c9d6e8;
  line-height: 2.0;
}
figure.diagram { margin: 2em 0; text-align: center; }
figure.diagram svg { max-width: 100%; height: auto; }
figure.diagram figcaption {
  font-size: 0.8em; color: #6b82a0; margin-top: 0.6em; text-align: left;
}
</style>

<div class="chapter-banner">
📖 <strong>Chapter Three of a ground-up account of how large language models work.</strong> <a href="/post/2026-07-17-the-grain-of-language">Chapter One</a> turned text into tokens; <a href="/post/2026-07-18-the-prediction-game">Chapter Two</a> gave each token a place in a space of meaning — but a frozen place, the same in every sentence. We ended on a single unsolved problem: the word “bank” cannot be both a riverside and a savings institution while wearing one fixed vector. This chapter solves it, and in solving it builds the mechanism the whole field is named after.
</div>

# Reading the Room: The Idea at the Heart of Every Language Model

<nav style="font-size:0.8em; background:#0d1117; border:1px solid #1e2d45; border-left:4px solid #00d4f5; border-radius:0 8px 8px 0; padding:0.9em 1.3em; margin:1.6em 0; line-height:1.95;">
<div style="color:#00d4f5; font-family:'JetBrains Mono',monospace; font-size:0.86em; letter-spacing:0.06em; margin-bottom:0.5em;">📚 HOW AN LLM WORKS · CONTENTS</div>
<span style="color:#6b82a0;">1.</span> <a href="/post/2026-07-17-the-grain-of-language">The Grain of Language</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">2.</span> <a href="/post/2026-07-18-the-prediction-game">The Prediction Game</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">3.</span> <strong style="color:#f59e0b;">Reading the Room</strong> &nbsp;·&nbsp;
<span style="color:#6b82a0;">4.</span> <a href="/post/2026-07-20-the-tower">The Tower</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">5.</span> <a href="/post/2026-07-21-how-noise-becomes-knowledge">How Noise Becomes Knowledge</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">6.</span> <a href="/post/2026-07-22-manners-for-a-mind">Manners for a Mind</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">7.</span> <a href="/post/2026-07-23-meaning-you-can-search">Meaning You Can Search</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">8.</span> <a href="/post/2026-07-24-the-agent">The Agent</a>

<div style="margin-top:0.6em; padding-top:0.5em; border-top:1px solid #1e2d45;"><a href="/static/How_an_LLM_Works.pdf"><img src="/static/book_cover_icon.png" alt="How an LLM Works — book cover" style="height:2.8em; vertical-align:middle; border-radius:2px; box-shadow:0 1px 5px rgba(0,0,0,0.55); margin-right:0.55em;"></a><a href="/static/How_an_LLM_Works.pdf" style="color:#f59e0b; font-weight:bold;">Download all eight chapters as a PDF book</a> <span style="color:#6b82a0;">— linked contents, ~66 pages</span></div>
</nav>

Let me put the last chapter's unfinished business back on the table, because everything here grows out of it.

We had given every token a vector — a location in a vast space where nearness means similarity of meaning. It was a real achievement: the model could now generalise, treating `ramipril` sensibly on first sight because it lives near `lisinopril`. But the vector was *fixed*. The embedding table hands over the same coordinates for `bank` whether the sentence is about a river or a cheque. And I argued that this is fatal, because meaning in language is not a property of words in isolation. It is a property of words *in company*. The single most important token for the sense of a sentence often arrives wearing a blank mask, and the mask is identical in situations that mean opposite things.

So the requirement is clear, even before we know how to meet it. Each token must be allowed to *look at the other tokens around it* and *update its own representation in light of what it finds*. The `bank` sitting near `river` and `current` should end up shaded toward riverside; the `bank` sitting near `deposited` and `cheque` should end up shaded toward finance. Same starting vector, two different destinations, and the difference decided entirely by the company each keeps.

The mechanism that does this is called **attention**, and it is, without exaggeration, the idea that made modern language models possible. Everything before it — tokenization, embeddings — is preparation. Everything after it is elaboration. This is the hinge. So we are going to build it slowly, from the ground, and I promise that by the end it will feel not clever but *inevitable* — the obvious thing to want, arrived at by asking a sequence of reasonable questions.

## Part I — The naive idea, and why it is not enough

Let us start with the simplest possible attempt, because its failure teaches us exactly what we really need.

A token must incorporate information from its neighbours. The crudest way to do that: just *average* the vectors of all the tokens in the sentence and mix a little of that average back into each token. Now every token knows, vaguely, "what kind of sentence am I in." The `bank` in the river sentence would pick up a little riverside flavour simply because `river` and `current` are in the average.

It is not a stupid idea. It is just badly undiscriminating. An average treats every neighbour as equally relevant. But when `bank` is trying to work out which sense it is, `river` is enormously relevant and the word `the` is almost totally irrelevant, and a flat average drowns the signal in the noise. What we actually want is a *weighted* average — one where `bank` leans heavily on `river`, glances at `current`, and all but ignores `the`.

Which raises the only question that matters: **where do the weights come from?** They cannot be fixed in advance, because which words matter depends entirely on the sentence. In "the bank of the river" the relevant partner is four words away; in "he robbed a bank" it is two words away and a completely different word. The weights have to be computed *on the fly*, from the actual content of the tokens involved. A token has to be able to look out at the sentence and decide, for itself, *this one matters to me, that one does not* — and it has to make that decision based on meaning, not position.

<div class="keyidea">
💡 <strong>The whole problem, in one sentence.</strong> Each token needs to compute, for every other token, a <em>relevance weight</em> — how much should I let this one influence me? — where the weight depends on the <em>content</em> of both tokens, and then take a weighted average of the others accordingly. Attention is nothing more than a specific, learnable, beautifully parallel way of doing exactly this. The rest of this chapter is just filling in the "specific."
</div>

## Part II — Three questions every token learns to ask

Here is the move that turns the vague wish above into a concrete mechanism, and it is genuinely elegant. To decide how much token A should attend to token B, we let each token play up to three roles, and we build each role out of the token's vector using a small learned transformation.

Think of it as each token being able to ask and answer three questions:

- A **query** — *"what am I looking for?"* This is token A's advertisement of what would be relevant to it. The `bank`-token's query might, loosely, encode "I'm an ambiguous noun; I'm looking for something that disambiguates me — a body of water, or money."
- A **key** — *"what do I offer?"* This is each token's advertisement of what it contains, phrased so that a matching query will recognise it. The `river`-token's key encodes "I am about water, geography, nature."
- A **value** — *"what will I actually hand over if you attend to me?"* This is the information a token contributes once it has been selected — the payload.

Each of these three is produced from the token's embedding by its own learned projection — three different "views" of the same underlying vector, each shaped during training to be good at its job.

<figure class="diagram">
<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A single token vector is projected into three roles: query, key, and value">
  <defs><marker id="qa1" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9 z" fill="#6b82a0"/></marker></defs>
  <rect x="0" y="0" width="720" height="360" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="32" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">THREE VIEWS OF ONE TOKEN</text>

  <!-- token vector -->
  <rect x="270" y="60" width="180" height="52" rx="10" fill="#2e1e5e" stroke="#a78bfa" stroke-width="2"/>
  <text x="360" y="82" text-anchor="middle" fill="#e8e3fa" font-family="monospace" font-size="14" font-weight="bold">“bank”  vector</text>
  <text x="360" y="100" text-anchor="middle" fill="#bdaef0" font-family="sans-serif" font-size="10">its embedding from Chapter Two</text>

  <!-- three projections -->
  <path d="M320,112 L200,150" stroke="#6b82a0" stroke-width="1.5" marker-end="url(#qa1)"/>
  <path d="M360,112 L360,150" stroke="#6b82a0" stroke-width="1.5" marker-end="url(#qa1)"/>
  <path d="M400,112 L520,150" stroke="#6b82a0" stroke-width="1.5" marker-end="url(#qa1)"/>
  <text x="245" y="140" fill="#6b82a0" font-family="monospace" font-size="9">×W_Q</text>
  <text x="372" y="140" fill="#6b82a0" font-family="monospace" font-size="9">×W_K</text>
  <text x="470" y="140" fill="#6b82a0" font-family="monospace" font-size="9">×W_V</text>

  <rect x="60" y="156" width="220" height="82" rx="10" fill="#4a3000" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="170" y="182" text-anchor="middle" fill="#fdeccd" font-family="sans-serif" font-size="13" font-weight="bold">QUERY</text>
  <text x="170" y="202" text-anchor="middle" fill="#f0c987" font-family="sans-serif" font-size="10.5">“what am I looking for?”</text>
  <text x="170" y="220" text-anchor="middle" fill="#f0c987" font-family="sans-serif" font-size="10">something that disambiguates me</text>

  <rect x="250" y="252" width="220" height="82" rx="10" fill="#0a4a5c" stroke="#00d4f5" stroke-width="1.5"/>
  <text x="360" y="278" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="13" font-weight="bold">KEY</text>
  <text x="360" y="298" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="10.5">“what do I offer?”</text>
  <text x="360" y="316" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="10">a label other tokens can match against</text>

  <rect x="440" y="156" width="220" height="82" rx="10" fill="#053d28" stroke="#10b981" stroke-width="1.5"/>
  <text x="550" y="182" text-anchor="middle" fill="#d3f5e6" font-family="sans-serif" font-size="13" font-weight="bold">VALUE</text>
  <text x="550" y="202" text-anchor="middle" fill="#8fd8b8" font-family="sans-serif" font-size="10.5">“what will I hand over?”</text>
  <text x="550" y="220" text-anchor="middle" fill="#8fd8b8" font-family="sans-serif" font-size="10">the information I contribute if chosen</text>
</svg>
<figcaption><strong>Figure 1.</strong> Every token is projected into three roles by three learned matrices (W_Q, W_K, W_V). The same word plays all three parts at once: it asks its own question (query), advertises itself to others (key), and stands ready to contribute (value). These three projections are among the parameters the model learns during training — the model discovers, from data, what makes a good question and a good answer.</figcaption>
</figure>

The trick, now, is how a query and a key are compared. Both are vectors — arrows in the same space — and there is a standard way to measure how well two vectors align: the **dot product**, which is large and positive when two vectors point the same way, near zero when they are unrelated, and negative when they point apart. So the relevance of token B to token A is simply: take A's query, take B's key, and dot them together. A high number means "B is exactly the kind of thing A was looking for." That single number is the raw ingredient of every attention weight.

## Part III — From raw scores to a spotlight

Let us make this concrete with the sentence that started us off. The `bank`-token issues its query, and we score it against the key of every token in the sentence — including itself. We get a row of raw numbers, one per token: high for `river`, moderate for `current`, low for `the` and `of`.

Raw scores, though, are awkward to use directly. They can be any size, positive or negative, and they do not add up to anything meaningful. What we want is to turn them into a clean set of *weights* — all positive, and summing to exactly one — so they behave like a spotlight of fixed total brightness that we can shine across the sentence, pouring most of it on the relevant words and only a sliver on the rest. The function that does this conversion is called the **softmax**, and while its formula is a small piece of arithmetic, all you need to hold is what it accomplishes: it takes any row of scores and squashes it into a tidy distribution of attention that sums to one, exaggerating the gaps so the strong scores get the lion's share.

<figure class="diagram">
<svg viewBox="0 0 720 420" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Scoring a query against every key, then softmax into attention weights that sum to one">
  <defs><marker id="qa2" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9 z" fill="#f59e0b"/></marker></defs>
  <rect x="0" y="0" width="720" height="420" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="30" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">“bank” DECIDES WHERE TO LOOK</text>
  <text x="360" y="50" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="10.5">sentence: “he sat on the bank of the river”</text>

  <!-- query chip -->
  <rect x="40" y="72" width="150" height="40" rx="8" fill="#4a3000" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="115" y="92" text-anchor="middle" fill="#fdeccd" font-family="monospace" font-size="12" font-weight="bold">query( bank )</text>
  <text x="115" y="107" text-anchor="middle" fill="#f0c987" font-family="sans-serif" font-size="9">dotted against every key ↓</text>

  <!-- table of tokens with raw score and weight bars -->
  <g font-family="monospace" font-size="11">
    <!-- headers -->
    <text x="230" y="140" fill="#6b82a0">token (its key)</text>
    <text x="430" y="140" fill="#6b82a0">raw score</text>
    <text x="545" y="140" fill="#6b82a0">attention weight (softmax)</text>

    <!-- river -->
    <text x="230" y="168" fill="#d8f6fd">river</text>
    <text x="450" y="168" fill="#9fdcec">8.9</text>
    <rect x="545" y="157" width="150" height="15" rx="3" fill="#10b981"/><text x="545" y="188" fill="#8fd8b8" font-size="9">0.62</text>

    <text x="230" y="200" fill="#d8f6fd">current*</text>
    <text x="450" y="200" fill="#9fdcec">6.1</text>
    <rect x="545" y="189" width="70" height="15" rx="3" fill="#00d4f5"/><text x="545" y="220" fill="#8fd8b8" font-size="9">0.21</text>

    <text x="230" y="232" fill="#c9d6e8">sat</text>
    <text x="450" y="232" fill="#6b82a0">3.0</text>
    <rect x="545" y="221" width="28" height="15" rx="3" fill="#a78bfa"/><text x="545" y="252" fill="#8fd8b8" font-size="9">0.09</text>

    <text x="230" y="264" fill="#c9d6e8">the</text>
    <text x="450" y="264" fill="#6b82a0">1.2</text>
    <rect x="545" y="253" width="12" height="15" rx="3" fill="#6b82a0"/><text x="545" y="284" fill="#8fd8b8" font-size="9">0.04</text>

    <text x="230" y="296" fill="#c9d6e8">of</text>
    <text x="450" y="296" fill="#6b82a0">0.8</text>
    <rect x="545" y="285" width="10" height="15" rx="3" fill="#6b82a0"/><text x="545" y="316" fill="#8fd8b8" font-size="9">0.04</text>
  </g>
  <text x="230" y="336" fill="#6b82a0" font-family="sans-serif" font-size="9">*for a token appearing later, see Part V on why the future is hidden</text>

  <rect x="150" y="356" width="420" height="44" rx="10" fill="#111827" stroke="#2a3f5f"/>
  <text x="360" y="376" text-anchor="middle" fill="#c9d6e8" font-family="sans-serif" font-size="11" font-weight="bold">the weights sum to 1.00 — a spotlight of fixed brightness</text>
  <text x="360" y="392" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="10">most of it falls on “river”, a little on “current”, almost none on “the”</text>
</svg>
<figcaption><strong>Figure 2.</strong> The scoring step for a single token. Its query is dotted against every key to produce raw scores; softmax turns those into attention weights that sum to one. Crucially, these weights are not stored anywhere — they are recomputed from scratch, from the actual content of this particular sentence, every single time. Change one word and the whole spotlight redraws.</figcaption>
</figure>

We now have, for our `bank`-token, a spotlight: 62% on `river`, 21% on `current`, and dribs and drabs elsewhere. The final step is the one we were aiming for all along. We take a *weighted average of the value vectors* — 62% of `river`'s value, 21% of `current`'s value, and so on — and that blended vector becomes the information `bank` has gathered from its context. Mixed back into `bank`'s own representation, it drags the meaning firmly toward riverside. The blank mask has been painted.

<figure class="diagram">
<svg viewBox="0 0 720 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The gathered context is a weighted sum of value vectors, updating the bank token toward its riverside sense">
  <defs><marker id="qa3" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9 z" fill="#10b981"/></marker></defs>
  <rect x="0" y="0" width="720" height="340" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="30" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">GATHER: A WEIGHTED BLEND OF VALUES</text>

  <!-- value chips with weights -->
  <g font-family="monospace" font-size="11">
    <rect x="50"  y="70" width="150" height="40" rx="8" fill="#053d28" stroke="#10b981"/><text x="125" y="88" text-anchor="middle" fill="#d3f5e6">value( river )</text><text x="125" y="103" text-anchor="middle" fill="#8fd8b8" font-size="9">× 0.62</text>
    <rect x="50"  y="120" width="150" height="40" rx="8" fill="#053d28" stroke="#10b981" opacity="0.75"/><text x="125" y="138" text-anchor="middle" fill="#d3f5e6">value( current )</text><text x="125" y="153" text-anchor="middle" fill="#8fd8b8" font-size="9">× 0.21</text>
    <rect x="50"  y="170" width="150" height="40" rx="8" fill="#053d28" stroke="#10b981" opacity="0.45"/><text x="125" y="188" text-anchor="middle" fill="#d3f5e6">value( sat )</text><text x="125" y="203" text-anchor="middle" fill="#8fd8b8" font-size="9">× 0.09</text>
    <rect x="50"  y="220" width="150" height="40" rx="8" fill="#053d28" stroke="#10b981" opacity="0.25"/><text x="125" y="238" text-anchor="middle" fill="#d3f5e6">value( the/of )</text><text x="125" y="253" text-anchor="middle" fill="#8fd8b8" font-size="9">× 0.08</text>
  </g>

  <text x="250" y="168" fill="#10b981" font-family="monospace" font-size="24">Σ</text>
  <path d="M210,165 L245,165" stroke="#10b981" stroke-width="2" marker-end="url(#qa3)"/>
  <path d="M270,165 L320,165" stroke="#10b981" stroke-width="2" marker-end="url(#qa3)"/>

  <rect x="330" y="120" width="180" height="90" rx="10" fill="#0a4a5c" stroke="#00d4f5" stroke-width="2"/>
  <text x="420" y="150" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="12" font-weight="bold">context gathered</text>
  <text x="420" y="170" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="10">a blended vector, mostly</text>
  <text x="420" y="186" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="10">“water / geography”</text>

  <path d="M510,165 L560,165" stroke="#00d4f5" stroke-width="2" marker-end="url(#qa3)"/>

  <rect x="565" y="120" width="120" height="90" rx="10" fill="#2e1e5e" stroke="#a78bfa" stroke-width="2"/>
  <text x="625" y="150" text-anchor="middle" fill="#e8e3fa" font-family="monospace" font-size="12" font-weight="bold">“bank”</text>
  <text x="625" y="170" text-anchor="middle" fill="#c9b8f5" font-family="sans-serif" font-size="9.5">now shaded</text>
  <text x="625" y="185" text-anchor="middle" fill="#c9b8f5" font-family="sans-serif" font-size="9.5">toward riverside</text>

  <text x="360" y="300" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11">In the “deposited the cheque” sentence, the very same machinery would light up “deposited” and “cheque”</text>
  <text x="360" y="318" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11">instead — and “bank” would be dragged toward finance. One mechanism, opposite outcomes, decided by content.</text>
</svg>
<figcaption><strong>Figure 3.</strong> The payoff. The token's updated representation is a weighted sum of the <em>value</em> vectors of everything it attended to. The static embedding of Chapter Two has become <em>contextual</em>: “bank” is no longer a fixed point but a point that has moved, in this sentence, toward the meaning its neighbours implied. The crack we ended the last chapter on is healed.</figcaption>
</figure>

And that — query, key, value; score, softmax, blend — is the entire mechanism. Read those two figures again and notice there is no magic anywhere in them, only a learnable, content-driven weighted average. Every token in the sentence does this simultaneously, each issuing its own query, each ending up with its own context-updated representation. The sentence walks in as a row of frozen, isolated vectors and walks out as a row of vectors that have *talked to each other*.

<div class="callout">
⚕️ <strong>The ward-round analogy, because it genuinely fits.</strong> Picture a multidisciplinary team meeting. Each patient's case (a token) silently broadcasts a question — <em>“what here is relevant to me?”</em> (its query). Every other case advertises what it holds — <em>“I'm the one with the deranged clotting”</em> (its key). Each case then listens, weights the others by relevance, and updates its own plan with a blend of what the relevant cases contribute (their values). Nobody reads every chart end to end; relevance is negotiated by content, in parallel, all at once. And — the part worth remembering — when a model attends to the <em>wrong</em> case, confidently attributing a fact to the wrong antecedent, you are watching an attention weight land in the wrong place. A surprising share of an LLM's plausible-but-wrong answers are, at bottom, attention pointed at the wrong word.
</div>

## Part IV — Why this was the breakthrough

It is worth pausing to appreciate *why* this particular design changed everything, because it did not merely work — it unlocked the entire scale of the modern era. Two properties are responsible.

The first is that attention is **content-addressed**, not position-addressed. Older approaches to sequence modelling processed text strictly left to right, carrying a running summary forward and asking, in effect, "what was a few steps back?" That makes reaching across long distances hard — by the time you are five hundred words in, the details of word twelve have been squeezed to mush. Attention asks a completely different question: not "who is near me?" but "who *matches* me?" A token can reach directly across a thousand others in a single step to the one word that resolves it, with no decay over distance. The same machinery, unchanged, handles a pronoun and its antecedent, a subject and its far-off verb, a closing bracket and its opening one, and a fact stated three paragraphs earlier. It never needed to be told which of these tasks it was doing; relevance is relevance.

The second is that attention is **completely parallel**. Because every token computes its query, its key, and its value independently, and because all the scores are just one big multiplication of queries against keys, the entire operation runs at once — not word by word, but the whole sentence in a single sweep. This is not a minor efficiency note. It is the reason these models could be trained on a meaningful fraction of the internet at all. The architecture finally matched what modern hardware is savagely good at: doing enormous numbers of multiplications simultaneously. An idea that was merely elegant would have stayed in a research paper. An idea that was elegant *and* parallel became the foundation of an industry.

## Part V — The one rule: you may not read the future

There is a single, crucial constraint I have been quietly deferring, and now it clicks into place with everything from Chapter Two.

Recall the game: the model is trained to predict the *next* token from the ones before it. Now imagine we let a token attend freely to every other token in the sentence, including the ones that come after it. When the model is trying to predict the word after `bank`, it could simply *peek* at that word through attention — and the whole exercise collapses into cheating. It would ace training by copying the answer and learn nothing.

So we impose one rule. When a token computes its attention, it is permitted to look only at itself and the tokens *before* it — never at the ones that follow. Before the softmax, the scores for all future positions are blanked out entirely, so they receive exactly zero weight. Information is allowed to flow backward-to-forward, never forward-to-backward. This is called the **causal mask**, and it is why this whole family of models earns the name *autoregressive*: each position is built only from the past, so that predicting the future remains an honest test.

<figure class="diagram">
<svg viewBox="0 0 720 400" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The causal mask: each token may attend only to itself and earlier tokens, forming a lower triangle">
  <rect x="0" y="0" width="720" height="400" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="30" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">THE CAUSAL MASK — NO PEEKING AHEAD</text>
  <text x="360" y="50" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="10.5">rows = the token doing the looking · columns = the token being looked at</text>

  <!-- column headers -->
  <g font-family="monospace" font-size="11" fill="#9fdcec">
    <text x="230" y="86" text-anchor="middle">the</text>
    <text x="300" y="86" text-anchor="middle">patient</text>
    <text x="378" y="86" text-anchor="middle">took</text>
    <text x="450" y="86" text-anchor="middle">two</text>
    <text x="530" y="86" text-anchor="middle">tablets</text>
  </g>

  <!-- rows -->
  <g font-family="monospace" font-size="11">
    <text x="150" y="116" text-anchor="end" fill="#fdeccd">the</text>
    <text x="150" y="156" text-anchor="end" fill="#fdeccd">patient</text>
    <text x="150" y="196" text-anchor="end" fill="#fdeccd">took</text>
    <text x="150" y="236" text-anchor="end" fill="#fdeccd">two</text>
    <text x="150" y="276" text-anchor="end" fill="#fdeccd">tablets</text>
  </g>

  <!-- grid cells: allowed = green (lower triangle incl diagonal), blocked = red -->
  <!-- helper coordinates: cols x = 205,275,350,420,500 ; each 55 wide, 30 tall, y rows 100,140,180,220,260 -->
  <!-- row the (only col1) -->
  <rect x="205" y="100" width="55" height="30" rx="4" fill="#053d28" stroke="#10b981"/>
  <rect x="275" y="100" width="55" height="30" rx="4" fill="#1a0c0c" stroke="#3d0f0f"/>
  <rect x="345" y="100" width="55" height="30" rx="4" fill="#1a0c0c" stroke="#3d0f0f"/>
  <rect x="415" y="100" width="55" height="30" rx="4" fill="#1a0c0c" stroke="#3d0f0f"/>
  <rect x="485" y="100" width="70" height="30" rx="4" fill="#1a0c0c" stroke="#3d0f0f"/>
  <!-- row patient (col1,2) -->
  <rect x="205" y="140" width="55" height="30" rx="4" fill="#053d28" stroke="#10b981"/>
  <rect x="275" y="140" width="55" height="30" rx="4" fill="#053d28" stroke="#10b981"/>
  <rect x="345" y="140" width="55" height="30" rx="4" fill="#1a0c0c" stroke="#3d0f0f"/>
  <rect x="415" y="140" width="55" height="30" rx="4" fill="#1a0c0c" stroke="#3d0f0f"/>
  <rect x="485" y="140" width="70" height="30" rx="4" fill="#1a0c0c" stroke="#3d0f0f"/>
  <!-- row took (1-3) -->
  <rect x="205" y="180" width="55" height="30" rx="4" fill="#053d28" stroke="#10b981"/>
  <rect x="275" y="180" width="55" height="30" rx="4" fill="#053d28" stroke="#10b981"/>
  <rect x="345" y="180" width="55" height="30" rx="4" fill="#053d28" stroke="#10b981"/>
  <rect x="415" y="180" width="55" height="30" rx="4" fill="#1a0c0c" stroke="#3d0f0f"/>
  <rect x="485" y="180" width="70" height="30" rx="4" fill="#1a0c0c" stroke="#3d0f0f"/>
  <!-- row two (1-4) -->
  <rect x="205" y="220" width="55" height="30" rx="4" fill="#053d28" stroke="#10b981"/>
  <rect x="275" y="220" width="55" height="30" rx="4" fill="#053d28" stroke="#10b981"/>
  <rect x="345" y="220" width="55" height="30" rx="4" fill="#053d28" stroke="#10b981"/>
  <rect x="415" y="220" width="55" height="30" rx="4" fill="#053d28" stroke="#10b981"/>
  <rect x="485" y="220" width="70" height="30" rx="4" fill="#1a0c0c" stroke="#3d0f0f"/>
  <!-- row tablets (1-5) -->
  <rect x="205" y="260" width="55" height="30" rx="4" fill="#053d28" stroke="#10b981"/>
  <rect x="275" y="260" width="55" height="30" rx="4" fill="#053d28" stroke="#10b981"/>
  <rect x="345" y="260" width="55" height="30" rx="4" fill="#053d28" stroke="#10b981"/>
  <rect x="415" y="260" width="55" height="30" rx="4" fill="#053d28" stroke="#10b981"/>
  <rect x="485" y="260" width="70" height="30" rx="4" fill="#053d28" stroke="#10b981"/>

  <rect x="590" y="150" width="18" height="14" rx="3" fill="#053d28" stroke="#10b981"/><text x="614" y="162" fill="#8fd8b8" font-family="sans-serif" font-size="10">allowed</text>
  <rect x="590" y="176" width="18" height="14" rx="3" fill="#1a0c0c" stroke="#3d0f0f"/><text x="614" y="188" fill="#e2a0a0" font-family="sans-serif" font-size="10">blocked</text>

  <text x="360" y="330" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11">Every token sees the past and itself; none sees the future. The green lower triangle is the whole rule.</text>
  <text x="360" y="352" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11">It is what keeps “predict the next token” an honest exam rather than a memory test with the answers showing.</text>
  <text x="360" y="380" text-anchor="middle" fill="#00d4f5" font-family="monospace" font-size="11">this is the exact link between Chapter Two's game and Chapter Three's mechanism</text>
</svg>
<figcaption><strong>Figure 4.</strong> The causal mask, drawn as a grid of who-may-look-at-whom. The permitted cells form a lower triangle: each token attends to itself and everything before it, never after. This single constraint is the seam that stitches attention to the prediction objective — it is why a model can be trained to predict the future without ever being shown it.</figcaption>
</figure>

## Part VI — What one glance cannot do

We have built something remarkable, and it is worth being precise about exactly how far it gets us — because the honest limits are what point straight at the next chapter.

Our attention mechanism lets every token look once across the sentence, gather the relevant context, and update itself. The frozen vectors of Chapter Two are now fluid, context-aware, alive to their surroundings. But look closely at two things it does *not* yet do.

First, a single attention operation can only track *one kind of relationship at a time*. Its one set of query and key projections learns one notion of "relevant" — perhaps "which earlier noun does this pronoun refer to." But a sentence is threaded with many relationships at once: grammatical agreement, who-did-what-to-whom, the matching of quotation marks, the long-range echo of a topic. One query-key scheme cannot be all of these simultaneously. We are going to need *many* attention operations running in parallel, each free to specialise in a different kind of relationship — and then a way to combine what they each found. That plurality has a name, *multi-head attention*, and it is the first thing we build next.

Second — and this is subtler — attention *moves information around* but does very little *thinking* with it. It is a superb librarian, fetching the right passages and laying them on the desk, but fetching is not the same as reasoning over what was fetched. After each token has gathered its context, it needs a moment to sit and *compute* on what it now holds — to transform the gathered information into something new. That step, a small computation applied to each token on its own, alternates with attention in a rhythm that repeats: *gather, then think; gather, then think*. Stack that rhythm dozens of times and you have the full engine — the **transformer block**, and the deep tower built from it.

So this is where we stand. We have the beating heart. We have watched a word turn its head, read the room, and change its meaning. What we do not yet have is the whole body: the many parallel glances, the per-token thinking that turns gathered context into inference, and the depth — the stacking of block upon block — that lets meaning be refined layer after layer until a confident next-token forecast can finally be read off the top.

Building that body, from this heart, is Chapter Four. And when it is finished, you will be able to look at a diagram of a real transformer — the kind that has intimidated readers for years — and find, in every box, something you understand from the inside.

*— Neal*

<div class="chapter-banner">
📖 <strong>Next chapter:</strong> <em>The Transformer Block</em> — many attention heads looking at once, the per-token computation that turns gathered context into thought, and the deep stack that refines meaning layer by layer into a prediction. We assemble the whole engine from the single part we just built.
</div>
