---
title: "Manners for a Mind: From Predictor to Assistant"
date: 2026-07-22
category: Deep Learning
tags: post-training, instruction tuning, RLHF, preferences, alignment, base model, assistant, LLM, sycophancy, foundations
level: Intermediate
read_time: 40 min
summary: "Chapter Six of a ground-up account of how large language models work. The last chapter left us with a base model — vast, fluent, knowledgeable, and useless: a mind without a manner, that answers your question with three more questions. This chapter is about the second, smaller, stranger training that gives it a manner — and about why the seams of that final shaping are exactly where a deployed model's most important behaviours, and its most dangerous failures, are quietly decided."
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
.sample-box {
  font-size: 0.82em;
  background: #0d1117;
  border: 1px solid #1e2d45;
  border-radius: 6px;
  padding: 0.9em 1.2em;
  margin: 1em 0;
  font-family: 'JetBrains Mono', monospace;
  color: #c9d6e8;
  line-height: 1.6;
}
.sample-box .label { color: #f59e0b; font-weight: bold; }
figure.diagram { margin: 2em 0; text-align: center; }
figure.diagram svg { max-width: 100%; height: auto; }
figure.diagram figcaption {
  font-size: 0.8em; color: #6b82a0; margin-top: 0.6em; text-align: left;
}
</style>

<div class="chapter-banner">
📖 <strong>Chapter Six of a ground-up account of how large language models work.</strong> The earlier chapters built the machine — <a href="/post/2026-07-17-the-grain-of-language">tokens</a>, <a href="/post/2026-07-18-the-prediction-game">meaning</a>, <a href="/post/2026-07-19-reading-the-room">attention</a>, <a href="/post/2026-07-20-the-tower">the tower</a> — and <a href="/post/2026-07-21-how-noise-becomes-knowledge">Chapter Five</a> filled it, turning a billion random numbers into a fluent, knowledgeable <em>base model</em> through the long descent of pretraining. But we ended on a warning: that base model is not the assistant you talk to. It is a mind without a manner. This chapter gives it one.
</div>

# Manners for a Mind: From Predictor to Assistant

<nav style="font-size:0.8em; background:#0d1117; border:1px solid #1e2d45; border-left:4px solid #00d4f5; border-radius:0 8px 8px 0; padding:0.9em 1.3em; margin:1.6em 0; line-height:1.95;">
<div style="color:#00d4f5; font-family:'JetBrains Mono',monospace; font-size:0.86em; letter-spacing:0.06em; margin-bottom:0.5em;">📚 HOW AN LLM WORKS · CONTENTS</div>
<span style="color:#6b82a0;">1.</span> <a href="/post/2026-07-17-the-grain-of-language">The Grain of Language</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">2.</span> <a href="/post/2026-07-18-the-prediction-game">The Prediction Game</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">3.</span> <a href="/post/2026-07-19-reading-the-room">Reading the Room</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">4.</span> <a href="/post/2026-07-20-the-tower">The Tower</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">5.</span> <a href="/post/2026-07-21-how-noise-becomes-knowledge">How Noise Becomes Knowledge</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">6.</span> <strong style="color:#f59e0b;">Manners for a Mind</strong> &nbsp;·&nbsp;
<span style="color:#6b82a0;">7.</span> <a href="/post/2026-07-23-meaning-you-can-search">Meaning You Can Search</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">8.</span> <a href="/post/2026-07-24-the-agent">The Agent</a>

<div style="margin-top:0.6em; padding-top:0.5em; border-top:1px solid #1e2d45;">📕 <a href="/static/How_an_LLM_Works.pdf" style="color:#f59e0b; font-weight:bold;">Download all eight chapters as a PDF book</a> <span style="color:#6b82a0;">— linked contents, ~66 pages</span></div>
</nav>

If you built and trained everything in the last five chapters — ground text into tokens, gave them meaning, built attention, stacked the tower, and ran the long descent until the loss flattened — you would hold in your hands one of the more remarkable artefacts humans have made: a base model. It has read a large fraction of everything ever written. It is fluent in dozens of languages, apparently knowledgeable across most of human endeavour, able to continue any text with uncanny plausibility.

And it would be almost useless to you.

Not because it lacks knowledge — it has more than any person alive. Because it lacks a *manner*. Ask it a question and it will not answer; it will *continue*, because continuing is the only thing it was ever trained to do. Type "What are the contraindications to thrombolysis?" and a base model might reply with three more exam-style questions, because on the internet a question like that is very often followed by others, in a revision guide or a viva. Nothing has malfunctioned. The model is doing precisely what Chapter Five rewarded it for: predicting the plausible continuation of a document. It has learned the shape of *all* text, which is emphatically not the same as the shape of *helpful* text.

This chapter is about the second training — the one that closes that gap. And I want to flag, up front, the single most surprising fact about it, because it reframes everything: **post-training adds almost no new machinery.** No new architecture. No new mechanism bolted onto the tower. Same weights, same attention, same feed-forward layers, same next-token interface we spent five chapters building. Only the *training signal* changes. Everything an assistant is — its helpfulness, its caution, its refusals, its manner — it is through the exact machine you already understand, nudged into a new posture. We are not building a new thing. We are teaching an existing thing to behave.

## Part I — Two objectives that only overlap

Let us name the mismatch precisely, because the whole chapter is an attempt to resolve it.

Pretraining optimised one objective: *continue the text the way this corpus would.* What we actually want from an assistant is a different objective: *respond to this person helpfully.* The trouble is that these two objectives are not the same — they merely *overlap*. A great deal of helpful text does appear on the internet, so a base model that continues well will often, by accident, be helpful. But the base model is aiming at the wrong target, and wherever the two targets diverge — wherever the most *plausible* continuation is not the most *helpful* response — it will follow plausibility every time.

<figure class="diagram">
<svg viewBox="0 0 720 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Two overlapping objectives: continue the text versus help the person">
  <rect x="0" y="0" width="720" height="340" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="30" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">TWO OBJECTIVES THAT ONLY OVERLAP</text>

  <circle cx="285" cy="180" r="105" fill="#0a4a5c" opacity="0.45" stroke="#00d4f5" stroke-width="1.5"/>
  <circle cx="435" cy="180" r="105" fill="#053d28" opacity="0.45" stroke="#10b981" stroke-width="1.5"/>

  <text x="215" y="150" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="12" font-weight="bold">continue</text>
  <text x="215" y="168" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="10.5">the text</text>
  <text x="215" y="200" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="9.5">(what pretraining</text>
  <text x="215" y="214" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="9.5">optimised)</text>

  <text x="505" y="150" text-anchor="middle" fill="#d3f5e6" font-family="sans-serif" font-size="12" font-weight="bold">help the</text>
  <text x="505" y="168" text-anchor="middle" fill="#8fd8b8" font-family="sans-serif" font-size="10.5">person</text>
  <text x="505" y="200" text-anchor="middle" fill="#8fd8b8" font-family="sans-serif" font-size="9.5">(what we actually</text>
  <text x="505" y="214" text-anchor="middle" fill="#8fd8b8" font-family="sans-serif" font-size="9.5">want)</text>

  <text x="360" y="176" text-anchor="middle" fill="#fdeccd" font-family="sans-serif" font-size="10.5" font-weight="bold">overlap</text>
  <text x="360" y="192" text-anchor="middle" fill="#f0c987" font-family="sans-serif" font-size="9">helpful text</text>
  <text x="360" y="205" text-anchor="middle" fill="#f0c987" font-family="sans-serif" font-size="9">that also exists</text>

  <text x="360" y="300" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11">Post-training's whole job: drag the model out of the blue region and into the green — so that “continue</text>
  <text x="360" y="320" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11">the text” and “respond helpfully” become, for this model, the same act.</text>
</svg>
<figcaption><strong>Figure 1.</strong> The base model lives in the blue circle — it continues text. We want it in the green — helping the person. They overlap, which is why a base model is <em>sometimes</em> useful, but they are not the same target. Post-training is the work of moving the model's default behaviour from one circle into the other.</figcaption>
</figure>

There are two ways to do that moving, applied in sequence, and they differ in a deep way: the first shows the model what to say, and the second lets it try and tells it which attempt was better. We take them in turn.

## Part II — Stage one: learning by demonstration

The first move is almost embarrassingly direct, and it reuses the entire machine of Chapter Five without modification.

We assemble a collection of *demonstration conversations* — tens or hundreds of thousands of them. Each is a small script: a user's message, followed by the response a good, careful assistant *should* give, written or curated by people. "Here is a question about thrombolysis; here is the calm, structured, honest answer we wish the model would produce." And then we simply continue training the base model on these conversations, with the exact loop from the last chapter — forward pass, measure the loss, backpropagate the blame, nudge the weights — except now the text it is learning to predict is the text of *good assistant responses*. This stage is called **instruction tuning** (you will also see it named supervised fine-tuning).

One detail makes the whole thing click into place with Chapter One, and it surprises almost everyone. A "conversation" is not a special data structure the model understands natively. It is presented to the model as exactly what everything is presented as — a flat sequence of tokens — with a few special marker tokens sprinkled in to delimit who is speaking:

<div class="sample-box">
&lt;|user|&gt; What are the contraindications to thrombolysis in acute stroke?<br/>
&lt;|assistant|&gt; The major contraindications fall into three groups: active bleeding risk, …<br/>
&lt;|end|&gt;
</div>

That is all a "chat" is: a document with role labels, learned as a convention like any other. The model is trained to predict the tokens of the *assistant* turns, given everything before them. When you had a conversation with an LLM this morning, the model received one long document in exactly this shape and did Chapter Four's forward pass on it, token by token. There is no chat engine hiding somewhere; there is only the tower, predicting the next token of a specially-formatted document.

<figure class="diagram">
<svg viewBox="0 0 720 330" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Instruction tuning: a conversation is a token sequence with role markers, trained with the same loop">
  <defs><marker id="ia6" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9 z" fill="#6b82a0"/></marker></defs>
  <rect x="0" y="0" width="720" height="330" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="30" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">INSTRUCTION TUNING — LEARN THE FORMAT BY EXAMPLE</text>

  <!-- token strip -->
  <g font-family="monospace" font-size="9.5">
    <rect x="40"  y="70" width="80"  height="30" rx="4" fill="#2e1e5e" stroke="#a78bfa"/><text x="80"  y="90" text-anchor="middle" fill="#e8e3fa">&lt;|user|&gt;</text>
    <rect x="124" y="70" width="150" height="30" rx="4" fill="#111827" stroke="#2a3f5f"/><text x="199" y="90" text-anchor="middle" fill="#c9d6e8">the question…</text>
    <rect x="278" y="70" width="95"  height="30" rx="4" fill="#0a4a5c" stroke="#00d4f5"/><text x="325" y="90" text-anchor="middle" fill="#d8f6fd">&lt;|assistant|&gt;</text>
    <rect x="377" y="70" width="230" height="30" rx="4" fill="#053d28" stroke="#10b981"/><text x="492" y="90" text-anchor="middle" fill="#d3f5e6">the ideal answer…</text>
    <rect x="611" y="70" width="70"  height="30" rx="4" fill="#111827" stroke="#2a3f5f"/><text x="646" y="90" text-anchor="middle" fill="#c9d6e8">&lt;|end|&gt;</text>
  </g>
  <text x="492" y="120" text-anchor="middle" fill="#10b981" font-family="sans-serif" font-size="10">↑ the model is trained to predict THESE tokens</text>

  <path d="M492,128 L492,150" stroke="#6b82a0" stroke-width="2" marker-end="url(#ia6)"/>

  <rect x="230" y="156" width="520" height="0" fill="none"/>
  <rect x="180" y="156" width="360" height="44" rx="8" fill="#4a3000" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="360" y="176" text-anchor="middle" fill="#fdeccd" font-family="sans-serif" font-size="11" font-weight="bold">the exact Chapter-Five loop</text>
  <text x="360" y="192" text-anchor="middle" fill="#f0c987" font-family="sans-serif" font-size="9.5">forward · loss · backprop · nudge — nothing new</text>

  <text x="360" y="246" text-anchor="middle" fill="#c9d6e8" font-family="sans-serif" font-size="11.5" font-weight="bold">After this stage, the mirror is gone: ask a question, get an answer.</text>
  <text x="360" y="272" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11">But demonstrations teach <tspan font-style="italic">format and typical content</tspan> — not fine judgement. And writing them by hand is slow</text>
  <text x="360" y="292" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11">and expensive, capping the model at “imitate a good human answer.” To go further we need a different kind of signal.</text>
</svg>
<figcaption><strong>Figure 2.</strong> Instruction tuning is just Chapter Five's training loop run on demonstration conversations, with the "chat format" revealed to be nothing more than role-marker tokens in an ordinary document. It works — the base model's mirror-like continuing gives way to answering. But it has two limits, and those limits are what the second stage exists to overcome.</figcaption>
</figure>

After instruction tuning, the transformation is real and immediate: the model that used to answer a question with more questions now answers it. But two gaps remain, and naming them sets up the second, more powerful stage. First, demonstrations teach *format and typical content*, but not *judgement* — the fine calls of how cautious to be, when to refuse, how to handle a request that is half-reasonable and half-dangerous, are poorly specified by examples alone. Second, hand-written demonstrations are expensive and slow, and they cap the model at "imitate a good human answer" when what we would really like is "produce the answer people actually *prefer* — even better than a demonstrator would have written."

## Part III — Stage two: learning from preferences

The second stage changes not the loop but the *kind of signal*. Instead of showing the model what to say, we let it generate, and we grade what it produces.

The core idea is a loop. Take a prompt. Let the model produce two (or more) different responses to it. Show a human rater both, and record only which one they *preferred*. Not a score out of ten — a simple choice: A or B. And notice the design wisdom hidden in that simplicity. Decades of measurement science, clinical assessment very much included, converge on the same finding: humans are unreliable at absolute ratings ("rate this answer 7/10") and far more consistent at forced choice ("which of these two is better?"). Preference data inherits that reliability. It is the same reason a good exam pairs a candidate against a standard rather than asking an examiner to conjure a number from the air.

Those thousands of comparisons are then used to train a second network — a **reward model** — built from the same transformer architecture, but with its final projection swapped: instead of a probability over the vocabulary, it outputs a single number, a learned estimate of "how much would a human prefer this response?" And finally, the assistant itself is nudged — by the same gradient-descent machinery — to produce responses the reward model scores highly, while being kept on a tether so it does not drift too far from its sensible instruction-tuned starting point.

<figure class="diagram">
<svg viewBox="0 0 720 400" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The preference loop: the model answers twice, a human picks the better, a reward model learns, the model is updated">
  <defs><marker id="pa6" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9 z" fill="#f59e0b"/></marker></defs>
  <rect x="0" y="0" width="720" height="400" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="30" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">THE PREFERENCE LOOP</text>

  <rect x="55" y="70" width="200" height="66" rx="10" fill="#0a4a5c" stroke="#00d4f5" stroke-width="1.5"/>
  <text x="155" y="98" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="12" font-weight="bold">model answers</text>
  <text x="155" y="116" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="10.5">the same prompt twice</text>

  <rect x="465" y="70" width="200" height="66" rx="10" fill="#2e1e5e" stroke="#a78bfa" stroke-width="1.5"/>
  <text x="565" y="98" text-anchor="middle" fill="#e8e3fa" font-family="sans-serif" font-size="12" font-weight="bold">human picks</text>
  <text x="565" y="116" text-anchor="middle" fill="#c9b8f5" font-family="sans-serif" font-size="10.5">the better one — A or B</text>

  <rect x="465" y="250" width="200" height="66" rx="10" fill="#053d28" stroke="#10b981" stroke-width="1.5"/>
  <text x="565" y="278" text-anchor="middle" fill="#d3f5e6" font-family="sans-serif" font-size="12" font-weight="bold">reward model learns</text>
  <text x="565" y="296" text-anchor="middle" fill="#8fd8b8" font-family="sans-serif" font-size="10.5">to predict the picks</text>

  <rect x="55" y="250" width="200" height="66" rx="10" fill="#4a3000" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="155" y="278" text-anchor="middle" fill="#fdeccd" font-family="sans-serif" font-size="12" font-weight="bold">model updated</text>
  <text x="155" y="296" text-anchor="middle" fill="#f0c987" font-family="sans-serif" font-size="10.5">toward higher-reward answers</text>

  <path d="M255,103 L460,103" stroke="#f59e0b" stroke-width="2" marker-end="url(#pa6)"/>
  <path d="M565,136 L565,246" stroke="#f59e0b" stroke-width="2" marker-end="url(#pa6)"/>
  <path d="M465,283 L259,283" stroke="#f59e0b" stroke-width="2" marker-end="url(#pa6)"/>
  <path d="M155,250 L155,140" stroke="#f59e0b" stroke-width="2" marker-end="url(#pa6)"/>

  <rect x="285" y="170" width="150" height="46" rx="8" fill="#111827" stroke="#2a3f5f"/>
  <text x="360" y="190" text-anchor="middle" fill="#c9d6e8" font-family="sans-serif" font-size="9.5">…kept tethered to the</text>
  <text x="360" y="205" text-anchor="middle" fill="#c9d6e8" font-family="sans-serif" font-size="9.5">instruction-tuned start</text>

  <text x="360" y="356" text-anchor="middle" fill="#f0c987" font-family="sans-serif" font-size="11" font-weight="bold">The target is not “the truth.” It is “what the reward model predicts a rater would prefer.”</text>
  <text x="360" y="378" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="10.5">Every gap between those two things is a failure mode waiting for deployment — the subject of Part V.</text>
</svg>
<figcaption><strong>Figure 3.</strong> The preference loop. It is optimisation against a <em>proxy</em>: not truth, but a model of human judgement, itself trained on judgements made quickly by raters who are rarely domain experts. That subtlety — optimising a stand-in for what we want, rather than the thing itself — is the seed of nearly everything that later goes wrong, and the reason the caption under this loop is the most important sentence in the chapter.</figcaption>
</figure>

<div class="keyidea">
💡 <strong>The idea to carry out of this chapter.</strong> Post-training optimises “what humans, as modelled, prefer” — not “what is true.” Usually these coincide, because people prefer correct, helpful answers when they can <em>tell</em>. But when correctness is hard for a rater to check, people reward confidence, fluency, agreement, and a definite answer over an honest “I don't know.” The model learns exactly that. Hold this single idea and the clinical failure modes below follow from it as corollaries, not surprises.
</div>

## Part IV — Same weights, different characters

Now the fact that strikes almost everyone as strange, and that quietly explains a great deal of an assistant's everyday behaviour: nothing was *removed* from the base model. Post-training is a comparatively gentle nudge in the vast space of weights. The enormous repertoire the base model built during pretraining — every register, persona, and viewpoint the internet contained, from a careful clinical discussion to an unhinged forum rant — is all still in there. What changed is not what the model *can* do, but what it *reaches for by default*.

The picture I find most faithful: pretraining built an immense landscape of possible behaviours, and a base model, prompted, falls into whichever region of that landscape the prompt statistically resembles. Post-training does not bulldoze regions. It *carves a groove* — a deep, comfortable channel labelled "helpful, harmless, honest assistant" — that the model now slides into from almost any starting point. The repertoire is untouched beneath; only the default has been reshaped.

<figure class="diagram">
<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Post-training carves a default groove into the base model's untouched repertoire of behaviours">
  <rect x="0" y="0" width="720" height="360" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="30" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">SAME WEIGHTS, DIFFERENT DEFAULT</text>
  <text x="360" y="50" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="10.5">the base repertoire (all of it still present) with an assistant groove carved through it</text>

  <!-- repertoire terrain -->
  <path d="M60,150 Q140,110 220,150 T380,150 T540,150 T680,150" stroke="#2a3f5f" stroke-width="2" fill="none"/>
  <text x="120" y="130" fill="#6b82a0" font-family="sans-serif" font-size="9">clinical voice</text>
  <text x="300" y="130" fill="#6b82a0" font-family="sans-serif" font-size="9">poetry</text>
  <text x="470" y="130" fill="#6b82a0" font-family="sans-serif" font-size="9">forum rant</text>
  <text x="610" y="130" fill="#6b82a0" font-family="sans-serif" font-size="9">code</text>

  <!-- the groove -->
  <path d="M60,250 Q200,250 300,255 Q360,258 420,255 Q560,250 680,250" stroke="#10b981" stroke-width="3" fill="none"/>
  <ellipse cx="360" cy="262" rx="120" ry="26" fill="#053d28" opacity="0.5"/>
  <circle cx="360" cy="262" r="9" fill="#10b981"/>
  <text x="360" y="300" text-anchor="middle" fill="#10b981" font-family="sans-serif" font-size="11" font-weight="bold">“helpful, harmless, honest assistant” — the carved default</text>

  <text x="360" y="332" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="10.5">The ball rests in the groove by default — but the whole terrain above is still reachable if something pulls it out.</text>
</svg>
<figcaption><strong>Figure 4.</strong> Post-training as a carved groove, not a bulldozer. The model's full range of behaviours survives; a deep default channel is cut so that it settles into "helpful assistant" from most prompts. This one picture explains three everyday facts at once, below.</figcaption>
</figure>

Three familiar observations fall straight out of that picture. **System prompts work** — a crafted instruction like "you are a terse triage assistant; answer in bullet points; escalate anything cardiac" cheaply repositions the model within its repertoire, because the groove is a default, not a cage. **Jailbreaks sometimes work** — an adversarial prompt is an attempt to *pull the model out of the groove* and back into some untamed region of the base repertoire that post-training made harder to reach but did not delete. And **fine-tuning works with astonishingly little data** — a few hundred examples can specialise a model, because you are not teaching it a subject from scratch; the knowledge is already there from pretraining, and you are merely relocating its default.

<div class="callout">
⚕️ <strong>The distinction that should change how you buy clinical AI.</strong> Pretraining is medical school and residency — years, enormous cost, and all the actual knowledge. Post-training is the induction week at a new hospital — quick, cheap, and it determines how you answer the phone, what you document, and when you escalate. Nobody would confuse induction week with medical school, yet in AI discourse the two are conflated constantly. So when a vendor tells you their model was “trained for healthcare,” your first question should be: <em>which of the two do you mean?</em> A model whose <em>pretraining</em> was rich in medicine is a different animal from one that merely had a medical induction week bolted onto a general base — and the answer changes everything about how you should validate it.
</div>

## Part V — The seams, and where the failures live

We can now do the thing this chapter was really for: read a deployed assistant's most important behaviours — and its most consequential failures — as direct consequences of the pipeline we have just built. None of what follows is a random glitch. Each is a seam of post-training, showing through.

**Sycophancy is a training artefact, not a personality quirk.** In the preference loop, agreeable answers win comparisons more often than blunt corrections — people, on average, prefer being agreed with. So the model acquires a measurable tilt toward endorsing whatever the user seems to believe. Put that in a clinical workflow and the danger is exact: the registrar types "elderly patient, fall, on apixaban, CT head clear, planning discharge — anything else?" and a sycophantic model is biased toward blessing the plan. The peril is precisely that it *feels* like a second opinion — it has the form of consultation with the incentives of a courtier. When you evaluate a clinical tool, test it with a wrong premise deliberately embedded and watch whether it pushes back. That single test tells you more than any accuracy benchmark.

**Confident fabrication survives — masked, not cured.** We watched the fluency-fidelity gap form in earlier chapters: statistical plausibility arrives long before factual grounding, at every scale. Post-training *reduces* fabrication, because raters do punish errors they can detect — but it cannot remove it, because the underlying generator is still a sampler over plausible continuations. And it adds a hazard of its own: the fabrications that survive are now delivered in the calm, structured, caveated register of a careful colleague, *because that is the register post-training rewards*. A base model's nonsense at least looked like nonsense. An assistant's nonsense looks like a well-written consult note with an invented reference in it.

**Refusals and caveats are a trained distribution — and it was calibrated for the public, not for you.** When a model declines, hedges, or says "consult a professional," it is following patterns learned from raters applying a policy — raters who were generally not clinicians, and a policy written for a general audience. So expect miscalibration at both ends in specialist use: over-refusal on legitimate clinical questions (an unusual but valid dosing scenario), and under-refusal where the surface framing looks benign. The calibration appropriate for a tool used *by clinicians* is simply different from one used *by the public* — and off-the-shelf assistants ship with the latter.

<figure class="diagram">
<svg viewBox="0 0 720 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The proxy gap: optimizing modelled preference rather than truth produces predictable failure modes">
  <rect x="0" y="0" width="720" height="340" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="30" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">THE PROXY GAP → PREDICTABLE FAILURES</text>

  <rect x="70" y="66" width="250" height="44" rx="8" fill="#053d28" stroke="#10b981" stroke-width="1.5"/>
  <text x="195" y="86" text-anchor="middle" fill="#d3f5e6" font-family="sans-serif" font-size="11" font-weight="bold">what we want</text>
  <text x="195" y="102" text-anchor="middle" fill="#8fd8b8" font-family="sans-serif" font-size="10">true, safe, genuinely helpful</text>

  <rect x="400" y="66" width="250" height="44" rx="8" fill="#4a3000" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="525" y="86" text-anchor="middle" fill="#fdeccd" font-family="sans-serif" font-size="11" font-weight="bold">what we optimise</text>
  <text x="525" y="102" text-anchor="middle" fill="#f0c987" font-family="sans-serif" font-size="10">what a rater is predicted to prefer</text>

  <text x="360" y="92" text-anchor="middle" fill="#f87171" font-family="monospace" font-size="16">≠</text>

  <!-- failure chips -->
  <g font-family="sans-serif">
    <rect x="55" y="150" width="300" height="52" rx="8" fill="#1a0c0c" stroke="#f87171" stroke-width="1.2"/>
    <text x="70" y="170" fill="#fde2e2" font-size="10.5" font-weight="bold">Sycophancy</text>
    <text x="70" y="188" fill="#e2a0a0" font-size="9.5">agreement wins comparisons → endorses your premise</text>

    <rect x="365" y="150" width="300" height="52" rx="8" fill="#1a0c0c" stroke="#f87171" stroke-width="1.2"/>
    <text x="380" y="170" fill="#fde2e2" font-size="10.5" font-weight="bold">Polished hallucination</text>
    <text x="380" y="188" fill="#e2a0a0" font-size="9.5">fabrication survives, now in a careful, caveated voice</text>

    <rect x="55" y="212" width="300" height="52" rx="8" fill="#1a0c0c" stroke="#f87171" stroke-width="1.2"/>
    <text x="70" y="232" fill="#fde2e2" font-size="10.5" font-weight="bold">Miscalibrated refusals</text>
    <text x="70" y="250" fill="#e2a0a0" font-size="9.5">policy tuned for the public, not the specialist</text>

    <rect x="365" y="212" width="300" height="52" rx="8" fill="#1a0c0c" stroke="#f87171" stroke-width="1.2"/>
    <text x="380" y="232" fill="#fde2e2" font-size="10.5" font-weight="bold">“The model said so” ≠ provenance</text>
    <text x="380" y="250" fill="#e2a0a0" font-size="9.5">nothing here connects a claim to a source</text>
  </g>

  <text x="360" y="298" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11">Each failure is the proxy showing through — the model doing exactly what it was rewarded to do, in a case</text>
  <text x="360" y="318" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11">where “what a rater would prefer” and “what is true and safe” quietly came apart.</text>
</svg>
<figcaption><strong>Figure 5.</strong> The failure modes of a deployed assistant, read off the pipeline. They are not bugs in the ordinary sense — no line of code is wrong. They are the predictable consequence of optimising a proxy for what we want, in the regions where the proxy and the goal diverge. Knowing <em>why</em> they occur is the difference between deploying carefully and deploying blindly.</figcaption>
</figure>

**And "the model said so" is not provenance.** This last one is the hinge to what comes next. Instruction tuning and preference learning teach a model to *present* answers beautifully — including confident, citation-shaped strings. But nothing in either stage connects an assertion to an actual source. The assistant's polish is not evidence; it is style, rewarded because style is what a hurried rater can judge. If you want an answer grounded in a document a human can open and check, the entire pipeline of this chapter cannot give it to you.

## Part VI — A complete mind, and its remaining blindness

Step back and take stock, because the machine is, in an important sense, now finished. Across six chapters we have ground text into tokens, given them meaning as geometry, built the attention that lets a token read the room, stacked it into a deep tower, filled that tower with knowledge through the long descent of pretraining, and — in this chapter — shaped the resulting base model into an assistant with a manner: something that answers, follows instructions, hedges, refuses, and speaks in the careful voice we asked for. That is, end to end, the thing you talk to. There is no further secret.

But look hard at what this finished assistant still cannot do, because it is precisely the shape of the final chapters. It knows only what pretraining happened to teach it — nothing about your hospital's formulary, nothing about the patient whose notes are open in front of you, nothing published after the day its training data was collected. And when it does not know, its post-training has taught it, too often, to answer anyway, fluently, in that trustworthy register, with a fabricated citation that no part of its training ever tied to a real source. It is a brilliant, well-mannered mind sealed inside the moment its training ended, with no way to look anything up and a trained disposition to bluff when it cannot.

Closing that gap — *without* the ruinous expense of retraining — means giving the model a way to reach outside itself: to search documents you control, pull the relevant passages into its context, and ground its answer in sources a human can inspect. Turning our sealed, fluent, occasionally-bluffing assistant into one that can *look things up and show its working* is the beginning of the machine's connection to the living world.

How that works — how text becomes searchable by *meaning*, and how retrieved passages are folded into the model's context to ground what it says — is Chapter Seven.

*— Neal*

<div class="chapter-banner">
📖 <strong>Next chapter:</strong> <em>Meaning You Can Search</em> — embeddings and retrieval. How documents become geometry, how a machine finds the right passage by meaning rather than keyword, and how grounding an answer in sources you control turns a sealed, bluffing assistant into one that can look things up and show its working.
</div>
