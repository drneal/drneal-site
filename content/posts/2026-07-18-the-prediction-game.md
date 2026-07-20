---
title: "The Prediction Game: How Tokens Learn to Mean Something"
date: 2026-07-18
category: Deep Learning
tags: next-token prediction, embeddings, meaning, vectors, LLM, probability, temperature, foundations, softmax
level: Beginner–Intermediate
read_time: 40 min
summary: "Chapter Two of a ground-up account of how large language models work. A model is handed a stream of tokens that mean nothing — arbitrary ID numbers — and a single, almost insultingly simple task: guess the next one. This is the story of why that one task is enough to summon everything an LLM can do, and of the quiet trick that turns a meaningless number into something that behaves like understanding: giving every token a place in space."
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
📖 <strong>Chapter Two of a ground-up account of how large language models work.</strong> In <a href="/post/2026-07-17-the-grain-of-language">Chapter One</a> we watched raw text from the internet get broken into tokens — the machine's self-made alphabet. But we left those tokens as what they really are at that stage: bare ID numbers, as meaningless as seat numbers at a stadium. This chapter is about the two ideas that breathe life into them.
</div>

# The Prediction Game: How Tokens Learn to Mean Something

<nav style="font-size:0.8em; background:#0d1117; border:1px solid #1e2d45; border-left:4px solid #00d4f5; border-radius:0 8px 8px 0; padding:0.9em 1.3em; margin:1.6em 0; line-height:1.95;">
<div style="color:#00d4f5; font-family:'JetBrains Mono',monospace; font-size:0.86em; letter-spacing:0.06em; margin-bottom:0.5em;">📚 HOW AN LLM WORKS · CONTENTS</div>
<span style="color:#6b82a0;">1.</span> <a href="/post/2026-07-17-the-grain-of-language">The Grain of Language</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">2.</span> <strong style="color:#f59e0b;">The Prediction Game</strong> &nbsp;·&nbsp;
<span style="color:#6b82a0;">3.</span> <a href="/post/2026-07-19-reading-the-room">Reading the Room</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">4.</span> <a href="/post/2026-07-20-the-tower">The Tower</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">5.</span> <a href="/post/2026-07-21-how-noise-becomes-knowledge">How Noise Becomes Knowledge</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">6.</span> <a href="/post/2026-07-22-manners-for-a-mind">Manners for a Mind</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">7.</span> <a href="/post/2026-07-23-meaning-you-can-search">Meaning You Can Search</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">8.</span> <a href="/post/2026-07-24-the-agent">The Agent</a>

<div style="margin-top:0.6em; padding-top:0.5em; border-top:1px solid #1e2d45;"><a href="/static/How_an_LLM_Works.pdf"><img src="/static/book_cover_icon.png" alt="How an LLM Works — book cover" style="height:2.8em; vertical-align:middle; border-radius:2px; box-shadow:0 1px 5px rgba(0,0,0,0.55); margin-right:0.55em;"></a><a href="/static/How_an_LLM_Works.pdf" style="color:#f59e0b; font-weight:bold;">Download all eight chapters as a PDF book</a> <span style="color:#6b82a0;">— linked contents, ~66 pages</span></div>
</nav>

At the close of the last chapter we had reduced a page of writing to a row of integers — token IDs, the grain into which language had been ground so a machine could swallow it. And I was careful to insist on something that should still be nagging at you: those integers mean *nothing*. Token 5,317 is not "closer" to token 5,318 than to token 90,001. The numbers are arbitrary labels, handed out in the order the tokenizer happened to build its vocabulary. If the model is ever going to seem to understand anything, that understanding cannot come from the numbers themselves. It has to be *built*.

This chapter is about how it gets built, and the answer comes in two movements that feel, at first, unrelated. The first is a goal — a single, almost comically modest task that the entire apparatus is trained to perform. The second is a transformation — the first thing the machine does to a token, which quietly turns a meaningless ID into something with the beginnings of meaning. By the end you will see that these two are not separate at all: the goal is what *creates* the meaning, as a kind of side effect, and that fact is the strangest and most important idea in the whole subject.

Let us take the goal first, because it is so small that its power is easy to miss.

## Part I — The whole game is "what comes next?"

Here is the entire objective a large language model is trained to accomplish. Ready?

Given a sequence of tokens, predict the next one.

That is it. That is the whole game. Not "understand the passage," not "answer the question," not "reason about the world" — just: here are some tokens, guess what token comes after them. A model that has read *"the patient was prescribed a course of"* is asked, simply, to fill in the blank. Antibiotics? Steroids? Physiotherapy? It must produce its best guess, and it is scored on nothing more than whether it matched the token that actually came next in some real piece of text.

The first time you hear this, it is genuinely deflating. All of it — the essays, the code, the eerie fluency, the appearance of thought — trained on a task you would set a parrot? It sounds like a category error, as though someone claimed that memorising a phone book could teach you to hold a conversation.

And then, if you sit with it, the deflation inverts into something closer to awe. Because think, really think, about what it would take to be *good* at this game. To reliably predict the next token in *any* text drawn from the whole internet, you cannot get by on surface tricks. Consider what predicting the blank actually demands across different sentences:

<div class="tokrow">
<span style="color:#6b82a0">“The capital of Kenya is ___”</span> &nbsp;→&nbsp; <span style="color:#8fd8b8">requires a fact</span><br/>
<span style="color:#6b82a0">“2, 4, 6, 8, ___”</span> &nbsp;→&nbsp; <span style="color:#8fd8b8">requires a pattern</span><br/>
<span style="color:#6b82a0">“She lied to him, so he no longer ___”</span> &nbsp;→&nbsp; <span style="color:#8fd8b8">requires a theory of people</span><br/>
<span style="color:#6b82a0">“def add(a, b): return a ___”</span> &nbsp;→&nbsp; <span style="color:#8fd8b8">requires the logic of code</span><br/>
<span style="color:#6b82a0">“The murderer, it turned out, was the ___”</span> &nbsp;→&nbsp; <span style="color:#8fd8b8">requires holding a whole story in mind</span>
</div>

To fill in the last blank correctly for a detective novel, the model would have to have tracked the plot, the clues, the misdirections — everything. The task is a keyhole, and behind the keyhole is a door that opens onto the whole of what the text was about. This is the pivotal realization of the entire field, and I want to state it as plainly as I can.

<div class="keyidea">
💡 <strong>The back-door of prediction.</strong> To predict the next token <em>well</em>, across all text, a system is forced to internalise whatever it takes to make that prediction — facts, grammar, patterns, cause and effect, the way people and stories behave. Understanding is not a separate goal bolted on top of prediction. It is the cheapest way to get good at prediction. We never asked the model to understand. We asked it to guess well, and understanding turned out to be the price of guessing well.
</div>

> A machine that could truly predict the next word of an arbitrary text would, somewhere inside itself, have to understand that text — and that back-door is the entire trick.

Everything downstream in this book — every capability, every failure — is a consequence of pushing a system relentlessly toward that one keyhole and seeing what it grows in order to fit through.

## Part II — The model never gives an answer. It gives a weather forecast.

There is a subtlety here that trips up almost everyone, and getting it right now will save you endless confusion later. When we say the model "predicts the next token," it is easy to picture it confidently declaring a single winner. That is not what happens, and the difference matters enormously.

The model does not output *a* token. It outputs a *probability for every token in the vocabulary at once* — all hundred thousand of them from Chapter One. Given *"the patient was prescribed a course of"*, its actual output is something like: `antibiotics` 41%, `steroids` 12%, `treatment` 9%, `physiotherapy` 4%, and a long, long tail of ever-smaller probabilities trailing off through every other token it knows, including the absurd ones. It is not an answer. It is a forecast — a full distribution of confidence spread across every possible next word.

<figure class="diagram">
<svg viewBox="0 0 720 430" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The model outputs a probability distribution over the whole vocabulary, then samples one token and feeds it back">
  <defs>
    <marker id="pa" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9 z" fill="#f59e0b"/></marker>
    <marker id="pc" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9 z" fill="#00d4f5"/></marker>
  </defs>
  <rect x="0" y="0" width="720" height="430" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="32" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">PREDICTION IS A FORECAST, NOT AN ANSWER</text>

  <!-- context -->
  <rect x="40" y="60" width="300" height="46" rx="8" fill="#2e1e5e" stroke="#a78bfa" stroke-width="1.5"/>
  <text x="190" y="80" text-anchor="middle" fill="#e8e3fa" font-family="sans-serif" font-size="11.5" font-weight="bold">the tokens so far</text>
  <text x="190" y="97" text-anchor="middle" fill="#bdaef0" font-family="monospace" font-size="10.5">“…prescribed a course of”</text>

  <rect x="400" y="60" width="150" height="46" rx="8" fill="#0a4a5c" stroke="#00d4f5" stroke-width="2"/>
  <text x="475" y="80" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="12" font-weight="bold">the model</text>
  <text x="475" y="97" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="10">one forward pass</text>
  <path d="M340,83 L394,83" stroke="#00d4f5" stroke-width="2" marker-end="url(#pc)"/>

  <!-- distribution bars -->
  <text x="60" y="150" fill="#c9d6e8" font-family="sans-serif" font-size="11.5" font-weight="bold">P(next token) — the whole vocabulary, ranked</text>
  <g font-family="monospace" font-size="11">
    <rect x="60" y="164" width="300" height="20" rx="3" fill="#10b981"/><text x="368" y="179" fill="#d3f5e6">antibiotics · 0.41</text>
    <rect x="60" y="190" width="150" height="20" rx="3" fill="#00d4f5"/><text x="218" y="205" fill="#d8f6fd">steroids · 0.12</text>
    <rect x="60" y="216" width="112" height="20" rx="3" fill="#00d4f5"/><text x="180" y="231" fill="#d8f6fd">treatment · 0.09</text>
    <rect x="60" y="242" width="60"  height="20" rx="3" fill="#f59e0b"/><text x="128" y="257" fill="#fdeccd">physiotherapy · 0.04</text>
    <rect x="60" y="268" width="30"  height="20" rx="3" fill="#a78bfa"/><text x="98"  y="283" fill="#e8e3fa">tablets · 0.02</text>
    <rect x="60" y="294" width="12"  height="20" rx="3" fill="#6b82a0"/><text x="80"  y="309" fill="#c9d6e8">… a very long tail of ever-tinier probabilities</text>
  </g>

  <!-- sample + loop -->
  <rect x="470" y="196" width="200" height="52" rx="10" fill="#4a3000" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="570" y="218" text-anchor="middle" fill="#fdeccd" font-family="sans-serif" font-size="12" font-weight="bold">draw ONE token</text>
  <text x="570" y="236" text-anchor="middle" fill="#f0c987" font-family="monospace" font-size="10.5">weighted by probability</text>
  <path d="M362,174 Q445,182 468,206" stroke="#f59e0b" stroke-width="1.5" fill="none" marker-end="url(#pa)"/>

  <path d="M570,248 L570,318 Q570,326 300,326 L40,326 Q28,326 28,110 L28,96 Q28,84 42,84" stroke="#f59e0b" stroke-width="2" fill="none" marker-end="url(#pa)"/>
  <text x="360" y="352" text-anchor="middle" fill="#f59e0b" font-family="sans-serif" font-size="11">append the drawn token to the context, and run the whole thing again — forever</text>

  <text x="360" y="398" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11">“Generating text” is this loop. A thousand-word reply is a thousand forecasts, each conditioned on the last.</text>
</svg>
<figcaption><strong>Figure 1.</strong> The generation loop. The model produces a distribution; a single token is <em>drawn</em> from it; that token is appended and the process repeats. Notice that the model does not plan a sentence — it commits to one token at a time, each choice reshaping the forecast for the next.</figcaption>
</figure>

This forecasting nature explains a fact everyone has noticed: ask the same model the same question twice and you may get two different answers. That is not a bug, and it is not the model "changing its mind." It is because generating text involves *drawing* from the distribution, and a draw has an element of chance. How much chance is governed by a single dial you have very likely met in an API or a settings panel: **temperature**. Turn the temperature down toward zero and the model almost always takes its single most probable token — reliable, repetitive, a little robotic. Turn it up and the draw gets more adventurous, reaching further into the tail — creative, surprising, and increasingly liable to wander into nonsense. Temperature is quite literally a knob on how much you let the dice matter.

<div class="callout">
🎲 <strong>Why "it's just autocomplete" is both fair and deeply misleading.</strong> The dismissive line contains a true observation — yes, mechanically, the model is completing text one probable token at a time, exactly like the suggestion strip above your phone keyboard. What the line misses is <em>everything about the difference in degree that becomes a difference in kind</em>. Your phone predicts the next word from the last two or three. This machine predicts it from thousands of prior tokens, using a model of the world it had to build in order to predict well. Calling it "just autocomplete" is like calling a surgeon "just someone with a knife." The verb is right; the noun is doing unimaginable work.
</div>

So: the goal is prediction, and the output is a forecast we sample from. But we still have not answered the question this chapter opened with. The forecast has to be *computed* from the input tokens — and the input tokens, remember, are meaningless integers. How does a meaningless integer participate in producing a rich probability distribution? For that, we need the second movement: the transformation that gives a token its first foothold on meaning.

## Part III — Giving every token a place in space

Here is the idea, and it is one of the most beautiful in all of machine learning. We are going to stop representing a token as a number, and start representing it as a *location*.

Picture a vast space — not the three dimensions we live in, but hundreds or thousands of them; hold the intuition even though you cannot picture the dimensions. Every token in the vocabulary is assigned a point in this space, specified by a list of numbers called a **vector** — its coordinates. The token `dog` is at one location; `cat` is at another; `lisinopril` at another still. This assignment — this big table mapping each of the hundred thousand tokens to its vector — is called the **embedding**, and the vectors are called embeddings too. It is, quite simply, the first thing that happens to a token once it enters the model: its ID is looked up in this table and swapped for its coordinates.

Now, why on earth would coordinates be better than a number? Because coordinates have *neighbours*, and neighbours can carry meaning. A single number line can only say "bigger" or "smaller." But a high-dimensional space can arrange its points so that **things with similar meaning sit close together**, and — this is the astonishing part — so that *directions* in the space correspond to *relationships*.

<figure class="diagram">
<svg viewBox="0 0 720 470" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A map of embedding space in which related medical concepts cluster and directions encode relationships">
  <rect x="0" y="0" width="720" height="470" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="30" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">MEANING BECOMES GEOMETRY</text>
  <text x="360" y="50" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="10.5">a flattened 2-D glimpse of a space that really has hundreds of dimensions</text>

  <!-- drug cluster -->
  <ellipse cx="185" cy="150" rx="130" ry="72" fill="#0a4a5c" opacity="0.30"/>
  <text x="185" y="100" text-anchor="middle" fill="#00d4f5" font-family="sans-serif" font-size="11" font-weight="bold">medications</text>
  <circle cx="146" cy="128" r="4" fill="#00d4f5"/><text x="185" y="132" text-anchor="middle" fill="#9fdcec" font-family="monospace" font-size="10">lisinopril</text>
  <circle cx="155" cy="152" r="4" fill="#00d4f5"/><text x="185" y="156" text-anchor="middle" fill="#9fdcec" font-family="monospace" font-size="10">aspirin</text>
  <circle cx="149" cy="176" r="4" fill="#00d4f5"/><text x="185" y="180" text-anchor="middle" fill="#9fdcec" font-family="monospace" font-size="10">metformin</text>

  <!-- symptom cluster -->
  <ellipse cx="540" cy="150" rx="130" ry="72" fill="#053d28" opacity="0.32"/>
  <text x="540" y="100" text-anchor="middle" fill="#10b981" font-family="sans-serif" font-size="11" font-weight="bold">symptoms</text>
  <circle cx="507" cy="128" r="4" fill="#10b981"/><text x="540" y="132" text-anchor="middle" fill="#8fd8b8" font-family="monospace" font-size="10">dyspnoea</text>
  <circle cx="513" cy="152" r="4" fill="#10b981"/><text x="540" y="156" text-anchor="middle" fill="#8fd8b8" font-family="monospace" font-size="10">oedema</text>
  <circle cx="510" cy="176" r="4" fill="#10b981"/><text x="540" y="180" text-anchor="middle" fill="#8fd8b8" font-family="monospace" font-size="10">fatigue</text>

  <!-- procedure cluster -->
  <ellipse cx="360" cy="360" rx="140" ry="66" fill="#2e1e5e" opacity="0.38"/>
  <text x="360" y="326" text-anchor="middle" fill="#a78bfa" font-family="sans-serif" font-size="11" font-weight="bold">procedures</text>
  <circle cx="318" cy="350" r="4" fill="#a78bfa"/><text x="360" y="354" text-anchor="middle" fill="#c9b8f5" font-family="monospace" font-size="10">angiography</text>
  <circle cx="309" cy="370" r="4" fill="#a78bfa"/><text x="360" y="374" text-anchor="middle" fill="#c9b8f5" font-family="monospace" font-size="10">echocardiogram</text>
  <circle cx="327" cy="390" r="4" fill="#a78bfa"/><text x="360" y="394" text-anchor="middle" fill="#c9b8f5" font-family="monospace" font-size="10">dialysis</text>

  <!-- relationship arrow: a consistent 'bearing' inside a cluster -->
  <defs><marker id="ra2" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L7,4 L0,8 z" fill="#f59e0b"/></marker></defs>
  <line x1="128" y1="178" x2="128" y2="126" stroke="#f59e0b" stroke-width="2.5" marker-end="url(#ra2)"/>

  <text x="360" y="440" text-anchor="middle" fill="#f0c987" font-family="sans-serif" font-size="11">Not only do similar things cluster — the <tspan font-style="italic">direction</tspan> from a drug to its class is roughly the same everywhere,</text>
  <text x="360" y="457" text-anchor="middle" fill="#f0c987" font-family="sans-serif" font-size="11">so relationships themselves become fixed compass bearings the model can follow.</text>
</svg>
<figcaption><strong>Figure 2.</strong> A cartoon of embedding space (real ones have hundreds of dimensions, which no picture can honestly show). Two properties matter: <em>proximity</em> encodes similarity, so the model can generalise from one drug to a related one it has seen less often; and <em>direction</em> encodes relationship, so the same "compass bearing" that points from a drug to its class points the same way for every drug at once.</figcaption>
</figure>

The famous demonstration of the direction idea, in ordinary-language embeddings, is almost a magic trick: take the vector for *king*, subtract the vector for *man*, add the vector for *woman*, and you land very near the vector for *queen*. The "royalty" and the "gender" of a word turn out to be *directions* you can travel along. In a medical embedding the same structure appears in our own vocabulary: *aspirin* is to *NSAID* roughly as *lisinopril* is to *ACE-inhibitor* — the "is-a-member-of-this-drug-class" relationship is a consistent bearing in the space. The model was never handed a drug classification. It reconstructed one, as geometry, purely from how these words are used.

<div class="keyidea">
💡 <strong>An embedding is a fixed address in a space where distance means dissimilarity of meaning.</strong> This single move — from arbitrary ID to meaningful coordinate — is what lets a model generalise at all. Having seen "lisinopril lowers blood pressure" a thousand times, it can make a sensible guess about "ramipril" the first time, because the two live in nearly the same neighbourhood. Without embeddings, every token would be an island. With them, meaning has a landscape, and the model can navigate it.
</div>

If this idea of meaning-as-geometry feels important, that is because it is: it returns, scaled up from single tokens to whole documents, when we reach the chapter on retrieval — the mechanism behind grounding a model in your own files. The geometry you are meeting here, at the level of one token, is the same geometry that will later let a machine search a library by meaning rather than by keyword. Learn it once, here, and it pays dividends twice.

## Part IV — Nobody puts the meaning there

Now for the part that genuinely borders on the uncanny, and that ties this chapter's two movements into a single knot.

Where does the arrangement of Figure 2 come from? Who decided that `aspirin` and `lisinopril` should be neighbours, that the drug-class direction should be consistent, that the space should be organised so beautifully? Surely a team of doctors sat down and placed the medical terms by hand?

No. Nobody placed anything. At the very start, before any training, the embedding table is filled with *random numbers*. Every token is flung to a random point in the space. `aspirin` and `poetry` and `dialysis` are scattered like buckshot, no cluster, no structure, no meaning whatsoever. The map begins as pure noise.

And then the prediction game begins. The model is shown ocean after ocean of real text and asked, over and over, to predict the next token — and every time it guesses, it is nudged to guess a little better. Crucially, those nudges do not only adjust some separate "prediction machinery." They reach all the way back and **move the embedding vectors themselves**. If treating `aspirin` and `ibuprofen` as neighbours helps the model predict text about pain relief, then the training gently slides their vectors together. If keeping `bank`-the-river and `bank`-the-money distinguishable helps, the training pulls on those too. Token by token, nudge by nudge, over billions of predictions, the random scatter organises itself into the landscape of meaning — not because meaning was the goal, but because a meaningful map is what makes the prediction game winnable.

<figure class="diagram">
<svg viewBox="0 0 720 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Embedding space begins as random scatter and organises into clusters as prediction training proceeds">
  <defs><marker id="ta" markerWidth="10" markerHeight="10" refX="7" refY="5" orient="auto"><path d="M0,0 L9,5 L0,10 z" fill="#f59e0b"/></marker></defs>
  <rect x="0" y="0" width="720" height="340" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="30" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">MEANING PRECIPITATES OUT OF PREDICTION</text>

  <!-- before -->
  <rect x="40" y="60" width="270" height="220" rx="10" fill="#0d1117" stroke="#3d0f0f" stroke-width="1.5"/>
  <text x="175" y="84" text-anchor="middle" fill="#f87171" font-family="sans-serif" font-size="12" font-weight="bold">before training — random noise</text>
  <circle cx="90"  cy="120" r="4" fill="#00d4f5"/><circle cx="250" cy="140" r="4" fill="#10b981"/>
  <circle cx="140" cy="210" r="4" fill="#a78bfa"/><circle cx="210" cy="105" r="4" fill="#00d4f5"/>
  <circle cx="80"  cy="250" r="4" fill="#10b981"/><circle cx="270" cy="230" r="4" fill="#a78bfa"/>
  <circle cx="180" cy="160" r="4" fill="#10b981"/><circle cx="120" cy="130" r="4" fill="#a78bfa"/>
  <circle cx="240" cy="190" r="4" fill="#00d4f5"/><circle cx="160" cy="245" r="4" fill="#00d4f5"/>
  <circle cx="100" cy="180" r="4" fill="#a78bfa"/><circle cx="220" cy="255" r="4" fill="#10b981"/>
  <text x="175" y="272" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="10">no clusters · every token an island</text>

  <path d="M325,172 L395,172" stroke="#f59e0b" stroke-width="2.5" marker-end="url(#ta)"/>
  <text x="360" y="150" text-anchor="middle" fill="#f0c987" font-family="sans-serif" font-size="10">billions of</text>
  <text x="360" y="206" text-anchor="middle" fill="#f0c987" font-family="sans-serif" font-size="10">predictions</text>

  <!-- after -->
  <rect x="410" y="60" width="270" height="220" rx="10" fill="#0d1117" stroke="#053d28" stroke-width="1.5"/>
  <text x="545" y="84" text-anchor="middle" fill="#10b981" font-family="sans-serif" font-size="12" font-weight="bold">after training — organised meaning</text>
  <ellipse cx="470" cy="130" rx="40" ry="30" fill="#0a4a5c" opacity="0.4"/>
  <circle cx="458" cy="122" r="4" fill="#00d4f5"/><circle cx="480" cy="132" r="4" fill="#00d4f5"/><circle cx="470" cy="145" r="4" fill="#00d4f5"/>
  <ellipse cx="610" cy="140" rx="40" ry="30" fill="#053d28" opacity="0.5"/>
  <circle cx="598" cy="132" r="4" fill="#10b981"/><circle cx="620" cy="142" r="4" fill="#10b981"/><circle cx="610" cy="155" r="4" fill="#10b981"/>
  <ellipse cx="540" cy="225" rx="44" ry="30" fill="#2e1e5e" opacity="0.5"/>
  <circle cx="525" cy="218" r="4" fill="#a78bfa"/><circle cx="552" cy="227" r="4" fill="#a78bfa"/><circle cx="542" cy="238" r="4" fill="#a78bfa"/>
  <text x="545" y="272" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="10">like clusters with like · relationships aligned</text>
</svg>
<figcaption><strong>Figure 3.</strong> The map is not designed; it is grown. Training on the prediction game reaches back and rearranges the embedding vectors themselves, so that the geometry of meaning condenses out of the single pressure to guess the next token well. We will open up exactly <em>how</em> a guess reaches back and moves a vector in a later chapter on training — for now, the point is simply that meaning is discovered, not installed.</figcaption>
</figure>

Pause on this, because it is the philosophical heart of the whole enterprise and it is almost never stated plainly. We did not teach the model what words mean. We could not have — nobody has a complete theory of what words mean. Instead we set up a game in which having a good internal model of meaning is *rewarded*, pointed the machine at a large fraction of everything humans have written, and let meaning *precipitate* out of the relentless pressure to predict. The understanding these systems have — such as it is — was not authored. It was distilled.

<div class="callout">
⚕️ <strong>A double-edged gift for those of us in medicine.</strong> The upside is remarkable: the model builds its own nosology, its own web of how clinical concepts relate, without ever being handed a textbook taxonomy — and that is why it can move so fluently across medicine. But look at the mechanism again. The map is distilled from <em>how words are used in the training text</em>. So if the text of the internet associates certain conditions with certain groups, certain symptoms with certain demographics, or reflects the historical blind spots of the medical literature, those associations do not merely appear in the output — they are baked into the very geometry, as distances and directions. The model's biases are not slogans it repeats. They are the shape of its space. That is a far harder thing to find, and to fix, than a bad sentence.
</div>

## Part V — The gap a lone vector cannot cross

We have come a long way. Tokens have become points in a meaningful space; the space organised itself through the prediction game; and the game, we argued, is a keyhole onto genuine understanding. It would be easy to feel we are nearly done — that a model is just a big embedding table plus some machinery to read off predictions. But there is a crack in what we have built so far, and finding it precisely is what sets up everything to come.

Here is the crack. The embedding of a token is *fixed*. `bank` gets one vector, always the same, no matter where it appears. But consider two sentences:

<div class="tokrow">
<span style="color:#8fd8b8">“He sat on the <span style="color:#f59e0b">bank</span> of the river and watched the current.”</span><br/>
<span style="color:#8fd8b8">“He deposited the cheque at the <span style="color:#f59e0b">bank</span> on the corner.”</span>
</div>

The word `bank` means something utterly different in each — a muddy riverside in one, a financial institution in the other. Yet the embedding table, knowing nothing of context, hands over the *identical* vector for `bank` both times. A fixed point in space simply cannot be a riverbank here and a savings bank there. The single most important word for the meaning of each sentence arrives at the model wearing the same blank mask.

<figure class="diagram">
<svg viewBox="0 0 720 350" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="One fixed embedding for the word bank cannot serve two different meanings without looking at its neighbours">
  <defs><marker id="ga" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9 z" fill="#6b82a0"/></marker></defs>
  <rect x="0" y="0" width="720" height="350" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="30" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">THE PROBLEM A FIXED VECTOR CANNOT SOLVE</text>

  <!-- one vector in the middle -->
  <rect x="300" y="150" width="120" height="46" rx="10" fill="#4a3000" stroke="#f59e0b" stroke-width="2"/>
  <text x="360" y="170" text-anchor="middle" fill="#fdeccd" font-family="monospace" font-size="13" font-weight="bold">“bank”</text>
  <text x="360" y="186" text-anchor="middle" fill="#f0c987" font-family="sans-serif" font-size="9.5">one fixed vector</text>

  <!-- sentence 1 -->
  <rect x="40" y="70" width="250" height="44" rx="8" fill="#0a4a5c" stroke="#00d4f5" stroke-width="1.5"/>
  <text x="165" y="89" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="10.5">“…the bank of the river…”</text>
  <text x="165" y="104" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="10">needs: riverside</text>
  <path d="M290,100 Q330,130 342,150" stroke="#6b82a0" stroke-width="1.5" fill="none" marker-end="url(#ga)"/>

  <!-- sentence 2 -->
  <rect x="430" y="70" width="250" height="44" rx="8" fill="#053d28" stroke="#10b981" stroke-width="1.5"/>
  <text x="555" y="89" text-anchor="middle" fill="#d3f5e6" font-family="sans-serif" font-size="10.5">“…deposited it at the bank…”</text>
  <text x="555" y="104" text-anchor="middle" fill="#8fd8b8" font-family="sans-serif" font-size="10">needs: institution</text>
  <path d="M430,100 Q390,130 378,150" stroke="#6b82a0" stroke-width="1.5" fill="none" marker-end="url(#ga)"/>

  <text x="360" y="240" text-anchor="middle" fill="#f87171" font-family="sans-serif" font-size="12" font-weight="bold">The same mask arrives for two opposite meanings.</text>
  <text x="360" y="266" text-anchor="middle" fill="#c9d6e8" font-family="sans-serif" font-size="11.5">The only cure: let the token <tspan font-style="italic">look at its neighbours</tspan> — “river”, “deposited” — and</text>
  <text x="360" y="286" text-anchor="middle" fill="#c9d6e8" font-family="sans-serif" font-size="11.5">adjust its own meaning in light of the company it keeps.</text>
  <text x="360" y="318" text-anchor="middle" fill="#00d4f5" font-family="monospace" font-size="12">that adjustment-by-context has a name — and it is the whole of Chapter Three</text>
</svg>
<figcaption><strong>Figure 4.</strong> The limitation that motivates everything next. A static embedding captures a token's meaning <em>in isolation</em>, which is genuinely useful — but language is not made of isolated words. Meaning is contextual. To resolve "bank", the token must be allowed to gather information from the words around it and update itself accordingly. Naming that operation precisely is the doorway out of this chapter.</figcaption>
</figure>

So we need something more. We need a token, once it has been given its starting vector, to *look around* — to see that "river" and "current" are nearby in one sentence and "deposited" and "cheque" in the other, and to let that company reshape its own meaning before any prediction is made. We need each token to stop being a fixed point and become a point that *adjusts itself in light of its neighbours*.

This is not a small tweak. It is the central mechanism of the entire architecture — the thing that separates a modern language model from every earlier attempt, the idea that made all of this work at last. It has a name, and you have heard the name even if you have never been shown what is under it.

It is called **attention**. It is the reason these models are built the way they are. And building it, from nothing, so that you understand not just what it does but *why it was the answer everyone was reaching for* — that is Chapter Three.

For now, hold the shape of what we have. A token enters as a meaningless number. It is handed a place in a vast space of meaning — a place that was not designed but grown, distilled out of the single pressure to predict what comes next. And there it sits, rich but static, wearing the same face in every sentence, waiting for permission to turn its head and look at the words around it.

We are about to grant that permission. And when we do, the whole thing comes alive.

*— Neal*

<div class="chapter-banner">
📖 <strong>Next chapter:</strong> <em>Attention</em> — how a token learns to look at its neighbours and become a different thing in every sentence. It is the idea at the dead centre of every large language model, and we will build it from first principles, one honest step at a time.
</div>
