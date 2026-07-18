---
title: "The Grain of Language: How a Machine Reads the Internet"
date: 2026-07-17
category: Deep Learning
tags: tokenization, byte pair encoding, BPE, tokens, LLM, pretraining, vocabulary, context window, UTF-8, foundations
level: Beginner–Intermediate
read_time: 40 min
summary: "The opening chapter of a ground-up account of how large language models actually work. Before a model can think, it must read — and reading, for a machine, means something stranger and more consequential than most people imagine. This is the story of how the raw text of the internet becomes the tokens a model sees, why the model builds its own alphabet to do it, and why that single design choice explains so many of an LLM's strangest habits."
featured: false
---

<style>
.chapter-banner {
  font-size: 0.85em;
  background: linear-gradient(135deg, #1a237e 0%, #283593 100%);
  color: white;
  padding: 1.2em 1.6em;
  border-radius: 8px;
  margin: 1.5em 0;
  line-height: 1.6;
}
.chapter-banner a { color: #90caf9; font-weight: bold; }
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
.tokrow {
  font-size: 0.82em;
  background: #0d1117;
  border: 1px solid #1e2d45;
  border-radius: 6px;
  padding: 0.9em 1.2em;
  margin: 1em 0;
  font-family: 'JetBrains Mono', monospace;
  color: #c9d6e8;
  line-height: 2.1;
}
.tok {
  padding: 0.15em 0.4em;
  border-radius: 4px;
  margin: 0 1px;
  white-space: pre;
}
figure.diagram { margin: 2em 0; text-align: center; }
figure.diagram svg { max-width: 100%; height: auto; }
figure.diagram figcaption {
  font-size: 0.8em; color: #6b82a0; margin-top: 0.6em; text-align: left;
}
</style>

<div class="chapter-banner">
📖 <strong>Chapter One of a ground-up account of how large language models work.</strong> No prior machine-learning knowledge is assumed — only curiosity and a willingness to look closely at something everyone uses and almost no one examines. We begin not with neurons or mathematics, but with a more basic question: before a language model can do anything clever, how does it even <em>read</em>?
</div>

# The Grain of Language: How a Machine Reads the Internet

<nav style="font-size:0.8em; background:#0d1117; border:1px solid #1e2d45; border-left:4px solid #00d4f5; border-radius:0 8px 8px 0; padding:0.9em 1.3em; margin:1.6em 0; line-height:1.95;">
<div style="color:#00d4f5; font-family:'JetBrains Mono',monospace; font-size:0.86em; letter-spacing:0.06em; margin-bottom:0.5em;">📚 HOW AN LLM WORKS · CONTENTS</div>
<span style="color:#6b82a0;">1.</span> <strong style="color:#f59e0b;">The Grain of Language</strong> &nbsp;·&nbsp;
<span style="color:#6b82a0;">2.</span> <a href="/post/2026-07-18-the-prediction-game">The Prediction Game</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">3.</span> <a href="/post/2026-07-19-reading-the-room">Reading the Room</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">4.</span> <a href="/post/2026-07-20-the-tower">The Tower</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">5.</span> <a href="/post/2026-07-21-how-noise-becomes-knowledge">How Noise Becomes Knowledge</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">6.</span> <a href="/post/2026-07-22-manners-for-a-mind">Manners for a Mind</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">7.</span> <a href="/post/2026-07-23-meaning-you-can-search">Meaning You Can Search</a> &nbsp;·&nbsp;
<span style="color:#6b82a0;">8.</span> <a href="/post/2026-07-24-the-agent">The Agent</a>
</nav>

Type a sentence into ChatGPT and press enter. In the fraction of a second before any answer begins to form, something happens that feels too mundane to matter and turns out to explain a startling amount about what these systems can and cannot do.

Your sentence is taken apart.

Not into words, exactly, and not into letters. Into pieces of a kind you have almost certainly never thought about — pieces the machine invented for itself before it ever met your sentence. Everything the model does afterward — every association it draws, every fact it recalls, every mistake it makes — happens downstream of this quiet act of disassembly. If you want to understand large language models from the ground up, and I mean genuinely from the ground, this is the ground. So this is where we start.

I have spent a long time teaching difficult technical material to people who are clever but not specialists — clinicians, mostly, and researchers from fields far from computer science. The lesson that experience has burned into me is that understanding almost always fails at the *foundation*, not the summit. People nod along at "it predicts the next word" and "it's a neural network," and then a hundred pages later nothing quite adds up, because the foundation was skipped. Tokenization is the most-skipped foundation of them all. Books gesture at it in a paragraph and move on. We are not going to move on. By the end of this chapter you will understand it better than most people who use these tools professionally, and you will never look at a chatbot's odd little failures the same way again.

## Part I — Where the words come from

Before we can talk about how a model reads, we have to talk about what it reads. And the honest answer, stripped of mystique, is: a very large pile of text, most of it scraped from the open internet.

This sounds almost disappointingly ordinary, and it is worth sitting with the strangeness underneath the ordinariness. A modern language model's entire sense of the world — its grasp of grammar, its store of facts, its imitation of reasoning, its uncanny fluency in dozens of languages — is a statistical residue left behind by an enormous quantity of human writing. There is no encyclopaedia inside it, no database, no rules typed in by hand. There is only text, and what the model managed to internalise by trying, billions of times, to predict what came next in that text. Get the text wrong and everything downstream is wrong. The corpus is not a detail of the build; it *is* the build.

So where does the pile come from? The starting point, for most of the field, is a remarkable public resource: [Common Crawl](https://commoncrawl.org/), a non-profit that has been quietly sending automated crawlers across the web since 2007 and archiving what they find. The scale is difficult to hold in the mind — over 300 billion pages accumulated across fifteen years, with three to five billion fresh pages added every month. It is, in a real sense, a photograph of the readable internet, taken over and over.

But here is the thing nobody tells you: that raw photograph is almost unusable. The open web is, to put it kindly, mostly junk. Spam, boilerplate navigation menus, cookie banners, auto-generated filler, adult content, malware pages, duplicated text copied across ten thousand sites, and markup — endless HTML tags wrapped around the actual prose like packaging around a small gift. Feed that directly to a model and you get a model that has learned the internet's worst habits. The single least glamorous and most decisive part of building a language model is *cleaning*.

The cleaning is a pipeline — a sequence of filters, each throwing away more of the raw crawl until what remains is something you would actually want a model to learn from.

<figure class="diagram">
<svg viewBox="0 0 720 500" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The data refinement funnel from raw web crawl to clean training corpus">
  <defs>
    <marker id="da" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9 z" fill="#6b82a0"/></marker>
  </defs>
  <rect x="0" y="0" width="720" height="500" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="34" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">FROM RAW WEB TO CLEAN CORPUS</text>

  <!-- funnel bars, narrowing -->
  <rect x="90"  y="60"  width="540" height="46" rx="8" fill="#3d0f0f" stroke="#f87171" stroke-width="1.5"/>
  <text x="360" y="82"  text-anchor="middle" fill="#fde2e2" font-family="sans-serif" font-size="12.5" font-weight="bold">Raw web crawl — hundreds of billions of pages</text>
  <text x="360" y="98"  text-anchor="middle" fill="#e2a0a0" font-family="sans-serif" font-size="10.5">spam · adult · malware · boilerplate · duplicates · raw HTML</text>

  <rect x="140" y="122" width="440" height="42" rx="8" fill="#2e1e5e" stroke="#a78bfa" stroke-width="1.5"/>
  <text x="360" y="143" text-anchor="middle" fill="#e8e3fa" font-family="sans-serif" font-size="12" font-weight="bold">① URL &amp; domain filtering</text>
  <text x="360" y="158" text-anchor="middle" fill="#9f8fd0" font-family="sans-serif" font-size="10">drop known spam, adult, malware, and low-quality domains</text>

  <rect x="175" y="180" width="370" height="42" rx="8" fill="#0a4a5c" stroke="#00d4f5" stroke-width="1.5"/>
  <text x="360" y="201" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="12" font-weight="bold">② Text extraction</text>
  <text x="360" y="216" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="10">strip the HTML packaging — keep only the human prose</text>

  <rect x="205" y="238" width="310" height="42" rx="8" fill="#0a4a5c" stroke="#00d4f5" stroke-width="1.5"/>
  <text x="360" y="259" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="12" font-weight="bold">③ Language filtering</text>
  <text x="360" y="274" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="10">keep the target languages; set the model's linguistic diet</text>

  <rect x="235" y="296" width="250" height="42" rx="8" fill="#4a3000" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="360" y="317" text-anchor="middle" fill="#fdeccd" font-family="sans-serif" font-size="12" font-weight="bold">④ Deduplication</text>
  <text x="360" y="332" text-anchor="middle" fill="#f0c987" font-family="sans-serif" font-size="10">remove text repeated across thousands of pages</text>

  <rect x="265" y="354" width="190" height="42" rx="8" fill="#4a3000" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="360" y="375" text-anchor="middle" fill="#fdeccd" font-family="sans-serif" font-size="12" font-weight="bold">⑤ PII removal</text>
  <text x="360" y="390" text-anchor="middle" fill="#f0c987" font-family="sans-serif" font-size="10">scrub personal identifiers</text>

  <rect x="285" y="418" width="150" height="46" rx="8" fill="#053d28" stroke="#10b981" stroke-width="2"/>
  <text x="360" y="440" text-anchor="middle" fill="#d3f5e6" font-family="sans-serif" font-size="12.5" font-weight="bold">Clean corpus</text>
  <text x="360" y="456" text-anchor="middle" fill="#8fd8b8" font-family="sans-serif" font-size="10">trillions of words of good text</text>

  <path d="M360,106 L360,120" stroke="#6b82a0" stroke-width="2" marker-end="url(#da)"/>
  <path d="M360,164 L360,178" stroke="#6b82a0" stroke-width="2" marker-end="url(#da)"/>
  <path d="M360,222 L360,236" stroke="#6b82a0" stroke-width="2" marker-end="url(#da)"/>
  <path d="M360,280 L360,294" stroke="#6b82a0" stroke-width="2" marker-end="url(#da)"/>
  <path d="M360,338 L360,352" stroke="#6b82a0" stroke-width="2" marker-end="url(#da)"/>
  <path d="M360,396 L360,416" stroke="#6b82a0" stroke-width="2" marker-end="url(#da)"/>
</svg>
<figcaption><strong>Figure 1.</strong> The refinement pipeline. Each stage discards more of the raw crawl. What survives — a few tens of terabytes of clean text from a vastly larger input — is the material the model actually learns from. Two of these stages, text extraction and language filtering, quietly decide what the model will be good at.</figcaption>
</figure>

If you would like to see how meticulous this cleaning actually is, the team at Hugging Face documented one such pipeline in unusual and generous detail for a dataset they call [FineWeb](https://huggingface.co/spaces/HuggingFaceFW/blogpost-fineweb-v1) — around fifteen trillion words of filtered English text, occupying roughly forty-four terabytes on disk. Read their write-up and one point becomes inescapable: an enormous fraction of the effort in building a frontier model goes not into the clever mathematics you will meet in later chapters, but into deciding, page by page and filter by filter, what counts as text worth learning from. It is the most consequential editorial decision in the field, and it is made almost entirely by engineering.

<div class="callout">
⚕️ <strong>A note for those of us in medicine, and it applies far beyond it.</strong> Look again at stage ③, language filtering. A pipeline tuned to keep English and discard "low-resource" languages is, in the same stroke, deciding that the model will be fluent in the medicine of the English-speaking world and clumsy in Swahili, in Amharic, in the clinical vocabulary of the places that most need cheap expertise. The model's blind spots are not accidents of the algorithm. They are inherited, faithfully, from what we chose to feed it. Every limitation you will later curse in a deployed tool was, somewhere, a line in a data-cleaning script.
</div>

So: we now have our pile. Tens of terabytes of clean, deduplicated, mostly-English human writing. A model cannot read a terabyte of text any more than it can read your sentence. It reads numbers. Which brings us to the real subject of this chapter — the bridge between text and number, and the surprising cleverness required to build it well.

## Part II — Why a machine cannot simply read

Here is a fact that is easy to state and easy to underestimate: a neural network does not process text. It processes sequences of numbers drawn from a fixed, finite set of symbols. Everything a model ever "sees" is a one-dimensional stream of these symbols, one after another, like beads on a string. Our entire job, in this chapter, is to turn a page of writing into such a stream — and to do it well, because *how* we do it turns out to matter enormously.

Let us take the most naive approaches first, because their failures are exactly what motivates the clever solution.

**Attempt one: one symbol per character.** The obvious idea. Let each distinct character — every letter, digit, punctuation mark — be a symbol. "cat" becomes three symbols: `c`, `a`, `t`. Clean and intuitive. But now consider that the model must handle not just English but every script humans write in: Cyrillic, Arabic, Chinese, Japanese, Korean, mathematical notation, emoji, and the thousands of rarer symbols in between. The universal catalogue of these characters, called Unicode, contains around 150,000 distinct code points and grows every year. A vocabulary of 150,000 symbols is workable in principle, but it is unstable — tied to a standard that keeps changing — and it wastes enormous capacity on symbols the model will almost never see. Worse, it still splits common English words into many symbols, which, as we are about to discover, is costly.

**Attempt two: work in raw bytes.** There is a beautiful, principled alternative. Every piece of digital text, in whatever script, is *already* stored as a sequence of bytes, using an encoding called UTF-8. A byte is just a number from 0 to 255 — so there are exactly 256 possible byte-symbols, a tiny and permanently fixed vocabulary. UTF-8 spends one byte on common English characters and two, three, or four bytes on rarer ones. It is universal, stable, and elegant. Let each byte be a symbol, and the vocabulary problem vanishes.

To see the ladder of representations underneath a single ordinary word, look closely:

<figure class="diagram">
<svg viewBox="0 0 720 430" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The layers of representation beneath the word cat, from text down to bits">
  <defs>
    <marker id="db" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9 z" fill="#6b82a0"/></marker>
  </defs>
  <rect x="0" y="0" width="720" height="430" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="34" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">WHAT LIVES UNDER THE WORD “cat”</text>

  <text x="60" y="82" fill="#6b82a0" font-family="sans-serif" font-size="11.5">what you see</text>
  <rect x="300" y="62" width="120" height="40" rx="8" fill="#2e1e5e" stroke="#a78bfa" stroke-width="1.5"/>
  <text x="360" y="87" text-anchor="middle" fill="#e8e3fa" font-family="monospace" font-size="18" font-weight="bold">cat</text>

  <path d="M360,102 L360,120" stroke="#6b82a0" stroke-width="2" marker-end="url(#db)"/>
  <text x="60" y="146" fill="#6b82a0" font-family="sans-serif" font-size="11.5">characters</text>
  <g font-family="monospace" font-size="16">
    <rect x="250" y="126" width="60" height="38" rx="7" fill="#0a4a5c" stroke="#00d4f5"/><text x="280" y="151" text-anchor="middle" fill="#d8f6fd">c</text>
    <rect x="330" y="126" width="60" height="38" rx="7" fill="#0a4a5c" stroke="#00d4f5"/><text x="360" y="151" text-anchor="middle" fill="#d8f6fd">a</text>
    <rect x="410" y="126" width="60" height="38" rx="7" fill="#0a4a5c" stroke="#00d4f5"/><text x="440" y="151" text-anchor="middle" fill="#d8f6fd">t</text>
  </g>

  <path d="M360,164 L360,182" stroke="#6b82a0" stroke-width="2" marker-end="url(#db)"/>
  <text x="60" y="208" fill="#6b82a0" font-family="sans-serif" font-size="11.5">Unicode code points</text>
  <g font-family="monospace" font-size="13">
    <rect x="240" y="188" width="80" height="38" rx="7" fill="#111827" stroke="#2a3f5f"/><text x="280" y="212" text-anchor="middle" fill="#c9d6e8">U+0063</text>
    <rect x="330" y="188" width="80" height="38" rx="7" fill="#111827" stroke="#2a3f5f"/><text x="370" y="212" text-anchor="middle" fill="#c9d6e8">U+0061</text>
    <rect x="420" y="188" width="80" height="38" rx="7" fill="#111827" stroke="#2a3f5f"/><text x="460" y="212" text-anchor="middle" fill="#c9d6e8">U+0074</text>
  </g>

  <path d="M360,226 L360,244" stroke="#6b82a0" stroke-width="2" marker-end="url(#db)"/>
  <text x="60" y="270" fill="#6b82a0" font-family="sans-serif" font-size="11.5">UTF-8 bytes (0–255)</text>
  <g font-family="monospace" font-size="15">
    <rect x="250" y="250" width="60" height="38" rx="7" fill="#4a3000" stroke="#f59e0b"/><text x="280" y="275" text-anchor="middle" fill="#fdeccd">99</text>
    <rect x="330" y="250" width="60" height="38" rx="7" fill="#4a3000" stroke="#f59e0b"/><text x="360" y="275" text-anchor="middle" fill="#fdeccd">97</text>
    <rect x="410" y="250" width="60" height="38" rx="7" fill="#4a3000" stroke="#f59e0b"/><text x="440" y="275" text-anchor="middle" fill="#fdeccd">116</text>
  </g>

  <path d="M360,288 L360,306" stroke="#6b82a0" stroke-width="2" marker-end="url(#db)"/>
  <text x="60" y="332" fill="#6b82a0" font-family="sans-serif" font-size="11.5">bits — the true floor</text>
  <g font-family="monospace" font-size="12.5">
    <rect x="210" y="312" width="90" height="34" rx="6" fill="#053d28" stroke="#10b981"/><text x="255" y="334" text-anchor="middle" fill="#d3f5e6">01100011</text>
    <rect x="315" y="312" width="90" height="34" rx="6" fill="#053d28" stroke="#10b981"/><text x="360" y="334" text-anchor="middle" fill="#d3f5e6">01100001</text>
    <rect x="420" y="312" width="90" height="34" rx="6" fill="#053d28" stroke="#10b981"/><text x="465" y="334" text-anchor="middle" fill="#d3f5e6">01110100</text>
  </g>

  <text x="360" y="392" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11.5">Three friendly letters sit on top of three numbers, which sit on top of twenty-four bits.</text>
  <text x="360" y="410" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11.5">A model could read text at any of these layers. The question is: which layer makes learning easiest?</text>
</svg>
<figcaption><strong>Figure 2.</strong> Every character rests on a stack of representations. Working in raw bytes (the amber row) gives a permanently fixed vocabulary of just 256 symbols. It is tempting to stop here — but there is a hidden cost, and it is the cost that forces the whole field toward something cleverer.</figcaption>
</figure>

The hidden cost of bytes is *length*. In UTF-8, an ordinary English word is several bytes long, and a paragraph is thousands. If every byte is a symbol, then the sequence the model must chew through becomes very long indeed. And here we run into a fact that will echo through every later chapter of this book: the machinery that lets a model relate each symbol to every other symbol grows *quadratically* with sequence length. Double the number of symbols and you roughly quadruple the work. Sequence length is the single most expensive resource a language model has. Spending it one byte at a time is ruinous.

So we are caught between two pressures, and naming them precisely is the key to everything that follows.

<div class="keyidea">
💡 <strong>The central tension of tokenization.</strong> A <em>small</em> vocabulary (like 256 bytes) is simple and universal but produces <em>long</em> sequences, which are slow and expensive. A <em>large</em> vocabulary produces <em>short</em> sequences but demands more of the model and leaves rare symbols starved of examples. We do not want either extreme. We want a vocabulary sitting in a carefully chosen middle — large enough to keep sequences short, small enough to stay learnable. The art of tokenization is finding that middle. And, wonderfully, we do not choose the middle by hand. We let the data choose it.
</div>

<figure class="diagram">
<svg viewBox="0 0 720 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A seesaw showing the trade-off between vocabulary size and sequence length">
  <rect x="0" y="0" width="720" height="340" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="34" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">THE TRADE-OFF YOU CANNOT ESCAPE</text>

  <!-- fulcrum -->
  <path d="M360,250 L330,300 L390,300 Z" fill="#2a3f5f"/>
  <!-- beam tilted -->
  <g transform="rotate(-9 360 246)">
    <rect x="120" y="238" width="480" height="14" rx="7" fill="#6b82a0"/>
    <!-- left pan: small vocab -->
    <circle cx="180" cy="232" r="6" fill="#00d4f5"/>
    <rect x="70" y="150" width="220" height="70" rx="10" fill="#0a4a5c" stroke="#00d4f5" stroke-width="1.5"/>
    <text x="180" y="178" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="12.5" font-weight="bold">Small vocabulary</text>
    <text x="180" y="197" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="10.5">e.g. 256 bytes — universal, simple</text>
    <text x="180" y="212" text-anchor="middle" fill="#f87171" font-family="sans-serif" font-size="10.5">but sequences become very long</text>
    <!-- right pan: large vocab -->
    <circle cx="540" cy="232" r="6" fill="#f59e0b"/>
    <rect x="430" y="150" width="220" height="70" rx="10" fill="#4a3000" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="540" y="178" text-anchor="middle" fill="#fdeccd" font-family="sans-serif" font-size="12.5" font-weight="bold">Huge vocabulary</text>
    <text x="540" y="197" text-anchor="middle" fill="#f0c987" font-family="sans-serif" font-size="10.5">short sequences — cheap to run</text>
    <text x="540" y="212" text-anchor="middle" fill="#f87171" font-family="sans-serif" font-size="10.5">but rare tokens starve, params balloon</text>
  </g>

  <rect x="255" y="286" width="210" height="40" rx="10" fill="#053d28" stroke="#10b981" stroke-width="2"/>
  <text x="360" y="311" text-anchor="middle" fill="#d3f5e6" font-family="sans-serif" font-size="12" font-weight="bold">The goal: a learned middle (~100k)</text>
</svg>
<figcaption><strong>Figure 3.</strong> Every tokenizer is a chosen point on this seesaw. Modern models land near a vocabulary of one to two hundred thousand symbols — the empirically-discovered sweet spot where sequences are short enough to be affordable and the vocabulary is small enough that every symbol still appears often enough to be learned well.</figcaption>
</figure>

## Part III — The machine builds its own alphabet

Now comes the idea at the heart of this chapter, and it is genuinely lovely. We are not going to hand the model a vocabulary. We are going to let it *grow* one from the data, greedily, by noticing which combinations of symbols happen most often and promoting them to symbols in their own right.

The method is called **byte pair encoding**, or BPE, and once you see it you cannot unsee it. Start from the humble byte vocabulary — 256 symbols, one per possible byte. Now run through the entire clean corpus and ask a single question: *which pair of adjacent symbols occurs most frequently?* In English text the answer, early on, is something like the pair `t` followed by `h`. So we do the obvious, audacious thing: we invent a brand-new symbol — call it token number 256 — that *means* "th", and we replace every adjacent `t`,`h` in the corpus with this single new token. The corpus just got a little shorter, and our vocabulary just got one symbol larger.

Then we do it again. With "th" now a single symbol, perhaps the most common adjacent pair becomes "th" followed by `e` — so we mint token 257 meaning "the". Again the corpus shrinks; again the vocabulary grows. And again, and again, tens of thousands of times, each new symbol built from two older ones, each merge chosen purely because the data made that pair common.

<figure class="diagram">
<svg viewBox="0 0 720 470" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Byte pair encoding building larger tokens by repeatedly merging the most frequent adjacent pair">
  <defs>
    <marker id="dm" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9 z" fill="#f59e0b"/></marker>
  </defs>
  <rect x="0" y="0" width="720" height="470" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="34" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">BYTE PAIR ENCODING — GROWING A VOCABULARY</text>
  <text x="360" y="56" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11">corpus fragment: “ the theme of the theatre ”</text>

  <!-- Stage 0 -->
  <text x="40" y="96" fill="#6b82a0" font-family="sans-serif" font-size="11">start: every character is a symbol</text>
  <g font-family="monospace" font-size="13">
    <rect x="40"  y="106" width="26" height="30" rx="5" fill="#111827" stroke="#2a3f5f"/><text x="53"  y="126" text-anchor="middle" fill="#c9d6e8">t</text>
    <rect x="68"  y="106" width="26" height="30" rx="5" fill="#111827" stroke="#2a3f5f"/><text x="81"  y="126" text-anchor="middle" fill="#c9d6e8">h</text>
    <rect x="96"  y="106" width="26" height="30" rx="5" fill="#111827" stroke="#2a3f5f"/><text x="109" y="126" text-anchor="middle" fill="#c9d6e8">e</text>
    <rect x="132" y="106" width="26" height="30" rx="5" fill="#111827" stroke="#2a3f5f"/><text x="145" y="126" text-anchor="middle" fill="#c9d6e8">t</text>
    <rect x="160" y="106" width="26" height="30" rx="5" fill="#111827" stroke="#2a3f5f"/><text x="173" y="126" text-anchor="middle" fill="#c9d6e8">h</text>
    <rect x="188" y="106" width="26" height="30" rx="5" fill="#111827" stroke="#2a3f5f"/><text x="201" y="126" text-anchor="middle" fill="#c9d6e8">e</text>
    <rect x="216" y="106" width="26" height="30" rx="5" fill="#111827" stroke="#2a3f5f"/><text x="229" y="126" text-anchor="middle" fill="#c9d6e8">m</text>
    <rect x="244" y="106" width="26" height="30" rx="5" fill="#111827" stroke="#2a3f5f"/><text x="257" y="126" text-anchor="middle" fill="#c9d6e8">e</text>
    <text x="290" y="126" fill="#6b82a0" font-family="sans-serif" font-size="11">…and so on</text>
  </g>
  <text x="470" y="126" fill="#00d4f5" font-family="monospace" font-size="11">most frequent pair:  t + h</text>

  <path d="M360,146 L360,164" stroke="#f59e0b" stroke-width="2" marker-end="url(#dm)"/>

  <!-- Stage 1 -->
  <text x="40" y="186" fill="#6b82a0" font-family="sans-serif" font-size="11">merge 1 → new symbol “th”</text>
  <g font-family="monospace" font-size="13">
    <rect x="40"  y="196" width="40" height="30" rx="5" fill="#0a4a5c" stroke="#00d4f5"/><text x="60"  y="216" text-anchor="middle" fill="#d8f6fd">th</text>
    <rect x="82"  y="196" width="26" height="30" rx="5" fill="#111827" stroke="#2a3f5f"/><text x="95"  y="216" text-anchor="middle" fill="#c9d6e8">e</text>
    <rect x="118" y="196" width="40" height="30" rx="5" fill="#0a4a5c" stroke="#00d4f5"/><text x="138" y="216" text-anchor="middle" fill="#d8f6fd">th</text>
    <rect x="160" y="196" width="26" height="30" rx="5" fill="#111827" stroke="#2a3f5f"/><text x="173" y="216" text-anchor="middle" fill="#c9d6e8">e</text>
    <rect x="188" y="196" width="26" height="30" rx="5" fill="#111827" stroke="#2a3f5f"/><text x="201" y="216" text-anchor="middle" fill="#c9d6e8">m</text>
    <rect x="216" y="196" width="26" height="30" rx="5" fill="#111827" stroke="#2a3f5f"/><text x="229" y="216" text-anchor="middle" fill="#c9d6e8">e</text>
    <text x="290" y="216" fill="#6b82a0" font-family="sans-serif" font-size="11">…and so on</text>
  </g>
  <text x="470" y="216" fill="#00d4f5" font-family="monospace" font-size="11">most frequent pair:  th + e</text>

  <path d="M360,236 L360,254" stroke="#f59e0b" stroke-width="2" marker-end="url(#dm)"/>

  <!-- Stage 2 -->
  <text x="40" y="276" fill="#6b82a0" font-family="sans-serif" font-size="11">merge 2 → new symbol “the”</text>
  <g font-family="monospace" font-size="13">
    <rect x="40"  y="286" width="52" height="30" rx="5" fill="#053d28" stroke="#10b981"/><text x="66"  y="306" text-anchor="middle" fill="#d3f5e6">the</text>
    <rect x="98"  y="286" width="52" height="30" rx="5" fill="#053d28" stroke="#10b981"/><text x="124" y="306" text-anchor="middle" fill="#d3f5e6">the</text>
    <rect x="156" y="286" width="26" height="30" rx="5" fill="#111827" stroke="#2a3f5f"/><text x="169" y="306" text-anchor="middle" fill="#c9d6e8">m</text>
    <rect x="184" y="286" width="26" height="30" rx="5" fill="#111827" stroke="#2a3f5f"/><text x="197" y="306" text-anchor="middle" fill="#c9d6e8">e</text>
    <text x="290" y="306" fill="#6b82a0" font-family="sans-serif" font-size="11">…the corpus keeps shrinking</text>
  </g>

  <path d="M360,326 L360,344" stroke="#f59e0b" stroke-width="2" marker-end="url(#dm)"/>

  <rect x="120" y="352" width="480" height="90" rx="10" fill="#111827" stroke="#2a3f5f" stroke-width="1.5"/>
  <text x="360" y="378" text-anchor="middle" fill="#c9d6e8" font-family="sans-serif" font-size="12.5" font-weight="bold">…repeat tens of thousands of times</text>
  <text x="360" y="400" text-anchor="middle" fill="#8fd8b8" font-family="sans-serif" font-size="11">Common words become single symbols. Rare words remain in pieces.</text>
  <text x="360" y="418" text-anchor="middle" fill="#8fd8b8" font-family="sans-serif" font-size="11">The final vocabulary — for GPT-4, about 100,000 symbols — is the model's alphabet.</text>
  <text x="360" y="434" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="10.5">Note “ the” with its leading space would become its own symbol too — spaces travel with words.</text>
</svg>
<figcaption><strong>Figure 4.</strong> BPE in motion. Notice the direction of travel: we do not chop words up, we <em>build symbols up</em> from bytes, guided entirely by frequency. The words you use constantly collapse into single tokens; the words you rarely use stay fragmented. The vocabulary is a fossil record of how the training corpus was actually written.</figcaption>
</figure>

When this process halts — for GPT-4's tokenizer, at a vocabulary of 100,277 symbols; for its successor GPT-4o, closer to 200,000 — you are left with something remarkable. The most common English words are each a single symbol. Common word-fragments like "ing", "tion", "pre" are single symbols, so even a word the tokenizer has never seen can be assembled from familiar pieces. And genuinely rare strings — an unusual surname, a chemical name, a snippet of code — dissolve into several small tokens, or in the limit, back into individual bytes. Nothing is ever un-representable, because at the very bottom the byte layer can always spell anything out. The scheme is, to use the technical words, *lossless* and *reversible*: you can always reconstruct the exact original text from the tokens, byte for byte.

These learned symbols are what we call **tokens**, and from here on they are the true units of everything. Not words. Not letters. Tokens — the alphabet the machine assembled for itself, one greedy merge at a time.

<div class="callout">
🔧 <strong>For the tinkerers.</strong> This is not a black box you have to take on faith. OpenAI released the exact tokenizer their models use as an open-source library called <a href="https://github.com/openai/tiktoken">tiktoken</a>, and it ships with a small educational module that will walk the BPE merges in front of you, step by step, on any text you give it. If you know a little Python, an hour spent watching it build a vocabulary from a paragraph of your own writing will teach you more than this entire chapter. That is not false modesty; it is how I learned it myself.
</div>

## Part IV — Looking the tokenizer in the eye

Diagrams and prose can only take intuition so far. The thing that finally made tokenization *click* for me — and for nearly everyone I have taught it to — was seeing a real tokenizer chew on real text, live. So I am going to ask you to stop reading for a few minutes and go do exactly that.

The tool I send everyone to is [Tiktokenizer](https://tiktokenizer.vercel.app/). Open it, choose a model such as GPT-4o, and type into the box. As you type, the text is split into coloured tiles — one per token — with a running count and, if you look, the integer ID of each token. Type your name. Type a sentence. Type a paragraph of a clinic letter. Watch where the cuts fall. It is quietly mesmerising, and it will surface a series of facts that no amount of reading prepares you for. Let me walk you through the ones that matter most, because each one is a lesson in disguise.

**Lesson one: the boundaries are not where you expect.** Type `tokenization` and you may find it is not one token but two or three — perhaps `token` + `ization`. The tokenizer has no notion of "words." It only knows the fragments its merges happened to build. Common words are whole; longer or rarer ones fracture along the seams of frequency, not the seams of meaning.

**Lesson two: the space is part of the word.** This one surprises everyone. In the tokenizer's eyes, `world` and ` world` — the second with a leading space — are *different tokens with different ID numbers*. The space travels attached to the front of the word that follows it. It makes sense once you see it: in real text, words are almost always preceded by a space, so " world" is far more common than a bare "world", and BPE duly gave the spaced version its own symbol. But it means the model's internal notion of a word includes its leading whitespace, which is not how any human thinks about language.

<div class="tokrow">
<span style="color:#6b82a0">the sentence</span> <span style="color:#c9d6e8">“The patient took two tablets”</span> <span style="color:#6b82a0">becomes six tokens →</span><br/>
<span class="tok" style="background:#2e1e5e;color:#e8e3fa">The</span><span class="tok" style="background:#0a4a5c;color:#d8f6fd"> patient</span><span class="tok" style="background:#4a3000;color:#fdeccd"> took</span><span class="tok" style="background:#053d28;color:#d3f5e6"> two</span><span class="tok" style="background:#3d0f0f;color:#fde2e2"> tablets</span><span class="tok" style="background:#111827;color:#c9d6e8">”</span><br/>
<span style="color:#6b82a0; font-size:0.9em">every tile is one token · note the leading spaces riding along inside four of them</span>
</div>

**Lesson three: capitalisation makes a different symbol.** `Hello`, `hello`, `HELLO`, and ` Hello` are, as far as the tokenizer is concerned, four unrelated symbols. The model has to *learn* from scratch that they are related — that the capitalised form at the start of a sentence means the same thing as the lowercase form mid-sentence. Nothing about the tokens tells it so. This is our first glimpse of a recurring theme: the tokenizer hands the model a set of arbitrary symbols and forces it to rediscover, statistically, the relationships that are obvious to us.

**Lesson four: numbers are a mess.** Type `127 + 677 = 804` and watch what happens to the digits. You will very often find the numbers carved into ragged pieces — `127` might be one token while `677` splits into `67` and `7`, and `804` into `80` and `4`. There is no consistent "one token per digit" or "one token per number" rule; the cuts fall wherever the training frequencies happened to put them. Hold on to this observation. It is, as we will see in a moment, the reason a system that can write a sonnet can also insist that 9.11 is larger than 9.9.

**Lesson five: not all languages are equal.** Paste an English sentence and count the tokens. Now paste its translation into a language that was thin in the training data — Swahili, say, or Amharic — and count again. The second will use noticeably more tokens to say the same thing, sometimes two or three times as many. The tokenizer's merges were learned from a corpus dominated by English, so English got the efficient single-token words while other languages were left in smaller, more expensive pieces.

<figure class="diagram">
<svg viewBox="0 0 720 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The same sentence costs more tokens in an under-represented language">
  <rect x="0" y="0" width="720" height="300" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="34" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">THE SAME MEANING, A DIFFERENT PRICE</text>

  <text x="50" y="86" fill="#8fd8b8" font-family="sans-serif" font-size="12" font-weight="bold">English — well represented in training</text>
  <g>
    <rect x="50"  y="98" width="70" height="30" rx="5" fill="#053d28" stroke="#10b981"/>
    <rect x="124" y="98" width="70" height="30" rx="5" fill="#053d28" stroke="#10b981"/>
    <rect x="198" y="98" width="70" height="30" rx="5" fill="#053d28" stroke="#10b981"/>
    <rect x="272" y="98" width="70" height="30" rx="5" fill="#053d28" stroke="#10b981"/>
  </g>
  <text x="360" y="118" fill="#8fd8b8" font-family="monospace" font-size="12">4 tokens</text>

  <text x="50" y="170" fill="#f0c987" font-family="sans-serif" font-size="12" font-weight="bold">A low-resource language — the same sentence</text>
  <g>
    <rect x="50"  y="182" width="34" height="30" rx="5" fill="#4a3000" stroke="#f59e0b"/>
    <rect x="88"  y="182" width="34" height="30" rx="5" fill="#4a3000" stroke="#f59e0b"/>
    <rect x="126" y="182" width="34" height="30" rx="5" fill="#4a3000" stroke="#f59e0b"/>
    <rect x="164" y="182" width="34" height="30" rx="5" fill="#4a3000" stroke="#f59e0b"/>
    <rect x="202" y="182" width="34" height="30" rx="5" fill="#4a3000" stroke="#f59e0b"/>
    <rect x="240" y="182" width="34" height="30" rx="5" fill="#4a3000" stroke="#f59e0b"/>
    <rect x="278" y="182" width="34" height="30" rx="5" fill="#4a3000" stroke="#f59e0b"/>
    <rect x="316" y="182" width="34" height="30" rx="5" fill="#4a3000" stroke="#f59e0b"/>
    <rect x="354" y="182" width="34" height="30" rx="5" fill="#4a3000" stroke="#f59e0b"/>
    <rect x="392" y="182" width="34" height="30" rx="5" fill="#4a3000" stroke="#f59e0b"/>
  </g>
  <text x="440" y="202" fill="#f0c987" font-family="monospace" font-size="12">10+ tokens</text>

  <text x="360" y="262" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11.5">More tokens means: a shorter effective memory, higher cost per query, and — because the model saw those</text>
  <text x="360" y="280" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11.5">fragments less often — weaker fluency. The inequity in the data becomes an inequity in the tool.</text>
</svg>
<figcaption><strong>Figure 5.</strong> Tokenization efficiency is not a neutral technicality. Because the context window and the price are both measured in tokens, a language that tokenizes inefficiently is, in effect, charged more and remembered less. For anyone hoping to deploy these tools in the world's under-served languages, this is a design constraint to reckon with from day one — not a footnote.</figcaption>
</figure>

## Part V — Why the disassembly explains the machine

We now arrive at the payoff, the reason I insisted we spend a whole chapter on what looks like plumbing. A great many of the notorious, widely-mocked failures of language models are not failures of *intelligence* at all. They are direct, predictable consequences of the fact that the model never sees letters — it sees tokens. Once you hold that fact firmly, a whole category of mystery evaporates.

Consider the famous one: *how many times does the letter "r" appear in "strawberry"?* Models have stumbled on this for years, and every time they do, someone declares that artificial intelligence is a fraud. But look at what we now know. To the model, "strawberry" is not a row of ten letters. It is two or three tokens — perhaps ` straw` and `berry`. The individual letters are *welded inside* those tokens, invisible and inaccessible. Asking the model to count the r's is like asking you to count the brushstrokes in a painting you are only allowed to view from across the room. The information has been compressed away at the very first step. The wonder is not that it sometimes miscounts; the wonder is that it manages as often as it does, by having memorised, statistically, facts about its own tokens.

> The model does not read the way we read. It never meets the letter. It meets the token — and a token is a wall between the machine and the fine grain of the word.

The same lens clarifies the arithmetic troubles. We saw in Tiktokenizer that numbers fracture into inconsistent pieces. A model asked to add two numbers is therefore not manipulating digits in orderly columns the way a child is taught to; it is pattern-matching over lumpy, irregular tokens whose boundaries bear no relation to place value. That such systems can do *any* reliable arithmetic is a testament to how much structure they extract despite the tokenizer, not because of it. And it is precisely why serious systems now hand arithmetic off to a calculator tool rather than trusting the raw model — a theme we will return to when we discuss tools and agents.

<div class="callout">
⚕️ <strong>The clinical translation, because this is where it stops being a curiosity.</strong> If a model cannot reliably count the letters in "strawberry," think hard before trusting it to notice that "hydralazine" and "hydroxyzine" differ by a few characters, or to catch a transposed digit in a dose. The failure mode is not random; it is structural, and it lives at the tokenizer. This does not make the tools useless — it makes them tools with a known blind spot, to be wrapped in checks precisely where that blind spot bites. Knowing <em>why</em> the blind spot exists is the difference between deploying carefully and deploying blindly.
</div>

There is even a genre of outright bizarre behaviour that traces to tokenization: rare tokens that were minted during the vocabulary-building phase but then barely appeared in the actual training text. These "glitch tokens" — famous examples were dug out of early GPT models — are symbols the model possesses but was never taught to use, and prompting with them can produce strange, evasive, or nonsensical output, like pressing a key on a piano that was installed but never tuned. It is a small, eerie reminder that the vocabulary and the training are two separate steps, and that a symbol's mere existence does not guarantee the model knows what to do with it.

## Part VI — From tokens to the machine

Let us close by placing this chapter in the arc of the book. We began with the open internet and refined it, filter by filter, into a clean corpus. We then confronted the problem that a neural network reads only sequences of symbols, weighed the naive options, and arrived at byte pair encoding — the method by which the machine grows its own alphabet of tokens, balancing vocabulary size against sequence length. We looked a real tokenizer in the eye, and we saw how its quirks ripple outward into the model's most-mocked failures.

Everything from here on operates on tokens. When you read, in later chapters, that a model has a "context window" of, say, 128,000 — that number is counted in *tokens*, not words or characters, which is why the efficiency of tokenization directly determines how much real text the model can hold in mind at once. When we build the prediction machinery, its input will be a sequence of token IDs and its output will be a probability spread across the whole token vocabulary — "given these tokens, which token comes next?" The tokenizer is the lens through which the model views all of language, and, as with any lens, its particular distortions shape everything seen through it.

If you would like a preview of where these tokens are headed — the vast machine they are about to enter — there is a beautiful [interactive visualiser](https://bbycroft.net/llm) that renders a working language model in three dimensions and lets you walk through it, stage by stage, watching the numbers flow. Scroll all the way to the bottom of that machine, to where everything begins, and you will find our old friends waiting: a row of token IDs, the raw input, the grain of language from which all the apparent magic upstream is eventually built. I would not open it just yet — much of it will look like beautiful nonsense until we have built up to it together — but bookmark it. By the final chapter, every stage in that visualisation will be something you understand from the inside.

For now, sit with the central surprise of this chapter, because it is the seed of everything: a language model does not read our language at all. It reads a language it built for itself, out of the frequencies of our writing, one greedy merge at a time. Before it is a mind, or a tool, or a threat, or a marvel, it is a reader of tokens. And a token, we now know, is not a word. It is the grain into which we ground our words so that a machine could swallow them.

What did we lose in the grinding — and what, against all reasonable expectation, survived it? That question is the whole of the next chapter.

*— Neal*

<div class="chapter-banner">
📖 <strong>Next chapter:</strong> we take the stream of tokens this chapter produced and ask the question that turns a pile of text into a mind-like thing — <em>what comes next?</em> The answer is the engine at the centre of every language model, and we will build it from nothing.
</div>
