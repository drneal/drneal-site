---
title: "Voice Clinical Notes: From Dictation to Structured EHR Entry in One Tap"
date: 2026-06-20
category: Clinical AI
tags: clinical NLP, voice recognition, Web Speech API, PWA, Flask, medical AI, EHR, FHIR, Capacitor, iOS, Android
level: Intermediate
read_time: 12 min
summary: How the Voice Clinical Notes app turns free-form dictation into a structured clinical note — PC, Hx, Exam, Ix, Assessment, Plan — using the Web Speech API, a Flask NLP formatting backend, and a Progressive Web App shell that installs on iOS and Android.
featured: true
---

*The app is live at [/voice-notes](/voice-notes). Open it in Chrome, Edge, or Safari (iOS 15+), tap Record, and dictate. Works as an installable home-screen app on both iOS and Android.*

---

In Season 2 of [The Pitt](https://www.imdb.com/title/tt31938062/) — the medical drama series set inside a Pittsburgh emergency department — one of the recurring pressures the clinical team faces is the documentation backlog. Doctors and nurses are accumulating undocumented encounters throughout their shift: the patient seen at 08:00 whose note hasn't been written by noon, the rapid assessment at 14:30 that still needs to make it into the system by handover. The tension is real and recognisable to anyone who has worked in a clinical environment. Clinicians spend roughly 35–45% of their time on documentation — time not spent on patient care.

The Voice Clinical Notes app is a direct attempt to address this. The design principle is radical simplicity: one button to record, one button to format, one tap to share. Nothing more.

## The Problem Being Solved

Clinical documentation has two distinct phases that are often conflated: the *cognitive* work of synthesising what happened with a patient, and the *transcription* work of getting that into a structured format in the EHR. Clinicians are excellent at the first — they do it continuously throughout a consultation. They are forced to do the second at a desk, often hours later, when the cognitive content is less fresh.

Voice dictation solves the transcription delay by capturing the cognitive work at the point of care. The missing piece has historically been the gap between a raw dictation and a structured note. Dictation services have existed for decades, but they produce a wall of text that still needs to be reformatted, sectioned, and proofread before entry into the EHR.

The Voice Clinical Notes app closes that gap automatically.

## Architecture: Three Components

### 1. Web Speech API (On-Device Transcription)

The recording button calls the browser's built-in [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API) via `SpeechRecognition` / `webkitSpeechRecognition`. This is a native browser capability — no audio is sent to this server, no third-party speech service is called, no API key is required. The transcription runs entirely on the user's device.

```javascript
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const r = new SpeechRecognition();
r.continuous     = true;   // keeps recording until the user stops
r.interimResults = true;   // shows words as you speak, not just at the end
r.lang           = 'en-GB';
```

`continuous = true` is the critical setting for clinical use: a short consultation note might be 90 seconds of continuous speech. The default Web Speech API session times out after a few seconds of silence. Setting `continuous = true` and adding an `onend` restart handler keeps the session alive across natural pauses in dictation:

```javascript
r.onend = () => { if (isRec) r.start(); };
```

Interim results appear in real time as the user speaks, giving immediate visual feedback that the recording is working. Final results are committed to the `finalText` buffer once the speech engine is confident in the transcription.

**Browser support:** Chrome, Edge, Chrome for Android (full). Safari on iOS 15+ (single-session, no continuous mode — the restart handler compensates). Firefox: not supported.

The relevant code is in [`templates/voice_notes.html`](https://github.com/drneal/drneal-site/blob/main/templates/voice_notes.html), in the `<script>` block at the bottom.

### 2. Flask NLP Formatting Backend (`POST /voice-notes/format`)

When the user taps Format, the raw transcript string is `POST`-ed to `/voice-notes/format`. The server calls `_format_clinical_note()`, defined in [`app.py`](https://github.com/drneal/drneal-site/blob/main/app.py).

The formatter does four things in sequence:

**Step 1 — Filler word removal.** Speech-to-text transcripts contain dictation fillers: "um", "uh", "er", "you know", "sort of". A regex pass strips these before any further processing.

**Step 2 — Entity extraction.** The transcript is passed through `_run_nlp_extractor()` — the same engine powering the [Clinical Text NLP Extractor](/nlp-extractor) demo. This returns all detected medications, diagnoses, vital signs, lab values, dosages, and dates with their positions in the text.

**Step 3 — Section classification.** Each sentence in the transcript is tested against six keyword-pattern classifiers:

```python
PC = re.compile(r'\b(presenting|complain|came in|brought in|attending)\b', re.I)
HX = re.compile(r'\b(background|history of|known|past medical|chronic)\b', re.I)
EX = re.compile(r'\b(examination|on exam|inspection|found on|appears)\b', re.I)
IX = re.compile(r'\b(blood|ECG|X-ray|CT|MRI|scan|result|showed|pending)\b', re.I)
AS = re.compile(r'\b(impression|assessment|likely|suspect|rule out|diagnosis)\b', re.I)
PL = re.compile(r'\b(plan|will|refer|admit|discharge|prescribe|follow.?up)\b', re.I)
```

Sentences are tested in priority order (Assessment → Plan → Investigations → Examination → History → Presenting Complaint) and assigned to the first matching section. Sentences containing extracted vital sign or lab entities are promoted to Examination or Investigations even without explicit keywords.

**Step 4 — Structured output.** Classified sentences are assembled into a formatted note with section headers, a timestamp, and deduplicated medication and diagnosis lists extracted by the NLP engine:

```
CLINICAL NOTE
Date: 20 June 2026
Time: 08:47

PRESENTING COMPLAINT:
  45-year-old male presenting with acute chest pain for 2 hours.

HISTORY:
  Background of hypertension and type 2 diabetes.

EXAMINATION:
  BP 158/92, HR 96, SpO2 97% on room air.

INVESTIGATIONS:
  ECG showed normal sinus rhythm. Troponin pending.

ASSESSMENT:
  Working impression is possible ACS.

PLAN:
  Serial ECGs. Aspirin 300 mg stat. Cardiology referral.

MEDICATIONS MENTIONED:
  - Aspirin 300 mg
  - Metformin

DIAGNOSES / CONDITIONS:
  - Hypertension
  - Type 2 Diabetes
  - ACS
```

### 3. Progressive Web App Shell

The app includes a [PWA manifest](https://developer.mozilla.org/en-US/docs/Web/Manifest) (`/static/voice-notes-manifest.json`) and a service worker (`/sw.js`) that caches the app shell for offline access. This enables:

- **iOS (Safari):** Tap the Share button → Add to Home Screen → the app installs as a full-screen icon, indistinguishable from a native app.
- **Android (Chrome):** Tap the three-dot menu → Add to Home Screen → same result.

Once installed, the app opens in standalone mode (no browser chrome, no address bar) and loads immediately from cache even without network access. The formatting step requires network (it calls the Flask backend), but the UI itself is available offline.

## Sharing and Export

After formatting, the note is available via four channels:

**Clipboard** — a single tap copies the entire note. On mobile this works via `navigator.clipboard.writeText()` with a legacy `execCommand` fallback for older iOS WebKit.

**WhatsApp** — opens `https://wa.me/?text=<encoded note>`. On mobile this opens directly in WhatsApp; on desktop it opens web.whatsapp.com. The entire structured note appears as a message ready to send to a colleague or to a group (e.g., a handover group chat).

**Email** — `mailto:?subject=Clinical Note&body=<encoded note>`. Opens the device's default mail client with the note pre-populated.

**SMS** — `sms:?body=<encoded note>`. Opens the SMS app. Useful for short notes; for longer ones, WhatsApp is more practical.

**Download as .txt** — plain text file, filename `clinical_note_YYYYMMDD_HHMM.txt`. Paste-into-EHR workflow.

**Download as .rtf** — Rich Text Format file. Compatible with Word, Pages, LibreOffice. Formatted with a monospaced font for alignment of section headers.

The sharing implementation is all client-side JavaScript in `templates/voice_notes.html`. No note content is persisted on the server.

## Privacy Architecture

This is worth being explicit about: **no audio is ever sent to the server**. The Web Speech API runs entirely inside the browser using the device's built-in speech engine (Google's engine on Android Chrome; Apple's on iOS Safari). The only data that leaves the device is the text transcript, which is sent to `/voice-notes/format` and discarded immediately after the formatted note is returned. There is no logging of transcript content, no database storage, and no retention.

For a production clinical deployment, additional controls would apply: TLS-only transport (already enforced by Render), audit logging of API calls (not content), and optionally a fully on-device formatting path using a locally-hosted language model — removing the network dependency entirely.

## The Path to Native iOS and Android

The PWA provides an excellent experience in Safari and Chrome on mobile, but true native distribution — App Store, Play Store — requires an additional build step. The architecture is designed for this:

**[Capacitor.js](https://capacitorjs.com)** (by Ionic) wraps any web app in a native shell with a single command sequence:

```bash
npm install @capacitor/core @capacitor/cli @capacitor/ios @capacitor/android
npx cap init "Voice Clinical Notes" "info.drnealaggarwal.clinicalnotes"
npx cap add ios
npx cap add android
npx cap sync
```

This generates an Xcode project (iOS) and an Android Studio project (Android). The web app runs inside a WKWebView (iOS) or WebView (Android). The critical native capability this unlocks is **native speech recognition**:

- **iOS:** `AVSpeechRecognizer` — Apple's on-device engine with offline support and significantly higher accuracy for medical terminology than the browser Web Speech API.
- **Android:** `android.speech.SpeechRecognizer` — similarly more capable than the browser API, with offline model support via Google's `RecognitionService`.

In the Capacitor build, the Web Speech API calls would be replaced by a Capacitor plugin (`@capacitor-community/speech-recognition`) that bridges to the native engine. The formatting backend remains unchanged — the native app sends the transcript to the same Flask API endpoint. The rest of the app (UI, formatting, sharing) is identical to the web version.

The result is an App Store-distributable application built from the same codebase with approximately two days of additional Capacitor/Xcode configuration work.

## Where This Sits in the Broader Clinical AI Stack

The Voice Clinical Notes app demonstrates a specific capability: converting unstructured speech into structured clinical documentation in real time. In a production clinical informatics deployment this is one component of a larger pipeline:

A **voice-captured note** → structured by NLP → **FHIR R4 resources** (Condition, MedicationStatement, Observation) → ingested by the **clinical data warehouse** → available for **population health analytics**, **clinical decision support**, and **audit**.

The formatting step in this demo is rule-based. In production, it would be replaced by a fine-tuned language model — a clinical BERT or GPT-4-class model trained on de-identified discharge summaries — with substantially higher accuracy on complex, long-form clinical dictation. The output format (SOAP or structured clinical note) would be configurable per specialty, per institution, and per clinician preference.

The demo is the proof-of-concept harness. The full stack is what runs in live deployments.

---

*Try the [Voice Clinical Notes app](/voice-notes). Open it on your phone in Safari (iOS) or Chrome (Android) and try dictating a clinical scenario. Tap Install to add it to your home screen.*

Sources:
- [The Pitt — IMDb](https://www.imdb.com/title/tt31938062/)
