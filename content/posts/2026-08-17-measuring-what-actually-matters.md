---
title: "Measuring What Actually Matters: Kirkpatrick 3 and 4 for Student-Clinicians"
date: 2026-08-17
category: AI & Medicine
tags: Kirkpatrick, programme evaluation, medical education, workplace-based assessment, mini-CEX, DOPS, chart audit, stepped wedge, interrupted time series, skill decay, Miller's pyramid, programmatic assessment, entrustment, clinical AI, Kenya, automation bias
level: All readers — no teaching background assumed
read_time: 41 min
summary: "The tenth of the Institute's ten pedagogical commitments is one sentence long: we measure at Kirkpatrick 3 and 4, or we admit we do not know. This is the fourth companion to the blueprint, and it unpacks that sentence completely — starting from zero, for a reader who has never planned a course in their life. What the four levels are and why almost every training programme stops at the second one. What 'behaviour' means when the behaviour in question is a habit of mind. How you would actually observe, audit and log a student-clinician at three and twelve months without fooling yourself. Why the independent-impression rule is my candidate for the fastest-decaying thing we teach, and what would refute that. What a stepped-wedge design buys you, what it costs, and what to do when you cannot run one. And a working catalogue of the other pedagogical instruments — Miller, entrustment, programmatic assessment, Angoff, retrospective pre-post, logic models, audit and feedback — with notes on how each would be used here."
featured: false
---

<div style="font-size:0.85em; background:#111827; border-left:4px solid #6b82a0; padding:0.9em 1.3em; border-radius:0 6px 6px 0; margin:1.5em 0; color:#9fb3cc;">
<em>I write here in a personal capacity. This is the fourth companion to <a href="/post/2026-08-05-another-arrow-in-the-quiver" style="color:#00d4f5;">Another Arrow in the Quiver</a>, following <a href="/post/2026-08-10-borrowed-from-an-art-school" style="color:#00d4f5;">Borrowed From an Art School</a> on where the competency framework came from, <a href="/post/2026-08-11-one-hidden-error" style="color:#00d4f5;">One Hidden Error</a> on the OSCE and the AI-OSCE, and <a href="/post/2026-08-12-the-angoff-panel-for-testing-clinicians" style="color:#00d4f5;">The Angoff Panel</a> on where the pass mark comes from. Read on its own it should still make sense; nothing here assumes you have taught before.</em>
</div>

<style>
.kp-callout { font-size: 0.9em; background: #101a2e; border-left: 4px solid #00d4f5; padding: 0.9em 1.3em; margin: 1.4em 0; border-radius: 0 4px 4px 0; }
.kp-warn { font-size: 0.9em; background: #1a0f14; border-left: 4px solid #f87171; padding: 0.9em 1.3em; margin: 1.4em 0; border-radius: 0 4px 4px 0; }
.kp-key { font-size: 0.95em; background: #0e1e1a; border-left: 4px solid #10b981; padding: 0.9em 1.3em; margin: 1.4em 0; border-radius: 0 4px 4px 0; }
.kp-note { font-size: 0.88em; background: #141033; border-left: 4px solid #a78bfa; padding: 0.9em 1.3em; margin: 1.4em 0; border-radius: 0 4px 4px 0; }
.kp-fig { margin: 2.2em auto 2.6em; max-width: 100%; }
.kp-fig svg { display: block; width: 100%; height: auto; border-radius: 10px; box-shadow: 0 2px 14px rgba(0,0,0,0.4); }
.kp-fig figcaption { font-size: 0.82em; color: #6b82a0; margin-top: 0.8em; text-align: center; font-style: italic; }
/* The diagrams carry a lot of small type, so let them break out of the
   780px reading column on screens wide enough to take it. */
@media (min-width: 1080px) {
  .kp-fig { width: min(1140px, calc(100vw - 3rem)); margin-left: 50%; transform: translateX(-50%); }
  .kp-fig figcaption { max-width: 820px; margin-left: auto; margin-right: auto; }
}
</style>

[Commitment ten](/post/2026-08-05-another-arrow-in-the-quiver#the-pedagogy-i-would-insist-on), in the [blueprint](/post/2026-08-05-another-arrow-in-the-quiver), is one sentence:

> **We measure at Kirkpatrick 3 and 4, or we admit we do not know.** Satisfaction scores are close to worthless.

It is the shortest of the ten and the one most likely to be quietly dropped, because it is the only one that costs money after the teaching has finished and everybody has gone home pleased with themselves. So it is worth setting out, at length and from first principles, exactly what it commits us to.

First, the whole set, because commitment ten does not stand alone — it is the last of four clusters, and the other nine are what it is measuring.

<figure class="kp-fig">
<svg viewBox="0 0 1240 1040" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Mind map of the ten pedagogical commitments in four colour-coded clusters — what we teach, how we teach, what counts as proof, and how we know it worked — with commitment ten, Kirkpatrick 3 and 4, highlighted">
<defs>
<marker id="mm-cy" markerWidth="13" markerHeight="13" refX="10.5" refY="6.5" orient="auto" markerUnits="userSpaceOnUse"><path d="M1,1 L12,6.5 L1,12 z" fill="#00d4f5"/></marker>
<linearGradient id="mmg-cy" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#00d4f5" stop-opacity="0.15"/><stop offset="100%" stop-color="#00d4f5" stop-opacity="0.9"/></linearGradient>
<marker id="mm-go" markerWidth="13" markerHeight="13" refX="10.5" refY="6.5" orient="auto" markerUnits="userSpaceOnUse"><path d="M1,1 L12,6.5 L1,12 z" fill="#f59e0b"/></marker>
<linearGradient id="mmg-go" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#f59e0b" stop-opacity="0.15"/><stop offset="100%" stop-color="#f59e0b" stop-opacity="0.9"/></linearGradient>
<marker id="mm-gr" markerWidth="13" markerHeight="13" refX="10.5" refY="6.5" orient="auto" markerUnits="userSpaceOnUse"><path d="M1,1 L12,6.5 L1,12 z" fill="#10b981"/></marker>
<linearGradient id="mmg-gr" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#10b981" stop-opacity="0.15"/><stop offset="100%" stop-color="#10b981" stop-opacity="0.9"/></linearGradient>
<marker id="mm-vi" markerWidth="13" markerHeight="13" refX="10.5" refY="6.5" orient="auto" markerUnits="userSpaceOnUse"><path d="M1,1 L12,6.5 L1,12 z" fill="#a78bfa"/></marker>
<linearGradient id="mmg-vi" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#a78bfa" stop-opacity="0.15"/><stop offset="100%" stop-color="#a78bfa" stop-opacity="0.9"/></linearGradient>
<radialGradient id="mm-core"><stop offset="0%" stop-color="#1b2e4d"/><stop offset="100%" stop-color="#0f1a2e"/></radialGradient>
<filter id="mm-glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="6" result="bl"/><feMerge><feMergeNode in="bl"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect x="0.0" y="0.0" width="1240.0" height="1040.0" rx="14" fill="#0d1424" stroke="#182742" stroke-width="1" fill-opacity="1.0"/>
<text x="620.0" y="40.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="19" fill="#c9d6e8" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="2.5" fill-opacity="1.0">THE TEN COMMITMENTS</text>
<text x="620.0" y="62.0" font-family="Helvetica, Arial, sans-serif" font-size="11.5" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">the pedagogy the Institute would be founded on — four clusters, ten promises, one of which this post is about</text>
<path d="M552,468 C534,398 486,361 474,285" fill="none" stroke="#00d4f5" stroke-width="17.2" stroke-opacity="0.22" stroke-linecap="round"/>
<path d="M552,468 C534,398 486,361 474,285" fill="none" stroke="#00d4f5" stroke-width="5.1" stroke-opacity="0.9" marker-end="url(#mm-cy)" stroke-linecap="round"/>
<circle cx="509" cy="376" r="12" fill="#0d1424" stroke="#00d4f5" stroke-width="1.5"/>
<text x="509.1" y="379.6" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12" fill="#00d4f5" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">2</text>
<rect x="324.0" y="223.0" width="212.0" height="58.0" rx="12" fill="#16233a" stroke="#00d4f5" stroke-width="1.8" fill-opacity="1.0"/>
<rect x="324" y="223" width="6" height="58" rx="3" fill="#00d4f5"/>
<text x="433.0" y="246.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.4" fill="#00d4f5" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0.9" fill-opacity="1.0">WHAT WE TEACH</text>
<text x="433.0" y="266.0" font-family="Helvetica, Arial, sans-serif" font-size="9.9" fill="#8ea4c0" text-anchor="middle" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">teach judgement</text>
<path d="M324,252 C319,252 319,190 314,190" fill="none" stroke="#00d4f5" stroke-width="3.1" stroke-opacity="0.55" marker-end="url(#mm-cy)"/>
<rect x="26.0" y="134.0" width="280.0" height="112.0" rx="11" fill="#111c30" stroke="#1e2d45" stroke-width="1" fill-opacity="1.0"/>
<rect x="26" y="134" width="280" height="3.5" rx="1.75" fill="#00d4f5" fill-opacity="0.55"/>
<circle cx="53" cy="164" r="14" fill="#00d4f5" fill-opacity="0.16" stroke="#00d4f5" stroke-width="1.4"/>
<text x="53.0" y="168.5" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12.5" fill="#00d4f5" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">1</text>
<g transform="translate(278.0,166.0) scale(0.98)" stroke="#00d4f5" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M0,-10 L0,8"/><path d="M-9,-6 L9,-6"/><path d="M-9,-6 L-13,2 L-5,2 Z" fill="#00d4f5" fill-opacity="0.25"/><path d="M9,-6 L5,2 L13,2 Z" fill="#00d4f5" fill-opacity="0.25"/><path d="M-6,8 L6,8"/><circle cx="0" cy="-11" r="1.8" fill="#00d4f5"/></g>
<text x="76.0" y="169.0" font-family="Helvetica, Arial, sans-serif" font-size="12.8" fill="#c9d6e8" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">Judgement, not tools</text>
<text x="42.0" y="194.0" font-family="Helvetica, Arial, sans-serif" font-size="10.3" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">If the vendor vanished overnight, would this</text>
<text x="42.0" y="208.5" font-family="Helvetica, Arial, sans-serif" font-size="10.3" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">still be worth teaching? If not, it is a</text>
<text x="42.0" y="223.0" font-family="Helvetica, Arial, sans-serif" font-size="10.3" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">manual.</text>
<path d="M324,252 C319,252 319,356 314,356" fill="none" stroke="#00d4f5" stroke-width="4.0" stroke-opacity="0.55" marker-end="url(#mm-cy)"/>
<rect x="26.0" y="300.0" width="280.0" height="112.0" rx="11" fill="#111c30" stroke="#1e2d45" stroke-width="1" fill-opacity="1.0"/>
<rect x="26" y="300" width="280" height="3.5" rx="1.75" fill="#00d4f5" fill-opacity="0.55"/>
<circle cx="53" cy="330" r="14" fill="#00d4f5" fill-opacity="0.16" stroke="#00d4f5" stroke-width="1.4"/>
<text x="53.0" y="334.5" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12.5" fill="#00d4f5" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">2</text>
<g transform="translate(278.0,332.0) scale(0.98)" stroke="#00d4f5" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="-2" cy="-2" r="7.5"/><path d="M3.5,3.5 L10,10"/><path d="M-5,-2 L-2,1 L2,-5" stroke="#f87171"/></g>
<text x="76.0" y="335.0" font-family="Helvetica, Arial, sans-serif" font-size="12.8" fill="#c9d6e8" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">Scepticism is drilled</text>
<text x="42.0" y="360.0" font-family="Helvetica, Arial, sans-serif" font-size="10.3" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">Not a lecture on limitations. A reflex, like</text>
<text x="42.0" y="374.5" font-family="Helvetica, Arial, sans-serif" font-size="10.3" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">spotting a deteriorating patient — and it is</text>
<text x="42.0" y="389.0" font-family="Helvetica, Arial, sans-serif" font-size="10.3" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">assessed.</text>
<path d="M688,468 C706,398 754,361 766,285" fill="none" stroke="#f59e0b" stroke-width="21.8" stroke-opacity="0.22" stroke-linecap="round"/>
<path d="M688,468 C706,398 754,361 766,285" fill="none" stroke="#f59e0b" stroke-width="6.4" stroke-opacity="0.9" marker-end="url(#mm-go)" stroke-linecap="round"/>
<circle cx="731" cy="376" r="12" fill="#0d1424" stroke="#f59e0b" stroke-width="1.5"/>
<text x="730.9" y="379.6" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12" fill="#f59e0b" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">3</text>
<rect x="704.0" y="223.0" width="212.0" height="58.0" rx="12" fill="#16233a" stroke="#f59e0b" stroke-width="1.8" fill-opacity="1.0"/>
<rect x="704" y="223" width="6" height="58" rx="3" fill="#f59e0b"/>
<text x="813.0" y="246.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.4" fill="#f59e0b" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0.9" fill-opacity="1.0">HOW WE TEACH</text>
<text x="813.0" y="266.0" font-family="Helvetica, Arial, sans-serif" font-size="9.9" fill="#8ea4c0" text-anchor="middle" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">in Kenyan cases, safely, together</text>
<path d="M916,252 C921,252 921,158 926,158" fill="none" stroke="#f59e0b" stroke-width="4.0" stroke-opacity="0.55" marker-end="url(#mm-go)"/>
<rect x="934.0" y="102.0" width="280.0" height="112.0" rx="11" fill="#111c30" stroke="#1e2d45" stroke-width="1" fill-opacity="1.0"/>
<rect x="934" y="102" width="280" height="3.5" rx="1.75" fill="#f59e0b" fill-opacity="0.55"/>
<circle cx="961" cy="132" r="14" fill="#f59e0b" fill-opacity="0.16" stroke="#f59e0b" stroke-width="1.4"/>
<text x="961.0" y="136.5" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12.5" fill="#f59e0b" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">5</text>
<g transform="translate(1186.0,134.0) scale(0.98)" stroke="#f59e0b" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M0,10 C0,10 8,0 8,-4 A8,8 0 1,0 -8,-4 C-8,0 0,10 0,10 Z" fill="#f59e0b" fill-opacity="0.18"/><circle cx="0" cy="-4" r="3"/></g>
<text x="984.0" y="137.0" font-family="Helvetica, Arial, sans-serif" font-size="12.8" fill="#c9d6e8" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">Kenyan cases only</text>
<text x="950.0" y="162.0" font-family="Helvetica, Arial, sans-serif" font-size="10.3" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">No vignette with insurance codes, drugs we</text>
<text x="950.0" y="176.5" font-family="Helvetica, Arial, sans-serif" font-size="10.3" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">cannot obtain, or investigations we do not</text>
<text x="950.0" y="191.0" font-family="Helvetica, Arial, sans-serif" font-size="10.3" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">have.</text>
<path d="M916,252 C921,252 921,296 926,296" fill="none" stroke="#f59e0b" stroke-width="2.2" stroke-opacity="0.55" marker-end="url(#mm-go)"/>
<rect x="934.0" y="240.0" width="280.0" height="112.0" rx="11" fill="#111c30" stroke="#1e2d45" stroke-width="1" fill-opacity="1.0"/>
<rect x="934" y="240" width="280" height="3.5" rx="1.75" fill="#f59e0b" fill-opacity="0.55"/>
<circle cx="961" cy="270" r="14" fill="#f59e0b" fill-opacity="0.16" stroke="#f59e0b" stroke-width="1.4"/>
<text x="961.0" y="274.5" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12.5" fill="#f59e0b" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">6</text>
<g transform="translate(1186.0,272.0) scale(0.98)" stroke="#f59e0b" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M0,-10 L9,-6 V1 C9,7 0,11 0,11 C0,11 -9,7 -9,1 V-6 Z" fill="#f59e0b" fill-opacity="0.18"/><path d="M-4,0 L-1,3.5 L4.5,-4"/></g>
<text x="984.0" y="275.0" font-family="Helvetica, Arial, sans-serif" font-size="12.8" fill="#c9d6e8" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">Simulation before patients</text>
<text x="950.0" y="300.0" font-family="Helvetica, Arial, sans-serif" font-size="10.3" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">Uncontroversial for central lines. It should be</text>
<text x="950.0" y="314.5" font-family="Helvetica, Arial, sans-serif" font-size="10.3" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">uncontroversial here too.</text>
<path d="M916,252 C921,252 921,434 926,434" fill="none" stroke="#f59e0b" stroke-width="4.0" stroke-opacity="0.55" marker-end="url(#mm-go)"/>
<rect x="934.0" y="378.0" width="280.0" height="112.0" rx="11" fill="#111c30" stroke="#1e2d45" stroke-width="1" fill-opacity="1.0"/>
<rect x="934" y="378" width="280" height="3.5" rx="1.75" fill="#f59e0b" fill-opacity="0.55"/>
<circle cx="961" cy="408" r="14" fill="#f59e0b" fill-opacity="0.16" stroke="#f59e0b" stroke-width="1.4"/>
<text x="961.0" y="412.5" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12.5" fill="#f59e0b" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">8</text>
<g transform="translate(1186.0,410.0) scale(0.98)" stroke="#f59e0b" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="-5" cy="-5" r="3"/><path d="M-10,7 C-10,1 -8,-1 -5,-1 C-2,-1 0,1 0,7"/><circle cx="5" cy="-5" r="3" stroke="#f59e0b"/><path d="M0,7 C0,1 2,-1 5,-1 C8,-1 10,1 10,7" stroke="#f59e0b"/><path d="M-2.5,-8 L2.5,-8" stroke-dasharray="1.5 1.5"/></g>
<text x="984.0" y="413.0" font-family="Helvetica, Arial, sans-serif" font-size="12.8" fill="#c9d6e8" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">Interprofessional by default</text>
<text x="950.0" y="438.0" font-family="Helvetica, Arial, sans-serif" font-size="10.3" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">Ward AI use is not a doctor problem or a nurse</text>
<text x="950.0" y="452.5" font-family="Helvetica, Arial, sans-serif" font-size="10.3" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">problem. The failure modes live in the</text>
<text x="950.0" y="467.0" font-family="Helvetica, Arial, sans-serif" font-size="10.3" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">handover.</text>
<path d="M552,556 C534,626 486,663 474,739" fill="none" stroke="#10b981" stroke-width="21.8" stroke-opacity="0.22" stroke-linecap="round"/>
<path d="M552,556 C534,626 486,663 474,739" fill="none" stroke="#10b981" stroke-width="6.4" stroke-opacity="0.9" marker-end="url(#mm-gr)" stroke-linecap="round"/>
<circle cx="509" cy="648" r="12" fill="#0d1424" stroke="#10b981" stroke-width="1.5"/>
<text x="509.1" y="652.4" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12" fill="#10b981" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">3</text>
<rect x="324.0" y="743.0" width="212.0" height="58.0" rx="12" fill="#16233a" stroke="#10b981" stroke-width="1.8" fill-opacity="1.0"/>
<rect x="324" y="743" width="6" height="58" rx="3" fill="#10b981"/>
<text x="433.0" y="766.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.4" fill="#10b981" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0.9" fill-opacity="1.0">WHAT COUNTS AS PROOF</text>
<text x="433.0" y="786.0" font-family="Helvetica, Arial, sans-serif" font-size="9.9" fill="#8ea4c0" text-anchor="middle" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">prove it or it did not happen</text>
<path d="M324,772 C319,772 319,648 314,648" fill="none" stroke="#10b981" stroke-width="2.2" stroke-opacity="0.55" marker-end="url(#mm-gr)"/>
<rect x="26.0" y="592.0" width="280.0" height="112.0" rx="11" fill="#111c30" stroke="#1e2d45" stroke-width="1" fill-opacity="1.0"/>
<rect x="26" y="592" width="280" height="3.5" rx="1.75" fill="#10b981" fill-opacity="0.55"/>
<circle cx="53" cy="622" r="14" fill="#10b981" fill-opacity="0.16" stroke="#10b981" stroke-width="1.4"/>
<text x="53.0" y="626.5" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12.5" fill="#10b981" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">3</text>
<g transform="translate(278.0,624.0) scale(0.98)" stroke="#10b981" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="-11" y="-8" width="8" height="16" rx="2" fill="#10b981" fill-opacity="0.18"/><rect x="3" y="-8" width="8" height="16" rx="2" fill="#10b981" fill-opacity="0.18"/><path d="M-1.5,-2 L1.5,-2 M-1.5,2 L1.5,2"/></g>
<text x="76.0" y="627.0" font-family="Helvetica, Arial, sans-serif" font-size="12.8" fill="#c9d6e8" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">Taught = assessed</text>
<text x="42.0" y="652.0" font-family="Helvetica, Arial, sans-serif" font-size="10.3" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">Nothing is taught that is not assessed. Nothing</text>
<text x="42.0" y="666.5" font-family="Helvetica, Arial, sans-serif" font-size="10.3" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">is assessed that was not taught.</text>
<path d="M324,772 C319,772 319,786 314,786" fill="none" stroke="#10b981" stroke-width="3.1" stroke-opacity="0.55" marker-end="url(#mm-gr)"/>
<rect x="26.0" y="730.0" width="280.0" height="112.0" rx="11" fill="#111c30" stroke="#1e2d45" stroke-width="1" fill-opacity="1.0"/>
<rect x="26" y="730" width="280" height="3.5" rx="1.75" fill="#10b981" fill-opacity="0.55"/>
<circle cx="53" cy="760" r="14" fill="#10b981" fill-opacity="0.16" stroke="#10b981" stroke-width="1.4"/>
<text x="53.0" y="764.5" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12.5" fill="#10b981" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">4</text>
<g transform="translate(278.0,762.0) scale(0.98)" stroke="#10b981" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="-10" y="-7" width="20" height="14" rx="2"/><path d="M-6,-2 L2,-2 M-6,2 L0,2"/><circle cx="0" cy="0" r="10.5" stroke="#f87171"/><path d="M-7.5,7.5 L7.5,-7.5" stroke="#f87171" stroke-width="2"/></g>
<text x="76.0" y="765.0" font-family="Helvetica, Arial, sans-serif" font-size="12.8" fill="#c9d6e8" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">No attendance awards</text>
<text x="42.0" y="790.0" font-family="Helvetica, Arial, sans-serif" font-size="10.3" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">No certificate for having been present. This</text>
<text x="42.0" y="804.5" font-family="Helvetica, Arial, sans-serif" font-size="10.3" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">will make us unpopular and it is not</text>
<text x="42.0" y="819.0" font-family="Helvetica, Arial, sans-serif" font-size="10.3" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">negotiable.</text>
<path d="M324,772 C319,772 319,924 314,924" fill="none" stroke="#10b981" stroke-width="3.1" stroke-opacity="0.55" marker-end="url(#mm-gr)"/>
<rect x="26.0" y="868.0" width="280.0" height="112.0" rx="11" fill="#111c30" stroke="#1e2d45" stroke-width="1" fill-opacity="1.0"/>
<rect x="26" y="868" width="280" height="3.5" rx="1.75" fill="#10b981" fill-opacity="0.55"/>
<circle cx="53" cy="898" r="14" fill="#10b981" fill-opacity="0.16" stroke="#10b981" stroke-width="1.4"/>
<text x="53.0" y="902.5" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12.5" fill="#10b981" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">7</text>
<g transform="translate(278.0,900.0) scale(0.98)" stroke="#10b981" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M-7,-10 H4 L8,-6 V10 H-7 Z" fill="#10b981" fill-opacity="0.14"/><path d="M4,-10 V-6 H8"/><path d="M-4,-2 H5 M-4,2 H5 M-4,6 H1"/><path d="M-9,8 L-3,8" stroke="#f59e0b" stroke-width="2"/></g>
<text x="76.0" y="903.0" font-family="Helvetica, Arial, sans-serif" font-size="12.8" fill="#c9d6e8" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">The learner produces work</text>
<text x="42.0" y="928.0" font-family="Helvetica, Arial, sans-serif" font-size="10.3" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">A logbook, a critique, an evaluation, a taught</text>
<text x="42.0" y="942.5" font-family="Helvetica, Arial, sans-serif" font-size="10.3" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">session — countersigned by a named senior.</text>
<path d="M688,556 C706,626 754,663 766,739" fill="none" stroke="#a78bfa" stroke-width="17.2" stroke-opacity="0.22" stroke-linecap="round"/>
<path d="M688,556 C706,626 754,663 766,739" fill="none" stroke="#a78bfa" stroke-width="5.1" stroke-opacity="0.9" marker-end="url(#mm-vi)" stroke-linecap="round"/>
<circle cx="731" cy="648" r="12" fill="#0d1424" stroke="#a78bfa" stroke-width="1.5"/>
<text x="730.9" y="652.4" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12" fill="#a78bfa" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">2</text>
<rect x="704.0" y="743.0" width="212.0" height="58.0" rx="12" fill="#16233a" stroke="#a78bfa" stroke-width="1.8" fill-opacity="1.0"/>
<rect x="704" y="743" width="6" height="58" rx="3" fill="#a78bfa"/>
<text x="813.0" y="766.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.4" fill="#a78bfa" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0.9" fill-opacity="1.0">HOW WE KNOW IT WORKED</text>
<text x="813.0" y="786.0" font-family="Helvetica, Arial, sans-serif" font-size="9.9" fill="#8ea4c0" text-anchor="middle" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">and measure whether it held</text>
<path d="M916,772 C921,772 921,732 926,732" fill="none" stroke="#a78bfa" stroke-width="2.2" stroke-opacity="0.55" marker-end="url(#mm-vi)"/>
<rect x="934.0" y="676.0" width="280.0" height="112.0" rx="11" fill="#111c30" stroke="#1e2d45" stroke-width="1" fill-opacity="1.0"/>
<rect x="934" y="676" width="280" height="3.5" rx="1.75" fill="#a78bfa" fill-opacity="0.55"/>
<circle cx="961" cy="706" r="14" fill="#a78bfa" fill-opacity="0.16" stroke="#a78bfa" stroke-width="1.4"/>
<text x="961.0" y="710.5" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12.5" fill="#a78bfa" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">9</text>
<g transform="translate(1186.0,708.0) scale(0.98)" stroke="#a78bfa" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="0" cy="-3" r="6.5" fill="#a78bfa" fill-opacity="0.16"/><path d="M-3,3 L-5,11 L0,8.5 L5,11 L3,3"/><path d="M-2.5,-3.5 L-0.5,-1.5 L3,-5.5"/></g>
<text x="984.0" y="711.0" font-family="Helvetica, Arial, sans-serif" font-size="12.8" fill="#c9d6e8" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">Faculty are certified</text>
<text x="950.0" y="736.0" font-family="Helvetica, Arial, sans-serif" font-size="10.3" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">And their teaching is observed. Nobody teaches</text>
<text x="950.0" y="750.5" font-family="Helvetica, Arial, sans-serif" font-size="10.3" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">on this programme unexamined.</text>
<path d="M916,772 C921,772 921,894 926,894" fill="none" stroke="#a78bfa" stroke-width="5.2" stroke-opacity="0.95" marker-end="url(#mm-vi)"/>
<g filter="url(#mm-glow)"><rect x="934.0" y="838.0" width="280.0" height="134.0" rx="11" fill="#15243c" stroke="#a78bfa" stroke-width="2.4" fill-opacity="1.0"/></g>
<rect x="934" y="838" width="280" height="3.5" rx="1.75" fill="#a78bfa" fill-opacity="1"/>
<circle cx="961" cy="868" r="14" fill="#a78bfa" fill-opacity="0.16" stroke="#a78bfa" stroke-width="1.4"/>
<text x="961.0" y="872.5" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12.5" fill="#a78bfa" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">10</text>
<g transform="translate(1186.0,870.0) scale(0.98)" stroke="#a78bfa" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="-10" y="2" width="4" height="7" fill="#a78bfa" fill-opacity="0.3"/><rect x="-3.5" y="-3" width="4" height="12" fill="#a78bfa" fill-opacity="0.55"/><rect x="3" y="-9" width="4" height="18" fill="#a78bfa" fill-opacity="0.85"/><path d="M-12,10 L11,10" stroke="#6b82a0"/></g>
<text x="984.0" y="873.0" font-family="Helvetica, Arial, sans-serif" font-size="12.8" fill="#c9d6e8" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">Kirkpatrick 3 and 4</text>
<text x="950.0" y="898.0" font-family="Helvetica, Arial, sans-serif" font-size="10.3" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">Behaviour and results, or we admit we do not</text>
<text x="950.0" y="912.5" font-family="Helvetica, Arial, sans-serif" font-size="10.3" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">know. Satisfaction scores are close to</text>
<text x="950.0" y="927.0" font-family="Helvetica, Arial, sans-serif" font-size="10.3" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">worthless.</text>
<text x="950.0" y="962.0" font-family="Helvetica, Arial, sans-serif" font-size="10.3" fill="#a78bfa" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">▸ this post unpacks this one, completely</text>
<g filter="url(#mm-glow)">
<ellipse cx="620" cy="512" rx="104" ry="56" fill="url(#mm-core)" stroke="#31507f" stroke-width="2"/>
</g>
<text x="620.0" y="500.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="24" fill="#c9d6e8" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="5" fill-opacity="1.0">TEN</text>
<text x="620.0" y="523.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="14.5" fill="#c9d6e8" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="2" fill-opacity="1.0">COMMITMENTS</text>
<text x="620.0" y="544.0" font-family="Helvetica, Arial, sans-serif" font-size="9.4" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">written into the founding documents</text>
<line x1="40" y1="988" x2="1200" y2="988" stroke="#1e2d45"/>
<text x="134.3" y="1014" font-family="Helvetica, Arial, sans-serif" font-size="13" fill="#00d4f5" text-anchor="middle" font-weight="bold" font-style="italic">teach judgement</text>
<circle cx="223.6" cy="1010" r="2.4" fill="#6b82a0"/>
<text x="402.0" y="1014" font-family="Helvetica, Arial, sans-serif" font-size="13" fill="#f59e0b" text-anchor="middle" font-weight="bold" font-style="italic">in Kenyan cases, safely, together</text>
<circle cx="580.4" cy="1010" r="2.4" fill="#6b82a0"/>
<text x="739.0" y="1014" font-family="Helvetica, Arial, sans-serif" font-size="13" fill="#10b981" text-anchor="middle" font-weight="bold" font-style="italic">prove it or it did not happen</text>
<circle cx="897.6" cy="1010" r="2.4" fill="#6b82a0"/>
<text x="1046.3" y="1014" font-family="Helvetica, Arial, sans-serif" font-size="13" fill="#a78bfa" text-anchor="middle" font-weight="bold" font-style="italic">and measure whether it held</text>
</svg>
<figcaption>The ten pedagogical commitments. Ten loose items sit right at the edge of working memory; four coloured groups do not. Read the phrases along the bottom as one sentence — <strong>teach judgement · in Kenyan cases, safely, together · prove it or it did not happen · and measure whether it held</strong>. The tenth is the subject of everything below.</figcaption>
</figure>

---

## Part 1 — What Kirkpatrick actually is

### 1.1 The problem it was invented to solve

In 1954 a doctoral student at the University of Wisconsin called Donald Kirkpatrick wrote a dissertation on how you would tell whether a training course had done anything. In November 1959 he turned it into a four-part series of articles for the journal of what was then the American Society of Training Directors, one article per idea. He was writing about supervisors in American industry, not clinicians, and he was not trying to build a theory. He was trying to stop people claiming success on the basis of the form the delegates filled in at the end of the day. ([Kirkpatrick Partners' own account](https://www.kirkpatrickpartners.com/wp-content/uploads/2021/11/Introduction-to-The-New-World-Kirkpatrick%C2%AE-Model.pdf); a useful historical corrective on the attribution is [Will Thalheimer's](https://www.worklearning.com/2018/01/30/donald-kirkpatrick-was-not-the-originator-of-the-four-level-model-of-learning-evaluation/).)

Seventy years later the four articles have hardened into the default vocabulary of training evaluation across every industry, including ours. That ubiquity is a problem in itself, because a framework everyone recites is a framework nobody examines.

### 1.2 The four levels, in plain language

Here is the whole model. If you have never planned a course in your life, this is all you need to start with.

Imagine you have just run a two-day workshop for twenty clinical officers. There are four completely different questions you could ask about it, and they are not four ways of asking the same thing. They are four different questions with four different answers, and it is entirely possible for the answer to be *yes* at one level and *no* at the next.

1. **Did they like it?** — *Reaction.* You find out by asking them.
2. **Did they learn it?** — *Learning.* You find out by testing them.
3. **Do they do it at work?** — *Behaviour.* You find out by going to their workplace, months later, and looking.
4. **Did anything change for the patient?** — *Results.* You find out by measuring something about the service, and by having designed the measurement before you started.

<figure class="kp-fig">
<svg viewBox="0 0 1010 646" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Kirkpatrick's four levels drawn as an ascending staircase — reaction, learning, behaviour, results — with Miller's pyramid levels mapped underneath and a marker showing where most programmes stop">
<defs><marker id="ld-a" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L9,5 L0,10 z" fill="#6b82a0"/></marker><marker id="ld-r" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L9,5 L0,10 z" fill="#f87171"/></marker></defs>
<rect x="0.0" y="0.0" width="1010.0" height="646.0" rx="14" fill="#0d1424" stroke="#182742" stroke-width="1" fill-opacity="1.0"/>
<text x="505.0" y="36.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="16" fill="#c9d6e8" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="1.6" fill-opacity="1.0">THE FOUR LEVELS — AND WHAT EACH ONE ACTUALLY ASKS</text>
<text x="505.0" y="57.0" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">climbing costs more at every step; the answers get more useful at exactly the same rate</text>
<rect x="104.0" y="320.0" width="200.0" height="186.0" rx="10" fill="#111c30" stroke="#f87171" stroke-width="1.6" fill-opacity="1.0"/>
<rect x="104" y="320" width="200" height="4" rx="2" fill="#f87171"/>
<text x="120.0" y="350.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11" fill="#f87171" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="1.4" fill-opacity="1.0">LEVEL 1</text>
<text x="120.0" y="374.0" font-family="Helvetica, Arial, sans-serif" font-size="17" fill="#c9d6e8" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0.6" fill-opacity="1.0">REACTION</text>
<text x="120.0" y="395.0" font-family="Helvetica, Arial, sans-serif" font-size="11.8" fill="#f87171" text-anchor="start" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">Did they like it?</text>
<text x="120.0" y="420.0" font-family="Helvetica, Arial, sans-serif" font-size="9.9" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">Happy sheets. Attendance. Star</text>
<text x="120.0" y="433.0" font-family="Helvetica, Arial, sans-serif" font-size="9.9" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">ratings.</text>
<line x1="120" y1="450" x2="288" y2="450" stroke="#1e2d45"/>
<text x="120.0" y="466.0" font-family="Helvetica, Arial, sans-serif" font-size="9.7" fill="#6b82a0" text-anchor="start" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">Correlates poorly with anything.</text>
<text x="120.0" y="479.0" font-family="Helvetica, Arial, sans-serif" font-size="9.7" fill="#6b82a0" text-anchor="start" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">Collect it to catch a broken</text>
<text x="120.0" y="492.0" font-family="Helvetica, Arial, sans-serif" font-size="9.7" fill="#6b82a0" text-anchor="start" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">room, not to claim an effect.</text>
<rect x="104.0" y="522.0" width="200.0" height="38.0" rx="7" fill="#0f1b2d" stroke="#1e2d45" stroke-width="1" fill-opacity="1.0"/>
<text x="204.0" y="546.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.2" fill="#6b82a0" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">—</text>
<rect x="320.0" y="276.0" width="200.0" height="230.0" rx="10" fill="#111c30" stroke="#f59e0b" stroke-width="1.6" fill-opacity="1.0"/>
<rect x="320" y="276" width="200" height="4" rx="2" fill="#f59e0b"/>
<text x="336.0" y="306.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11" fill="#f59e0b" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="1.4" fill-opacity="1.0">LEVEL 2</text>
<text x="336.0" y="330.0" font-family="Helvetica, Arial, sans-serif" font-size="17" fill="#c9d6e8" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0.6" fill-opacity="1.0">LEARNING</text>
<text x="336.0" y="351.0" font-family="Helvetica, Arial, sans-serif" font-size="11.8" fill="#f59e0b" text-anchor="start" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">Did they learn it?</text>
<text x="336.0" y="376.0" font-family="Helvetica, Arial, sans-serif" font-size="9.9" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">MCQ, OSCE, AI-OSCE, simulation</text>
<text x="336.0" y="389.0" font-family="Helvetica, Arial, sans-serif" font-size="9.9" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">scores.</text>
<line x1="336" y1="406" x2="504" y2="406" stroke="#1e2d45"/>
<text x="336.0" y="422.0" font-family="Helvetica, Arial, sans-serif" font-size="9.7" fill="#6b82a0" text-anchor="start" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">Real, but a classroom fact.</text>
<text x="336.0" y="435.0" font-family="Helvetica, Arial, sans-serif" font-size="9.7" fill="#6b82a0" text-anchor="start" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">Proves capability under</text>
<text x="336.0" y="448.0" font-family="Helvetica, Arial, sans-serif" font-size="9.7" fill="#6b82a0" text-anchor="start" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">observation, not conduct on a</text>
<text x="336.0" y="461.0" font-family="Helvetica, Arial, sans-serif" font-size="9.7" fill="#6b82a0" text-anchor="start" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">Tuesday ward round.</text>
<rect x="320.0" y="522.0" width="200.0" height="38.0" rx="7" fill="#0f1b2d" stroke="#1e2d45" stroke-width="1" fill-opacity="1.0"/>
<text x="420.0" y="540.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.2" fill="#f59e0b" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">KNOWS · KNOWS HOW ·</text>
<text x="420.0" y="552.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.2" fill="#f59e0b" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">SHOWS HOW</text>
<rect x="536.0" y="232.0" width="200.0" height="274.0" rx="10" fill="#111c30" stroke="#00d4f5" stroke-width="1.6" fill-opacity="1.0"/>
<rect x="536" y="232" width="200" height="4" rx="2" fill="#00d4f5"/>
<text x="552.0" y="262.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11" fill="#00d4f5" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="1.4" fill-opacity="1.0">LEVEL 3</text>
<text x="552.0" y="286.0" font-family="Helvetica, Arial, sans-serif" font-size="17" fill="#c9d6e8" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0.6" fill-opacity="1.0">BEHAVIOUR</text>
<text x="552.0" y="307.0" font-family="Helvetica, Arial, sans-serif" font-size="11.8" fill="#00d4f5" text-anchor="start" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">Do they do it at work?</text>
<text x="552.0" y="332.0" font-family="Helvetica, Arial, sans-serif" font-size="9.9" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">Observation, chart audit,</text>
<text x="552.0" y="345.0" font-family="Helvetica, Arial, sans-serif" font-size="9.9" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">interaction logs.</text>
<line x1="552" y1="362" x2="720" y2="362" stroke="#1e2d45"/>
<text x="552.0" y="378.0" font-family="Helvetica, Arial, sans-serif" font-size="9.7" fill="#6b82a0" text-anchor="start" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">The first level that is about</text>
<text x="552.0" y="391.0" font-family="Helvetica, Arial, sans-serif" font-size="9.7" fill="#6b82a0" text-anchor="start" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">practice. Costly, awkward, and</text>
<text x="552.0" y="404.0" font-family="Helvetica, Arial, sans-serif" font-size="9.7" fill="#6b82a0" text-anchor="start" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">the point of the whole exercise.</text>
<rect x="536.0" y="522.0" width="200.0" height="38.0" rx="7" fill="#0f1b2d" stroke="#1e2d45" stroke-width="1" fill-opacity="1.0"/>
<text x="636.0" y="546.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.2" fill="#00d4f5" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">DOES</text>
<rect x="752.0" y="188.0" width="200.0" height="318.0" rx="10" fill="#111c30" stroke="#10b981" stroke-width="1.6" fill-opacity="1.0"/>
<rect x="752" y="188" width="200" height="4" rx="2" fill="#10b981"/>
<text x="768.0" y="218.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11" fill="#10b981" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="1.4" fill-opacity="1.0">LEVEL 4</text>
<text x="768.0" y="242.0" font-family="Helvetica, Arial, sans-serif" font-size="17" fill="#c9d6e8" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0.6" fill-opacity="1.0">RESULTS</text>
<text x="768.0" y="263.0" font-family="Helvetica, Arial, sans-serif" font-size="11.8" fill="#10b981" text-anchor="start" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">Did the patient benefit?</text>
<text x="768.0" y="288.0" font-family="Helvetica, Arial, sans-serif" font-size="9.9" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">Facility indicators, safety</text>
<text x="768.0" y="301.0" font-family="Helvetica, Arial, sans-serif" font-size="9.9" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">incidents, escalation times.</text>
<line x1="768" y1="318" x2="936" y2="318" stroke="#1e2d45"/>
<text x="768.0" y="334.0" font-family="Helvetica, Arial, sans-serif" font-size="9.7" fill="#6b82a0" text-anchor="start" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">What everybody claims and almost</text>
<text x="768.0" y="347.0" font-family="Helvetica, Arial, sans-serif" font-size="9.7" fill="#6b82a0" text-anchor="start" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">nobody measures. Requires a</text>
<text x="768.0" y="360.0" font-family="Helvetica, Arial, sans-serif" font-size="9.7" fill="#6b82a0" text-anchor="start" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">design, agreed before you start.</text>
<rect x="752.0" y="522.0" width="200.0" height="38.0" rx="7" fill="#0f1b2d" stroke="#1e2d45" stroke-width="1" fill-opacity="1.0"/>
<text x="852.0" y="540.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.2" fill="#10b981" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">PATIENT &amp; SYSTEM</text>
<text x="852.0" y="552.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.2" fill="#10b981" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">OUTCOMES</text>
<text x="90.0" y="542.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.5" fill="#6b82a0" text-anchor="end" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">MILLER</text>
<text x="90.0" y="554.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.5" fill="#6b82a0" text-anchor="end" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">level</text>
<path d="M104,598 L942,598" stroke="#6b82a0" stroke-width="1.6" marker-end="url(#ld-a)"/>
<text x="108.0" y="618.0" font-family="Helvetica, Arial, sans-serif" font-size="10.2" fill="#6b82a0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">cheap · fast · nearly meaningless</text>
<text x="936.0" y="618.0" font-family="Helvetica, Arial, sans-serif" font-size="10.2" fill="#10b981" text-anchor="end" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">expensive · slow · the only evidence worth having</text>
<path d="M506,208 L538,208" stroke="#f87171" stroke-width="2.2" stroke-dasharray="5 4" marker-end="url(#ld-r)"/>
<text x="522.0" y="196.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10" fill="#f87171" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">THE GAP WHERE MOST PROGRAMMES STOP</text>
</svg>
<figcaption>The four levels as a staircase. Each step costs more to climb than the one below it, in money, in time, and in the number of people whose cooperation you need. Underneath each is the corresponding level of Miller's pyramid — the standard way clinical educators describe what an assessment is actually evidence <em>of</em>.</figcaption>
</figure>

<div class="kp-callout">
<strong>The single most important thing to understand about the levels.</strong> They are not a quality ranking of <em>evidence</em>. They are a ranking of <em>what question you are entitled to answer</em>. A beautifully conducted Level 2 study is excellent evidence about Level 2 and no evidence at all about Level 3. The commonest error in medical education — and I have made it myself — is to run a rigorous Level 2 assessment and then write a discussion section about practice change.
</div>

### 1.3 Why almost everybody stops at two

Because levels 1 and 2 happen in the room, while you still have everyone's attention and a budget line, and levels 3 and 4 happen somewhere else, months later, after the funder's report is due.

Level 1 costs a sheet of paper. Level 2 costs an exam and someone to mark it. Level 3 costs a trained observer travelling to a facility, an ethics approval, a data-sharing agreement, a clinician's afternoon, and a statistician. Level 4 costs all of that plus a study design agreed before the intervention starts, which means you have to have been thinking about evaluation at the moment you were most excited about the teaching.

That asymmetry — not laziness, not dishonesty — is why the literature on educational interventions is a very tall pile of Level 2 studies. It is also why any institution that intends to do better has to write the commitment down *in advance*, in a founding document, where breaking it requires a public argument. Hence commitment ten.

### 1.4 The 2016 update: plan backwards, and build the drivers

In 2016 James and Wendy Kirkpatrick published what they call the **New World Kirkpatrick Model**, and it fixed the two things that were most often got wrong.

**Plan backwards.** Do not design a course and then wonder how to evaluate it. Choose the Level 4 result you are trying to move, define the Level 3 behaviours that would plausibly move it, define the Level 2 capabilities those behaviours require, and only then write the curriculum. Evaluation stops being an appendix and becomes the design brief.

**Build the required drivers.** This is the more useful of the two. The New World model names the thing that sits *between* Level 2 and Level 3 — the reinforcement, encouragement, reward and monitoring in the workplace without which a trained capability simply never becomes a habit. If you teach a clinician something on Friday and nobody on the ward ever mentions it again, you have not built a behaviour. You have built a memory, and memories decay.

<figure class="kp-fig">
<svg viewBox="0 0 940 470" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Backwards design: the Level 4 patient outcome is chosen first and the curriculum derived from it, while evidence and causal claims travel in the opposite direction, with the four required drivers shown underneath">
<defs><marker id="bw-g" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L9,5 L0,10 z" fill="#10b981"/></marker><marker id="bw-c" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L9,5 L0,10 z" fill="#00d4f5"/></marker></defs>
<rect x="0.0" y="0.0" width="940.0" height="470.0" rx="14" fill="#0d1424" stroke="#182742" stroke-width="1" fill-opacity="1.0"/>
<text x="470.0" y="36.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="15" fill="#c9d6e8" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="1.4" fill-opacity="1.0">DESIGN RUNS RIGHT TO LEFT. EVIDENCE RUNS LEFT TO RIGHT.</text>
<text x="470.0" y="57.0" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">you choose the Level 4 indicator first, then work backwards to what you teach on Monday morning</text>
<rect x="46.0" y="130.0" width="196.0" height="150.0" rx="11" fill="#111c30" stroke="#00d4f5" stroke-width="1.6" fill-opacity="1.0"/>
<rect x="46" y="130" width="196" height="4" rx="2" fill="#00d4f5"/>
<text x="60.0" y="158.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11" fill="#00d4f5" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="1.3" fill-opacity="1.0">CURRICULUM</text>
<text x="60.0" y="182.0" font-family="Helvetica, Arial, sans-serif" font-size="13.5" fill="#c9d6e8" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">What we teach</text>
<text x="60.0" y="200.0" font-family="Helvetica, Arial, sans-serif" font-size="13.5" fill="#c9d6e8" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">on Monday morning</text>
<text x="60.0" y="230.0" font-family="Helvetica, Arial, sans-serif" font-size="9.6" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">the independent-impression</text>
<text x="60.0" y="243.0" font-family="Helvetica, Arial, sans-serif" font-size="9.6" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">rule; naming the modality;</text>
<text x="60.0" y="256.0" font-family="Helvetica, Arial, sans-serif" font-size="9.6" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">error drills</text>
<path d="M248,205 L270,205" stroke="#00d4f5" stroke-width="2.4" marker-end="url(#bw-c)"/>
<rect x="276.0" y="130.0" width="196.0" height="150.0" rx="11" fill="#111c30" stroke="#00d4f5" stroke-width="1.6" fill-opacity="1.0"/>
<rect x="276" y="130" width="196" height="4" rx="2" fill="#00d4f5"/>
<text x="290.0" y="158.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11" fill="#00d4f5" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="1.3" fill-opacity="1.0">LEVEL 2</text>
<text x="290.0" y="182.0" font-family="Helvetica, Arial, sans-serif" font-size="13.5" fill="#c9d6e8" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">What they can do</text>
<text x="290.0" y="200.0" font-family="Helvetica, Arial, sans-serif" font-size="13.5" fill="#c9d6e8" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">under observation</text>
<text x="290.0" y="230.0" font-family="Helvetica, Arial, sans-serif" font-size="9.6" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">AI-OSCE with a seeded error;</text>
<text x="290.0" y="243.0" font-family="Helvetica, Arial, sans-serif" font-size="9.6" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">conjunctive pass on detection</text>
<path d="M478,205 L500,205" stroke="#00d4f5" stroke-width="2.4" marker-end="url(#bw-c)"/>
<rect x="506.0" y="130.0" width="196.0" height="150.0" rx="11" fill="#111c30" stroke="#f59e0b" stroke-width="1.6" fill-opacity="1.0"/>
<rect x="506" y="130" width="196" height="4" rx="2" fill="#f59e0b"/>
<text x="520.0" y="158.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11" fill="#f59e0b" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="1.3" fill-opacity="1.0">LEVEL 3</text>
<text x="520.0" y="182.0" font-family="Helvetica, Arial, sans-serif" font-size="13.5" fill="#c9d6e8" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">What they actually do</text>
<text x="520.0" y="200.0" font-family="Helvetica, Arial, sans-serif" font-size="13.5" fill="#c9d6e8" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">in the workplace</text>
<text x="520.0" y="230.0" font-family="Helvetica, Arial, sans-serif" font-size="9.6" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">observed encounters, chart</text>
<text x="520.0" y="243.0" font-family="Helvetica, Arial, sans-serif" font-size="9.6" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">audit, interaction logs at 3</text>
<text x="520.0" y="256.0" font-family="Helvetica, Arial, sans-serif" font-size="9.6" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">and 12 months</text>
<path d="M708,205 L730,205" stroke="#00d4f5" stroke-width="2.4" marker-end="url(#bw-c)"/>
<rect x="736.0" y="130.0" width="196.0" height="150.0" rx="11" fill="#111c30" stroke="#10b981" stroke-width="1.6" fill-opacity="1.0"/>
<rect x="736" y="130" width="196" height="4" rx="2" fill="#10b981"/>
<text x="750.0" y="158.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11" fill="#10b981" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="1.3" fill-opacity="1.0">LEVEL 4</text>
<text x="750.0" y="182.0" font-family="Helvetica, Arial, sans-serif" font-size="13.5" fill="#c9d6e8" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">What changes</text>
<text x="750.0" y="200.0" font-family="Helvetica, Arial, sans-serif" font-size="13.5" fill="#c9d6e8" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">for the patient</text>
<text x="750.0" y="230.0" font-family="Helvetica, Arial, sans-serif" font-size="9.6" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">escalation time, documentation</text>
<text x="750.0" y="243.0" font-family="Helvetica, Arial, sans-serif" font-size="9.6" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">completeness, AI-contributed</text>
<text x="750.0" y="256.0" font-family="Helvetica, Arial, sans-serif" font-size="9.6" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">harm</text>
<path d="M912,104 L66,104" stroke="#10b981" stroke-width="3" stroke-dasharray="9 5" marker-end="url(#bw-g)"/>
<text x="470.0" y="94.0" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#10b981" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">PLANNING — start here, at the outcome you care about</text>
<text x="470.0" y="306.0" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#00d4f5" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">DELIVERY AND EVIDENCE — this is the direction the causal claim has to travel</text>
<rect x="46.0" y="336.0" width="848.0" height="96.0" rx="11" fill="#131f36" stroke="#a78bfa" stroke-width="1.6" fill-opacity="1.0"/>
<text x="66.0" y="362.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11.5" fill="#a78bfa" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="1.3" fill-opacity="1.0">REQUIRED DRIVERS</text>
<text x="66.0" y="380.0" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">the reinforcement that sits under Level 3 — without it, Level 2 never becomes Level 3</text>
<circle cx="72.0" cy="398" r="3.4" fill="#a78bfa"/>
<text x="82.0" y="402.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.8" fill="#a78bfa" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">REINFORCE</text>
<text x="82.0" y="416.0" font-family="Helvetica, Arial, sans-serif" font-size="9" fill="#6b82a0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">pocket card, sandbox prompt,</text>
<text x="82.0" y="427.0" font-family="Helvetica, Arial, sans-serif" font-size="9" fill="#6b82a0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">ward round question</text>
<circle cx="274.0" cy="398" r="3.4" fill="#a78bfa"/>
<text x="284.0" y="402.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.8" fill="#a78bfa" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">ENCOURAGE</text>
<text x="284.0" y="416.0" font-family="Helvetica, Arial, sans-serif" font-size="9" fill="#6b82a0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">named senior who asks about it</text>
<text x="284.0" y="427.0" font-family="Helvetica, Arial, sans-serif" font-size="9" fill="#6b82a0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">and means it</text>
<circle cx="476.0" cy="398" r="3.4" fill="#a78bfa"/>
<text x="486.0" y="402.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.8" fill="#a78bfa" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">REWARD</text>
<text x="486.0" y="416.0" font-family="Helvetica, Arial, sans-serif" font-size="9" fill="#6b82a0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">counts for CPD points and</text>
<text x="486.0" y="427.0" font-family="Helvetica, Arial, sans-serif" font-size="9" fill="#6b82a0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">appraisal, visibly</text>
<circle cx="678.0" cy="398" r="3.4" fill="#a78bfa"/>
<text x="688.0" y="402.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.8" fill="#a78bfa" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">MONITOR</text>
<text x="688.0" y="416.0" font-family="Helvetica, Arial, sans-serif" font-size="9" fill="#6b82a0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">audit that somebody actually</text>
<text x="688.0" y="427.0" font-family="Helvetica, Arial, sans-serif" font-size="9" fill="#6b82a0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">reads and returns</text>
</svg>
<figcaption>Design runs right to left; evidence runs left to right. You choose the patient-level outcome first and derive the curriculum from it, but the causal claim has to travel the other way, through each stage, and each arrow is a place where it can fail. Underneath, the four required drivers — the reinforcement without which Level 2 never becomes Level 3.</figcaption>
</figure>

<div class="kp-key">
For our purposes the required drivers are not a footnote. My honest expectation is that the drivers will turn out to matter more than the curriculum. Two facilities receiving identical teaching, one of which has a consultant who asks "what did you think before you asked it?" on every ward round and one of which does not, will produce different Level 3 data — and the difference will have nothing to do with the course.
</div>

### 1.5 The criticisms, which are serious and which I accept

I would not want to build an institution on a 1959 industrial training model without saying plainly what is wrong with it.

**It smuggles in a causal chain that may not exist.** The levels are usually presented as a hierarchy in which each level causes the next. There is no strong empirical basis for that. Someone can change behaviour without having scored well on the test, and can score well without changing anything. Treating the hierarchy as a causal ladder is an assumption, not a finding.

**It was built for simple interventions with short endpoints.** [Yardley and Dornan's 2012 critique in *Medical Education*](https://asmepublications.onlinelibrary.wiley.com/doi/10.1111/j.1365-2923.2011.04076.x) is the one to read. Their conclusion is uncomfortable and, I think, correct: the levels carry so many implicit assumptions that they suit only relatively simple instructional designs, short-term endpoints, and beneficiaries other than the learner — conditions met by perhaps a fifth of medical education evidence reviews. Applied outside those conditions as a critical-appraisal tool, the hierarchy adds little and can actively mislead.

**It treats the learner as a means.** Level 4 is defined as benefit to the organisation. A clinician who becomes a better, more sceptical thinker has gained something the model has no box for.

So why use it? Because it is a shared vocabulary that a hospital board, a professional council, a funder and a clinician-educator can all read without a glossary — and because the specific failure it was invented to prevent (declaring victory on the strength of a happy sheet) is precisely the failure most likely to occur here. I use it as a **checklist against self-deception**, not as a theory of learning. Where it does not fit, I would say so in the evaluation report rather than force the data into it.

### 1.6 Two extensions worth knowing

Two adaptations are standard in health professions education and both improve on the original for our purposes.

**Barr, Freeth and Hammick's split levels**, developed for interprofessional education, subdivide two of the four: Level 2a (modification of attitudes and perceptions) and 2b (acquisition of knowledge and skills); Level 4a (change in organisational practice) and 4b (benefit to patients). Given commitment eight — [interprofessional wherever the work is interprofessional](/post/2026-08-05-another-arrow-in-the-quiver#the-pedagogy-i-would-insist-on) — this split is the one I would actually adopt. Attitude towards AI and skill with AI are different things and they can move in opposite directions. So can organisational practice and patient benefit.

**[Moore's expanded outcomes framework](https://www.tandfonline.com/doi/full/10.1080/10401334.2021.1950540)** stretches the four into seven for continuing medical education: participation, satisfaction, learning (declarative and procedural), competence, performance, patient health, community health. Its virtue is the explicit gap it opens between **competence** (level 5's neighbour — can do, in a controlled setting) and **performance** (does do, in practice). That gap is exactly where the AI-OSCE ends and workplace assessment begins, and CPD frameworks in several jurisdictions are built on it.

<div class="kp-note">
<strong>Vocabulary, once, so the rest of this post is unambiguous.</strong><br>
<strong>Competence</strong> — what a clinician can do when they know they are being assessed. Measured by examination and simulation. Kirkpatrick 2. Miller's <em>shows how</em>.<br>
<strong>Performance</strong> — what a clinician does when nobody has told them it counts. Measured in the workplace. Kirkpatrick 3. Miller's <em>does</em>.<br>
The distance between them is not a defect in the assessment. It is a real and permanent feature of professional practice, and the entire argument of this post is that you have to go and measure it rather than assume it away.
</div>

---

## Part 2 — Applying this to student-clinicians: levels 1 and 2

From here on, everything is concrete. The cohort I have in mind is a group of student-clinicians and early-career clinicians — medical officers, clinical officers, nurses and midwives — completing Level 1 of the Institute's [common core](/post/2026-08-05-another-arrow-in-the-quiver), the module that teaches the [Clinical 4Ds](/post/2026-08-10-borrowed-from-an-art-school): Delegation, Description, Discernment and Diligence.

### 2.1 Level 1 — what we collect, and the one thing it is good for

We collect reaction data. We collect it on the day, it takes four minutes, and we largely ignore it. But "largely" is not "entirely", and it is worth being precise about the exception, because the blanket dismissal of Level 1 is its own kind of sloppiness.

**What reaction data cannot tell you:** whether anything was learned, whether anything changed, or whether the teaching was any good. Learner satisfaction and learning outcome are weakly and sometimes inversely related. Effortful teaching that produces durable learning frequently feels worse in the room than fluent teaching that produces nothing — the well-documented gap between how well people think they are learning and how well they actually are.

**What it can tell you:** whether something was *broken*. A room where nobody could hear. A simulation that crashed. A facilitator who was hostile. Those are real, actionable, and invisible in the exam data. So the form we would use has almost nothing on it about enjoyment and four questions of the New World "relevance and commitment" type:

- What is one thing you will do differently on your next shift?
- What is one thing that will make that difficult?
- Was there anything in the two days you could not follow?
- Was there anything that did not work — room, kit, sandbox, materials?

Question one is a free-text field that turns into a Level 3 hypothesis. Question two is a free-text field that turns into a required-driver specification. Neither is a satisfaction score.

<div class="kp-warn">
<strong>The rule I would enforce.</strong> No Level 1 result ever appears in a report, a board paper, or a funding application as evidence of effect. Not once, not with a caveat. The moment "97% of participants rated the course highly" is permitted into an outcome section, commitment ten is dead, because that sentence is always available and always cheaper than the truth.
</div>

### 2.2 Level 2 — what "learning" means when the thing taught is a habit of mind

Level 2 is where most of the Institute's assessment machinery lives, and I have written about the two hardest parts of it elsewhere: [what an AI-OSCE is and why one station hides a deliberate error](/post/2026-08-11-one-hidden-error), and [how the pass mark is set by a modified Angoff panel rather than an arbitrary 50%](/post/2026-08-12-the-angoff-panel-for-testing-clinicians). I will not repeat those here. What matters for the present argument is the shape of the claim a Level 2 pass licenses.

The Institute's Level 2 evidence has three components:

**A 40-item invigilated knowledge test**, weighted 40% towards Discernment, with a cut score set by panel. This establishes *knows* and, for the reasoning items, *knows how*.

**An AI-OSCE**, in which the candidate consults with a standardised patient while an AI system is available in the sandbox, and in which some stations seed a clinical error into the AI's output. Scored on delegation, description, error detection and correction, and documentation and disclosure. Error detection is a **conjunctive** requirement — you cannot pass by compensating elsewhere, in the same way a candidate cannot compensate for a fatal drug error with excellent communication. This establishes *shows how*.

**A countersigned portfolio product** — a logbook, a critique of a real AI-assisted decision, a taught session — read and signed by a named senior person, per [commitment seven](/post/2026-08-05-another-arrow-in-the-quiver#the-pedagogy-i-would-insist-on).

<div class="kp-key">
<strong>What a Level 2 pass entitles us to say:</strong> this candidate, on a specified day, in a simulated encounter, in the knowledge that they were being assessed, detected a seeded error and documented it appropriately.<br><br>
<strong>What it does not entitle us to say:</strong> anything whatsoever about what they will do at 3 a.m. in a busy casualty department in eight months' time, when the model is fluent and confident and they are tired and the queue is thirty deep.
</div>

That second paragraph is the whole reason Level 3 exists, and it is not a hypothetical worry. The [2025 NEJM AI randomised trial](https://ai.nejm.org/doi/full/10.1056/AIoa2501001) that motivated the entire blueprint found physicians who had already completed twenty hours of AI-literacy training still deferring to deliberately erroneous model output. Those physicians would, I have no doubt, have passed a knowledge test on automation bias. The knowledge was not the binding constraint. That is a Level 2/Level 3 dissociation, observed directly, in exactly our population, on exactly our topic.

---

## Part 3 — Level 3, in operational detail

Here is what the blueprint says, in full, and what the rest of this section unpacks:

> **Level 3 — behaviour.** At three and twelve months post-training: workplace-based assessment by a trained observer; chart audit for documentation of AI-assisted decisions; and, with consent and appropriate governance, sandbox interaction logs showing whether the independent-impression rule survived contact with real work. My working hypothesis — which I would want tested and would not be surprised to see refuted — is that the independent-impression discipline decays fastest and needs the earliest booster.

Four claims are packed into that paragraph: a set of target behaviours, a schedule, three data sources, and a falsifiable hypothesis. Take them in order.

### 3.1 First, name the behaviours — or you are not measuring anything

You cannot measure "behaviour". You can only measure *specified behaviours*, and specifying them is most of the work. A Level 3 plan that says "we will assess whether they apply their learning" is not a plan; it is a sentence that sounds like a plan.

Here are the four I would specify, in descending order of how much I care about them.

**B1 — The independent-impression rule.** *Before opening the model on a diagnostic question, the clinician forms and records their own working impression.* This is the load-bearing behaviour of the entire curriculum, so it is worth being exact about why.

Automation bias is not principally a failure of knowledge. It is an anchoring effect. Once a fluent, confident, well-formatted differential is on the screen, the clinician's own reasoning is no longer independent of it — it is a revision of it. Every subsequent thought is conducted in the model's frame. [The systematic review by Goddard, Roudsari and Wyatt](https://academic.oup.com/jamia/article-abstract/19/1/121/732254) puts automation bias errors at roughly 6–11% of cases in decision-support studies, in both directions: errors of *commission* (following incorrect advice) and errors of *omission* (failing to act because the system did not prompt). Commission errors, they found, arise from a combination of not attending to available contradictory information and a belief in the superior judgement of the automated aid.

The rule is the countermeasure, and it works by sequence rather than by effort. It does not ask the clinician to be more sceptical, which is not a thing a person can reliably do on demand. It asks them to **commit to a position before the anchor arrives**, which converts an unfalsifiable intention into an observable act with a timestamp. That is precisely what makes it measurable — and it is why I would put it first.

**B2 — Naming the modality.** *Before delegating, the clinician can say which of automation, augmentation or agency they are operating in.* Almost every serious failure mode I can construct involves someone operating in agency mode while believing they are in augmentation mode. Twenty minutes of teaching; disproportionate yield.

**B3 — Documentation and disclosure.** *Where AI materially contributed to a clinical decision, the record says so, says how, and says what the clinician did about it.* This is also the behaviour with the clearest legal and governance load — see [The Law Is Part of the Architecture](/post/2026-08-01-the-law-is-part-of-the-architecture) for why, under the Digital Health Act and its data-governance requirements, this is not merely good manners.

**B4 — Escalation unchanged by model reassurance.** *A clinician who would have escalated on clinical grounds still escalates when the model is reassuring.* The hardest to observe and, if it fails, the one that kills someone.

<div class="kp-callout">
Notice that every one of these is written as an observable act with an actor, a trigger and a verb. "Demonstrates appropriate scepticism" is not on the list, because two trained observers cannot reliably agree on whether it happened. If you cannot write the behaviour in a form where two observers would agree, you cannot assess it, and you should either rewrite it or drop it. That constraint disciplines the curriculum as much as the evaluation.
</div>

### 3.2 The schedule, and why three and twelve

Three months and twelve months are not arbitrary, and they are not simply convenient.

The retention literature in procedural and resuscitation skills is reasonably consistent on shape even where it disagrees on magnitude. A [2021 systematic review of retention after simulation training](https://onlinelibrary.wiley.com/doi/10.1002/aet2.10536) found significant decline in performance scores as early as three months, with scores nonetheless remaining above baseline at three and six months — decay, then partial plateau, rather than a return to zero. The [advanced life support literature](https://www.resuscitationjournal.com/article/S0300-9572(12)00125-6/abstract) reports knowledge and skills decaying by six months to a year, with **skills decaying faster than knowledge**.

That last finding is the one I would generalise from, cautiously. If skills decay faster than knowledge in resuscitation, then in our setting the *procedural discipline* (do this before that) should decay faster than the *declarative content* (what a language model is). Three months is early enough to catch the first slope and still act on it. Twelve months tells you whether anything survived a year of real work, staff rotation, and a new model version. Six months would be better than nothing but is the least informative single point — it lands in the plateau, where the curve is flattest and least diagnostic.

<figure class="kp-fig">
<svg viewBox="0 0 940 560" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Hypothesised decay curves for four trained behaviours over twelve months, with measurement windows at three and twelve months, an acceptable-practice threshold, and a booster placed just after the three-month measurement">
<defs><marker id="dc-a" markerWidth="12" markerHeight="12" refX="9.5" refY="6" orient="auto" markerUnits="userSpaceOnUse"><path d="M1,1 L11,6 L1,11 z" fill="#10b981"/></marker><linearGradient id="dc-band" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#f87171" stop-opacity="0.16"/><stop offset="100%" stop-color="#f87171" stop-opacity="0.02"/></linearGradient></defs>
<rect x="0.0" y="0.0" width="940.0" height="560.0" rx="14" fill="#0d1424" stroke="#182742" stroke-width="1" fill-opacity="1.0"/>
<text x="470.0" y="36.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="16" fill="#c9d6e8" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="1.6" fill-opacity="1.0">WHAT LEVEL 3 IS LOOKING FOR — AND WHEN TO LOOK</text>
<text x="470.0" y="57.0" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">the hypothesis: the independent-impression rule decays fastest, so it needs the earliest booster</text>
<line x1="96" y1="78" x2="96" y2="416" stroke="#1e2d45" stroke-width="1.4"/>
<line x1="96" y1="416" x2="806" y2="416" stroke="#1e2d45" stroke-width="1.4"/>
<line x1="96" y1="416.0" x2="796" y2="416.0" stroke="#1e2d45" stroke-opacity="0.55" stroke-dasharray="3 5"/>
<text x="86.0" y="420.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.5" fill="#6b82a0" text-anchor="end" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">0</text>
<line x1="96" y1="333.5" x2="796" y2="333.5" stroke="#1e2d45" stroke-opacity="0.55" stroke-dasharray="3 5"/>
<text x="86.0" y="337.5" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.5" fill="#6b82a0" text-anchor="end" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">25</text>
<line x1="96" y1="251.0" x2="796" y2="251.0" stroke="#1e2d45" stroke-opacity="0.55" stroke-dasharray="3 5"/>
<text x="86.0" y="255.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.5" fill="#6b82a0" text-anchor="end" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">50</text>
<line x1="96" y1="168.5" x2="796" y2="168.5" stroke="#1e2d45" stroke-opacity="0.55" stroke-dasharray="3 5"/>
<text x="86.0" y="172.5" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.5" fill="#6b82a0" text-anchor="end" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">75</text>
<line x1="96" y1="86.0" x2="796" y2="86.0" stroke="#1e2d45" stroke-opacity="0.55" stroke-dasharray="3 5"/>
<text x="86.0" y="90.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.5" fill="#6b82a0" text-anchor="end" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">100</text>
<text x="44.0" y="120.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.6" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">% of</text>
<text x="44.0" y="133.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.6" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">encounters</text>
<text x="44.0" y="146.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.6" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">at standard</text>
<line x1="96.0" y1="416" x2="96.0" y2="422" stroke="#1e2d45"/>
<text x="96.0" y="438.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.6" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">end of</text>
<text x="96.0" y="450.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.6" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">course</text>
<line x1="271.0" y1="416" x2="271.0" y2="422" stroke="#1e2d45"/>
<text x="271.0" y="438.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.6" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">3 months</text>
<line x1="446.0" y1="416" x2="446.0" y2="422" stroke="#1e2d45"/>
<text x="446.0" y="438.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.6" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">6</text>
<line x1="621.0" y1="416" x2="621.0" y2="422" stroke="#1e2d45"/>
<text x="621.0" y="438.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.6" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">9</text>
<line x1="796.0" y1="416" x2="796.0" y2="422" stroke="#1e2d45"/>
<text x="796.0" y="438.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.6" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">12 months</text>
<rect x="96" y="218.0" width="700" height="198.0" fill="url(#dc-band)"/>
<line x1="96" y1="218.0" x2="796" y2="218.0" stroke="#f87171" stroke-width="1.6" stroke-dasharray="7 4"/>
<text x="104.0" y="210.0" font-family="Helvetica, Arial, sans-serif" font-size="9.8" fill="#f87171" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">acceptable-practice threshold (set in advance, not after)</text>
<polyline points="96.0,99.2 101.8,105.2 107.7,111.1 113.5,116.8 119.3,122.3 125.2,127.7 131.0,132.9 136.8,138.0 142.7,142.9 148.5,147.6 154.3,152.2 160.2,156.7 166.0,161.1 171.8,165.3 177.7,169.4 183.5,173.3 189.3,177.2 195.2,180.9 201.0,184.6 206.8,188.1 212.7,191.5 218.5,194.8 224.3,198.1 230.2,201.2 236.0,204.2 241.8,207.2 247.7,210.0 253.5,212.8 259.3,215.5 265.2,218.1 271.0,220.6 276.8,223.1 282.7,225.5 288.5,227.8 294.3,230.0 300.2,232.2 306.0,234.3 311.8,236.4 317.7,238.4 323.5,240.3 329.3,242.2 335.2,244.0 341.0,245.8 346.8,247.5 352.7,249.1 358.5,250.8 364.3,252.3 370.2,253.8 376.0,255.3 381.8,256.8 387.7,258.1 393.5,259.5 399.3,260.8 405.2,262.1 411.0,263.3 416.8,264.5 422.7,265.7 428.5,266.8 434.3,267.9 440.2,268.9 446.0,270.0 451.8,271.0 457.7,271.9 463.5,272.9 469.3,273.8 475.2,274.7 481.0,275.6 486.8,276.4 492.7,277.2 498.5,278.0 504.3,278.7 510.2,279.5 516.0,280.2 521.8,280.9 527.7,281.6 533.5,282.2 539.3,282.9 545.2,283.5 551.0,284.1 556.8,284.7 562.7,285.2 568.5,285.8 574.3,286.3 580.2,286.8 586.0,287.3 591.8,287.8 597.7,288.3 603.5,288.8 609.3,289.2 615.2,289.6 621.0,290.0 626.8,290.5 632.7,290.9 638.5,291.2 644.3,291.6 650.2,292.0 656.0,292.3 661.8,292.7 667.7,293.0 673.5,293.3 679.3,293.6 685.2,293.9 691.0,294.2 696.8,294.5 702.7,294.8 708.5,295.0 714.3,295.3 720.2,295.5 726.0,295.8 731.8,296.0 737.7,296.3 743.5,296.5 749.3,296.7 755.2,296.9 761.0,297.1 766.8,297.3 772.7,297.5 778.5,297.7 784.3,297.9 790.2,298.0 796.0,298.2" fill="none" stroke="#00d4f5" stroke-width="2.6" stroke-linecap="round"/>
<circle cx="796.0" cy="298.2" r="3.6" fill="#00d4f5"/>
<polyline points="96.0,99.2 101.8,101.3 107.7,103.4 113.5,105.4 119.3,107.4 125.2,109.3 131.0,111.3 136.8,113.2 142.7,115.1 148.5,116.9 154.3,118.7 160.2,120.5 166.0,122.3 171.8,124.0 177.7,125.7 183.5,127.4 189.3,129.0 195.2,130.6 201.0,132.2 206.8,133.8 212.7,135.3 218.5,136.9 224.3,138.4 230.2,139.8 236.0,141.3 241.8,142.7 247.7,144.1 253.5,145.5 259.3,146.9 265.2,148.2 271.0,149.5 276.8,150.8 282.7,152.1 288.5,153.3 294.3,154.6 300.2,155.8 306.0,157.0 311.8,158.2 317.7,159.3 323.5,160.5 329.3,161.6 335.2,162.7 341.0,163.8 346.8,164.9 352.7,165.9 358.5,166.9 364.3,168.0 370.2,169.0 376.0,170.0 381.8,170.9 387.7,171.9 393.5,172.8 399.3,173.8 405.2,174.7 411.0,175.6 416.8,176.4 422.7,177.3 428.5,178.2 434.3,179.0 440.2,179.8 446.0,180.7 451.8,181.5 457.7,182.2 463.5,183.0 469.3,183.8 475.2,184.5 481.0,185.3 486.8,186.0 492.7,186.7 498.5,187.4 504.3,188.1 510.2,188.8 516.0,189.5 521.8,190.1 527.7,190.8 533.5,191.4 539.3,192.1 545.2,192.7 551.0,193.3 556.8,193.9 562.7,194.5 568.5,195.1 574.3,195.7 580.2,196.2 586.0,196.8 591.8,197.3 597.7,197.9 603.5,198.4 609.3,198.9 615.2,199.4 621.0,199.9 626.8,200.4 632.7,200.9 638.5,201.4 644.3,201.9 650.2,202.3 656.0,202.8 661.8,203.2 667.7,203.7 673.5,204.1 679.3,204.5 685.2,205.0 691.0,205.4 696.8,205.8 702.7,206.2 708.5,206.6 714.3,207.0 720.2,207.4 726.0,207.8 731.8,208.1 737.7,208.5 743.5,208.9 749.3,209.2 755.2,209.6 761.0,209.9 766.8,210.2 772.7,210.6 778.5,210.9 784.3,211.2 790.2,211.5 796.0,211.8" fill="none" stroke="#f59e0b" stroke-width="2.6" stroke-linecap="round"/>
<circle cx="796.0" cy="211.8" r="3.6" fill="#f59e0b"/>
<polyline points="96.0,99.2 101.8,99.9 107.7,100.5 113.5,101.1 119.3,101.8 125.2,102.4 131.0,103.0 136.8,103.6 142.7,104.2 148.5,104.8 154.3,105.4 160.2,106.0 166.0,106.6 171.8,107.2 177.7,107.8 183.5,108.4 189.3,108.9 195.2,109.5 201.0,110.1 206.8,110.6 212.7,111.2 218.5,111.7 224.3,112.2 230.2,112.8 236.0,113.3 241.8,113.8 247.7,114.3 253.5,114.9 259.3,115.4 265.2,115.9 271.0,116.4 276.8,116.9 282.7,117.4 288.5,117.9 294.3,118.3 300.2,118.8 306.0,119.3 311.8,119.8 317.7,120.2 323.5,120.7 329.3,121.1 335.2,121.6 341.0,122.1 346.8,122.5 352.7,122.9 358.5,123.4 364.3,123.8 370.2,124.2 376.0,124.7 381.8,125.1 387.7,125.5 393.5,125.9 399.3,126.3 405.2,126.7 411.0,127.1 416.8,127.5 422.7,127.9 428.5,128.3 434.3,128.7 440.2,129.1 446.0,129.5 451.8,129.9 457.7,130.2 463.5,130.6 469.3,131.0 475.2,131.4 481.0,131.7 486.8,132.1 492.7,132.4 498.5,132.8 504.3,133.1 510.2,133.5 516.0,133.8 521.8,134.2 527.7,134.5 533.5,134.8 539.3,135.2 545.2,135.5 551.0,135.8 556.8,136.1 562.7,136.5 568.5,136.8 574.3,137.1 580.2,137.4 586.0,137.7 591.8,138.0 597.7,138.3 603.5,138.6 609.3,138.9 615.2,139.2 621.0,139.5 626.8,139.8 632.7,140.1 638.5,140.4 644.3,140.6 650.2,140.9 656.0,141.2 661.8,141.5 667.7,141.7 673.5,142.0 679.3,142.3 685.2,142.5 691.0,142.8 696.8,143.1 702.7,143.3 708.5,143.6 714.3,143.8 720.2,144.1 726.0,144.3 731.8,144.6 737.7,144.8 743.5,145.1 749.3,145.3 755.2,145.5 761.0,145.8 766.8,146.0 772.7,146.2 778.5,146.5 784.3,146.7 790.2,146.9 796.0,147.1" fill="none" stroke="#10b981" stroke-width="2.6" stroke-linecap="round"/>
<circle cx="796.0" cy="147.1" r="3.6" fill="#10b981"/>
<polyline points="96.0,99.2 101.8,99.3 107.7,99.5 113.5,99.6 119.3,99.8 125.2,99.9 131.0,100.1 136.8,100.2 142.7,100.4 148.5,100.5 154.3,100.7 160.2,100.8 166.0,100.9 171.8,101.1 177.7,101.2 183.5,101.4 189.3,101.5 195.2,101.6 201.0,101.8 206.8,101.9 212.7,102.0 218.5,102.2 224.3,102.3 230.2,102.4 236.0,102.6 241.8,102.7 247.7,102.8 253.5,103.0 259.3,103.1 265.2,103.2 271.0,103.4 276.8,103.5 282.7,103.6 288.5,103.8 294.3,103.9 300.2,104.0 306.0,104.1 311.8,104.3 317.7,104.4 323.5,104.5 329.3,104.6 335.2,104.8 341.0,104.9 346.8,105.0 352.7,105.1 358.5,105.2 364.3,105.4 370.2,105.5 376.0,105.6 381.8,105.7 387.7,105.8 393.5,106.0 399.3,106.1 405.2,106.2 411.0,106.3 416.8,106.4 422.7,106.6 428.5,106.7 434.3,106.8 440.2,106.9 446.0,107.0 451.8,107.1 457.7,107.2 463.5,107.3 469.3,107.5 475.2,107.6 481.0,107.7 486.8,107.8 492.7,107.9 498.5,108.0 504.3,108.1 510.2,108.2 516.0,108.3 521.8,108.4 527.7,108.5 533.5,108.7 539.3,108.8 545.2,108.9 551.0,109.0 556.8,109.1 562.7,109.2 568.5,109.3 574.3,109.4 580.2,109.5 586.0,109.6 591.8,109.7 597.7,109.8 603.5,109.9 609.3,110.0 615.2,110.1 621.0,110.2 626.8,110.3 632.7,110.4 638.5,110.5 644.3,110.6 650.2,110.7 656.0,110.8 661.8,110.9 667.7,111.0 673.5,111.1 679.3,111.2 685.2,111.3 691.0,111.3 696.8,111.4 702.7,111.5 708.5,111.6 714.3,111.7 720.2,111.8 726.0,111.9 731.8,112.0 737.7,112.1 743.5,112.2 749.3,112.3 755.2,112.4 761.0,112.4 766.8,112.5 772.7,112.6 778.5,112.7 784.3,112.8 790.2,112.9 796.0,113.0" fill="none" stroke="#a78bfa" stroke-width="2.6" stroke-linecap="round"/>
<circle cx="796.0" cy="113.0" r="3.6" fill="#a78bfa"/>
<rect x="256.0" y="78" width="30" height="338" fill="#c9d6e8" fill-opacity="0.05" stroke="#c9d6e8" stroke-opacity="0.18"/>
<text x="271.0" y="70.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#c9d6e8" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">MEASURE</text>
<rect x="781.0" y="78" width="30" height="338" fill="#c9d6e8" fill-opacity="0.05" stroke="#c9d6e8" stroke-opacity="0.18"/>
<text x="796.0" y="70.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#c9d6e8" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">MEASURE</text>
<path d="M411.0,356.6 L297.2,247.7" stroke="#10b981" stroke-width="2.2" marker-end="url(#dc-a)"/>
<text x="428.5" y="360.6" font-family="Helvetica, Arial, sans-serif" font-size="10.2" fill="#10b981" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">booster here — 45 minutes, one seeded-error case, not a repeat of the course</text>
<text x="96.0" y="474.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10" fill="#c9d6e8" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="1.2" fill-opacity="1.0">WHAT DECAYS, FASTEST FIRST</text>
<line x1="96" y1="490" x2="122" y2="490" stroke="#00d4f5" stroke-width="2.8"/>
<text x="130.0" y="494.0" font-family="Helvetica, Arial, sans-serif" font-size="10.4" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">Independent impression before opening the model</text>
<text x="696.0" y="494.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.6" fill="#00d4f5" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">half-life ≈ 2.3 months (hypothesised)</text>
<line x1="96" y1="507" x2="122" y2="507" stroke="#f59e0b" stroke-width="2.8"/>
<text x="130.0" y="511.0" font-family="Helvetica, Arial, sans-serif" font-size="10.4" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">Naming the modality — automation / augmentation / agency</text>
<text x="696.0" y="511.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.6" fill="#f59e0b" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">half-life ≈ 4.3 months (hypothesised)</text>
<line x1="96" y1="524" x2="122" y2="524" stroke="#10b981" stroke-width="2.8"/>
<text x="130.0" y="528.0" font-family="Helvetica, Arial, sans-serif" font-size="10.4" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">Documenting that AI was used, and how</text>
<text x="696.0" y="528.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.6" fill="#10b981" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">half-life ≈ 7.7 months (hypothesised)</text>
<line x1="96" y1="541" x2="122" y2="541" stroke="#a78bfa" stroke-width="2.8"/>
<text x="130.0" y="545.0" font-family="Helvetica, Arial, sans-serif" font-size="10.4" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">Factual knowledge of what the model is</text>
<text x="696.0" y="545.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.6" fill="#a78bfa" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">half-life ≈ 15.4 months (hypothesised)</text>
</svg>
<figcaption>The hypothesis, drawn. These curves are <strong>illustrative and not data</strong> — they are what commitment ten predicts, laid out so that it can be checked. If the real curves come back in a different order, the hypothesis is wrong and the booster goes somewhere else. The dashed line is the acceptable-practice threshold, which has to be set before the first measurement rather than drawn around whatever we happen to find.</figcaption>
</figure>

### 3.3 Data source one — workplace-based assessment by a trained observer

**What it is.** A senior clinician sits in on a real consultation, watches, and completes a short structured form immediately afterwards, with feedback to the trainee. The two standard instruments are the **mini-CEX** (mini Clinical Evaluation Exercise, for whole encounters) and **DOPS** (Direct Observation of Procedural Skills, for procedures). Both are cheap, brief, and designed for repetition rather than perfection.

**How it would be adapted here.** A conventional mini-CEX form scores history, examination, professionalism, clinical judgement, organisation. Ours would add four domains mapped directly onto B1–B4, each with an anchored scale and each with a free-text justification field. The critical design decision is that **the observer records the sequence**, not just the quality: did the clinician form an impression before opening the model, or after? That is a binary with a timestamp, not a judgement call, and it is the single most valuable field on the form.

**How many, and why it matters.** This is where most workplace-based assessment schemes fall over, so the numbers deserve stating. A single mini-CEX is a very noisy measurement. Reliability accumulates across encounters and across assessors: work on the mini-CEX has reported reliability around 0.73 when aggregating roughly fifteen encounters, and the [composite reliability literature](https://link.springer.com/article/10.1007/s10459-013-9450-z) shows that a *portfolio* combining instruments gets there faster — a coefficient near 0.80 from a combination of mini-CEXs, DOPS and multi-source feedback rounds, with fewer of each than any single instrument would need alone. The practical implication for us is emphatic: **do not attempt to make a high-stakes judgement from one observation.** Aggregate.

**What contaminates it.** Three things, all documented, all worth designing against:

- **Hawthorne effect.** They behave well because you are watching. This is not a reason to abandon observation; it is a reason to read observation as a measure of *best-case* behaviour. If the independent-impression rule is not followed even when a consultant is sitting in the corner with a clipboard, you have learned something extremely important.
- **Assessor stringency.** In published analyses of mini-CEX score variance, examiner stringency has been found to account for a substantial share — around 29% in one dataset, against roughly 13% for the trainee's own aptitude for the attachment. Which is to say: *who assesses you can matter more than how good you are.* The mitigations are assessor training, multiple assessors per trainee, and never using a single assessor's score as a gate.
- **Case mix.** A straightforward case gives the trainee no reason to consult a model at all, and therefore no opportunity to demonstrate B1. The sampling frame has to specify diagnostic-uncertainty encounters, or the instrument measures nothing.

<div class="kp-note">
<strong>Operational note.</strong> I would specify: minimum eight observed encounters across the twelve months, at least four different assessors, at least six encounters flagged in advance as involving diagnostic uncertainty, all assessors having completed the faculty certification of <a href="/post/2026-08-05-another-arrow-in-the-quiver#the-pedagogy-i-would-insist-on" style="color:#00d4f5;">commitment nine</a> and having had at least one of their own observations observed. Assessor-level score distributions published internally each quarter, so that a systematically lenient or harsh assessor is visible without anyone having to make an accusation.
</div>

### 3.4 Data source two — chart audit

**What it is.** Structured retrospective review of the clinical record against explicit criteria. It is unobtrusive, it scales, it covers everyone rather than a sample of the willing, and it is the workhorse of quality measurement in health systems everywhere. It has been used to evaluate CME programmes precisely because it reaches Level 3 without requiring anyone to be observed — see, for example, [this study using chart review to evaluate a CME programme](https://pmc.ncbi.nlm.nih.gov/articles/PMC10548990/).

**What we would audit.** For each sampled encounter: is there a recorded working impression, and is it timestamped before the AI interaction? Is AI involvement documented at all? Is the nature of the contribution described? Where the model's output was not followed, is the reasoning recorded? Where a decision was escalated or not escalated, is the rationale there?

**How to do it without fooling yourself.** Chart audit is easy to do and easy to do badly. The design points that matter:

- **Specify the sampling frame before you look.** Consecutive encounters in defined windows, stratified by clinician and by presentation type. Not "cases the clinician chose to submit", which measures self-presentation.
- **Blind the auditors** to whether the clinician has completed training, and to the audit period, as far as the record permits.
- **Double-code a fraction** — 15–20% is conventional — and report inter-rater agreement with a chance-corrected statistic (Cohen's or Fleiss's kappa). An audit without a reported kappa is an opinion with a denominator.
- **Pilot the codebook** on twenty records and expect to rewrite half of it. Every ambiguity you find in the pilot is an ambiguity that would otherwise have become noise.

<div class="kp-warn">
<strong>The limitation that cannot be designed away.</strong> Chart audit measures documentation, not thought. A clinician who has completely surrendered their judgement to the model can write an impeccable note recording an independent impression they did not actually form. If documentation improves and observed behaviour does not, the honest interpretation is that we have taught documentation — and that is a real finding, and a curriculum problem, and it must not be reported as behaviour change.
</div>

### 3.5 Data source three — sandbox interaction logs

**What it is.** The Institute's teaching platform is model-agnostic by architecture, and its sandbox can record the sequence of interactions: what was asked, when, in what order, and what happened next. That makes it the only one of the three sources that directly observes **order of operations** — which, for B1, is the entire measurement.

**What it can establish.** Whether a working impression was entered before the first model query. Time-to-first-query from the start of the encounter. Whether the clinician queried again after receiving an answer, or accepted it. Whether outputs flagged as uncertain were treated differently from confident ones. These are behavioural traces of exactly the discipline we are trying to instil, collected without an observer in the room and therefore without a Hawthorne effect.

**What it must never become.** This is the point in the design where an evaluation turns into surveillance if nobody is paying attention, and I would want the constraints written into the founding instruments alongside the [independence rules](/post/2026-08-05-another-arrow-in-the-quiver):

- **Explicit, specific, revocable consent** to log analysis for evaluation, separate from consent to use the platform, and refusable without any effect on certification.
- **Purpose limitation in writing.** Logs are analysed for aggregate evaluation. They are not used for individual performance management, not shared with employers, and not admissible in a disciplinary process. If that undertaking cannot be given and kept, the logs should not be collected.
- **Minimisation and pseudonymisation** at the point of collection, with a retention period and a deletion date, consistent with the Digital Health Act's data-governance provisions and the Data Protection Act.
- **Governance approval and publication** of the analysis protocol before any analysis is run.

<div class="kp-callout">
A clinician who suspects the logs are being read by their employer will change their behaviour — and the behaviour they will adopt is <em>performing the ritual</em>: typing an impression they have not formed, because the system is watching. At that point the instrument has not merely stopped measuring the behaviour, it has actively destroyed it. Trust is not an ethical nicety here; it is a measurement precondition.
</div>

### 3.6 Triangulation — why three sources and not one

None of the three is trustworthy alone. Each is biased in a direction you can name in advance, and — this is the point — the directions do not coincide.

<figure class="kp-fig">
<svg viewBox="0 0 940 560" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Three Level 3 data sources — observed encounter, chart audit and sandbox interaction log — each with what it sees and the bias it carries, converging on a single defensible statement about behaviour">
<defs><marker id="tr-a" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L9,5 L0,10 z" fill="#6b82a0"/></marker></defs>
<rect x="0.0" y="0.0" width="940.0" height="560.0" rx="14" fill="#0d1424" stroke="#182742" stroke-width="1" fill-opacity="1.0"/>
<text x="470.0" y="36.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="15" fill="#c9d6e8" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="1.3" fill-opacity="1.0">NO SINGLE LEVEL 3 SOURCE IS TRUSTWORTHY. THREE, TRIANGULATED, ARE.</text>
<text x="470.0" y="57.0" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">each source is biased in a direction you can name in advance — which is what makes the combination usable</text>
<rect x="46.0" y="96.0" width="272.0" height="214.0" rx="11" fill="#111c30" stroke="#00d4f5" stroke-width="1.6" fill-opacity="1.0"/>
<rect x="46" y="96" width="272" height="4" rx="2" fill="#00d4f5"/>
<g transform="translate(74.0,130.0) scale(1.0)" stroke="#00d4f5" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="-8" y="-9" width="16" height="19" rx="2" fill="#00d4f5" fill-opacity="0.14"/><rect x="-3.5" y="-12" width="7" height="4" rx="1.2" fill="#00d4f5"/><path d="M-4.5,-3 L-2.5,-1 L1,-5" /><path d="M-4.5,3 L-2.5,5 L1,1" /></g>
<text x="98.0" y="128.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11.5" fill="#00d4f5" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0.8" fill-opacity="1.0">OBSERVED ENCOUNTER</text>
<text x="98.0" y="144.0" font-family="Helvetica, Arial, sans-serif" font-size="9.6" fill="#6b82a0" text-anchor="start" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">mini-CEX / DOPS, trained observer</text>
<line x1="60" y1="158" x2="304" y2="158" stroke="#1e2d45"/>
<text x="60.0" y="178.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#10b981" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">SEES</text>
<text x="60.0" y="194.0" font-family="Helvetica, Arial, sans-serif" font-size="10" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">Sees reasoning and disclosure. Nothing</text>
<text x="60.0" y="207.0" font-family="Helvetica, Arial, sans-serif" font-size="10" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">else does.</text>
<text x="60.0" y="232.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#f87171" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">MISSES / BIASED BY</text>
<text x="60.0" y="248.0" font-family="Helvetica, Arial, sans-serif" font-size="10" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">HAWTHORNE — they behave well because you</text>
<text x="60.0" y="261.0" font-family="Helvetica, Arial, sans-serif" font-size="10" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">are watching. Ceiling effects; observer</text>
<text x="60.0" y="274.0" font-family="Helvetica, Arial, sans-serif" font-size="10" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">stringency is a real variance component.</text>
<path d="M182.0,316 L182.0,352 L470.0,372 L470.0,396" fill="none" stroke="#00d4f5" stroke-width="2.2" stroke-opacity="0.7"/>
<rect x="348.0" y="96.0" width="272.0" height="214.0" rx="11" fill="#111c30" stroke="#f59e0b" stroke-width="1.6" fill-opacity="1.0"/>
<rect x="348" y="96" width="272" height="4" rx="2" fill="#f59e0b"/>
<g transform="translate(376.0,130.0) scale(1.0)" stroke="#f59e0b" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M-7,-10 H4 L8,-6 V10 H-7 Z" fill="#f59e0b" fill-opacity="0.14"/><path d="M4,-10 V-6 H8"/><path d="M-4,-2 H5 M-4,2 H5 M-4,6 H1"/><path d="M-9,8 L-3,8" stroke="#f59e0b" stroke-width="2"/></g>
<text x="400.0" y="128.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11.5" fill="#f59e0b" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0.8" fill-opacity="1.0">CHART AUDIT</text>
<text x="400.0" y="144.0" font-family="Helvetica, Arial, sans-serif" font-size="9.6" fill="#6b82a0" text-anchor="start" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">structured retrospective note review</text>
<line x1="362" y1="158" x2="606" y2="158" stroke="#1e2d45"/>
<text x="362.0" y="178.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#10b981" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">SEES</text>
<text x="362.0" y="194.0" font-family="Helvetica, Arial, sans-serif" font-size="10" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">Unobtrusive, cheap at scale, covers</text>
<text x="362.0" y="207.0" font-family="Helvetica, Arial, sans-serif" font-size="10" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">everyone.</text>
<text x="362.0" y="232.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#f87171" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">MISSES / BIASED BY</text>
<text x="362.0" y="248.0" font-family="Helvetica, Arial, sans-serif" font-size="10" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">Measures documentation, not thought. A</text>
<text x="362.0" y="261.0" font-family="Helvetica, Arial, sans-serif" font-size="10" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">clinician can write the right note after</text>
<text x="362.0" y="274.0" font-family="Helvetica, Arial, sans-serif" font-size="10" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">doing the wrong thing.</text>
<path d="M484.0,316 L484.0,352 L470.0,372 L470.0,396" fill="none" stroke="#f59e0b" stroke-width="2.2" stroke-opacity="0.7"/>
<rect x="650.0" y="96.0" width="272.0" height="214.0" rx="11" fill="#111c30" stroke="#10b981" stroke-width="1.6" fill-opacity="1.0"/>
<rect x="650" y="96" width="272" height="4" rx="2" fill="#10b981"/>
<g transform="translate(678.0,130.0) scale(1.0)" stroke="#10b981" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="-9" y="-8" width="18" height="16" rx="2" fill="#10b981" fill-opacity="0.14"/><path d="M-5.5,-4 L-2.5,-1 L-5.5,2"/><path d="M-0.5,3 H5"/><path d="M-9,-4.5 H9" stroke-opacity="0.4"/></g>
<text x="702.0" y="128.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11.5" fill="#10b981" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0.8" fill-opacity="1.0">SANDBOX INTERACTION LOG</text>
<text x="702.0" y="144.0" font-family="Helvetica, Arial, sans-serif" font-size="9.6" fill="#6b82a0" text-anchor="start" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">consented, governed, purpose-limited</text>
<line x1="664" y1="158" x2="908" y2="158" stroke="#1e2d45"/>
<text x="664.0" y="178.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#10b981" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">SEES</text>
<text x="664.0" y="194.0" font-family="Helvetica, Arial, sans-serif" font-size="10" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">The only source that sees the order of</text>
<text x="664.0" y="207.0" font-family="Helvetica, Arial, sans-serif" font-size="10" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">operations.</text>
<text x="664.0" y="232.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#f87171" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">MISSES / BIASED BY</text>
<text x="664.0" y="248.0" font-family="Helvetica, Arial, sans-serif" font-size="10" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">Consent and governance are not optional.</text>
<text x="664.0" y="261.0" font-family="Helvetica, Arial, sans-serif" font-size="10" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">Timestamps prove sequence, never</text>
<text x="664.0" y="274.0" font-family="Helvetica, Arial, sans-serif" font-size="10" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">understanding.</text>
<path d="M786.0,316 L786.0,352 L470.0,372 L470.0,396" fill="none" stroke="#10b981" stroke-width="2.2" stroke-opacity="0.7"/>
<rect x="170.0" y="402.0" width="600.0" height="74.0" rx="12" fill="#132339" stroke="#a78bfa" stroke-width="1.8" fill-opacity="1.0"/>
<text x="470.0" y="430.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12.5" fill="#a78bfa" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="1.2" fill-opacity="1.0">ONE DEFENSIBLE STATEMENT ABOUT BEHAVIOUR</text>
<text x="470.0" y="452.0" font-family="Helvetica, Arial, sans-serif" font-size="10.4" fill="#8ea4c0" text-anchor="middle" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">concordant across three sources with non-overlapping biases — or reported as discordant, which is itself a finding</text>
<rect x="46.0" y="494.0" width="848.0" height="78.0" rx="10" fill="#1a0f14" stroke="#f87171" stroke-width="1.4" fill-opacity="1.0"/>
<text x="66.0" y="518.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#f87171" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="1.2" fill-opacity="1.0">IF THE THREE DISAGREE</text>
<text x="66.0" y="538.0" font-family="Helvetica, Arial, sans-serif" font-size="10.4" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">do not average them. Ask which bias explains the gap — good notes with poor observed reasoning is a</text>
<text x="66.0" y="552.0" font-family="Helvetica, Arial, sans-serif" font-size="10.4" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">documentation-theatre signal, and a different curriculum problem entirely.</text>
</svg>
<figcaption>Three sources with non-overlapping biases. The observed encounter sees reasoning but is contaminated by being observed; the chart audit is unobtrusive but sees only what was written; the log sees sequence but never understanding. Agreement across all three is worth far more than a strong result from any one — and disagreement is itself informative, provided you resist the urge to average it away.</figcaption>
</figure>

The discipline this imposes is worth stating explicitly, because it is where evaluations usually go soft: **decide, before you collect anything, what you will conclude from each pattern of agreement and disagreement.** Write it down. Four cases:

| Observation | Chart | Log | Reasonable reading |
|---|---|---|---|
| Good | Good | Good | The behaviour is established. Report it, publish the effect size, and check again at twelve months. |
| Poor | Good | Poor | Documentation theatre. We have taught note-writing, not reasoning. Curriculum problem, and a serious one. |
| Good | Poor | Good | The behaviour exists; the record does not reflect it. A documentation and workflow problem — real, but a different fix. |
| Good | Good | Poor | Look hard at the log analysis before you believe it. Sandbox use may simply not reflect real workflow if clinicians have moved to a consumer tool on their own phone — which is itself the most important finding in the study. |

That last row deserves emphasis. If trained clinicians abandon the governed sandbox for an ungoverned consumer chatbot, every instrument above is measuring the wrong system, and the correct response is not a better log analysis but an urgent conversation about why the sanctioned tool lost.

### 3.7 The hypothesis, and what would refute it

The blueprint states a working hypothesis: **the independent-impression discipline decays fastest and needs the earliest booster.** I want to be precise about its status, because a hypothesis you cannot lose is not a hypothesis.

**The reasoning behind it.** B1 is procedural rather than declarative; procedural skills decay faster in the retention literature. It is also the behaviour with the highest immediate cost to the clinician — it takes thirty seconds *before* the shortcut, at the exact moment the shortcut is most tempting, and the pressure to skip it rises with queue length. And it is the least visible to colleagues: nobody can tell from the outside whether you formed an impression first, so social reinforcement is weak. Three independent reasons to expect fast decay.

**What would refute it.** If, at three months, the observed and logged rate of independent impression before first query is not significantly lower than at course exit — or is not lower than the corresponding rates for B2 and B3 — the hypothesis is wrong. It is also refuted, differently, if all four behaviours decay at indistinguishable rates, which would mean the specificity of the claim was unfounded and that boosters should be general rather than targeted.

**What we would do if refuted.** Move the booster. The point of a stated hypothesis is that being wrong is cheap and informative, provided you said it out loud first. Which is why it is in the blueprint rather than in a drawer.

<div class="kp-key">
<strong>On the booster itself.</strong> The correct response to decay is not to repeat the course. Repetition of the original material is the least efficient intervention available. The evidence on retention favours brief, spaced, effortful retrieval over massed re-teaching — the testing effect, which is one of the most robust findings in the learning sciences. So: 45 minutes, one seeded-error case, a required retrieval attempt before any teaching, feedback, done. Timed to land just after the three-month measurement, so that the measurement is uncontaminated and the intervention is still early enough to matter.
</div>

---

## Part 4 — Level 4, in operational detail

Again, the blueprint text in full:

> **Level 4 — results.** Facility-level indicators agreed in advance: documentation completeness, appropriate investigation rates, time-to-escalation for deteriorating patients, and incidents in which AI contributed to harm. Where we can run a stepped-wedge design across facilities, we should. Where we cannot, we should report the limitation honestly rather than implying causation from a before-and-after chart.

Three things are being committed to: indicators fixed in advance, a randomised design where feasible, and honesty about causation where it is not.

### 4.1 "Agreed in advance" is the load-bearing phrase

Everything else in that paragraph is technique. This is the part that determines whether the evaluation is worth anything.

If indicators are chosen after the data are in, you will choose the ones that moved. Not through dishonesty — through the ordinary human process of finding the favourable comparison more interesting than the unfavourable one, and of constructing a plausible story about why it was the right measure all along. The published literature on selective outcome reporting is unambiguous that this happens routinely in fields staffed by careful, well-intentioned people.

So: indicators, definitions, numerators, denominators, analysis method, subgroups and stopping rules, all written down and registered before the first facility is trained. Preferably published. If the pre-registered analysis produces a null result, the null result is the finding.

### 4.2 The four indicators, operationalised

Naming an indicator is not defining it. Each of the four needs a numerator, a denominator, a data source and an anticipated failure mode.

**Documentation completeness.**
*Numerator:* encounters in which AI involvement is documented with nature of contribution and clinician action. *Denominator:* encounters in which the interaction log shows an AI interaction occurred. *Source:* chart audit linked to sandbox log. *Failure mode:* the easiest indicator to move by exhortation alone, and therefore the weakest evidence of anything that matters. Treat a large improvement here with suspicion, not celebration.

**Appropriate investigation rates.**
*Numerator:* investigations ordered that meet pre-specified appropriateness criteria for the presentation. *Denominator:* all investigations ordered for that presentation. *Source:* chart audit against a criteria set agreed by a clinical panel before the study. *Failure mode:* "appropriate" is a judgement, and the panel that defines it is doing standard-setting — the same problem, with the same solution, as [setting a cut score](/post/2026-08-12-the-angoff-panel-for-testing-clinicians). Note also that this indicator is **directionally ambiguous**: AI can drive both over-investigation (defensive prompting on a long differential) and under-investigation (false reassurance). The pre-registration must state which direction constitutes improvement for which presentation, or the indicator is unfalsifiable.

**Time-to-escalation for deteriorating patients.**
*Numerator/measure:* median minutes from first recorded abnormal early-warning score to documented senior review. *Denominator:* patients meeting the deterioration trigger. *Source:* observation charts and clinical record. *Failure mode:* highly sensitive to staffing, bed state and time of day. Requires adjustment and adequate volume; in a small facility, a handful of night shifts can swing it.

**Incidents in which AI contributed to harm.**
*Numerator:* reported incidents where structured review judges AI to have contributed. *Denominator:* admissions or encounters. *Source:* incident reporting plus mortality and morbidity review. *Failure mode:* rare-event counting with a reporting rate that the intervention itself will change. Training people to notice AI-related harm will increase reported AI-related harm. **A rise in this indicator after training may be a success, not a failure**, and the pre-registration has to say so in advance, or the first honest facility will be punished for its honesty.

<div class="kp-callout">
<strong>Balancing measures.</strong> Any serious Level 4 set includes indicators that would detect the intervention doing harm. Ours: consultation duration (are we making every encounter slower?), clinician-reported cognitive load, referral rates (are we shifting risk upwards rather than managing it?), and — the one I would most want to see — whether sanctioned-tool use falls while overall AI use does not, which would mean we had driven the behaviour underground.
</div>

### 4.3 The stepped-wedge design

The attribution problem at Level 4 is severe. Facility indicators move for a hundred reasons — a new clinical officer, a drug stock-out, a change in referral patterns, a national guideline, a rainy season. A before-and-after comparison cannot distinguish any of that from your training.

A **stepped-wedge cluster randomised trial** is the design that fits this situation almost too well.

<figure class="kp-fig">
<svg viewBox="0 0 940 560" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A stepped-wedge design: five facilities across six periods, each crossing from control to trained in a randomised order, forming a staircase, with notes on why it works, what it costs and when it cannot be run">
<defs><marker id="sw-a" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9 z" fill="#10b981"/></marker></defs>
<rect x="0.0" y="0.0" width="940.0" height="560.0" rx="14" fill="#0d1424" stroke="#182742" stroke-width="1" fill-opacity="1.0"/>
<text x="470.0" y="36.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="15.5" fill="#c9d6e8" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="1.3" fill-opacity="1.0">THE STEPPED WEDGE — EVERYBODY GETS IT, IN A RANDOMISED ORDER</text>
<text x="470.0" y="57.0" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">the design that makes a rollout you were going to do anyway into evidence you can defend</text>
<text x="238.0" y="78.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.6" fill="#6b82a0" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">PERIOD 0</text>
<text x="238.0" y="92.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">baseline</text>
<text x="334.0" y="78.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.6" fill="#6b82a0" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">PERIOD 1</text>
<text x="334.0" y="92.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">month 3</text>
<text x="430.0" y="78.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.6" fill="#6b82a0" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">PERIOD 2</text>
<text x="430.0" y="92.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">month 6</text>
<text x="526.0" y="78.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.6" fill="#6b82a0" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">PERIOD 3</text>
<text x="526.0" y="92.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">month 9</text>
<text x="622.0" y="78.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.6" fill="#6b82a0" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">PERIOD 4</text>
<text x="622.0" y="92.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">month 12</text>
<text x="718.0" y="78.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.6" fill="#6b82a0" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">PERIOD 5</text>
<text x="718.0" y="92.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">month 15</text>
<text x="176.0" y="131.0" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#c9d6e8" text-anchor="end" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">Facility A</text>
<rect x="193.0" y="104.0" width="90.0" height="46.0" rx="6" fill="#0f2036" stroke="#00d4f5" stroke-width="1.3" fill-opacity="0.55"/>
<text x="238.0" y="131.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">control</text>
<rect x="289.0" y="104.0" width="90.0" height="46.0" rx="6" fill="#10321f" stroke="#10b981" stroke-width="1.3" fill-opacity="0.9"/>
<text x="334.0" y="131.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#10b981" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">TRAINED</text>
<rect x="385.0" y="104.0" width="90.0" height="46.0" rx="6" fill="#10321f" stroke="#10b981" stroke-width="1.3" fill-opacity="0.9"/>
<text x="430.0" y="131.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#10b981" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">TRAINED</text>
<rect x="481.0" y="104.0" width="90.0" height="46.0" rx="6" fill="#10321f" stroke="#10b981" stroke-width="1.3" fill-opacity="0.9"/>
<text x="526.0" y="131.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#10b981" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">TRAINED</text>
<rect x="577.0" y="104.0" width="90.0" height="46.0" rx="6" fill="#10321f" stroke="#10b981" stroke-width="1.3" fill-opacity="0.9"/>
<text x="622.0" y="131.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#10b981" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">TRAINED</text>
<rect x="673.0" y="104.0" width="90.0" height="46.0" rx="6" fill="#10321f" stroke="#10b981" stroke-width="1.3" fill-opacity="0.9"/>
<text x="718.0" y="131.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#10b981" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">TRAINED</text>
<path d="M289,100 L289,154" stroke="#f59e0b" stroke-width="2.6"/>
<text x="176.0" y="185.0" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#c9d6e8" text-anchor="end" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">Facility B</text>
<rect x="193.0" y="158.0" width="90.0" height="46.0" rx="6" fill="#0f2036" stroke="#00d4f5" stroke-width="1.3" fill-opacity="0.55"/>
<text x="238.0" y="185.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">control</text>
<rect x="289.0" y="158.0" width="90.0" height="46.0" rx="6" fill="#0f2036" stroke="#00d4f5" stroke-width="1.3" fill-opacity="0.55"/>
<text x="334.0" y="185.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">control</text>
<rect x="385.0" y="158.0" width="90.0" height="46.0" rx="6" fill="#10321f" stroke="#10b981" stroke-width="1.3" fill-opacity="0.9"/>
<text x="430.0" y="185.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#10b981" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">TRAINED</text>
<rect x="481.0" y="158.0" width="90.0" height="46.0" rx="6" fill="#10321f" stroke="#10b981" stroke-width="1.3" fill-opacity="0.9"/>
<text x="526.0" y="185.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#10b981" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">TRAINED</text>
<rect x="577.0" y="158.0" width="90.0" height="46.0" rx="6" fill="#10321f" stroke="#10b981" stroke-width="1.3" fill-opacity="0.9"/>
<text x="622.0" y="185.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#10b981" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">TRAINED</text>
<rect x="673.0" y="158.0" width="90.0" height="46.0" rx="6" fill="#10321f" stroke="#10b981" stroke-width="1.3" fill-opacity="0.9"/>
<text x="718.0" y="185.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#10b981" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">TRAINED</text>
<path d="M385,154 L385,208" stroke="#f59e0b" stroke-width="2.6"/>
<text x="176.0" y="239.0" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#c9d6e8" text-anchor="end" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">Facility C</text>
<rect x="193.0" y="212.0" width="90.0" height="46.0" rx="6" fill="#0f2036" stroke="#00d4f5" stroke-width="1.3" fill-opacity="0.55"/>
<text x="238.0" y="239.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">control</text>
<rect x="289.0" y="212.0" width="90.0" height="46.0" rx="6" fill="#0f2036" stroke="#00d4f5" stroke-width="1.3" fill-opacity="0.55"/>
<text x="334.0" y="239.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">control</text>
<rect x="385.0" y="212.0" width="90.0" height="46.0" rx="6" fill="#0f2036" stroke="#00d4f5" stroke-width="1.3" fill-opacity="0.55"/>
<text x="430.0" y="239.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">control</text>
<rect x="481.0" y="212.0" width="90.0" height="46.0" rx="6" fill="#10321f" stroke="#10b981" stroke-width="1.3" fill-opacity="0.9"/>
<text x="526.0" y="239.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#10b981" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">TRAINED</text>
<rect x="577.0" y="212.0" width="90.0" height="46.0" rx="6" fill="#10321f" stroke="#10b981" stroke-width="1.3" fill-opacity="0.9"/>
<text x="622.0" y="239.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#10b981" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">TRAINED</text>
<rect x="673.0" y="212.0" width="90.0" height="46.0" rx="6" fill="#10321f" stroke="#10b981" stroke-width="1.3" fill-opacity="0.9"/>
<text x="718.0" y="239.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#10b981" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">TRAINED</text>
<path d="M481,208 L481,262" stroke="#f59e0b" stroke-width="2.6"/>
<text x="176.0" y="293.0" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#c9d6e8" text-anchor="end" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">Facility D</text>
<rect x="193.0" y="266.0" width="90.0" height="46.0" rx="6" fill="#0f2036" stroke="#00d4f5" stroke-width="1.3" fill-opacity="0.55"/>
<text x="238.0" y="293.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">control</text>
<rect x="289.0" y="266.0" width="90.0" height="46.0" rx="6" fill="#0f2036" stroke="#00d4f5" stroke-width="1.3" fill-opacity="0.55"/>
<text x="334.0" y="293.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">control</text>
<rect x="385.0" y="266.0" width="90.0" height="46.0" rx="6" fill="#0f2036" stroke="#00d4f5" stroke-width="1.3" fill-opacity="0.55"/>
<text x="430.0" y="293.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">control</text>
<rect x="481.0" y="266.0" width="90.0" height="46.0" rx="6" fill="#0f2036" stroke="#00d4f5" stroke-width="1.3" fill-opacity="0.55"/>
<text x="526.0" y="293.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">control</text>
<rect x="577.0" y="266.0" width="90.0" height="46.0" rx="6" fill="#10321f" stroke="#10b981" stroke-width="1.3" fill-opacity="0.9"/>
<text x="622.0" y="293.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#10b981" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">TRAINED</text>
<rect x="673.0" y="266.0" width="90.0" height="46.0" rx="6" fill="#10321f" stroke="#10b981" stroke-width="1.3" fill-opacity="0.9"/>
<text x="718.0" y="293.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#10b981" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">TRAINED</text>
<path d="M577,262 L577,316" stroke="#f59e0b" stroke-width="2.6"/>
<text x="176.0" y="347.0" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#c9d6e8" text-anchor="end" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">Facility E</text>
<rect x="193.0" y="320.0" width="90.0" height="46.0" rx="6" fill="#0f2036" stroke="#00d4f5" stroke-width="1.3" fill-opacity="0.55"/>
<text x="238.0" y="347.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">control</text>
<rect x="289.0" y="320.0" width="90.0" height="46.0" rx="6" fill="#0f2036" stroke="#00d4f5" stroke-width="1.3" fill-opacity="0.55"/>
<text x="334.0" y="347.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">control</text>
<rect x="385.0" y="320.0" width="90.0" height="46.0" rx="6" fill="#0f2036" stroke="#00d4f5" stroke-width="1.3" fill-opacity="0.55"/>
<text x="430.0" y="347.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">control</text>
<rect x="481.0" y="320.0" width="90.0" height="46.0" rx="6" fill="#0f2036" stroke="#00d4f5" stroke-width="1.3" fill-opacity="0.55"/>
<text x="526.0" y="347.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">control</text>
<rect x="577.0" y="320.0" width="90.0" height="46.0" rx="6" fill="#0f2036" stroke="#00d4f5" stroke-width="1.3" fill-opacity="0.55"/>
<text x="622.0" y="347.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">control</text>
<rect x="673.0" y="320.0" width="90.0" height="46.0" rx="6" fill="#10321f" stroke="#10b981" stroke-width="1.3" fill-opacity="0.9"/>
<text x="718.0" y="347.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.4" fill="#10b981" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">TRAINED</text>
<path d="M673,316 L673,370" stroke="#f59e0b" stroke-width="2.6"/>
<path d="M289,104 L289,158 L385,158 L385,212 L481,212 L481,266 L577,266 L577,320 L673,320 L673,374" fill="none" stroke="#f59e0b" stroke-width="3" stroke-opacity="0.85"/>
<text x="780.0" y="360.0" font-family="Helvetica, Arial, sans-serif" font-size="11.5" fill="#f59e0b" text-anchor="start" font-weight="bold" font-style="italic" letter-spacing="0" fill-opacity="1.0">the wedge</text>
<rect x="46.0" y="408.0" width="272.0" height="116.0" rx="10" fill="#111c30" stroke="#10b981" stroke-width="1.4" fill-opacity="1.0"/>
<rect x="46.0" y="408" width="4" height="116" rx="2" fill="#10b981"/>
<text x="62.0" y="432.0" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#10b981" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">Why it works here</text>
<text x="62.0" y="452.0" font-family="Helvetica, Arial, sans-serif" font-size="9.7" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">Every facility is trained eventually,</text>
<text x="62.0" y="465.0" font-family="Helvetica, Arial, sans-serif" font-size="9.7" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">so nobody is denied the programme.</text>
<text x="62.0" y="478.0" font-family="Helvetica, Arial, sans-serif" font-size="9.7" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">Randomising the order — not the</text>
<text x="62.0" y="491.0" font-family="Helvetica, Arial, sans-serif" font-size="9.7" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">receipt — is what buys you the</text>
<text x="62.0" y="504.0" font-family="Helvetica, Arial, sans-serif" font-size="9.7" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">counterfactual.</text>
<rect x="334.0" y="408.0" width="272.0" height="116.0" rx="10" fill="#111c30" stroke="#f59e0b" stroke-width="1.4" fill-opacity="1.0"/>
<rect x="334.0" y="408" width="4" height="116" rx="2" fill="#f59e0b"/>
<text x="350.0" y="432.0" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#f59e0b" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">What it costs you</text>
<text x="350.0" y="452.0" font-family="Helvetica, Arial, sans-serif" font-size="9.7" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">Time and secular trend are confounded</text>
<text x="350.0" y="465.0" font-family="Helvetica, Arial, sans-serif" font-size="9.7" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">with the intervention, so the analysis</text>
<text x="350.0" y="478.0" font-family="Helvetica, Arial, sans-serif" font-size="9.7" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">must adjust for period. Contamination</text>
<text x="350.0" y="491.0" font-family="Helvetica, Arial, sans-serif" font-size="9.7" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">between facilities is a real and</text>
<text x="350.0" y="504.0" font-family="Helvetica, Arial, sans-serif" font-size="9.7" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">reportable risk.</text>
<rect x="622.0" y="408.0" width="272.0" height="116.0" rx="10" fill="#111c30" stroke="#f87171" stroke-width="1.4" fill-opacity="1.0"/>
<rect x="622.0" y="408" width="4" height="116" rx="2" fill="#f87171"/>
<text x="638.0" y="432.0" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#f87171" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">When you cannot run it</text>
<text x="638.0" y="452.0" font-family="Helvetica, Arial, sans-serif" font-size="9.7" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">Fewer than about four clusters, or a</text>
<text x="638.0" y="465.0" font-family="Helvetica, Arial, sans-serif" font-size="9.7" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">rollout order you do not control. Then</text>
<text x="638.0" y="478.0" font-family="Helvetica, Arial, sans-serif" font-size="9.7" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">say so, use segmented regression, and</text>
<text x="638.0" y="491.0" font-family="Helvetica, Arial, sans-serif" font-size="9.7" fill="#8ea4c0" text-anchor="start" font-weight="normal" font-style="normal" letter-spacing="0" fill-opacity="1.0">call it what it is.</text>
</svg>
<figcaption>Five facilities, six periods. Every facility begins as a control and every facility ends up trained; what is randomised is the <em>order</em>, not the receipt. Each facility acts as its own control before crossover, and contributes to the concurrent control group for the facilities that have not yet crossed. The staircase is the wedge.</figcaption>
</figure>

**Why it fits.** You are going to roll the programme out to every facility anyway — the Institute's whole purpose is national coverage. A parallel-arm trial would require withholding training from half the facilities indefinitely, which is neither politically nor ethically viable. The stepped wedge randomises only the sequence. Nobody is denied anything; they are asked to wait a defined and randomly allocated number of months. That is a very different conversation with a hospital superintendent, and it is the reason the design has become common in health systems research.

**What it costs you, honestly.** Time and treatment effect are confounded by construction, because later periods contain more trained facilities. The analysis must include a fixed effect for period, and it depends on the assumption that secular trends are common across clusters. It is also, as the [CONSORT extension for stepped-wedge trials](https://trialsjournal.biomedcentral.com/articles/10.1186/s13063-018-3116-3) sets out, potentially at *greater* risk of certain biases than a parallel cluster trial — within-cluster contamination in particular, since every cluster experiences both conditions. The extension exists precisely because these trials were being reported without the information needed to judge them; the requirement to give a clear justification for choosing the design is the part I would hold us to hardest.

**The practical parameters.** You need enough clusters — below about four, the randomisation buys you very little and the analysis is fragile. You need an estimate of the intra-cluster correlation coefficient to power the study at all, and you almost never have a good one in advance, so you plan for a range and say what you assumed. You need to specify the transition period during which a facility is training and neither cleanly control nor cleanly intervention, and either exclude it or model it. And you need to think hard about contamination: clinicians rotate between facilities in exactly the health systems where this design is attractive, and a rotating registrar carries the intervention across a cluster boundary in their head.

### 4.4 When you cannot run a wedge

Often you will not be able to. The rollout order may be decided by a ministry, by a funder, or by which facility has working connectivity. That is not a reason to abandon Level 4 — it is a reason to be explicit about what a weaker design can and cannot support.

The fallback is an **interrupted time series** analysed by segmented regression, with a concurrent control series where one exists. The [Cochrane EPOC standard](https://www.cochranelibrary.com/cdsr/doi/10.1002/14651858.CD000259.pub4/full) is at least three data points before and three after; more is much better, and monthly points over two years either side is a reasonable target. The method estimates two things a before-and-after chart cannot: a **level change** at the intervention point and a **slope change** afterwards.

<figure class="kp-fig">
<svg viewBox="0 0 940 470" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Two charts of the same underlying data: a before-and-after bar chart claiming a 25-point improvement, and a segmented regression showing a pre-existing trend with only a small genuine level change at the point of training">
<defs><marker id="it-r" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9 z" fill="#f87171"/></marker></defs>
<rect x="0.0" y="0.0" width="940.0" height="470.0" rx="14" fill="#0d1424" stroke="#182742" stroke-width="1" fill-opacity="1.0"/>
<text x="470.0" y="36.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="15.5" fill="#c9d6e8" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="1.4" fill-opacity="1.0">THE SAME DATA, HONESTLY AND DISHONESTLY DRAWN</text>
<text x="470.0" y="57.0" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#6b82a0" text-anchor="middle" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">the left-hand chart is the one that gets into the annual report; the right-hand one is the one that is true</text>
<rect x="46.0" y="88.0" width="410.0" height="340.0" rx="11" fill="#111c30" stroke="#f87171" stroke-width="1.6" fill-opacity="1.0"/>
<text x="62.0" y="114.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12" fill="#f87171" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">BEFORE-AND-AFTER BAR CHART</text>
<line x1="92" y1="136" x2="92" y2="366" stroke="#1e2d45"/>
<line x1="92" y1="366" x2="426" y2="366" stroke="#1e2d45"/>
<rect x="92.0" y="262.5" width="151.8181818181818" height="103.5" fill="#6b82a0" fill-opacity="0.25"/>
<rect x="274.18181818181813" y="205.0" width="151.81818181818187" height="161.0" fill="#10b981" fill-opacity="0.45"/>
<text x="167.9" y="254.5" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#6b82a0" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">BEFORE  45%</text>
<text x="350.1" y="197.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" fill="#10b981" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">AFTER  70%</text>
<text x="251.0" y="386.0" font-family="Helvetica, Arial, sans-serif" font-size="13" fill="#f87171" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">"a 25-point improvement"</text>
<text x="251.0" y="404.0" font-family="Helvetica, Arial, sans-serif" font-size="9.8" fill="#f87171" text-anchor="middle" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">every point of which the trend would have delivered anyway</text>
<rect x="486.0" y="88.0" width="410.0" height="340.0" rx="11" fill="#111c30" stroke="#10b981" stroke-width="1.6" fill-opacity="1.0"/>
<text x="502.0" y="114.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12" fill="#10b981" text-anchor="start" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">SEGMENTED REGRESSION (ITS)</text>
<line x1="532" y1="136" x2="532" y2="366" stroke="#1e2d45"/>
<line x1="532" y1="366" x2="866" y2="366" stroke="#1e2d45"/>
<circle cx="532.0" cy="297.0" r="3.4" fill="#00d4f5"/>
<circle cx="562.4" cy="287.8" r="3.4" fill="#00d4f5"/>
<circle cx="592.7" cy="280.9" r="3.4" fill="#00d4f5"/>
<circle cx="623.1" cy="271.7" r="3.4" fill="#00d4f5"/>
<circle cx="653.5" cy="262.5" r="3.4" fill="#00d4f5"/>
<circle cx="683.8" cy="253.3" r="3.4" fill="#00d4f5"/>
<circle cx="714.2" cy="237.2" r="3.4" fill="#10b981"/>
<circle cx="744.5" cy="230.3" r="3.4" fill="#10b981"/>
<circle cx="774.9" cy="221.1" r="3.4" fill="#10b981"/>
<circle cx="805.3" cy="211.9" r="3.4" fill="#10b981"/>
<circle cx="835.6" cy="205.0" r="3.4" fill="#10b981"/>
<circle cx="866.0" cy="195.8" r="3.4" fill="#10b981"/>
<line x1="532.0" y1="297.0" x2="683.8" y2="253.3" stroke="#00d4f5" stroke-width="2.4"/>
<line x1="683.8" y1="253.3" x2="866.0" y2="200.4" stroke="#00d4f5" stroke-width="1.8" stroke-dasharray="6 4" stroke-opacity="0.7"/>
<line x1="714.2" y1="237.2" x2="866.0" y2="195.8" stroke="#10b981" stroke-width="2.4"/>
<line x1="699.0" y1="136" x2="699.0" y2="366" stroke="#f59e0b" stroke-width="1.8" stroke-dasharray="5 4"/>
<text x="699.0" y="130.0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.2" fill="#f59e0b" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">TRAINING</text>
<path d="M847.8,203.9 L847.8,196.7" stroke="#f87171" stroke-width="2"/>
<text x="691.0" y="386.0" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#10b981" text-anchor="middle" font-weight="bold" font-style="normal" letter-spacing="0" fill-opacity="1.0">level change ≈ +3 points, slope unchanged</text>
<text x="691.0" y="404.0" font-family="Helvetica, Arial, sans-serif" font-size="9.8" fill="#8ea4c0" text-anchor="middle" font-weight="normal" font-style="italic" letter-spacing="0" fill-opacity="1.0">small, real, and the only number you can defend</text>
<path d="M462,258 L478,258" stroke="#f87171" stroke-width="2.4" marker-end="url(#it-r)"/>
</svg>
<figcaption>Identical underlying data, drawn twice. On the left, the chart that gets into the annual report: two bars, a 25-point improvement, and no way to see that the indicator was already climbing steadily before anyone was trained. On the right, the same series with its pre-existing trend made visible and extrapolated — leaving a real but modest level change of about three points, which is the only number anybody can defend.</figcaption>
</figure>

This figure is, to me, the single most useful thing in the post. The left-hand chart is not a fabrication; every number in it is true. It is the *shape of the presentation* that manufactures the claim. Adding a control series strengthens it further, moving the analysis towards a difference-in-differences estimator that removes shocks common to all facilities — a national guideline change, a strike, a supply interruption.

And where even that is not available: say so. "We observed an improvement in documentation completeness from 45% to 70% over the period. We cannot attribute this to the training programme, because the indicator was already improving and we had no control series." That sentence costs nothing except the pleasure of a stronger claim, and it is the difference between an evaluation and an advertisement.

<div class="kp-key">
It is entirely possible that a rigorous evaluation will show that some of what we teach does not change behaviour, or changes it in ways that do not benefit patients. If that happens, the correct response is to publish it and change the curriculum. <strong>An institution that cannot survive its own negative findings is not an institution worth building.</strong>
</div>

---

## Part 5 — The other pedagogical instruments, and how each would be used

Kirkpatrick is a frame for asking questions. It contains no instruments. Everything that actually generates the evidence comes from somewhere else, and it is worth naming each tool, saying what it buys, and saying how it would be used here.

### 5.1 Miller's pyramid, and entrustment above it

**What it is.** George Miller's 1990 framework describes four levels of what an assessment is evidence of: **knows** (facts), **knows how** (applying them), **shows how** (demonstrating in a controlled setting), **does** (performing unobserved in practice). It is the most useful single diagram in assessment because it stops people confusing the bottom of the pyramid with the top.

**How we would use it.** As a blueprinting tool. Every assessment item in the Institute's programme is tagged with its Miller level, and the tags are published in the assessment blueprint. The rule that follows is [commitment three](/post/2026-08-05-another-arrow-in-the-quiver#the-pedagogy-i-would-insist-on)'s operational form: **no certificate is issued on *knows* alone**, and every certificate requires evidence at *shows how* and at least one countersigned data point at *does*.

**The extension.** [Ten Cate and colleagues have proposed a fifth level — entrustment, or "trusted with future care"](https://academic.oup.com/academicmedicine/article-abstract/96/2/199/8346705) — which reframes the question from *how good is this trainee's performance* to *what would I now let this trainee do unsupervised*. That is the question a supervisor actually asks, and phrasing it that way tends to produce better-calibrated judgements than a numerical rating scale. For us the natural **entrustable professional activity** is: *"independently conducts an AI-assisted diagnostic consultation, including detection and disclosure of model error."* Rated on a supervision scale — observed only / with direct supervision / with indirect supervision / independently / able to supervise others — rather than on a 1-to-9 performance scale that no two assessors interpret alike.

### 5.2 Programmatic assessment

**What it is.** [Van der Vleuten and Schuwirth's principle](https://www.tandfonline.com/doi/full/10.1080/0142159X.2018.1555369): no single assessment is ever adequate for a high-stakes decision. Instead, collect many low-stakes data points, each optimised for feedback rather than judgement, triangulate across methods, and have a committee synthesise them into the high-stakes decision when enough information has accumulated. Individual data points are maximised for learning; the decision is made on aggregate.

**How we would use it.** This is the organising principle for the entire Level 2/Level 3 apparatus, and it resolves the reliability problem from §3.3 elegantly. No single mini-CEX gates anything. No single chart audit gates anything. A **competence committee** — not the trainee's own supervisor — reviews the accumulated portfolio and makes a documented, reasoned progression decision, with the reasoning written down. That last part matters more than it sounds: narrative quality in the record is what makes the decision defensible when it is challenged.

**The failure mode to design against.** Programmatic assessment collapses if the "low-stakes" data points are perceived as high-stakes. The moment trainees believe every mini-CEX is a judgement, they stop volunteering difficult cases and start volunteering easy ones, and the whole system measures case selection.

### 5.3 The AI-OSCE with a seeded error

Covered in full in [One Hidden Error](/post/2026-08-11-one-hidden-error). Its role in the measurement architecture is specific and worth restating: it is the **only instrument that can create a known ground truth**. In the workplace you never know whether the model was right, so you cannot score detection. In a station where you planted the error, you know exactly what should have been caught, and the conjunctive requirement on the error-detection domain means it cannot be compensated away.

Its limitation is equally specific: it measures *shows how*, in a candidate who knows they are being assessed, and it is therefore an upper bound on real-world performance. Which is the entire argument for Part 3.

### 5.4 Standard setting

Every judgement above — passed, competent, acceptable, improved — requires a line, and a line requires a defensible process. The [modified Angoff panel](/post/2026-08-12-the-angoff-panel-for-testing-clinicians) is how the knowledge test's cut score is set; borderline regression is the appropriate method for the OSCE, since the station data give you the borderline group directly.

The point I want to carry across into Level 4 is that this problem does not disappear when you move from exams to indicators. "Appropriate investigation rate" needs a standard as much as a 40-item MCQ does, and the same argument applies: a cut score is a policy decision about acceptable risk, and the only thing that makes it defensible is the quality and transparency of the process that produced it.

### 5.5 Retrospective pre-post, for the self-report you cannot avoid

**The problem.** Some things — confidence, perceived competence, self-reported frequency — can only be measured by asking. And a conventional pre-then-post self-report is systematically broken by **response-shift bias**: the course changes the learner's internal yardstick. A clinician who rated their AI competence 4/5 before the course may rate it 3/5 afterwards, having learned enough to know what they did not know. On a naive analysis, the course made them worse.

**The fix.** Ask both questions at the end. "Rate your competence now" and "thinking back, rate your competence before the course" — the *post-then-pre* design. Both ratings then use the same, post-course yardstick. The [evidence](https://eric.ed.gov/?id=EJ818361) is that this detects treatment effects that traditional pre-post analyses miss, though it introduces its own memory and social-desirability distortions and should never be the only measure of anything.

**How we would use it.** For confidence and self-efficacy only, always alongside an objective measure, and reported separately. The most interesting result would be a **divergence**: confidence rising while observed error detection falls is the signature of exactly the failure the whole programme exists to prevent, and it is a signal you can only get if you measure both.

### 5.6 A logic model

**What it is.** A one-page diagram of inputs → activities → outputs → short-term outcomes → long-term outcomes, with the assumptions on each arrow made explicit. Unglamorous, and the single highest-yield hour in the design of any evaluation.

**How we would use it.** As the artefact the Level 4 pre-registration is derived from. Its value is that it forces you to write the assumptions on the arrows. The arrow from "clinicians trained in the independent-impression rule" to "reduced time-to-escalation" carries at least four assumptions — that the rule survives to the workplace, that it changes what the clinician concludes, that the conclusion changes what they do, and that what they do is what determines escalation time. Writing them out tells you which are testable, which are heroic, and where the evaluation should look first when the result is null.

### 5.7 Audit and feedback, as a required driver

**What it is.** Measuring practice and giving clinicians the result. It is the most-studied behaviour-change intervention in health services research. [The Cochrane review](https://www.cochranelibrary.com/cdsr/doi/10.1002/14651858.CD000259.pub4/full) finds small but potentially important improvements in professional practice — and, more usefully, tells you *when* it works: when baseline performance is poor, when feedback comes from a supervisor or a respected colleague, when it is delivered more than once, when it is given both verbally and in writing, and when it includes explicit targets and an action plan.

**How we would use it.** This is where the evaluation stops being extractive. The chart audit of §3.4 is collected for evaluation; returning it to the clinician, with a target and an action plan, converts it into one of the required drivers. Same data, two functions. And a Level 3 measurement programme that gives nothing back to the people being measured will not survive contact with a busy clinical service, regardless of how good the design is.

### 5.8 Spaced retrieval, for the booster

The booster in §3.7 is a teaching intervention, and the retention literature is fairly clear about its shape. Effortful retrieval beats re-presentation; spacing beats massing; a test is a better learning event than a lecture. So the booster starts with a case and a required attempt *before* any teaching, rather than with a recap of the original slides. This is also why the interval matters: the booster is scheduled to land where the decay curve is steepest, which is precisely the information §3.2 is designed to give us.

### 5.9 The catalogue, in one table

| Instrument | Kirkpatrick level | What it buys | How we would use it | Principal failure mode |
|---|---|---|---|---|
| Reaction form (relevance/commitment type) | 1 | Detects broken delivery; generates L3 hypotheses | Four questions, none about enjoyment | Being cited as evidence of effect |
| MCQ with Angoff cut score | 2 | Defensible knowledge threshold | 40 items, 40% weight on Discernment | Tests recall of scepticism, not scepticism |
| AI-OSCE with seeded error | 2 | Known ground truth; conjunctive error domain | Gate to certification | Upper bound only; candidate knows they are watched |
| Countersigned portfolio product | 2→3 | Forces production, not attendance | Named senior signs it | Signature becomes a formality |
| mini-CEX / DOPS | 3 | Sees reasoning and disclosure | ≥8 encounters, ≥4 assessors, aggregated | Hawthorne; assessor stringency |
| Chart audit | 3 / 4a | Unobtrusive, scales, covers everyone | Blinded, double-coded, kappa reported | Measures documentation, not thought |
| Sandbox interaction log | 3 | Order of operations, no observer effect | Consented, purpose-limited, aggregate only | Becomes surveillance; destroys the behaviour |
| Entrustment / EPA scale | 3 | Asks the question supervisors actually ask | Supervision-level anchors | Drifts to a performance rating in practice |
| Multi-source feedback | 3 | Interprofessional view of handover behaviour | Nurse and pharmacy raters included | Popularity contest without anchored items |
| Retrospective pre-post | 2a | Corrects response-shift bias | Confidence only, alongside objective data | Memory and social desirability |
| Stepped-wedge CRT | 4 | Randomised counterfactual without denial | Where rollout order is ours to set | Confounding with time; contamination |
| Interrupted time series | 4 | Separates level change from pre-existing trend | Fallback; ≥3 points either side | Needs many points; no control series |
| Logic model | all | Makes assumptions on the arrows explicit | Derives the pre-registration | Written once, never revisited |
| Audit and feedback | driver | Turns measurement into reinforcement | Return the audit with a target and plan | One-off feedback with no action plan |

---

## Part 6 — What this apparatus still cannot tell you

Four honest limits, which I would want in the evaluation report rather than discovered by a critic.

**It cannot establish that the training caused the patient outcome.** Even a well-run stepped wedge across five facilities gives you an association under assumptions, with a confidence interval that will be wide. The causal chain from a two-day course to a mortality figure has at least six links and every one leaks.

**It cannot measure the counterfactual clinician.** We can measure what trained clinicians do. We cannot easily observe what the same clinician would have done untrained on the same patient. This is a limitation of the world, not of the design.

**It will be confounded by the model changing under us.** The system a cohort trained on in March is not the system they use in December. Model updates are a time-varying confounder that no educational design controls, and in a stepped wedge they are partially confounded with period. The honest response is to record model versions as a covariate and say plainly that it is a limitation.

**It cannot capture what I would most like to know** — whether a clinician has become a better thinker, or has merely acquired a compliant new ritual. B1 measured by timestamp is a proxy for a habit of mind, and a proxy is what it will remain. Anyone claiming otherwise is overselling.

---

## What I would write into the founding documents

Compressed, so it fits on one page of an operations manual.

1. **No Level 1 result is ever reported as an outcome.** Reaction data informs delivery and generates hypotheses. Nothing else.
2. **Every certificate requires evidence at *shows how* and at least one countersigned data point at *does*.** Nothing is issued on *knows* alone.
3. **Level 3 is measured at three and twelve months** on four pre-specified behaviours, from three sources with non-overlapping biases, aggregated across at least eight encounters and four assessors, with the analysis of concordance and discordance specified in advance.
4. **Interaction logs are consented, purpose-limited, pseudonymised, time-limited, and inadmissible in any individual performance process.** No exceptions, and the undertaking is published.
5. **Level 4 indicators, definitions, analysis and stopping rules are registered before the first facility is trained.** Balancing measures included. A rise in reported AI-related harm is pre-declared as potentially favourable.
6. **A stepped-wedge design is used wherever the rollout order is ours to set.** Where it is not, segmented regression with a control series where available, and an explicit statement that causation is not established.
7. **The evaluation protocol and its results are published regardless of outcome**, per the independence rules, and the external examiner sees the analysis before the board does.
8. **Every audit returns to the clinician** with a target and an action plan, within four weeks. Measurement that gives nothing back does not survive.

---

## Coda

The reason commitment ten is written the way it is — *"or we admit we do not know"* — is that the second clause is the one that will actually be needed. Most of the time, for most of what we teach, a rigorous evaluation will return a wide confidence interval around a small effect, and the honest sentence will be that we cannot yet say.

That is not a failure of the evaluation. It is what evaluation is for. The alternative — a satisfaction score, a bar chart, and a claim — is available at all times, costs nothing, and tells you nothing about whether a clinician in a district hospital at three in the morning still forms their own impression before the machine offers one.

That is the only question worth answering. It is expensive to answer. Commitment ten is the promise to pay.

---

If you want the rest of the design: the [full blueprint](/post/2026-08-05-another-arrow-in-the-quiver) sets out the institution, the five tracks and the five gated levels; [Borrowed From an Art School](/post/2026-08-10-borrowed-from-an-art-school) traces where the competency framework came from and what its licence permits; [One Hidden Error](/post/2026-08-11-one-hidden-error) covers the OSCE and the AI-OSCE in detail; [The Angoff Panel](/post/2026-08-12-the-angoff-panel-for-testing-clinicians) covers standard setting; [The Law Is Part of the Architecture](/post/2026-08-01-the-law-is-part-of-the-architecture) covers the Kenyan legal and data-governance frame that Part 3.5 depends on; and [AI Walks Into the Clinic](/post/2026-07-28-ai-walks-into-the-clinic-chatgpt-health) is on how fast the ground is moving underneath all of it. Other writing is in the [archive](/archive), and things I have built are under [demos](/demos) and [lessons](/lessons).

---

## References

**The model itself**

- Kirkpatrick, D. L. (1959–60). Four-part series, *Journal of the American Society of Training Directors*. Summarised, with the later revision, in Kirkpatrick Partners, [*An Introduction to the New World Kirkpatrick Model*](https://www.kirkpatrickpartners.com/wp-content/uploads/2021/11/Introduction-to-The-New-World-Kirkpatrick%C2%AE-Model.pdf).
- Thalheimer, W. [*Donald Kirkpatrick was NOT the originator of the four-level model*](https://www.worklearning.com/2018/01/30/donald-kirkpatrick-was-not-the-originator-of-the-four-level-model-of-learning-evaluation/) — a useful corrective on attribution.
- Yardley, S. and Dornan, T. (2012). [*Kirkpatrick's levels and education 'evidence'*](https://asmepublications.onlinelibrary.wiley.com/doi/10.1111/j.1365-2923.2011.04076.x). *Medical Education* 46(1):97–106. The critique to read before adopting the model.
- Moore, D. E. et al., expanded outcomes framework, levels 1–7 — see [*A Conceptual Framework for Continuing Medical Education and Population Health*](https://www.tandfonline.com/doi/full/10.1080/10401334.2021.1950540).
- Barr, H., Freeth, D., Hammick, M. et al., split levels 2a/2b and 4a/4b for interprofessional education — see the National Academies' [*Measuring the Impact of Interprofessional Education*](https://www.ncbi.nlm.nih.gov/books/NBK338356/).

**Assessment**

- Miller, G. E. (1990). *The assessment of clinical skills/competence/performance*. *Academic Medicine* 65(9):S63–7.
- Ten Cate, O. et al. (2021). [*Entrustment Decision Making: Extending Miller's Pyramid*](https://academic.oup.com/academicmedicine/article-abstract/96/2/199/8346705). *Academic Medicine* 96(2):199–204.
- Schuwirth, L. and van der Vleuten, C. et al. (2019). [*Programmatic assessment: can we provide evidence for saturation of information?*](https://www.tandfonline.com/doi/full/10.1080/0142159X.2018.1555369) *Medical Teacher* 41(6):676–82. The originating idea is in van der Vleuten et al., *A model for programmatic assessment fit for purpose*, *Medical Teacher* (2012).
- Moonen-van Loon, J. et al. (2013). [*Composite reliability of a workplace-based assessment toolbox for postgraduate medical education*](https://link.springer.com/article/10.1007/s10459-013-9450-z). *Advances in Health Sciences Education*.
- Howard, G. S. et al. on response-shift bias; and [*Controlling response shift bias: the retrospective pre-test design*](https://eric.ed.gov/?id=EJ818361), *Assessment & Evaluation in Higher Education* (2008).

**Retention and decay**

- Legoux, C. et al. (2021). [*Retention of Critical Procedural Skills After Simulation Training: A Systematic Review*](https://onlinelibrary.wiley.com/doi/10.1002/aet2.10536). *AEM Education and Training*.
- Yang, C.-W. et al. (2012). [*A systematic review of retention of adult advanced life support knowledge and skills in healthcare providers*](https://www.resuscitationjournal.com/article/S0300-9572(12)00125-6/abstract). *Resuscitation*.

**Evaluation design**

- Hemming, K., Taljaard, M., McKenzie, J. E. et al. (2018). *Reporting of stepped wedge cluster randomised trials: extension of the CONSORT 2010 statement with explanation and elaboration.* *BMJ* 363:k1614. Introduced in [*Trials*](https://trialsjournal.biomedcentral.com/articles/10.1186/s13063-018-3116-3).
- Ivers, N. et al. [*Audit and feedback: effects on professional practice*](https://www.cochranelibrary.com/cdsr/doi/10.1002/14651858.CD000259.pub4/full), Cochrane Database of Systematic Reviews (2025 update of the 2012 review).
- Penfold, R. B. and Zhang, F. (2013). [*Use of interrupted time series analysis in evaluating health care quality improvements*](https://www.academicpedsjnl.net/article/S1876-2859(13)00210-6/fulltext). *Academic Pediatrics* 13(6):S38–44.
- [*Using chart reviews to evaluate a Continuing Medical Education (CME) program*](https://pmc.ncbi.nlm.nih.gov/articles/PMC10548990/), *BMC Medical Education* (2023) — a worked example of reaching Moore level 5 (performance) by retrospective record review.

**Clinical AI and automation bias**

- [*Automation Bias in Large Language Model–Assisted Diagnostic Reasoning among Physicians Trained in AI Literacy — A Randomized Clinical Trial*](https://ai.nejm.org/doi/full/10.1056/AIoa2501001), *NEJM AI*, 2025. The trial the blueprint is built around.
- Goddard, K., Roudsari, A. and Wyatt, J. C. (2012). [*Automation bias: a systematic review of frequency, effect mediators, and mitigators*](https://academic.oup.com/jamia/article-abstract/19/1/121/732254). *JAMIA* 19(1):121–7.
- [OpenAI and Penda Health, *Pioneering an AI clinical copilot*](https://openai.com/index/ai-clinical-copilot-penda-health/), the underlying [real-world study](https://arxiv.org/pdf/2507.16947), and the [critical reading in STAT News](https://www.statnews.com/2025/10/01/penda-health-open-ai-safety-net-study-kenya-artificial-intelligence/).
- [AAMC, *Artificial Intelligence Competencies Across the Learning Continuum*](https://www.aamc.org/about-us/medical-education/ai-competencies); [WHO, *Ethics and governance of AI for health: guidance on large multi-modal models*](https://www.who.int/publications/b/70584).

---

<div style="font-size:0.8em; color:#6b82a0; font-style:italic; margin-top:2em;">
In the spirit of the framework's own Diligence competency: this post was drafted with AI assistance. The argument, the design decisions, the operational specifications and the stated hypothesis are mine, and I take full responsibility for the accuracy of its contents. The decay curves in Figure 4 are illustrative of a hypothesis and are not data.
</div>
