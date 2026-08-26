---
title: "Not Shown Is Not Locked: The Patient Record I Am Building"
date: 2026-08-25
category: AI & Medicine
tags: electronic health records, MedLattice, post-quantum cryptography, ML-KEM, ML-DSA, SLH-DSA, encryption, distributed ledger, blockchain, Ethereum, smart contracts, FHIR, patient consent, break-glass, Caldicott, minimum necessary, GDPR, HIPAA, 42 CFR Part 2, EHDS, Kenya, Digital Health Act, data protection, health informatics, clinical software, quantum computing
level: All readers — no technical background assumed
read_time: 26 min
summary: "In almost every hospital system in the world, 'the receptionist cannot see your diagnosis' means the software declines to draw it on her screen. The diagnosis is sitting in the same database, behind the same login, protected by a rule rather than a lock. A misconfiguration, an injection flaw or a disgruntled administrator turns 'cannot' into 'can'. MedLattice is the electronic patient record I have been building on the opposite premise: that every part of a record should be separately locked, that people should be handed only the keys they actually need, and that the encryption should be chosen for the length of a human life rather than the length of a procurement cycle. This is the whole design in plain English — the drawers and the envelopes, the key tree that makes fine-grained sharing cryptographic instead of cosmetic, the shared logbook that no single hospital can quietly edit, what the patient controls, what happens at three in the morning when there is no time for any of it, how a record gets erased when the logbook cannot forget, and — at length, because every security document should have one — what this does not do."
featured: false
---

<div style="font-size:0.85em; background:#111827; border-left:4px solid #6b82a0; padding:0.9em 1.3em; border-radius:0 6px 6px 0; margin:1.5em 0; color:#9fb3cc;">
<em>I write here in a personal capacity. This post is a plain-English account of a system I am designing and building; it is not clinical guidance, not legal advice, and not a product announcement. The technical specification behind it exists and is complete, and it is linked in full at the end.</em>
</div>

<style>
.ml-key { font-size: 0.95em; background: #101a2e; border-left: 4px solid #00d4f5; padding: 0.9em 1.3em; margin: 1.4em 0; border-radius: 0 4px 4px 0; }
.ml-story { font-size: 0.93em; background: #1d1408; border-left: 4px solid #f0a836; padding: 0.9em 1.3em; margin: 1.4em 0; border-radius: 0 4px 4px 0; }
.ml-honest { font-size: 0.93em; background: #1a0f14; border-left: 4px solid #f87171; padding: 0.9em 1.3em; margin: 1.4em 0; border-radius: 0 4px 4px 0; }
.ml-good { font-size: 0.93em; background: #0e1e1a; border-left: 4px solid #10b981; padding: 0.9em 1.3em; margin: 1.4em 0; border-radius: 0 4px 4px 0; }
.ml-fig { background: #0c1420; border: 1px solid #1f2b3d; border-radius: 8px; padding: 1.2em 1em 0.6em; margin: 1.8em 0; text-align: center; }
.ml-fig figcaption { font-size: 0.82em; color: #8ba0b8; text-align: left; padding: 0.8em 0.6em 0.4em; line-height: 1.55; }
</style>

There is a sentence in every hospital's information-governance policy that is not true in the way people think it is.

It says something like: *the receptionist cannot see your diagnosis.*

What that sentence actually describes, in almost every system I have ever looked at, is a rule. Your diagnosis and your name are sitting in the same database. The receptionist has a valid login to that database. When she opens your record, a piece of software consults a permissions table, decides she is not entitled to the diagnosis field, and declines to draw it on the screen.

The diagnosis was never locked. It was merely not shown.

Most of the time that distinction does not matter, because most of the time the software works. It matters on the day the software does not work — a misconfigured interface, an injection flaw, a badly scoped export, a reporting tool that bypasses the application layer, a database administrator who is angry about something. Every one of those turns *cannot see* into *can see*, instantly and completely, and there is no second line of defence, because there was only ever the one.

That gap is the thing I have been building against. This post is the whole design, in plain English, with no mathematics in it.

## What I am building, in one page

MedLattice is an electronic patient record built on a simple inversion: **lock every piece of the record separately, and hand out only the keys a person actually needs.**

A patient's record is divided into about twenty *drawers* — basic details, medications, test results, mental health, genetics, and so on. Each drawer has its own lock. Inside a drawer, each individual fact sits in its own sealed envelope with its own lock. When a receptionist looks somebody up, she is handed the keys to the name, the date of birth and the appointment — and nothing else.

Here is the part that matters. If somebody stole the entire filing cabinet and handed it to her — every scrambled envelope in it — she still could not open the diagnosis. Not because a policy forbids it. Because she was never given a key that opens it, and there is no way to make one from the keys she holds.

Alongside this sits a **shared logbook** that every participating hospital keeps a copy of. It records who was given which keys, when, and for what stated reason. Because everybody holds a copy, no single hospital can quietly edit it afterwards. The logbook contains no medical information at all — only the record of who looked at what, and who was refused.

And the locks themselves are built to survive quantum computers, which is a sentence that needs a paragraph of its own later, because the reason is not the one people usually assume.

<div class="ml-key">
<strong>The four things that make this different from a conventional record system</strong>

<strong>1. The locks are real.</strong> "The clerk cannot see the diagnosis" does not mean the screen hides it. It means she has no key that opens it.

<strong>2. Being senior is not a licence.</strong> A consultant has no right to your record unless a consultant is actually treating you. The system checks for a real clinical relationship, not a job title.

<strong>3. The logbook cannot be quietly edited.</strong> Every hospital holds a copy. Every look — and every refused look — is written down.

<strong>4. It is built for the next fifty years, not the next five.</strong> The encryption is chosen for the length of a human life, because that is how long a medical record has to stay private.
</div>

The rest of this post is the reasoning behind those four sentences.

## Three problems I am building against

### Problem one: the colleague who looks you up

The single most common privacy failure in health systems is not a hacker. It is a member of staff with a completely legitimate login looking up somebody they should not: a neighbour, an ex-partner, a colleague, a local celebrity, the person their daughter is seeing.

They have a valid account. They have a valid role. Every check the system knows how to perform, they pass. It has no reason to stop them, and in most systems it does not — it records the access in a log that nobody reads until there is already a complaint.

MedLattice asks a second question. Not just *are you a nurse?* but *are you this patient's nurse, right now?*

Access for the purpose of treatment requires a live care relationship, created by an actual appointment or admission and expiring when it ends. Without one, seniority makes no difference whatsoever. The most senior consultant in the hospital is refused exactly as firmly as a first-week student, and the refusal is written into the shared logbook where the Caldicott Guardian can see it.

I want to be precise about why this is the first problem rather than the third. Encryption is the part of this work that is intellectually interesting, and it is the part that gets written about. But if you ranked actual harms to actual patients by frequency, inappropriate access by credentialled insiders would sit far above cryptanalysis, and it will still be sitting there in 2050. A design that solves the interesting problem and not the common one has failed at the thing it was for.

### Problem two: the database that walks out of the door

When a hospital database is stolen — and they are stolen, regularly, everywhere — the reason it is catastrophic is that it is one container. Get into it and you have everything. Every patient, every note, every result, every image.

MedLattice has no such container. Each patient's record is split into separately locked drawers, and each fact inside a drawer is separately locked again. Somebody who takes the whole storage system gets an enormous quantity of scrambled data and no keys at all, because the keys are not kept with the data. They live in dedicated tamper-resistant hardware that will not release one without an authorisation recorded in the shared logbook.

This changes the shape of a breach in a way I think is underappreciated. In a conventional system, "the database was exfiltrated" and "the records were disclosed" are the same event. Here they are two events, and the second one requires a separate and much harder compromise. That is not a guarantee — nothing is — but it is the difference between one failure and two.

### Problem three: steal it now, read it in 2040

Encryption is a race between the lock and the tools available to pick it. Quantum computers are a genuinely new kind of tool, and when they are large enough they will break most of the encryption in use today. Nobody knows exactly when. Estimates cluster somewhere between 2030 and 2040, and the people making them disagree with each other in public.

The date is not really the point, and the argument about the date is a distraction.

The point is that an attacker does not have to wait in order to *steal* the data. They can copy encrypted records today, store them, and open them when the tools catch up. For a credit card number this hardly matters, because the card expires long before the tools arrive. For a genetic test result it matters enormously, because it never expires — and it is not only about the patient. A genome implicates siblings, children and grandchildren who never consented to anything.

So the question I ask is not *when will quantum computers arrive?* It is: *how long does this record need to stay private, and does that period stretch past the arrival date?*

For a medical record, the answer is obviously yes, by decades. Kenya's Digital Health Act 2023 alone requires health records to be kept for twenty years, and that is a floor, not a lifetime. A record created for a child today has to hold its secrecy into the 2090s.

Which is why MedLattice uses quantum-resistant encryption for every record from the very first one, rather than adopting it later when the threat feels closer. There is no upgrade path for a file that has already been copied. You cannot retrospectively re-encrypt something that is sitting on somebody else's disk.

## How the record is put together

### Drawers

A patient's record in MedLattice is not one document. It is divided into about twenty categories, each separately locked:

Basic details · Insurance and billing · Observations and vital signs · Allergies · Medications · Diagnoses · Procedures · Routine laboratory results · Specialist laboratory results · Imaging details · Scan images · Pathology · Clinical notes · Genetics · Mental health · Sexual and reproductive health · Substance use · Social circumstances · Advance decisions · Anonymised data for research

Splitting the record this way is what makes fine-grained sharing possible at all. A pharmacist needs medications, allergies, diagnoses and kidney function. She does not need the psychiatric formulation — and in MedLattice she is not merely *not shown* it. She is not given a key to that drawer.

Adding a twenty-first category later is an administrative decision. It does not require anything already in existence to be re-encrypted, which is the sort of property that decides whether a system is still maintainable in year eight.

### Sensitivity levels

Separately from the categories, every part of the record carries one of four sensitivity levels.

| Level | What it means | Typical content |
|---|---|---|
| **Open** | No restriction | Anonymised data used for research |
| **Normal** | Ordinary clinical care | Most of the record |
| **Restricted** | Extra care needed | Mental health, sexual health, genetics, safeguarding |
| **Very restricted** | Exceptional | Patient is a member of staff; protected identity; live safeguarding investigation |

Every member of staff carries a matching clearance, and the rule is simply that your clearance has to reach the level of the thing you are asking for.

<div class="ml-key">
<strong>A detail that is worth sitting with</strong>

The same clinical fact can live in two places at two different levels — and this is deliberate, not an accident of filing.

A prescription for lithium appears in <strong>Medications</strong> at the normal level, as a drug and a dose. <em>Why</em> the patient takes it appears in <strong>Mental health</strong> at the restricted level.

So an emergency doctor treating an unconscious patient can see that she takes lithium — which is clinically vital, because lithium toxicity is dangerous, easily missed and rapidly fatal — without thereby acquiring her psychiatric history.

The clinically necessary fact travels. The sensitive context does not. Getting that separation right is most of the work in designing the categories, and it is a clinical judgement rather than an engineering one.
</div>

### Envelopes

Inside each drawer, the record is broken down further still — down to the individual fact.

Surname is one envelope. Date of birth is another. The diagnosis code, the diagnosis description, the free-text note, the date of onset — four more.

In the working demonstration I built alongside the specification, a patient's basic-details drawer came to thirteen separate envelopes, and a five-drawer record came to forty-five.

This is the level at which "need to know" stops being a policy and starts being arithmetic.

## Who sees what

The table below is the default configuration. It is not fixed in the code — it is a setting the organisation controls, and every change to it is written into the shared logbook where an auditor can see who changed what and when.

| Who | What they can reach |
|---|---|
| **The patient** | Everything in their own record |
| **Reception clerk** | Name, date of birth, contact details, insurance. Nothing clinical whatsoever |
| **Healthcare assistant** | Name, date of birth, observations and vital signs |
| **Nurse** | The above, plus allergies, medications, and the *name* of each diagnosis — but not the notes behind it |
| **Junior doctor** | Full ordinary clinical record: notes, routine results, imaging details |
| **Consultant** | The above, plus specialist results, pathology, genetics, social circumstances |
| **Pharmacist** | Medications, allergies, diagnoses, and only the kidney and liver results that affect dosing |
| **Laboratory scientist** | Specimen and result information only — no clinical notes |
| **Radiologist** | Imaging, plus the diagnoses and procedures needed to report it |
| **Mental health clinician** | Mental health and substance use, plus medications and diagnoses |
| **Emergency clinician** | Broad clinical access, plus the ability to break the glass in an emergency |
| **Coding and records staff** | Coded diagnoses and procedures; notes reduced to the summary line |
| **Billing** | Surname, date of birth, membership number, procedure code and date. Nothing else |
| **Researcher** | Anonymised data only |
| **Auditor, data protection officer, Caldicott Guardian** | Who looked at what, when and why — **never the medical content itself** |
| **IT and hosting staff** | **Nothing.** Not restricted by policy — excluded by the locks |

Three of those rows deserve a comment, because each one is a decision that conventional systems get wrong by default.

**A consultant does not automatically outrank a psychiatrist.** A general-medicine consultant, however senior, cannot open the mental health or substance use drawers. Seniority and specialty are different axes, and ordinary role-based access control — which almost always models permissions as a hierarchy of grades — cannot express the distinction at all. It is not a subtle point of ethics either: the federal rules on substance-use records in the United States require exactly this separation, and British information-governance guidance requires the equivalent. I have written the test that asserts it, and it passes.

**The Caldicott Guardian and the data protection officer see the logbook, not the records.** Their job is to know who accessed what and whether it was appropriate. They do not need the clinical content in order to do that job, so they are not given it. This is a genuinely uncomfortable design decision to explain in a meeting — it sounds like a demotion — and it is the right one. An oversight function that requires access to everything it oversees is a new risk wearing a lanyard.

**The people who run the computers see nothing at all.** This is the row that makes outsourced hosting defensible. A hosting provider physically holds the servers, and in a conventional system that means they could in principle read everything on them; the protection is a contract and a background check. Here they hold scrambled data and are never given a key. Their exclusion is not a promise. It is a consequence of the arithmetic, and it holds whether or not they are honest.

## How the locks actually work

You do not need the mathematics, but the shape of the idea is worth having, because it is what makes everything else possible.

### Keys that make other keys

Imagine a building where the master key for a floor can be used to *cut* the keys for the corridors on that floor, and each corridor key can cut the keys for the rooms off it — but the process only runs downwards. From a room key you cannot work backwards to the corridor key, and from one corridor key you cannot reach the corridor next door.

<figure class="ml-fig">
<svg viewBox="0 0 660 300" width="100%" style="max-width:640px" role="img" aria-label="A key tree. The top node is the whole drawer. Below it sit two corridor nodes. Corridor A leads to surname and date of birth; corridor B leads to diagnosis and clinical note. The clerk is handed the corridor A key only, from which she can cut the two keys beneath it and no others.">
  <g stroke="#33455c" stroke-width="1.5" fill="none">
    <path d="M330 56 L180 106"/><path d="M330 56 L480 106"/>
    <path d="M180 134 L95 188"/><path d="M180 134 L265 188"/>
    <path d="M480 134 L395 188"/><path d="M480 134 L565 188"/>
  </g>
  <g font-family="ui-sans-serif,system-ui,-apple-system,sans-serif" font-size="13" text-anchor="middle">
    <rect x="255" y="28" width="150" height="28" rx="5" fill="#16243a" stroke="#4a6684" stroke-width="1.4"/>
    <text x="330" y="46" fill="#cfe0f2">whole drawer</text>
    <rect x="110" y="106" width="140" height="28" rx="5" fill="#0e2b22" stroke="#10b981" stroke-width="1.4"/>
    <text x="180" y="124" fill="#8ff0cc">corridor A</text>
    <rect x="410" y="106" width="140" height="28" rx="5" fill="#151d29" stroke="#3b4c63" stroke-width="1.4"/>
    <text x="480" y="124" fill="#7f8ea1">corridor B</text>
    <rect x="30" y="188" width="130" height="28" rx="5" fill="#0e2b22" stroke="#10b981" stroke-width="1.4"/>
    <text x="95" y="206" fill="#8ff0cc">surname</text>
    <rect x="200" y="188" width="130" height="28" rx="5" fill="#0e2b22" stroke="#10b981" stroke-width="1.4"/>
    <text x="265" y="206" fill="#8ff0cc">date of birth</text>
    <rect x="330" y="188" width="130" height="28" rx="5" fill="#151d29" stroke="#3b4c63" stroke-width="1.4"/>
    <text x="395" y="206" fill="#6d7d90">diagnosis</text>
    <rect x="500" y="188" width="130" height="28" rx="5" fill="#151d29" stroke="#3b4c63" stroke-width="1.4"/>
    <text x="565" y="206" fill="#6d7d90">clinical note</text>
  </g>
  <g font-family="ui-sans-serif,system-ui,-apple-system,sans-serif" font-size="11.5">
    <text x="30" y="248" fill="#10b981">The clerk is handed this one key. From it she can</text>
    <text x="30" y="266" fill="#10b981">cut the two keys below it — and only those.</text>
    <text x="360" y="248" fill="#7f8ea1">She cannot reach these. Not “is not shown” —</text>
    <text x="360" y="266" fill="#7f8ea1">cannot. The cutting only runs downwards.</text>
  </g>
</svg>
<figcaption>How one small key releases exactly the right facts and nothing more. A real drawer has more branches, but the principle does not change: a reader is handed the highest key that covers exactly what they are entitled to, and nothing above it.</figcaption>
</figure>

That is essentially what MedLattice does, except the building is a patient's record and the keys are numbers. Give somebody the key one level up and they get everything beneath it. Give them a key two levels down and they get a single fact. The system works out the smallest set of keys that covers exactly what a person is entitled to and hands over only those — typically between 32 and 160 bytes of key material, which is to say a handful of characters.

This is why the guarantee is so much stronger than a permissions setting. A permissions setting can be wrong. A misconfiguration, a software bug, an injection attack or an angry administrator can all turn *cannot see* into *can see*. A key that does not exist cannot be misconfigured into existence.

It also has a property that matters operationally rather than philosophically: narrowing somebody's future access costs nothing. Broadening it retrospectively is impossible, which is a constraint I have to design around rather than a bug — you cannot un-give a key somebody has already derived. The system handles that by rotating the whole tree periodically, which is the sort of maintenance task that has to be routine rather than exceptional, or it will not happen at all.

### Two locks, not one

Every lock in MedLattice is actually two locks in series: a traditional one and a new quantum-resistant one. Both have to be picked to get in.

This looks like belt and braces, and in a sense it is — but it is the right kind. The traditional method has been studied for forty years and is trusted, but a quantum computer will eventually defeat it. The new method resists quantum computers, but it has only been a published standard since August 2024, and new cryptography occasionally turns out to have flaws that took a decade of attention to find.

Using both means a failure of either one on its own is survivable. I would not bet a fifty-year secret on a two-year-old algorithm alone, and I would not bet it on a forty-year-old one either.

### Which encryption, specifically

For the record, and for anyone who wants to check the claim rather than take it:

| What it does | What it is |
|---|---|
| Locks up each individual fact | **AES-256** — the standard used for classified government material |
| Delivers keys to the right person | **ML-KEM-1024**, published by NIST in August 2024, paired with a traditional method |
| Signs clinical entries so authorship can be proved | **ML-DSA-87**, published by NIST in August 2024, paired with a traditional method |
| Protects the history of the record | **SLH-DSA** — a completely different kind of mathematics, chosen on purpose |

That last row is the one that usually needs explaining, and it is the design decision I am most pleased with.

<div class="ml-key">
<strong>Why I protect the history differently from the content</strong>

Most of MedLattice's security rests on one branch of mathematics — the same branch, as it happens, that both new NIST standards are built on. It is well studied and currently believed to be sound. But it is one branch.

So it is worth asking: if that branch were broken in fifteen years, what exactly would be lost?

<em>Future privacy</em> would be lost, and there is no way around that. Privacy, once gone, does not come back. But there is something considerably worse that could happen, and unlike the first it is avoidable: somebody could go back and <strong>rewrite</strong> the historical record. If that were possible, every past medical record becomes worthless as evidence — in a negligence claim, at an inquest, in a disciplinary hearing, anywhere the question is what was actually known and when.

So the integrity of history is protected by a completely different kind of mathematics, one that relies only on the simplest and best-understood building block in the field. A collapse of the first kind would be very bad. It would not let anybody quietly alter what was recorded.
</div>

## The shared logbook

This is the part people mean when they say "blockchain", and it is worth being precise about what it is doing here, because the word arrives carrying a great deal of baggage that has nothing to do with this.

### What it is

Every participating organisation — hospitals, laboratories, insurers, the public health authority — runs a copy of the same logbook. When something is written to it, all the copies agree on the entry before it counts. Entries can be added but never altered or removed.

**There is no cryptocurrency involved.** Nothing is bought or sold. There is no mining, no token, no speculation, no energy-hungry computation, and no public market of any kind. This is a shared, append-only notebook among known and vetted organisations, and nothing more than that. The technology is borrowed; the economics are not.

### What goes in it

| In the logbook | Not in the logbook |
|---|---|
| Who exists on the system, and their public keys | Any name, date of birth or address |
| Who holds which role, and until when | Any diagnosis, medication, note, image or result |
| What each patient has consented to or refused | Any private key, and in fact any key at all |
| Every grant of access: who, what, why, for how long | Any free-text field a person could type into |
| Every disclosure that actually took place | Anything a regulator would call medical information |
| Every refused attempt | |
| A fingerprint proving a record has not been altered | |

The right-hand column is a hard rule rather than a preference, and I enforce it mechanically. There is a test in the suite that walks every function of the system's ledger programs and fails the build if any of them accepts a free-text field, because free text is where medical information gets into places it should never be. A rule that depends on a future contributor remembering it is not a control; it is a hope. I have written that sentence before, in a different context, and I keep finding it is the load-bearing one.

The reason the rule matters so much is that the logbook cannot be erased. Anything put into it is there permanently — which is exactly the wrong property for medical information and exactly the right property for a record of who looked at it.

### Why bother with copies at all

The traditional answer to *who watches the watchers?* is an audit log. The problem with an audit log is that whoever runs the database also runs the log. If the log says nothing happened, you are taking the operator's word for it, and the operator is precisely the party you were trying to check.

Here the log is held by every participating organisation simultaneously. To alter or suppress an entry, a majority of independent organisations would have to co-operate in the alteration — and even then, a daily fingerprint of the whole logbook is lodged with an outside timestamping service, so the tampering would still be detectable afterwards.

For a hospital, though, the practical benefit is far more immediate than any of that. When something goes wrong and the regulator asks *exactly whose records were exposed, and which parts of them*, the answer is a query rather than a three-week forensic investigation. In Kenya the notification deadline to the Digital Health Agency is 48 hours; under the Data Protection Act it is 72; under the European rules it is 72. Those deadlines get met with evidence rather than with estimates, which is a materially different conversation to have with a regulator.

## What the patient controls

This is not a system in which the patient is merely the subject of a record. She holds a key of her own, and with it she can:

- **See her whole record.** Every drawer, every envelope.
- **Restrict a category.** She can mark mental health, or sexual health, or anything else, as off limits. This overrides the staff permission table — a consultant who would otherwise be entitled is refused, and the refusal is logged.
- **Dismiss a clinician.** She can sever the relationship with any individual member of staff, which cuts their access on their very next query. Not overnight. Next query.
- **Share deliberately.** She can grant one drawer to a named specialist for a second opinion — including a doctor at another institution who has no relationship with her at all and no other route into her record. The grant is limited in time and in the number of times it can be used.
- **Be told.** If a restriction of hers is overridden in an emergency, she is notified. That notification is generated by the system, not by a person deciding whether to send it.

There are exactly three situations in which a restriction can be overridden: a genuine emergency, a legal requirement such as a court order, and a mandatory public-health notification such as a notifiable infectious disease. All three are recorded, all three notify her, and all three are reviewed afterwards.

<div class="ml-good">
<strong>If a patient loses her key</strong>

People lose things, and the record must not be lost with them. Recovery works by agreement between several parties — typically the enrolling hospital, a second clinical organisation, and somebody the patient has nominated herself. Two out of three can restore access.

Because this is also the most attractive way to attack a patient's privacy, recovery is deliberately slow and loud: a 72-hour delay, notifications to every contact on file, and a permanent entry in the logbook. Somebody attempting to impersonate a patient has to do it in public and then wait three days while everyone she knows is told about it.
</div>

## Emergencies

Any system this careful about access raises an obvious objection, and it is the first one every clinician makes: what happens when a patient arrives unconscious at three in the morning and there is no time for any of this?

The answer is a break-glass procedure, and my design intent is worth stating plainly, because it decides every detail underneath it: **it should be easy to use and impossible to hide.**

An emergency clinician can override the relationship requirement and the patient's restrictions with a single action. There is no approval to wait for and nobody to telephone. Anything else would be a system that gets a patient killed on a Sunday night, and I would rather ship no system at all than that one.

What happens in exchange is this:

- The clinician has to type a reason. It is recorded.
- Access expires automatically after four hours. Not at the end of the shift — four hours. Longer than a resuscitation, shorter than a shift, which is the window I settled on and am willing to be argued out of.
- It stays inside the clinician's normal limits. An emergency doctor breaking the glass gets the emergency drawers. They do not thereby acquire the genetics drawer, because genetics is not part of emergency care.
- The patient is notified.
- A counter goes up. Every clinician's lifetime break-glass count is visible.
- The patient can revoke it, and the revocation takes effect on the next query.

That last set of controls is the whole point of the design. A clinician who breaks the glass twice a year in genuine emergencies has nothing whatever to worry about, and nobody will bother them about it. A clinician who breaks it eleven times in a month becomes visible to the Caldicott Guardian without anybody having to go looking for a pattern — which is the opposite of how this works today, where finding that pattern requires somebody to already suspect it.

## Forgetting

European and British law give people a right to have their data erased. A logbook that cannot be altered obviously cannot forget. Those two facts appear to be in direct opposition, and it is a perfectly reasonable objection to the entire approach — it is the objection I would raise first if somebody brought this design to me.

The resolution is the reason the medical content is kept outside the logbook in the first place.

**Erasure is done by destroying the key.** The scrambled data may sit in storage indefinitely, but once the only key to it has been destroyed it can never be read by anybody — including by the hospital holding it. It is a locked box thrown into the sea with its only key melted down. What remains in the logbook is a note that an erasure happened, when, at whose request and under what legal basis. That note contains nothing whatever about the patient.

<div class="ml-honest">
<strong>Where this gets genuinely difficult</strong>

Two honest complications, and I would rather put them here than let somebody find them later.

<strong>First: erasure and retention can be legally opposed.</strong> British and European law give a right to erasure. Kenya's Digital Health Act 2023 requires health records to be kept for twenty years. For a patient with records in both places, these instructions contradict each other outright, and no amount of clever engineering makes that go away.

MedLattice handles it with a <em>legal hold</em> — a marker in the logbook that blocks erasure and names the law requiring it. An erasure request against a held record is refused, the refusal is recorded, and the patient is told which law caused it. That is what the European regulation itself contemplates for processing that is required by law. It is not a satisfying answer. It is the correct one, and the alternative is a system that quietly breaks one law or the other and hopes nobody checks.

<strong>Second: whether destroying the key counts, in law, as erasing the data has not been definitively settled.</strong> Most regulators take the view that making data permanently unintelligible is sufficient. No court has finally decided it. I have written that residual risk into the specification as something to be accepted explicitly rather than assumed away, and the erasure procedure also destroys the identifiers, so that the fallback position is as strong as I can make it.
</div>

## What this does not do

Every security document should contain a section like this. Most do not, which is one of the reasons I distrust most of them.

<div class="ml-honest">
<strong>The limits, stated plainly</strong>

<strong>It cannot stop a clinician who is entitled to see a record from misusing what they saw.</strong> If a doctor legitimately treating you photographs the screen, no encryption in the world prevents it. What the system does is make every access attributable, which turns a technical control into an evidential one — but the prevention is not technical, and I will not pretend otherwise.

<strong>"Quantum-proof" means "quantum-resistant as far as anybody currently knows".</strong> Nobody can prove any encryption secure against an algorithm that has not been invented yet, and anyone who tells you otherwise is selling something. What I can honestly say is this: MedLattice uses the strongest published standards, pairs each with an independent traditional method so that a failure of either alone is survivable, uses a different kind of mathematics again to protect the historical record, and can retire a broken algorithm across the whole network within seconds of deciding to.

<strong>It leaks a little information even with no medical content in the logbook.</strong> Somebody with full access to the logbook cannot read anything — but they can see that activity is occurring, and how often. Frequent access to a particular record suggests somebody is unwell. I reduce this (identifiers are scrambled and rotated, and an empty drawer of every category is created for every patient, so that <em>having</em> a mental health drawer reveals nothing) but I do not eliminate it, and eliminating it entirely would be expensive. That should be a decision made knowingly rather than by default, which is why it is on the list of things awaiting a signature rather than quietly resolved in code.

<strong>It is not designed to resist a lawful warrant.</strong> If a court orders disclosure, the system complies — visibly, with the disclosure recorded like any other. This is a deliberate choice, not an oversight. A system that hospitals cannot lawfully operate is of no use to any patient.

<strong>One older piece of technology remains inside it.</strong> The underlying ledger software still uses an older form of digital signature that a quantum computer would eventually break. This is a real gap and I say so in the specification rather than glossing it. Four things reduce it: the network is closed to outsiders, no medical confidentiality depends on that signature, every request is separately signed with quantum-resistant cryptography, and a replacement is already specified and can be deployed on my own network ahead of the wider ecosystem. It is a gap I can see the end of, but it is a gap today.
</div>

## Does it actually work?

The specification is not a proposal on paper, and I have a low opinion of architecture documents that are. The security-critical parts have been written, run and tested, so the claims in this post can be checked rather than believed.

| What I built | What happened |
|---|---|
| Three programs that run on the shared ledger | All three compile and run |
| A test suite covering every rule described in this post | **61 tests, 61 passed, none failed** |
| A working demonstration of the encryption | Ran end to end |
| A patient record across five drawers and forty-five envelopes | Built and then queried from seven different staff positions |
| Speed | About 54 fully recorded record accesses per second — roughly a hundred times more than a region of two million patients would need |

The demonstration ends by making the central claim testable, which was the whole reason I wrote it. It takes the reception clerk's keys, hands her *every scrambled envelope in the drawer* — as if the entire system had been compromised in her favour — and tries to open all thirteen.

Four open. They are the four she is entitled to.

The other nine fail. Not "are not displayed". Fail, because the keys required to open them cannot be derived from the keys she holds, and no amount of access to the ciphertext changes that.

That is the difference between a rule and a lock, and it is the entire argument for building it this way.

## What happens next

The plan runs to five phases over roughly two and a half years: build and independent audit; a shadow pilot in one department running alongside the existing system with no clinical dependency; live use in one hospital; expansion to a consortium of organisations; and finally the research and secondary-use pipeline.

Two things in that plan are worth flagging to a non-technical reader, because they are the parts that get cut when a timeline gets compressed and they are the parts that must not be.

**The pilot deliberately does nothing.** For four months the system runs in the shadow of the existing record system, mirroring it read-only, with no clinical decision depending on it at any point. It has to reconcile ten thousand accesses against the incumbent system's own audit log before anybody relies on it for anything. This is the correct way to introduce a system that will eventually be trusted with an entire record, and it is slower than anybody wants it to be.

**I practise the emergency twice a year.** The system's main defence against a cryptographic breakthrough is the ability to swap out an algorithm and re-key the whole estate quickly. An untested emergency procedure is not a procedure — it is a paragraph. So twice a year the whole estate gets re-keyed as a drill, with a target of 72 hours, and if the drill fails then that is the most useful thing I will learn all year.

The specification closes with fourteen decisions awaiting a signature. Most are technical. Two are not, and both are the kind of judgement that should not be made by an engineer working alone:

- Whether to accept the unresolved legal question about erasure — that destroying a key counts, in law, as deleting the data.
- How far to go in disguising the *pattern* of access, given that hiding it completely has a real cost and an unproven benefit.

## The specification

Everything in this post is the plain-English account. Underneath it sits the technical document it was written from — the one with the mathematics in it, where every claim made above is stated precisely enough to be checked and, where it is uncertain, said to be uncertain.

**Here is that specification in full, at version 1.0.**

<div style="font-size:0.92em; background:#101a2e; border-left:4px solid #f59e0b; padding:1em 1.3em; margin:1.4em 0; border-radius:0 4px 4px 0;">
📄 <a href="/static/MedLattice_Specification_v1.0.pdf" style="color:#f59e0b; font-weight:bold;">MedLattice Technical Specification v1.0 (PDF)</a> <span style="color:#6b82a0;">&mdash; 40 pages: the architecture, the cryptographic parameters and the reasoning behind each one, the threat model with its residual risks, the regulatory analysis across four jurisdictions, the complete source of the three ledger programs, and the transcripts of the test suite and the working demonstration.</span>
</div>

Version 1.0 means exactly what it says. It is a complete document, not a finished one — open to discussion, correction and refinement, and I would far rather it were read that way than treated as settled. Fourteen of its decisions are still awaiting a signature, and at least two of those are judgements I should not be making on my own.

So if you read it, [get in touch](/contact). Clinicians, informaticians, regulators, security researchers, anybody with a reason to take it apart. I am particularly interested in hearing from anybody who thinks a part of it is wrong, because that is considerably more useful to me than agreement.

<div class="ml-key">
<strong>Where I would most like to be argued with</strong>

The category boundaries — which clinical facts belong in which drawer, and at which sensitivity level — are a clinical judgement dressed up as an engineering decision, and they are the part of this design most likely to be wrong in a way that matters at three in the morning. The lithium example earlier is one I am confident about. There are twenty categories and I am not confident about all of them.

If you have ever been the person who needed one fact from a record you were not entitled to, I would like to know which fact it was.
</div>

## A short glossary

| Term | What it means here |
|---|---|
| **Break the glass** | The emergency override. Instantly available, automatically expiring, always recorded, always notified |
| **Caldicott Guardian** | The senior person in a British healthcare organisation responsible for protecting patient confidentiality |
| **Crypto-shredding** | Erasing data by destroying the only key to it, rather than by deleting the data itself |
| **Drawer** *(technically: compartment)* | One separately locked category of a patient's record — medications, genetics, mental health, and so on |
| **Encryption** | Scrambling information so that only somebody with the right key can read it |
| **Envelope** *(technically: element cell)* | One individually locked fact inside a drawer — a surname, a date, a diagnosis code |
| **FHIR** | The international standard for how medical information is structured, so that different hospitals' systems can understand each other |
| **Key** | The number that unlocks a piece of scrambled information. Whoever holds it can read it; whoever does not, cannot |
| **Ledger / logbook** | The shared, append-only record held by every participating organisation. Contains no medical information |
| **NIST** | The American standards body that ran the international competition to choose the new quantum-resistant encryption, and published the winners in August 2024 |
| **Post-quantum / quantum-resistant** | Encryption designed to remain secure against quantum computers |
| **Purpose of use** | The reason given for each access — treatment, emergency, billing, research, audit, legal. Recorded every time, and checked: billing staff cannot claim to be providing treatment |
| **Quantum computer** | A fundamentally different kind of computer which, once large enough, will break most of the encryption in use today |
| **Smart contract** | A small program that runs on the shared ledger. Everybody can read it, everybody runs the same copy, and nobody can change it quietly |

<div style="font-size:0.85em; background:#111827; border-left:4px solid #6b82a0; padding:0.9em 1.3em; border-radius:0 6px 6px 0; margin:2em 0; color:#9fb3cc;">
<em>MedLattice is a design I am building, not a product on sale. Nothing here should be read as a claim that it is finished. It is a design that has been made concrete enough to be criticised, with the security-critical parts implemented and tested so that the claims can be checked rather than taken on trust — which is the only standard I think is worth applying to anything that holds a medical record.</em>
</div>
