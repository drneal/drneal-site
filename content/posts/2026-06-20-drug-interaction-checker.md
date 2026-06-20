---
title: "Drug Interaction Checker: Screening Polypharmacy with CYP Pharmacology and a Curated Interaction Database"
date: 2026-06-20
category: Clinical AI
tags: pharmacology, drug interactions, polypharmacy, CYP enzymes, patient safety, Flask, clinical decision support, FHIR, RxNorm
level: Intermediate
read_time: 14 min
summary: How the Drug Interaction Checker works — covering the CYP enzyme system, QTc prolongation, serotonin syndrome, the triple whammy, and the engineering decisions behind building a deterministic, explainable interaction screening tool in Python.
featured: false
---

*The app is live at [/drug-checker](/drug-checker). Enter a medication list and press Check. The cardiology preset loads a typical high-risk polypharmacy case.*

---

Adverse drug reactions caused by drug–drug interactions account for approximately 6–7% of all hospital admissions in the UK — a figure that has barely shifted in 20 years despite the BNF, electronic prescribing systems, and a steady stream of published guidance. The tools exist. The gap is at the point of prescribing: checking interactions is slow, manual, and competes with everything else happening in a busy clinical environment.

The Drug Interaction Checker addresses this at the level of workflow friction. Enter a medication list — one drug per line, paste a clinic letter, or feed it the output from the [Voice Clinical Notes](/voice-notes) tool — and every drug pair is screened in under 100 milliseconds. Each flagged interaction is presented with its mechanism, its clinical effect, and a specific management recommendation.

## Why Polypharmacy Is a Solved Problem in Theory and a Crisis in Practice

The pharmacology of drug–drug interactions has been well understood for decades. The CYP450 enzyme system was characterised in the 1970s. QTc prolongation as a mechanism for torsades de pointes was established by the 1990s. The triple whammy (ACE inhibitor + NSAID + diuretic → AKI) was named and described in the early 2000s.

Yet in 2026, a patient on warfarin is still routinely prescribed fluconazole for oral candidiasis without an INR check being arranged. A patient on amiodarone is still started on azithromycin for a community-acquired chest infection. A patient on lithium is still given ibuprofen by their GP for joint pain. These are not failures of knowledge — they are failures of system design. The knowledge is not surfaced at the right moment, in the right format, with the right specificity.

The BNF lists thousands of interactions. Most prescribers cannot hold that information in working memory under time pressure. What they need is not a comprehensive list — it is a rapid, specific alert at the moment of prescribing, with enough context to act on it immediately.

## The Interaction Database

The database underlying this tool contains approximately 90 drug pairs, organised into four severity tiers:

**Contraindicated** — combinations that should never be co-prescribed. The prototypic examples are MAO inhibitors (selegiline, rasagiline, linezolid) combined with serotonergic drugs (SSRIs, SNRIs, tramadol), which cause serotonin syndrome; and PDE5 inhibitors (sildenafil, tadalafil) combined with nitrates (GTN, isosorbide mononitrate), which cause severe, potentially fatal hypotension.

**Major** — combinations where serious harm is likely without active management. Dose adjustment, close monitoring, or substitution with a safer alternative is required. This tier contains the bulk of the database and covers the most clinically consequential interactions.

**Moderate** — combinations where harm is possible but manageable with appropriate monitoring, dose selection, or minor substitution. The clopidogrel + omeprazole interaction (omeprazole inhibits CYP2C19, reducing clopidogrel activation) is the archetypal moderate interaction — simply switching to pantoprazole resolves it.

**Minor** — included for completeness but not the focus of this tool.

Coverage prioritises interactions that kill or cause serious harm in real clinical practice rather than attempting exhaustive theoretical pair enumeration. The clinical justification for each interaction is reviewed against the BNF, MIMS, and primary literature before inclusion.

## The CYP Enzyme System: The Engine Behind Most Drug Interactions

Approximately 90% of phase I hepatic drug metabolism is mediated by the cytochrome P450 family of enzymes. Understanding which enzymes metabolise which drugs, and which drugs inhibit or induce those enzymes, explains the majority of clinically significant pharmacokinetic interactions.

The four enzymes that matter most in polypharmacy:

**CYP2C9** metabolises warfarin (S-enantiomer, the pharmacologically active form), phenytoin, losartan, and several NSAIDs. Inhibitors of CYP2C9 — amiodarone, fluconazole, metronidazole, miconazole, amiodarone — raise warfarin levels and precipitate haemorrhage. Inducers — rifampicin, carbamazepine, St John's Wort — dramatically reduce warfarin effect and increase thrombotic risk.

**CYP3A4** is the most abundant hepatic CYP enzyme and metabolises roughly 50% of commonly prescribed drugs, including statins (simvastatin, atorvastatin), ciclosporin, tacrolimus, many calcium channel blockers, and amiodarone itself. Inhibitors include clarithromycin, erythromycin, itraconazole, fluconazole (at higher doses), and grapefruit. The simvastatin + clarithromycin combination is one of the most reliably dangerous: clarithromycin raises simvastatin acid levels by 8–10× in some patients, making rhabdomyolysis probable with even brief co-prescription.

**CYP2D6** metabolises codeine, tramadol, metoprolol, and several antidepressants. Fluoxetine and paroxetine are potent CYP2D6 inhibitors — co-prescribing them with tramadol not only raises the serotonin syndrome risk inherent in that combination but also alters tramadol's conversion to its active metabolite, producing unpredictable analgesic effect and toxicity.

**CYP1A2** metabolises theophylline, clozapine, and caffeine. Ciprofloxacin and clarithromycin inhibit CYP1A2, raising theophylline levels into the toxic range — the reason theophylline monitoring is mandatory when a quinolone is started in a patient with COPD.

## Serotonin Syndrome: The Most Underdiagnosed Major Interaction Category

Serotonin syndrome results from excess serotonergic activity in the central and peripheral nervous systems, presenting as the triad of mental status changes (agitation, confusion), autonomic instability (tachycardia, hyperthermia, diaphoresis), and neuromuscular abnormalities (clonus, hyperreflexia, rigidity). Severe cases progress to hyperthermia, rhabdomyolysis, seizures, and death.

The interaction categories:

**MAO inhibitors + serotonin reuptake inhibitors.** Classic serotonin syndrome. Selegiline (used in Parkinson's disease) and rasagiline are the MAOIs most commonly encountered in modern prescribing. Linezolid (a glycylcycline antibiotic) has weak but clinically significant MAO-inhibiting activity and is frequently overlooked as a precipitant. The required washout periods are often not observed: ≥14 days after stopping an MAOI before starting an SSRI; ≥5 weeks after stopping fluoxetine (whose active metabolite norfluoxetine has a half-life of 1–2 weeks) before starting an MAOI.

**SSRIs/SNRIs + tramadol.** Tramadol inhibits serotonin and noradrenaline reuptake in addition to its weak μ-opioid agonism. Combined with SSRIs, this produces a clinically significant serotonin syndrome risk. This combination is common in primary care (chronic pain + depression) and is responsible for a substantial proportion of serotonin syndrome cases presenting to emergency departments.

**Triptans + SSRIs.** Technically a moderate interaction — triptans (sumatriptan, rizatriptan, zolmitriptan) are 5-HT1B/1D agonists and combined with SSRIs can produce serotonin syndrome — but the clinical significance in practice is debated. Many patients are on both. The key message is vigilance for symptoms rather than automatic avoidance.

## QTc Prolongation: A Cardiac Channelopathy at the Prescribing Level

Drug-induced QTc prolongation results from blockade of the cardiac delayed rectifier potassium current IKr (encoded by the HERG gene), which is responsible for cardiac repolarisation. When QTc exceeds approximately 500 ms, the risk of torsades de pointes — a polymorphic ventricular tachycardia — rises sharply. Torsades may degenerate into ventricular fibrillation.

The most commonly encountered QTc-prolonging drugs in clinical practice:

- **Antiarrhythmics:** amiodarone, sotalol, flecainide (QRS widening rather than QTc), dronedarone
- **Macrolide antibiotics:** clarithromycin (greatest risk), azithromycin, erythromycin
- **Fluoroquinolones:** ciprofloxacin, levofloxacin, moxifloxacin
- **Antipsychotics:** haloperidol (highest risk), quetiapine, olanzapine, ziprasidone
- **Antiemetics:** ondansetron, domperidone
- **Antifungals:** fluconazole

The critical point for the interaction checker is that **combinations of QTc-prolonging drugs multiply the risk non-linearly**. Amiodarone + azithromycin is not two moderate risks — it is a qualitatively different exposure, because amiodarone also inhibits CYP3A4 (raising azithromycin levels) while both drugs independently block IKr.

A baseline ECG before prescribing any QTc-prolonging drug and regular monitoring of QTc during co-administration is mandatory. The interaction checker flags this as MAJOR rather than MODERATE because the consequences (torsades, VF) are potentially irreversible.

## The Triple Whammy: Drug-Induced AKI That Is Entirely Preventable

The triple whammy is the combination of an ACE inhibitor (or ARB) + NSAID + diuretic, and it is the single most common cause of preventable drug-induced acute kidney injury in primary care.

The mechanism: loop or thiazide diuretics reduce circulating volume. ACE inhibitors reduce the efferent arteriolar tone that compensates for reduced renal perfusion, impairing the kidney's ability to autoregulate glomerular filtration. NSAIDs inhibit prostaglandin synthesis in the afferent arteriole, removing a second compensatory mechanism. When all three are present simultaneously, the kidney loses all three mechanisms for maintaining GFR under conditions of reduced perfusion — and AKI follows, often precipitated by a relatively minor insult such as an intercurrent illness with reduced oral intake.

The interaction checker flags each component pair (ACE inhibitor + NSAID, and ACE inhibitor + furosemide) separately, because the triple combination is the highest-risk scenario and both component interactions are individually significant. The clinical message is: use paracetamol instead of NSAIDs in any patient on both an ACE inhibitor and a diuretic.

## The Opioid + Benzodiazepine Combination: A Population-Level Crisis

Co-prescription of opioids and benzodiazepines has been identified by the FDA, MHRA, and multiple regulatory bodies as a leading contributor to opioid overdose deaths. The mechanism is straightforward — additive CNS and respiratory depression — but the combination remains common in practice, particularly in patients with chronic pain and comorbid anxiety or sleep disorders.

The interaction checker flags all opioid + benzodiazepine pairs as MAJOR, with the specific recommendation that if co-prescription is unavoidable (as it sometimes is in palliative care), naloxone should be accessible, doses should be minimised, and respiratory rate monitored. This is deliberately specific — a generic "use caution" alert is ignored at the prescribing interface. A specific action item is more likely to change behaviour.

## Engineering: Why Rule-Based Rather Than API-Driven

The first design decision was whether to call the RxNorm and OpenFDA APIs at runtime or embed a curated database in the application. The case for API-driven:

- Exhaustive coverage: RxNorm contains 1.1 million drug name strings; OpenFDA drug labelling covers all approved drugs
- Automatically updated as new interactions are identified
- Handles brand names, generic names, and combination products without explicit aliasing

The case for a curated database:

- No latency: the check runs in <1 ms
- No network dependency: works offline and on slow connections
- Deterministic: the same input always produces the same output, auditable by a pharmacist
- Clinically reviewed: every interaction in the database has been reviewed against the BNF and primary literature, not scraped from automated FDA label parsing
- Explainable: the mechanism field is written for a prescriber, not extracted from a dense drug monograph

For a demo and proof-of-concept tool, the curated database is clearly superior. For a production deployment integrated with an EHR, the production path would be:

1. **RxNorm normalisation:** map every free-text drug name to an RxCUI (RxNorm Concept Unique Identifier) via the NLM RxNorm API
2. **OpenFDA interaction lookup:** check drug pairs against the FDA drug interaction database via the OpenFDA REST API
3. **FHIR R4 output:** detected interactions mapped to `DetectedIssue` resources with severity (`high`, `moderate`, `low`), code (`drug-drug`), and a structured reference to both implicated drugs via `MedicationRequest` resources
4. **EHR integration:** `DetectedIssue` resources surfaced at the point of prescribing via a SMART on FHIR application embedded in the EHR interface

## Drug Name Normalisation

Clinicians do not write drug names consistently. "Warfarin 5 mg OD", "Coumadin", "warfarin", and "WARFARIN (INR monitoring required)" are all the same drug. The normalisation pipeline:

1. Convert to lowercase
2. Strip trailing dose and frequency information using regex: `\d+ mg OD` → removed
3. Check against an alias dictionary mapping brand names and alternative spellings to canonical generics (Coumadin → warfarin, Lasix → furosemide, frusemide → furosemide)
4. Exact match against the medication vocabulary from the [NLP Extractor](/nlp-extractor) — 250+ canonical drug names
5. Partial match fallback: if the normalised string is a substring of a known drug name (or vice versa), accept the match

This handles the common cases. It misses: drugs not in the vocabulary, non-English drug names, and highly abbreviated entries. The `drugs_unrecognised` response field surfaces anything that could not be matched, so the user knows which entries were skipped.

## Where This Sits in the Clinical AI Stack

The interaction checker is one component of what a complete clinical decision support system requires at the prescribing interface:

**Input layer:** structured medication list from EHR (FHIR `MedicationRequest` resources) or extracted from free text via the NLP extractor or voice notes formatter.

**Normalisation layer:** RxNorm API maps drug names to RxCUIs; dose and frequency are extracted and structured.

**Screening layer:** all drug pairs checked against the interaction database. This tool.

**Output layer:** FHIR R4 `DetectedIssue` resources, severity-graded, with structured references to the implicated medications and a coded clinical recommendation.

**Integration layer:** SMART on FHIR app surfacing the `DetectedIssue` list at the prescribing screen, within the EHR workflow — not in a separate window that requires the prescriber to leave the prescribing interface.

The demo collapses all of these layers into a single tool that runs in the browser, without EHR integration, to demonstrate the screening logic and the clinical content. The production path extends each layer into its full institutional context.

---

*Try the [Drug Interaction Checker](/drug-checker). The cardiology preset — warfarin + amiodarone + digoxin + furosemide + spironolactone + aspirin + simvastatin + ramipril — generates five major interactions in a single medication list that is not unusual on a cardiology ward round.*
