---
title: "What I'm Building Next: A Bitcoin Rail for the Clinical AI Institute"
date: 2026-09-10
category: AI & Medicine
tags: bitcoin, lightning network, payments, Kenya, Virtual Asset Service Providers Act, MedLattice, clinical AI, blockchain, fintech, draft
level: All readers — no technical background assumed
read_time: 9 min
summary: "This is a working note, not a finished piece — a look at the payment system I have started drafting for the Institute, currently called Malipo Rail, while it is still wet. The blueprint sets out a five-year, USD 17.38 million funding model and never specifies how any of that money actually moves: how a donor's gift becomes a disbursement, how a member hospital pays its dues, how a patient pays a bill. I have been sketching an answer built on Bitcoin and the Lightning Network rather than an Institute-issued coin or a public Ethereum system, sitting beside MedLattice rather than inside it, because the record I built on the premise that clinical data should never touch a public market or a token is not a record I want to now bolt a cryptocurrency onto. I say here why bitcoin over the alternatives, why Kenya's regulatory position and its bitcoin-using population make this plausible rather than exotic, and where the draft is still thin. A full, proper write-up follows once more of it has been argued with — this post will be replaced when it does."
featured: false
---

<div style="font-size:0.85em; background:#111827; border-left:4px solid #6b82a0; padding:0.9em 1.3em; border-radius:0 6px 6px 0; margin:1.5em 0; color:#9fb3cc;">
<em>I write here in a personal capacity. This post is a status update on work in progress, not a finished piece — it exists to keep readers of the <a href="/post/2026-08-05-another-arrow-in-the-quiver">Institute blueprint</a> and <a href="/post/2026-08-25-not-shown-is-not-locked">MedLattice</a> posts abreast of what comes next while I am still arguing with myself about the details. I expect to delete this post and replace it with a proper, full-length piece once the design has been through more rounds of that argument.</em>
</div>

<style>
.mr-honest { font-size: 0.93em; background: #1a0f14; border-left: 4px solid #f87171; padding: 0.9em 1.3em; margin: 1.4em 0; border-radius: 0 4px 4px 0; }
.mr-key { font-size: 0.95em; background: #101a2e; border-left: 4px solid #00d4f5; padding: 0.9em 1.3em; margin: 1.4em 0; border-radius: 0 4px 4px 0; }
</style>

<div style="font-size:0.8em; background:#1a1f2e; border-left:4px solid #1a237e; padding:1em 1.4em; border-radius:0 6px 6px 0; margin:1.5em 0;">
  🎧 <strong>Listen to this post (10 minutes):</strong> A short summary of where the draft stands — why bitcoin and Lightning rather than an Institute coin or an Ethereum system, why the payment rail sits beside MedLattice rather than inside it, and what Kenya's new virtual-asset regulations mean for a self-custodied treasury.<br/><br/>
  <audio controls preload="none" style="width:100%; margin-top:0.4em;">
    <source src="https://pub-f57cd770c3d9448dafde9725cbc874b9.r2.dev/audio/Kenyas_Bitcoin_Rail_for_Clinical_AI.mp3" type="audio/mpeg">
    Your browser does not support the audio element.
  </audio>
</div>

I have been holding bitcoin for over fifteen years now, since close to its inception, and at this point I understand bitcoin core at the protocol level rather than as a speculative position — the UTXO model, script, why the block size debate mattered, what SegWit actually fixed, how Lightning sits on top as a second layer rather than a replacement for the base chain. I am saying that plainly because it is the reason this post exists. I do not want to bolt a generic "accept crypto" plugin onto the Institute. I want to use what bitcoin and Lightning are actually good at in service of a specific, unglamorous problem the <a href="/post/2026-08-05-another-arrow-in-the-quiver">blueprint</a> left open on purpose: getting money from patients, donors and member hospitals to where the training and certification actually happens.

**This is what I am currently working on.** What follows is a discussion of a first draft — not an announcement, not a finished architecture, and not something anyone should treat as settled. I want to think out loud about it here, the way I did with MedLattice before it hardened into something I was prepared to publish a full specification for.

## The gap the blueprint left open

The blueprint's financial model is precise about the destination and silent about the mechanism. USD 17.38 million over five years. USD 5.34 million in earned income by Year 5. A USD 12.05 million subsidy requirement made up of host-institution contribution, philanthropy, CPD income and research grants. Twenty-one thousand, seven hundred and forty-six clinicians certificated, at a cost that is meant to fall from USD 799 to USD 544 per head. None of that says how a donor's pledge becomes an actual disbursement gated at the founding, pilot and scale-up decision points, how a member hospital pays its dues, or how a patient at one of those hospitals pays a bill at all. That was the right thing to leave out of the blueprint — it wasn't the blueprint's job — but it isn't optional, and I have started drafting an answer. I am currently calling it **Malipo Rail** — *malipo* being Kiswahili for "payments" — though I want to be clear that is a working name, not a decision.

## Why bitcoin, not our own coin, not Ethereum

I went through this properly rather than assuming my own priors, because it is the decision everything else depends on.

An Institute-issued coin sounds appealing until you look at what it would actually cost and what it would actually signal. Kenya's Virtual Asset Service Providers Regulations, 2026 — gazetted in July, now in force, with existing operators required to hold a licence by 4 November — put token issuance and stablecoin issuance on the list of ten explicitly licensed activities, and a stablecoin issuer needs KES 300 million in paid-up capital before it can start. That is money the blueprint's own model has no room for. And even if it did, a hospital-adjacent institution minting a coin patients or hospitals are asked to hold sits far too close to the thing the blueprint's own governance safeguards exist to rule out — no vendor funding curriculum for its own products, no undisclosed equity. I don't want the Institute's financial health to depend on anyone acquiring something we control the supply of.

An Ethereum-based system has a real case for it, and not a hypothetical one — MedLattice already runs on a permissioned Ethereum-compatible consortium chain, so the tooling and the team's fluency with it already exist and are proven. But that is a *permissioned* chain holding no financial assets by design. A public Ethereum system carrying real money is a different trust model entirely, and putting it under the same broad label as MedLattice's clinical ledger is exactly the kind of architectural conflation that gets reported, if it ever goes wrong, as "the AI hospital's blockchain was hacked" without anyone distinguishing which one.

Bitcoin and Lightning earn the position by elimination as much as by their own merits, though the merits are real: over fifteen years of the base layer surviving attack by the best-resourced adversaries on the planet with its core assumptions intact, no issuer whose insolvency or policy change can hurt a treasury meant to outlast any single hospital administration, and Lightning settling in milliseconds for fractions of a cent — which is the only way a patient-facing micropayment makes sense at all.

<div class="mr-honest">
<strong>Where this is genuinely unresolved</strong>

Bitcoin's price moves by double digits in weeks, which means nobody should ever see a hospital bill denominated in raw BTC — that has to be solved with a stable settlement leg, and I have not settled how. And the new VASP Regulations do not, as far as I can establish, contain any explicit treatment of a self-custodial Lightning node that never holds anyone else's funds. Whether the Institute can hold donor bitcoin in its own multisignature custody without itself needing a wallet-provider licence is an open legal question, not a design decision I am entitled to make unilaterally. It is the single highest-priority item on my list, and it needs an actual Kenyan VASP lawyer before a satoshi changes hands.
</div>

## Why this sits beside MedLattice, not inside it

<a href="/post/2026-08-25-not-shown-is-not-locked">MedLattice</a> was built on one governing premise — *not shown is not locked* — and its own specification says, in as many words, that it avoids cryptocurrency, tokens and public markets entirely. I am not revising that. A payment rail is a genuinely different problem from a clinical record, and I think it can sit next to MedLattice without contradicting it, provided the two stay structurally separate rather than becoming one blockchain for everything.

The way I currently have this drafted: MedLattice gains one new compartment — Financial, alongside the existing twenty or so — holding invoice records and payment status at the same per-fact encryption granularity as everything else, plus three new contracts on the same permissioned chain that never hold a wallet address, a private key or a single satoshi. They record cryptographic attestations of payments that happened off-chain on Lightning — proof that something was paid, without the on-chain record ever being able to say by whom or for what clinical reason. A compromise of the payment rail should not be able to touch a single patient record, and a compromise of MedLattice should not be able to touch a single sat. That separation is the part of the draft I am most confident about; everything downstream of it is still being argued with.

## Kenya is the reason this isn't exotic

None of this would be worth drafting in a country where phone-based instant payment was a novelty. It isn't, here. M-Pesa has over 40 million monthly active users and has spent almost two decades teaching an entire population that money can live on a phone and move in seconds without a bank branch anywhere in the loop — which is exactly the expectation Lightning has to meet, not introduce. On peer-to-peer bitcoin venues, M-Pesa is already the dominant settlement leg. Roughly one in ten Kenyans is estimated to hold some cryptocurrency, driven largely by remittances and by people hedging shilling depreciation with dollar-pegged stablecoins. And the regulatory environment, rather than being hostile or absent, now has an actual licensing regime with a named central bank regulator and a named capital-markets regulator — which is more regulatory clarity than most jurisdictions bitcoin operates in have managed. I want to flag one thing honestly rather than repeat a line I see everywhere in industry coverage: it's commonly said that Kenya leads the world in peer-to-peer bitcoin trading. I went looking for that in Chainalysis's own published index and could not confirm it — Kenya doesn't appear in their top-twenty tables at all, though the wider Sub-Saharan Africa region shows genuinely strong adoption growth. I'd rather under-claim here than hand a funder a superlative I can't stand behind.

## What else is sketched, not built

An idea for a free app — patients, doctors and nurses, hospital finance staff, funders, and developers who contribute to the build — where paying a bill or receiving a grant is one small part of a larger institute-progress dashboard anyone can open and see where we actually stand against the blueprint's own milestones. A decision log, in the same style I used for MedLattice's open items, currently running to twelve unresolved questions — custody model, whether a non-transferable internal credit for subsidised care is legally distinct from a token, whether claim payment should ever reference a hospital's pedagogical compliance data (I am nervous about that last one, for reasons that deserve their own post). None of it is built. Most of it is not even settled in my own head yet.

That is the honest state of this, and it's why this post gets replaced rather than expanded once the argument has actually happened. If you have a view on any of it — particularly the Kenyan VASP question, which I genuinely cannot resolve from a desk — I would rather hear it now than after the design has calcified.
