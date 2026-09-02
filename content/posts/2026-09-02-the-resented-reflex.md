---
title: "The Resented Reflex: Training Doubt When AI Literacy Has Already Failed"
date: 2026-09-02
category: AI & Medicine
tags: automation bias, discernment, clinical AI, medical education, simulation, signal detection theory, cognitive forcing, deskilling, debiasing, assessment, Kenya, AI fluency
level: All readers — no technical background assumed
read_time: 41 min
summary: "Commitment two of the Institute's ten is nine words long: scepticism is trained explicitly, and it is assessed. It is the commitment the founding evidence directly implicates, and the one I have never properly defended. This is the fifth companion to the blueprint. It reads the randomised trial the whole argument rests on closely enough to say what it does and does not establish — including that it enrolled 44 physicians. It assembles the convergent evidence from mammography, dermatology, pathology, colonoscopy and thirty years of aviation human factors, including the study whose average effect was zero while concealing help for the weakest readers and harm to the strongest on exactly the hardest cases. Then it confronts the literature nobody designing an AI curriculum wants to cite: taught debiasing does not transfer, and a controlled trial in 191 senior medical students found cognitive forcing strategies made no difference at all. What survives that is a design rather than a syllabus — the independent-impression rule as a structural constraint, a seeded-error bank with a deliberately unstable base rate, and scoring by signal detection rather than catch rate, because a candidate who rejects every AI output is not discerning, they are useless in a different direction. Ends with what would refute the whole thing."
featured: false
---

<div style="font-size:0.85em; background:#111827; border-left:4px solid #6b82a0; padding:0.9em 1.3em; border-radius:0 6px 6px 0; margin:1.5em 0; color:#9fb3cc;">
<em>I write here in a personal capacity. This is the fifth companion to <a href="/post/2026-08-05-another-arrow-in-the-quiver" style="color:#00d4f5;">Another Arrow in the Quiver</a>, following <a href="/post/2026-08-10-borrowed-from-an-art-school" style="color:#00d4f5;">Borrowed From an Art School</a> on where the competency framework came from, <a href="/post/2026-08-11-one-hidden-error" style="color:#00d4f5;">One Hidden Error</a> on the OSCE and the AI-OSCE, <a href="/post/2026-08-12-the-angoff-panel-for-testing-clinicians" style="color:#00d4f5;">The Angoff Panel</a> on where the pass mark comes from, and <a href="/post/2026-08-17-measuring-what-actually-matters" style="color:#00d4f5;">Measuring What Actually Matters</a> on how we would know whether any of it worked. Read on its own it should still make sense; nothing here assumes a background in statistics or in teaching.</em>
</div>

<style>
.rr-callout { font-size: 0.9em; background: #101a2e; border-left: 4px solid #00d4f5; padding: 0.9em 1.3em; margin: 1.4em 0; border-radius: 0 4px 4px 0; }
.rr-warn { font-size: 0.9em; background: #1a0f14; border-left: 4px solid #f87171; padding: 0.9em 1.3em; margin: 1.4em 0; border-radius: 0 4px 4px 0; }
.rr-key { font-size: 0.95em; background: #0e1e1a; border-left: 4px solid #10b981; padding: 0.9em 1.3em; margin: 1.4em 0; border-radius: 0 4px 4px 0; }
.rr-note { font-size: 0.88em; background: #141033; border-left: 4px solid #a78bfa; padding: 0.9em 1.3em; margin: 1.4em 0; border-radius: 0 4px 4px 0; }
.rr-fig { margin: 2.2em auto 2.6em; max-width: 100%; }
.rr-fig svg { display: block; width: 100%; height: auto; border-radius: 10px; box-shadow: 0 2px 14px rgba(0,0,0,0.4); }
.rr-fig figcaption { font-size: 0.82em; color: #6b82a0; margin-top: 0.8em; text-align: center; font-style: italic; }
@media (min-width: 1080px) {
  .rr-fig { width: min(1140px, calc(100vw - 3rem)); margin-left: 50%; transform: translateX(-50%); }
  .rr-fig figcaption { max-width: 820px; margin-left: auto; margin-right: auto; }
}
</style>

Commitment two, in the [blueprint](/post/2026-08-05-another-arrow-in-the-quiver), is nine words:

> **Scepticism is trained explicitly, and it is assessed.** Not a lecture on limitations — a drilled reflex, like recognising a deteriorating patient.

Of the ten commitments this is the one I have leaned on hardest and defended least. Every other companion post in this series has been about machinery — how you set a pass mark, how you build an examination, how you measure whether any of it survived contact with a ward. This one is about the thing the machinery is for. It is also the only commitment that the trial I keep citing directly implicates, because that trial is a study of people who had been taught about AI and were harmed by it anyway.

So this post does four things. It reads that trial properly, including the parts that weaken it. It assembles the wider evidence, which is older and broader than anyone writing an AI curriculum in 2026 seems to acknowledge. It then confronts a literature that ought to terrify everyone in this field and is almost never cited in it — the medical education research showing that taught debiasing does not work. And it sets out what I would build instead, in enough operational detail that somebody could disagree with a specific number rather than with a mood.

I will say the conclusion at the top, because it is the part I would most like argued with.

<div class="rr-key">
<strong>Discernment is not a knowledge deficit, and it cannot be fixed with information.</strong> It is a cost problem: verifying a plausible answer is expensive, and being right is usually free. A curriculum that treats it as a knowledge deficit — a module, a lecture, a list of limitations, a mnemonic — is answering a question nobody asked, and the evidence that this fails is thirty years old. What changes behaviour is structure, drill and consequence: a workflow that makes the clinician's own impression a fixed point, simulation to a mastery standard, and an assessment that a fluent, confident, well-liked candidate can actually fail.
</div>

---

## Part 1 — The trial, read properly

The study is [*Automation Bias in Large Language Model–Assisted Diagnostic Reasoning among Physicians Trained in AI Literacy*](https://ai.nejm.org/doi/full/10.1056/AIoa2501001), by Qazi and colleagues, published in *NEJM AI* in 2025 and available as a [preprint](https://www.medrxiv.org/content/10.1101/2025.08.23.25334280v1). It was prospectively registered (NCT06963957) before enrolment, with the statistical analysis plan uploaded in advance. I want to set out what it actually did, because I have seen it cited three times now as though it showed that AI makes doctors worse, which is not what it showed.

**The population.** Forty-four physicians registered with the Pakistan Medical and Dental Council, recruited from two consecutive cohorts of a training programme at the Lahore University of Management Sciences. Median clinical experience ten years. Every one of them had completed a twenty-hour AI-literacy course covering large language model capabilities, prompt engineering, and strategies for critically evaluating AI-generated output. This is the feature that makes the trial worth building a curriculum around: the participants were not naive. They were the product of exactly the intervention most health systems are currently commissioning.

**The design.** Randomised 1:1, single-blind, participants blinded to the study's aims. Six clinical vignettes across internal medicine, cardiology, neurology, paediatrics, infectious disease and emergency medicine, developed by three physician co-authors, with the too-easy and the too-rare deliberately excluded. Seventy-five minutes. The control arm received unmodified ChatGPT-4o output on all six cases. The treatment arm received output into which subtle but clinically significant errors had been embedded on three of the six — errors designed to be detectable by a competent physician but not obvious on casual reading — with the position of the erroneous cases randomised so that no pattern could be learned.

Three features of the design matter more than the headline number.

First, **consultation was voluntary and required an explicit click**. Nobody was forced to look at the model. This is the on-demand pattern that is actually spreading in clinical practice, as opposed to the mandatory-review or always-visible designs used in most earlier work, and it is the pattern that preserves the autonomy everyone invokes when they say the clinician remains responsible.

Second, **both arms kept their ordinary resources** — medical databases, standard search — with a browser extension specifically blocking Google's AI Overviews so that the control arm's exposure was genuinely controlled. That is a level of methodological care I would not have expected.

Third, **the primary endpoint was reasoning, not the answer**. Participants documented their top three differentials with supporting and opposing evidence, their top choice with justification, and recommended next steps. Three blinded physicians scored each response against a rubric developed by independent solution of every case and consensus resolution of discrepancies. Inter-rater reliability was high (Krippendorff's α = 0.93) and the instrument's internal consistency was strong (Cronbach's α = 0.80).

**The result.** Mean diagnostic reasoning accuracy was 84.9% in the control arm and 73.3% in the treatment arm: an adjusted difference of **−14.0 percentage points** (95% CI −18.9 to −9.1; *P* < .0001) from a pre-specified linear mixed-effects model with random effects for participant and for case. On the secondary endpoint, top-choice diagnostic accuracy, 90.5% versus 76.1%, an adjusted **−18.3 percentage points** (95% CI −26.6 to −10.0; *P* < .0001).

Now the detail that I think is the most important single number in the paper, and which almost nobody quotes.

<div class="rr-callout">
<strong>Consultation rates were the same in both arms: 68.9% of cases in the treatment group, 66.7% in the control group (<em>P</em> = .69).</strong> The physicians who were harmed did not consult the model more than the physicians who were not. They consulted it at the same rate, read what it said, and were degraded by the content. This rules out the comfortable explanation — that the problem is overuse and the fix is to use it less. The problem is what happens inside a clinician's head between reading a plausible paragraph and writing down a differential, and it happens at ordinary rates of use.
</div>

**The subgroups**, which are where the paper gets interesting and where I would be most careful. Physicians at or above the median of ten years' practice were harmed *more* (−16.6 percentage points, 95% CI −23.1 to −10.1) than those below it (−9.1, 95% CI −18.1 to −0.1). Physicians using large language models at least weekly showed a significant decrement (−11.0, 95% CI −18.5 to −3.6); infrequent users' point estimate was almost identical (−10.7) but its interval crossed zero (95% CI −24.5 to 3.1), which is a statement about sample size rather than about infrequent users. And male physicians showed −25.8 (95% CI −33.8 to −17.7) against −2.1 in female physicians (95% CI −9.8 to 5.5, not significant).

### What I would and would not teach from this

<div class="rr-warn">
<strong>I would not teach the gender finding, and I would not put it on a slide.</strong> Twenty-two participants per arm, split by sex, gives cells of roughly ten people. The subgroup analyses were not adjusted for multiple comparisons — the authors say so. A difference of that size between two handfuls of people, in one institution in one city, with a mechanism offered post hoc, is a hypothesis at best and noise at worst. The same caution applies with less force to the experience and frequency findings, which at least have a plausible mechanism and point in a direction other work supports. Citing the striking subgroup and ignoring the interval is precisely the sloppiness this entire curriculum is supposed to train against, and I would be a hypocrite to do it in the lecture where I introduce the trial.
</div>

The honest summary of the trial's limits, most of which the authors state themselves:

- **Forty-four people.** The recruitment target was fifty; the observed effect was large enough that the study remained adequately powered, but this is a small trial and the confidence intervals are correspondingly generous.
- **Vignettes, not patients.** No time pressure of the real kind, no multimorbidity, no relatives in the corridor, no consequence for being wrong.
- **The errors were ours, not the model's.** Errors introduced deliberately by a panel of physicians are the errors physicians can imagine. Real model failures may be more subtle, or differently shaped, or concentrated in places we would not think to seed.
- **One model, one session.** ChatGPT-4o, in mid-2025, in a single 75-minute sitting. Whether the effect grows or shrinks with months of use is exactly the question the design cannot answer.
- **Physicians only.** No nurses, no clinical officers, no pharmacists — which for an institution whose largest and highest-yield cadre is nursing is a substantial gap.
- **No mitigation was tested.** The trial establishes the problem. It says nothing whatever about the fix, which is the entire subject of this post.

What survives all of that is the direction and the rough order of magnitude. A pre-registered randomised design, blinded graders, high inter-rater reliability, a pre-specified primary endpoint, an effect of fourteen points with an interval nowhere near zero, and an equal consultation rate that closes off the easy explanation. I am comfortable building on the claim that *AI-literacy training did not protect these physicians*. I am not comfortable building on any number in the paper to two significant figures, and the curriculum should not depend on one.

---

## Part 2 — This is not one study

The reason I am willing to design an institution around a 44-person trial is that it is not load-bearing on its own. It is the most recent and most directly relevant point on a line that runs back through radiology, dermatology, pathology and endoscopy to thirty years of aviation human factors. The consistency is the argument.

### The taxonomy, from the cockpit

The vocabulary comes from Linda Skitka, Kathleen Mosier and colleagues, working on glass-cockpit aviation in the late 1990s. Their [*Does automation bias decision-making?*](https://www.sciencedirect.com/science/article/abs/pii/S1071581999902525) and [*Accountability and automation bias*](https://www.sciencedirect.com/science/article/abs/pii/S107158199990349X) established the split that still organises the field:

- **Errors of omission** — failing to respond to a problem because the automation did not flag it. The system said nothing, so nothing was done.
- **Errors of commission** — following an automated directive despite contradictory information available from more reliable sources, because the operator either did not check or discounted what they found.

Raja Parasuraman and Victor Riley's [*Humans and Automation: Use, Misuse, Disuse, Abuse*](https://journals.sagepub.com/doi/10.1518/001872097778543886) (*Human Factors*, 1997) gave the field its other durable frame: over-reliance is **misuse**, neglect of a useful aid is **disuse**, and both are failures. This is the origin of the inverted-U I use in the blueprint, and of John Lee and Katrina See's later [*Trust in Automation: Designing for Appropriate Reliance*](https://journals.sagepub.com/doi/10.1518/hfes.46.1.50_30392) (2004), which is where the language of *calibrated* trust comes from. The target has never been maximal trust and has never been minimal trust. It is trust that tracks the actual reliability of the thing in front of you, which is a discrimination problem, and I will come back to that word because it determines how the examination has to be scored.

<div class="rr-note">
<strong>Why the aviation provenance matters practically.</strong> It means the failure mode was characterised, named and studied for a decade before anyone put a language model in a clinic — and it means the mitigations were also tried. We are not at the beginning of this. We are quite late to it, holding a tool whose surface is more persuasive than anything the aviation literature ever tested.
</div>

### The medical evidence

**Goddard, Roudsari and Wyatt**, [*Automation bias: a systematic review of frequency, effect mediators, and mitigators*](https://academic.oup.com/jamia/article-abstract/19/1/121/732254) (*JAMIA*, 2012), is the review that establishes the pattern in clinical decision support: overall performance usually improves, and the new errors the system introduces usually go unrecognised. Both halves of that sentence are true simultaneously, which is why arguments about clinical AI go round in circles — the advocate quotes the first half and the sceptic quotes the second, and neither is wrong.

**Lyell and Coiera**, [*Automation bias and verification complexity: a systematic review*](https://academic.oup.com/jamia/article/24/2/423/2631492) (*JAMIA*, 2017), screened 890 papers to 40 and found automation bias concentrated in single tasks with **high verification complexity**, typically diagnosis rather than monitoring — contradicting the received human-factors view that it is a multitasking phenomenon. Their conclusion is that automation bias tracks cognitive load, and that mitigation should therefore target load reduction.

<div class="rr-key">
That finding is the hinge of this entire post. <strong>If automation bias is driven by verification complexity, then it is a cost problem, not an ignorance problem.</strong> The clinician is not failing to check because they do not know they should. They are failing to check because checking is expensive, the answer looks right, and there are eleven people waiting. Every intervention I propose later is an attempt to lower the cost of checking or raise the cost of not checking. Telling people to check harder does neither.
</div>

**Povyakalo, Alberdi, Strigini and Ayton**, [*How to Discriminate between Computer-Aided and Computer-Hindered Decisions*](https://journals.sagepub.com/doi/10.1177/0272989X12465490) (*Medical Decision Making*, 2013), is the study I would put in front of any minister of health being sold a national screening deployment. Fifty professionals read 180 mammograms with and without computer-aided detection. The original analysis found no significant average effect. The reanalysis found that CAD raised sensitivity by about 0.016 for the 44 least discriminating readers on 45 relatively easy, mostly CAD-detected cancers — and *lowered* sensitivity by 0.145 for the 6 most discriminating readers on the 15 relatively difficult cancers.

<div class="rr-warn">
Read that twice. <strong>The average effect was nil. Underneath the average, the tool gave a small benefit to weak readers on easy cancers and did substantial harm to the best readers on the hardest cancers.</strong> That is the worst possible distribution of an effect and it is completely invisible in the headline. It is also the distribution you would expect from automation bias operating on people whose independent judgement was worth the most. Any evaluation of clinical AI that reports only a mean, without stratifying by reader skill and case difficulty, is capable of concealing exactly this.
</div>

**Dratsch and colleagues**, [*Automation Bias in Mammography*](https://pubs.rsna.org/doi/10.1148/radiol.222176) (*Radiology*, 2023), gave 27 radiologists 50 mammograms with purported AI-generated BI-RADS categories, incorrect on 12 of the 40 in the test set. Incorrect suggestions impaired performance across the whole experience range, from inexperienced to very experienced. The inexperienced were hit hardest; the very experienced were hit too.

**Tschandl and colleagues**, [*Human–computer collaboration for skin cancer recognition*](https://www.nature.com/articles/s41591-020-0942-0) (*Nature Medicine*, 2020), reached the two-sided version of the same conclusion: good AI support improved accuracy beyond either party alone, with the least experienced gaining most — and faulty AI misled the entire spectrum of clinicians, experts included.

**Gaube and colleagues**, [*Do as AI say: susceptibility in deployment of clinical decision-aids*](https://www.nature.com/articles/s41746-021-00385-9) (*npj Digital Medicine*, 2021), ran a design I find quietly devastating. Physicians received chest radiographs with diagnostic advice — *all* of it written by human experts, some of it labelled as coming from an AI. Radiologists rated advice as lower quality when it carried the AI label; physicians with less task expertise did not. But diagnostic accuracy was significantly worse when the advice was inaccurate **regardless of the label**. The scepticism the experts expressed about the source did not translate into protection from the content.

**Budzyń and colleagues**, [*Endoscopist deskilling risk after exposure to artificial intelligence in colonoscopy*](https://www.thelancet.com/journals/langas/article/PIIS2468-1253(25)00133-5/abstract) (*Lancet Gastroenterology & Hepatology*, 2025), looked at four Polish centres in the ACCEPT trial and compared *unassisted* colonoscopy in the three months before AI was introduced with unassisted colonoscopy in the three months after. Adenoma detection rate fell from 28.4% (226 of 795) to 22.4% (145 of 648) — an absolute difference of **−6.0 percentage points** in procedures where no AI was present at all.

This is observational, it is a before-and-after within a trial context, and it has every confounder that design implies; the accompanying commentary says so. But it is the first substantial real-world signal that the underlying human skill degrades, and it degrades in the direction and on the timescale that would matter to us. Six points of adenoma detection is not a subtle finding.

**Vaccaro, Almaatouq and Malone**, [*When combinations of humans and AI are useful: a systematic review and meta-analysis*](https://www.nature.com/articles/s41562-024-02024-1) (*Nature Human Behaviour*, 2024), pooled 106 experimental studies and 370 effect sizes. On average, human–AI combinations performed **significantly worse than the better of human or AI alone**. Losses were concentrated in decision-making tasks; gains were in content creation. Where humans outperformed the AI, the combination gained; where the AI outperformed humans, the combination lost.

And **Krügel, Ostermaier and Uhl**, [*ChatGPT's inconsistent moral advice influences users' judgment*](https://www.nature.com/articles/s41598-023-31341-0) (*Scientific Reports*, 2023), established something with direct consequences for how we assess: users were influenced by inconsistent advice even when they knew it came from a chatbot, and **they underestimated how much they had been influenced**.

<div class="rr-key">
<strong>Therefore self-report cannot measure discernment.</strong> "How much did the AI influence your decision?" is not a measurement instrument; it is a measurement of what people believe about themselves, and we have direct evidence that the belief is wrong in a known direction. Every assessment described in Part 6 is behavioural for this reason. Confidence questionnaires have a role — they detect the dangerous combination of high confidence and low performance — but never as evidence of the skill.
</div>

<figure class="rr-fig">
<svg viewBox="0 0 1240 560" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Convergent evidence on automation bias: quantified degradations from four studies with confidence intervals where reported, and five further studies where the direction is established but the magnitude is not summarised here">
<rect x="0" y="0" width="1240" height="560" rx="14" fill="#0d1424" stroke="#182742" stroke-width="1"/>
<text x="620.0" y="40" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="19" fill="#c9d6e8" text-anchor="middle" font-weight="bold" letter-spacing="2.5">CONVERGENT EVIDENCE</text>
<text x="620.0" y="63" font-family="Helvetica, Arial, sans-serif" font-size="11.5" fill="#6b82a0" text-anchor="middle">nine studies, four modalities, three decades — the units differ, so this is a picture of consistency, not a meta-analysis</text>
<text x="60" y="92" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11" fill="#6b82a0" letter-spacing="1.5">QUANTIFIED — CHANGE IN EACH STUDY&#39;S OWN UNITS (PERCENTAGE POINTS)</text>
<line x1="470.0" y1="112" x2="470.0" y2="316" stroke="#243a5e" stroke-width="0.8" stroke-dasharray="3 4"/>
<text x="470.0" y="334" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#6b82a0" text-anchor="middle">-30</text>
<line x1="564.4" y1="112" x2="564.4" y2="316" stroke="#243a5e" stroke-width="0.8" stroke-dasharray="3 4"/>
<text x="564.4" y="334" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#6b82a0" text-anchor="middle">-25</text>
<line x1="658.9" y1="112" x2="658.9" y2="316" stroke="#243a5e" stroke-width="0.8" stroke-dasharray="3 4"/>
<text x="658.9" y="334" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#6b82a0" text-anchor="middle">-20</text>
<line x1="753.3" y1="112" x2="753.3" y2="316" stroke="#243a5e" stroke-width="0.8" stroke-dasharray="3 4"/>
<text x="753.3" y="334" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#6b82a0" text-anchor="middle">-15</text>
<line x1="847.8" y1="112" x2="847.8" y2="316" stroke="#243a5e" stroke-width="0.8" stroke-dasharray="3 4"/>
<text x="847.8" y="334" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#6b82a0" text-anchor="middle">-10</text>
<line x1="942.2" y1="112" x2="942.2" y2="316" stroke="#243a5e" stroke-width="0.8" stroke-dasharray="3 4"/>
<text x="942.2" y="334" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#6b82a0" text-anchor="middle">-5</text>
<line x1="1036.7" y1="112" x2="1036.7" y2="316" stroke="#6b82a0" stroke-width="1.6" stroke-dasharray=""/>
<text x="1036.7" y="334" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#6b82a0" text-anchor="middle">+0</text>
<line x1="1131.1" y1="112" x2="1131.1" y2="316" stroke="#243a5e" stroke-width="0.8" stroke-dasharray="3 4"/>
<text x="1131.1" y="334" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#6b82a0" text-anchor="middle">+5</text>
<text x="1036.7" y="104" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10" fill="#6b82a0" text-anchor="middle">no change</text>
<text x="446" y="127" font-family="Helvetica, Arial, sans-serif" font-size="12.5" fill="#c9d6e8" text-anchor="end" font-weight="bold">Qazi 2025 — LLM, physicians</text>
<text x="446" y="142" font-family="Helvetica, Arial, sans-serif" font-size="10.5" fill="#6b82a0" text-anchor="end">diagnostic reasoning accuracy</text>
<line x1="679.7" y1="123" x2="864.8" y2="123" stroke="#00d4f5" stroke-width="3.4" stroke-opacity="0.5" stroke-linecap="round"/>
<line x1="679.7" y1="115" x2="679.7" y2="131" stroke="#00d4f5" stroke-width="2" stroke-opacity="0.75"/>
<line x1="864.8" y1="115" x2="864.8" y2="131" stroke="#00d4f5" stroke-width="2" stroke-opacity="0.75"/>
<circle cx="772.2" cy="123" r="6.5" fill="#00d4f5"/>
<text x="772.2" y="110" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#00d4f5" text-anchor="middle">-14.0  [-18.9, -9.1]</text>
<text x="446" y="173" font-family="Helvetica, Arial, sans-serif" font-size="12.5" fill="#c9d6e8" text-anchor="end" font-weight="bold">Qazi 2025 — LLM, physicians</text>
<text x="446" y="188" font-family="Helvetica, Arial, sans-serif" font-size="10.5" fill="#6b82a0" text-anchor="end">top-choice diagnostic accuracy</text>
<line x1="534.2" y1="169" x2="847.8" y2="169" stroke="#00d4f5" stroke-width="3.4" stroke-opacity="0.5" stroke-linecap="round"/>
<line x1="534.2" y1="161" x2="534.2" y2="177" stroke="#00d4f5" stroke-width="2" stroke-opacity="0.75"/>
<line x1="847.8" y1="161" x2="847.8" y2="177" stroke="#00d4f5" stroke-width="2" stroke-opacity="0.75"/>
<circle cx="691.0" cy="169" r="6.5" fill="#00d4f5"/>
<text x="691.0" y="156" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#00d4f5" text-anchor="middle">-18.3  [-26.6, -10.0]</text>
<text x="446" y="219" font-family="Helvetica, Arial, sans-serif" font-size="12.5" fill="#c9d6e8" text-anchor="end" font-weight="bold">Povyakalo 2013 — CAD mammography</text>
<text x="446" y="234" font-family="Helvetica, Arial, sans-serif" font-size="10.5" fill="#6b82a0" text-anchor="end">6 most discriminating readers, 15 hardest cancers</text>
<circle cx="762.8" cy="215" r="6.5" fill="#f87171"/>
<text x="762.8" y="202" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#f87171" text-anchor="middle">-14.5  (no CI reported)</text>
<text x="446" y="265" font-family="Helvetica, Arial, sans-serif" font-size="12.5" fill="#c9d6e8" text-anchor="end" font-weight="bold">Povyakalo 2013 — CAD mammography</text>
<text x="446" y="280" font-family="Helvetica, Arial, sans-serif" font-size="10.5" fill="#6b82a0" text-anchor="end">44 least discriminating readers, 45 easiest cancers</text>
<circle cx="1066.9" cy="261" r="6.5" fill="#10b981"/>
<text x="1066.9" y="248" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#10b981" text-anchor="middle">+1.6  (no CI reported)</text>
<text x="446" y="311" font-family="Helvetica, Arial, sans-serif" font-size="12.5" fill="#c9d6e8" text-anchor="end" font-weight="bold">Budzyń 2025 — colonoscopy</text>
<text x="446" y="326" font-family="Helvetica, Arial, sans-serif" font-size="10.5" fill="#6b82a0" text-anchor="end">adenoma detection rate, unassisted procedures</text>
<circle cx="923.3" cy="307" r="6.5" fill="#a78bfa"/>
<text x="923.3" y="294" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#a78bfa" text-anchor="middle">-6.0  (no CI reported)</text>
<line x1="60" y1="374" x2="1180" y2="374" stroke="#182742" stroke-width="1"/>
<text x="60" y="398" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11" fill="#6b82a0" letter-spacing="1.5">DIRECTION ESTABLISHED — MAGNITUDE NOT REDUCIBLE TO ONE NUMBER, SO NOT PLOTTED</text>
<rect x="64.0" y="412" width="210.0" height="86" rx="7" fill="#101a2e" stroke="#182742" stroke-width="1"/>
<text x="76.0" y="432" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11.5" fill="#00d4f5" font-weight="bold">Dratsch 2023</text>
<text x="76.0" y="446" font-family="Helvetica, Arial, sans-serif" font-size="9.5" fill="#6b82a0" font-style="italic">Radiology</text>
<text x="76.0" y="464" font-family="Helvetica, Arial, sans-serif" font-size="10" fill="#c9d6e8">incorrect AI BI-RADS impaired</text>
<text x="76.0" y="477" font-family="Helvetica, Arial, sans-serif" font-size="10" fill="#c9d6e8">readers at every experience</text>
<text x="76.0" y="490" font-family="Helvetica, Arial, sans-serif" font-size="10" fill="#c9d6e8">level</text>
<rect x="288.0" y="412" width="210.0" height="86" rx="7" fill="#101a2e" stroke="#182742" stroke-width="1"/>
<text x="300.0" y="432" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11.5" fill="#00d4f5" font-weight="bold">Tschandl 2020</text>
<text x="300.0" y="446" font-family="Helvetica, Arial, sans-serif" font-size="9.5" fill="#6b82a0" font-style="italic">Nature Medicine</text>
<text x="300.0" y="464" font-family="Helvetica, Arial, sans-serif" font-size="10" fill="#c9d6e8">faulty AI misled the whole</text>
<text x="300.0" y="477" font-family="Helvetica, Arial, sans-serif" font-size="10" fill="#c9d6e8">spectrum of clinicians,</text>
<text x="300.0" y="490" font-family="Helvetica, Arial, sans-serif" font-size="10" fill="#c9d6e8">experts included</text>
<rect x="512.0" y="412" width="210.0" height="86" rx="7" fill="#101a2e" stroke="#182742" stroke-width="1"/>
<text x="524.0" y="432" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11.5" fill="#00d4f5" font-weight="bold">Gaube 2021</text>
<text x="524.0" y="446" font-family="Helvetica, Arial, sans-serif" font-size="9.5" fill="#6b82a0" font-style="italic">npj Digital Medicine</text>
<text x="524.0" y="464" font-family="Helvetica, Arial, sans-serif" font-size="10" fill="#c9d6e8">inaccurate advice degraded</text>
<text x="524.0" y="477" font-family="Helvetica, Arial, sans-serif" font-size="10" fill="#c9d6e8">accuracy whatever it was</text>
<text x="524.0" y="490" font-family="Helvetica, Arial, sans-serif" font-size="10" fill="#c9d6e8">labelled as</text>
<rect x="736.0" y="412" width="210.0" height="86" rx="7" fill="#101a2e" stroke="#182742" stroke-width="1"/>
<text x="748.0" y="432" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11.5" fill="#00d4f5" font-weight="bold">Vaccaro 2024</text>
<text x="748.0" y="446" font-family="Helvetica, Arial, sans-serif" font-size="9.5" fill="#6b82a0" font-style="italic">Nature Human Behaviour</text>
<text x="748.0" y="464" font-family="Helvetica, Arial, sans-serif" font-size="10" fill="#c9d6e8">106 studies: human–AI worse on</text>
<text x="748.0" y="477" font-family="Helvetica, Arial, sans-serif" font-size="10" fill="#c9d6e8">average than the better of</text>
<text x="748.0" y="490" font-family="Helvetica, Arial, sans-serif" font-size="10" fill="#c9d6e8">either alone</text>
<rect x="960.0" y="412" width="210.0" height="86" rx="7" fill="#101a2e" stroke="#182742" stroke-width="1"/>
<text x="972.0" y="432" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11.5" fill="#00d4f5" font-weight="bold">Krügel 2023</text>
<text x="972.0" y="446" font-family="Helvetica, Arial, sans-serif" font-size="9.5" fill="#6b82a0" font-style="italic">Scientific Reports</text>
<text x="972.0" y="464" font-family="Helvetica, Arial, sans-serif" font-size="10" fill="#c9d6e8">users are influenced by advice</text>
<text x="972.0" y="477" font-family="Helvetica, Arial, sans-serif" font-size="10" fill="#c9d6e8">and underestimate the</text>
<text x="972.0" y="490" font-family="Helvetica, Arial, sans-serif" font-size="10" fill="#c9d6e8">influence</text>
</svg>
<figcaption>The case does not rest on one trial. Four studies report a quantified degradation, in four different units — diagnostic reasoning score, top-choice accuracy, reader sensitivity, adenoma detection rate — so the horizontal axis is a scale of magnitude and emphatically not a pooled effect. <strong>The two Povyakalo rows are the ones to look at.</strong> The same tool, in the same study, helped the weakest readers slightly on the easiest cancers and harmed the strongest readers substantially on the hardest — and the study's average effect was null. The five studies in the lower band establish the same direction in designs that do not reduce to a single percentage.</figcaption>
</figure>

---

## Part 3 — Why teaching literacy produces the problem it claims to solve

Here is the distinction the whole commitment turns on, stated as precisely as I can manage.

**AI literacy** is knowledge *about* the system. What a language model is. Why it produces fluent text without a model of truth. What a hallucination is and roughly how often it happens. How to write a better prompt. Which tasks it is good at. This is genuinely useful, it is teachable in a day, and it is what almost every clinical AI curriculum currently on offer consists of.

**AI discernment** is a behaviour *in the presence of* the system. It is the act of forming your own impression before you look; of noticing that the paragraph in front of you is internally consistent and externally wrong; of paying the verification cost when you are tired, behind, and the answer looks right. It is not knowledge. It is a performance, executed under load, repeatedly, for years.

The Qazi trial is the cleanest available demonstration that the first does not produce the second. Twenty hours of the first, and the second was absent when it was needed. And there are three mechanisms in the literature that explain why, none of which is fixed by more of the first.

### Mechanism one: cognitive offloading

The availability of a plausible answer reduces the effort invested in generating your own. This is the mechanism the trial's authors invoke and it is the one clinicians recognise immediately when it is described to them, usually with a slightly guilty expression. It is not laziness in any morally interesting sense. It is the same adaptive process that lets you stop doing mental arithmetic when there is a calculator on the desk, and it is normally a good thing. It becomes dangerous only when the calculator is wrong sometimes and you have no cheap way of telling which times.

### Mechanism two: the narrative surface

Qazi and colleagues make a point in their introduction that I think is underrated, and it distinguishes this generation of tools from everything the older literature studied. A conventional model outputs a discrete classification with a confidence score: *malignant, 92%*. That is a claim you can hold at arm's length. It announces itself as a machine output and it carries its own uncertainty on its face. A language model outputs a narrative — differentials with supporting and opposing evidence, a recommended next step, a caveat, a hedge in the right place. It has the surface features of clinical reasoning. It reads like a good registrar.

That surface is doing work. It is not merely that the output is persuasive; it is that the output *mimics the very signals clinicians use to judge whether reasoning is sound*. We are trained to trust an argument that considers alternatives and states its evidence. Here is a system that generates the form of that reliably and the substance of it only usually.

### Mechanism three: fluency lowers friction

This is the mechanism I find most uncomfortable, because it implicates my own teaching. The trial found the significant decrement among physicians using language models **at least weekly**. The infrequent users' point estimate was nearly identical, so I will not claim the trial demonstrates that frequent use is worse — the honest reading is that the trial was underpowered to distinguish them. But it is consistent with a mechanism that is independently plausible: the more fluent the user, the lower the friction, the faster the consult, the less deliberate the reading, and the more the output slides into the reasoning unexamined.

<div class="rr-warn">
<strong>If that mechanism is real, then a curriculum that teaches fluency and stops there does not merely fail to help. It hands the clinician a faster route to the failure mode.</strong> It is the equivalent of teaching someone to place a central line without teaching them to recognise a pneumothorax — a comparison I have used before and now think is too generous, because the pneumothorax at least announces itself.
</div>

### The economics, stated plainly

Put the three mechanisms together with Lyell and Coiera's finding that automation bias tracks verification complexity, and the shape of the problem is economic rather than epistemic.

Consider what it costs a clinician to verify a plausible AI-generated differential in a district hospital at eleven at night. Two minutes at least, often ten. Attention taken from a queue. A working memory already carrying four other patients. And what does verification usually buy? Confirmation that the answer was fine. The expected return on any individual act of checking is low, because the tool is usually right — which is exactly the condition under which automation bias flourishes. A tool that was wrong half the time would train scepticism by itself, for free, in a week. A tool that is wrong three per cent of the time trains the opposite, and the three per cent is where the patients are.

<div class="rr-key">
<strong>You do not solve a cost problem by informing people that the cost exists.</strong> You solve it by changing the costs. Every element of the design in Part 6 is either a reduction in the cost of checking — structure, protocol, tooling, a second person — or an increase in the cost of not checking: assessment, countersignature, audit, consequence. This is why commitment two has two clauses, and why the second one is the one that does the work.
</div>

---

## Part 4 — The literature nobody designing an AI curriculum wants to cite

I have now made the case that scepticism must be trained. Before describing how, I have to deal with the evidence that training it does not work, because it exists, it is good, and I have not seen it cited once in a clinical AI curriculum document.

### Taught debiasing does not transfer

The medical education community spent a decade on this in the context of ordinary diagnostic error — anchoring, availability, premature closure — long before AI. The intervention was **cognitive forcing strategies**: teaching clinicians to recognise the situations in which a given bias arises and to deliberately apply a counter-routine.

**Sherbino, Kulasegaram, Howey and Norman**, [*Ineffectiveness of cognitive forcing strategies to reduce biases in diagnostic reasoning: a controlled trial*](https://www.cambridge.org/core/journals/canadian-journal-of-emergency-medicine/article/ineffectiveness-of-cognitive-forcing-strategies-to-reduce-biases-in-diagnostic-reasoning-a-controlled-trial/B768948819704516DBE325909A8D611E) (*CJEM*, 2014), allocated 191 senior medical students on a four-week emergency medicine rotation to cognitive forcing strategy instruction or control, and tested them at the end of the rotation. There was no difference in the rate of diagnostic error between the groups. An earlier [exploratory study](https://pubmed.ncbi.nlm.nih.gov/21240788/) by the same group had pointed the same way.

That result is not isolated. The pattern across the debiasing literature in medicine is that instruction in bias recognition reliably improves people's ability to *name* biases and reliably fails to improve their diagnostic accuracy. Knowing the name of the trap does not keep you out of it.

And from the aviation side, **Skitka, Mosier, Burdick and Rosenblatt**, [*Automation Bias and Errors: Are Crews Better Than Individuals?*](https://www.tandfonline.com/doi/abs/10.1207/S15327108IJAP1001_5) (*International Journal of Aviation Psychology*, 2000), tested training that focused explicitly on automation bias and its associated errors. It reduced **commission** errors and did not reduce **omission** errors.

<div class="rr-warn">
<strong>That asymmetry is the single most operationally important finding in this post and I want to be blunt about what it implies.</strong> Training can teach a clinician to challenge a wrong recommendation that is in front of them. There is no good evidence that it teaches them to notice the thing the system never mentioned. And in clinical medicine, the omission is the killer: the differential that quietly lacks the tropical diagnosis, the drug interaction not raised, the red flag not asked about. If our simulation bank is built mostly of wrong statements — because wrong statements are easy to write and satisfying to catch — we will be training the error type that training already handles and neglecting the one it does not.
</div>

### What this means for commitment two

Taken at face value, this literature says: writing "scepticism is trained explicitly" into a founding document is close to writing a wish. If I stopped here, the intellectually honest move would be to strike the commitment.

I do not think that is the right conclusion, and here is the argument for why — which is also the argument for what the commitment has to be changed into.

The interventions that failed were **instructional**. A course. A strategy. A named routine to be recalled and applied under load, by an individual, unprompted, in an environment that neither required it nor checked for it. The interventions that have worked in adjacent domains were **structural and procedural**: they changed the task, or they changed what the person was accountable for, or they drilled the behaviour to automaticity against a standard.

<div class="rr-key">
So commitment two, as written, is under-specified in a way that would let it fail exactly as Sherbino's intervention failed. What it needs is a third clause, and I would now write it as: <strong>scepticism is trained explicitly, built into the workflow structurally, and assessed behaviourally.</strong> The middle clause is the one the evidence says is missing from every AI curriculum I have read, including, until I wrote this post, the fine print of my own.
</div>

---

## Part 5 — What the evidence says does work

Three things have support. None is a lecture.

### One: cognitive forcing as structure, not as strategy

The distinction between Sherbino's failed intervention and this one is subtle and it is everything. Sherbino taught people a strategy to apply. The alternative is to build the forcing function into the task so that no recall, no discipline and no virtue is required.

**Buçinca, Malaya and Gajos**, [*To Trust or to Think: Cognitive Forcing Functions Can Reduce Overreliance on AI in AI-Assisted Decision-Making*](https://dl.acm.org/doi/10.1145/3449287) (*Proceedings of the ACM on Human–Computer Interaction*, 2021), tested interventions that structurally interrupt the path of least resistance — most relevantly, requiring the person to commit to their own answer *before* the AI's recommendation is revealed. Their cognitive forcing interventions significantly reduced overreliance, where simply adding explanations to the AI's recommendation did not.

Their theoretical framing is worth stating because it explains why explanation-based approaches keep disappointing: people rarely engage analytically with each individual recommendation and explanation. They develop a general heuristic about whether to follow this system, and then apply the heuristic. A better explanation feeds the heuristic. Only a structural interruption reaches the analytical process at all.

<div class="rr-note">
<strong>And the finding I would put in the faculty handbook.</strong> Buçinca and colleagues also found a trade-off: participants performed better with cognitive forcing and <em>liked it less</em>. Subjective trust and preference moved in the opposite direction from performance. This is not a defect to be designed away. It is the price, and it is why the reflex in this post's title is a resented one. Any institution that optimises its teaching for participant satisfaction will delete the intervention that works, and will have a spreadsheet full of Level 1 scores proving it was right to. I have written about <a href="/post/2026-08-17-measuring-what-actually-matters">why satisfaction data must never be reported as an outcome</a>; this is the concrete case where it would do direct harm.
</div>

### Two: simulation-based mastery learning

If discernment is a performance rather than a knowledge state, it belongs in the tradition of procedural skill acquisition, where the evidence is far more encouraging than in the debiasing tradition.

**McGaghie, Issenberg, Cohen, Barsuk and Wayne**'s [meta-analytic comparison](https://pmc.ncbi.nlm.nih.gov/articles/PMC3102783/) of simulation-based medical education with deliberate practice against traditional clinical education found a pooled effect size of 0.71 (95% CI 0.65–0.76) in favour of simulation with deliberate practice, across the 14 of 3,742 screened studies that met inclusion criteria, and their [critical review of simulation-based mastery learning with translational outcomes](https://asmepublications.onlinelibrary.wiley.com/doi/10.1111/medu.12391) (*Medical Education*, 2014) documents transfer to patient-level results — central line infections, for the canonical example.

The operative words are *deliberate practice* and *mastery*. Not exposure to a simulator. Repeated attempts against a pre-set standard, with immediate specific feedback, continuing until the standard is reached, with the time to reach it allowed to vary between learners rather than the standard varying. That is a different and more expensive thing than what most institutions mean when they say simulation, and it is the only version with this evidence behind it.

### Three: accountability

Skitka, Mosier and Burdick's [accountability study](https://www.sciencedirect.com/science/article/abs/pii/S107158199990349X) found that making participants accountable — for their overall performance or specifically for their decision accuracy — lowered rates of automation bias. This is the cheapest of the three interventions and the one most easily eroded, because accountability that is announced but never enacted decays within about one rotation.

Institutionally it means the countersignature is not paperwork, the audit returns to a named person, and somebody senior occasionally asks a clinician why they accepted a particular recommendation — not punitively, and not rarely enough to be forgettable.

<div class="rr-callout">
<strong>The three combine into one sentence.</strong> Make the clinician commit before they look; drill the catching of errors to a mastery standard against a pass mark that can be failed; and make somebody answerable afterwards for what was accepted. Structure, drill, consequence. Nothing in that sentence is a module.
</div>

---

## Part 6 — The design

This is the part I would want criticised on specifics. Everything above is argument; what follows is a set of decisions, several of which I hold loosely and one or two of which I suspect are wrong in ways I cannot yet see.

### 6.1 The independent-impression rule

**The rule.** Before any AI output is visible, the clinician records their own impression: a leading diagnosis, two alternatives, and the single finding that would most change their mind. Only then does the output unlock.

This is Buçinca's cognitive forcing function, implemented as a workflow constraint rather than as advice. In simulation it is enforced by the platform — the output is behind a control that does not respond until the impression field is complete. In the workplace it is enforced by protocol and by the record, which is weaker, and I will come back to that.

**Three failure modes I would design against from the start.**

*The hedged impression.* The obvious defeat is to write something so vague it cannot be contradicted — "query sepsis, query cardiac, query other" — preserving the option to agree with whatever appears. This converts the rule into a keystroke. So the impression is scored for **specificity and commitment**, and an impression that does not commit is scored as absent, not as partial. Learners are told this explicitly in the first hour, because the point is not to catch them out.

*The retrospective edit.* If the interface permits revision of the impression after the output is revealed, the data is worthless and so is the drill. The impression is timestamped and locked. This is a technical requirement, not a policy one.

*Ritualisation.* The most likely long-run failure is that the rule survives as a form and dies as a habit — a box filled in at speed by someone who has already decided to read the output first. I do not have a clean defence against this. The partial defences are that the impression is periodically scored rather than merely collected, and that the workplace-based assessment described in the [Kirkpatrick companion](/post/2026-08-17-measuring-what-actually-matters) looks at the *content* of impressions and not their presence.

<div class="rr-note">
<strong>An honest note on where this rule comes from.</strong> The independent-impression rule is not something I derived from a trial in clinical medicine. It is the direct clinical translation of Buçinca's laboratory result, supported by the general principle that anchoring is prevented by fixing the anchor rather than by resisting it. I believe it is the highest-yield single element of the design. It has not been tested in a clinical population. In the <a href="/post/2026-08-17-measuring-what-actually-matters">evaluation design</a> I named it as my candidate for the fastest-decaying thing we teach, and I would want it measured first and abandoned if it does not hold.
</div>

### 6.2 The seeded-error bank

Every simulation encounter runs on a sandbox where we control what the model appears to say. A proportion of encounters contain a seeded clinically significant error.

**The taxonomy.** This is the part that has to be Kenyan and specific, per commitment five, and it has to be weighted towards omission, per Skitka. Working categories:

| Category | Example | Type |
|---|---|---|
| Dose or interval wrong for organ function | A standard dose in a patient with an eGFR of 22 | Commission |
| Omitted local differential | A febrile returning-traveller differential with no malaria, or a lymphadenopathy differential with no TB | **Omission** |
| Omitted red flag | A back pain assessment that never asks about bladder function | **Omission** |
| Fabricated or misattributed citation | A confident reference to a guideline that does not say that | Commission |
| Guideline correct elsewhere, wrong here | A recommendation presupposing an investigation unavailable at a Level 4 facility | Commission |
| Nomenclature collision | A drug name that maps to a different agent in our supply chain | Commission |
| Confidently normal reading of an abnormal value | A potassium of 6.1 characterised as "mildly raised, monitor" | Commission |
| Silent scope error | A differential that answers the question asked while ignoring the more important question | **Omission** |
| Skin-tone-dependent misread | A cellulitis or pressure-area assessment degraded on darker skin | Commission |
| Language-transfer error | A history taken in Kiswahili or Dholuo, rendered into English, with the compounding error preserved | Commission |

<div class="rr-key">
<strong>I would mandate that at least 40% of seeded errors are omissions</strong> — the missing differential, the unasked red flag, the unaddressed question — even though omissions are harder to write, harder to score, and much less satisfying for a learner to catch. The reason is Skitka: commission errors are the ones training already reduces. Building a bank of the easy kind and calling it discernment training would produce good pass rates and no protection.
</div>

**The base rate problem, which I do not think has a clean answer.**

In the Qazi trial the seeded-error rate was 50% of cases in the treatment arm. In the blueprint I said roughly one in three, varied so learners cannot game it. Both of those are wildly higher than the real-world rate of clinically significant error in a competent contemporary model, which — depending on task, model and how you define significant — is plausibly in the low single figures per cent.

That gap is a genuine design tension. Train at a high rate and you build a vigilant reflex, but you also train a criterion calibrated to a world that does not exist, and you risk producing under-trust: the clinician who rejects the useful retinopathy screen and misses the retinopathy. Train at the true rate and most learners will complete an entire simulation block without encountering a single error, which trains nothing at all and wastes very expensive faculty time.

My resolution, offered as a decision rather than a solution:

1. **The training rate is deliberately high and deliberately unstable** — varied between 20% and 40% across blocks, never announced, never fixed. High enough to generate practice repetitions; unstable enough that no base rate can be learned and applied as a heuristic, which is precisely the failure Buçinca describes.
2. **The assessment rate is set separately, disclosed as a design choice in the assessment blueprint, and held constant within a cohort** for fairness. Candidates are told that some proportion of stations contain errors and are not told which or how many.
3. **The recertification rate is set from our own audit data** — whatever our incident reporting and case review say the real local rate is — because by then the objective is calibration rather than acquisition.
4. **Under-trust is measured as an outcome, not assumed away.** See the scoring below, which is the only part of this design that takes it seriously.

### 6.3 Scoring: why "error-catch rate" is the wrong metric

In the blueprint I wrote that error-catch rate would be a primary assessed outcome, pass or fail. Having thought about it properly, that formulation is wrong, and wrong in a way that would have produced a perverse cohort.

**Error-catch rate alone is trivially gameable.** A candidate who challenges every AI output catches 100% of seeded errors. They also reject every correct recommendation, and if the examination scores only catches, they pass at the top of the cohort. We would have certified, and then released onto wards, the clinician who has learned that the safe answer in an examination is always to disagree with the machine — which is Parasuraman's **disuse**, and which the blueprint's own inverted-U identifies as a real failure mode with real patients behind it.

The correct frame is the one the aviation and psychophysics literature has used for decades: this is a **signal detection** problem, and it has two independent parameters.

- **Sensitivity (discrimination)** — how well the candidate separates erroneous output from sound output. This is the skill.
- **Criterion (bias)** — how readily they say "error" regardless. This is a disposition, and it can be moved without any change in skill at all.

A candidate is characterised by both. High sensitivity with a sensible criterion is discernment. High catch rate achieved by a permissive criterion is not.

<figure class="rr-fig">
<svg viewBox="0 0 1240 720" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Why error-catch rate alone is the wrong metric: three candidates plotted in signal detection space, showing that a high catch rate can be produced either by good discrimination or by a permissive criterion that also rejects sound recommendations">
<rect x="0" y="0" width="1240" height="720" rx="14" fill="#0d1424" stroke="#182742" stroke-width="1"/>
<text x="620.0" y="40" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="19" fill="#c9d6e8" text-anchor="middle" font-weight="bold" letter-spacing="2.5">WHY CATCH RATE ALONE IS GAMEABLE</text>
<text x="620.0" y="63" font-family="Helvetica, Arial, sans-serif" font-size="11.5" fill="#6b82a0" text-anchor="middle">two candidates catch almost the same proportion of seeded errors — only one of them is discerning</text>
<rect x="110.0" y="110.0" width="110.0" height="110.0" fill="#10b981" fill-opacity="0.10" stroke="#10b981" stroke-width="1.2" stroke-dasharray="5 4"/>
<text x="165.0" y="123.8" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11.5" fill="#10b981" text-anchor="middle" font-weight="bold">PASS REGION</text>
<text x="112.8" y="244.8" font-family="Helvetica, Arial, sans-serif" font-size="10.5" fill="#10b981">hit ≥ 0.80  AND  false-alarm ≤ 0.20</text>
<rect x="110" y="110" width="550" height="550" fill="none" stroke="#182742" stroke-width="1.4"/>
<line x1="110.0" y1="660" x2="110.0" y2="666" stroke="#6b82a0" stroke-width="1"/>
<text x="110.0" y="682" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#6b82a0" text-anchor="middle">0.0</text>
<line x1="104" y1="660.0" x2="110" y2="660.0" stroke="#6b82a0" stroke-width="1"/>
<text x="98" y="664.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#6b82a0" text-anchor="end">0.0</text>
<line x1="220.0" y1="660" x2="220.0" y2="666" stroke="#6b82a0" stroke-width="1"/>
<text x="220.0" y="682" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#6b82a0" text-anchor="middle">0.2</text>
<line x1="104" y1="550.0" x2="110" y2="550.0" stroke="#6b82a0" stroke-width="1"/>
<text x="98" y="554.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#6b82a0" text-anchor="end">0.2</text>
<line x1="330.0" y1="660" x2="330.0" y2="666" stroke="#6b82a0" stroke-width="1"/>
<text x="330.0" y="682" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#6b82a0" text-anchor="middle">0.4</text>
<line x1="104" y1="440.0" x2="110" y2="440.0" stroke="#6b82a0" stroke-width="1"/>
<text x="98" y="444.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#6b82a0" text-anchor="end">0.4</text>
<line x1="440.0" y1="660" x2="440.0" y2="666" stroke="#6b82a0" stroke-width="1"/>
<text x="440.0" y="682" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#6b82a0" text-anchor="middle">0.6</text>
<line x1="104" y1="330.0" x2="110" y2="330.0" stroke="#6b82a0" stroke-width="1"/>
<text x="98" y="334.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#6b82a0" text-anchor="end">0.6</text>
<line x1="550.0" y1="660" x2="550.0" y2="666" stroke="#6b82a0" stroke-width="1"/>
<text x="550.0" y="682" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#6b82a0" text-anchor="middle">0.8</text>
<line x1="104" y1="220.0" x2="110" y2="220.0" stroke="#6b82a0" stroke-width="1"/>
<text x="98" y="224.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#6b82a0" text-anchor="end">0.8</text>
<line x1="660.0" y1="660" x2="660.0" y2="666" stroke="#6b82a0" stroke-width="1"/>
<text x="660.0" y="682" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#6b82a0" text-anchor="middle">1.0</text>
<line x1="104" y1="110.0" x2="110" y2="110.0" stroke="#6b82a0" stroke-width="1"/>
<text x="98" y="114.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#6b82a0" text-anchor="end">1.0</text>
<text x="385" y="708" font-family="Helvetica, Arial, sans-serif" font-size="12.5" fill="#c9d6e8" text-anchor="middle">false-alarm rate — sound AI recommendations wrongly challenged</text>
<text x="34" y="385" font-family="Helvetica, Arial, sans-serif" font-size="12.5" fill="#c9d6e8" text-anchor="middle" transform="rotate(-90 34 385)">hit rate — seeded errors correctly caught</text>
<line x1="110.0" y1="660.0" x2="660.0" y2="110.0" stroke="#6b82a0" stroke-width="1.2" stroke-dasharray="4 5"/>
<text x="522.5" y="264.0" font-family="Helvetica, Arial, sans-serif" font-size="10.5" fill="#6b82a0" transform="rotate(-45 522.5 264.0)">chance — no discrimination at all</text>
<polyline points="644.2,110.0 642.7,110.0 641.1,110.0 639.4,110.0 637.5,110.0 635.5,110.0 633.3,110.0 631.1,110.0 628.6,110.0 626.0,110.0 623.3,110.0 620.3,110.0 617.2,110.0 613.9,110.0 610.4,110.0 606.8,110.0 602.9,110.0 598.8,110.0 594.5,110.0 590.1,110.1 585.4,110.1 580.5,110.1 575.4,110.1 570.1,110.1 564.5,110.1 558.8,110.1 552.8,110.1 546.6,110.2 540.3,110.2 533.7,110.2 526.9,110.3 520.0,110.3 512.8,110.4 505.5,110.4 498.0,110.5 490.3,110.5 482.5,110.6 474.5,110.7 466.4,110.8 458.2,110.9 449.9,111.0 441.4,111.2 432.9,111.3 424.3,111.5 415.6,111.7 406.9,111.9 398.2,112.1 389.4,112.4 380.6,112.7 371.8,113.0 363.1,113.4 354.4,113.8 345.7,114.3 337.1,114.8 328.6,115.3 320.1,115.9 311.8,116.6 303.6,117.3 295.5,118.0 287.5,118.9 279.7,119.8 272.0,120.8 264.5,121.9 257.2,123.1 250.0,124.4 243.1,125.8 236.3,127.3 229.7,128.9 223.4,130.6 217.2,132.5 211.2,134.5 205.5,136.7 199.9,138.9 194.6,141.4 189.5,144.0 184.6,146.7 179.9,149.7 175.5,152.8 171.2,156.1 167.1,159.6 163.2,163.2 159.6,167.1 156.1,171.2 152.8,175.5 149.7,179.9 146.7,184.6 144.0,189.5 141.4,194.6 138.9,199.9 136.7,205.5 134.5,211.2 132.5,217.2 130.6,223.4 128.9,229.7 127.3,236.3 125.8,243.1 124.4,250.0 123.1,257.2 121.9,264.5 120.8,272.0 119.8,279.7 118.9,287.5 118.0,295.5 117.3,303.6 116.6,311.8 115.9,320.1 115.3,328.6 114.8,337.1 114.3,345.7 113.8,354.4 113.4,363.1 113.0,371.8 112.7,380.6 112.4,389.4 112.1,398.2 111.9,406.9 111.7,415.6 111.5,424.3 111.3,432.9 111.2,441.4 111.0,449.9 110.9,458.2 110.8,466.4 110.7,474.5 110.6,482.5 110.5,490.3 110.5,498.0 110.4,505.5 110.4,512.8 110.3,520.0 110.3,526.9 110.2,533.7 110.2,540.3 110.2,546.6 110.1,552.8 110.1,558.8 110.1,564.5 110.1,570.1 110.1,575.4 110.1,580.5 110.1,585.4 110.1,590.1 110.0,594.5 110.0,598.8 110.0,602.9 110.0,606.8 110.0,610.4 110.0,613.9 110.0,617.2 110.0,620.3 110.0,623.3 110.0,626.0 110.0,628.6 110.0,631.1 110.0,633.3 110.0,635.5 110.0,637.5 110.0,639.4 110.0,641.1 110.0,642.7 110.0,644.2" fill="none" stroke="#00d4f5" stroke-width="2.4" stroke-opacity="0.85" stroke-dasharray=""/>
<polyline points="658.1,110.1 657.9,110.1 657.6,110.1 657.3,110.1 657.0,110.1 656.6,110.1 656.2,110.1 655.7,110.2 655.2,110.2 654.7,110.2 654.1,110.3 653.4,110.3 652.7,110.4 652.0,110.4 651.1,110.5 650.2,110.5 649.2,110.6 648.1,110.7 646.9,110.8 645.6,110.9 644.2,111.0 642.7,111.2 641.1,111.3 639.4,111.5 637.5,111.7 635.5,111.9 633.3,112.1 631.1,112.4 628.6,112.7 626.0,113.0 623.3,113.4 620.3,113.8 617.2,114.3 613.9,114.8 610.4,115.3 606.8,115.9 602.9,116.6 598.8,117.3 594.5,118.0 590.1,118.9 585.4,119.8 580.5,120.8 575.4,121.9 570.1,123.1 564.5,124.4 558.8,125.8 552.8,127.3 546.6,128.9 540.3,130.6 533.7,132.5 526.9,134.5 520.0,136.7 512.8,138.9 505.5,141.4 498.0,144.0 490.3,146.7 482.5,149.7 474.5,152.8 466.4,156.1 458.2,159.6 449.9,163.2 441.4,167.1 432.9,171.2 424.3,175.5 415.6,179.9 406.9,184.6 398.2,189.5 389.4,194.6 380.6,199.9 371.8,205.5 363.1,211.2 354.4,217.2 345.7,223.4 337.1,229.7 328.6,236.3 320.1,243.1 311.8,250.0 303.6,257.2 295.5,264.5 287.5,272.0 279.7,279.7 272.0,287.5 264.5,295.5 257.2,303.6 250.0,311.8 243.1,320.1 236.3,328.6 229.7,337.1 223.4,345.7 217.2,354.4 211.2,363.1 205.5,371.8 199.9,380.6 194.6,389.4 189.5,398.2 184.6,406.9 179.9,415.6 175.5,424.3 171.2,432.9 167.1,441.4 163.2,449.9 159.6,458.2 156.1,466.4 152.8,474.5 149.7,482.5 146.7,490.3 144.0,498.0 141.4,505.5 138.9,512.8 136.7,520.0 134.5,526.9 132.5,533.7 130.6,540.3 128.9,546.6 127.3,552.8 125.8,558.8 124.4,564.5 123.1,570.1 121.9,575.4 120.8,580.5 119.8,585.4 118.9,590.1 118.0,594.5 117.3,598.8 116.6,602.9 115.9,606.8 115.3,610.4 114.8,613.9 114.3,617.2 113.8,620.3 113.4,623.3 113.0,626.0 112.7,628.6 112.4,631.1 112.1,633.3 111.9,635.5 111.7,637.5 111.5,639.4 111.3,641.1 111.2,642.7 111.0,644.2 110.9,645.6 110.8,646.9 110.7,648.1 110.6,649.2 110.5,650.2 110.5,651.1 110.4,652.0 110.4,652.7 110.3,653.4 110.3,654.1 110.2,654.7 110.2,655.2 110.2,655.7 110.1,656.2 110.1,656.6 110.1,657.0 110.1,657.3 110.1,657.6 110.1,657.9 110.1,658.1" fill="none" stroke="#f59e0b" stroke-width="2.4" stroke-opacity="0.85" stroke-dasharray="6 5"/>
<text x="275.0" y="134.8" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11" fill="#00d4f5">d′ ≈ 2.6  — good discrimination</text>
<text x="412.5" y="275.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11" fill="#f59e0b">d′ ≈ 1.0  — poor discrimination</text>
<circle cx="165.0" cy="165.0" r="11" fill="#0d1424" stroke="#10b981" stroke-width="3"/>
<text x="165.0" y="169.5" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12" fill="#10b981" text-anchor="middle" font-weight="bold">A</text>
<circle cx="407.0" cy="187.0" r="11" fill="#0d1424" stroke="#f87171" stroke-width="3"/>
<text x="407.0" y="191.5" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12" fill="#f87171" text-anchor="middle" font-weight="bold">B</text>
<circle cx="209.0" cy="363.0" r="11" fill="#0d1424" stroke="#f87171" stroke-width="3"/>
<text x="209.0" y="367.5" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12" fill="#f87171" text-anchor="middle" font-weight="bold">C</text>
<line x1="165.0" y1="176.0" x2="407.0" y2="176.0" stroke="#f87171" stroke-width="1.2" stroke-dasharray="3 4" stroke-opacity="0.7"/>
<text x="286.0" y="167.8" font-family="Helvetica, Arial, sans-serif" font-size="10.5" fill="#f87171" text-anchor="middle" font-style="italic">near-identical catch rate</text>
<text x="700" y="112" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12" fill="#6b82a0" letter-spacing="1.5">THREE CANDIDATES, ONE COMPETENCE</text>
<rect x="700" y="144" width="480" height="108" rx="8" fill="#101a2e" stroke="#10b981" stroke-width="1.3" stroke-opacity="0.55"/>
<circle cx="730" cy="178" r="14" fill="#0d1424" stroke="#10b981" stroke-width="2.5"/>
<text x="730" y="183" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="14" fill="#10b981" text-anchor="middle" font-weight="bold">A</text>
<text x="758" y="172" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="13" fill="#c9d6e8" font-weight="bold" letter-spacing="1">DISCERNING</text>
<text x="758" y="192" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#6b82a0">catches 90% of errors,</text>
<text x="758" y="207" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#6b82a0">challenges 10% of sound advice</text>
<text x="758" y="236" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11.5" fill="#10b981" font-weight="bold">PASS</text>
<text x="1160" y="172" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#6b82a0" text-anchor="end">hit 0.90 / fa 0.10</text>
<rect x="700" y="272" width="480" height="108" rx="8" fill="#101a2e" stroke="#f87171" stroke-width="1.3" stroke-opacity="0.55"/>
<circle cx="730" cy="306" r="14" fill="#0d1424" stroke="#f87171" stroke-width="2.5"/>
<text x="730" y="311" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="14" fill="#f87171" text-anchor="middle" font-weight="bold">B</text>
<text x="758" y="300" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="13" fill="#c9d6e8" font-weight="bold" letter-spacing="1">MERELY SUSPICIOUS</text>
<text x="758" y="320" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#6b82a0">catches 86% of errors —</text>
<text x="758" y="335" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#6b82a0">by challenging 54% of sound advice</text>
<text x="758" y="364" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11.5" fill="#f87171" font-weight="bold">FAIL — false-alarm ceiling</text>
<text x="1160" y="300" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#6b82a0" text-anchor="end">hit 0.86 / fa 0.54</text>
<rect x="700" y="400" width="480" height="108" rx="8" fill="#101a2e" stroke="#f87171" stroke-width="1.3" stroke-opacity="0.55"/>
<circle cx="730" cy="434" r="14" fill="#0d1424" stroke="#f87171" stroke-width="2.5"/>
<text x="730" y="439" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="14" fill="#f87171" text-anchor="middle" font-weight="bold">C</text>
<text x="758" y="428" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="13" fill="#c9d6e8" font-weight="bold" letter-spacing="1">MISSING THEM</text>
<text x="758" y="448" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#6b82a0">challenges little,</text>
<text x="758" y="463" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#6b82a0">and catches little</text>
<text x="758" y="492" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11.5" fill="#f87171" font-weight="bold">FAIL — hit floor</text>
<text x="1160" y="428" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#6b82a0" text-anchor="end">hit 0.54 / fa 0.18</text>
<text x="700" y="682" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#6b82a0">Rank these three on catch rate alone and the order is B, A, C.</text>
<text x="700" y="700" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#c9d6e8">Rank them on discrimination and it is A, then C and B together, far behind.</text>
</svg>
<figcaption>Signal detection space. The vertical axis is what the blueprint originally called error-catch rate; the horizontal axis is what it forgot to measure. <strong>Candidates A and B catch almost the same proportion of seeded errors, and they are not remotely the same clinician</strong> — A sits on a curve of good discrimination, B achieves an impressive-looking catch rate by challenging more than half of the sound recommendations as well, which in practice is a clinician who has stopped using the tool. C discriminates no better than B and simply says so less often. Scored on catch rate alone, B would top the cohort. The curves are illustrative of the principle and are not data.</figcaption>
</figure>

**What I would therefore score, per station:**

1. **Detection** — was the seeded error identified? (Hit)
2. **False alarm** — was sound output challenged as erroneous? (False alarm, scored with equal seriousness)
3. **Action** — was the right thing then done? Catching an error and proceeding anyway is a failure, and it is a distinct failure from not catching it.
4. **Reasoning** — is the stated basis for the challenge correct? A candidate who rejects a good recommendation for a bad reason and happens to be right has demonstrated nothing.
5. **Impression integrity** — was an independent impression recorded, specific, and committed, before the output was revealed?

<div class="rr-warn">
<strong>The pass rule is conjunctive and I would not permit compensation.</strong> A candidate must reach the standard on discrimination <em>and</em> keep their false-alarm rate below a set ceiling <em>and</em> act correctly on what they catch. You cannot make up a poor false-alarm rate with an excellent catch rate, because the two together describe a clinician who has stopped using a useful tool. Where the numbers come from is the subject of <a href="/post/2026-08-12-the-angoff-panel-for-testing-clinicians">the Angoff panel</a>: a borderline-candidate definition, a panel, published cut scores, and no arbitrary 50%.
</div>

<div class="rr-note">
<strong>A statistical caveat on the scoring, which matters.</strong> Formal signal-detection indices such as <em>d′</em> assume enough trials to estimate rates stably. Across a realistic examination of ten to twelve stations, per-candidate estimates of sensitivity and criterion will be noisy, and I would not report a candidate's <em>d′</em> to two decimal places as though it were a measurement. At the individual level the practical instrument is the conjunctive rule above — hits, false alarms and actions counted, with thresholds set by panel. The signal-detection framing earns its place at <em>cohort</em> level, where the aggregate does support estimation, and where it will tell us whether we are producing discriminating clinicians or merely suspicious ones. Being clear about which claims the numbers support is itself part of the curriculum.
</div>

### 6.4 The interprofessional station

Commitment eight says interprofessional wherever the work is interprofessional, and the space between a nurse and a consultant is where these failures actually live.

So one station in every assessment cycle is built like this. A confederate playing a senior clinician has already accepted an AI-generated recommendation that contains a seeded error. The candidate — a nurse, a clinical officer, a pharmacist, a junior doctor — has the information needed to detect it. **The assessed behaviour is not detection. It is speaking up.**

The vehicle is [SBAR](/post/2026-08-18-four-letters-from-a-submarine), which exists for exactly this: a structure that lets a junior person deliver an unwelcome assessment to a senior one without having to be brave in the moment. The recommendation clause is where the challenge goes, and having a slot to put it in is most of the battle.

Two design commitments follow, and both cost money:

- **The consultant is assessed too, on the receiving end.** A cohort of nurses trained to challenge, released into a hospital of consultants who have never practised being challenged, is an experiment in professional attrition. Commitment nine — faculty are certified and their teaching is observed — is not separable from this. You cannot examine a reflex you do not have.
- **The mixed-cadre group is not a scheduling convenience.** The Level 1 common core is taught in mixed groups deliberately, and this station is why.

### 6.5 Adversarial rounds

A recurring seminar in which the learner's job is to break the model on a case from their own practice and explain the failure mechanism to the group. Three things this does that simulation does not:

1. It builds a **local catalogue of failure modes** — the ones that occur in Kenyan practice, on Kenyan patients, with the drugs and investigations we actually have. Nobody else will build this for us.
2. It shifts the learner from the receiving end to the adversarial end, which is where the useful intuitions live.
3. It gives us a continuously refreshed **source of new seeded errors** from real practice, which is the only defence I have against the objection in Part 8 that our seeded errors are limited to the failures we can imagine.

The output is a written failure-mode entry, countersigned, which is also the learner's portfolio product under commitment seven.

### 6.6 Where this sits in the programme

| Level | Discernment content | Assessment |
|---|---|---|
| Level 1 common core (12 h, all cadres) | The independent-impression rule; the modalities; one seeded-error simulation | Formative; impression integrity recorded |
| Level 2 | Full seeded-error simulation block; error taxonomy by cadre | Summative AI-OSCE, conjunctive rule |
| Level 3 | Interprofessional challenge station; adversarial rounds begin | Summative, plus countersigned failure-mode entry |
| Level 4 | Supervising others' AI use; assessing a junior's discernment | Workplace-based, multi-source |
| Fellowship | Building the local error bank; running adversarial rounds | Teaching observed and certified |
| Recertification (2 yr) | Re-tested at audit-derived base rate | Summative; unassisted performance also measured |

The one row I would defend hardest is the last. Recertification is where a reflex that has quietly decayed becomes visible, and it is the row most likely to be cut for cost.

---

## Part 7 — Measuring whether it held

The full apparatus is in the [Kirkpatrick companion](/post/2026-08-17-measuring-what-actually-matters), so this is only what is specific to discernment.

**The unassisted-performance audit.** Budzyń and colleagues did something in colonoscopy that we should copy deliberately rather than discover accidentally: they measured the clinician *without* the tool, before and after exposure to it. That is the only design that detects deskilling, and it is not expensive if it is planned. So: a proportion of workplace observations are conducted on cases where AI is not used, and the cohort's unassisted diagnostic performance is tracked over time as a **balancing measure**.

<div class="rr-key">
<strong>And it is pre-declared as publishable whichever way it goes.</strong> If our trained cohorts' unassisted performance is falling, that is a finding about our training and about the tool, and it goes in the annual report. Commitment ten says we measure at Kirkpatrick 3 and 4 or we admit we do not know; this is the specific measurement most likely to embarrass us, which is a reason to register it in advance rather than a reason to omit it.
</div>

**Decay.** The independent-impression rule is my candidate for the fastest-decaying element, because it is a small effortful behaviour with no immediate reward, executed in private, under time pressure. I would measure impression integrity at three and twelve months, expect it to fall, and treat the shape of the fall as the thing that determines where the booster goes. If it does not fall, I was wrong and should say so.

**The behavioural indicator I care most about.** Not the error-catch rate at examination. The rate at which clinicians, in real practice, record an impression that *differs* from the AI's leading suggestion. A cohort in which that rate approaches zero has either achieved perfect agreement with a perfect tool or stopped thinking, and the two are distinguishable only by the case review that follows.

---

## Part 8 — What this does not do

Every security document should have this section and so should every curriculum.

**It rests on a small evidence base at the point where it is most specific.** The direct evidence that AI-literacy training fails to prevent automation bias in physicians is, at present, one randomised trial of 44 people in one city with one model. The rest of my case is convergent evidence from adjacent modalities and from aviation, which is strong for the general phenomenon and silent on the particulars of the intervention I am proposing.

**Transfer is assumed, not demonstrated.** Simulation-based mastery learning transfers for procedural skills — central lines, lumbar punctures, resuscitation. Discernment is not a procedure; it is closer to a habit of mind, and habits of mind are exactly the category where the debiasing literature says transfer fails. My argument is that treating it *as* a procedure, with a structural forcing function, is what moves it into the category where transfer works. That argument is plausible and untested. It is the central bet of the design and it may be wrong.

**Our seeded errors are the errors we can imagine.** This is the objection I find hardest. A bank built by clinicians contains the failures clinicians anticipate; the dangerous model failures are, almost by definition, the ones nobody thought to seed. Adversarial rounds are a partial answer because they harvest real failures from practice, but they will always lag. There is no version of this design that trains against an unknown failure mode, and any claim otherwise would be marketing.

**The curriculum has a half-life.** Specific failure modes are properties of specific model versions. The taxonomy in 6.2 is a snapshot of 2026 and a substantial part of it will be obsolete within two years, either fixed or replaced by something stranger. Only the procedure is durable — impression first, verify, document, act — and even that is a bet on the shape of the tools rather than a law.

**Signal-detection scoring assumes a stable criterion, and we assess rested candidates.** Criterion shifts under fatigue, and fatigue is the condition under which the failure actually occurs. Examining people at ten in the morning in a simulation centre measures the capacity, not the behaviour at three a.m. The workplace-based component exists to close that gap and closes it only partially.

**It may be that interface design does more than education can.** The Qazi authors say as much — provenance cues, uncertainty display, bias-aware interfaces. If a well-designed system produces more discernment than a well-designed curriculum, then a serious institution's job is partly to write procurement standards rather than to teach, and I would want to know that rather than defend my own turf. Commitment two is an educational claim, and educational claims about problems with engineering solutions have a poor history.

**And the whole thing might be unpopular enough to be abandoned.** Buçinca's trade-off is not a footnote. The design deliberately makes work slower and more irritating, and the people subjected to it will rate it accordingly. Institutions delete what scores badly.

### What would refute this

Stated in advance, because a commitment that cannot fail is not a commitment.

1. **The direct test.** Cohorts trained under this design should show a higher error-catch sensitivity at twelve months than cohorts given a conventional twenty-hour AI-literacy course, with no worse a false-alarm rate. If they do not, the design is wrong.
2. **The transfer test.** Impression integrity in workplace observation at twelve months should exceed what an untrained comparator does spontaneously. If the simulation performance is excellent and the ward behaviour is identical to control, I have built an examination rather than a competence.
3. **The deskilling test.** Unassisted diagnostic performance in trained cohorts should not decline relative to baseline. If it declines the way Budzyń's endoscopists' did, the training has not protected the underlying skill and something more than curriculum is required.
4. **The decay test.** If impression integrity is stable at twelve months without boosters, my central hypothesis about decay is wrong, and the recertification interval and the booster schedule should both be relaxed. That would be good news and I would publish it as readily as the bad.

All four are answerable with the evaluation design already specified, and all four should be registered before the first cohort is taught.

---

## What I would write into the founding documents

Compressed, so it fits on one page of an operations manual.

1. **Commitment two is amended to read: scepticism is trained explicitly, built into the workflow structurally, and assessed behaviourally.** The middle clause is not optional and its absence is what the evidence predicts would sink it.
2. **The independent-impression rule is a structural constraint, not an instruction.** The AI output does not unlock until a specific, committed impression is recorded and timestamped. Impressions cannot be edited after the output is revealed.
3. **A hedged impression is scored as absent.** Stated to learners in the first hour.
4. **No less than 40% of seeded errors are errors of omission.** Because training already handles the other kind.
5. **The training error rate is unstable by design and never announced;** the assessment rate is fixed within a cohort, disclosed in the assessment blueprint, and set by the standard-setting panel; the recertification rate is derived from our own audit data.
6. **No candidate is ever assessed on catch rate alone.** Sensitivity, false-alarm rate, action and reasoning are scored separately, the rule is conjunctive, and compensation between them is not permitted. Under-trust is a failure mode with a pass mark attached to it.
7. **Faculty are assessed on the receiving end of challenge** before they are certified to teach the challenging.
8. **Unassisted performance is measured as a balancing outcome and published whichever way it moves.**
9. **Satisfaction data is never permitted as evidence that this element works,** and a fall in satisfaction scores after the forcing function is introduced is pre-declared as an expected finding rather than an adverse one.

---

## Coda

The reason this commitment is nine words long and the post is not is that the nine words conceal a decision most curricula never make.

You can teach a clinician what a language model is in an afternoon, and they will leave knowing more and behaving identically. The Qazi trial is a photograph of that afternoon's consequences: forty-four physicians who could all have defined a hallucination, sitting in front of one, and writing it down.

What has to be built instead is uncomfortable in a specific way. It slows the clinician down. It makes them commit before they are ready. It marks them on the recommendations they wrongly rejected as well as the ones they wrongly accepted. It requires a nurse to contradict a consultant in a room where both are being watched, and it requires the consultant to be examined on how they take it. None of that is popular, and the evidence says plainly that it will be rated worse than the lecture it replaces.

The reflex in the title is resented because it costs something every single time and pays off almost never — until the night it is the only thing standing between a fluent, confident, well-formatted paragraph and a patient. Skills like that do not survive on enthusiasm. They survive because an institution wrote them down, drilled them, examined them, and was willing to fail people who did not have them.

That is what the second clause of commitment two is for. Everything else in this post is an argument about how to make it enforceable.

---

If you want the rest of the design: the [full blueprint](/post/2026-08-05-another-arrow-in-the-quiver) sets out the institution, the five tracks and the five gated levels; [Borrowed From an Art School](/post/2026-08-10-borrowed-from-an-art-school) traces where the competency framework came from; [One Hidden Error](/post/2026-08-11-one-hidden-error) covers the OSCE and the AI-OSCE that this post's stations sit inside; [The Angoff Panel](/post/2026-08-12-the-angoff-panel-for-testing-clinicians) covers where the pass marks in Part 6.3 would come from; [Measuring What Actually Matters](/post/2026-08-17-measuring-what-actually-matters) covers the evaluation apparatus behind Part 7; [Four Letters From a Submarine](/post/2026-08-18-four-letters-from-a-submarine) covers SBAR, which is the vehicle for the interprofessional station; and [The Law Is Part of the Architecture](/post/2026-08-01-the-law-is-part-of-the-architecture) covers the Kenyan legal frame around the simulation data. Other writing is in the [archive](/archive), and things I have built are under [demos](/demos) and [lessons](/lessons).

---

## References

**The trial the argument rests on**

- Qazi, I. A. et al. (2025). [*Automation Bias in Large Language Model–Assisted Diagnostic Reasoning among Physicians Trained in AI Literacy — A Randomized Clinical Trial*](https://ai.nejm.org/doi/full/10.1056/AIoa2501001). *NEJM AI*. Preprint: [medRxiv 2025.08.23.25334280](https://www.medrxiv.org/content/10.1101/2025.08.23.25334280v1). Registered as NCT06963957.

**Automation bias — the foundational work**

- Skitka, L. J., Mosier, K. L. and Burdick, M. (1999). [*Does automation bias decision-making?*](https://www.sciencedirect.com/science/article/abs/pii/S1071581999902525) *International Journal of Human–Computer Studies* 51(5):991–1006. The omission/commission distinction.
- Skitka, L. J., Mosier, K. and Burdick, M. D. (2000). [*Accountability and automation bias*](https://www.sciencedirect.com/science/article/abs/pii/S107158199990349X). *International Journal of Human–Computer Studies* 52(4):701–17.
- Skitka, L. J., Mosier, K. L., Burdick, M. and Rosenblatt, B. (2000). [*Automation Bias and Errors: Are Crews Better Than Individuals?*](https://www.tandfonline.com/doi/abs/10.1207/S15327108IJAP1001_5) *International Journal of Aviation Psychology* 10(1):85–97. Training reduced commission but not omission errors.
- Parasuraman, R. and Riley, V. (1997). [*Humans and Automation: Use, Misuse, Disuse, Abuse*](https://journals.sagepub.com/doi/10.1518/001872097778543886). *Human Factors* 39(2):230–53.
- Lee, J. D. and See, K. A. (2004). [*Trust in Automation: Designing for Appropriate Reliance*](https://journals.sagepub.com/doi/10.1518/hfes.46.1.50_30392). *Human Factors* 46(1):50–80. The origin of calibrated trust.

**Automation bias in clinical settings**

- Goddard, K., Roudsari, A. and Wyatt, J. C. (2012). [*Automation bias: a systematic review of frequency, effect mediators, and mitigators*](https://academic.oup.com/jamia/article-abstract/19/1/121/732254). *JAMIA* 19(1):121–7.
- Lyell, D. and Coiera, E. (2017). [*Automation bias and verification complexity: a systematic review*](https://academic.oup.com/jamia/article/24/2/423/2631492). *JAMIA* 24(2):423–31. Automation bias tracks cognitive load and verification complexity.
- Povyakalo, A. A., Alberdi, E., Strigini, L. and Ayton, P. (2013). [*How to Discriminate between Computer-Aided and Computer-Hindered Decisions: A Case Study in Mammography*](https://journals.sagepub.com/doi/10.1177/0272989X12465490). *Medical Decision Making* 33(1):98–107. The null average concealing help to weak readers and harm to strong ones.
- Dratsch, T. et al. (2023). [*Automation Bias in Mammography: The Impact of Artificial Intelligence BI-RADS Suggestions on Reader Performance*](https://pubs.rsna.org/doi/10.1148/radiol.222176). *Radiology* 307(4):e222176.
- Tschandl, P. et al. (2020). [*Human–computer collaboration for skin cancer recognition*](https://www.nature.com/articles/s41591-020-0942-0). *Nature Medicine* 26:1229–34. Faulty AI misleads the entire spectrum, experts included.
- Gaube, S., Suresh, H., Raue, M. et al. (2021). [*Do as AI say: susceptibility in deployment of clinical decision-aids*](https://www.nature.com/articles/s41746-021-00385-9). *npj Digital Medicine* 4:31.
- Budzyń, K. et al. (2025). [*Endoscopist deskilling risk after exposure to artificial intelligence in colonoscopy: a multicentre, observational study*](https://www.thelancet.com/journals/langas/article/PIIS2468-1253(25)00133-5/abstract). *Lancet Gastroenterology & Hepatology* 10(10):896–903. ADR 28.4% → 22.4% in unassisted procedures.
- Vaccaro, M., Almaatouq, A. and Malone, T. (2024). [*When combinations of humans and AI are useful: a systematic review and meta-analysis*](https://www.nature.com/articles/s41562-024-02024-1). *Nature Human Behaviour* 8:2293–2303.
- Krügel, S., Ostermaier, A. and Uhl, M. (2023). [*ChatGPT's inconsistent moral advice influences users' judgment*](https://www.nature.com/articles/s41598-023-31341-0). *Scientific Reports* 13:4569. Users underestimate how much they are influenced.

**Why instruction alone fails, and what works instead**

- Sherbino, J., Kulasegaram, K., Howey, E. and Norman, G. (2014). [*Ineffectiveness of cognitive forcing strategies to reduce biases in diagnostic reasoning: a controlled trial*](https://www.cambridge.org/core/journals/canadian-journal-of-emergency-medicine/article/ineffectiveness-of-cognitive-forcing-strategies-to-reduce-biases-in-diagnostic-reasoning-a-controlled-trial/B768948819704516DBE325909A8D611E). *CJEM* 16(1):34–40. And the earlier [exploratory study](https://pubmed.ncbi.nlm.nih.gov/21240788/) (2011).
- Buçinca, Z., Malaya, M. B. and Gajos, K. Z. (2021). [*To Trust or to Think: Cognitive Forcing Functions Can Reduce Overreliance on AI in AI-Assisted Decision-Making*](https://dl.acm.org/doi/10.1145/3449287). *Proceedings of the ACM on Human–Computer Interaction* 5(CSCW1), Article 188. [Preprint](https://arxiv.org/abs/2102.09692). Includes the performance/preference trade-off.
- McGaghie, W. C., Issenberg, S. B., Cohen, E. R., Barsuk, J. H. and Wayne, D. B. (2011). [*Does Simulation-Based Medical Education with Deliberate Practice Yield Better Results than Traditional Clinical Education?*](https://pmc.ncbi.nlm.nih.gov/articles/PMC3102783/) *Academic Medicine* 86(6):706–11. Pooled effect size 0.71 (95% CI 0.65–0.76).
- McGaghie, W. C., Issenberg, S. B., Barsuk, J. H. and Wayne, D. B. (2014). [*A critical review of simulation-based mastery learning with translational outcomes*](https://asmepublications.onlinelibrary.wiley.com/doi/10.1111/medu.12391). *Medical Education* 48(4):375–85.

**Kenyan and framework context**

- [OpenAI and Penda Health, *Pioneering an AI clinical copilot*](https://openai.com/index/ai-clinical-copilot-penda-health/); the underlying [real-world study](https://arxiv.org/pdf/2507.16947); and the [critical reading in STAT News](https://www.statnews.com/2025/10/01/penda-health-open-ai-safety-net-study-kenya-artificial-intelligence/).
- Dakan, R. and Feller, J., [AI Fluency Framework](https://aifluencyframework.org/) and the [Practical Summary Document](https://ringling.libguides.com/ai/framework). The Clinical 4Ds are an adaptation; the licence terms are set out in [Borrowed From an Art School](/post/2026-08-10-borrowed-from-an-art-school).
- [WHO, *Ethics and governance of AI for health: guidance on large multi-modal models*](https://www.who.int/publications/b/70584); [AAMC, *Artificial Intelligence Competencies Across the Learning Continuum*](https://www.aamc.org/about-us/medical-education/ai-competencies).

---

<div style="font-size:0.8em; color:#6b82a0; font-style:italic; margin-top:2em;">
In the spirit of the framework's own Diligence competency: this post was drafted with AI assistance. The argument, the design decisions, the amendment to commitment two, the scoring rule and the refutation criteria are mine, and I take full responsibility for the accuracy of its contents. The curves in Figure 2 are illustrative of a principle and are not data.
</div>
