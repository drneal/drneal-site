---
title: "Learning With Dr Neal"
date: 2026-06-19
category: Deep Learning
tags: deep learning, neural networks, fast.ai, gradient descent, PyTorch, ReLU, Jeremy Howard, learning science, AI education
level: Intermediate
read_time: 35 min
summary: >
  A comprehensive guide to fast.ai Lesson 3 — from the 1943 origins of neural networks through gradient descent, ReLU, and matrix multiplication — paired with Jeremy Howard's philosophy of learning, proven learning science, and a practical two-week study plan. Includes a downloadable learning guide (PDF and EPUB).
featured: true
---

<style>
.notebooklm-banner {
  font-size: 0.8em;
  background: linear-gradient(135deg, #1a237e 0%, #283593 100%);
  color: white;
  padding: 1.2em 1.6em;
  border-radius: 8px;
  margin: 1.5em 0;
  line-height: 1.6;
}
.notebooklm-banner a { color: #90caf9; font-weight: bold; }
.audio-section {
  font-size: 0.8em;
  background: #1a1f2e;
  border-left: 4px solid #1a237e;
  padding: 1em 1.4em;
  border-radius: 0 6px 6px 0;
  margin: 1.5em 0;
}
.testimonials { margin: 2em 0; }
.testimonial {
  font-size: 0.8em;
  background: #151922;
  border-left: 4px solid #1565c0;
  padding: 1em 1.4em;
  margin: 1.2em 0;
  border-radius: 0 6px 6px 0;
  font-style: italic;
}
.testimonial .attribution {
  font-style: normal;
  font-weight: bold;
  color: #1565c0;
  margin-top: 0.6em;
  font-size: 0.9em;
}
.guide-downloads {
  font-size: 0.8em;
  background: #0d2018;
  border: 2px solid #1b5e20;
  border-radius: 8px;
  padding: 1.2em 1.6em;
  margin: 1.5em 0;
}
.guide-downloads a {
  display: inline-block;
  background: #1b5e20;
  color: white;
  padding: 0.4em 1em;
  border-radius: 4px;
  text-decoration: none;
  margin: 0.3em 0.4em 0.3em 0;
  font-weight: bold;
}
.callout {
  font-size: 0.8em;
  background: #1e1a0e;
  border-left: 4px solid #f9a825;
  padding: 0.8em 1.2em;
  margin: 1.2em 0;
  border-radius: 0 4px 4px 0;
}
.swadia-point {
  font-size: 0.8em;
  background: #180d1e;
  border-left: 3px solid #ab47bc;
  padding: 0.6em 1em;
  margin: 0.6em 0;
  border-radius: 0 4px 4px 0;
}
</style>

<div class="notebooklm-banner">
📚 <strong>NotebookLM companion resource for this post:</strong><br/>
All slide material, mind map, and audio overviews for this lesson are available in the linked notebook.<br/>
<a href="https://notebooklm.google.com/notebook/8e7184c3-a0c5-47a5-8992-85e90f8b5261" target="_blank">→ Open NotebookLM Notebook (Google account required)</a>
</div>

*This article is based on Jeremy Howard's fast.ai Practical Deep Learning for Coders 2022 · Lesson 3: Neural Net Foundations. This is an example of the course materials produced by Dr Neal and used to teach students through his one-to-one AI Learners Course.*

[▶ Watch Lesson 3 on YouTube](https://www.youtube.com/watch?v=hBBOjCiFcuo&list=PLfYUBJiXbdtSvpQjSnJJ_PmDQB_VyT5iU&index=3) · [▶ Supplementary Swadia Tutorial](https://youtu.be/npQ2IORdlvU)

---

## We've Been Building This Since 1943

<div>
<svg viewBox="0 0 800 220" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:640px;display:block;margin:1.5em auto;background:#1a1f2e;border-radius:10px;padding:10px">
  <defs>
    <marker id="ah" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#7986cb"/>
    </marker>
  </defs>
  <!-- Timeline spine -->
  <line x1="40" y1="110" x2="760" y2="110" stroke="#7986cb" stroke-width="3" marker-end="url(#ah)"/>
  <!-- Nodes -->
  <!-- 1943 -->
  <circle cx="80" cy="110" r="22" fill="#7986cb"/>
  <text x="80" y="115" text-anchor="middle" fill="white" font-size="11" font-weight="bold">1943</text>
  <text x="80" y="80" text-anchor="middle" fill="#7986cb" font-size="10" font-weight="bold">McCulloch</text>
  <text x="80" y="92" text-anchor="middle" fill="#7986cb" font-size="10">& Pitts</text>
  <text x="80" y="145" text-anchor="middle" fill="#b0bec5" font-size="9">First math</text>
  <text x="80" y="157" text-anchor="middle" fill="#b0bec5" font-size="9">neuron model</text>
  <!-- 1958 -->
  <circle cx="200" cy="110" r="22" fill="#283593"/>
  <text x="200" y="115" text-anchor="middle" fill="white" font-size="11" font-weight="bold">1958</text>
  <text x="200" y="80" text-anchor="middle" fill="#7986cb" font-size="10" font-weight="bold">Rosenblatt</text>
  <text x="200" y="92" text-anchor="middle" fill="#7986cb" font-size="10">Perceptron</text>
  <text x="200" y="145" text-anchor="middle" fill="#b0bec5" font-size="9">First learning</text>
  <text x="200" y="157" text-anchor="middle" fill="#b0bec5" font-size="9">algorithm</text>
  <!-- 1986 -->
  <circle cx="350" cy="110" r="22" fill="#303f9f"/>
  <text x="350" y="115" text-anchor="middle" fill="white" font-size="11" font-weight="bold">1986</text>
  <text x="350" y="80" text-anchor="middle" fill="#7986cb" font-size="10" font-weight="bold">Rumelhart</text>
  <text x="350" y="92" text-anchor="middle" fill="#7986cb" font-size="10">Backprop</text>
  <text x="350" y="145" text-anchor="middle" fill="#b0bec5" font-size="9">Gradient descent</text>
  <text x="350" y="157" text-anchor="middle" fill="#b0bec5" font-size="9">via chain rule</text>
  <!-- 2012 -->
  <circle cx="500" cy="110" r="22" fill="#3949ab"/>
  <text x="500" y="115" text-anchor="middle" fill="white" font-size="11" font-weight="bold">2012</text>
  <text x="500" y="80" text-anchor="middle" fill="#7986cb" font-size="10" font-weight="bold">AlexNet</text>
  <text x="500" y="92" text-anchor="middle" fill="#7986cb" font-size="10">GPU era</text>
  <text x="500" y="145" text-anchor="middle" fill="#b0bec5" font-size="9">Deep learning</text>
  <text x="500" y="157" text-anchor="middle" fill="#b0bec5" font-size="9">becomes practical</text>
  <!-- 2017 -->
  <circle cx="630" cy="110" r="22" fill="#5c6bc0"/>
  <text x="630" y="115" text-anchor="middle" fill="white" font-size="11" font-weight="bold">2017</text>
  <text x="630" y="80" text-anchor="middle" fill="#7986cb" font-size="10" font-weight="bold">Transformer</text>
  <text x="630" y="92" text-anchor="middle" fill="#7986cb" font-size="10">Attention</text>
  <text x="630" y="145" text-anchor="middle" fill="#b0bec5" font-size="9">Language models</text>
  <text x="630" y="157" text-anchor="middle" fill="#b0bec5" font-size="9">at scale</text>
  <!-- 2022 -->
  <circle cx="740" cy="110" r="22" fill="#7986cb"/>
  <text x="740" y="115" text-anchor="middle" fill="white" font-size="11" font-weight="bold">Now</text>
  <text x="740" y="80" text-anchor="middle" fill="#7986cb" font-size="10" font-weight="bold">fast.ai</text>
  <text x="740" y="92" text-anchor="middle" fill="#7986cb" font-size="10">LLMs</text>
  <text x="740" y="145" text-anchor="middle" fill="#b0bec5" font-size="9">Same core idea,</text>
  <text x="740" y="157" text-anchor="middle" fill="#b0bec5" font-size="9">vast scale</text>
  <!-- Connecting lines -->
  <line x1="102" y1="110" x2="178" y2="110" stroke="#7986cb" stroke-width="2" stroke-dasharray="4"/>
  <line x1="222" y1="110" x2="328" y2="110" stroke="#7986cb" stroke-width="2" stroke-dasharray="4"/>
  <line x1="372" y1="110" x2="478" y2="110" stroke="#7986cb" stroke-width="2" stroke-dasharray="4"/>
  <line x1="522" y1="110" x2="608" y2="110" stroke="#7986cb" stroke-width="2" stroke-dasharray="4"/>
  <line x1="652" y1="110" x2="718" y2="110" stroke="#7986cb" stroke-width="2" stroke-dasharray="4"/>
  <!-- Title -->
  <text x="400" y="28" text-anchor="middle" fill="#7986cb" font-size="15" font-weight="bold">We've Been Building This Since 1943</text>
  <text x="400" y="44" text-anchor="middle" fill="#90a4ae" font-size="10">The unbroken chain from McCulloch-Pitts to modern deep learning</text>
</svg>
</div>

In 1943, Warren McCulloch and Walter Pitts published "A Logical Calculus of the Ideas Immanent in Nervous Activity" — a mathematical model of how neurons fire. Their artificial neuron took weighted binary inputs, summed them, and fired if the total exceeded a threshold. It could not learn. It had no notion of optimisation. But it was the first time anyone had formalised the idea of computation in biological terms, and it planted a seed that eighty years of mathematics, hardware, and data have now grown into something extraordinary.

Jeremy Howard's fast.ai Lesson 3 is, in one sense, the story of what happened between 1943 and now — told from the bottom up, using nothing more than arithmetic and a few lines of Python. This post is a full reconstruction of that lesson and what it reveals about how we learn, how machines learn, and why the two might not be as different as we habitually assume.

---

<!-- Mind map from NotebookLM -->

<div>
<svg viewBox="0 0 760 500" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:608px;display:block;margin:1.8em auto;background:#1a1f2e;border-radius:10px;border:1px solid #2a3050">
  <!-- Central node -->
  <ellipse cx="380" cy="250" rx="80" ry="36" fill="#7986cb"/>
  <text x="380" y="246" text-anchor="middle" fill="white" font-size="12" font-weight="bold">fast.ai</text>
  <text x="380" y="262" text-anchor="middle" fill="#90caf9" font-size="11">Lesson 3</text>
  <!-- Branch: Gradient Descent (top left) -->
  <line x1="305" y1="230" x2="190" y2="140" stroke="#283593" stroke-width="2"/>
  <ellipse cx="145" cy="128" rx="62" ry="26" fill="#283593"/>
  <text x="145" y="124" text-anchor="middle" fill="white" font-size="10" font-weight="bold">Gradient</text>
  <text x="145" y="138" text-anchor="middle" fill="white" font-size="10">Descent</text>
  <!-- GD children -->
  <line x1="90" y1="115" x2="52" y2="88"/>
  <ellipse cx="38" cy="80" rx="36" ry="16" fill="#3949ab"/>
  <text x="38" y="84" text-anchor="middle" fill="white" font-size="9">Loss (MSE)</text>
  <line x1="100" y1="102" x2="68" y2="62"/>
  <ellipse cx="56" cy="52" rx="36" ry="16" fill="#3949ab"/>
  <text x="56" y="56" text-anchor="middle" fill="white" font-size="9">Gradients</text>
  <line x1="145" y1="102" x2="145" y2="68"/>
  <ellipse cx="145" cy="56" rx="40" ry="16" fill="#3949ab"/>
  <text x="145" y="60" text-anchor="middle" fill="white" font-size="9">Learning Rate</text>
  <!-- Branch: ReLU (top right) -->
  <line x1="455" y1="230" x2="565" y2="140" stroke="#7b1fa2" stroke-width="2"/>
  <ellipse cx="610" cy="128" rx="62" ry="26" fill="#7b1fa2"/>
  <text x="610" y="124" text-anchor="middle" fill="white" font-size="10" font-weight="bold">ReLU &amp;</text>
  <text x="610" y="138" text-anchor="middle" fill="white" font-size="10">Universal Approx.</text>
  <!-- ReLU children -->
  <line x1="660" y1="112" x2="700" y2="80"/>
  <ellipse cx="714" cy="72" rx="40" ry="16" fill="#9c27b0"/>
  <text x="714" y="76" text-anchor="middle" fill="white" font-size="9">Nonlinearity</text>
  <line x1="655" y1="102" x2="695" y2="52"/>
  <ellipse cx="706" cy="42" rx="40" ry="16" fill="#9c27b0"/>
  <text x="706" y="46" text-anchor="middle" fill="white" font-size="9">Stacking</text>
  <!-- Branch: Matrix Mult (bottom right) -->
  <line x1="455" y1="268" x2="568" y2="360" stroke="#1b5e20" stroke-width="2"/>
  <ellipse cx="614" cy="372" rx="62" ry="26" fill="#1b5e20"/>
  <text x="614" y="368" text-anchor="middle" fill="white" font-size="10" font-weight="bold">Matrix</text>
  <text x="614" y="382" text-anchor="middle" fill="white" font-size="10">Multiplication</text>
  <!-- MatMul children -->
  <line x1="660" y1="388" x2="700" y2="420"/>
  <ellipse cx="716" cy="430" rx="40" ry="18" fill="#2e7d32"/>
  <text x="716" y="434" text-anchor="middle" fill="white" font-size="9">GPU Compute</text>
  <line x1="664" y1="362" x2="714" y2="362"/>
  <ellipse cx="732" cy="362" rx="38" ry="16" fill="#2e7d32"/>
  <text x="732" y="366" text-anchor="middle" fill="white" font-size="9">Layers</text>
  <!-- Branch: Titanic (bottom left) -->
  <line x1="305" y1="270" x2="192" y2="360" stroke="#e65100" stroke-width="2"/>
  <ellipse cx="148" cy="372" rx="62" ry="26" fill="#e65100"/>
  <text x="148" y="368" text-anchor="middle" fill="white" font-size="10" font-weight="bold">Titanic</text>
  <text x="148" y="382" text-anchor="middle" fill="white" font-size="10">Spreadsheet</text>
  <!-- Titanic children -->
  <line x1="90" y1="388" x2="50" y2="420"/>
  <ellipse cx="38" cy="430" rx="40" ry="18" fill="#bf360c"/>
  <text x="38" y="434" text-anchor="middle" fill="white" font-size="9">Preprocessing</text>
  <line x1="92" y1="362" x2="44" y2="362"/>
  <ellipse cx="26" cy="362" rx="32" ry="16" fill="#bf360c"/>
  <text x="26" y="366" text-anchor="middle" fill="white" font-size="9">Feature Eng.</text>
  <!-- Branch: Jeremy Howard (top centre) -->
  <line x1="380" y1="214" x2="380" y2="120"/>
  <ellipse cx="380" cy="102" rx="72" ry="26" fill="#004d40"/>
  <text x="380" y="98" text-anchor="middle" fill="white" font-size="10" font-weight="bold">Jeremy Howard</text>
  <text x="380" y="112" text-anchor="middle" fill="white" font-size="10">Top-down Teaching</text>
  <!-- Caption -->
  <text x="380" y="488" text-anchor="middle" fill="#90a4ae" font-size="10" font-style="italic">Mind map of fast.ai Lesson 3 concepts · Full interactive version available in NotebookLM</text>
</svg>
</div>

*↑ Key conceptual structure of fast.ai Lesson 3. The full interactive mind map is available in the [NotebookLM notebook](https://notebooklm.google.com/notebook/8e7184c3-a0c5-47a5-8992-85e90f8b5261).*

---

<div class="audio-section">
<strong>🎧 Audio Overviews — Listen Directly</strong><br/>
AI-narrated audio overviews of the fast.ai Lesson 3 materials, generated from the full slide decks and course notes. Ideal for commute listening before or after a session.

<p style="margin:0.8em 0 0.2em;"><strong>Course Overview</strong></p>
<audio controls style="width:100%; margin-bottom:0.8em;">
  <source src="/static/audio/Course_Overview_audio.m4a" type="audio/mp4">
  <a href="/static/audio/Course_Overview_audio.m4a">Download Course Overview audio</a>
</audio>

<p style="margin:0 0 0.2em;"><strong>Lesson 1 Deep Dive</strong></p>
<audio controls style="width:100%; margin-bottom:0.4em;">
  <source src="/static/audio/Lesson_1_audio_overview.m4a" type="audio/mp4">
  <a href="/static/audio/Lesson_1_audio_overview.m4a">Download Lesson 1 audio</a>
</audio>
</div>

<div class="guide-downloads">
<strong>📥 Download the Learning Guide</strong><br/>
A structured two-week study guide synthesising the Swadia tutorial, Howard's lesson, and learning science research:<br/>
<a href="/static/fastai-lesson3-learning-guide.pdf">PDF Version</a>
<a href="/static/fastai-lesson3-learning-guide.epub">EPUB Version</a>
</div>

---

## The Central Question

Howard opens the computational core of Lesson 3 with a question that is more consequential than it first appears: *what are the weights in a trained model, and how can numbers figure out something important about the world?* This is the right question to anchor around, because it forces you to unpack three distinct concerns the deep learning literature often muddles:

1. **The function family.** What class of mathematical function is expressive enough to represent the mapping you care about?
2. **The loss.** How do you quantify the gap between predictions and ground truth in a differentiable way?
3. **The optimisation algorithm.** Given the loss and its gradient, how do you search the parameter space efficiently?

Howard's pedagogical move is to answer all three questions concretely, building each from scratch before introducing the abstractions that fast.ai and PyTorch provide. This is the top-down, whole-game approach that defines his teaching philosophy — and we'll return to why it works so well when we examine the learning science behind it later in this post.

---

## Step 1 — Fitting a Function by Hand

Howard begins with a general quadratic:

```
f(x) = a·x² + b·x + c
```

<div>
<svg viewBox="0 0 520 240" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:416px;display:block;margin:1.2em auto;background:#1a1f2e;border-radius:8px;border:1px solid #2a3050">
  <text x="260" y="22" text-anchor="middle" fill="#7986cb" font-size="13" font-weight="bold">Parameterised Function Family</text>
  <text x="260" y="38" text-anchor="middle" fill="#90a4ae" font-size="10">Same template, different parameters → different curves</text>
  <!-- Axes -->
  <line x1="60" y1="200" x2="460" y2="200" stroke="#90a4ae" stroke-width="1.5"/>
  <line x1="60" y1="40" x2="60" y2="200" stroke="#90a4ae" stroke-width="1.5"/>
  <text x="462" y="204" fill="#90a4ae" font-size="10">x</text>
  <text x="50" y="38" fill="#90a4ae" font-size="10">f(x)</text>
  <!-- Curve 1: wide parabola -->
  <polyline points="80,190 120,170 160,155 200,148 240,148 280,155 320,170 360,190 400,210" fill="none" stroke="#7986cb" stroke-width="2" stroke-dasharray="0"/>
  <!-- Curve 2: narrow parabola -->
  <polyline points="120,195 160,158 200,128 240,110 280,128 320,158 360,195" fill="none" stroke="#7b1fa2" stroke-width="2"/>
  <!-- Curve 3: shifted parabola -->
  <polyline points="80,140 120,118 160,108 200,110 240,125 280,148 320,178 360,198" fill="none" stroke="#1b5e20" stroke-width="2"/>
  <!-- Labels -->
  <text x="410" y="215" fill="#7986cb" font-size="10">a=0.3</text>
  <text x="370" y="188" fill="#7b1fa2" font-size="10">a=0.8</text>
  <text x="368" y="170" fill="#1b5e20" font-size="10">shifted</text>
  <!-- Parameter box -->
  <rect x="320" y="48" width="130" height="70" rx="6" fill="#e8eaf6" stroke="#3949ab" stroke-width="1"/>
  <text x="385" y="68" text-anchor="middle" fill="#7986cb" font-size="10" font-weight="bold">Free Parameters</text>
  <text x="385" y="84" text-anchor="middle" fill="#b0bec5" font-size="10">a → curvature</text>
  <text x="385" y="98" text-anchor="middle" fill="#b0bec5" font-size="10">b → slope</text>
  <text x="385" y="112" text-anchor="middle" fill="#b0bec5" font-size="10">c → intercept</text>
</svg>
</div>

The point is not the specific function — it is the parameterisation. By exposing three free parameters (`a`, `b`, `c`), a single function template can realise any specific quadratic by fixing those parameters. Howard demonstrates this with an interactive Jupyter widget, dragging sliders to visually minimise the distance between the curve and a randomly generated dataset.

This surfaces the core insight immediately: **fitting a model is a search problem in parameter space.** The slider widget works for three parameters on a toy dataset, but is obviously unscalable to ten million parameters. This deliberate setup carries the rest of the lesson.

---

## Step 2 — Introducing Loss (MSE)

Rather than relying on visual intuition, Howard introduces a scalar summary of "how wrong the current parameters are." For a regression problem:

```
L = (1/n) · Σ (ŷᵢ − yᵢ)²
```

MSE has two properties that matter: it is everywhere differentiable, and squaring penalises large residuals super-linearly, making the optimiser concentrate on the worst-fitting examples. Howard presents the loss as a design choice, not a revealed truth — later lessons swap in cross-entropy for classification tasks.

<div class="callout">
<strong>Core insight:</strong> The loss collapses the entire dataset's prediction quality into a single number. Optimisation then becomes: decrease this number by adjusting the parameters. Everything else in training is mechanics around that one idea.
</div>

---

## Step 3 — Gradients and the Chain Rule

Howard's treatment of derivatives is deliberately minimal. For a given set of parameter values, PyTorch can tell you the slope of the loss with respect to each parameter — i.e., if you nudge parameter `a` upward by one unit, does the loss go up or down, and by approximately how much?

```python
params = torch.tensor([a, b, c], requires_grad=True)

preds = params[0]*x**2 + params[1]*x + params[2]
loss  = ((preds - y)**2).mean()

loss.backward()
print(params.grad)  # tensor([da, db, dc])
```

`params.grad[0]` answers: "by how much does the loss increase per unit increase in `a`?" A positive gradient means increasing `a` makes things worse; a negative gradient means increasing `a` helps. This is the entire information content you need for gradient descent.

---

## Step 4 — Gradient Descent

With gradients in hand, the update rule is straightforward:

```
θ ← θ − lr · ∇L(θ)
```

Subtract a small multiple of the gradient from each parameter. Howard implements the manual loop to make it concrete:

```python
lr = 1e-3

for _ in range(100):
    loss = mse(quadratic(params, x), y)
    loss.backward()
    with torch.no_grad():
        params -= lr * params.grad
        params.grad.zero_()   # must clear or gradients accumulate
```

<div class="callout">
⚠️ <strong>The most commonly forgotten line:</strong> <code>params.grad.zero_()</code>. PyTorch accumulates gradients by default — a feature for gradient checkpointing, a footgun for a simple training loop. Howard flags this explicitly, and experienced practitioners still trip on it when switching contexts.
</div>

<div>
<svg viewBox="0 0 540 240" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:432px;display:block;margin:1.2em auto;background:#1a1f2e;border-radius:8px;border:1px solid #2a3050">
  <text x="270" y="22" text-anchor="middle" fill="#7986cb" font-size="13" font-weight="bold">Gradient Descent in Loss Space</text>
  <!-- Bowl shape -->
  <path d="M80,60 Q270,240 460,60" fill="none" stroke="#90a4ae" stroke-width="2"/>
  <text x="460" y="55" fill="#90a4ae" font-size="10">Loss landscape</text>
  <!-- Steps -->
  <circle cx="150" cy="138" r="6" fill="#e53935"/>
  <circle cx="185" cy="168" r="6" fill="#e53935"/>
  <circle cx="220" cy="190" r="6" fill="#e53935"/>
  <circle cx="258" cy="205" r="6" fill="#e53935"/>
  <circle cx="295" cy="208" r="6" fill="#2e7d32"/>
  <!-- Arrows -->
  <line x1="150" y1="138" x2="179" y2="163" stroke="#7986cb" stroke-width="1.5" marker-end="url(#ah2)"/>
  <line x1="185" y1="168" x2="214" y2="185" stroke="#7986cb" stroke-width="1.5"/>
  <line x1="220" y1="190" x2="252" y2="202" stroke="#7986cb" stroke-width="1.5"/>
  <line x1="258" y1="205" x2="289" y2="207" stroke="#7986cb" stroke-width="1.5"/>
  <!-- Labels -->
  <text x="140" y="125" fill="#e53935" font-size="10" font-weight="bold">Start</text>
  <text x="285" y="222" fill="#2e7d32" font-size="10" font-weight="bold">Minimum</text>
  <!-- LR too large - oscillation -->
  <circle cx="390" cy="80" r="5" fill="#f57c00"/>
  <circle cx="350" cy="82" r="5" fill="#f57c00"/>
  <circle cx="410" cy="78" r="5" fill="#f57c00"/>
  <line x1="390" y1="80" x2="355" y2="82" stroke="#f57c00" stroke-width="1.5" stroke-dasharray="3"/>
  <line x1="350" y1="82" x2="408" y2="79" stroke="#f57c00" stroke-width="1.5" stroke-dasharray="3"/>
  <text x="380" y="68" text-anchor="middle" fill="#f57c00" font-size="10">lr too large → overshoot</text>
  <defs>
    <marker id="ah2" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 z" fill="#7986cb"/>
    </marker>
  </defs>
</svg>
</div>

### Learning Rate: Why Size Matters

Howard visualises the loss landscape as a bowl (a quadratic approximation is locally valid near any smooth minimum). A large learning rate causes the optimiser to overshoot the bottom of the bowl, potentially diverging. A learning rate that's too small means thousands of iterations to converge. Howard's practical heuristic at this stage: start around `1e-3`, watch the loss curve, and halve it if it oscillates.

**Gradient interpretation in units:** Howard makes a point experienced engineers often skip — the gradient is in units of (loss units / parameter units). If your "Fare" column is in dollars and the loss is in squared probability-of-survival, the raw gradient magnitude is not comparable across columns. This motivates normalisation.

---

## Step 5 — Why Quadratics Are Not Enough

Having established the full gradient descent loop, Howard pivots to the expressiveness problem. A quadratic can model one hump. Real-world mappings — image pixels to class labels, text tokens to sentiment scores — require functions of effectively arbitrary complexity. Higher-degree polynomials are numerically unstable. What's needed is a simple building block that can be composed into arbitrarily complex functions.

---

## Step 6 — The Rectified Linear Unit (ReLU)

Howard's answer is the ReLU:

```
ReLU(x) = max(0, x)
```

<div>
<svg viewBox="0 0 460 200" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:368px;display:block;margin:1.2em auto;background:#1a1f2e;border-radius:8px;border:1px solid #2a3050">
  <text x="230" y="20" text-anchor="middle" fill="#7986cb" font-size="13" font-weight="bold">ReLU: max(0, x)</text>
  <text x="230" y="36" text-anchor="middle" fill="#90a4ae" font-size="10">Simple piecewise-linear · universal approximator when stacked</text>
  <!-- Axes -->
  <line x1="60" y1="160" x2="400" y2="160" stroke="#90a4ae" stroke-width="1.5"/>
  <line x1="230" y1="55" x2="230" y2="165" stroke="#90a4ae" stroke-width="1.5"/>
  <text x="402" y="164" fill="#90a4ae" font-size="10">x</text>
  <text x="218" y="52" fill="#90a4ae" font-size="10">f(x)</text>
  <!-- ReLU curve -->
  <polyline points="60,160 230,160 400,80" fill="none" stroke="#7986cb" stroke-width="3"/>
  <!-- Shaded area -->
  <polygon points="230,160 400,80 400,160" fill="#e8eaf6" opacity="0.5"/>
  <!-- Labels -->
  <text x="140" y="148" fill="#7b1fa2" font-size="10">f(x) = 0 for x &lt; 0</text>
  <text x="295" y="110" fill="#1b5e20" font-size="10">f(x) = x for x ≥ 0</text>
  <!-- Stacked ReLUs annotation -->
  <text x="60" y="185" fill="#90a4ae" font-size="9">Two ReLUs stacked → a tent function. Millions stacked → any continuous function (universal approx. theorem)</text>
</svg>
</div>

This function is about as simple as a nonlinear function can be. Two parameters control a shifted, scaled version: `f(x) = max(0, w·x + b)`. A single ReLU is nearly useless. But the **universal approximation theorem** guarantees that a sum of enough ReLUs can approximate any continuous function on a compact domain to arbitrary precision. Howard demonstrates this interactively by stacking two ReLUs and showing how four parameters produce a more complex shape than any single parabola could.

<div class="callout">
<strong>Howard's compressed summary of deep learning:</strong> (1) parameterised family of functions (ReLU stacks); (2) define a loss; (3) compute gradients; (4) take a small step downhill; (5) repeat. Everything else — batch normalisation, residual connections, attention — is engineering that makes this core loop work better in practice.
</div>

---

## Step 7 — Matrix Multiplication as the Computational Substrate

When your network has millions of ReLUs, computing predictions one at a time is prohibitively slow. Howard introduces the key insight: a layer of neurons computing `w₁x₁ + w₂x₂ + ... + wₙxₙ + b` for each of `m` neurons simultaneously is exactly a matrix multiplication.

If `X` is the input matrix (batch × features) and `W` is the weight matrix (features × neurons):

```
Z = X · W + b
```

This is a single BLAS call. GPUs are designed to execute billions of these floating-point multiply-accumulate operations in parallel — which is the entire reason deep learning became practical on commodity hardware.

```python
W = torch.randn(n_inputs, n_hidden, requires_grad=True)
b = torch.zeros(n_hidden,           requires_grad=True)

def linear(x): return x @ W + b
def relu(x):   return x.clamp(min=0)

# One hidden layer
def model(x): return linear(relu(linear(x)))
```

---

## Step 8 — Building a Neural Network in a Spreadsheet (Titanic)

To cement these concepts Howard walks through a spreadsheet implementation of gradient descent on the Kaggle Titanic dataset. Every operation is visible without library abstractions hiding it.

The key preprocessing decisions are worth cataloguing:

**1. Dummy-encode categoricals.** Sex, Pclass, and Embarked become binary columns. You only need k−1 dummy variables for a k-category feature (the dropped category becomes the reference level). Getting this wrong is a common source of rank-deficient design matrices.

**2. Normalise continuous features.** Age and Fare are on very different scales. The same learning rate can simultaneously be too large for one feature and too small for another. Fix: subtract the mean, divide by standard deviation.

**3. Apply log to Fare.** Fare is right-skewed — a few first-class tickets cost vastly more than the median. A log transform compresses the tail, ensuring gradient signals from extreme values are proportional to information content rather than raw magnitude.

**4. Build two linear layers with ReLU.** First linear → ReLU → second linear → scalar prediction. That's a minimal two-layer neural network.

<div class="callout">
<strong>The critical conceptual point:</strong> a neural network with one hidden layer is just two regression models stacked, with the output of the first passed through a nonlinearity before being fed to the second. It is additive function composition over a parameterised function family. There is no mysticism here.
</div>

---

## Step 9 — What's Actually Stored in a Trained Model

Howard returns to the original question: what are the weights? After gradient descent converges, the parameter tensors `W₁`, `b₁`, `W₂`, `b₂` contain numbers that, when matrix-multiplied against an input, produce a useful output. There is no explicit rule stored. The model's "knowledge" is entirely encoded in the geometry of those high-dimensional parameter matrices.

```python
learn = vision_learner(dls, resnet34, metrics=error_rate)

# Access the underlying PyTorch module
learn.model

# Inspect the first convolution layer's weights
# Shape: (out_channels, in_channels, kernel_h, kernel_w)
learn.model[0][0].weight.shape

# Numbers that started as Gaussian noise, evolved into edge detectors
learn.model[0][0].weight.data[:2]
```

Those numbers started as Gaussian noise and evolved into detectors for edges, textures, and eventually semantic concepts — all through the gradient descent loop Howard just walked through from scratch.

---

## Step 10 — Model Selection and the Pareto Frontier

The lesson opens with a survey of image model architectures benchmarked on top-1 accuracy, inference speed, and parameter count. Howard's framework for using that chart:

The wrong approach is to always pick the highest-accuracy model. The right approach is to identify the **Pareto frontier** — models where no other model is simultaneously faster and more accurate — then pick based on deployment constraints. For a latency-sensitive API endpoint, a smaller EfficientNet variant may dominate a more accurate but slower ViT. For an offline batch pipeline, the ranking flips.

Howard also makes a point about data quantity that the industry consistently gets wrong: the dominant mistake is collecting more labelled data when the model is already bottlenecked on something else. Before commissioning a labelling campaign, fit a model on what you have, examine the failure modes, and decide whether the errors are data-limited or architecture-limited.

---

## Swadia's Supplementary Tutorial: 10 Key Points

[▶ Watch the Swadia tutorial on YouTube](https://youtu.be/npQ2IORdlvU)

The following points synthesise the core pedagogical contributions of the Swadia tutorial, structured as an ordered learning sequence that complements Howard's top-down approach:

<div class="swadia-point"><strong>Point 1 — Context First, Mechanics Second.</strong> Before any equation is introduced, establish why it matters. Neural networks exist to solve the function-approximation problem. Anchoring every formula in this problem statement prevents the 'math without meaning' trap that causes most learners to stall.</div>

<div class="swadia-point"><strong>Point 2 — The Biological Metaphor Is a Scaffold, Not a Specification.</strong> The McCulloch-Pitts neuron (1943) gave us the vocabulary. Modern artificial neurons follow this template as a scaffold for intuition, not a literal description of computation. Don't over-invest in the analogy.</div>

<div class="swadia-point"><strong>Point 3 — Parameters Are the Entire Knowledge of the Model.</strong> After training, a model IS its weight matrices. There is no other store of information. Internalising this dispels the mysticism around 'AI knowing things' and grounds all subsequent questions in concrete mathematics.</div>

<div class="swadia-point"><strong>Point 4 — Loss Is a Design Choice.</strong> MSE, cross-entropy, Huber loss — engineering choices with mathematical consequences. Students should practice swapping loss functions and observing the effects rather than treating any one as canonical.</div>

<div class="swadia-point"><strong>Point 5 — The Learning Rate Is the Most Important Hyperparameter.</strong> Too large: the optimiser overshoots. Too small: training takes forever. Learning rate scheduling and warmup strategies follow from this single observation.</div>

<div class="swadia-point"><strong>Point 6 — One Hidden Layer Is Enough; Depth Adds Efficiency.</strong> A single hidden layer can approximate any function. What depth buys you is efficiency — the same approximation using far fewer parameters. This is the practical motivation for 'deep' learning.</div>

<div class="swadia-point"><strong>Point 7 — Overfitting Means the Model Learned the Data, Not the Task.</strong> Train loss down, validation loss up — that is the diagnostic. Regularisation, dropout, and data augmentation are interventions at this diagnostic point.</div>

<div class="swadia-point"><strong>Point 8 — GPUs Accelerate Matrix Multiplication, Not Magic.</strong> A forward pass is a sequence of matrix multiplications interleaved with elementwise nonlinearities. GPUs are designed precisely for this pattern of computation.</div>

<div class="swadia-point"><strong>Point 9 — Feature Engineering Is Still Required.</strong> Log-transforming skewed features, normalising continuous inputs, and dummy-encoding categoricals are not optional. They directly affect the condition number of gradient updates.</div>

<div class="swadia-point"><strong>Point 10 — Transfer Learning Is the Practical Default.</strong> Training from scratch is rarely necessary. Pretrained models encode general feature hierarchies that fine-tune to new tasks with a fraction of the data and compute. This is the workflow that makes deep learning practically useful outside of large research labs.</div>

---

## Jeremy Howard: The Man Who Decided to Democratise AI

<div>
<svg viewBox="0 0 700 180" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:560px;display:block;margin:1.5em auto;background:#0d2018;border-radius:8px;border:1px solid #1b5e20">
  <text x="350" y="26" text-anchor="middle" fill="#1b5e20" font-size="13" font-weight="bold">Jeremy Howard — The fast.ai Origin Story</text>
  <!-- Timeline -->
  <line x1="40" y1="90" x2="660" y2="90" stroke="#2e7d32" stroke-width="2"/>
  <!-- Nodes -->
  <circle cx="80"  cy="90" r="18" fill="#2e7d32"/>
  <text x="80"  y="87" text-anchor="middle" fill="white" font-size="9" font-weight="bold">Melb.</text>
  <text x="80"  y="99" text-anchor="middle" fill="white" font-size="9">Univ.</text>
  <text x="80"  y="112" text-anchor="middle" fill="#1b5e20" font-size="9">Philosophy</text>
  <text x="80"  y="122" text-anchor="middle" fill="#90a4ae" font-size="8">degree</text>
  <circle cx="190" cy="90" r="18" fill="#388e3c"/>
  <text x="190" y="87" text-anchor="middle" fill="white" font-size="9" font-weight="bold">McKinsey</text>
  <text x="190" y="99" text-anchor="middle" fill="white" font-size="9">/ AT Kearney</text>
  <text x="190" y="112" text-anchor="middle" fill="#1b5e20" font-size="9">8 years</text>
  <text x="190" y="122" text-anchor="middle" fill="#90a4ae" font-size="8">consulting</text>
  <circle cx="320" cy="90" r="18" fill="#43a047"/>
  <text x="320" y="87" text-anchor="middle" fill="white" font-size="9" font-weight="bold">Kaggle</text>
  <text x="320" y="99" text-anchor="middle" fill="white" font-size="9">#1 Global</text>
  <text x="320" y="112" text-anchor="middle" fill="#1b5e20" font-size="9">2010–2011</text>
  <text x="320" y="122" text-anchor="middle" fill="#90a4ae" font-size="8">World's best</text>
  <circle cx="450" cy="90" r="18" fill="#66bb6a"/>
  <text x="450" y="87" text-anchor="middle" fill="#1b5e20" font-size="9" font-weight="bold">fast.ai</text>
  <text x="450" y="99" text-anchor="middle" fill="#1b5e20" font-size="9">founded</text>
  <text x="450" y="112" text-anchor="middle" fill="#1b5e20" font-size="9">2016</text>
  <text x="450" y="122" text-anchor="middle" fill="#90a4ae" font-size="8">w/ R. Thomas</text>
  <circle cx="580" cy="90" r="18" fill="#81c784"/>
  <text x="580" y="87" text-anchor="middle" fill="#1b5e20" font-size="9" font-weight="bold">Answer</text>
  <text x="580" y="99" text-anchor="middle" fill="#1b5e20" font-size="9">.AI</text>
  <text x="580" y="112" text-anchor="middle" fill="#1b5e20" font-size="9">Nov 2024</text>
  <text x="580" y="122" text-anchor="middle" fill="#90a4ae" font-size="8">applied AI lab</text>
</svg>
</div>

Jeremy Howard did not follow a conventional path into AI research. He studied philosophy at the University of Melbourne — a choice that shaped his thinking about pedagogy, ethics, and the difference between knowing something and understanding it. After eight years in management consulting (McKinsey and AT Kearney), he taught himself machine learning, competed on Kaggle, and became the world's top-ranked data scientist in 2010 and 2011 — not through access to proprietary data or exclusive compute, but through systematic application of techniques available to anyone.

That experience convinced Howard of something that would define his subsequent career: the gap between AI researchers and practitioners was not a capability gap but a pedagogical one. The knowledge existed; the on-ramps did not.

### The fast.ai Philosophy

In 2016, Howard co-founded fast.ai with Rachel Thomas with a simple mission: make deep learning accessible to domain experts who were not career machine learning researchers. The pedagogical approach they developed — sometimes called the "top-down" or "whole game" method — inverts the conventional curriculum sequence.

Traditional deep learning courses begin with linear algebra, probability theory, and optimisation — the theoretical foundations. Students spend months on prerequisites before writing a line of code that does anything useful. Howard's observation was that this approach works for students who have already committed to years of study, but fails the practitioner who needs to know whether deep learning is applicable to their domain before making that commitment.

fast.ai begins with a working model. Lesson 1 trains a state-of-the-art image classifier in four lines of code. Students see results before they understand the mechanism. This creates what Howard calls "a hook" — genuine motivation to then go deeper and understand why it worked. The prerequisite mathematics becomes meaningful precisely because the student has already used the tool and wants to understand it more deeply.

This is not a shortcut. Howard is emphatic that full understanding is the goal — but he maintains that the fastest path to full understanding is not the conventional prerequisite-first route. This claim is, it turns out, well-supported by learning science research, as we'll see below.

### Howard on the Future

Howard's public writings and interviews reveal a consistent thread: he believes that the dominant risk from AI is not malevolence but concentration — the scenario in which powerful AI tools are accessible only to the largest institutions, further entrenching existing inequalities. fast.ai is explicitly a counter-measure to this scenario.

In his 2024 AI panel discussions and interviews, Howard has argued that the most important technical development of the next decade will not be larger models but more efficient ones — models that run on commodity hardware and can be customised by individual practitioners. His founding of Answer.AI in November 2024, described as a "results-focused AI lab," is a direct expression of this philosophy.

---

## The Learning Science Behind Howard's Approach

The success of fast.ai's pedagogy is not accidental — it maps closely onto findings from cognitive science and educational psychology that have accumulated over decades. Understanding why the approach works will help you extract more value from it.

### Desirable Difficulty

Howard's top-down method creates what educational psychologists call "desirable difficulty." Encountering the whole problem before understanding all the parts is initially uncomfortable. This discomfort is the signal that learning is occurring, not evidence that something is wrong. Research by Robert Bjork at UCLA has consistently shown that more challenging learning conditions produce better long-term retention, even when they produce slower initial performance.

### Worked Examples and Cognitive Load Theory

The fast.ai notebooks are worked examples. John Sweller's cognitive load theory predicts that novices learn more efficiently from studying worked examples than from attempting to solve problems independently from the outset. Problem-solving requires cognitive resources for both domain content and problem-solving strategy simultaneously — a load that exceeds the working memory capacity of most learners encountering a new domain. Worked examples free cognitive resources for the content itself.

### Spaced Repetition and Interleaving

The fast.ai curriculum returns to the same concepts multiple times across lessons, each time with more context and depth. This is spaced repetition in practice — exposure to material after increasing intervals is the most evidence-based intervention for long-term retention (Ebbinghaus, 1885; Cepeda et al., 2006). Interleaving different types of practice — gradient descent, then matrix multiplication, then the spreadsheet — further improves retention compared to blocking (practicing one topic exhaustively before moving to the next).

### The Feynman Technique at Scale

fast.ai's forums are central to the pedagogy. Students are encouraged to explain concepts to each other — a structured implementation of the Feynman Technique. Every point of confusion in an explanation to another person reveals a gap in the explainer's own understanding. The forums create a low-stakes environment for this kind of public retrieval practice at scale.

---

## What AI Will Do for Learners Who Act Now

The transformation under way is not a future scenario — it is the current state of every field that processes information. Learners who invest time in foundations now gain access to capabilities that currently require expensive specialist consultants:

**Personal productivity tools.** Fine-tuned language models for your specific domain. Image classifiers trained on your own data. NLP extractors that pull structured information from unstructured text — clinical notes, legal documents, research papers. These tools currently require specialist ML engineers for most organisations. Practitioners who complete fast.ai can build them independently.

**Professional differentiation.** In medicine, law, finance, engineering, and research — every field that processes data — practitioners who can build and evaluate AI tools will command significant advantages over those who can only consume them.

**Research acceleration.** For scientists, the ability to build custom models means reduced dependence on off-the-shelf tools that may not fit your domain. The ability to fine-tune a language model on your own corpus, or to train an image classifier on your own labelled data, compresses research timelines that once required collaborations with dedicated ML labs.

**Agency in an AI world.** Perhaps most importantly: understanding how neural networks work gives you the conceptual tools to evaluate AI claims critically, audit model outputs, and make informed decisions about when to trust and when to question AI systems. This is the difference between using AI as a tool and being used by it.

The window during which this knowledge provides a genuine competitive advantage is finite. It will close. The practitioners who move through it will not be those who waited for a simpler on-ramp — they will be those who found a guide who could make the existing on-ramp navigable.

---

## Why Study with Dr. Neal Aggarwal?

Forty years of teaching information technology and artificial intelligence across academic, corporate, and individual-mentorship contexts confer a particular kind of understanding that no amount of self-study can replicate: the ability to recognise where a given student is stuck, why they're stuck there, and what angle of re-entry will unstick them.

The fast.ai curriculum is excellent. But it was designed for a specific learner archetype, and most learners are not that archetype. They have domain knowledge that the curriculum doesn't assume. They have cognitive habits developed in adjacent fields. They have time constraints the standard schedule doesn't accommodate. They have professional motivations that the canonical examples don't speak to.

Working through fast.ai with a guide who has led hundreds of learners through this material means those mismatches get resolved in real time, not after three weeks of stalling on a concept that could have been reframed in five minutes.

The practical outcome: students who study with Dr. Neal complete the fast.ai curriculum in half the median time, with substantially deeper practical understanding — and they leave with a project, not just a certificate.

[→ Contact Dr. Neal Aggarwal for 1-to-1 sessions, group workshops, and curriculum design](https://drnealaggarwal.info)

---

## Download the Learning Guide

A structured two-week study plan synthesising Howard's Lesson 3, the Swadia tutorial's 10 key points, and learning science research:

<div class="guide-downloads">
<strong>📥 Fast.ai Lesson 3: Structured Learning Guide</strong><br/>
Includes: 10 Swadia key points · Two-week study plan · Checkpoint questions · Code patterns to memorise · Learning science strategies<br/>
<a href="/static/fastai-lesson3-learning-guide.pdf">Download PDF</a>
<a href="/static/fastai-lesson3-learning-guide.epub">Download EPUB</a>
</div>

---

## Testimonials

<div class="testimonials">

<div class="testimonial">
"I'd worked through three different deep learning courses before finding Dr. Neal's guided approach to fast.ai. What distinguished this experience was his insistence on understanding before application — every time I thought I had the right answer, he'd ask a question that revealed I'd memorised a pattern rather than grasped the principle. It took longer, but I came out the other side genuinely able to build things, not just run notebooks."
<div class="attribution">— Dr. M., Computational Biologist, UCL</div>
</div>

<div class="testimonial">
"The fast.ai curriculum is exceptional, but navigating it alone meant I kept stopping at the same points. Dr. Neal's capacity to identify precisely which conceptual link was missing — and to supply exactly the right analogy or worked example to repair it — is something I've rarely encountered in 20 years of postgraduate education. He manages the rare combination of technical rigour and genuine patience for the learner's pace."
<div class="attribution">— Prof. P., Department of Computer Science, University of Edinburgh</div>
</div>

<div class="testimonial">
"Genuinely transformed how I work. Three months after completing the fast.ai course under Dr. Neal's guidance, I had deployed a custom NLP pipeline that is saving my research group approximately 15 hours per week on literature screening. I couldn't have built that from the course alone — the targeted mentorship was what converted understanding into deployment."
<div class="attribution">— Dr. K., Senior Research Fellow, Pharmacology</div>
</div>

<div class="testimonial">
"Excellent teaching. Clear, direct, technically uncompromising."
<div class="attribution">— Ms. R., Lead Data Analyst, NHS Digital</div>
</div>

<div class="testimonial">
"What I will remember most about studying with Dr. Neal is his uncommon willingness to let you stay confused for exactly as long as is productive, and then to step in with precisely the right intervention. He does not rush to resolve discomfort — he understands that struggle is often where the real learning is happening. At the same time, he has an acute sense of when confusion has become discouraging rather than productive, and pivots accordingly. I've studied with a number of excellent teachers over a long academic career; Dr. Neal's attunement to the individual learner's state is genuinely exceptional."
<div class="attribution">— Prof. A., Emeritus Professor of Statistics, Imperial College London</div>
</div>

</div>

---

## Key Takeaways

**Gradient descent is parameter search guided by local slope information.** The loss surface is high-dimensional and non-convex, but local gradient information is sufficient to make progress because the surface is smooth enough in practice that short steps in the downhill direction rarely get stuck catastrophically.

**ReLUs are not the only activation function, but they are the canonical example of why nonlinearity is necessary.** A stack of purely linear layers collapses to a single linear transformation regardless of depth.

**Matrix multiplication is not an implementation detail** — it is the reason deep learning runs on GPUs and scales to billion-parameter models.

**Normalisation and log-transforming skewed features are not preprocessing niceties.** They directly affect the condition number of gradient updates.

**What comes next:** Lesson 3 closes with a preview of NLP via Hugging Face Transformers — demonstrating that the same machinery (parameterised function family, loss, gradient descent) scales to sequence-to-sequence tasks with no fundamental change in the algorithm. The architecture changes; the optimisation loop does not.

---

## References and Resources

<div class="notebooklm-banner">
📚 <strong>NotebookLM Notebook for This Lesson</strong><br/>
Slide decks, mind map, and AI-generated audio overview:<br/>
<a href="https://notebooklm.google.com/notebook/8e7184c3-a0c5-47a5-8992-85e90f8b5261" target="_blank">→ Open in NotebookLM (Google account required)</a>
</div>

**Primary fast.ai Resources**

- [fast.ai Lesson 3 Official Page](https://course.fast.ai/Lessons/lesson3.html)
- [Lesson 3 Video — YouTube](https://www.youtube.com/watch?v=hBBOjCiFcuo)
- [Lesson 3 Summary — fast.ai](https://course.fast.ai/Lessons/Summaries/lesson3.html)
- [How does a neural net really work? — Kaggle Notebook (Jeremy Howard)](https://www.kaggle.com/code/jhoward/how-does-a-neural-net-really-work)
- [Which image models are best? — Kaggle Notebook (Jeremy Howard)](https://www.kaggle.com/code/jhoward/which-image-models-are-best/)
- [Chapter 4: MNIST Basics — fastbook GitHub](https://github.com/fastai/fastbook/blob/master/04_mnist_basics.ipynb)
- [Swadia Supplementary Tutorial — YouTube](https://youtu.be/npQ2IORdlvU)
- [fast.ai Community Forums](https://forums.fast.ai)
- [fast.ai GitHub Course Repository](https://github.com/fastai/course22)

**The Book**

- [Deep Learning for Coders with fastai and PyTorch — Amazon](https://www.amazon.com/Deep-Learning-Coders-fastai-PyTorch/dp/1492045527) (Howard & Gugger, O'Reilly 2020)
- [Full book available free on GitHub](https://github.com/fastai/fastbook) — the entire text, including all notebooks, is openly available for those who cannot afford to purchase it.

**Historical Context**

- McCulloch, W.S. & Pitts, W. (1943). A Logical Calculus of the Ideas Immanent in Nervous Activity. *Bulletin of Mathematical Biophysics*, 5(4), 115–133.
- Rosenblatt, F. (1958). The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain. *Psychological Review*, 65(6), 386–408.
- Rumelhart, D.E., Hinton, G.E. & Williams, R.J. (1986). Learning Representations by Back-propagating Errors. *Nature*, 323, 533–536.

**Learning Science**

- Bjork, R.A. (1994). Memory and Metamemory Considerations in the Training of Human Beings. In J. Metcalfe & A. Shimamura (Eds.), *Metacognition*. MIT Press.
- Sweller, J. (1988). Cognitive Load During Problem Solving. *Cognitive Science*, 12(2), 257–285.
- Cepeda, N.J. et al. (2006). Distributed Practice in Verbal Recall Tasks. *Psychological Bulletin*, 132(3), 354–380.

---

*Based on Jeremy Howard's fast.ai Practical Deep Learning for Coders 2022 · Lesson 3: Neural Net Foundations · This is an example of the course materials produced by Dr Neal and used to teach students through his one-to-one AI Learners Course.*

*Post by Dr. Neal Aggarwal · [drnealaggarwal.info](https://drnealaggarwal.info) · 40+ years teaching IT and AI*
