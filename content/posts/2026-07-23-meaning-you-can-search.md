---
title: "Meaning You Can Search: Embeddings, Retrieval, and Grounding"
date: 2026-07-23
category: Deep Learning
tags: embeddings, retrieval, RAG, vector search, semantic search, grounding, provenance, LLM, clinical AI, foundations
level: Intermediate
read_time: 40 min
summary: "Chapter Seven of a ground-up account of how large language models work. The assistant we finished building is sealed inside the moment its training ended — it knows nothing of your documents, and it bluffs when it does not know. This chapter gives it a way to reach outside itself: to turn text into geometry, search a body of knowledge by meaning rather than by keyword, and ground its answers in sources a human can open and check. It is the machine's first honest connection to the living world."
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
figure.diagram { margin: 2em 0; text-align: center; }
figure.diagram svg { max-width: 100%; height: auto; }
figure.diagram figcaption {
  font-size: 0.8em; color: #6b82a0; margin-top: 0.6em; text-align: left;
}
</style>

<div class="chapter-banner">
📖 <strong>Chapter Seven of a ground-up account of how large language models work.</strong> Across six chapters we built a complete assistant — <a href="/post/2026-07-17-the-grain-of-language">tokens</a>, <a href="/post/2026-07-18-the-prediction-game">meaning</a>, <a href="/post/2026-07-19-reading-the-room">attention</a>, <a href="/post/2026-07-20-the-tower">the tower</a>, <a href="/post/2026-07-21-how-noise-becomes-knowledge">training</a>, and the <a href="/post/2026-07-22-manners-for-a-mind">manners</a> that made it helpful. And we ended on its defining blindness: it knows only what pretraining happened to teach it, and it has been trained to answer anyway — fluently — even when it does not know. This chapter opens a window.
</div>

# Meaning You Can Search: Embeddings, Retrieval, and Grounding

<nav style="font-size:0.8em; background:#0d1117; border:1px solid #1e2d45; border-left:4px solid #00d4f5; border-radius:0 8px 8px 0; padding:0.9em 1.3em; margin:1.6em 0; line-height:1.95;">
<div style="color:#00d4f5; font-family:'JetBrains Mono',monospace; font-size:0.86em; letter-spacing:0.06em; margin-bottom:0.5em;">📚 HOW AN LLM WORKS · CONTENTS</div>
<span style="color:#6b82a0;">1.</span> <a href="/post/2026-07-17-the-grain-of-language">The Grain of Language</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">2.</span> <a href="/post/2026-07-18-the-prediction-game">The Prediction Game</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">3.</span> <a href="/post/2026-07-19-reading-the-room">Reading the Room</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">4.</span> <a href="/post/2026-07-20-the-tower">The Tower</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">5.</span> <a href="/post/2026-07-21-how-noise-becomes-knowledge">How Noise Becomes Knowledge</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">6.</span> <a href="/post/2026-07-22-manners-for-a-mind">Manners for a Mind</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">7.</span> <strong style="color:#f59e0b;">Meaning You Can Search</strong> &nbsp;·&nbsp;
<span style="color:#6b82a0;">8.</span> <a href="/post/2026-07-24-the-agent">The Agent</a>

<div style="margin-top:0.6em; padding-top:0.5em; border-top:1px solid #1e2d45;"><a href="/static/How_an_LLM_Works.pdf"><img src="/static/book_cover_icon.png" alt="How an LLM Works — book cover" style="height:2.8em; vertical-align:middle; border-radius:2px; box-shadow:0 1px 5px rgba(0,0,0,0.55); margin-right:0.55em;"></a><a href="/static/How_an_LLM_Works.pdf" style="color:#f59e0b; font-weight:bold;">Download all eight chapters as a PDF book</a> <span style="color:#6b82a0;">— linked contents, ~66 pages</span></div>
</nav>

The assistant we finished in the last chapter has a strange and specific kind of ignorance, and it is worth stating precisely, because the whole of this chapter is a response to it.

It is not that the assistant knows too little. It knows an extraordinary amount — a compressed, blurry impression of a large fraction of everything ever written, up to the day its training data was collected. The problem is threefold and exact. It knows nothing that was written *after* that day. It knows nothing that was never *public* — not your hospital's formulary, not the protocol your department agreed last month, not the notes of the patient in front of you. And, as Chapter Six established, when it does not know, it has been trained to produce a confident, well-mannered answer regardless, sometimes complete with a citation that corresponds to no real source. It is a brilliant mind, sealed inside a moment, with a trained disposition to bluff.

You might imagine the fix is to retrain it on the missing knowledge. For facts, this is almost always the wrong tool — we saw why in Chapter Five. Pretraining is a months-long, multi-million-dollar industrial process, and the lighter fine-tuning of Chapter Six relocates a model's *defaults*, not its reliably-recallable knowledge. What we actually want is something far more surgical: at the very moment a question is asked, *reach into a body of documents we control, find the passages that bear on it, and lay them in front of the model as part of its context* — so that when the model does its Chapter Four forward pass, the evidence is already on the page. The model then does what it has always done, continue the text, except the text now contains the facts.

That is **retrieval-augmented generation** — RAG — and it rests on a single idea of real beauty, one we have already met in miniature and now scale up: that meaning itself can be given coordinates.

## Part I — The same geometry, scaled up

Cast your mind back to Chapter Two. We took each *token* and gave it a vector — a location in a high-dimensional space arranged so that tokens with similar meaning sit near each other, and directions encode relationships. I promised, at the time, that this idea would return, scaled up from single tokens to whole documents. Here it is.

An **embedding model** — itself a transformer, trained for precisely this one job — reads an entire sentence, paragraph, or passage and outputs a *single* vector that represents the meaning of the whole thing. And it is trained so that **passages with similar meaning land near each other in the space**. Not similar *wording* — similar *meaning*. This distinction is the entire point, so let me make it concrete. A good embedding model places "the patient developed an itchy rash after her first dose of amoxicillin" close to "penicillin allergy — urticaria documented," and far from "the rash resolved after the statin was stopped" — even though, word for word, the sentence about the statin shares more vocabulary with the first than the allergy note does. Meaning, not surface, decides proximity.

How does it learn to do that? By training on contrast, at scale — shown millions of pairs known to be related (a question and its answer, a title and its abstract, two paraphrases of one sentence) and nudged, by the same gradient descent of Chapter Five, to pull related pairs together and push unrelated ones apart, until distance in the space *means* dissimilarity of meaning.

<figure class="diagram">
<svg viewBox="0 0 720 470" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Document passages as points in embedding space, clustered by meaning, with a query landing near the right cluster">
  <rect x="0" y="0" width="720" height="470" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="30" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">A MAP OF DOCUMENTS BY MEANING</text>
  <text x="360" y="50" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="10.5">a flattened glimpse of a space with hundreds of dimensions — each dot is a whole passage</text>

  <!-- anticoag cluster -->
  <ellipse cx="180" cy="160" rx="135" ry="76" fill="#0a4a5c" opacity="0.32"/>
  <text x="180" y="104" text-anchor="middle" fill="#00d4f5" font-family="sans-serif" font-size="11" font-weight="bold">anticoagulation</text>
  <circle cx="100" cy="147" r="4" fill="#00d4f5"/><text x="180" y="150" text-anchor="middle" fill="#9fdcec" font-family="monospace" font-size="9">“hold apixaban 48h pre-op”</text>
  <circle cx="103" cy="175" r="4" fill="#00d4f5"/><text x="180" y="178" text-anchor="middle" fill="#9fdcec" font-family="monospace" font-size="9">“warfarin INR target 2–3”</text>

  <!-- allergy cluster -->
  <ellipse cx="545" cy="160" rx="140" ry="76" fill="#053d28" opacity="0.34"/>
  <text x="545" y="104" text-anchor="middle" fill="#10b981" font-family="sans-serif" font-size="11" font-weight="bold">drug allergy</text>
  <circle cx="457" cy="147" r="4" fill="#10b981"/><text x="545" y="150" text-anchor="middle" fill="#8fd8b8" font-family="monospace" font-size="9">“urticaria after amoxicillin”</text>
  <circle cx="481" cy="175" r="4" fill="#10b981"/><text x="545" y="178" text-anchor="middle" fill="#8fd8b8" font-family="monospace" font-size="9">“penicillin allergy”</text>

  <!-- lipids cluster -->
  <ellipse cx="360" cy="360" rx="140" ry="68" fill="#2e1e5e" opacity="0.4"/>
  <text x="360" y="312" text-anchor="middle" fill="#a78bfa" font-family="sans-serif" font-size="11" font-weight="bold">lipid management</text>
  <circle cx="269" cy="349" r="4" fill="#a78bfa"/><text x="360" y="352" text-anchor="middle" fill="#c9b8f5" font-family="monospace" font-size="9">“rash resolved off the statin”</text>
  <circle cx="296" cy="379" r="4" fill="#a78bfa"/><text x="360" y="382" text-anchor="middle" fill="#c9b8f5" font-family="monospace" font-size="9">“LDL target post-MI”</text>

  <!-- query -->
  <circle cx="510" cy="220" r="8" fill="none" stroke="#f59e0b" stroke-width="2.5"/>
  <circle cx="510" cy="220" r="3" fill="#f59e0b"/>
  <text x="405" y="250" fill="#f59e0b" font-family="sans-serif" font-size="10.5" font-weight="bold">query: “can this patient have co-amoxiclav?”</text>
  <line x1="510" y1="212" x2="520" y2="184" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="4,3"/>

  <text x="360" y="440" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11">The query lands nearest the allergy cluster — although “co-amoxiclav” appears in none of those passages,</text>
  <text x="360" y="457" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11">and “rash” appears in the <tspan font-style="italic">wrong</tspan> one. Meaning-distance routes it correctly. This is retrieval by concept, not string.</text>
</svg>
<figcaption><strong>Figure 1.</strong> Chapter Two's geometry, now at the scale of whole passages. Note the decisive win over old-fashioned keyword search: the question about co-amoxiclav shares no words with the penicillin-allergy note, and the word "rash" sits in the lipid cluster — yet the query still lands where it should, because the embedding model matches on meaning. A keyword search would have missed the most important note in the chart.</figcaption>
</figure>

<div class="keyidea">
💡 <strong>The reduction that powers everything.</strong> An embedding turns a piece of text into a fixed address in a space where distance means dissimilarity of meaning. Once text is geometry, the vague task "find the documents relevant to this question" becomes the crisp, ancient, computationally-cheap task "find the nearest points to this point." That single reduction — meaning to coordinates, relevance to distance — is what makes semantic search, retrieval, and the memory of an AI system all possible with the same machinery.
</div>

Two practical notes before we build with it. Similarity between two vectors is usually measured by the *cosine* of the angle between them — how nearly they point the same way, ignoring their lengths. And searching for nearest neighbours among millions of vectors is made fast by specialised indexes (the "vector databases" you may have heard named are, at heart, exactly this index plus bookkeeping). At the scale of a single clinic — thousands of documents — you do not even need them; comparing a query against every stored vector takes milliseconds.

## Part II — The pipeline: two lanes meeting at the context window

With embeddings in hand, retrieval-augmented generation is two pipelines that meet at a single point — the model's context window from Chapter Four.

The first lane is done *once*, ahead of time, and refreshed on a schedule. Take your documents — guidelines, protocols, papers, notes. Cut them into passages of a manageable size (this "chunking" step is quietly one of the most consequential choices in the whole system, and we will see why in Part V). Run every chunk through the embedding model to get its vector. Store the vectors, alongside the original text and a note of where each came from, in an index. That is the ingestion lane: a library, converted into searchable geometry.

The second lane runs *every time a question is asked*. Embed the question with the same model, into the same space. Find its nearest neighbours in the index — the handful of chunks whose meaning sits closest to the question. Then assemble a prompt that places those retrieved passages, plus the question, plus a clear instruction, into the model's context window — and let the model answer.

<figure class="diagram">
<svg viewBox="0 0 720 500" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The RAG pipeline: an ingestion lane and a question lane meeting at the context window">
  <defs><marker id="ra7" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9 z" fill="#6b82a0"/></marker></defs>
  <rect x="0" y="0" width="720" height="500" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="30" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">RAG: TWO LANES, ONE CONTEXT WINDOW</text>

  <text x="185" y="60" text-anchor="middle" fill="#00d4f5" font-family="sans-serif" font-size="12" font-weight="bold">INGESTION — once, refreshed on a schedule</text>
  <text x="545" y="60" text-anchor="middle" fill="#10b981" font-family="sans-serif" font-size="12" font-weight="bold">QUESTION TIME — every query</text>

  <!-- ingestion -->
  <rect x="60" y="74" width="250" height="48" rx="9" fill="#111827" stroke="#00d4f5" stroke-width="1.3"/><text x="185" y="94" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="11" font-weight="bold">your documents</text><text x="185" y="110" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="9.5">guidelines · protocols · notes</text>
  <path d="M185,122 L185,138" stroke="#6b82a0" stroke-width="2" marker-end="url(#ra7)"/>
  <rect x="60" y="142" width="250" height="48" rx="9" fill="#111827" stroke="#00d4f5" stroke-width="1.3"/><text x="185" y="162" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="11" font-weight="bold">chunk into passages</text><text x="185" y="178" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="9.5">a fraught choice — see Part V</text>
  <path d="M185,190 L185,206" stroke="#6b82a0" stroke-width="2" marker-end="url(#ra7)"/>
  <rect x="60" y="210" width="250" height="48" rx="9" fill="#111827" stroke="#00d4f5" stroke-width="1.3"/><text x="185" y="230" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="11" font-weight="bold">embed each chunk</text><text x="185" y="246" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="9.5">one vector per passage</text>
  <path d="M185,258 L185,274" stroke="#6b82a0" stroke-width="2" marker-end="url(#ra7)"/>
  <rect x="60" y="278" width="250" height="48" rx="9" fill="#0a4a5c" stroke="#00d4f5" stroke-width="2"/><text x="185" y="298" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="11" font-weight="bold">the index</text><text x="185" y="314" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="9.5">vectors + text + source</text>

  <!-- question -->
  <rect x="410" y="74" width="250" height="48" rx="9" fill="#111827" stroke="#10b981" stroke-width="1.3"/><text x="535" y="94" text-anchor="middle" fill="#d3f5e6" font-family="sans-serif" font-size="11" font-weight="bold">the question</text><text x="535" y="110" text-anchor="middle" fill="#8fd8b8" font-family="sans-serif" font-size="9.5">“perioperative DOAC plan?”</text>
  <path d="M535,122 L535,138" stroke="#6b82a0" stroke-width="2" marker-end="url(#ra7)"/>
  <rect x="410" y="142" width="250" height="48" rx="9" fill="#111827" stroke="#10b981" stroke-width="1.3"/><text x="535" y="162" text-anchor="middle" fill="#d3f5e6" font-family="sans-serif" font-size="11" font-weight="bold">embed the question</text><text x="535" y="178" text-anchor="middle" fill="#8fd8b8" font-family="sans-serif" font-size="9.5">same model, same space</text>
  <path d="M535,190 L535,206" stroke="#6b82a0" stroke-width="2" marker-end="url(#ra7)"/>
  <rect x="410" y="210" width="250" height="48" rx="9" fill="#111827" stroke="#10b981" stroke-width="1.3"/><text x="535" y="230" text-anchor="middle" fill="#d3f5e6" font-family="sans-serif" font-size="11" font-weight="bold">nearest neighbours</text><text x="535" y="246" text-anchor="middle" fill="#8fd8b8" font-family="sans-serif" font-size="9.5">the closest chunks from the index</text>
  <path d="M310,302 Q380,302 408,250" stroke="#00d4f5" stroke-width="2" fill="none" marker-end="url(#ra7)"/>
  <path d="M535,258 L535,274" stroke="#6b82a0" stroke-width="2" marker-end="url(#ra7)"/>

  <!-- context window -->
  <rect x="115" y="360" width="490" height="62" rx="9" fill="#4a3000" stroke="#f59e0b" stroke-width="2"/>
  <text x="360" y="384" text-anchor="middle" fill="#fdeccd" font-family="sans-serif" font-size="12" font-weight="bold">context window: question + retrieved passages + instruction</text>
  <text x="360" y="404" text-anchor="middle" fill="#f0c987" font-family="sans-serif" font-size="9.5">“Answer only from the passages below. Cite each claim. Say so if they don't contain the answer.”</text>
  <path d="M535,278 Q535,340 470,360" stroke="#6b82a0" stroke-width="2" fill="none" marker-end="url(#ra7)"/>

  <path d="M360,422 L360,438" stroke="#6b82a0" stroke-width="2" marker-end="url(#ra7)"/>
  <rect x="235" y="442" width="250" height="42" rx="9" fill="#053d28" stroke="#10b981" stroke-width="1.5"/>
  <text x="360" y="468" text-anchor="middle" fill="#d3f5e6" font-family="sans-serif" font-size="12" font-weight="bold">grounded answer, with citations</text>
</svg>
<figcaption><strong>Figure 2.</strong> The full pipeline. The vital thing to notice: <em>the model itself is unchanged</em> — the same weights from Chapter Six, doing the same forward pass from Chapter Four. Every piece of new engineering lives <em>outside</em> the model, in the machinery that decides what gets placed into its context window. Fresh knowledge is one re-index away, no retraining involved.</figcaption>
</figure>

Sit with the modesty of that architecture for a moment, because it is easy to miss how much it buys. We did not touch the model. We built a search engine over documents we control, and we arranged for its results to be handed to the model as reading material at the instant of the question. The two instructions in that context window — *answer only from these passages* and *say so if they don't contain the answer* — are what do the safety work, converting a bluffing generalist into a grounded specialist for the length of one reply.

## Part III — Why this beats retraining, and heals Chapter Six's wound

It is worth being crisp about why retrieval, and not fine-tuning, is the right answer to "make the model know our material" — because the alternative is sold constantly, and because one of retrieval's advantages is precisely the wound we left open at the end of the last chapter.

<figure class="diagram">
<svg viewBox="0 0 720 320" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Four advantages of retrieval over baking knowledge into the weights">
  <rect x="0" y="0" width="720" height="320" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="30" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">RETRIEVAL vs BAKING KNOWLEDGE INTO WEIGHTS</text>

  <g font-family="sans-serif">
    <rect x="45" y="66" width="300" height="70" rx="9" fill="#053d28" stroke="#10b981" stroke-width="1.3"/>
    <text x="60" y="90" fill="#d3f5e6" font-size="11.5" font-weight="bold">Updateable in minutes</text>
    <text x="60" y="110" fill="#8fd8b8" font-size="9.5">guideline changed Tuesday? re-index Tuesday.</text>
    <text x="60" y="125" fill="#8fd8b8" font-size="9.5">a fine-tune is a frozen snapshot</text>

    <rect x="375" y="66" width="300" height="70" rx="9" fill="#053d28" stroke="#10b981" stroke-width="1.3"/>
    <text x="390" y="90" fill="#d3f5e6" font-size="11.5" font-weight="bold">Auditable provenance ★</text>
    <text x="390" y="110" fill="#8fd8b8" font-size="9.5">real citations to real passages a human</text>
    <text x="390" y="125" fill="#8fd8b8" font-size="9.5">can open — the thing Chapter Six lacked</text>

    <rect x="45" y="150" width="300" height="70" rx="9" fill="#053d28" stroke="#10b981" stroke-width="1.3"/>
    <text x="60" y="174" fill="#d3f5e6" font-size="11.5" font-weight="bold">Access control that works</text>
    <text x="60" y="194" fill="#8fd8b8" font-size="9.5">the index can serve different users</text>
    <text x="60" y="209" fill="#8fd8b8" font-size="9.5">different documents; weights cannot</text>

    <rect x="375" y="150" width="300" height="70" rx="9" fill="#053d28" stroke="#10b981" stroke-width="1.3"/>
    <text x="390" y="174" fill="#d3f5e6" font-size="11.5" font-weight="bold">Honest failure</text>
    <text x="390" y="194" fill="#8fd8b8" font-size="9.5">found nothing relevant? it can say so —</text>
    <text x="390" y="209" fill="#8fd8b8" font-size="9.5">far more reliably than a bluffing base</text>
  </g>

  <text x="360" y="258" text-anchor="middle" fill="#f0c987" font-family="sans-serif" font-size="11.5" font-weight="bold">★ Post-training could only ever produce citation-SHAPED text. Retrieval produces citations that resolve.</text>
  <text x="360" y="286" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11">The chain from a claim to its source becomes inspectable — the single most important property for high-stakes use.</text>
</svg>
<figcaption><strong>Figure 3.</strong> Why retrieval is the default answer for knowledge. The starred advantage is the one that matters most here: at the end of Chapter Six we saw that "the model said so" is not provenance, because nothing in training ties an assertion to a source. Retrieval is what finally ties them — the model's answer can carry real references to real passages a human can open and verify.</figcaption>
</figure>

Read those four advantages against the alternative and the case is close to decisive for factual knowledge. A fine-tune bakes yesterday's guideline permanently into the weights, available to every user, unciteable, and impossible to revoke. An index is a living document set: update it, restrict it per user, and — because the answer is drawn from named passages — audit it. And when the right passage simply is not there, a well-instructed model asked to answer *only* from what it was given will decline far more reliably than one asked to consult its own parametric memory, where, as we know from Chapter Five, something plausible-sounding is always available.

## Part IV — Where retrieval fails, and how to catch it

Retrieval is the best answer we have to grounding, which is exactly why you must know its failure modes cold. They fall into two families, and a clinician's instinct for how diagnostic cascades fail will serve you well here.

**The retrieval can fail** — the right passage exists in the index but does not come back. Sometimes the cause is bad chunking: the answer was split across two chunks, or a chunk was severed from the context that gave it meaning ("the dose is 5 mg" — of *what*?). Sometimes it is a vocabulary the embedding model handles poorly, or a question whose answer requires *synthesising across many documents* when only a handful of chunks were retrieved. And sometimes it is a subtler trap that deserves its own picture, because it is the one I test for first in any clinical retrieval system.

<figure class="diagram">
<svg viewBox="0 0 720 320" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Similar is not the same as relevant or correct: contradictory passages on one topic embed close together">
  <rect x="0" y="0" width="720" height="320" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="30" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">SIMILAR ≠ RELEVANT ≠ CORRECT</text>

  <ellipse cx="360" cy="168" rx="300" ry="94" fill="#0a4a5c" opacity="0.28"/>
  <text x="360" y="86" text-anchor="middle" fill="#00d4f5" font-family="sans-serif" font-size="11" font-weight="bold">“metformin + contrast imaging” neighbourhood — everything here embeds close together</text>

  <circle cx="176" cy="147" r="6" fill="#10b981"/><text x="360" y="151" text-anchor="middle" fill="#d3f5e6" font-family="sans-serif" font-size="10.5">“continue metformin if eGFR ≥ 30, standard contrast” — current</text>
  <circle cx="131" cy="191" r="6" fill="#f87171"/><text x="360" y="195" text-anchor="middle" fill="#fde2e2" font-family="sans-serif" font-size="10.5">“withhold metformin 48h post-contrast” — superseded 2019 policy, never purged</text>
  <circle cx="194" cy="233" r="6" fill="#f87171"/><text x="360" y="237" text-anchor="middle" fill="#fde2e2" font-family="sans-serif" font-size="10.5">“metformin contraindicated” — from a paediatric protocol</text>

  <circle cx="505" cy="132" r="8" fill="none" stroke="#f59e0b" stroke-width="2.5"/><circle cx="505" cy="132" r="3" fill="#f59e0b"/>
  <text x="345" y="118" fill="#f59e0b" font-family="sans-serif" font-size="10.5" font-weight="bold">query: “hold metformin before CT contrast?”</text>

  <text x="360" y="296" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11">All three passages sit near the query. Embeddings measure <tspan font-style="italic">topical closeness</tspan> — they cannot tell current from</text>
  <text x="360" y="314" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11">superseded, adult from paediatric, or “do” from “don't.” Those distinctions are invisible to the geometry.</text>
</svg>
<figcaption><strong>Figure 4.</strong> The failure I watch for first. Contradictory guidance on the same topic — current and superseded, adult and paediatric, "do" and "don't" — embeds <em>close together</em>, because topical similarity is exactly what the geometry captures. Currency, population, and polarity must be handled by metadata, index hygiene, and the model's reading of the retrieved text — never by the vector search, which is blind to all three.</figcaption>
</figure>

**The generation can fail even when retrieval succeeded** — the right passages arrive and the model still gets it wrong. It may blend the retrieved facts with its own parametric memory, answering from the blur of pretraining rather than the document in front of it. It may over-trust a passage that matched on topic but does not actually apply. Or the crucial passage may sit in the middle of a long, stuffed context, where models demonstrably attend least — recall from Chapter Three that attention *can* reach anything in the window, but Chapter Six's training instilled *habits* about where it tends to look.

The discipline that follows is the same one we apply to any diagnostic cascade: **measure the stages separately.** Score the retrieval on its own — for a set of test questions, did the right passages come back at all? This is checkable without any model, just by inspecting what the search returned. Then, separately, score the generation *given* correct passages — was the answer faithful to them, and did it cite? A single end-to-end accuracy number confounds the two exactly the way "overall mortality" confounds case-mix with quality of care, and is about as useful for finding out what to fix.

<div class="callout">
⚕️ <strong>Two things to settle before any clinical deployment.</strong> First: an embedding is <em>derived from</em> the text it represents and can be partially inverted — so a vector index built from clinical notes is itself protected health information, with the same storage, access, and audit obligations as the source records. A folder of vectors is not an anonymous by-product; treat it as the chart. Second: when a retrieval product demos a beautiful cited answer, ask to see the passages it retrieved but was <em>not</em> shown — the ones ranked just below the cutoff. Whether the truth was sitting one rank below the line is the single most informative thing you can learn about the system's margin of safety.
</div>

## Part V — A window, not yet a door

Stand back and see what we have added. The sealed assistant of Chapter Six can now reach outside itself. Point it at a body of documents you control, and at the moment of a question it searches them by *meaning*, pulls the relevant passages into its context, and answers from them — with citations a human can open and check. The bluffing generalist has become, for the length of a reply, a grounded specialist that shows its working. The wound we left at the end of the last chapter — fluent confidence with no provenance — is, at last, dressed.

And yet notice the shape of what we have built, because it points straight at the final chapter. Everything in this chapter is *reactive* and *single-shot*. A question comes in; we do one retrieval; we produce one answer. The retriever is a *tool* — a thing the system can use to reach beyond its own weights — but it is a tool wielded once, on a fixed schedule, by machinery outside the model. The model itself did not *decide* to search. It did not look at what came back and think "that's not enough, let me search again with a better query." It did not, having found a guideline, go on to check the patient's notes, and then a drug database, chaining one lookup into the next. It answered once and stopped.

But a hard question in the real world is rarely one lookup. It is a small investigation — search, read, refine the search, cross-reference, decide what to do next. What if the model could do that? What if, instead of handing it a single retrieval, we gave it a *set* of tools — search, a calculator, a way to read a file, a way to take an action — and let *it* decide, step by step, which to use and when, looping until the task was actually done?

That is the leap from a model that *answers* to a system that *acts*. It is where retrieval becomes one tool among many, where the single-shot reply becomes a loop, and where the language model stops being an oracle you consult and becomes an agent that works on your behalf. Building it — and understanding both its power and the new care it demands — is Chapter Eight, the last piece of the machine.

*— Neal*

<div class="chapter-banner">
📖 <strong>Next chapter:</strong> <em>The Agent</em> — what happens when you give the model tools and let it decide, in a loop, which to use and when. Retrieval becomes one instrument among many; a single answer becomes an investigation; and the oracle you consult becomes a system that acts on your behalf. The final chapter, where every piece we have built is assembled into the thing reshaping how the work actually gets done.
</div>
