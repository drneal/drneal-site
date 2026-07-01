---
title: "DR Detector: A Doctor's Complete Guide to AI-Powered Diabetic Retinopathy Screening"
date: 2026-07-01
tags: ["diabetic retinopathy", "AI", "clinical tools", "ophthalmology", "screening", "mobile health", "offline", "fundus photography"]
summary: "A step-by-step, jargon-free guide for doctors and nurses who want to use DR Detector — the offline AI retinal screening app — in their clinic today. No tech background required."
---

# DR Detector: A Doctor's Complete Guide to AI-Powered Diabetic Retinopathy Screening

**Downloads:** &nbsp; [📋 User Manual (PDF)](/static/dr_detector_user_manual.pdf) &nbsp;|&nbsp; [🔧 Developer Manual (PDF)](/static/dr_detector_developer_manual.pdf)

---

> **In a hurry?** Jump straight to [Quick Start — 5 Steps](#quick-start-5-steps).

---

Diabetic retinopathy (DR) is a disease that whispers. By the time a patient notices something is wrong with their vision, significant and sometimes irreversible damage has already been done to the retina. We know that early detection and timely referral can prevent **up to 98% of severe vision loss** — yet globally, access to retinal screening is desperately unequal. Ophthalmologists are concentrated in cities; your patients may be hours away.

DR Detector was built to change that arithmetic.

It is a fully **offline** AI screening application that runs on a standard smartphone or laptop. You attach an inexpensive camera adapter to your phone, point it at the patient's eye, press a button, and within five seconds the app tells you whether the retina shows signs of diabetic retinopathy — and exactly what to do next. No internet. No cloud. No patient data ever leaving the device.

This guide will walk you through everything from unboxing to your first screened patient, step by step.

---

## What DR Detector Does (and Doesn't Do)

Before we begin, it is important to be clear about what this tool is.

**What it is:** A clinical screening *aid* — the equivalent of a triage nurse who tells you "this patient probably needs to see a specialist." It helps you decide who to refer and how urgently.

**What it is not:** A diagnostic device. It has not been cleared by the FDA, CE, or any other regulatory authority as a standalone diagnostic tool. A positive result from DR Detector must always be followed up by a trained ophthalmologist.

**What it detects:** Diabetic retinopathy graded across four severity levels. It does *not* detect glaucoma, hypertensive retinopathy, diabetic macular oedema (DMO), or other retinal conditions.

**Accuracy:** On validated test data, the model achieves approximately 83–86% four-class accuracy and ~91% sensitivity for referable DR (Grade 2 and above). These are strong screening-level numbers; local validation on your own patient population is always recommended.

---

## What You Need Before You Start

### 1. A Smartphone or Laptop

DR Detector works on:

- **iPhone** running iOS 15 or later (iOS 17 recommended)
- **Android phone** running Android 8.1 or later (Android 13 recommended)
- **Windows PC** — Windows 10 or 11
- **Mac** — macOS 11 (Big Sur) or later
- **Linux** — Ubuntu 20.04 or later

Your device needs at least **2 GB of RAM** and **200 MB of free storage** (1 GB recommended if you want to keep an image archive). You do not need any particular brand of phone — a mid-range Android from the last four years will work well.

### 2. A Retinal Camera Adapter

This is the one piece of hardware you need to buy. It is a small clip or lens attachment that fits over your phone's rear camera and redirects the light from the patient's retina onto your phone's image sensor. Four options at different price points:

| Device | Platform | Approximate Cost | Notes |
|---|---|---|---|
| **D-EYE Fundus Camera** | iPhone | ~$500 | Clinical-grade; best optical quality |
| **Volk iNview** | iOS / Android | ~$300 | Non-mydriatic; wide field of view |
| **Peek Retina Adapter** | Android | ~$200 | Designed for low-resource settings |
| **DIY 20D Lens Adapter** | Any phone | $50–100 | 3D-printable frame + 20-dioptre condensing lens |

For most primary care or community settings, the **Peek Retina Adapter** or **Volk iNview** strike the best balance of cost and clinical quality. The DIY option is surprisingly capable if you have access to a 3D printer.

### 3. The DR Detector App Installed

Download and install the app on your device. Once installed, you do not need internet again — the AI model, the database, and the PDF generator all live entirely on the device.

📋 **[Download the User Manual for full installation instructions](/static/dr_detector_user_manual.pdf)**

---

## Before Your First Patient: A Five-Minute Setup Check

Run through this once before your first clinic session. You only need to do this once.

**Camera permission:** When you open the app for the first time, it will ask permission to use your camera. Tap **Allow** (or **Grant**). Without this permission the app cannot function. If you accidentally tapped Deny, go to: *Settings → Privacy → Camera → DR Detector* (iPhone) or *Settings → Apps → DR Detector → Permissions* (Android) and enable it.

**Clean the adapter lens:** Use a lens cloth (the kind for glasses) to clean the adapter lens and your phone's camera lens. Fingerprints are the most common cause of low-quality images.

**Test image quality:** Attach the adapter to your phone and point it at a well-lit retinal photography poster or any high-contrast image. You should see a clear, bright circle filling the viewfinder. If the image is dark or blurry, the adapter may be misaligned — adjust the distance between the adapter and the lens by 2–3 mm until the image clears.

**Confirm the screen stays awake:** DR Detector is designed to keep the screen awake during a clinic session. If yours dims, check that battery-saver mode is not overriding this.

---

## Quick Start: 5 Steps {#quick-start-5-steps}

Once set up, screening a single patient takes under two minutes and follows exactly five steps.

### Step 1 — Attach the Camera

Clip the retinal camera adapter firmly over your phone's rear camera lens. Make sure the lens surfaces are clean and the adapter is securely seated — it should not wobble.

### Step 2 — Enter the Patient ID

Open DR Detector. The **Capture Screen** opens automatically. Tap the **Patient ID** field and type the patient's clinic number (up to 20 characters, letters and numbers). If the patient has been screened before, their history will be automatically accessible once their ID is entered.

For a new walk-in patient with no existing clinic number, tap **[+NEW]**. The app creates a new unique ID (in the format PT-XXXXXX) that you can note in their records.

### Step 3 — Position and Capture

Ask the patient to sit comfortably, look straight ahead, and try not to blink. **Dim the room** — this is important. A darker room causes the pupil to dilate naturally, giving you a much clearer retinal image.

Hold the phone gently against the adapter and look at the viewfinder. You should see the retina with the optic disc (a pale, round area) visible somewhere in the frame. A **dashed circle** on screen shows you where to position the optic disc — try to centre it within this guide ring.

When the image looks clear, press the **CAPTURE IMAGE** button. A brief spinner appears while the image is saved.

**Good technique tip:** Rest your wrist against the patient's cheekbone to steady your hand. This single habit reduces motion blur more than anything else.

### Step 4 — Wait Five Seconds and Read the Result

The **Analysis Screen** opens automatically. A progress bar advances through four steps — Loading model, Preprocessing, Inference, Confidence — and the result appears.

You will see:

- A **colour-coded grade** (Green / Yellow / Orange / Red) filling most of the screen
- The **grade name** (e.g., "Moderate NPDR")
- A **confidence percentage** (e.g., "87%")
- A plain-English **clinical action** (e.g., "Refer to ophthalmologist within 3 months")

That is your result. See the next section for what each colour means.

### Step 5 — Save and Proceed

- Tap **SAVE** to store the result in the local database.
- Tap **PDF** to generate a formatted A4 report you can print or share.
- Tap **NEXT** to go straight to the next patient (this also auto-saves the current result).

> ⚠️ **Important:** If you press the back arrow to return to the Capture Screen without tapping SAVE or NEXT, the result will **not** be saved. Always use NEXT or SAVE to move on.

---

## Understanding Your Results

Results follow the International Clinical Diabetic Retinopathy (ICDR) Severity Scale — the same grading system used by ophthalmologists worldwide.

### 🟢 GREEN — No Retinopathy

No signs of diabetic retinopathy are detected. The retina appears healthy.

**Action:** Reassure the patient. Encourage good glycaemic control, blood pressure management, and lipid control. **Bring them back for screening in 12 months.**

### 🟡 YELLOW — Mild NPDR (Non-Proliferative Diabetic Retinopathy)

Microaneurysms (tiny dot-like haemorrhages) are present. This is the earliest detectable stage of DR.

**Action:** The patient does not need an emergency referral, but should be reviewed by an ophthalmologist within **6 months**. This is also a good moment to intensify medical management — tighter HbA1c targets, blood pressure optimisation.

### 🟠 ORANGE — Moderate NPDR

Haemorrhages, hard exudates, or other changes beyond isolated microaneurysms are present.

**Action:** Refer to an ophthalmologist **within 3 months**. Begin discussing the possibility of laser treatment or intravitreal injection with the patient so they are not surprised when the specialist raises it.

### 🔴 RED — Severe NPDR or Proliferative DR (PDR)

Extensive lesions, venous abnormalities, or neovascularisation (new blood vessel growth) are present. This is a sight-threatening stage.

**Action:** **URGENT referral — same day if at all possible.** If same-day ophthalmology is unavailable, refer within one week at the absolute latest. Anti-VEGF therapy or pan-retinal photocoagulation may be urgently needed to prevent vitreous haemorrhage and blindness.

---

## What the Confidence Percentage Means

The confidence figure tells you how certain the AI model is about its result. Think of it like a betting probability.

| Confidence | What it Means | What to Do |
|---|---|---|
| **90–100%** | High — clear image, strong signal | Act on the result with confidence |
| **70–89%** | Moderate — acceptable for screening | Proceed; note the confidence in the patient record |
| **60–69%** | Low — image may be blurry or poorly lit | Consider retaking the image |
| **Below 60%** | Very low — result unreliable | **Retake the image before acting** |

A low confidence score almost always means an image quality problem, not a problem with the patient. See the image quality section below for how to improve it.

---

## Getting a Good Retinal Image: The Practical Guide

Image quality is the single most important factor determining accuracy. In clinic, you will quickly develop an eye for what a good fundus image looks like. Here are the practices that make the biggest difference:

**Dim the room.** This is the most important step. A brighter environment means smaller pupils, which means a worse image. Turn off overhead lights, close blinds, and conduct the exam in as dark a corner as possible. If the clinic has no dimmer, a simple cubicle curtain works.

**Use tropicamide where appropriate.** 1% tropicamide drops dilate the pupil reliably and significantly improve image quality. Wait 15–20 minutes after instillation. This is not mandatory — the app works with natural pupils — but if you have the drops available, use them for patients where image quality is repeatedly low.

**Centre the optic disc.** The dashed guide ring on the Capture Screen is your friend. You want the pale, round optic disc sitting inside or near the centre of that ring. This ensures the critical peripapillary and macular zones are captured.

**Steady your hand.** Press your wrist gently against the patient's cheekbone — this anchor removes most of the tremor that causes motion blur.

**Clean the lenses before every session.** Not every patient — every session. Sebum and dust accumulate quickly on the adapter lens.

**For patients with cataracts:** Moderate-to-severe lens opacity will reduce your fundus image quality significantly and the app will flag low confidence. Note this in the record and refer the patient for cataract assessment alongside the DR referral.

---

## Saving Records and Printing Reports

### The Local Database

Every result you save (by tapping SAVE or NEXT) is stored in a database on the device itself. This database is private — it is not accessible to other apps, and it does not sync to any server. It stores: the patient ID, screening ID, date and time, grade, confidence, the full probability breakdown across all four grades, the retinal image, and the inference time.

To review a patient's history, enter their Patient ID on the Capture Screen and tap the history icon (clock symbol). You will see a chronological timeline of all their previous screenings — useful for monitoring disease progression across annual checks.

### Exporting a PDF Report

Tap the **PDF** button on the Analysis Screen to generate a formal A4 screening report. The report includes everything that would appear in a clinical referral letter: patient ID, date, grade, confidence, probability breakdown, a copy of the retinal image, the clinical action recommendation, and the regulatory disclaimer.

Once generated, the device's native share sheet appears. You can:

- **Print** directly to a Bluetooth or Wi-Fi printer in the clinic
- **Email** to the referral ophthalmology department
- **Send via WhatsApp** to a specialist colleague (common in many health systems)
- **Save to the device's Files app** for later upload to an EMR system

This makes DR Detector compatible with essentially any referral workflow your institution uses — no special integration is required.

---

## Working Offline

One of DR Detector's defining features is that it is entirely self-contained. Once installed, **no internet connection is required for any function**. The AI model is bundled inside the app. The database is local. PDF generation happens on-device.

The only time internet connectivity is relevant is if you choose to *share* a PDF report via email or WhatsApp — those apps need connectivity to send the message, but DR Detector itself does not.

This means the app works equally well in a rural community clinic with no broadband, a remote field camp, a ship's medical bay, or a prison health service. Anywhere you have a phone, you have the screening capability.

---

## Patient History and Longitudinal Monitoring

For patients with diabetes who require annual screening, DR Detector builds an automatic longitudinal record. Each time a patient is screened using the same Patient ID, the result is added to their timeline in the History Screen.

This lets you track progression over time: a patient who was GREEN last year and is now YELLOW needs more intensive medical management and closer monitoring. A patient who has been stable GREEN for three consecutive years might be considered lower risk than someone newly diagnosed.

The History Screen shows each screening as a card: date, grade (with colour), and confidence. Scroll down through a patient's history to see the full arc of their retinal health.

---

## Troubleshooting: Common Problems and Fixes

**The app is asking for camera permission but I already granted it**

Go to your device settings. On iPhone: *Settings → Privacy & Security → Camera → DR Detector* — toggle this On. On Android: *Settings → Apps → DR Detector → Permissions → Camera → Allow*.

**Analysis is taking more than 10 seconds**

On first use, the AI model needs to be loaded into memory — this takes longer. Subsequent analyses will be much faster (typically 1–4 seconds). If slowness persists, close all other apps running in the background to free RAM.

**Confidence is below 60% on every image**

This is almost always an image quality issue. Work through this checklist in order: (1) Clean the adapter lens and phone camera lens. (2) Dim the room further. (3) Ask the patient to look directly ahead. (4) Adjust the adapter distance from the eye by 1–2 mm in each direction until the image brightens. (5) Consider tropicamide drops if available.

**PDF won't share from the app**

Some Android devices with enterprise security policies restrict in-app sharing. Workaround: tap *Save to Files* instead, then open the Files app and share the PDF from there.

**The app crashes immediately after capturing**

The device has insufficient free RAM. Close all background apps, free at least 500 MB of storage, and try again. If the problem persists, the device may not meet the minimum specification.

**Patient's previous history is not showing up**

Patient IDs are case-sensitive on some platforms. Check that you are entering the exact same ID (same capitalisation, same format) that was used in previous sessions. If you used PT-XXXXXX auto-generated IDs, copy-paste rather than retyping where possible.

**Screen is turning off during the exam**

DR Detector is designed to keep the screen awake, but aggressive battery-saver settings can override this. Go to *Settings → Battery* and temporarily disable battery saver mode during your clinic session.

---

## Referral Guidance at a Glance

The table below summarises the recommended clinical actions. Adapt these to your local referral pathways and ophthalmology service availability.

| Grade | Interval | Priority | Key Points |
|---|---|---|---|
| **No Retinopathy** | Annual screening | Routine | Optimise HbA1c, BP, lipids. Rescreen in 12 months |
| **Mild NPDR** | 6-month review | Non-urgent | Intensify medical management. Ophthalmology review within 6 months |
| **Moderate NPDR** | 3-month referral | Semi-urgent | Haemorrhages / exudates present. Refer within 3 months |
| **Severe NPDR / PDR** | Same-day to 1 week | **URGENT** | Neovascularisation risk. Same-day if possible. Anti-VEGF may be needed |

---

## Safety, Limitations, and Medicolegal Notes

Please read this section before using DR Detector in clinical practice.

**This is not a licensed medical device.** DR Detector has not been cleared by the FDA, CE, CDSCO, or any equivalent regulatory body. It must not be used as a standalone diagnostic device, and a clinician's judgement must always take precedence over any app output.

**It does not detect everything.** The app grades diabetic retinopathy only. It does not detect diabetic macular oedema (which requires OCT or slit-lamp biomicroscopy), glaucoma, hypertensive retinopathy, age-related macular degeneration, or any other retinal condition. A GREEN result from DR Detector is not a full retinal examination.

**Training data limitations.** The AI model was trained primarily on the EyePACS dataset, which is predominantly composed of US patients. Performance may vary with different retinal pigmentation profiles. If you are deploying in a population significantly different from a US primary care population, local validation is strongly recommended.

**Cataracts degrade performance.** Lens opacities reduce fundus image quality and can cause the model to undergrade retinopathy severity. Always consider the patient's lens status when interpreting a result.

**Data privacy.** Retinal images are biometric health data. Protect the device with a PIN or biometric lock. Enable device-level encryption. If the device is shared between clinicians, establish a policy for patient ID management to prevent accidental cross-contamination of records. Records cannot be deleted from within the app — your institution's data governance policy applies.

---

## Frequently Asked Questions

**Does the app need internet to work?**
No. Every function — capturing, analysing, saving, and PDF export — works completely offline. Internet is only needed if you choose to send the PDF via email or WhatsApp after it is generated.

**How many patients can I screen per day?**
There is no built-in limit. Experienced operators typically screen 60–120 patients per day in a structured camp setting.

**Can I use the front (selfie) camera?**
No. The rear camera is required because it has higher resolution and is the only lens the adapter is designed for.

**What if I screen the wrong patient by mistake?**
Records cannot be deleted from within the app. Note the error in your patient management system and follow your institution's data correction procedure.

**Can two clinicians share one device?**
Yes, but establish a clear patient ID convention to avoid confusion about whose patients are in the history.

**What about patients who cannot cooperate?** (e.g., severe cognitive impairment, children)
Image quality will likely be low. The app will flag this with a confidence score below 60%. Use clinical judgement — if you cannot obtain a reliable image, note this and refer on clinical grounds rather than waiting for a high-confidence app result.

---

## Getting the Full Documentation

The manuals below are available to download directly:

📋 **[DR Detector User Manual (PDF)](/static/dr_detector_user_manual.pdf)** — Comprehensive guide for clinicians and health workers. Covers setup, operation, image quality, troubleshooting, and referral guidance.

🔧 **[DR Detector Developer Manual (PDF)](/static/dr_detector_developer_manual.pdf)** — Technical reference for software engineers and ML practitioners covering architecture, API, ML pipeline, and deployment.

---

## A Final Word

DR Detector is a tool built in the belief that preventable blindness is, above all, a systems problem — not a medical one. We know what diabetic retinopathy looks like, we know how to treat it, and we know that early referral saves sight. The bottleneck is access: access to equipment, to specialists, to reliable infrastructure.

This app cannot solve all of that. But it can put a meaningful screening capability in the pocket of a primary care doctor in a rural clinic, a nurse in a community health camp, or a medical officer on a remote posting — and that is a start worth making.

If you have questions about the software or encounter a clinical scenario not covered in this guide, the full technical documentation is linked above.

---

*DR Detector is a clinical screening aid only. Results must always be interpreted by a trained health professional. This application has not been cleared as a medical device by any regulatory authority.*
