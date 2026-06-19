---
title: "Taking Claude Fully Agentic"
date: "January 25, 2026"
category: "AI Engineering"
tags: "AI, agentic, Claude Code, LLM engineering"
level: "Intermediate"
read_time: "12 minutes"
featured: false
summary: "Superclaude = claude --dangerously-skip-permissions. The transition from manual coder to system architect is the biggest productivity jump in my 40+ years of electronics development."
---

## The 10 Levels of AI-Driven Development

```bash
superclaude = claude --dangerously-skip-permissions
```

Type that into a terminal and Claude will go fully agentic and fully autonomous. **Spoiler Alert:** REALLY know at a deep level what you're doing and don't come crying to me if you don't!

The transition from being a manual coder to a system architect represents the most significant productivity jump in my forty+ years of electronics development. After much thought, I believe there are ten distinct levels of AI integration in development practice. Developers can move beyond writing lines of code to focus on high-level design and supervision.

---

## Level 0: Vibe Coding

This entry-level approach involves asking an AI chat for a code snippet or a complete sketch, then copying and pasting it into your IDE while "hoping for the best". It's a common first step, but inefficient — your copy-and-paste fingers will eventually need a holiday.

## Level 1: Spec-driven Development

You define your requirements in plain language and let the AI generate the code. The key difference: you never touch the code directly. If something fails, you update the specification rather than the code and let the AI regenerate.

## Level 2: Functional Specification Documents (FSD)

Move your specifications into structured Markdown files. Markdown is the perfect format — readable by humans and easily parsed by AI models, serving as a single source of truth for the project.

## Level 3: Agents

Moving beyond simple chat interfaces, agents like Claude Code, Gemini CLI, or Codex can see your entire project folder. Unlike standard chats that require complete documents, these agents can edit individual lines across long program files without overloading the context window.

## Level 4: GitHub Integration

Once you use agents that can edit your files, version control becomes essential. It protects you from accidental corruption if the AI makes a mistake and provides a history that becomes vital as projects grow in complexity.

## Level 5: Full Execution Control

Move past "sandboxed" agents that can only read files. Allow agents to run terminal commands, install dependencies, and execute scripts. This eliminates the scenario where you have to manually execute the AI's instructions like an employee of your agent.

## Level 6: Development VMs

Isolate the agent within a Virtual Machine. By granting "YOLO" mode, it can execute entire workflows — installing software, configuring environments — without asking for permission at every step.

## Level 7: Parallel Projects

A VM and a terminal allows managing multiple projects simultaneously. Agents store and resume their internal knowledge files (`claude.md`, `agents.md`) within the project directory, restoring context when you return.

## Level 8: CLI Integration

Using the Arduino CLI or PlatformIO CLI, the agent can compile, upload, and read serial logs in real-time. The AI sees its own compilation errors and automatically adjusts the code until the project behaves as intended.

## Level 9: Automated Data Sheet Analysis

Instead of manually reading 100-page PDF data sheets, drop the raw PDF into the project directory. The AI analyses it and generates a working library for a new chip in minutes.

## Level 10: Beyond Arduino

The final level involves moving to professional frameworks like ESP-IDF. Because the AI handles the steep learning curve and framework complexities, the simplicity of the Arduino IDE is no longer a requirement.

---

## Why Claude?

To me, [Claude from Anthropic](https://www.anthropic.com) is currently the most effective LLM and agent for electronics development. Claude makes significantly fewer errors when editing project files — I've had other models completely corrupt a main project file during editing. Beyond code generation, Claude Code is the most capable agent for full execution control.

Claude is also able to handle highly technical troubleshooting and data analysis that previously required human expertise. For instance, I've had Claude successfully debug a third-party library by adding serial print statements and analysing logs — a level of automation akin to "completed staff work."

To streamline my workflow further, I use a custom shell command `superclaude` to launch Claude with `--dangerously-skip-permissions`, allowing the agent to solve problems autonomously while I focus on high-level supervision.

That is, in essence, what system architecture at Level 10 looks like.
