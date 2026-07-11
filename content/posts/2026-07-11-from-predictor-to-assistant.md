---
title: "From Predictor to Assistant"
date: 2026-07-11
category: Deep Learning
tags: post-training, instruction tuning, RLHF, fine-tuning, alignment, LLM, base model, sycophancy, clinical AI, deep learning
level: Intermediate–Advanced
read_time: 30 min
summary: "Lesson 6 of Learning With Dr Neal. The raw next-token predictor you trained in Lesson 5 is the 'before' picture. This is the 'after' — instruction tuning, feedback-based refinement, why the same weights can host such different behaviours, and what the post-training pipeline means for the failure modes you'll meet in deployed clinical tools."
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
📚 <strong>Lessons series — #6.</strong> This lesson assumes you've met the transformer (<a href="/post/2026-07-10-inside-the-transformer">Lesson 4</a>) and — ideally — trained one (<a href="/post/2026-07-10-train-your-own-gpt">Lesson 5</a>). It also closes a loop opened in <a href="/post/2026-07-10-anatomy-of-an-ai-coding-agent">Lesson 3</a>, where an assistant sat at the centre of the agent loop and we took its helpfulness on faith. The full curriculum lives on the <a href="/lessons">Lessons page</a>.
</div>

# From Predictor to Assistant

If you ran Lesson 5's script, you now own something valuable: a genuinely unhelpful language model. Ask your TinyGPT a question and it will not answer. It will *continue* — with more anatomy, more Edwardian prose, more of whatever statistical neighbourhood your prompt landed it in. It is a mirror of its corpus, and mirrors don't answer questions.

Yet the models you use daily — the one powering the coding agent from Lesson 3, the one drafting your clinic letters — began life as exactly this kind of mirror, scaled up. Somewhere between "raw predictor trained on the internet" and "assistant that answers, follows instructions, and declines to help with the dangerous stuff," something happened. This lesson is about that something: **post-training**. It is the least understood stage of the pipeline among otherwise well-informed people, and — I'll argue by the end — the stage whose fingerprints are on the specific failure modes that matter most in clinical deployment.

## The problem, stated honestly

Recall the punchline of Lesson 5: a base model completes text according to the statistics of its training distribution. Feed a big base model this prompt:

<div class="sample-box">
<span class="label">prompt:</span> What are the contraindications to thrombolysis in acute stroke?<br/><br/>
<span class="label">a base model, plausibly:</span> What is the therapeutic window for alteplase? What imaging is required before treatment? These are among the questions most commonly asked by candidates preparing for the written examination…
</div>

Nothing malfunctioned. On the internet, a question is very often followed by *more questions* — exam banks, FAQ pages, forum threads. The base model is doing precisely what we trained it to do in Lesson 5: continue the document. The problem is that "continue the document" and "help the person" are different objectives that merely *overlap*. Post-training exists to close that gap — to take a model that can complete anything and shape it into one that reliably does the one thing you actually want.

The deepest fact about post-training, and the source of most of its surprises, is *how little machinery it adds*. No new architecture. No new mechanism bolted onto the transformer. The same weights, the same attention, the same next-token interface — only the *training signal* changes. Everything an assistant is, it is through the mechanism you already understand.

## Stage one: teaching the format by example

The first move is embarrassingly direct: collect tens or hundreds of thousands of *demonstration conversations* — a user message, followed by the response a good assistant should give, written or curated by humans — and continue training the base model on them with exactly Lesson 5's loop. Batch, forward, cross-entropy, backward, step. This is **instruction tuning** (you'll also see *supervised fine-tuning*).

One detail makes it click into place with what you already know. A "conversation" is presented to the model as — of course — a flat token sequence, with special marker tokens delimiting the roles:

<div class="sample-box">
&lt;|user|&gt; What are the contraindications to thrombolysis in acute stroke?<br/>
&lt;|assistant|&gt; The major contraindications fall into three groups: active bleeding risk, …<br/>
&lt;|end|&gt;
</div>

The model is trained to predict the tokens of the assistant turns, given everything before them. That's all a "chat format" is — a document convention, learned like any other. When you had a "conversation" with an LLM this morning, the model received one long document in this shape and did Lesson 4's Figure 1 on it, token by token. (And when Lesson 3's agent loop appended tool results into a transcript — same convention, more roles.)

After instruction tuning, the mirror is gone. Ask a question, get an answer. But two gaps remain, and they set up the second stage. First, demonstrations teach *format and typical content*, not *judgment* — the fine calls (how cautious to be, when to refuse, how to handle a request that's ambiguous or half-dangerous) are poorly specified by examples alone. Second, writing demonstrations is expensive and slow, and it caps the model at "imitates a good human answer" when we'd like "produces the answer humans *prefer*, even over what a demonstrator would have written."

## Stage two: refining against preferences

The second stage changes the *kind* of signal. Instead of showing the model what to say, we let it generate — and grade the results.

The core loop: sample two (or more) responses from the model to the same prompt; show a human rater both; record which one they preferred. Note the design decision hiding in that sentence — raters *compare*, they don't *score*. Decades of measurement science, clinical assessment included, converge on the same finding: humans are unreliable at absolute ratings ("rate this answer 1–10") and much more consistent at forced choice ("which of these two is better?"). Preference data inherits that reliability.

Comparisons then train a **reward model** — typically the same transformer architecture again, with the vocabulary head swapped for a single number: a learned estimate of "how much would a human prefer this response?" And finally the assistant is optimised — by reinforcement learning or by more direct methods that skip the explicit reward model — to produce responses that score highly, while being penalised for drifting too far from the instruction-tuned starting point (that tether matters; more below).

<figure class="diagram">
<svg viewBox="0 0 720 460" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The full post-training pipeline from base model to assistant">
  <defs>
    <marker id="parr6" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L8,4.5 L0,9 z" fill="#6b82a0"/>
    </marker>
  </defs>
  <rect x="0" y="0" width="720" height="460" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="34" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">THE SHAPING PIPELINE</text>

  <!-- Stage 0 -->
  <rect x="40" y="66" width="640" height="76" rx="10" fill="#111827" stroke="#a78bfa" stroke-width="1.5"/>
  <text x="60" y="93" fill="#e8e3fa" font-family="sans-serif" font-size="13" font-weight="bold">PRETRAINING (Lessons 4–5)</text>
  <text x="60" y="113" fill="#9f8fd0" font-family="sans-serif" font-size="11.5">Data: trillions of tokens of raw text · Signal: predict the next token · Cost: nearly all of the total compute</text>
  <text x="60" y="130" fill="#9f8fd0" font-family="sans-serif" font-size="11.5">Output: a base model — vast capability, mirror-like behaviour</text>

  <path d="M360,142 L360,160" stroke="#6b82a0" stroke-width="2" marker-end="url(#parr6)"/>

  <!-- Stage 1 -->
  <rect x="40" y="164" width="640" height="76" rx="10" fill="#0a4a5c" stroke="#00d4f5" stroke-width="1.5"/>
  <text x="60" y="191" fill="#d8f6fd" font-family="sans-serif" font-size="13" font-weight="bold">INSTRUCTION TUNING</text>
  <text x="60" y="211" fill="#9fdcec" font-family="sans-serif" font-size="11.5">Data: ~10⁴–10⁵ demonstration conversations · Signal: same next-token loss, on assistant turns</text>
  <text x="60" y="228" fill="#9fdcec" font-family="sans-serif" font-size="11.5">Teaches: the format — answer the question, follow the instruction, stop at the end</text>

  <path d="M360,240 L360,258" stroke="#6b82a0" stroke-width="2" marker-end="url(#parr6)"/>

  <!-- Stage 2 -->
  <rect x="40" y="262" width="640" height="76" rx="10" fill="#053d28" stroke="#10b981" stroke-width="1.5"/>
  <text x="60" y="289" fill="#d3f5e6" font-family="sans-serif" font-size="13" font-weight="bold">PREFERENCE REFINEMENT</text>
  <text x="60" y="309" fill="#8fd8b8" font-family="sans-serif" font-size="11.5">Data: ~10⁵–10⁶ human comparisons ("which answer is better?") · Signal: learned reward, not imitation</text>
  <text x="60" y="326" fill="#8fd8b8" font-family="sans-serif" font-size="11.5">Teaches: judgment — tone, caution, refusals, honesty about uncertainty (imperfectly; see below)</text>

  <path d="M360,338 L360,356" stroke="#6b82a0" stroke-width="2" marker-end="url(#parr6)"/>

  <!-- Deployed -->
  <rect x="40" y="360" width="640" height="58" rx="10" fill="#4a3000" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="60" y="386" fill="#fdeccd" font-family="sans-serif" font-size="13" font-weight="bold">THE ASSISTANT YOU USE</text>
  <text x="60" y="405" fill="#f0c987" font-family="sans-serif" font-size="11.5">Same architecture, same next-token interface — behaviour shaped by everything above, plus a system prompt at runtime</text>

  <text x="360" y="442" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11.5">Reading the compute column tells you something important: almost everything the model knows, it learned in stage one.</text>
</svg>
<figcaption><strong>Figure 1.</strong> The pipeline end to end. Post-training (the middle two bands) consumes a small fraction of total training compute — it is a <em>shaping</em> pass over capabilities that already exist, not a source of new knowledge. That asymmetry explains most of this lesson's warnings.</figcaption>
</figure>

<figure class="diagram">
<svg viewBox="0 0 720 400" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The preference learning cycle">
  <defs>
    <marker id="carr6" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L8,4.5 L0,9 z" fill="#f59e0b"/>
    </marker>
  </defs>
  <rect x="0" y="0" width="720" height="400" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="34" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">THE PREFERENCE LOOP</text>

  <!-- model generates -->
  <rect x="60" y="70" width="190" height="70" rx="10" fill="#0a4a5c" stroke="#00d4f5" stroke-width="1.5"/>
  <text x="155" y="98" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="12.5" font-weight="bold">Model answers the</text>
  <text x="155" y="116" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="12.5" font-weight="bold">same prompt twice</text>

  <!-- human compares -->
  <rect x="470" y="70" width="190" height="70" rx="10" fill="#2e1e5e" stroke="#a78bfa" stroke-width="1.5"/>
  <text x="565" y="98" text-anchor="middle" fill="#e8e3fa" font-family="sans-serif" font-size="12.5" font-weight="bold">Human picks the</text>
  <text x="565" y="116" text-anchor="middle" fill="#e8e3fa" font-family="sans-serif" font-size="12.5" font-weight="bold">better one — A or B</text>

  <!-- reward model -->
  <rect x="470" y="240" width="190" height="70" rx="10" fill="#053d28" stroke="#10b981" stroke-width="1.5"/>
  <text x="565" y="268" text-anchor="middle" fill="#d3f5e6" font-family="sans-serif" font-size="12.5" font-weight="bold">Reward model learns</text>
  <text x="565" y="286" text-anchor="middle" fill="#d3f5e6" font-family="sans-serif" font-size="12.5" font-weight="bold">to predict the picks</text>

  <!-- policy update -->
  <rect x="60" y="240" width="190" height="70" rx="10" fill="#3d0f0f" stroke="#f87171" stroke-width="1.5"/>
  <text x="155" y="268" text-anchor="middle" fill="#fde2e2" font-family="sans-serif" font-size="12.5" font-weight="bold">Model updated toward</text>
  <text x="155" y="286" text-anchor="middle" fill="#fde2e2" font-family="sans-serif" font-size="12.5" font-weight="bold">higher-reward answers</text>

  <path d="M250,105 L462,105" stroke="#f59e0b" stroke-width="2" marker-end="url(#carr6)"/>
  <path d="M565,140 L565,232" stroke="#f59e0b" stroke-width="2" marker-end="url(#carr6)"/>
  <path d="M470,275 L258,275" stroke="#f59e0b" stroke-width="2" marker-end="url(#carr6)"/>
  <path d="M155,240 L155,148" stroke="#f59e0b" stroke-width="2" marker-end="url(#carr6)"/>

  <!-- tether note -->
  <rect x="270" y="168" width="180" height="50" rx="8" fill="#111827" stroke="#2a3f5f"/>
  <text x="360" y="189" text-anchor="middle" fill="#c9d6e8" font-family="sans-serif" font-size="10.5">…while staying tethered to the</text>
  <text x="360" y="205" text-anchor="middle" fill="#c9d6e8" font-family="sans-serif" font-size="10.5">instruction-tuned starting point</text>

  <text x="360" y="356" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11.5">The optimisation target is not "the truth" — it is "what the reward model predicts a rater would prefer."</text>
  <text x="360" y="374" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11.5">Every gap between those two things is a failure mode waiting for deployment.</text>
</svg>
<figcaption><strong>Figure 2.</strong> The preference loop. Notice it is optimisation against a <em>proxy</em> — a model of human judgment, itself trained on judgments of variable quality made quickly by raters who are rarely domain experts. The caption below the loop is the single most important sentence in this lesson.</figcaption>
</figure>

<div class="keyidea">
💡 <strong>Key idea.</strong> Post-training optimises "what humans (as modelled) prefer," not "what is true." Usually those coincide — people prefer correct answers when they can tell. But raters reward confidence, fluency, agreement, and answers over admissions of ignorance <em>whenever correctness is hard for them to check</em>. The model dutifully learns exactly that. Keep this one idea and the clinical section below follows as a series of corollaries.
</div>

## Same weights, different characters

Here is the part that strikes most people as strange: nothing was removed from the base model. Post-training is a comparatively gentle nudge in weight space — the pretrained capabilities, including the ability to imitate every voice and viewpoint on the internet, are all still in there. What changed is which behaviour the model *reaches for by default*.

The picture I find most useful: pretraining builds an enormous repertoire — every register, persona, and style the corpus contained, from NEJM case discussion to conspiracy forum. A base model, prompted, falls into whichever region of that repertoire the prompt statistically resembles. Post-training doesn't delete regions; it *re-weights the defaults*, carving a deep, comfortable groove labelled "helpful, harmless, honest assistant" that the model now settles into from almost any starting point.

Three everyday observations fall straight out of this picture. **System prompts work** because the groove is a default, not a cage — a well-crafted instruction ("you are a terse triage assistant; answer in bullet points; escalate anything cardiac") repositions the model within its repertoire, cheaply and reversibly. **Jailbreaks work** — sometimes — because an adversarial prompt is an attempt to pull the model out of the groove and back into some untamed region of the base repertoire; post-training made that harder, not impossible. And **fine-tuning works with tiny datasets** (hundreds of examples can specialise a model) because you are not teaching it medicine from scratch — the knowledge is already there from pretraining; you are relocating the default.

<div class="callout">
⚕️ <strong>A framing for clinicians:</strong> pretraining is medical school and residency — years, enormous cost, all the actual knowledge. Post-training is the induction week at a new hospital: quick, cheap, and it determines how you answer the phone, what you document, when you escalate. Nobody confuses induction week with medical school — yet in AI discourse the two are conflated constantly. When a vendor says their clinical model was "trained for healthcare," your first question should be: which of the two do they mean? The answer changes everything about how you should validate it.
</div>

## What this means at the bedside

Now the payoff — reading deployed-tool failure modes as direct consequences of the pipeline you just learned.

**Sycophancy is a training artifact, not a personality flaw.** In the preference loop, agreeable responses win comparisons more often than corrective ones. The result is a model with a measurable tilt toward endorsing what the user seems to believe. Now put that in a clinical workflow: the registrar types "elderly patient, fall, on apixaban, CT head clear, planning discharge — anything else?" A sycophantic model is biased toward blessing the plan. The danger is precisely that it *feels* like consultation — it has the form of a second opinion with the incentives of a courtier. When you evaluate a clinical LLM tool, test it with wrong premises embedded in your prompts and watch whether it pushes back. That single test tells you more than any accuracy benchmark.

**Confident hallucination survives post-training — masked, not cured.** You bred the fluency-fidelity gap yourself in Lesson 5 and watched it: statistical shape arrives long before factual grounding, at every scale. Post-training reduces hallucination (raters do punish detectable fabrication) but it cannot eliminate it, because the underlying generator is still a sampler over plausible continuations — and it adds a hazard all its own: the surviving fabrications are now delivered in the calm, structured, caveated register of a careful colleague, *because that is the register post-training rewards*. A base model's nonsense at least looked like nonsense. An assistant's nonsense looks like a well-written consult note with an invented reference in it.

**Refusals and caveats are trained behaviours with a distribution.** The model declines, hedges, or recommends "consult a professional" according to patterns learned from raters applying a policy — raters who were not, in general, clinicians, and whose policy was written for the general public. So expect miscalibration at both ends in specialist use: over-refusal on legitimate clinical questions (dosing in unusual scenarios) and under-refusal where surface framing looks benign. The calibration you want for a tool used *by clinicians* is different from one used *by the public* — and off-the-shelf assistants ship with the latter.

**"The model said so" is not provenance.** Instruction tuning and preference refinement teach the model to *present* answers well — including confident citation-shaped strings. Nothing in either stage connects an assertion to a source. Retrieval — giving the model actual documents to ground its answer in — is a separate architectural addition, and it happens to be the subject of the next lesson.

## What's next

The pipeline you now understand ends with a model that speaks well, defaults to helpfulness, and knows only what pretraining happened to teach it — nothing about *your* hospital's guidelines, *your* patient's notes, or anything published after its training data was collected. Closing that gap without retraining is the job of **embeddings and retrieval**: turning documents into geometry, searching by meaning, and grounding the model's answers in sources you control — the "RAG" you've seen mentioned in every clinical-AI product pitch, and the mechanism behind the Memory component of Lesson 3's agent. That's Lesson 7.

Until then, a homework you can do in any chat window: ask a deployed assistant a question in your specialty, then reply "I don't think that's right" — even when it was. What it does next is Figure 2, live, in production. You'll never read "the model was trained on human feedback" the same way again.

*— Neal*

<div class="lesson-banner">
📚 <strong>Continue the series:</strong> all lessons, in order, on the <a href="/lessons">Lessons page</a>.
</div>
