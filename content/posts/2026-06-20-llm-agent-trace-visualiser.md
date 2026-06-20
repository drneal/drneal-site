---
title: "LLM Agent Trace Visualiser: Debugging Multi-Step AI Agents Step by Step"
date: 2026-06-20
category: AI Engineering
tags: LLM agents, Claude API, OpenAI, tool use, observability, debugging, multi-agent, token usage, extended thinking, Flask, JavaScript
level: Intermediate
read_time: 12 min
summary: How the LLM Agent Trace Visualiser works — parsing Claude and OpenAI API traces, normalising tool_use and tool_result blocks, rendering extended thinking, and what agent observability requires in production beyond a timeline viewer.
featured: false
---

*The tool is live at [/agent-trace](/agent-trace). Paste any Claude or OpenAI agent session JSON. The sample trace loads automatically — a six-step clinical agent that calls NLP extraction, drug interaction checking, and synthesises a prioritised clinical summary with extended thinking.*

---

When a multi-step LLM agent fails — loops, hallucinates a tool call, produces wrong output, or simply spends ten times the expected tokens — the first question is always: *where exactly did it go wrong?* The raw JSON that comes back from the Anthropic or OpenAI API contains everything needed to answer that question, but reading nested JSON by hand at scale is tedious, and the information you actually care about (what did the model think before calling that tool? what did the tool return? which step burned the most tokens?) is buried under several layers of structure.

The LLM Agent Trace Visualiser solves one specific problem: making a raw API trace human-readable without losing any of the information it contains.

## What the Anthropic Messages API Actually Returns

The Anthropic Messages API uses a structured messages format where each message has a `role` (`user` or `assistant`) and a `content` field that can be a plain string or an array of typed blocks. Understanding this block structure is essential for parsing agent traces correctly.

An assistant message in an agentic context typically looks like this:

```json
{
  "role": "assistant",
  "content": [
    {
      "type": "thinking",
      "thinking": "The user wants drug interaction screening. I should first extract the medication list via the NLP tool, then check all pairs. Warfarin + amiodarone is the most urgent concern..."
    },
    {
      "type": "text",
      "text": "I'll start by extracting the medications, then check all pairwise interactions."
    },
    {
      "type": "tool_use",
      "id": "toolu_01NlpExtract",
      "name": "nlp_extractor",
      "input": {
        "text": "Warfarin 5mg OD, Amiodarone 200mg OD..."
      }
    }
  ],
  "usage": {
    "input_tokens": 312,
    "output_tokens": 203
  }
}
```

The `thinking` block is an extended thinking block — Claude's internal reasoning prior to generating a response. It is only present when the `extended_thinking` feature is enabled on the API call. Extended thinking gives you visibility into the chain-of-thought that influenced the tool call or the text response that follows.

The tool result comes back in the next user message, paired to the tool call by matching `tool_use_id`:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01NlpExtract",
      "content": "{\"medications\":[\"warfarin\",\"amiodarone\",...],\"total_entities\":16}"
    }
  ]
}
```

Note that tool result messages have `role: "user"` — the tool result is technically returned to the model as a user turn, which is why in a multi-turn agent loop the conversation alternates: assistant → tool_use → user (tool_result) → assistant → tool_use → user (tool_result) → ... → assistant (final response).

## OpenAI's Parallel Structure

The OpenAI Chat Completions API uses a different field structure for the same concept. Tool calls appear in a `tool_calls` array at the message level rather than inside the `content` array:

```json
{
  "role": "assistant",
  "content": "I'll extract the medications first.",
  "tool_calls": [
    {
      "id": "call_abc123",
      "type": "function",
      "function": {
        "name": "nlp_extractor",
        "arguments": "{\"text\": \"Warfarin 5mg OD...\"}"
      }
    }
  ]
}
```

Note that `function.arguments` is a JSON string (not a parsed object), which requires an additional `JSON.parse()` step. Tool results use `role: "tool"` rather than `role: "user"` with a `tool_result` content block:

```json
{
  "role": "tool",
  "tool_call_id": "call_abc123",
  "content": "{\"medications\":[\"warfarin\",...],\"total\":8}"
}
```

The visualiser's backend parser (`_parse_agent_trace()` in `app.py`) normalises both formats into the same internal step structure before sending data to the frontend. This is the only server-side work — once normalised, all rendering is client-side JavaScript.

## What the Parser Does

The normalisation function takes a raw trace in any of four formats and emits a unified list of steps, each containing:

- `role`: user / assistant / tool / system
- `blocks`: array of typed content blocks (text, thinking, tool_use, tool_result), all normalised to a common schema
- `input_tokens` / `output_tokens`: from the usage field if present

The key parsing decisions:

**Tool argument deserialisation.** OpenAI serialises tool call arguments as a JSON string. The parser detects strings and attempts `json.loads()`; if that fails (malformed JSON from a streaming partial completion), it wraps the raw string as `{"raw": "..."}` rather than raising an exception.

**Tool result content normalisation.** Claude's `tool_result` content field can be a string, a list of typed text blocks, or a list containing images and text mixed. The parser flattens list content to a single concatenated string for display.

**Format detection heuristics.** The parser checks for the presence of key fields in the following order: `messages` key (messages-array wrapper) → `choices` key (OpenAI completion response) → `role` key at top level (single Anthropic response) → list (raw messages array). Unknown formats raise a descriptive error rather than silently returning empty results.

**Token accounting.** Anthropic uses `input_tokens`/`output_tokens`; OpenAI uses `prompt_tokens`/`completion_tokens` at the top-level usage object. The parser checks both. Token counts are accumulated across all messages for the totals in the metadata strip.

## Why Agent Observability Is Harder Than It Looks

A trace visualiser is the simplest form of agent observability. In production, it is necessary but not sufficient.

**What a visualiser gives you:** the ability to inspect a single trace after the fact — to see which tool was called, what inputs it received, what it returned, and how many tokens each step consumed. This is useful for debugging individual failures and for understanding the general structure of an agent's behaviour.

**What production observability requires beyond this:**

*Latency per step.* The trace format from both APIs does not include timestamps. You need to instrument your agent loop to capture wall-clock time at each `messages.create()` call. Latency matters enormously in clinical and agentic contexts: a tool that takes 8 seconds to respond versus 400ms will dominate user experience.

*Sampling and aggregation.* Single-trace inspection doesn't reveal patterns. You need to aggregate across hundreds or thousands of traces to find systemic issues: tools that fail at a 3% rate, specific input patterns that cause hallucinated tool calls, token spend that correlates with input length in a non-linear way.

*Streaming support.* Neither the Anthropic nor OpenAI streaming response formats emit complete `usage` blocks until the final chunk. If you're using streaming (essential for any user-facing agent), you need to reconstruct the full message from the stream before logging the trace.

*Ground truth evaluation.* A trace showing the right tool calls in the right order does not mean the final answer was correct. Trace logging needs to be paired with output evaluation — either human review or automated assertion checks — to detect semantic failures that don't manifest as obvious structural errors.

Production tooling that handles all of this — [LangSmith](https://smith.langchain.com), [Weights & Biases Weave](https://wandb.ai/site/weave), [Arize Phoenix](https://phoenix.arize.com) — is worth evaluating for any agent deployed beyond a single-user prototype. The visualiser in this demo handles the "inspect one trace" use case; those platforms handle the rest.

## The Sample Trace: A Clinical Agent in Six Steps

The sample trace that loads on page open demonstrates a clinical agent workflow built on the tools already in this site:

**Step 1 (user):** A query asking the agent to analyse a 74-year-old patient's 8-drug medication list for interactions and produce a clinical summary.

**Step 2 (assistant):** Extended thinking reveals the model's pre-call reasoning — immediately identifying the warfarin + amiodarone combination as the highest-priority concern before any tool is called. This is followed by a brief text turn explaining the planned approach, then a `tool_use` block calling `nlp_extractor` with the raw medication string.

**Step 3 (user, tool_result):** The NLP extractor returns 8 normalised medication names and 16 total entities (medications + dosages).

**Step 4 (assistant):** A second tool call to `drug_interaction_checker` with the extracted medication array, requesting mechanism details.

**Step 5 (user, tool_result):** 5 major interactions returned, all with mechanism, clinical effect, and recommended management action.

**Step 6 (assistant):** Another thinking block — the model prioritises the interactions before writing — followed by the final clinical summary, structured by urgency tier (urgent today / within 1 week / at next review).

The total token spend across the 6 messages is approximately 1,750 tokens. The two tool calls add no tokens to the count (tool execution happens outside the context window), but each tool result re-enters the context as a user message, growing the context linearly with each round-trip.

## Token Economics of Multi-Step Agents

One of the most practically useful aspects of trace visualisation is exposing the token accounting of multi-step agents. The pattern that surprises most engineers who haven't built production agents before: **input tokens grow with every step**.

In a six-step conversation:
- Step 1 (user): 120 input tokens
- Step 2 (assistant): 120 + 190 (assistant text) = 310 input tokens
- Step 3 (user, tool result): 310 + assistant step + 250 (tool result) = 750 input tokens
- Step 4 (assistant): 750 + tool result = ~900 input tokens
- Step 5 (user, tool result): 900 + assistant step + 600 (tool result) = ~1,700 input tokens
- Step 6 (assistant): ~1,700 input tokens just to generate the final response

The full context of every prior step is re-sent with each API call. This means the input token cost of a k-step agent grows as O(k²) in the worst case (if each step adds a fixed amount to the context). For a 20-step agent with substantial tool outputs, this can make individual API calls surprisingly expensive.

Implications for agent design: tool results should return the minimum information needed for the next step, not the complete raw response. If a drug interaction checker returns 2,000 tokens of detail when the agent only needs severity grades and drug pairs, that overhead compounds across every subsequent step in the conversation.

## FHIR Integration Path for Clinical Agents

The sample trace shows a clinical agent that calls NLP extraction and drug interaction checking as if they were production tools. In a real clinical deployment, these tools would be exposed as FHIR-compliant endpoints rather than direct API calls:

The `nlp_extractor` tool would accept a FHIR `DocumentReference` resource containing the clinical note and return FHIR `Condition`, `MedicationStatement`, `Observation`, and `AllergyIntolerance` resources extracted from the text.

The `drug_interaction_checker` tool would accept an array of FHIR `MedicationRequest` resources (not free-text drug names) and return FHIR `DetectedIssue` resources with coded severity, implicated drug references, and structured management recommendations.

The agent's final summary would be formatted as a FHIR `ClinicalImpression` resource, with the detected issues referenced by ID and the plan structured as a `CarePlan`.

The visualiser would then render not just raw JSON blocks but a structured FHIR resource timeline, showing which resources were created at each step and how they reference each other — a significantly more useful view for clinical informatics teams auditing agent-assisted decision making.

---

*Try the [LLM Agent Trace Visualiser](/agent-trace). Load the sample trace and step through the extended thinking blocks to see the clinical reasoning that precedes each tool call.*
