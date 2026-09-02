---
title: "The Capstone: Build a Grounded Assistant"
date: 2026-07-12
category: Deep Learning
tags: RAG, embeddings, retrieval, evaluation, recall, hands-on exercise, clinical AI, LLM, capstone, deep learning
level: Advanced
read_time: 40 min
summary: "Lesson 8 of Learning With Dr Neal — the capstone. Build a working retrieval assistant over a folder of your own documents: local embeddings, the twenty-line retriever, grounded answers with citations, and an honest recall@k evaluation that will teach you more about deployed clinical AI than any product demo ever will."
featured: false
series: Learning With Dr Neal
series_index: 8
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
📚 <strong>Lessons series — #8, the capstone.</strong> This build uses everything: gradient-trained models (<a href="/post/2026-06-19-how-deep-neural-networks-really-work">1</a>–<a href="/post/2026-06-26-deep-learning-spreadsheet-exercise">2</a>), the transformer (<a href="/post/2026-07-10-inside-the-transformer">4</a>), what training produces (<a href="/post/2026-07-10-train-your-own-gpt">5</a>), what post-training shapes (<a href="/post/2026-07-11-from-predictor-to-assistant">6</a>), and retrieval (<a href="/post/2026-07-11-meaning-as-geometry">7</a>) — assembled into the pattern at the heart of <a href="/post/2026-07-10-anatomy-of-an-ai-coding-agent">Lesson 3</a>'s agent. You'll want Python, ~2 GB of disk for a local embedding model, and a folder of documents. The full curriculum lives on the <a href="/lessons">Lessons page</a>.
</div>

Seven lessons ago you learned what a neuron computes. Today you assemble the whole stack into the most practically useful pattern in applied AI right now: an assistant that answers questions **from your documents, with citations, on your machine** — and, crucially, an evaluation harness that tells you honestly when it fails.

That last clause is the real lesson. Anyone can wire up retrieval in an afternoon (you will, below, in about sixty lines). What separates a toy from a tool — and a safe deployment from a liability — is knowing its failure rate on *your* questions over *your* corpus. By the end you'll have both the tool and the number.

<div style="font-size:0.8em; background:#1a1f2e; border-left:4px solid #1a237e; padding:1em 1.4em; border-radius:0 6px 6px 0; margin:1.5em 0;">
  🎬 <strong>Watch the video overview:</strong> Build a grounded assistant in nine minutes — the visual companion to this capstone.<br/><br/>
  <video controls preload="metadata" style="width:100%; margin-top:0.4em; border-radius:6px;">
    <source src="https://pub-f57cd770c3d9448dafde9725cbc874b9.r2.dev/video/Build_Grounded_Assistant.mp4" type="video/mp4">
    <a href="https://pub-f57cd770c3d9448dafde9725cbc874b9.r2.dev/video/Build_Grounded_Assistant.mp4">Download the video</a>
  </video>
</div>

## What we're building

<figure class="diagram">
<svg viewBox="0 0 720 470" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Architecture of the capstone build">
  <defs>
    <marker id="carr8" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L8,4.5 L0,9 z" fill="#6b82a0"/>
    </marker>
  </defs>
  <rect x="0" y="0" width="720" height="470" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="34" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">THE BUILD — ONE SCRIPT, FIVE PARTS</text>

  <!-- docs folder -->
  <rect x="40" y="70" width="180" height="64" rx="10" fill="#2e1e5e" stroke="#a78bfa" stroke-width="1.5"/>
  <text x="130" y="97" text-anchor="middle" fill="#e8e3fa" font-family="sans-serif" font-size="12.5" font-weight="bold">docs/ — your corpus</text>
  <text x="130" y="117" text-anchor="middle" fill="#9f8fd0" font-family="sans-serif" font-size="10.5">guidelines · protocols · papers</text>

  <!-- chunker -->
  <rect x="270" y="70" width="180" height="64" rx="10" fill="#111827" stroke="#00d4f5" stroke-width="1.5"/>
  <text x="360" y="97" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="12.5" font-weight="bold">① Chunker</text>
  <text x="360" y="117" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="10.5">overlapping windows, ~1,200 chars</text>

  <!-- embedder -->
  <rect x="500" y="70" width="180" height="64" rx="10" fill="#111827" stroke="#00d4f5" stroke-width="1.5"/>
  <text x="590" y="97" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="12.5" font-weight="bold">② Local embedder</text>
  <text x="590" y="117" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="10.5">runs on your laptop — no API</text>

  <path d="M220,102 L262,102" stroke="#6b82a0" stroke-width="2" marker-end="url(#carr8)"/>
  <path d="M450,102 L492,102" stroke="#6b82a0" stroke-width="2" marker-end="url(#carr8)"/>

  <!-- index -->
  <rect x="270" y="186" width="180" height="64" rx="10" fill="#0a4a5c" stroke="#00d4f5" stroke-width="2"/>
  <text x="360" y="213" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="12.5" font-weight="bold">③ Vector index</text>
  <text x="360" y="233" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="10.5">one NumPy matrix + metadata</text>

  <path d="M590,134 Q590,218 458,218" stroke="#6b82a0" stroke-width="2" fill="none" marker-end="url(#carr8)"/>

  <!-- question path -->
  <rect x="40" y="302" width="180" height="64" rx="10" fill="#053d28" stroke="#10b981" stroke-width="1.5"/>
  <text x="130" y="329" text-anchor="middle" fill="#d3f5e6" font-family="sans-serif" font-size="12.5" font-weight="bold">Your question</text>
  <text x="130" y="349" text-anchor="middle" fill="#8fd8b8" font-family="sans-serif" font-size="10.5">interactive prompt or --ask</text>

  <rect x="270" y="302" width="180" height="64" rx="10" fill="#111827" stroke="#10b981" stroke-width="1.5"/>
  <text x="360" y="329" text-anchor="middle" fill="#d3f5e6" font-family="sans-serif" font-size="12.5" font-weight="bold">④ Retriever</text>
  <text x="360" y="349" text-anchor="middle" fill="#8fd8b8" font-family="sans-serif" font-size="10.5">top-5 by cosine, sources attached</text>

  <rect x="500" y="302" width="180" height="64" rx="10" fill="#4a3000" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="590" y="329" text-anchor="middle" fill="#fdeccd" font-family="sans-serif" font-size="12.5" font-weight="bold">Grounded answer</text>
  <text x="590" y="349" text-anchor="middle" fill="#f0c987" font-family="sans-serif" font-size="10.5">LLM + citations (optional key)</text>

  <path d="M220,334 L262,334" stroke="#6b82a0" stroke-width="2" marker-end="url(#carr8)"/>
  <path d="M450,334 L492,334" stroke="#6b82a0" stroke-width="2" marker-end="url(#carr8)"/>
  <path d="M360,250 L360,294" stroke="#6b82a0" stroke-width="2" marker-end="url(#carr8)"/>

  <!-- eval -->
  <rect x="180" y="398" width="360" height="52" rx="10" fill="#3d0f0f" stroke="#f87171" stroke-width="1.5"/>
  <text x="360" y="420" text-anchor="middle" fill="#fde2e2" font-family="sans-serif" font-size="12.5" font-weight="bold">⑤ Evaluation harness — recall@5 on YOUR questions</text>
  <text x="360" y="440" text-anchor="middle" fill="#e2a0a0" font-family="sans-serif" font-size="10.5">the part every demo skips, and the part that makes you dangerous in a vendor meeting</text>

  <path d="M300,366 L300,392" stroke="#6b82a0" stroke-width="2" marker-end="url(#carr8)"/>
</svg>
<figcaption><strong>Figure 1.</strong> The capstone architecture. Parts ①–④ are Lesson 7's Figure 2 made concrete; part ⑤ is this lesson's contribution. The complete script is a single file, linked below — read it before you run it; there is nothing in it you haven't met.</figcaption>
</figure>

The complete script: **[build_rag_assistant.py](/static/build_rag_assistant.py)**. Setup is two installs — `pip install sentence-transformers numpy`, plus optionally `pip install anthropic` and an API key if you want generated answers rather than retrieval-only. Everything else below walks through the decisions in the code, which is where the learning lives.

## Step 0: choose your corpus — carefully

Any folder of `.txt` or `.md` files works. Aim for something between twenty and a few hundred documents that you *know well* — that last property is what makes the evaluation meaningful. Good choices: a society's published guidelines, a course's worth of lecture notes, your own blog or thesis, a set of departmental protocols *if and only if they contain no patient data*.

<div class="callout">
⚠️ <strong>Say it before the tooling makes it easy to forget:</strong> do this first build with public documents. The moment patient-identifiable text enters the pipeline you have created a new PHI store (the chunk text <em>and</em> the vectors — <a href="/post/2026-07-11-meaning-as-geometry" style="color:#00d4f5;">Lesson 7</a> explained why embeddings of clinical text are themselves PHI), and everything you know about information governance applies to a folder called <code>.rag_index</code> just as it does to a filing cabinet. Learn the mechanics on safe material; involve your governance people before the real thing.
</div>

## Step 1: chunking — the decision everyone underestimates

The script splits each document into windows of ~1,200 characters with 200 characters of **overlap** between consecutive chunks. Both numbers are arguments you should experiment with, because chunking is where more real-world RAG systems quietly fail than anywhere else.

Why chunk at all? Because retrieval granularity is answer granularity. Embed whole documents and your retriever can only say "the answer is somewhere in this 40-page guideline" — too coarse to ground a specific claim. Chunk too small and you get the orphaned-context problem from Lesson 7: a chunk reading "the dose is 5 mg once daily" retrieves beautifully and means nothing, because the drug name lives in the previous chunk. The overlap is the compromise: each boundary region appears in two chunks, halving the chance that a critical sentence gets severed from its context.

The production-grade refinement, once you've felt the failure: split on *structure* (section headings, paragraphs) rather than character counts, and prepend each chunk with its document title and section path — "AF Guideline 2025 › Anticoagulation › Perioperative management: …". Ten lines of extra code; dramatic retrieval improvement on hierarchical documents like guidelines. The script keeps character windows for clarity; the upgrade is your first exercise.

## Steps 2–4: embed, retrieve, answer

The embedding model runs locally — a small sentence-transformer, ~90 MB, downloads on first run, embeds a few hundred documents in about a minute on a laptop, no data leaving your machine. Retrieval is Lesson 7's twenty lines: normalise, dot product, top-k. Answering assembles the prompt you've already seen, with the two instructions that do the safety work: *answer only from the passages* and *say so if they don't contain the answer*.

One design choice worth pausing on: **the script prints the retrieved passages before any generated answer** — always, in every mode:

<div class="sample-box">
<span class="label">question></span> when should DOACs be held before elective surgery?<br/><br/>
<span class="label">── retrieved passages ──</span><br/>
&nbsp;0.71&nbsp; [periop_anticoag_2025.md] &nbsp;For procedures with standard bleeding risk, apixaban and rivaroxaban should be held…<br/>
&nbsp;0.66&nbsp; [periop_anticoag_2025.md] &nbsp;…renal function modifies the interval: for CrCl below 50 mL/min, extend…<br/>
&nbsp;0.59&nbsp; [af_guideline_summary.md] &nbsp;Bridging with LMWH is not recommended for DOAC-treated patients undergoing…<br/>
&nbsp;0.44&nbsp; [warfarin_protocol_2019.md] &nbsp;Warfarin should be withheld five days prior, with INR checked…<br/>
&nbsp;0.41&nbsp; [dental_extraction_advice.md] &nbsp;Most dental procedures do not require interruption of anticoagulation…
</div>

Get in the habit of reading that list *before* reading any generated answer. It is the system's differential diagnosis — and note the two lower-ranked passages: a 2019 warfarin protocol (topically adjacent, wrong drug class) and dental advice (relevant only sometimes). Lesson 7's Figure 3, live in your own terminal. Whether the generator handles them gracefully is exactly what the next step measures.

## Step 5: the evaluation — where the capstone earns its name

Now the part that separates this lesson from every RAG tutorial on the internet. Write a file called `eval.tsv`: one line per test, a question you know the corpus can answer, a tab, and the filename that contains the answer.

<div class="sample-box">
when should apixaban be held before elective surgery?&nbsp;&nbsp;→&nbsp;&nbsp;periop_anticoag_2025.md<br/>
is bridging needed for DOAC patients?&nbsp;&nbsp;→&nbsp;&nbsp;af_guideline_summary.md<br/>
what INR is required before a dental extraction?&nbsp;&nbsp;→&nbsp;&nbsp;dental_extraction_advice.md<br/>
…(aim for 20–30 lines; fifteen minutes of work)
</div>

Then `python build_rag_assistant.py docs/ --eval eval.tsv` scores **recall@5**: for what fraction of your questions did the right document appear in the top five retrieved chunks? This is the retrieval-only metric Lesson 7 argued for — no LLM involved, no fluency to seduce you, just a number.

<figure class="diagram">
<svg viewBox="0 0 720 380" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The evaluation loop and how to read its results">
  <defs>
    <marker id="earr8" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L8,4.5 L0,9 z" fill="#f59e0b"/>
    </marker>
  </defs>
  <rect x="0" y="0" width="720" height="380" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="34" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">THE CALIBRATION LOOP</text>

  <rect x="40" y="70" width="190" height="70" rx="10" fill="#111827" stroke="#00d4f5" stroke-width="1.5"/>
  <text x="135" y="98" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="12.5" font-weight="bold">Write 20–30 questions</text>
  <text x="135" y="118" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="10.5">whose answers you can locate</text>

  <rect x="265" y="70" width="190" height="70" rx="10" fill="#111827" stroke="#10b981" stroke-width="1.5"/>
  <text x="360" y="98" text-anchor="middle" fill="#d3f5e6" font-family="sans-serif" font-size="12.5" font-weight="bold">Run --eval</text>
  <text x="360" y="118" text-anchor="middle" fill="#8fd8b8" font-family="sans-serif" font-size="10.5">recall@5, one ✓/✗ per question</text>

  <rect x="490" y="70" width="190" height="70" rx="10" fill="#4a3000" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="585" y="98" text-anchor="middle" fill="#fdeccd" font-family="sans-serif" font-size="12.5" font-weight="bold">Autopsy every ✗</text>
  <text x="585" y="118" text-anchor="middle" fill="#f0c987" font-family="sans-serif" font-size="10.5">what came back instead — and why?</text>

  <path d="M230,105 L257,105" stroke="#f59e0b" stroke-width="2" marker-end="url(#earr8)"/>
  <path d="M455,105 L482,105" stroke="#f59e0b" stroke-width="2" marker-end="url(#earr8)"/>
  <path d="M585,140 Q585,200 360,200 Q135,200 135,146" stroke="#f59e0b" stroke-width="2" fill="none" marker-end="url(#earr8)"/>
  <text x="360" y="192" text-anchor="middle" fill="#f59e0b" font-family="monospace" font-size="11">fix → re-run → converge</text>

  <!-- typical findings -->
  <rect x="40" y="232" width="640" height="118" rx="10" fill="#111827" stroke="#2a3f5f" stroke-width="1.5"/>
  <text x="60" y="258" fill="#c9d6e8" font-family="sans-serif" font-size="12" font-weight="bold">What the ✗ autopsies typically reveal (in rough order of frequency):</text>
  <text x="60" y="282" fill="#6b82a0" font-family="sans-serif" font-size="11.5">· vocabulary mismatch — your question says "hold", the document says "interrupt" (fix: better embedder, hybrid search)</text>
  <text x="60" y="302" fill="#6b82a0" font-family="sans-serif" font-size="11.5">· answer severed at a chunk boundary (fix: structural chunking, more overlap)</text>
  <text x="60" y="322" fill="#6b82a0" font-family="sans-serif" font-size="11.5">· a superseded or adjacent document outranks the right one (fix: metadata filters, purge old versions)</text>
  <text x="60" y="342" fill="#6b82a0" font-family="sans-serif" font-size="11.5">· the question needs synthesis across many files — beyond top-k retrieval entirely (fix: an agent that searches iteratively)</text>
</svg>
<figcaption><strong>Figure 2.</strong> The evaluation loop, and the taxonomy of what you'll find. Expect a first-run recall@5 somewhere between 60% and 90% — almost never 100%. Every miss is a small, safe, laptop-scale preview of a failure that ships inside commercial clinical AI products every day.</figcaption>
</figure>

Two disciplines while you iterate. Don't tune on your test set into oblivion — after a few fix-and-re-run cycles, write ten *fresh* questions and see if the improvements held (derivation and validation cohorts; you know this dance). And spot-check *faithfulness* separately: for five questions where retrieval succeeded, read the generated answer against the passages, sentence by sentence. Anything asserted that the passages don't support is [Lesson 6](/post/2026-07-11-from-predictor-to-assistant)'s polished hallucination surviving inside a "grounded" system — the single most important thing to catch, and the reason the citation instruction exists.

<div class="keyidea">
💡 <strong>Key idea.</strong> After this afternoon you own something rarer than a working RAG system: a <em>calibrated</em> one — a tool whose failure rate, failure modes, and fixes you have personally measured on your own material. Scale changes the engineering (indexes, rerankers, caching); it does not change the epistemics. When a vendor cannot answer "what's your retrieval recall on questions like ours, and how did you measure it?", you now know precisely what they haven't done.
</div>

## Where this connects back — and forward

Wire the pieces into [Lesson 3](/post/2026-07-10-anatomy-of-an-ai-coding-agent)'s picture and notice what you've built: `retrieve()` is a **tool**; the folder is **Memory**; the answer loop is one turn of the **agent loop**. Give an agent this script as a callable tool and it will search your corpus iteratively — rephrasing queries, chasing cross-references, synthesising across files — which is exactly the fix Figure 2 prescribes for the hardest failure class. The capstone isn't beside the agent architecture; it's a component of it.

And the series arc is now closed. A neuron ([Lesson 1](/post/2026-06-19-how-deep-neural-networks-really-work)) — trained by hand (2) — stacked into a transformer (4) — trained into a language model (5) — shaped into an assistant (6) — grounded in your documents (7, 8) — wrapped in an agent that acts (3). Eight lessons, and there is no box in any vendor's architecture diagram you can't now open.

## What's next

The foundations are laid, which changes the character of what follows: from here the series turns to the topics that keep practitioners honest — evaluating LLM systems properly (beyond today's recall@k), interpretability (what's actually inside the weights you trained), and multimodality (images, and what that means for those of us who look at scans and slides for a living). In whichever order the questions arrive.

Until then: build the thing. Point it at documents you know, write your twenty questions, get your number. Then — this is the graduation exercise — show a colleague the beautiful cited answer *and* the ranked passage list behind it, and teach them the difference. That's the whole curriculum, paid forward in five minutes.

*— Neal*

<div class="lesson-banner">
📚 <strong>The full series, in order:</strong> the <a href="/lessons">Lessons page</a> — from "what is a neuron?" to the assistant you just built.
</div>
