---
title: "From High School Grad to AI Expert: How I Train State-of-the-Art Deep Learning Practitioners"
date: "November 8, 2025"
category: "AI Engineering"
tags: "AI, education, deep learning, teaching"
level: "Easy"
read_time: "4 minutes"
featured: false
summary: "For many years I have trained more than 600 AI practitioners — from medical doctors to high school graduates — transforming coders into effective AI engineers. Here is the approach that works."
---

For many years, I have had the privilege of training aspiring Machine Learning and Deep Learning students, helping them transition from coders to effective AI practitioners. To date, I have trained more than **600 AI practitioners**, with student backgrounds ranging impressively from medical doctors to high school graduates.

This range is not accidental. It reflects a core belief: the mental models required for machine learning are learnable by anyone with sufficient curiosity and rigour. Prior programming experience helps but is not the gate it is often assumed to be.

## The Problem With Most AI Courses

Most AI courses fall into one of two failure modes:

**Too shallow.** They teach APIs and libraries without explaining what is happening underneath. Students can call `model.fit()` but cannot debug a training run that diverges or explain why their model fails on out-of-distribution data. This produces prompt engineers who cannot engineer anything harder than a prompt.

**Too academic.** They start with the mathematics and work forward. By the time students reach something they can run, they've lost the intuition for why any of it matters. Graduate students emerge knowing the Jacobian of a softmax but not how to read a loss curve.

The approach I've developed over years of iteration sits between these. It is:

1. **Hands-on first.** Every concept is demonstrated with running code before the mathematics is introduced. Students must see the thing behave before they learn why it behaves that way.

2. **Incrementally mathematical.** Once the intuition is established, we go deep. I use Jeremy Howard's [fast.ai](https://www.fast.ai/) approach as a base and extend it significantly, particularly into the low-level machinery that most courses skip.

3. **Project-anchored.** Each student works on a project in their own domain from week two. A cardiologist builds a classifier for ECG anomalies. A trader builds a prediction pipeline for FX data. A software developer builds a code embedding search engine. The domain expertise they already have becomes an asset rather than irrelevant background.

4. **Rigorously debugged.** I spend significant time teaching students *how to fail intelligently* — how to read error messages, interpret training curves, diagnose data leakage, and reason about what a model has and has not learned.

## What the Best Students Do Differently

After 600+ students, the pattern is clear. The students who progress fastest are not the ones with the most prior coding experience. They are the ones who:

- Ask "why" before "how"
- Read source code rather than just documentation
- Break things deliberately to understand how they work
- Build from scratch at least once before using a library abstraction

The single most common failure mode among students who struggle: they treat ML libraries as black boxes and then cannot reason about model behaviour when something goes wrong.

## Where to Start If You're Not Yet a Student

[Fast.ai's Practical Deep Learning for Coders](https://course.fast.ai/) remains the best starting point for most people. Read [Andrej Karpathy's neural network zero-to-hero series](https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ) immediately after. Then come talk to me about the next level.
