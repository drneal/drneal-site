---
title: "Meaning as Geometry: Embeddings, Retrieval, and RAG"
date: 2026-07-11
category: Deep Learning
tags: embeddings, vector search, RAG, retrieval, semantic search, LLM, clinical AI, grounding, provenance, deep learning
level: Intermediate–Advanced
read_time: 30 min
summary: "Lesson 7 of Learning With Dr Neal. The assistant from Lesson 6 knows nothing about your hospital's guidelines, your patient's notes, or anything published since its training data was collected. Closing that gap without retraining is the job of embeddings and retrieval — turning documents into geometry, searching by meaning, and grounding answers in sources you control."
featured: false
series: Learning With Dr Neal
series_index: 7
companion: 2026-07-23-meaning-you-can-search
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
📚 <strong>Lessons series — #7.</strong> This lesson builds directly on <a href="/post/2026-07-11-from-predictor-to-assistant">Lesson 6</a> (what the assistant is) and <a href="/post/2026-07-10-inside-the-transformer">Lesson 4</a> (token embeddings, the context window), and finally explains the machinery behind the Memory component of <a href="/post/2026-07-10-anatomy-of-an-ai-coding-agent">Lesson 3</a>'s agent. The full curriculum lives on the <a href="/lessons">Lessons page</a>.
</div>

The assistant we assembled across Lessons 4–6 has a strange epistemic profile. It writes beautifully, defaults to helpfulness, and knows a compressed, blurry copy of everything its pretraining corpus contained — as of the day that corpus was collected. It knows *nothing else*. Not your hospital's antimicrobial guidelines. Not the trial published last month. Not the allergy documented in the notes of the patient in front of you. And, as [Lesson 6](/post/2026-07-11-from-predictor-to-assistant) established, it will answer questions about all of these anyway — fluently.

You could try to fix this by retraining. For facts, that's the wrong tool: pretraining is a nine-figure industrial process, and Lesson 6's fine-tuning relocates *defaults*, not reliably-recallable knowledge. What you actually want is something more surgical: at the moment a question is asked, *find the right passages from documents you control and hand them to the model as context*. The model then does what it has always done — continue a transcript — except the transcript now contains the evidence.

That is retrieval-augmented generation — **RAG** — and it rests on one genuinely beautiful idea: that meaning itself can be given coordinates.

<div class="audio-section">
  🎬 <strong>Watch:</strong> Meaning as Geometry — the video companion to this lesson.<br/><br/>
  <video controls preload="metadata" style="width:100%; margin-top:0.4em; border-radius:6px;">
    <source src="https://pub-f57cd770c3d9448dafde9725cbc874b9.r2.dev/video/Meaning_as_Geometry.mp4" type="video/mp4">
    <a href="https://pub-f57cd770c3d9448dafde9725cbc874b9.r2.dev/video/Meaning_as_Geometry.mp4">Download the video</a>
  </video>
</div>

<div class="audio-section">
  🎧 <strong>Listen to this post:</strong> How RAG prevents AI hallucinations — the audio companion to this lesson.<br/><br/>
  <audio controls style="width:100%; margin-top:0.4em;">
    <source src="https://pub-f57cd770c3d9448dafde9725cbc874b9.r2.dev/audio/How_RAG_prevents_AI_hallucinations.mp3" type="audio/mpeg">
    <a href="https://pub-f57cd770c3d9448dafde9725cbc874b9.r2.dev/audio/How_RAG_prevents_AI_hallucinations.mp3">Download the audio</a>
  </audio>
</div>

## Meaning as geometry

You met embeddings in [Lesson 4](/post/2026-07-10-inside-the-transformer) as the transformer's front door: each *token* gets a learned vector, and tokens used similarly end up near each other. The idea scales up. An **embedding model** — itself a transformer, trained for exactly this job — reads a whole sentence, paragraph, or document chunk and outputs a single vector, typically a few hundred to a few thousand numbers, such that **texts with similar meaning land near each other in the vector space**.

Not similar *wording* — similar *meaning*. A well-trained embedding model places "the patient developed an itchy rash after the first dose of amoxicillin" close to "penicillin allergy — urticaria" and far from "the patient's rash improved after stopping the statin," even though the surface vocabulary overlaps more with the latter. How? Training by contrast: the model sees millions of pairs known to be related (question and its answer, title and its abstract, two translations of one sentence) and is optimised to pull related pairs together and push unrelated ones apart. Geometry is sculpted until distance *means* dissimilarity.

<figure class="diagram">
<svg viewBox="0 0 720 460" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Clinical sentences as points in embedding space, clustered by meaning">
  <rect x="0" y="0" width="720" height="460" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="34" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">A MAP OF MEANING (2 OF 1,024 DIMENSIONS)</text>

  <!-- anticoagulation cluster -->
  <ellipse cx="185" cy="150" rx="140" ry="80" fill="#0a4a5c" opacity="0.35"/>
  <text x="185" y="90" text-anchor="middle" fill="#00d4f5" font-family="sans-serif" font-size="11.5" font-weight="bold">anticoagulation</text>
  <circle cx="140" cy="130" r="5" fill="#00d4f5"/>
  <text x="150" y="126" fill="#9fdcec" font-family="sans-serif" font-size="10">"hold apixaban 48h pre-op"</text>
  <circle cx="120" cy="170" r="5" fill="#00d4f5"/>
  <text x="130" y="184" fill="#9fdcec" font-family="sans-serif" font-size="10">"warfarin — INR target 2–3"</text>
  <circle cx="230" cy="155" r="5" fill="#00d4f5"/>
  <text x="240" y="151" fill="#9fdcec" font-family="sans-serif" font-size="10">"DOAC reversal agents"</text>

  <!-- allergy cluster -->
  <ellipse cx="530" cy="150" rx="150" ry="80" fill="#053d28" opacity="0.35"/>
  <text x="530" y="90" text-anchor="middle" fill="#10b981" font-family="sans-serif" font-size="11.5" font-weight="bold">drug allergy</text>
  <circle cx="480" cy="140" r="5" fill="#10b981"/>
  <text x="490" y="136" fill="#8fd8b8" font-family="sans-serif" font-size="10">"urticaria after amoxicillin"</text>
  <circle cx="560" cy="170" r="5" fill="#10b981"/>
  <text x="570" y="184" fill="#8fd8b8" font-family="sans-serif" font-size="10">"penicillin allergy — documented"</text>
  <circle cx="590" cy="130" r="5" fill="#10b981"/>
  <text x="480" y="115" fill="#8fd8b8" font-family="sans-serif" font-size="10">"anaphylaxis to cephalosporin"</text>

  <!-- lipids cluster -->
  <ellipse cx="360" cy="345" rx="150" ry="70" fill="#2e1e5e" opacity="0.4"/>
  <text x="360" y="292" text-anchor="middle" fill="#a78bfa" font-family="sans-serif" font-size="11.5" font-weight="bold">lipid management</text>
  <circle cx="310" cy="330" r="5" fill="#a78bfa"/>
  <text x="320" y="326" fill="#c9b8f5" font-family="sans-serif" font-size="10">"rash improved off the statin"</text>
  <circle cx="340" cy="370" r="5" fill="#a78bfa"/>
  <text x="350" y="384" fill="#c9b8f5" font-family="sans-serif" font-size="10">"LDL target post-MI"</text>
  <circle cx="430" cy="345" r="5" fill="#a78bfa"/>
  <text x="440" y="341" fill="#c9b8f5" font-family="sans-serif" font-size="10">"ezetimibe added"</text>

  <!-- query -->
  <circle cx="520" cy="215" r="8" fill="none" stroke="#f59e0b" stroke-width="2.5"/>
  <circle cx="520" cy="215" r="3" fill="#f59e0b"/>
  <text x="415" y="240" fill="#f59e0b" font-family="sans-serif" font-size="11" font-weight="bold">query: "can this patient have co-amoxiclav?"</text>
  <line x1="520" y1="207" x2="525" y2="178" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="4,3"/>
  <line x1="513" y1="209" x2="487" y2="147" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="4,3"/>

  <text x="360" y="440" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11.5">The query lands nearest the allergy cluster — despite sharing almost no words with the notes it needs to find.</text>
</svg>
<figcaption><strong>Figure 1.</strong> Embedding space, cartooned in two dimensions (real spaces have hundreds to thousands). Note the crucial win over keyword search: "co-amoxiclav" doesn't appear anywhere in the allergy documentation, and "rash" appears in the <em>wrong</em> cluster — yet meaning-distance routes the query correctly. This is retrieval by concept, not by string.</figcaption>
</figure>

<div class="keyidea">
💡 <strong>Key idea.</strong> An embedding is a fixed address for a piece of text in a space where distance ≈ dissimilarity of meaning. Once text is geometry, "find documents relevant to this question" becomes "find the nearest points" — a problem computers have been fast at for decades. That single reduction powers semantic search, RAG, memory systems, deduplication, and clustering alike.
</div>

Two practical notes before we build with it. Similarity is usually measured by **cosine similarity** — the angle between vectors, ignoring length. And nearest-neighbour search over millions of vectors is made fast by approximate indexes (the "vector databases" you've heard of are, at heart, this index plus bookkeeping). At clinic scale — thousands of documents — you don't even need that: brute-force comparison is milliseconds.

## The RAG pipeline

With embeddings in hand, retrieval-augmented generation is two pipelines meeting at a context window:

<figure class="diagram">
<svg viewBox="0 0 720 520" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The RAG pipeline: ingestion lane and question lane meeting at the context window">
  <defs>
    <marker id="rarr7" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L8,4.5 L0,9 z" fill="#6b82a0"/>
    </marker>
  </defs>
  <rect x="0" y="0" width="720" height="520" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="34" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">RAG: TWO LANES, ONE CONTEXT WINDOW</text>

  <!-- lane headers -->
  <text x="185" y="66" text-anchor="middle" fill="#00d4f5" font-family="sans-serif" font-size="12.5" font-weight="bold">INGESTION — done once, refreshed on schedule</text>
  <text x="545" y="66" text-anchor="middle" fill="#10b981" font-family="sans-serif" font-size="12.5" font-weight="bold">QUESTION TIME — every query</text>

  <!-- ingestion lane -->
  <rect x="60" y="80" width="250" height="54" rx="9" fill="#111827" stroke="#00d4f5" stroke-width="1.5"/>
  <text x="185" y="103" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="12" font-weight="bold">Your documents</text>
  <text x="185" y="121" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="10.5">guidelines · protocols · notes · papers</text>

  <path d="M185,134 L185,152" stroke="#6b82a0" stroke-width="2" marker-end="url(#rarr7)"/>

  <rect x="60" y="156" width="250" height="54" rx="9" fill="#111827" stroke="#00d4f5" stroke-width="1.5"/>
  <text x="185" y="179" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="12" font-weight="bold">Chunk</text>
  <text x="185" y="197" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="10.5">split into passages (~200–800 tokens)</text>

  <path d="M185,210 L185,228" stroke="#6b82a0" stroke-width="2" marker-end="url(#rarr7)"/>

  <rect x="60" y="232" width="250" height="54" rx="9" fill="#111827" stroke="#00d4f5" stroke-width="1.5"/>
  <text x="185" y="255" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="12" font-weight="bold">Embed every chunk</text>
  <text x="185" y="273" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="10.5">one vector per passage</text>

  <path d="M185,286 L185,304" stroke="#6b82a0" stroke-width="2" marker-end="url(#rarr7)"/>

  <rect x="60" y="308" width="250" height="54" rx="9" fill="#0a4a5c" stroke="#00d4f5" stroke-width="2"/>
  <text x="185" y="331" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="12" font-weight="bold">Vector index</text>
  <text x="185" y="349" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="10.5">vectors + original text + source metadata</text>

  <!-- question lane -->
  <rect x="420" y="80" width="250" height="54" rx="9" fill="#111827" stroke="#10b981" stroke-width="1.5"/>
  <text x="545" y="103" text-anchor="middle" fill="#d3f5e6" font-family="sans-serif" font-size="12" font-weight="bold">The question</text>
  <text x="545" y="121" text-anchor="middle" fill="#8fd8b8" font-family="sans-serif" font-size="10.5">"perioperative DOAC plan for this patient?"</text>

  <path d="M545,134 L545,152" stroke="#6b82a0" stroke-width="2" marker-end="url(#rarr7)"/>

  <rect x="420" y="156" width="250" height="54" rx="9" fill="#111827" stroke="#10b981" stroke-width="1.5"/>
  <text x="545" y="179" text-anchor="middle" fill="#d3f5e6" font-family="sans-serif" font-size="12" font-weight="bold">Embed the question</text>
  <text x="545" y="197" text-anchor="middle" fill="#8fd8b8" font-family="sans-serif" font-size="10.5">same model, same space</text>

  <path d="M545,210 L545,228" stroke="#6b82a0" stroke-width="2" marker-end="url(#rarr7)"/>

  <rect x="420" y="232" width="250" height="54" rx="9" fill="#111827" stroke="#10b981" stroke-width="1.5"/>
  <text x="545" y="255" text-anchor="middle" fill="#d3f5e6" font-family="sans-serif" font-size="12" font-weight="bold">Nearest neighbours</text>
  <text x="545" y="273" text-anchor="middle" fill="#8fd8b8" font-family="sans-serif" font-size="10.5">top-k most similar chunks from the index</text>

  <!-- index feeds retrieval -->
  <path d="M310,335 Q400,335 435,286" stroke="#00d4f5" stroke-width="2" fill="none" marker-end="url(#rarr7)"/>

  <path d="M545,286 L545,304" stroke="#6b82a0" stroke-width="2" marker-end="url(#rarr7)"/>

  <!-- context window -->
  <rect x="150" y="386" width="420" height="60" rx="9" fill="#4a3000" stroke="#f59e0b" stroke-width="2"/>
  <text x="360" y="410" text-anchor="middle" fill="#fdeccd" font-family="sans-serif" font-size="12.5" font-weight="bold">Context window: question + retrieved passages + instructions</text>
  <text x="360" y="430" text-anchor="middle" fill="#f0c987" font-family="sans-serif" font-size="10.5">"Answer from the passages below. Cite the source of every claim. Say so if they don't contain the answer."</text>

  <path d="M545,304 Q545,360 480,386" stroke="#6b82a0" stroke-width="2" fill="none" marker-end="url(#rarr7)"/>

  <path d="M360,446 L360,462" stroke="#6b82a0" stroke-width="2" marker-end="url(#rarr7)"/>
  <rect x="230" y="466" width="260" height="40" rx="9" fill="#053d28" stroke="#10b981" stroke-width="1.5"/>
  <text x="360" y="491" text-anchor="middle" fill="#d3f5e6" font-family="sans-serif" font-size="12" font-weight="bold">Grounded answer, with citations</text>
</svg>
<figcaption><strong>Figure 2.</strong> The full RAG pipeline. The model itself is unmodified — same weights as Lesson 6, doing Lesson 4's next-token prediction. All the new engineering lives <em>outside</em> the model, in what gets placed into its context window. Fresh knowledge is one re-index away, no retraining involved.</figcaption>
</figure>

In code, the question-time lane is almost embarrassingly short. Given any embedding function (every major model provider offers one; good open-weight models run locally):

```python
import numpy as np

# ingest once: chunks = list of (text, source) pairs
vecs = np.stack([embed(text) for text, _ in chunks])       # (N, d)
vecs /= np.linalg.norm(vecs, axis=1, keepdims=True)        # unit length

def retrieve(question, k=5):
    q = embed(question)
    q /= np.linalg.norm(q)
    sims = vecs @ q                     # cosine similarity with every chunk
    top = np.argsort(sims)[-k:][::-1]   # k best matches
    return [chunks[i] for i in top]

def answer(question):
    passages = retrieve(question)
    context = "\n\n".join(f"[{src}] {text}" for text, src in passages)
    return llm(f"Answer using ONLY these passages. Cite sources. "
               f"If they don't contain the answer, say so.\n\n"
               f"{context}\n\nQuestion: {question}")
```

Twenty lines, and every one of them is a concept you already own: the embedding is Lesson 4's front door scaled up, the `llm()` call is Lesson 6's assistant, and the prompt assembly is [Lesson 3](/post/2026-07-10-anatomy-of-an-ai-coding-agent)'s context management. This is also, incidentally, exactly how the Memory system in Lesson 3's agent works: memory notes are chunks, session start embeds the task, and the nearest notes get injected into context. You have now closed that loop.

## Why this beats retraining for knowledge

It's worth being crisp about why retrieval, not fine-tuning, is the default answer to "make the model know our stuff" — because vendors regularly sell the opposite.

**Updateable in minutes.** Guideline changed Tuesday? Re-index Tuesday. A fine-tuned model is a snapshot; an index is a living document set.

**Auditable provenance — the thing Lesson 6 said was missing.** A RAG answer can carry real citations to real passages that a human can open and check. The chain from claim to source is inspectable at last. Post-training alone could only ever produce citation-*shaped* text.

**Access control that actually works.** Retrieval respects permissions: the index can serve different users different document sets. Knowledge baked into weights is available to every user of the model, always — you cannot revoke a fact from a fine-tune.

**Honest failure.** When retrieval finds nothing relevant, the system can *say so* — and a well-prompted model asked to answer only from provided passages will decline far more reliably than one asked to search its own parametric memory, where ([Lesson 5](/post/2026-07-10-train-your-own-gpt)) something plausible-sounding is always available.

## Where RAG fails — and how to catch it

RAG is the best answer we have to grounding, which is precisely why you should know its failure modes cold. They come in two families.

**Retrieval fails.** The right passage exists but doesn't come back. Causes: bad chunking (the answer straddles two chunks, or a chunk lost its context — "the dose is 5 mg" of *what*?); vocabulary mismatch that even embeddings can't bridge (your guidelines say "NOAC," the query says "DOAC," older embedding models may separate them); or the answer requiring *synthesis across many documents* when only five chunks were retrieved. And one failure mode subtle enough to deserve its own picture:

<figure class="diagram">
<svg viewBox="0 0 720 320" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Semantic similarity is not relevance: opposite statements embed close together">
  <rect x="0" y="0" width="720" height="320" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="34" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">SIMILAR ≠ RELEVANT ≠ CORRECT</text>

  <ellipse cx="360" cy="170" rx="290" ry="95" fill="#0a4a5c" opacity="0.3"/>
  <text x="360" y="88" text-anchor="middle" fill="#00d4f5" font-family="sans-serif" font-size="11.5" font-weight="bold">"metformin + contrast imaging" neighbourhood — everything here embeds close together</text>

  <circle cx="180" cy="150" r="6" fill="#10b981"/>
  <text x="192" y="146" fill="#d3f5e6" font-family="sans-serif" font-size="11">"continue metformin if eGFR ≥ 30 and contrast load standard"</text>

  <circle cx="200" cy="200" r="6" fill="#f87171"/>
  <text x="212" y="204" fill="#fde2e2" font-family="sans-serif" font-size="11">"withhold metformin for 48h post-contrast" — superseded 2019 policy, never purged</text>

  <circle cx="480" cy="235" r="6" fill="#f87171"/>
  <text x="360" y="256" fill="#fde2e2" font-family="sans-serif" font-size="11">"metformin is contraindicated (paediatric protocol)"</text>

  <circle cx="520" cy="130" r="8" fill="none" stroke="#f59e0b" stroke-width="2.5"/>
  <circle cx="520" cy="130" r="3" fill="#f59e0b"/>
  <text x="405" y="115" fill="#f59e0b" font-family="sans-serif" font-size="11" font-weight="bold">query: "hold metformin before CT contrast?"</text>

  <text x="360" y="296" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11.5">All three passages are near the query. Embeddings measure topical closeness — they cannot tell current from superseded, adult from paediatric, or "do" from "don't."</text>
</svg>
<figcaption><strong>Figure 3.</strong> The failure mode I test for first in any clinical RAG product. Contradictory guidance on the same topic embeds <em>close together</em> — topical similarity is what the geometry encodes. Currency, population, and polarity must be handled by metadata filters, index hygiene, and the model's reading of the retrieved text — not by the vector search, which is blind to all three.</figcaption>
</figure>

**Generation fails despite good retrieval.** The passages arrive and the model still gets it wrong: it blends retrieved facts with its parametric memory (answering from the blur of pretraining rather than the document in front of it); it over-trusts a passage that keyword-matches but doesn't apply; or the answer sits in the middle of a long stuffed context where models demonstrably attend least — recall from Lesson 4 that attention *can* reach everything in the window, but post-training taught models *habits* about where to look.

The evaluation discipline follows directly, and it's the same one we apply to any diagnostic cascade: **measure the stages separately**. Score retrieval on its own (for a set of test questions, did the right passages come back? — recall@k, checkable without any LLM), then score generation given correct passages (faithful? cited? complete?). A single end-to-end accuracy number confounds the two exactly the way "overall mortality" confounds case-mix with quality of care.

<div class="callout">
⚕️ <strong>Two clinical notes before you deploy anything.</strong> First: an embedding of a patient note is <em>derived from</em> the note and can be partially inverted — treat vector indexes of clinical text as PHI, with the same storage, access, and audit obligations as the source documents. Second: when a RAG product demo shows you a beautiful cited answer, ask to see the retrieved passages it was <em>not</em> shown — the ones ranked 6th through 20th. Whether the truth was sitting just below the cutoff is the single most informative thing you can learn about the system's margin of safety.
</div>

## What's next

Look at what's now on the bench: a model you understand down to the attention head (Lessons 4–5), shaped into an assistant whose failure modes you can name (Lesson 6), grounded in documents you control (this lesson), wrapped in an agent loop with tools, memory, and permissions (Lesson 3). Every component of a production clinical AI system, understood end to end.

Lesson 8 — [now live](/post/2026-07-12-build-a-grounded-assistant) — puts it all together with our hands: we'll **build a working retrieval assistant over your own documents** — a folder of guidelines or papers, a local embedding model, the twenty-line pipeline above, and an honest evaluation of where it succeeds and fails. Like Lesson 5, it will run on your laptop, and like Lesson 5, the point is calibration: after you've watched your own retriever return a superseded protocol with a confident citation, no product pitch will ever sound quite the same.

Until then: next time someone shows you a clinical AI tool and says "it's grounded in your guidelines," you know the three questions to ask. *What's in the index? What came back below the cutoff? And what happens when the passages contradict each other?* The answers will tell you whether you're looking at Figure 2 — or at Lesson 6's fluent confidence wearing a lab coat.

*— Neal*

<div class="lesson-banner">
📚 <strong>Continue the series:</strong> all lessons, in order, on the <a href="/lessons">Lessons page</a>.
</div>
