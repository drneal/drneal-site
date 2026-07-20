---
title: "How Noise Becomes Knowledge: Training a Language Model"
date: 2026-07-21
category: Deep Learning
tags: training, gradient descent, backpropagation, loss function, cross-entropy, pretraining, base model, LLM, foundations
level: Intermediate
read_time: 45 min
summary: "Chapter Five of a ground-up account of how large language models work. We built the whole engine in the last chapter — and admitted it was empty, a magnificent tower full of random numbers that would output pure gibberish. This chapter fills it. It is the story of how a single measure of one wrong guess can reach back through a hundred layers and correct every weight that caused it — and how, repeated across a large fraction of everything humans have written, that one procedure turns noise into something that knows the world."
featured: false
---

<a href="/static/img/How_Large_Language_Models_Work.png" target="_blank" rel="noopener"><img src="/static/img/How_Large_Language_Models_Work.png" alt="How an LLM Works — a one-page visual map of all eight chapters" style="display:block; width:100%; height:auto; border-radius:10px; margin:0.4em 0 1.8em; box-shadow:0 2px 12px rgba(0,0,0,0.35);"></a>

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
figure.diagram { margin: 2em 0; text-align: center; }
figure.diagram svg { max-width: 100%; height: auto; }
figure.diagram figcaption {
  font-size: 0.8em; color: #6b82a0; margin-top: 0.6em; text-align: left;
}
</style>

<div class="chapter-banner">
📖 <strong>Chapter Five of a ground-up account of how large language models work.</strong> Across <a href="/post/2026-07-17-the-grain-of-language">four</a> <a href="/post/2026-07-18-the-prediction-game">chapters</a> we <a href="/post/2026-07-19-reading-the-room">built</a> the whole <a href="/post/2026-07-20-the-tower">engine</a> — tokens, embeddings, attention, the deep tower — and each time I quietly deferred the same question: where do all the numbers inside it come from? Three times I promised an answer later. This is later.
</div>

# How Noise Becomes Knowledge: Training a Language Model

<nav style="font-size:0.8em; background:#0d1117; border:1px solid #1e2d45; border-left:4px solid #00d4f5; border-radius:0 8px 8px 0; padding:0.9em 1.3em; margin:1.6em 0; line-height:1.95;">
<div style="color:#00d4f5; font-family:'JetBrains Mono',monospace; font-size:0.86em; letter-spacing:0.06em; margin-bottom:0.5em;">📚 HOW AN LLM WORKS · CONTENTS</div>
<span style="color:#6b82a0;">1.</span> <a href="/post/2026-07-17-the-grain-of-language">The Grain of Language</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">2.</span> <a href="/post/2026-07-18-the-prediction-game">The Prediction Game</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">3.</span> <a href="/post/2026-07-19-reading-the-room">Reading the Room</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">4.</span> <a href="/post/2026-07-20-the-tower">The Tower</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">5.</span> <strong style="color:#f59e0b;">How Noise Becomes Knowledge</strong> &nbsp;·&nbsp;
<span style="color:#6b82a0;">6.</span> <a href="/post/2026-07-22-manners-for-a-mind">Manners for a Mind</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">7.</span> <a href="/post/2026-07-23-meaning-you-can-search">Meaning You Can Search</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">8.</span> <a href="/post/2026-07-24-the-agent">The Agent</a>

<div style="margin-top:0.6em; padding-top:0.5em; border-top:1px solid #1e2d45;"><a href="/static/How_an_LLM_Works.pdf"><img src="/static/book_cover_icon.png" alt="How an LLM Works — book cover" style="height:2.8em; vertical-align:middle; border-radius:2px; box-shadow:0 1px 5px rgba(0,0,0,0.55); margin-right:0.55em;"></a><a href="/static/How_an_LLM_Works.pdf" style="color:#f59e0b; font-weight:bold;">Download all eight chapters as a PDF book</a> <span style="color:#6b82a0;">— linked contents, ~66 pages</span></div>
</nav>

Let me begin by making the problem vivid, because its difficulty is easy to underestimate and the solution is easy to take for granted once you have seen it.

At the end of the last chapter we had assembled a complete transformer — the embedding table, the attention heads with their query, key, and value projections, the feed-forward layers, the residual stream, the whole tower, and the final projection that reads a prediction off the top. It is an engine of real intricacy. And I told you the uncomfortable truth: if you built it today and ran a sentence through it, it would produce *gibberish*. Every one of its parameters — and there may be billions of them — begins life as a random number. The embedding that we later admired for placing `aspirin` near `ibuprofen` starts as buckshot. The attention heads that we said track pronouns start attending to nothing in particular. The feed-forward layers that hold the model's knowledge start holding noise.

So here is the question this chapter answers, and I want you to feel how audacious it is. We have a machine with a billion knobs, all set randomly. We want to turn those random settings into precisely the configuration that makes the machine fluent, knowledgeable, and startlingly capable. Nobody can set a billion knobs by hand, and nobody knows what the right settings even are. How, then, does the machine find them *itself*?

The answer is one of the most beautiful procedures humans have ever devised, and it has just three moving parts: a way to *measure* how wrong the machine currently is, a way to work out which direction to nudge every knob to make it *less* wrong, and the patience to do this a truly staggering number of times. Measure, nudge, repeat. That is all training is. Let us build each part.

## Part I — Measuring wrongness

You cannot improve what you cannot measure, so everything starts with turning "the model is wrong" into a single, honest number.

We have exactly what we need, and we have had it since Chapter One. Recall that language modelling is *self-supervised*: we take real text, and at every position the "correct answer" is simply the token that actually came next. So we can play the following game against any piece of writing. Show the model the text up to some point. Let it produce its forecast — the full probability distribution over the vocabulary from Chapter Two. Then look at the token that *truly* came next, and ask a pointed question: **how much probability did the model put on the truth?**

If the model was confident and right — it put 70% of its forecast on the token that actually followed — it was barely wrong at all. If it was confident and *wrong* — it put 70% on some other token and a measly 0.1% on the truth — it was badly, embarrassingly wrong. The measure of wrongness we use, called the **cross-entropy loss**, captures exactly this: it is large when the model assigned low probability to the true next token, and small when it assigned high probability. You can think of it, without losing anything important, as a number that measures the model's *surprise* at the correct answer. A good model is rarely surprised by what comes next; a bad one is constantly astonished.

<figure class="diagram">
<svg viewBox="0 0 720 380" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The loss measures how much probability the model put on the token that truly came next">
  <rect x="0" y="0" width="720" height="380" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="30" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">THE LOSS: SURPRISE AT THE TRUTH</text>
  <text x="360" y="50" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="10.5">context: “the patient was prescribed a course of ___”   ·   truth: “antibiotics”</text>

  <!-- good model -->
  <text x="180" y="86" text-anchor="middle" fill="#8fd8b8" font-family="sans-serif" font-size="12" font-weight="bold">a well-trained model</text>
  <g font-family="monospace" font-size="10">
    <rect x="70" y="100" width="150" height="16" rx="3" fill="#10b981"/><text x="228" y="113" fill="#8fd8b8">antibiotics 0.62 ✓</text>
    <rect x="70" y="122" width="45"  height="16" rx="3" fill="#00d4f5"/><text x="123" y="135" fill="#9fdcec">steroids 0.11</text>
    <rect x="70" y="144" width="20"  height="16" rx="3" fill="#a78bfa"/><text x="98"  y="157" fill="#c9b8f5">tablets 0.04</text>
  </g>
  <rect x="70" y="176" width="220" height="40" rx="8" fill="#0e1e1a" stroke="#10b981"/>
  <text x="180" y="194" text-anchor="middle" fill="#d3f5e6" font-family="sans-serif" font-size="10.5">put 0.62 on the truth →</text>
  <text x="180" y="209" text-anchor="middle" fill="#8fd8b8" font-family="monospace" font-size="11" font-weight="bold">low loss (little surprise)</text>

  <!-- bad model -->
  <text x="540" y="86" text-anchor="middle" fill="#e2a0a0" font-family="sans-serif" font-size="12" font-weight="bold">an untrained (random) model</text>
  <g font-family="monospace" font-size="10">
    <rect x="430" y="100" width="60" height="16" rx="3" fill="#6b82a0"/><text x="498" y="113" fill="#c9d6e8">giraffe 0.03</text>
    <rect x="430" y="122" width="55" height="16" rx="3" fill="#6b82a0"/><text x="493" y="135" fill="#c9d6e8">the 0.03</text>
    <rect x="430" y="144" width="10" height="16" rx="3" fill="#3d0f0f"/><text x="448" y="157" fill="#e2a0a0">antibiotics 0.005 ✓</text>
  </g>
  <rect x="430" y="176" width="220" height="40" rx="8" fill="#1a0c0c" stroke="#f87171"/>
  <text x="540" y="194" text-anchor="middle" fill="#fde2e2" font-family="sans-serif" font-size="10.5">put 0.005 on the truth →</text>
  <text x="540" y="209" text-anchor="middle" fill="#e2a0a0" font-family="monospace" font-size="11" font-weight="bold">high loss (great surprise)</text>

  <text x="360" y="266" text-anchor="middle" fill="#c9d6e8" font-family="sans-serif" font-size="11.5" font-weight="bold">One number, computed at every position of every training example.</text>
  <text x="360" y="292" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11">Averaged over a whole batch of text, it becomes the single score that training exists to drive downward.</text>
  <text x="360" y="316" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11">Lower loss is not an abstraction — it is, quite literally, the model being less often surprised by real writing.</text>
  <text x="360" y="344" text-anchor="middle" fill="#00d4f5" font-family="monospace" font-size="11">the entire goal of training: make this number smaller</text>
</svg>
<figcaption><strong>Figure 1.</strong> The loss turns "how wrong is the model right now?" into one number, by asking how much probability it placed on the token that actually came next. It is high for a confidently-wrong model and low for a confidently-right one. This single number — averaged over many predictions — is the compass for everything that follows.</figcaption>
</figure>

So now we have a number. For any setting of the billion knobs, we can compute a loss — a measure of how badly, on average, the machine currently predicts real text. And the entire problem of training has been transformed into something almost tractable-sounding: *find the setting of the knobs that makes this number as small as possible.* We have turned "teach a machine to understand language" into "minimise a number." That reframing is the whole ballgame.

## Part II — Which way is downhill?

Here is a way to picture the task that will carry you a long way. Imagine the loss as a *landscape*. Every possible setting of the billion knobs is a location, and the height of the terrain at that location is the loss — how wrong the model is with those settings. A random starting point is somewhere high up on a hillside, in the fog. The configuration we want — low loss, fluent model — is down in a valley we cannot see. Training is the search for that valley. And the rule for the search is the simplest imaginable: *always step downhill.*

But downhill in a landscape of a billion dimensions? You cannot see it, cannot picture it, cannot survey it. What you *can* do, remarkably, is feel the slope directly under your feet. For each of the billion knobs, calculus lets us ask a precise local question: *if I nudged this one knob a hair in the positive direction, would the loss go up or down, and how steeply?* Collect that answer for every knob at once and you have the **gradient** — a vector that points in the direction of steepest *increase* of the loss. And if the gradient points most steeply uphill, then its exact opposite points most steeply downhill. So we take a small step in that opposite direction, and we have, with certainty, reduced the loss a little. Every knob moves a touch toward "less wrong."

<figure class="diagram">
<svg viewBox="0 0 720 380" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Gradient descent: the loss as a landscape, stepping downhill toward a valley">
  <defs><marker id="ga5" markerWidth="10" markerHeight="10" refX="7" refY="5" orient="auto"><path d="M0,0 L9,5 L0,10 z" fill="#f59e0b"/></marker></defs>
  <rect x="0" y="0" width="720" height="380" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="30" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">GRADIENT DESCENT — ALWAYS STEP DOWNHILL</text>

  <!-- valley curve -->
  <path d="M60,90 C200,110 250,300 360,300 C470,300 520,110 660,90" stroke="#2a3f5f" stroke-width="2.5" fill="none"/>
  <text x="90" y="82" fill="#6b82a0" font-family="sans-serif" font-size="10">high loss (random start)</text>
  <text x="360" y="330" text-anchor="middle" fill="#10b981" font-family="sans-serif" font-size="10.5">low loss (fluent model) — the valley</text>

  <!-- steps as balls -->
  <circle cx="120" cy="118" r="9" fill="#f87171"/>
  <path d="M132,128 L175,165" stroke="#f59e0b" stroke-width="2" marker-end="url(#ga5)"/>
  <circle cx="185" cy="175" r="9" fill="#f59e0b"/>
  <path d="M197,184 L238,222" stroke="#f59e0b" stroke-width="2" marker-end="url(#ga5)"/>
  <circle cx="248" cy="232" r="9" fill="#f59e0b"/>
  <path d="M260,240 L305,272" stroke="#f59e0b" stroke-width="2" marker-end="url(#ga5)"/>
  <circle cx="318" cy="282" r="9" fill="#f59e0b"/>
  <path d="M332,288 L344,294" stroke="#f59e0b" stroke-width="2" marker-end="url(#ga5)"/>
  <circle cx="360" cy="298" r="10" fill="#10b981"/>

  <!-- annotations -->
  <text x="150" y="150" fill="#f0c987" font-family="sans-serif" font-size="10">gradient says “downhill is this way”</text>
  <rect x="440" y="150" width="240" height="86" rx="10" fill="#111827" stroke="#2a3f5f"/>
  <text x="560" y="174" text-anchor="middle" fill="#c9d6e8" font-family="sans-serif" font-size="11" font-weight="bold">the step size is the “learning rate”</text>
  <text x="560" y="195" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="10">too small → training crawls</text>
  <text x="560" y="212" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="10">too large → it overshoots the valley</text>
  <text x="560" y="229" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="10">and bounces, never settling</text>

  <text x="360" y="360" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11">Each step lowers the loss a little. The art is only in the step size and the sheer number of steps.</text>
</svg>
<figcaption><strong>Figure 2.</strong> Gradient descent, the engine of all learning here. The loss is a landscape over the space of all parameters; the gradient reveals the downhill direction; we take a small step that way and repeat. The size of each step is the <em>learning rate</em> — one of the few dials a human sets — and getting it wrong in either direction (crawling, or overshooting and bouncing) is one of the most common ways training fails.</figcaption>
</figure>

If gradient descent feels familiar it should — it is the same "small step downhill on a loss" that underlies essentially all of machine learning, and it is exactly what you would do, blindfolded, to find the bottom of a valley: feel which way the ground slopes beneath your feet, and shuffle that way, over and over. What makes it feel like magic in a language model is only the dimensionality. You are not on a hillside; you are on a surface with a billion independent directions, feeling the slope in all of them at once, and stepping downhill in that unimaginable space. The idea is humble. The scale is not.

<div class="callout">
⚕️ <strong>The trainee analogy, and where it holds.</strong> Think of the loss as the feedback a trainee gets on every single prediction they make — not a term-end exam, but a correction after each guess. "You said antibiotics; it was antibiotics — good, barely adjust." "You said giraffe; it was antibiotics — badly wrong, adjust sharply." A human trainee integrates such feedback slowly and holistically. The machine does something more literal and more thorough: it works out, for <em>every</em> internal parameter that contributed to the guess, the precise direction that parameter should move to have made the guess a little better — and moves all of them at once. It is feedback turned into a billion simultaneous, individually-tailored corrections.
</div>

## Part III — The astonishing part: assigning the blame

I have been gliding over the hardest question, and now we face it, because it is the genuine miracle at the centre of this chapter.

Computing the gradient means working out, for each of a billion knobs, how the loss would change if that knob moved. But the loss is computed at the very *top* of the tower — after the token has passed up through a hundred layers of attention and feed-forward — while the knobs are scattered throughout every one of those layers, deep below. How can a single number at the summit possibly tell a particular weight, buried in the twelfth attention head of the fortieth block, which way *it* should move? The mistake happened at the top; the causes are everywhere underneath. This is the problem of *credit assignment* — apportioning responsibility for the error back to every part that contributed — and for decades it was the barrier that made deep networks seem hopeless.

The solution is an algorithm called **backpropagation**, and its essential idea is one every clinician will recognise as root-cause analysis. When something goes wrong at the end of a long process, you do not shrug and blame everything equally. You trace backward. You ask: given the final error, how much did the *last* step contribute? Then, holding that accountable, how much did the step *before* it contribute to *that*? And so on, backward, apportioning a share of the blame at each stage to the stages that fed it. Backpropagation does exactly this, mechanically and exactly, using the chain rule of calculus. It starts with the loss at the top, computes how much the topmost layer's weights contributed, then uses that to compute how much the layer below contributed, and so on — a single sweep from the summit all the way down to the embeddings, leaving behind, on every weight, a precise note: *nudge yourself in this direction, by this much.*

<figure class="diagram">
<svg viewBox="0 0 720 440" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Backpropagation: the error at the top flows backward down the tower, assigning a correction to every weight">
  <defs>
    <marker id="up5" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9 z" fill="#00d4f5"/></marker>
    <marker id="dn5" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9 z" fill="#f87171"/></marker>
  </defs>
  <rect x="0" y="0" width="720" height="440" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="30" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">BACKPROPAGATION — TRACING THE BLAME</text>

  <!-- blocks -->
  <g>
    <rect x="270" y="360" width="180" height="40" rx="8" fill="#2e1e5e" stroke="#a78bfa" stroke-width="1.3"/><text x="360" y="385" text-anchor="middle" fill="#e8e3fa" font-family="sans-serif" font-size="10.5">embeddings</text>
    <rect x="270" y="300" width="180" height="40" rx="8" fill="#0a4a5c" stroke="#00d4f5" stroke-width="1.3"/><text x="360" y="325" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="10.5">block 1</text>
    <rect x="270" y="240" width="180" height="40" rx="8" fill="#0a4a5c" stroke="#00d4f5" stroke-width="1.3"/><text x="360" y="265" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="10.5">block 2 … </text>
    <rect x="270" y="180" width="180" height="40" rx="8" fill="#0a4a5c" stroke="#00d4f5" stroke-width="1.3"/><text x="360" y="205" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="10.5">block N</text>
    <rect x="270" y="120" width="180" height="40" rx="8" fill="#053d28" stroke="#10b981" stroke-width="1.6"/><text x="360" y="145" text-anchor="middle" fill="#d3f5e6" font-family="sans-serif" font-size="10.5">prediction</text>
    <rect x="270" y="66" width="180" height="38" rx="8" fill="#4a3000" stroke="#f59e0b" stroke-width="1.6"/><text x="360" y="90" text-anchor="middle" fill="#fdeccd" font-family="sans-serif" font-size="10.5" font-weight="bold">LOSS (surprise)</text>
  </g>

  <!-- forward arrows (left) -->
  <path d="M250,380 L250,85" stroke="#00d4f5" stroke-width="2" marker-end="url(#up5)"/>
  <text x="205" y="232" text-anchor="middle" fill="#00d4f5" font-family="sans-serif" font-size="10" transform="rotate(-90 205 232)">forward: text → prediction → loss</text>

  <!-- backward arrows (right) -->
  <path d="M470,85 L470,380" stroke="#f87171" stroke-width="2" marker-end="url(#dn5)"/>
  <text x="512" y="232" text-anchor="middle" fill="#f87171" font-family="sans-serif" font-size="10" transform="rotate(90 512 232)">backward: blame → every weight</text>

  <!-- notes -->
  <text x="600" y="130" fill="#e2a0a0" font-family="sans-serif" font-size="9.5">“nudge −”</text>
  <text x="600" y="210" fill="#e2a0a0" font-family="sans-serif" font-size="9.5">“nudge +”</text>
  <text x="600" y="270" fill="#e2a0a0" font-family="sans-serif" font-size="9.5">“nudge −”</text>
  <text x="600" y="330" fill="#e2a0a0" font-family="sans-serif" font-size="9.5">“barely move”</text>

  <text x="360" y="414" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="10.5">One forward pass to make the guess and measure the loss;</text>
  <text x="360" y="431" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="10.5">one backward pass to apportion the blame to every weight. Then step, and repeat.</text>
</svg>
<figcaption><strong>Figure 3.</strong> Backpropagation. Text flows <em>up</em> the tower to produce a prediction and a loss (blue). Then the blame flows <em>down</em> (red): the error is traced backward, layer by layer, until every weight in the entire model — billions of them — has received a precise, individual instruction for how to change. What sounds impossible is, mechanically, just the chain rule applied with ruthless bookkeeping, and it costs only about one extra pass through the network.</figcaption>
</figure>

I want to dwell on how astonishing this is, because familiarity has dulled it for the field and it should not be dulled for you. A single number — the model's surprise at one token — is decomposed, exactly, into billions of individual responsibilities, one for every parameter that had any hand in producing it, no matter how deep it sits or how indirectly it contributed. And it is done efficiently, in a single backward sweep, not by the impossible brute force of testing each knob one at a time. Backpropagation is the reason deep learning works at all. Without it, the tower we built in Chapter Four would be an unteachable monument. With it, the tower can be *corrected*, wholesale, from a single measure of a single mistake.

<div class="keyidea">
💡 <strong>The complete recipe, in one breath.</strong> Show the model some text. Let it predict the next token (a <em>forward</em> pass up the tower). Measure its surprise at the truth (the loss). Trace that surprise backward to a correction for every weight (the <em>backward</em> pass — backpropagation). Nudge every weight a small step in its correcting direction (gradient descent). That is one training step. Everything else — the fluency, the knowledge, the apparent reasoning — is this one step, repeated.
</div>

## Part IV — One step is nothing; repetition is everything

Here is the deflating and then re-inflating truth about a single training step: it barely does anything. One nudge, on one small batch of text, moves each of the billion knobs by a hair. Run it once and the model is imperceptibly less terrible than before — still, to any observer, producing gibberish. If training were a single step, or a thousand, it would be a curiosity and nothing more.

The magic is entirely in the *repetition*, at a scale that is genuinely hard to hold in the mind. The step is repeated millions of times, over batch after batch of text, until the model has been nudged by essentially every sentence in a corpus of *trillions* of tokens — a large fraction of the readable internet from Chapter One, passed through the tower and turned into corrections. And slowly, then all at once, structure precipitates out of the noise. The embedding vectors drift from random scatter into the meaningful landscape of Chapter Two. The attention heads settle into their specialities. The feed-forward layers fill with fact. Gibberish becomes grammar; grammar becomes fluency; fluency becomes something that argues and codes and diagnoses. Watch the loss fall and the generated text change in lockstep:

<figure class="diagram">
<svg viewBox="0 0 720 400" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The training loop and the falling loss curve, with generated text evolving from noise to fluent sentences">
  <defs><marker id="lc5" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9 z" fill="#f59e0b"/></marker></defs>
  <rect x="0" y="0" width="720" height="400" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="30" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">THE LOSS FALLS; MEANING PRECIPITATES</text>

  <!-- axes -->
  <line x1="70" y1="70" x2="70" y2="250" stroke="#2a3f5f" stroke-width="2"/>
  <line x1="70" y1="250" x2="440" y2="250" stroke="#2a3f5f" stroke-width="2"/>
  <text x="52" y="80" fill="#6b82a0" font-family="monospace" font-size="10">high</text>
  <text x="52" y="248" fill="#6b82a0" font-family="monospace" font-size="10">low</text>
  <text x="255" y="272" text-anchor="middle" fill="#6b82a0" font-family="monospace" font-size="10">training steps →</text>
  <text x="40" y="160" fill="#6b82a0" font-family="monospace" font-size="10" transform="rotate(-90 40 160)">loss</text>

  <!-- loss curve -->
  <path d="M72,80 C130,150 200,215 300,235 C360,244 400,246 438,247" stroke="#f59e0b" stroke-width="2.5" fill="none"/>
  <circle cx="80"  cy="86"  r="4" fill="#f87171"/>
  <circle cx="180" cy="200" r="4" fill="#f59e0b"/>
  <circle cx="300" cy="235" r="4" fill="#10b981"/>

  <!-- sample snapshots -->
  <rect x="470" y="66" width="230" height="58" rx="8" fill="#0d1117" stroke="#3d0f0f"/>
  <text x="480" y="84" fill="#f87171" font-family="monospace" font-size="9" font-weight="bold">early — high loss</text>
  <text x="480" y="102" fill="#c9d6e8" font-family="monospace" font-size="8.5">“Th qz,eKf a—rr tse nul dp”</text>
  <text x="480" y="116" fill="#6b82a0" font-family="monospace" font-size="8">pure noise</text>

  <rect x="470" y="140" width="230" height="58" rx="8" fill="#0d1117" stroke="#4a3000"/>
  <text x="480" y="158" fill="#f59e0b" font-family="monospace" font-size="9" font-weight="bold">midway — falling</text>
  <text x="480" y="176" fill="#c9d6e8" font-family="monospace" font-size="8.5">“The pation was of the and”</text>
  <text x="480" y="190" fill="#6b82a0" font-family="monospace" font-size="8">word-shaped, meaningless</text>

  <rect x="470" y="214" width="230" height="58" rx="8" fill="#0d1117" stroke="#053d28"/>
  <text x="480" y="232" fill="#10b981" font-family="monospace" font-size="9" font-weight="bold">late — low loss</text>
  <text x="480" y="250" fill="#c9d6e8" font-family="monospace" font-size="8.5">“The patient was prescribed a”</text>
  <text x="480" y="264" fill="#6b82a0" font-family="monospace" font-size="8">fluent, grammatical</text>

  <text x="360" y="316" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11">The curve and the samples are the same story told two ways. As surprise falls, the machine's writing climbs</text>
  <text x="360" y="336" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11">from random characters, to word-shaped nonsense, to real sentences — meaning condensing out of pure repetition.</text>
  <text x="360" y="366" text-anchor="middle" fill="#00d4f5" font-family="monospace" font-size="11">nobody wrote the knowledge in · it was distilled from the pressure to predict</text>
</svg>
<figcaption><strong>Figure 4.</strong> Training in one picture. The loss curve falls steeply at first (spelling and word statistics are cheap to learn) then more slowly (grammar, then meaning, then knowledge). The generated samples track it exactly: noise, then word-shaped noise, then fluency. This is the promise from Chapter Two made literal — meaning is not installed, it <em>precipitates</em> out of the single relentless pressure to predict the next token.</figcaption>
</figure>

This whole phase has a name — **pretraining** — and it is, by a wide margin, the most expensive thing that happens to a language model. It consumes almost the entire compute budget: months of computation across thousands of specialised processors, at a cost that runs well into the millions. Nearly everything the finished model knows, it learned here, in this long descent, from this one repeated step. When people speak of the staggering resources behind frontier AI, it is overwhelmingly *this* they are describing — not the clever architecture, which is comparatively cheap to specify, but the brute, patient, enormously scaled application of measure-nudge-repeat.

## Part V — What the descent gives you, and what it does not

When the loss finally flattens and pretraining ends, we have something genuinely new in the world: a **base model**. The random noise is gone. The tower is full of structure — an embedding space that knows medicine and poetry and code, attention heads that parse grammar, feed-forward layers dense with fact. It is fluent in dozens of languages, apparently knowledgeable across most of human writing, and able to continue almost any text you give it with uncanny plausibility. Noise has become knowledge. The promise of this chapter's title is kept.

And yet — this is the twist that sets up everything still to come — a raw base model is *not* the helpful assistant you talk to. It has been trained to do exactly one thing: continue text in the way its corpus would. So its instinct, faced with your input, is not to *help* but to *continue*. Ask a base model a question and you may get, in reply, not an answer but *more questions* — because on the internet a question is very often followed by other questions, in an exam, an FAQ, a forum thread. It has learned the shape of all text, which is not the same as the shape of *helpful* text.

<figure class="diagram">
<svg viewBox="0 0 720 320" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A base model continues text rather than answering, motivating the need for post-training">
  <defs><marker id="ba5" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9 z" fill="#6b82a0"/></marker></defs>
  <rect x="0" y="0" width="720" height="320" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="30" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">A BASE MODEL CONTINUES — IT DOES NOT YET HELP</text>

  <rect x="40" y="70" width="300" height="44" rx="8" fill="#2e1e5e" stroke="#a78bfa" stroke-width="1.5"/>
  <text x="190" y="90" text-anchor="middle" fill="#e8e3fa" font-family="sans-serif" font-size="10.5" font-weight="bold">you ask:</text>
  <text x="190" y="106" text-anchor="middle" fill="#bdaef0" font-family="monospace" font-size="9.5">“What are the contraindications to X?”</text>

  <path d="M340,92 L385,92" stroke="#6b82a0" stroke-width="2" marker-end="url(#ba5)"/>

  <rect x="390" y="60" width="290" height="66" rx="8" fill="#1a0c0c" stroke="#f87171" stroke-width="1.3"/>
  <text x="535" y="80" text-anchor="middle" fill="#fde2e2" font-family="sans-serif" font-size="10.5" font-weight="bold">a base model may reply:</text>
  <text x="535" y="98" text-anchor="middle" fill="#e2a0a0" font-family="monospace" font-size="9">“What is the usual dose of X?</text>
  <text x="535" y="112" text-anchor="middle" fill="#e2a0a0" font-family="monospace" font-size="9">What monitoring is required? …”</text>

  <text x="360" y="170" text-anchor="middle" fill="#f0c987" font-family="sans-serif" font-size="11.5" font-weight="bold">Nothing malfunctioned. It continued the document, exactly as trained.</text>
  <text x="360" y="200" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11">“Continue the text” and “help the person” are different objectives that only overlap. Pretraining gave us the</text>
  <text x="360" y="220" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11">first — a vast, fluent, knowledgeable predictor. Turning it into the second is a separate act of shaping.</text>
  <text x="360" y="260" text-anchor="middle" fill="#00d4f5" font-family="monospace" font-size="11">that shaping — instruction tuning &amp; feedback — is Chapter Six</text>
</svg>
<figcaption><strong>Figure 5.</strong> The base model's telling limitation. It is not broken; it is doing precisely what training rewarded — continuing text. But "continue the text" and "answer the question helpfully" are different goals, and the gap between them is exactly the work of the next chapter.</figcaption>
</figure>

<div class="callout">
⚕️ <strong>A base model is a brilliant, unshaped mind.</strong> Picture a physician with encyclopaedic knowledge and total fluency who has, however, never been taught the <em>role</em> of a doctor — never learned that when a worried person describes symptoms, the thing to do is respond helpfully rather than, say, continue writing the textbook chapter the symptoms came from. The knowledge is all there. The <em>orientation toward being useful</em> is not. That orientation is not knowledge; it is a posture, and it has to be trained in separately. Which is precisely why the model you actually talk to went through a second, quite different kind of training after this one.
</div>

## Part VI — What we have, and the one thing left

Stand back and see how far we have come. Five chapters ago we had raw text from the internet. We ground it into tokens. We gave the tokens meaning as geometry. We built attention, the glance that lets a token read the room. We stacked attention and computation into a deep tower. And in this chapter we filled that tower — turning a billion random numbers into fluent knowledge by the humblest of procedures, applied at inhuman scale: measure the surprise, trace the blame, nudge every weight, repeat until the internet has passed through.

That is a complete, trained, knowledgeable language model. If your goal was to understand how the raw intelligence of these systems comes to be, you now understand it, end to end, with no gaps papered over and no magic left unexamined. The engine is built and it is full.

But it is not yet the thing in your pocket. The base model we have made is a mind without a manner — it will complete your sentence, mimic any voice, continue any document, and answer your question with three more questions, because helpfulness was never the target. The final transformation — the one that turns this vast, fluent, faintly feral predictor into something that answers, follows instructions, admits uncertainty, and declines to help with the dangerous things — is not more of the same training. It is a second kind of shaping entirely, smaller and stranger and, in its way, more consequential for how these systems behave in the world.

How a base model becomes an assistant — instruction tuning, learning from human preferences, and why the very same weights can host such wildly different personalities — is Chapter Six.

*— Neal*

<div class="chapter-banner">
📖 <strong>Next chapter:</strong> <em>From Predictor to Assistant</em> — the second, stranger training that turns a text-continuing base model into the helpful, careful assistant you actually talk to. We look at what changes, what does not, and why the seams of this final shaping are exactly where a deployed model's most important behaviours — and its most consequential failures — are decided.
</div>
