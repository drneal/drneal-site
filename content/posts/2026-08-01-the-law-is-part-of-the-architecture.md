---
title: "The Law Is Part of the Architecture: Building Medical Software for Kenyan Facilities"
date: 2026-08-01
category: AI & Medicine
tags: medical software, Kenya, Digital Health Act, data protection, ODPC, clinical safety, eMAR, care homes, health informatics, FHIR, regulatory compliance, medical AI
level: All readers
read_time: 22 min
summary: "A third of my care-home specification did not survive one question: under which country's law does this run? Kenya now has a health-specific digital statute, a certification regime for the software itself, and a 72-hour breach clock. This is the work I do — building clinical software for Kenyan care homes and small hospitals that is lawful to deploy, capable of certification, and still standing after contact with the night shift."
featured: false
---

<div style="font-size:0.9em; background:linear-gradient(135deg,#0f3d2e 0%,#14532d 100%); color:#eafff4; padding:1.2em 1.6em; border-radius:8px; margin:1.5em 0; line-height:1.6;">
⚕️ <strong>A service for medical institutions.</strong> I design and build clinical software for Kenyan care homes, retirement homes and small non-surgical hospitals — systems that are legally deployable here, certifiable by the Digital Health Agency, and actually used by the staff they are built for. This post is about what that takes, and why so much health software never survives contact with either the regulator or the night shift.
</div>

I have been writing specifications for a care-home management system — the kind of thing a fifty-bed facility runs on: residents, medications, staff, tasks, inventory, the lot. I wrote what I thought was a thorough one. Roles, subscription tiers, voice input, offline working, an AI assistant, audit trails, hosting, the whole surface.

Then I stopped and asked a question that most people building health software in this country never ask early enough, and often never ask at all.

**Under which country's law does this run?**

A third of the specification did not survive the answer.

Not the features. The features were fine. What did not survive was the architecture underneath them — where the data would live, who could see it, how it would sync, and which of its cleverest capabilities were quietly illegal in Nairobi. Every one of those was a decision I had made without knowing I was making it, because I had absorbed a set of defaults from software built elsewhere.

That is the gap I work in.

## The problem: software that cannot lawfully be used

There is no shortage of health software in East Africa. There is a serious shortage of health software that a licensed facility can lawfully run.

The failure is rarely dramatic. Nobody builds an obviously illegal system. What happens is subtler: a developer builds a competent application using the ordinary tools of the trade — a US or European cloud provider, a managed database in whichever region was fastest, an API call to a foreign model, a convenient repository for backups — and every one of those ordinary choices turns out to carry a Kenyan legal consequence that was invisible at the time it was made.

By the time anyone notices, the consequence is structural. You cannot move where the data lives after you have built three years of workflow on top of it. You cannot retrofit an audit trail that records reads as well as writes. You cannot un-send patient information across a border.

And in the last two years the ground has moved decisively. Kenya now has a health-specific digital statute with regulations in force, a certification regime for the software itself, and an active data protection regulator. The window in which you could build a Kenyan clinical system on generic assumptions has closed.

Meanwhile the second failure — the one that has nothing to do with law — remains exactly what it has always been. Clinical software that is perfectly compliant and perfectly useless, because the people it was built for route around it within a fortnight.

I build against both failures. Here is how.

## The service, in one sentence

**Give me a clinical problem in a Kenyan facility — a care home, a retirement home, a small hospital without theatres or advanced imaging — and I will design and build a system that is lawful to run here, capable of certification, and built around what your staff actually do on a night shift rather than what a specification says they do.**

Everything below is the reasoning behind that sentence.

## Part One: The law is not an afterthought

### Four instruments, not one

Almost every developer I meet who is building health software in Kenya has heard of the Data Protection Act. Rather fewer have read the Health Act. Very few indeed have worked through the Digital Health Act and its 2025 regulations, which is unfortunate, because that is the one that decides whether their product is allowed to exist.

Four instruments govern this work:

| Instrument | What it decides for you |
|---|---|
| **Data Protection Act 2019** (Cap. 411C) and the General Regulations 2021 | Health data as *sensitive personal data*; registration with the Office of the Data Protection Commissioner; mandatory impact assessments; consent; breach notification; cross-border transfer; where a copy of the data must physically sit |
| **Health Act 2017** | Confidentiality of a user's health information, and the narrow conditions under which it may be disclosed |
| **Digital Health Act 2023** and the Digital Health Regulations 2025 | Certification of the software itself; onboarding to the national health information system; exchange standards; restrictions on health data leaving the country |
| **Facility and professional licensing** — KMPDC, the Nursing Council, the Pharmacy and Poisons Board, the Clinical Officers Council | Who your users are, who may lawfully perform which action inside your application, and what an inspector will ask to see |

There is a persistent assumption — I have heard it from good engineers — that building for Kenya is a lighter regulatory lift than building for the United States or Europe. On three specific points it is materially heavier. Those three points are worth spelling out, because each one invalidates an architecture that a competent developer would otherwise reach for by default.

### 1. Your software is itself a regulated product

This is the change in kind, and it is the one I find people have most often missed.

Under the Digital Health Act and its regulations, a healthcare provider or facility is required to use a digital health solution that has been **certified by the Digital Health Agency**. And the application for certification is made by the *solution provider* — by the person who built it. There is a live certification programme covering electronic medical record systems, hospital information systems, pharmacy, laboratory and diagnostic software. A certificate runs for two years and must then be renewed.

Certification is assessed against a published framework. The criteria reported in the regulations include system and data quality, compliance with the reporting and alerting required under prevailing health-sector policy, compliance with the information security, privacy and confidentiality standards set out in the Kenya Health Data Governance Framework, and — this one has teeth — **the capacity to perform health information exchange**.

Sit with what that means for a moment.

It means your software is not a private arrangement between you and your customer. It is a product that a national agency assesses. It means certification is not a launch formality to be handled by someone else after the product is finished — it is a gate that stands in front of your first paying customer. And it means that a great deal of what you might have considered your own design freedom has already been decided for you by a framework document you have not read.

Three practical consequences follow, and they reach right back into the first week of development.

**The certification framework is your requirements specification.** Not an approximation of it — the actual thing. Obtain it before you write code, together with the Kenya Health Data Governance Framework, and treat both as binding input. I would rather discover a mandated reporting field in week one than rebuild a schema around it in month nine.

**Interoperability moves to the front of the queue.** "Capacity to perform information exchange" is not a Phase Three nicety. It means modelling your clinical entities on **FHIR R4** from the first commit — Patient, Practitioner, MedicationRequest, MedicationAdministration, Observation, Condition, AllergyIntolerance, CarePlan, Encounter — and using standard drug terminology rather than free-text drug names. Free text is what most systems store, and it is the reason most systems cannot check an interaction or hand a record to a hospital.

**One product, not many copies.** I had originally sketched a model in which each subscribing facility got its own repository and its own deployment. It is a tempting architecture — clean isolation, simple mental model. It is also finished, on certification grounds alone. If every customer runs a divergent fork, you cannot attest that the fourteenth facility is running the certified artefact. What you need is a single versioned product, one release pipeline, and per-tenant *configuration* rather than per-tenant *code*. Tenants are separated inside the database — by row-level security or by schema — not by giving each of them a different copy of the software.

There is a strategic point buried in this, and it is worth stating plainly because it is not obvious. Certification is a barrier to entry. Barriers to entry cut in both directions. Most vendors chasing this market are building hospital systems; a **certified system built specifically for care homes and small facilities** is a far more defensible position than the same product without the certificate. I would rather budget for that process deliberately than treat it as friction to be minimised.

### 2. The data has to live here — and that constrains the AI

Two provisions bite together.

Section 47 of the Digital Health Act restricts the cross-border transfer of personal health information, with commentary suggesting the exception is drawn narrowly around health tourism. Separately, the Data Protection (General) Regulations 2021 require, for processing in areas of strategic interest — health among them — that at least one serving copy of the data be retained in a **data centre located in Kenya**.

Read them together and plan conservatively. The consequences are severe and immediate:

- The convenient managed platforms have **no Kenyan region**. Neither AWS, nor Azure, nor Google Cloud. The nearest regions are in South Africa, which is still a cross-border transfer.
- Which means the primary copy belongs in a Nairobi facility — carrier-neutral colocation or a local managed provider. That is a bigger operational lift than clicking deploy, it changes your cost base substantially, and it needs to be priced *before* anyone commits to a subscription figure.
- Backups are data. Offshore backups are cross-border transfers.
- Call recordings and their transcripts are health data. So is the audio.

And then the sharp edge, which I did not see until I went looking for it:

**An API call to a foreign language model, carrying patient information, is a cross-border transfer of health data.**

That single sentence constrains the most interesting part of the product. It applies equally to cloud speech-to-text, which is the other capability everybody wants, because dictation is transformative for clinical documentation and nobody wants to type on a ward.

I do not think this kills the AI layer. I think it disciplines it, which is probably no bad thing. There are four routes, in descending order of legal comfort:

1. **De-identify before transmission.** Strip direct identifiers, send only the clinical text the task requires, re-identify locally on return. This works well for summarisation, drafting and structuring. It works less well where the model genuinely needs full context.
2. **Restrict the assistant to tasks that touch no patient data at all** — policy questions, navigating the application, drafting from templates, explaining a procedure to a new member of staff.
3. **Explicit, specific, documented consent** for cross-border processing, supported by an impact assessment that addresses it directly. I regard this as fragile ground in a care home, where a substantial proportion of residents lack the capacity to give it.
4. **Local or on-premises inference** for anything touching patient data. More expensive, less capable, and it removes the question entirely.

My working position for a first release is the first two together, with the boundary **enforced in code rather than maintained by convention**. A rule that depends on a developer remembering it is not a control. It is a hope.

I should add the honest caveat: the interaction between section 47 of the Digital Health Act and the transfer provisions of the Data Protection Act is genuinely unsettled in professional commentary. I am not a lawyer. I read the instruments, I plan for the strict reading, and I tell clients to retain a Kenyan advocate with health and data-protection practice before committing architecture. That is not a disclaimer bolted on at the end — it is a line item in the project plan, and it comes before the first commit.

### 3. Seventy-two hours

Under the Data Protection Act, a personal data breach must be reported to the Office of the Data Protection Commissioner within **72 hours**, with notification to the affected individuals where there is a real risk to their rights and freedoms.

For comparison, the American regime most developers have absorbed by osmosis allows sixty days.

Seventy-two hours is not a policy you can write after launch and file. It is a capability, and it has to be built:

- Centralised, tamper-evident logging that would let you establish what was accessed and by whom, quickly and defensibly
- Anomaly detection that surfaces the event in the first place — you cannot report in 72 hours what you discover in three weeks
- A written, rehearsed incident runbook with named people and a decision tree
- Pre-drafted notification templates for the regulator and for data subjects
- Contractual clarity on who notifies whom, and an internal deadline — realistically 24 hours to the facility — so that they can still meet theirs

An organisation that has never rehearsed this will not achieve it. The clock does not wait for you to work out who is in charge.

### 4. Consent stops being a checkbox and becomes a data structure

The Health Act makes information concerning a user — including their health status, their treatment, and **the fact of their stay in a health facility** — confidential. It may be disclosed on the user's written consent in the prescribed form, on a court order, where another law requires it, or where non-disclosure poses a serious threat to public health.

That last clause about the *fact of a stay* deserves more attention than it usually gets. It means the visitor log is confidential. It means the family portal is confidential. It means that the marketing case study, the demonstration screenshot and the conference slide are all constrained.

The design consequence is that consent cannot be a boolean on the resident record. It has to be a first-class, versioned, auditable entity: what was consented to, on what date, in which prescribed form, witnessed by whom, expiring when, and withdrawn when. And it has to be joined to a model of capacity and substitute decision-making, because in a care home a large fraction of residents cannot give written consent themselves.

There is a practice here that most facilities will recognise, and that most software quietly ignores: the daughter telephones, and whoever answers tells her how her mother is doing. That is a disclosure. It requires a lawful basis. Building a nominated-contacts model tied to recorded consent or documented legal authority is not bureaucratic overhead — it is the difference between a facility that can answer an inspector and one that cannot.

### What actually gets easier

Because the above reads heavily, it is worth being even-handed. Several things about building here are genuinely simpler than the alternatives:

- **One jurisdiction, one regulator.** No fifty-state patchwork, no interaction with a different medical records statute in every territory.
- **Standardised processing agreements** rather than individually negotiated contracts with every vendor in the chain.
- **A defined national exchange standard** to build towards, instead of guessing at a fragmented market.
- **Certification as a moat.** Once held, it is a real and durable advantage.
- **A genuine market gap.** Kenyan care homes and small non-surgical facilities are served almost entirely by software designed for large hospitals, or by paper.

## Part Two: Compliance is the easy half

Everything above is knowable. It is written down, it can be read, and a careful engineer working with a good advocate will get it right.

The harder half is clinical. And here I have an advantage that most people building this software do not, which is that I have spent a working lifetime inside the system it is meant to serve — as a physician and a surgeon, from Kenyatta National Hospital onwards. I know what a medication round looks like at two in the morning when there are two staff on the floor. I know what happens to a form that takes too long to fill in.

### The document nobody specifies

Read a dozen specifications for care-home software and you will find task lists, dashboards, resident profiles and reporting. You will very often not find the **Medication Administration Record**.

This is remarkable, because the MAR is the legally central artefact in a care home. It is the first thing an inspector asks for. It is the document that determines whether an adverse event was a tragedy or a liability. A care-home system without a properly designed eMAR is not a clinical system; it is an address book with colours.

Designing it properly means:

- Order entry with drug, dose, route, frequency, start and stop dates and indication — handling scheduled, PRN, STAT and variable-dose regimes distinctly
- Administration windows, and an explicit definition of what constitutes late as opposed to missed
- Verification at the point of administration, and structured reason codes for missed, refused, held, withheld, self-administered and out-of-stock — because "not given" without a reason is worse than no record at all
- A **controlled substances register** with running balance, dual-witness signature, shift-change count and a discrepancy workflow, meeting the requirements of the Pharmacy and Poisons Board and the narcotics legislation
- Allergy checking and drug–drug interaction checking, high-alert flags, and look-alike/sound-alike warnings
- **Scope-of-practice enforcement** mapped to the actual professional councils — a care assistant must not be able to sign for an injectable, and the system should know that from the registration category, not from a role name someone invented
- Medicines reconciliation on admission and on return from hospital, which is where a large share of real medication errors are generated
- Prescriber identity, verbal-order read-back, and countersigning

That list is not a wish list. It is the minimum for a system that is safe to put in front of a medication trolley.

### The task list has to come from somewhere

The specification I wrote described a caregiver opening a tablet and seeing every resident with coloured markers beside their name: red for urgent, amber for soon, green for later. It is a good interface. I still believe in it.

But when I looked hard at it, I realised I had never said where those markers came from.

Tasks must be *derived*. They come from care plans, from medication schedules, from clinical orders, from assessment review dates. Which means the care plan — individualised, with problems, goals, interventions and review dates, with multidisciplinary input and an overdue-review alert — is not an optional module. It is the engine that drives the only screen anyone looks at.

And the escalation rule set — what turns amber into red, and after how long, and who is paged when a red task is never actioned — is the heart of the product. It deserves to be written down explicitly and tuned against real data, because the failure mode is well known and quietly catastrophic: **if everything is red, nothing is.** Alarm fatigue is not a UX inconvenience. It is a patient safety mechanism failing.

### Assessment and escalation in a facility with no doctor on site

The single greatest clinical contribution software can make in this setting has nothing to do with dashboards. It is early warning.

A care home does not have a physician on the premises at three in the morning. It has a care assistant who may notice that a resident seems "not herself". Structured observation with an automatic early warning score — NEWS2 or equivalent — converts that intuition into a number, and the number into a defined escalation with a named recipient. That is a mechanism that saves lives, and it is cheap to build.

Around it belongs the standard instrument set for this population: falls risk with a post-fall protocol; pressure injury risk with a repositioning schedule and a wound module that records measurements and healing; nutrition screening with weight trends and unintentional-loss alerts; cognition, mood and delirium screening; and a **non-verbal pain instrument**, because a resident with advanced dementia cannot rate their pain out of ten and will otherwise be recorded as having none.

Then incident reporting — falls, medication errors and near-misses, wandering, aggression, injuries of unknown origin, safeguarding allegations, restraint use, deaths — each with a structured form, an investigation workflow, and a countdown to the statutory notification deadline.

And advance directives. Code status must be on a persistent banner at the top of the record, not three taps deep in a tab. That is a design decision with a body count attached to getting it wrong.

### Three things a specification always gets wrong

**Records that can be deleted.** Clinical records are never deleted and never overwritten. A correction is an *amendment*: the original preserved, a new version added, with author, timestamp and stated reason, and the prior version reachable. This has to be enforced at the database layer, because if it is enforced only in application code it will eventually not be enforced at all.

**Unlimited administrator access.** Every specification I have seen, including my own, grants the executive tier unrestricted access to everything. It is a natural thing to write and it is wrong. It breaches the minimum-necessary principle, it is the first finding in any audit, and it is particularly indefensible for developers, who should never hold standing access to live patient data. The correct pattern is role-scoped access for everyone, plus a **break-glass path** — elevated access granted against a stated reason, time-boxed, alerting a second named person, and reviewed afterwards. Development and staging environments run on synthetic data.

**Offline sync treated as a feature.** "It should work offline and sync when the connection returns" is one sentence to write and a project to build. It needs an explicit capability matrix: what may be read offline, and what may be *written* offline. My position is that viewing records and recording observations offline is reasonable; **signing for a medication offline is dangerous**, because two devices can double-sign the same dose. Conflict resolution cannot be last-write-wins — that silently corrupts clinical records. Append-only event logging where possible, and a human review queue where a genuine conflict occurs. Never an automatic merge.

There is a related discovery that only comes from walking the building. Offline is usually framed as an internet problem. In practice it is a *building* problem — thick walls, the basement laundry, the far end of the east wing. That is a different engineering requirement, and no amount of specification writing will surface it. You find it by walking the corridors with a device in your hand.

### Voice: a safety problem wearing a UX costume

I built a [voice dictation tool](/voice-notes) for my own site, and I want that experience inside clinical software, because typing on a ward is a fantasy. But medical dictation carries constraints that general dictation does not:

- **Nothing is ever auto-submitted.** The transcript is presented, editable, and confirmed by a human before anything reaches a record.
- **Numeric fields do not accept free dictation** without structured confirmation. "Fifteen" against "fifty" is a fatal error class, and it is not rare.
- A **custom medical lexicon** is essential. Generic speech recognition mangles drug names, and a mangled drug name in a record is worse than a blank.
- **Language and accent must be tested against the actual staff population** — English, Swahili, and the code-switching that real conversation in a Nairobi facility consists of. Testing dictation with my own voice tells me nothing useful.
- The physical environment is noisy corridors, masks and gloves.
- And dictating clinical detail aloud in a shared lounge is itself a disclosure — which belongs in the user guide, not discovered later.

### Where the AI belongs, and where it does not

This is a business-defining decision rather than a technical one, and it should be made deliberately and early.

If an assistant offers clinical suggestions — diagnosis, treatment, interpretation — you are in the territory of clinical decision support, and in most jurisdictions that raises the question of whether you are building **a regulated medical device** rather than a piece of software. That is a different regulatory pathway, a different cost base and a different company.

My position for a first release is an assistant that is explicitly **non-diagnostic**: it summarises, drafts, searches and answers questions about the facility's own information. It does not create orders. It does not alter clinical records. Anything it produces that reaches a record passes through a clinician's sign-off. Every prompt and response is logged into the audit trail alongside the record it touched.

There is one application I would put near the front of the queue, because the value is enormous and the risk is low: **the shift handover**. A structured SBAR summary composed automatically from the last shift's events, presented to a human to check and amend, is the single most useful thing a language model can do in a care home. It saves the outgoing staff twenty minutes, it gives the incoming staff a better picture than they get today, and it invents nothing that is not already in the record.

Two operational cautions from building these systems. Dictated notes and uploaded documents are **untrusted input** that ends up inside prompts, and should be treated with the suspicion that implies. And model usage is metered and unbounded — quotas, caching, tiering a cheap model for classification against an expensive one for synthesis, and alerting, all need to exist from day one, or the economics of the product quietly invert.

## Part Three: How I work

### The failure that has nothing to do with technology

Clinical software rarely fails on features. It fails on workflow fit, and the failure is quiet.

Staff use the system for the minimum required to avoid being spoken to, and maintain a parallel paper system for the work they actually do. The system is not rejected — it is degraded into a compliance ritual. And the audit trail then records not what happened, but what somebody typed at the end of a shift, which is worse than paper because it carries an authority it has not earned.

There is a simple test for this, and I recommend it to anyone evaluating a system.

**Every care facility has a brain sheet** — the folded paper a caregiver keeps in a pocket with the six things they must not forget. If the software does not replace that sheet, the software has lost. And you cannot design the replacement from a specification. You have to see the sheet, and see what is written on it at three in the afternoon against what is written on it at three in the morning.

### The method

**Step 1 — Decide the law before deciding the architecture.** Jurisdiction, governing instruments, the certification framework, the data protection impact assessment. This is unglamorous and it is where the project is won or lost. It also produces artefacts the facility needs anyway, including its own regulatory registrations.

**Step 2 — Shadow a real facility.** Not a workshop, not an advisory board, not a questionnaire. A full shift, including nights and a weekend, because night shift is skeleton staffing with a different task profile and the highest risk. What people say about their workflow and what they do are systematically different, and the gap between them is where the product lives.

**Step 3 — Photograph every paper form in the building.** The MAR chart, the turning chart, the fluid balance chart, the handover sheet, the incident form, the fridge temperature log. Those forms are the requirements specification, written by people who have already solved the problem imperfectly. Nothing is guessed.

**Step 4 — Take the baselines.** Time the medication round on paper. Count outstanding tasks per resident per shift. Map the wifi dead zones. If the digital round is slower than the paper round, staff will batch-sign, and you will have built a machine that manufactures falsified records. That number governs the design.

**Step 5 — Build in phases, smallest safe thing first.** Authentication and role model, resident registry, admissions and bed management, care plans, the task board with a defined escalation rule set, the eMAR, clinical notes with voice, observations with early-warning escalation, incident reporting, advance directives, audit trail. Online only, on synthetic data, piloted before it is sold. Staff records, rostering, pharmacy inventory, family communication and reporting follow. Kitchen and diet orders, telephony, the AI assistant, billing and exchange come after that.

**Step 6 — Measure adoption honestly.** Not satisfaction surveys. Medication round duration against the paper baseline. The proportion of tasks signed within the administration window against those batched at shift end. The rate of double documentation. And unprompted use in week six, after I have stopped visiting. That last measure is the only one that matters. If usage decays the moment I am not in the building, it is a demonstration, not a product.

### Two failure modes I watch for in myself

**Building for the buyer rather than the user.** The owner or matron signs for the software and wants dashboards, audit reports and compliance evidence. The care assistant wants three fewer taps. Build for the buyer and the users route around it, the data quality collapses, and the dashboards the buyer paid for become fiction. The caregiver's task board is the product; executive reporting is a byproduct of caregivers using it willingly.

**My own clinical training as a distortion.** I am a physician. The primary user of this software is not. She is a care assistant with a fraction of my training, doing physically demanding work, for whom entering an observation is an interruption rather than a natural act of documentation. Physician mental models of the record — problem lists, differentials, structured notes — do not transfer to that user. Watching someone with no clinical education attempt an interface tells me more than any amount of my own review.

## Why this matters for institutions

- **The system can be lawfully deployed.** Certification, localisation, consent and breach obligations are designed in from the first week rather than discovered in an audit.
- **The compliance burden moves in your favour.** Registration, impact assessment and inspection-ready records become part of the software rather than a separate annual scramble.
- **The clinical core is built by someone who has worked in it.** eMAR, early-warning escalation, incident reporting and advance directives designed by a clinician, not inferred from a competitor's screenshots.
- **It survives contact with the night shift.** Because the design starts on the floor of a real facility, not in a specification document.
- **Nothing is guessed.** The forms, the timings, the connectivity, the escalation thresholds — all measured in the building where the software will run.

<div style="font-size:0.9em; background:#1e1a0e; border-left:4px solid #f59e0b; padding:0.9em 1.3em; margin:1.4em 0; border-radius:0 4px 4px 0;">
⚕️ <strong>A note on scope and responsibility.</strong> I am a physician and an engineer, not an advocate. Every project of this kind includes retaining a Kenyan lawyer with health-sector and data-protection practice, and the regulatory positions in this article should be confirmed against the instruments as they stand on the day you build — the Digital Health regulations are actively developing. Systems I build are designed as clinical record and workflow tools. They are not medical devices, and they do not provide diagnosis or treatment recommendations. Where a project would cross that line, the regulatory pathway is assessed before any code is written, not after.
</div>

## If you are running a facility, or building for one

If you run a care home, a retirement home or a small non-surgical hospital and you are still working on paper — or on software that your staff have quietly stopped using — that is exactly the problem I work on. And if you are already carrying a system and are not certain whether it is lawful to run under the current regime, that is worth an hour of somebody's attention before it is worth a year of somebody's remediation.

Send me the shape of the problem: how many beds, what you are running now, and what breaks most often. I will tell you honestly whether software is the answer.

The law is not an obstacle you clear on the way to building the product. It is part of the architecture, and it is cheaper to pour it with the foundations than to inject it into a finished building.

*— Neal*

## References

- [Digital Health Act, 2023 (No. 15 of 2023)](https://new.kenyalaw.org/akn/ke/act/2023/15/eng@2023-11-24)
- [Digital Health (Health Information Management Procedures) Regulations, 2025 (LN 76 of 2025)](https://new.kenyalaw.org/akn/ke/act/ln/2025/76/eng@2025-04-11)
- [Digital Health (Data Exchange Component) Regulations, 2025 (LN 77 of 2025)](https://new.kenyalaw.org/akn/ke/act/ln/2025/77/eng@2025-04-11)
- [Digital Health Agency — Certification Programme](https://certification.dha.go.ke/)
- [Health Act, 2017 (No. 21 of 2017)](https://new.kenyalaw.org/akn/ke/act/2017/21/eng@2022-12-31)
- [Office of the Data Protection Commissioner](https://www.odpc.go.ke/faqs/)
- [Kenya Medical Practitioners and Dentists Council — health facility registration](https://kmpdc.go.ke/registration-of-a-health-facility/)
- [Clyde &amp; Co, "Health data protection in Kenya: strategic compliance" (2026)](https://www.clydeco.com/en/insights/2026/03/health-data-protection-in-kenya-strategic-complian)
- [CIPESA, "Does Kenya's Digital Health Act Mark A New Era for Data Governance and Regulation?"](https://cipesa.org/2024/05/does-kenyas-digital-health-act-mark-a-new-era-for-data-governance-and-regulation/)
