---
title: "Inside the Clinical Text NLP Extractor: Entity Recognition, Rule-Based Pipelines, and the Path to Production BioBERT"
date: 2026-06-20
category: Clinical NLP
tags: clinical NLP, natural language processing, NER, BioBERT, FHIR, spaCy, Python, medical AI, information extraction, SNOMED CT
level: Intermediate
read_time: 14 min
summary: A detailed walkthrough of the Clinical Text NLP Extractor live demo — how the rule-based entity extraction pipeline works, what each entity type captures, where the code lives, and how this maps to the fine-tuned BioBERT system used in production clinical informatics work.
featured: false
---

*The live demo is at [/nlp-extractor](/nlp-extractor). Paste any clinical note and see entities extracted and highlighted in under 50 ms.*

---

Clinical notes are one of the richest — and most difficult — data sources in medicine. A single discharge summary contains more structured clinical information than a dozen database fields: the patient's diagnoses, their medication list with dosages and frequencies, the vital signs on admission, abnormal lab values, and a timeline of clinical events expressed in natural language. The challenge is getting that information out in a form a system can act on.

The [Clinical Text NLP Extractor](/nlp-extractor) is a live demo of an information extraction pipeline for unstructured clinical text. It identifies six entity types simultaneously, highlights them in the source note with distinct colours, and outputs a structured table with confidence scores. This post explains exactly how it works, what it demonstrates about my broader clinical informatics practice, and where every line of the relevant code lives.

## What Skills This Is Demonstrating

Before the technical details, it is worth being explicit about what this demo is designed to show:

**Clinical domain knowledge as a prerequisite for NLP.** Building a medical NLP system that works requires understanding the clinical content — what the abbreviations mean, how dosages are expressed in different specialties, which diagnosis terms are synonymous. The 300+ condition vocabulary and 250+ drug list in this demo are not copied from a generic database; they reflect years of working with clinical data in real healthcare settings.

**Information extraction pipeline design.** The extractor follows the standard NLP pipeline: tokenisation, pattern matching, entity boundary detection, conflict resolution (no overlapping spans), and structured output. Each component has a specific responsibility and is independently testable.

**Robust regex engineering.** Clinical text is messy — inconsistent formatting, non-standard abbreviations, free-text descriptions mixed with structured data. The date patterns handle eight different date formats; the dosage patterns capture `mg`, `mcg`, `µg`, `mL`, `IU`, and frequency abbreviations like `BD`, `TDS`, `PRN`, `nocte`. Writing regex that is simultaneously specific enough to avoid false positives and general enough to capture real clinical variation is a non-trivial engineering task.

**Graceful degradation.** The demo makes no external calls and has no dependencies beyond the Python standard library and Flask. It runs correctly whether or not internet access is available, whether or not a GPU is present, and whether or not any ML models are installed. This is a deliberate engineering choice: production NLP systems need fallback behaviour.

---

## The Six Entity Types

### MEDICATION

Medications are matched against a curated vocabulary of 250+ drugs covering all major therapeutic areas: cardiovascular agents, antibiotics, analgesics and anti-inflammatories, psychiatric and neurological drugs, respiratory inhalers, diabetes medications, gastrointestinal agents, thyroid and endocrine drugs, rheumatology biologics, and haematological agents. The list is sorted by descending name length before matching, so longer names like `piperacillin-tazobactam` are found before the shorter substring `piperacillin`. Word-boundary anchors (`\b`) prevent partial-word false matches.

The vocabulary is defined in `_NLP_MEDICATIONS` in [`app.py`](https://github.com/drneal/drneal-site/blob/main/app.py), beginning at the `# Clinical Text NLP Extractor` section.

### DIAGNOSIS

The diagnosis vocabulary covers 300+ conditions across all major specialty areas: cardiovascular, respiratory, metabolic, renal, gastrointestinal, musculoskeletal, neurological, psychiatric, infectious disease, and oncology. Both full terms and widely used abbreviations are included — `atrial fibrillation` and `AF`, `myocardial infarction` and `NSTEMI`, `COPD` and `chronic obstructive pulmonary disease` — so the extractor works on both fully-spelled prose and abbreviation-heavy clinical shorthand.

Defined in `_NLP_DIAGNOSES` in [`app.py`](https://github.com/drneal/drneal-site/blob/main/app.py).

### DOSAGE

Dosages are captured by a set of regex patterns covering numeric quantities with units (`10 mg`, `18 mcg`, `500 mL`, `5000 IU`), percentage concentrations followed by a preparation type (`0.5% cream`), frequency abbreviations (`OD`, `BD`, `TDS`, `PRN`, `nocte`, `stat`), verbal frequencies (`twice daily`, `three times a day`), and quantity phrases (`2 tablets`, `3 puffs`). The pattern also catches `loading dose`, `maintenance dose`, and `starting dose` phrases that contextualise the numeric value.

### DATE

The date extractor handles eight formats including DD/MM/YYYY, named-month formats (`15th June 2026`, `March 2024`), ISO 8601 (`2026-06-20`), relative references (`yesterday`, `3 weeks ago`, `last Monday`), and contextual phrases (`since January 2025`). In clinical notes, relative dates are as clinically significant as absolute ones — "admitted 3 days ago" requires a different processing path than "admitted 12/06/2026", but both need to be flagged.

### LAB VALUE

Lab values follow the pattern `[name] [optional colon] [numeric value] [optional unit]`. The extractor covers 20+ common laboratory parameters: full blood count (Hb, WBC, PLT, Hct), renal function (Cr, eGFR, urea), liver function (ALT, AST, ALP, GGT, bilirubin), metabolic panel (Na, K, Ca, glucose, HbA1c), coagulation (INR, APTT), inflammatory markers (CRP, ESR, procalcitonin), cardiac biomarkers (troponin, BNP, NT-proBNP), and lipids (cholesterol, LDL, HDL, triglycerides).

### VITAL SIGN

Vital signs patterns cover the standard observations set: blood pressure (systolic/diastolic format `BP 158/94`), heart rate (`HR 88 bpm`), oxygen saturation (`SpO2 96%`, `O2 sat 96%`), temperature (`Temp 37.2°C`), respiratory rate (`RR 18`), Glasgow Coma Scale (`GCS 15/15`), BMI, weight, and height. The patterns are written to accept both abbreviated and full-word variants and to tolerate optional colons and spaces between the label and the value.

---

## A Sample Extraction

Here is a short clinical note and the entities the extractor identifies:

```
65-year-old male, admitted 12/06/2026 with decompensated heart failure.
Medications: amlodipine 10 mg OD, ramipril 5 mg OD, metformin 500 mg BD.
Observations: BP 162/98, HR 88 bpm, SpO2 94%.
Investigations: HbA1c 8.4%, Cr 118 µmol/L, NT-proBNP 2840.
```

| Entity text | Type | Confidence |
|---|---|---|
| 12/06/2026 | DATE | 95% |
| heart failure | DIAGNOSIS | 88% |
| amlodipine | MEDICATION | 90% |
| 10 mg | DOSAGE | 92% |
| OD | DOSAGE | 92% |
| ramipril | MEDICATION | 90% |
| 5 mg | DOSAGE | 92% |
| metformin | MEDICATION | 90% |
| 500 mg | DOSAGE | 92% |
| BD | DOSAGE | 92% |
| BP 162/98 | VITAL_SIGN | 96% |
| HR 88 bpm | VITAL_SIGN | 96% |
| SpO2 94% | VITAL_SIGN | 96% |
| HbA1c 8.4% | LAB_VALUE | 94% |
| Cr 118 µmol/L | LAB_VALUE | 94% |
| NT-proBNP 2840 | LAB_VALUE | 94% |

16 entities extracted from a 4-line note in under 20 ms.

---

## How the Pipeline Handles Conflicts

The most important engineering constraint in any NER system is that entity spans must not overlap. The extractor maintains a `seen_spans` list of `(start, end)` tuples and checks every candidate span against it before committing:

```python
def no_overlap(s: int, e: int) -> bool:
    return all(e <= a or s >= b for a, b in seen_spans)
```

The extraction order matters: dates, dosages, vital signs, and lab values are matched first (with higher specificity patterns), then medications, then diagnoses. This means a phrase like `metformin 500 mg BD` correctly yields three separate entities (`metformin` as MEDICATION, `500 mg` as DOSAGE, `BD` as DOSAGE) rather than having the dosage absorbed into a diagnosis match.

The full extraction function is `_run_nlp_extractor()` in [`app.py`](https://github.com/drneal/drneal-site/blob/main/app.py), in the `# Clinical Text NLP Extractor` section. The Flask routes are immediately below:

- `GET /nlp-extractor` — renders the HTML page with three preloaded clinical note presets
- `POST /nlp-extractor/run` — accepts `{"text": "..."}` JSON, returns `{"ok": true, "entities": [...], "counts": {...}, "total": N}`

The interactive frontend — text area, preset buttons, real-time highlighting, entity table — is in [`templates/nlp_extractor.html`](https://github.com/drneal/drneal-site/blob/main/templates/nlp_extractor.html).

---

## Rule-Based Pipelines vs. ML: When to Use Which

A common question in clinical NLP is whether to use rule-based systems or learned models. The honest answer is: both, at different stages.

Rule-based systems like this demo have several genuine advantages. They are fully deterministic — the same input always produces the same output, which matters enormously in a regulated clinical environment. They are interpretable — you can inspect exactly why a span was or was not extracted. They are fast, requiring no GPU or inference overhead. And they handle highly structured sub-domains (dosages, vital signs, lab values) better than most general-purpose models because the patterns are explicit and exhaustive.

The limitation is generalisation. A vocabulary matcher will miss drug names not on its list, diagnoses expressed in unusual phrasings, and entities in unfamiliar abbreviation systems. It has no understanding of clinical context — it will extract `aspirin` from a sentence saying the patient is allergic to aspirin and currently not taking it.

This is why the production system uses a fine-tuned [BioBERT](https://en.wikipedia.org/wiki/BERT_(language_model)) model. BioBERT is a version of BERT pre-trained on PubMed abstracts and PubMed Central full-text articles, giving it a domain-specific language model that understands clinical terminology far better than a general BERT model. Fine-tuned on annotated clinical notes with NER labels, it achieves substantially higher recall on rare drug names, multi-word diagnoses, and contextually modified entities. The vocabulary matcher in this demo is effectively what the training signal supervision replaces.

---

## From Extraction to FHIR R4

Entity extraction is the first step in a clinical NLP pipeline. What happens next depends on the use case, but in my production work the pipeline continues through:

**SNOMED CT normalisation.** Raw text strings like `heart failure` are mapped to their canonical SNOMED CT concept identifiers (e.g., `84114007` — Heart failure). This is non-trivial because the same condition may be described as `cardiac failure`, `CCF`, `congestive heart failure`, or `LVF` depending on the clinician and specialty. A normalisation layer built on approximate string matching against the SNOMED CT release maps these variants to a single canonical concept.

**FHIR R4 resource generation.** Extracted and normalised entities are serialised as [FHIR R4](https://en.wikipedia.org/wiki/Fast_Healthcare_Interoperability_Resources) resources: medications become `MedicationStatement` resources, diagnoses become `Condition` resources, lab values become `Observation` resources. This structured output is what downstream systems — clinical data warehouses, population health platforms, decision support tools — can ingest and query.

**De-identification.** Before any of the above runs in a real clinical context, the text is de-identified: patient names, dates of birth, NHS/hospital numbers, and other direct identifiers are removed or pseudonymised. The demo skips this step because it runs on synthetic text only.

This is what distinguishes a demo pipeline from a production system: not the entity extraction accuracy (which is easier to improve than people expect), but the infrastructure around normalisation, standardisation, provenance tracking, and governance that makes the output trustworthy and auditable.

---

## What This Demo Leaves Out (Deliberately)

The demo does not run a machine learning model, does not connect to any database, does not de-identify text, and does not output FHIR. It is a transparent, inspectable demonstration of the entity extraction logic that sits at the centre of the production pipeline. The goal is to show that the underlying NLP competency is real and auditable — not to ship a production system in a browser demo.

If you work in clinical informatics and want to discuss pipeline design, model fine-tuning on your specific corpus, or FHIR integration architecture, [get in touch](/about#contact).

---

## Where to Find the Code

Everything in the demo is in two files in the repository.

The NLP engine — all entity vocabularies, regex patterns, and the `_run_nlp_extractor()` function — is in [`app.py`](https://github.com/drneal/drneal-site/blob/main/app.py), starting at the comment `# Clinical Text NLP Extractor`. The function takes a plain string and returns a dictionary with entity spans, type counts, and totals. It has no side effects and no external dependencies beyond the Python standard library's `re` module.

The interactive frontend — three clinical note presets, the colour-coded highlighted output, the entity count chips, and the structured table with confidence bars — is in [`templates/nlp_extractor.html`](https://github.com/drneal/drneal-site/blob/main/templates/nlp_extractor.html). All JavaScript is inline at the bottom of the file.

---

*Try the [NLP Extractor live](/nlp-extractor). Load the cardiology, respiratory, or oncology preset and observe how the extraction adapts across different clinical contexts and vocabulary sets.*
