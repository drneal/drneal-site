---
title: "Anatomy of an AI Coding Agent"
date: 2026-07-10
category: AI Agents
tags: AI agents, agent loop, tool use, LLM, permissions, sub-agents, agentic coding, architecture
level: Intermediate
read_time: 30 min
summary: "Lesson 3 of Learning With Dr Neal. What separates a chatbot from an agent, the six building blocks every production agent shares, how a single request travels from your keystroke to the final answer, and how a permission system keeps an autonomous loop from wrecking your machine."
featured: false
---

<style>
.lesson-banner {
  font-size: 0.85em;
  background: linear-gradient(135deg, #1a237e 0%, #283593 100%);
  color: white;
  padding: 1.2em 1.6em;
  border-radius: 8px;
  margin: 1.5em 0;
  line-height: 1.6;
}
.lesson-banner a { color: #90caf9; font-weight: bold; }
.audio-section {
  font-size: 0.8em;
  background: #1a1f2e;
  border-left: 4px solid #1a237e;
  padding: 1em 1.4em;
  border-radius: 0 6px 6px 0;
  margin: 1.5em 0;
}
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
figure.diagram {
  margin: 2em 0;
  text-align: center;
}
figure.diagram svg {
  max-width: 100%;
  height: auto;
}
figure.diagram figcaption {
  font-size: 0.8em;
  color: #6b82a0;
  margin-top: 0.6em;
  text-align: left;
}
</style>

<div class="lesson-banner">
📚 <strong>Lessons series — #3.</strong> This lesson assumes you understand what a neural network is and roughly how an LLM predicts text. If you don't, start with <a href="/post/2026-06-19-how-deep-neural-networks-really-work">Lesson 1</a> and <a href="/post/2026-06-26-deep-learning-spreadsheet-exercise">Lesson 2</a>, then come back. The full curriculum lives on the <a href="/lessons">Lessons page</a>.
</div>

# Anatomy of an AI Coding Agent

In the first two lessons we went down to the metal: what a neural network actually computes, and how gradient descent tunes it. This lesson goes the other direction — up the stack — to answer a question I kept asking myself when I first watched a coding agent refactor one of my Flask projects on its own: *what is this thing, structurally?*

Not "how does the model work" — we covered that. The question is: what is wrapped **around** the model to turn a text predictor into something that reads your files, runs your tests, notices the tests failed, fixes the bug, and runs them again — without you touching the keyboard?

It turns out the answer is surprisingly compact. Strip away the polish and every serious coding agent — and there are now several in production use — is the same small set of parts arranged the same way. Once you can see those parts, agents stop being magic and start being *engineering*. That's the goal of this lesson.

<div class="audio-section">
  🎧 <strong>Listen to this post:</strong> The six organs of an autonomous agent — an audio companion to this lesson for the commute.<br/><br/>
  <audio controls style="width:100%; margin-top:0.4em;">
    <source src="https://pub-f57cd770c3d9448dafde9725cbc874b9.r2.dev/audio/Six_organs_of_an_autonomous_agent.m4a" type="audio/mp4">
    <a href="https://pub-f57cd770c3d9448dafde9725cbc874b9.r2.dev/audio/Six_organs_of_an_autonomous_agent.m4a">Download the audio</a>
  </audio>
</div>

<div class="audio-section">
  🎬 <strong>Watch the video overview:</strong> Anatomy of an AI agent in eight minutes — the visual companion to this lesson.<br/><br/>
  <video controls preload="metadata" style="width:100%; margin-top:0.4em; border-radius:6px;">
    <source src="https://pub-f57cd770c3d9448dafde9725cbc874b9.r2.dev/audio/Anatomy_of_an_AI_Agent.mp4" type="video/mp4">
    <a href="https://pub-f57cd770c3d9448dafde9725cbc874b9.r2.dev/audio/Anatomy_of_an_AI_Agent.mp4">Download the video</a>
  </video>
</div>

## A program that writes its own instructions

Start with what an agent is *not*.

A classic command-line program is a fixed function. You give `grep` a pattern and a file; it searches and exits. It never decides that, actually, what you really needed was to also edit the file. The sequence of operations is frozen at the moment the programmer wrote it. That's the contract we've had with software for seventy years: **the instructions are decided before the program runs**.

An agent tears that contract up. You hand it a goal in plain English — "add error handling to the login function" — and the sequence of operations is *invented at runtime* by a language model. The model reads the goal, decides it should first look at the file, then reads the result of that action, decides what to do next, and so on until it judges the job done.

Here's the reframe that made it click for me, as someone who has written a lot of conventional code:

<div class="keyidea">
💡 <strong>Key idea.</strong> In an agent, the LLM's output <em>is the control flow</em>. The "program" is just a loop that keeps asking the model "what next?" and executing whatever it answers. Everything else — the file access, the shell, the safety rails, the memory — is plumbing around that loop.
</div>

That loop has a name in the trade: the **agent loop** (you'll also hear "query loop" or "orchestration loop"). It's worth staring at, because it is genuinely the whole trick:

<figure class="diagram">
<svg viewBox="0 0 720 440" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The agent loop shown as a repeating cycle">
  <defs>
    <marker id="arrA" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L8,4.5 L0,9 z" fill="#00d4f5"/>
    </marker>
    <marker id="arrG" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L8,4.5 L0,9 z" fill="#10b981"/>
    </marker>
  </defs>
  <rect x="0" y="0" width="720" height="440" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="34" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">THE AGENT LOOP</text>

  <!-- Goal in -->
  <rect x="20" y="180" width="130" height="64" rx="10" fill="#2e1e5e" stroke="#a78bfa" stroke-width="1.5"/>
  <text x="85" y="207" text-anchor="middle" fill="#e8e3fa" font-family="sans-serif" font-size="13" font-weight="bold">Your goal</text>
  <text x="85" y="226" text-anchor="middle" fill="#bdaef0" font-family="sans-serif" font-size="11">plain English</text>

  <!-- Model node (top of cycle) -->
  <rect x="290" y="66" width="180" height="66" rx="10" fill="#0a4a5c" stroke="#00d4f5" stroke-width="1.5"/>
  <text x="380" y="94" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="13" font-weight="bold">Model thinks</text>
  <text x="380" y="113" text-anchor="middle" fill="#9fdcec" font-family="sans-serif" font-size="11">reads history → replies</text>

  <!-- Decision node (right) -->
  <rect x="520" y="187" width="170" height="66" rx="10" fill="#4a3000" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="605" y="214" text-anchor="middle" fill="#fdeccd" font-family="sans-serif" font-size="13" font-weight="bold">Any actions</text>
  <text x="605" y="233" text-anchor="middle" fill="#f0c987" font-family="sans-serif" font-size="13" font-weight="bold">requested?</text>

  <!-- Execute node (bottom) -->
  <rect x="290" y="308" width="180" height="66" rx="10" fill="#053d28" stroke="#10b981" stroke-width="1.5"/>
  <text x="380" y="336" text-anchor="middle" fill="#d3f5e6" font-family="sans-serif" font-size="13" font-weight="bold">Run the tools</text>
  <text x="380" y="355" text-anchor="middle" fill="#8fd8b8" font-family="sans-serif" font-size="11">read / edit / shell / search</text>

  <!-- Results node (left) -->
  <rect x="180" y="187" width="150" height="66" rx="10" fill="#111827" stroke="#2a3f5f" stroke-width="1.5"/>
  <text x="255" y="214" text-anchor="middle" fill="#c9d6e8" font-family="sans-serif" font-size="13" font-weight="bold">Results added</text>
  <text x="255" y="233" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11">to the transcript</text>

  <!-- Done -->
  <rect x="540" y="66" width="150" height="60" rx="10" fill="#053d28" stroke="#10b981" stroke-width="1.5"/>
  <text x="615" y="92" text-anchor="middle" fill="#d3f5e6" font-family="sans-serif" font-size="13" font-weight="bold">Done ✓</text>
  <text x="615" y="110" text-anchor="middle" fill="#8fd8b8" font-family="sans-serif" font-size="11">final answer shown</text>

  <!-- Arrows: goal -> results box start -->
  <path d="M150,212 L172,215" stroke="#a78bfa" stroke-width="2" fill="none" marker-end="url(#arrA)"/>
  <!-- results -> model (up-right) -->
  <path d="M270,187 Q290,130 282,110" stroke="#00d4f5" stroke-width="2" fill="none" marker-end="url(#arrA)"/>
  <!-- model -> decision -->
  <path d="M470,110 Q560,130 590,180" stroke="#00d4f5" stroke-width="2" fill="none" marker-end="url(#arrA)"/>
  <!-- decision (yes) -> execute -->
  <path d="M590,253 Q560,310 478,336" stroke="#f59e0b" stroke-width="2" fill="none" marker-end="url(#arrG)"/>
  <text x="580" y="300" fill="#f59e0b" font-family="monospace" font-size="12">yes</text>
  <!-- execute -> results -->
  <path d="M290,336 Q230,310 250,261" stroke="#10b981" stroke-width="2" fill="none" marker-end="url(#arrG)"/>
  <!-- decision (no) -> done -->
  <path d="M613,187 L615,133" stroke="#10b981" stroke-width="2" fill="none" marker-end="url(#arrG)"/>
  <text x="628" y="165" fill="#10b981" font-family="monospace" font-size="12">no</text>

  <text x="360" y="420" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11.5">The loop repeats — often dozens of times — until the model stops asking for actions.</text>
</svg>
<figcaption><strong>Figure 1.</strong> The agent loop. The model never "does" anything itself — it only writes requests. The loop executes them, feeds the outcomes back in, and asks again. Termination is the model's choice: a reply containing no action requests ends the cycle.</figcaption>
</figure>

Notice what's *absent* from Figure 1: there is no branch for "handle tool results". Results are simply appended to the running transcript and the model is called again with the longer transcript. The model sees what happened and reacts. That re-entrancy — one loop, no special cases — is what makes agents feel coherent across twenty-step tasks.

And notice how the loop ends. Nobody signals completion. The model just… stops requesting actions, and writes a final answer instead. The stop condition is a *behaviour*, not a flag. (Production agents add hard backstops — a turn limit, a token budget, a user abort — because a model that never stops requesting actions would loop forever and bill you for the privilege.)

## The six building blocks

If the loop is the heart, what's the rest of the organism? Having pulled apart several of these systems, I keep finding the same six organs, whatever the codebase calls them. Learn these six and you can navigate any agent's source — or design your own.

<figure class="diagram">
<svg viewBox="0 0 720 500" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Six building blocks arranged around the central agent loop">
  <rect x="0" y="0" width="720" height="500" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="34" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">SIX BUILDING BLOCKS</text>

  <!-- centre hub -->
  <circle cx="360" cy="265" r="62" fill="#0a4a5c" stroke="#00d4f5" stroke-width="2"/>
  <text x="360" y="260" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="13" font-weight="bold">Agent</text>
  <text x="360" y="278" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="13" font-weight="bold">Loop</text>

  <!-- spokes -->
  <line x1="360" y1="203" x2="360" y2="130" stroke="#2a3f5f" stroke-width="1.5"/>
  <line x1="308" y1="232" x2="185" y2="168" stroke="#2a3f5f" stroke-width="1.5"/>
  <line x1="412" y1="232" x2="535" y2="168" stroke="#2a3f5f" stroke-width="1.5"/>
  <line x1="308" y1="298" x2="185" y2="362" stroke="#2a3f5f" stroke-width="1.5"/>
  <line x1="412" y1="298" x2="535" y2="362" stroke="#2a3f5f" stroke-width="1.5"/>
  <line x1="360" y1="327" x2="360" y2="392" stroke="#2a3f5f" stroke-width="1.5"/>

  <!-- Interface (top) -->
  <rect x="280" y="66" width="160" height="62" rx="10" fill="#111827" stroke="#a78bfa" stroke-width="1.5"/>
  <text x="360" y="92" text-anchor="middle" fill="#e8e3fa" font-family="sans-serif" font-size="13" font-weight="bold">1 · Interface</text>
  <text x="360" y="110" text-anchor="middle" fill="#9f8fd0" font-family="sans-serif" font-size="10.5">where you type &amp; watch</text>

  <!-- Tools (upper left) -->
  <rect x="30" y="108" width="160" height="62" rx="10" fill="#111827" stroke="#10b981" stroke-width="1.5"/>
  <text x="110" y="134" text-anchor="middle" fill="#d3f5e6" font-family="sans-serif" font-size="13" font-weight="bold">2 · Toolbox</text>
  <text x="110" y="152" text-anchor="middle" fill="#7fb99f" font-family="sans-serif" font-size="10.5">every action it can take</text>

  <!-- Sub-agents (upper right) -->
  <rect x="530" y="108" width="160" height="62" rx="10" fill="#111827" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="610" y="134" text-anchor="middle" fill="#fdeccd" font-family="sans-serif" font-size="13" font-weight="bold">3 · Sub-agents</text>
  <text x="610" y="152" text-anchor="middle" fill="#c9a35f" font-family="sans-serif" font-size="10.5">loops inside the loop</text>

  <!-- State (lower left) -->
  <rect x="30" y="360" width="160" height="62" rx="10" fill="#111827" stroke="#00d4f5" stroke-width="1.5"/>
  <text x="110" y="386" text-anchor="middle" fill="#d8f6fd" font-family="sans-serif" font-size="13" font-weight="bold">4 · State</text>
  <text x="110" y="404" text-anchor="middle" fill="#6fa9bd" font-family="sans-serif" font-size="10.5">session facts &amp; UI data</text>

  <!-- Memory (lower right) -->
  <rect x="530" y="360" width="160" height="62" rx="10" fill="#111827" stroke="#f87171" stroke-width="1.5"/>
  <text x="610" y="386" text-anchor="middle" fill="#fde2e2" font-family="sans-serif" font-size="13" font-weight="bold">5 · Memory</text>
  <text x="610" y="404" text-anchor="middle" fill="#c98a8a" font-family="sans-serif" font-size="10.5">notes that survive sessions</text>

  <!-- Hooks (bottom) -->
  <rect x="280" y="392" width="160" height="62" rx="10" fill="#111827" stroke="#a78bfa" stroke-width="1.5"/>
  <text x="360" y="418" text-anchor="middle" fill="#e8e3fa" font-family="sans-serif" font-size="13" font-weight="bold">6 · Hooks</text>
  <text x="360" y="436" text-anchor="middle" fill="#9f8fd0" font-family="sans-serif" font-size="10.5">your rules, auto-enforced</text>

  <text x="360" y="482" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11.5">Everything else in a production agent — renderers, cost meters, config — exists to serve these six.</text>
</svg>
<figcaption><strong>Figure 2.</strong> The six recurring components of a production coding agent, arranged around the loop they all serve. The names vary between products; the roles don't.</figcaption>
</figure>

**1. The interface.** The surface you interact with — a terminal UI, an editor pane, a chat window. Its only real job is to feed your input into the loop and stream the loop's output back to you. A well-built agent keeps this layer thin, which is why the same core can drive a terminal, an IDE plugin, and a headless script-mode with no changes underneath.

**2. The toolbox.** A tool is any action the model can request: read a file, write a file, run a shell command, search the web, grep the codebase. The design insight that separates good agents from fragile ones is that a tool is *not just a function*. Each tool carries its own metadata: a schema describing its inputs, a declaration of whether it's safe to run in parallel with others, its own permission rules, and instructions for how its output should be displayed. The tool describes itself; the loop stays generic. Add a forty-first tool and you touch zero lines of orchestration code. Compare that with the alternative — a central dispatcher with a growing `if/else` chain that "knows about" every tool — and you can see why self-description wins as systems grow.

**3. Sub-agents.** Here's the recursive move: one of the tools in the toolbox is *"spawn another agent"*. The child gets its own fresh transcript, its own (possibly restricted) toolbox, and runs its own copy of the same loop. The parent sees only the child's final report. This is how an agent parallelises a big refactor or delegates "go research how this library works" without polluting its own context window. The crucial design rule: a sub-agent is the *same loop*, not a special-cased mini-version — so it inherits every guarantee (permissions, limits, error handling) automatically. Sub-agents live through a simple lifecycle — queued, running, then finished, failed, or cancelled — which the parent can inspect at any time.

**4. State.** Agents keep two very different kinds of state, and mature systems keep them physically separate. First, *session infrastructure*: working directory, which model is in use, accumulated cost, session ID. Set once at startup, read constantly, changed rarely — a plain mutable object is fine. Second, *live UI state*: the message stream, pending approvals, progress spinners. This changes many times a second and must push updates to the screen, so it lives in a small reactive store. Mixing the two is a classic beginner error: make everything reactive and you pay subscription overhead on data that changes once; make nothing reactive and your UI goes stale.

**5. Memory.** The context window is amnesiac — wipe the session and the agent forgets your project's conventions, your preferred test framework, that painful debugging discovery from last Tuesday. Memory fixes this with plain markdown files at several scopes: per-project notes checked into the repo, personal notes in your home directory, shared notes for a team. The elegant part is *retrieval*: at session start the agent doesn't dump every note into context (that would burn the window). Instead a cheap model call skims the available notes and selects only those relevant to the current task. Memory is, in effect, a tiny retrieval-augmented system bolted onto the agent — same principle as RAG in clinical NLP, applied to the agent's own notes-to-self.

**6. Hooks.** User-defined tripwires at fixed points in the lifecycle: before a tool runs, after it finishes, when the loop is about to stop, and a couple of dozen more. A hook can be a shell script, a one-shot LLM check, or a webhook — and it can *block* the action, rewrite its inputs, inject extra context, or halt the whole loop. Hooks are how you encode "never touch the production config" or "always run the linter after edits" as enforced policy rather than a polite request in a prompt. That distinction matters more than it looks: prompts are suggestions the model usually follows; hooks are code, and code doesn't get creative.

<div class="callout">
⚕️ <strong>A medical analogy that holds up well:</strong> the loop is the cardiac cycle; the toolbox is the motor system; state is the working memory of the moment; memory files are the patient record; hooks are the spinal reflexes that act before conscious thought; and sub-agents are the referral — sending a well-defined question to a colleague and getting back a report, not their whole thought process.
</div>

## The life of a single request

Abstractions are only useful if you can follow a concrete case through them. So: you type *"add error handling to the login function"* and press Enter. What actually happens?

<figure class="diagram">
<svg viewBox="0 0 720 480" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Timeline of one request through the agent">
  <rect x="0" y="0" width="720" height="480" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="34" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">ONE REQUEST, STEP BY STEP</text>

  <!-- time axis -->
  <line x1="70" y1="70" x2="70" y2="440" stroke="#2a3f5f" stroke-width="2"/>
  <text x="52" y="80" text-anchor="end" fill="#6b82a0" font-family="monospace" font-size="11">t=0</text>
  <text x="52" y="438" text-anchor="end" fill="#6b82a0" font-family="monospace" font-size="11">done</text>

  <!-- step 1 -->
  <circle cx="70" cy="90" r="5" fill="#a78bfa"/>
  <rect x="95" y="72" width="590" height="36" rx="8" fill="#111827" stroke="#a78bfa"/>
  <text x="110" y="95" fill="#e8e3fa" font-family="sans-serif" font-size="12.5"><tspan font-weight="bold">1 · Housekeeping.</tspan> Transcript too long? Summarise older turns first ("compaction").</text>

  <!-- step 2 -->
  <circle cx="70" cy="140" r="5" fill="#00d4f5"/>
  <rect x="95" y="122" width="590" height="36" rx="8" fill="#111827" stroke="#00d4f5"/>
  <text x="110" y="145" fill="#d8f6fd" font-family="sans-serif" font-size="12.5"><tspan font-weight="bold">2 · Model call.</tspan> Full transcript sent; the reply streams back token by token.</text>

  <!-- step 3 with overlap band -->
  <circle cx="70" cy="190" r="5" fill="#10b981"/>
  <rect x="95" y="172" width="590" height="52" rx="8" fill="#053d28" stroke="#10b981"/>
  <text x="110" y="193" fill="#d3f5e6" font-family="sans-serif" font-size="12.5"><tspan font-weight="bold">3 · Eager start.</tspan> Mid-stream, a read-only request appears — e.g. "open login.py".</text>
  <text x="110" y="212" fill="#8fd8b8" font-family="sans-serif" font-size="12">Safe tools start <tspan font-weight="bold">while the model is still talking</tspan>. Reads overlap the stream.</text>

  <!-- step 4 -->
  <circle cx="70" cy="252" r="5" fill="#f59e0b"/>
  <rect x="95" y="234" width="590" height="52" rx="8" fill="#111827" stroke="#f59e0b"/>
  <text x="110" y="255" fill="#fdeccd" font-family="sans-serif" font-size="12.5"><tspan font-weight="bold">4 · Remaining actions run.</tspan> Parallel-safe ones together; risky ones one at a time.</text>
  <text x="110" y="274" fill="#c9a35f" font-family="sans-serif" font-size="12">Each action passes: validate → hooks → permission check → execute.</text>

  <!-- step 5 -->
  <circle cx="70" cy="314" r="5" fill="#00d4f5"/>
  <rect x="95" y="296" width="590" height="36" rx="8" fill="#111827" stroke="#00d4f5"/>
  <text x="110" y="319" fill="#d8f6fd" font-family="sans-serif" font-size="12.5"><tspan font-weight="bold">5 · Feedback.</tspan> All results are appended to the transcript as new messages.</text>

  <!-- step 6 -->
  <circle cx="70" cy="364" r="5" fill="#f87171"/>
  <rect x="95" y="346" width="590" height="36" rx="8" fill="#111827" stroke="#f87171"/>
  <text x="110" y="369" fill="#fde2e2" font-family="sans-serif" font-size="12.5"><tspan font-weight="bold">6 · Loop test.</tspan> More actions requested? → back to step 2 with the longer transcript.</text>

  <!-- step 7 -->
  <circle cx="70" cy="414" r="5" fill="#10b981"/>
  <rect x="95" y="396" width="590" height="36" rx="8" fill="#053d28" stroke="#10b981"/>
  <text x="110" y="419" fill="#d3f5e6" font-family="sans-serif" font-size="12.5"><tspan font-weight="bold">7 · Finish.</tspan> No actions requested — the reply is the answer. The loop reports <tspan font-family="monospace">why</tspan> it ended.</text>

  <text x="360" y="462" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11.5">Steps 2–6 typically repeat several times per user request. Step 3 is the speed trick most people never notice.</text>
</svg>
<figcaption><strong>Figure 3.</strong> The lifecycle of one request. The green band at step 3 is the subtle part: tool execution and model streaming overlap in time rather than strictly alternating.</figcaption>
</figure>

Three details in that timeline repay attention.

**The loop is a producer you pull from, not a callback that pushes at you.** Implementation-wise, the loop is typically written as a generator — a function that *yields* a stream of messages which the interface consumes at its own pace. If the UI falls behind, the generator naturally pauses; if you hit Escape, the consumer simply stops pulling and the loop winds down cleanly. And when the loop finishes, it returns a typed reason: completed normally, aborted by user, ran out of token budget, hit the turn limit, or halted by a hook. Compare that to a tangle of callbacks where "why did it stop?" is a debugging session. This is a beautiful example of a general lesson: *choose the language construct whose shape matches your problem*, and half your edge cases evaporate.

**Speculative tool execution.** In step 3, the agent starts running read-only tools *before the model has finished its sentence*. By the time the model's reply is complete, the file contents it asked for may already be sitting in hand. It's a small gamble — very occasionally the rest of the model's output invalidates the request and the result is thrown away — but reads are cheap and latency is the thing users feel most. Anaesthetists will recognise the pattern: you draw up the likely drugs before you're certain you'll need them, because the cost of being wrong is small and the cost of waiting is not.

**No separate "result-handling" phase.** Step 5 is just an append. The intelligence about *what the results mean* lives entirely in the model, which reads them on the next pass. The plumbing stays dumb; the model stays smart. Whenever you find yourself writing clever result-interpretation logic in the loop itself, you're probably duplicating — badly — something the model would do better.

## The safety problem: permissions

Everything above should make you slightly nervous. We've built a system where a stochastic text generator decides which shell commands run on your machine. It can edit files, hit the network, and rewrite git history. The gap between "useful colleague" and "rm -rf incident" is exactly one badly-chosen tool call wide.

The answer every mature agent converges on is a **permission system**, and its two components are worth understanding because you'll be configuring them, not just admiring them.

First, **modes** — named postures that set the overall trust level for a session. Rather than sprinkling ad-hoc `if allowed` checks through every tool, the agent resolves *every* action through the currently active mode. Typical postures, from paranoid to reckless: a **read-only/planning mode** where all mutations are blocked (lovely for "look at my codebase and propose a plan" sessions); a **default interactive mode** where each risky action needs your explicit yes; an **auto-accept-edits mode** where file edits sail through but shell commands still prompt; an **auto mode** where a second, lightweight LLM reviews each proposed action against the conversation and approves the ones consistent with what you asked for; and an unrestricted mode for sandboxes and CI, which you should treat like an unblinded trial — legitimate, but only in controlled conditions.

Second, the **resolution chain** — the fixed order in which an individual action gets judged:

<figure class="diagram">
<svg viewBox="0 0 720 400" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Permission resolution chain">
  <defs>
    <marker id="arrW" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L8,4.5 L0,9 z" fill="#6b82a0"/>
    </marker>
  </defs>
  <rect x="0" y="0" width="720" height="400" rx="12" fill="#0d1424" stroke="#1e2d45"/>
  <text x="360" y="34" text-anchor="middle" fill="#c9d6e8" font-family="monospace" font-size="16" font-weight="bold">WHO DECIDES? — THE PERMISSION CHAIN</text>

  <!-- Stage 1 -->
  <rect x="30" y="70" width="200" height="86" rx="10" fill="#111827" stroke="#a78bfa" stroke-width="1.5"/>
  <text x="130" y="97" text-anchor="middle" fill="#e8e3fa" font-family="sans-serif" font-size="13" font-weight="bold">① Your hooks</text>
  <text x="130" y="117" text-anchor="middle" fill="#9f8fd0" font-family="sans-serif" font-size="11">Hard rules fire first.</text>
  <text x="130" y="133" text-anchor="middle" fill="#9f8fd0" font-family="sans-serif" font-size="11">A match settles it — no appeal.</text>

  <!-- Stage 2 -->
  <rect x="260" y="70" width="200" height="86" rx="10" fill="#111827" stroke="#10b981" stroke-width="1.5"/>
  <text x="360" y="97" text-anchor="middle" fill="#d3f5e6" font-family="sans-serif" font-size="13" font-weight="bold">② The tool itself</text>
  <text x="360" y="117" text-anchor="middle" fill="#7fb99f" font-family="sans-serif" font-size="11">Each tool knows its own risk.</text>
  <text x="360" y="133" text-anchor="middle" fill="#7fb99f" font-family="sans-serif" font-size="11">It may allow, deny, or say "ask".</text>

  <!-- Stage 3 -->
  <rect x="490" y="70" width="200" height="86" rx="10" fill="#111827" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="590" y="97" text-anchor="middle" fill="#fdeccd" font-family="sans-serif" font-size="13" font-weight="bold">③ The active mode</text>
  <text x="590" y="117" text-anchor="middle" fill="#c9a35f" font-family="sans-serif" font-size="11">Session posture decides how</text>
  <text x="590" y="133" text-anchor="middle" fill="#c9a35f" font-family="sans-serif" font-size="11">"ask" cases are handled.</text>

  <path d="M230,113 L252,113" stroke="#6b82a0" stroke-width="2" marker-end="url(#arrW)"/>
  <path d="M460,113 L482,113" stroke="#6b82a0" stroke-width="2" marker-end="url(#arrW)"/>

  <!-- outcomes row -->
  <path d="M590,156 L590,190 L130,190 L130,208" stroke="#6b82a0" stroke-width="1.5" fill="none" marker-end="url(#arrW)"/>
  <path d="M590,156 L590,190 L360,190 L360,208" stroke="#6b82a0" stroke-width="1.5" fill="none" marker-end="url(#arrW)"/>
  <path d="M590,156 L590,208" stroke="#6b82a0" stroke-width="1.5" fill="none" marker-end="url(#arrW)"/>

  <rect x="40" y="214" width="180" height="76" rx="10" fill="#053d28" stroke="#10b981" stroke-width="1.5"/>
  <text x="130" y="242" text-anchor="middle" fill="#d3f5e6" font-family="sans-serif" font-size="13" font-weight="bold">✓ Allowed</text>
  <text x="130" y="262" text-anchor="middle" fill="#8fd8b8" font-family="sans-serif" font-size="11">Runs immediately.</text>
  <text x="130" y="278" text-anchor="middle" fill="#8fd8b8" font-family="sans-serif" font-size="11">Still logged.</text>

  <rect x="270" y="214" width="180" height="76" rx="10" fill="#4a3000" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="360" y="242" text-anchor="middle" fill="#fdeccd" font-family="sans-serif" font-size="13" font-weight="bold">? You're asked</text>
  <text x="360" y="262" text-anchor="middle" fill="#f0c987" font-family="sans-serif" font-size="11">Approve once, for the session,</text>
  <text x="360" y="278" text-anchor="middle" fill="#f0c987" font-family="sans-serif" font-size="11">always — or refuse.</text>

  <rect x="500" y="214" width="180" height="76" rx="10" fill="#3d0f0f" stroke="#f87171" stroke-width="1.5"/>
  <text x="590" y="242" text-anchor="middle" fill="#fde2e2" font-family="sans-serif" font-size="13" font-weight="bold">✗ Blocked</text>
  <text x="590" y="262" text-anchor="middle" fill="#e2a0a0" font-family="sans-serif" font-size="11">The model is told no —</text>
  <text x="590" y="278" text-anchor="middle" fill="#e2a0a0" font-family="sans-serif" font-size="11">and must plan around it.</text>

  <!-- sub-agent note -->
  <rect x="40" y="316" width="640" height="52" rx="10" fill="#111827" stroke="#2a3f5f" stroke-width="1.5"/>
  <text x="360" y="338" text-anchor="middle" fill="#c9d6e8" font-family="sans-serif" font-size="12" font-weight="bold">Sub-agent rule: children can't approve their own risky actions.</text>
  <text x="360" y="356" text-anchor="middle" fill="#6b82a0" font-family="sans-serif" font-size="11.5">Requests escalate upward — to the parent agent, and ultimately to you. Nothing dangerous happens out of sight.</text>
</svg>
<figcaption><strong>Figure 4.</strong> How one proposed action gets judged. Deterministic user rules outrank the tool's own assessment, which outranks the session's mode. Whatever the route, the outcome is one of three colours.</figcaption>
</figure>

The ordering is the point. Your explicit rules (hooks) always win. The tool's self-assessment comes next — a file-read can wave itself through; a shell command mostly can't. Only the ambiguous residue reaches the mode, which decides whether that means "ask the human", "ask a reviewing model", or "allow and log".

The sub-agent rule at the bottom of Figure 4 deserves a highlight, because it's the kind of thing you only think of after an incident: a child agent must **escalate** permission requests up to its parent rather than approve its own. Without this, delegation becomes a laundering scheme — the parent spawns a child precisely because the child would face no prompts. With it, autonomy stays bounded no matter how deep the recursion goes.

<div class="callout">
⚠️ <strong>Practical note.</strong> When you first run a coding agent, resist the temptation to switch off the prompts because they're annoying. Run in default mode for a week and <em>read what it asks you</em>. You'll build an accurate mental model of what the agent actually tries to do — which is exactly the calibration you need before granting it more autonomy. Trust is earned on both sides of this relationship.
</div>

## One model, many doorways

A short but practically important detail. Production agents rarely hard-code *how* they reach the model. The same request might travel to the provider's API directly, or through an enterprise cloud platform (AWS, Google, Azure all resell frontier models behind their own authentication). Well-architected agents hide this behind a single factory: at startup, configuration decides which doorway to use, a client is constructed with a common interface, and *nothing else in the system ever knows the difference*. The loop, the tools, the permissions — all provider-agnostic.

Why should you care? Because it's the pattern to copy whenever you integrate LLMs into your own work. If your hospital's data-governance team insists on the Azure route while your prototype used the direct API, that switch should be one line of config — not surgery. Design the seam in from day one.

## Design rules worth stealing

I want to close the loop back to *your* projects — many readers of this series are scientists and clinicians who will end up building small agentic tools of their own (my drug-interaction pipeline is already halfway there). Here are the transferable rules, distilled:

**Make the loop the only loop.** Sub-agents, headless scripts, chat UIs — every entry point should drive the *same* loop function. The moment you fork a "lite" variant, behaviours diverge and bugs breed in the gap.

**Let tools describe themselves.** Schema, risk level, parallel-safety, display format — attached to the tool, not centralised in the orchestrator. Your future self, adding tool number twelve, will thank you.

**Split calm state from busy state.** Configuration set once at startup goes in a plain object. Rapidly-changing display state goes in a reactive store. Two access patterns, two containers.

**Name your trust levels.** A handful of explicit permission modes beats a hundred scattered checks. When something goes wrong at 2 a.m., "which mode was active?" is answerable; "which of the hundred checks misfired?" is not.

**Escalate, don't self-approve.** Any delegated worker — sub-agent, background job, cron task — routes its dangerous decisions upward. Autonomy is granted, never assumed.

**Prefer files over databases for memory.** Markdown notes that a human can read, edit, and version-control turn out to be a superb memory substrate — and letting a cheap model select which notes matter at session start keeps the context window lean.

None of these requires a research lab. They're just good engineering, discovered under the pressure of making agents work for real users — and they compose into systems that feel far more capable than any single part suggests.

## What's next

We now have both ends of the stack: neurons and gradients at the bottom (Lessons 1–2), and the agent architecture at the top (this lesson). The obvious gap is the middle — the **transformer**: how a language model actually turns a transcript into the next token, why attention was such a breakthrough, and what "context window" physically means. That's where this series goes next — in fact, [Lesson 4 is now live](/post/2026-07-10-inside-the-transformer). We'll build one, piece by piece, small enough to train yourself.

Until then: the next time you watch an agent quietly read three files, run your tests, and fix the failure — you'll know exactly which of the six organs just fired, and in what order.

*— Neal*

<div class="lesson-banner">
📚 <strong>Continue the series:</strong> all lessons, in order, on the <a href="/lessons">Lessons page</a>.
</div>
