---
title: "Learning With Dr Neal"
date: 2026-06-26
category: Deep Learning
tags: deep learning, neural networks, fast.ai, gradient descent, spreadsheet, Excel, OpenOffice, Jeremy Howard, chapter 4, hands-on exercise
level: Beginner–Intermediate
read_time: 25 min
summary: "Before Chapter 4 throws you into the deep end, build a working neural network from scratch — in a spreadsheet. No code. No libraries. Just arithmetic you can see and touch."
featured: true
---

<style>
.audio-section {
  font-size: 0.8em;
  background: #1a1f2e;
  border-left: 4px solid #1a237e;
  padding: 1em 1.4em;
  border-radius: 0 6px 6px 0;
  margin: 1.5em 0;
}
.callout {
  font-size: 0.8em;
  background: #1e1a0e;
  border-left: 4px solid #f9a825;
  padding: 0.8em 1.2em;
  margin: 1.2em 0;
  border-radius: 0 4px 4px 0;
}
.openoffice-box {
  font-size: 0.8em;
  background: #0d1e2e;
  border: 1px solid #1565c0;
  border-left: 4px solid #42a5f5;
  border-radius: 0 6px 6px 0;
  padding: 1em 1.4em;
  margin: 1.5em 0;
}
.openoffice-box a { color: #90caf9; font-weight: bold; }
.step-header {
  font-size: 0.75em;
  background: #1a237e;
  color: #e8eaf6;
  padding: 0.3em 0.8em;
  border-radius: 4px;
  display: inline-block;
  margin-bottom: 0.4em;
  letter-spacing: 0.05em;
  font-weight: bold;
}
.excel-cmd {
  font-size: 0.8em;
  background: #1b3a1b;
  border-left: 3px solid #43a047;
  padding: 0.5em 1em;
  margin: 0.6em 0;
  border-radius: 0 4px 4px 0;
  font-family: monospace;
}
.oo-cmd {
  font-size: 0.8em;
  background: #1a2a3a;
  border-left: 3px solid #42a5f5;
  padding: 0.5em 1em;
  margin: 0.6em 0;
  border-radius: 0 4px 4px 0;
  font-family: monospace;
}
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
</style>

*This article accompanies Jeremy Howard's fast.ai Practical Deep Learning for Coders 2022 · Lesson 3, specifically the section from 1:04:30 to 1:20:47. It is part of the curriculum materials produced by Dr Neal for one-to-one AI Learners sessions.*

<audio controls style="width:100%;margin:1rem 0;">
  <source src="/static/audio/Build_a_Titanic_predictor_in_Excel.m4a" type="audio/mp4">
  Your browser does not support the audio element.
</audio>

[▶ Watch Lesson 3 on YouTube — jump to 1:04:30](https://www.youtube.com/watch?v=hBBOjCiFcuo&t=3870s)

---

## A Word Before You Start: This Is Chapter 4's Prelude

Chapter 4 of *Deep Learning for Coders with fastai and PyTorch* is where the hairy stuff really begins. It covers MNIST from scratch — building a complete image classifier using nothing but raw PyTorch tensors, gradient descent, and the same mathematical machinery that runs every serious deep learning model in the world. It is not light reading.

The exercise in this post is Jeremy Howard's recommended prelude to that chapter. If you can build a working neural network in a spreadsheet — and actually understand every cell — you will find Chapter 4 considerably less intimidating. The algebra is identical. The only difference is that the spreadsheet makes every intermediate value visible and touchable, whereas Python compresses it into a few lines of tensor arithmetic. If you have not yet worked through the full Lesson 3 material — gradient descent, ReLU, and how neural networks approximate any function — [read that companion post first](/post/2026-06-19-how-deep-neural-networks-really-work) before attempting the steps below.

This exercise is in the video, but not in chapter 3 nor 4 in the book. It is important to follow these steps keying in the column headings, figures and formulae as in these steps so you get a real feel for how a neural network works. You will be surprised at how much easier this exercise will make reading chapter 4 and all the other technologies that come after that.

<div class="callout">
💡 <strong>Three versions of this exercise, in increasing order of ambition:</strong><br/>
1. <strong>Excel</strong> (Windows/Mac) — follow the steps below exactly as Jeremy does in the video<br/>
2. <strong>OpenOffice / LibreOffice Calc</strong> (free, open source, any OS) — identical logic, equivalent commands<br/>
3. <strong>Python / NumPy</strong> (ambitious) — if you want to translate every step to code before tackling Chapter 4
</div>

---

## What OpenOffice Is (and Where to Get It)

**OpenOffice** and its more actively maintained fork **LibreOffice** are free, open-source office productivity suites that include a full-featured spreadsheet application called **Calc**. Calc reads and writes `.xlsx` files, supports all the functions used in this exercise (`SUMPRODUCT`, `MAX`, `MMULT`, `TRANSPOSE`, and a built-in Solver), and runs on Windows, macOS, and Linux.

<div class="openoffice-box">
📥 <strong>Download links (both are free and open source):</strong><br/><br/>
→ <a href="https://www.libreoffice.org/download/download-libreoffice/" target="_blank">LibreOffice (recommended — most actively maintained)</a><br/>
→ <a href="https://www.openoffice.org/download/" target="_blank">Apache OpenOffice</a><br/><br/>
Both are completely free, contain no ads, and require no account or licence key. LibreOffice is the version most developers recommend today. For the purposes of this exercise, either works identically — all the commands below apply to both.
</div>

---

## The Big Picture: What You Are Building

You are building a neural network that predicts Titanic survival. The architecture has two stages:

**Stage 1 — Linear Regression Model:** Multiply each passenger feature by a learnable coefficient, sum the results, and produce a single prediction number. This is a single neuron.

**Stage 2 — Neural Network:** Take two of those linear neurons, apply a ReLU (replace negatives with zero) to each, and add them together. This is a one-hidden-layer neural network — the same fundamental structure as modern deep learning, just tiny.

Both stages are trained by **gradient descent**: a numerical optimisation that adjusts the coefficients to minimise the error between your predictions and the known outcomes. In the spreadsheet you will run this using the built-in Solver tool. In Python you would use PyTorch's autograd. The mathematics is the same.

---

## Part 1: Setting Up Your Data

### Step 1 — Download the Titanic dataset

The fast.ai course uses the Titanic dataset from Kaggle. You can download `train.csv` from [kaggle.com/c/titanic/data](https://www.kaggle.com/c/titanic/data) (free account required) or use Jeremy's course spreadsheet directly from the course repo:

[▶ Download titanic-backprop.xlsx from GitHub](https://github.com/fastai/course22/tree/master/xl)

If using your own CSV, open it in Excel or LibreOffice Calc via **File → Open**.

---

### Step 2 — Prepare the feature columns

Jeremy uses a small, cleaned subset. Set up your spreadsheet so that **Row 1 is a header row** and data begins in Row 2. You need the following columns (add or compute them as needed):

| Column | Label | Notes |
|---|---|---|
| A | `survived` | 0 = died, 1 = survived (this is your **target** — what you're predicting) |
| B | `pclass` | Ticket class: 1, 2, or 3 |
| C | `sex` | **Convert to numeric:** male = 0, female = 1 |
| D | `age` | Numeric. Fill missing values with the column median |
| E | `sibsp` | Number of siblings/spouses aboard |
| F | `parch` | Number of parents/children aboard |
| G | `fare` | Ticket fare (numeric) |
| H | `embarked` | **Convert to numeric:** S = 0, C = 1, Q = 2 |

To remove rows where a column value is zero or empty, use AutoFilter:

1. Click any cell in your data range
2. **Data → AutoFilter** — dropdown arrows appear on each column header
3. Click the dropdown on your target column
4. Select **"Standard Filter..."**
5. Set: Field = your column, Condition = `=`, Value = `0`
6. Click OK — only rows with 0 are shown
7. Select all those visible rows (click the first row number, Shift+click the last)
8. Right-click a row number → **Delete Rows**
9. **Data → AutoFilter** again to turn off the filter

The remaining rows will all be non-zero.

For removing rows where **Age is empty** (not zero), the steps are the same but in step 5 set Condition = `=`, Value = leave blank (empty string). Or in the dropdown look for **(Empty)** as a filter option — click it, select all visible rows, delete, then remove the filter.

**Converting Sex to numeric in Excel:**
This exercise is in the video, but not in chapter 3 nor 4 in the book. It is important to follow these steps keying in the column headings, figures and formulae as in these steps so you get a real feel for how a neural network works. You will be surprised at how much easier this exercise will make reading chapter 4 and all the other technologies that come after that.

<div class="excel-cmd">
=IF(B2="male", 0, 1)
</div>

**OpenOffice/LibreOffice Calc — identical formula:**

<div class="oo-cmd">
=IF(B2="male", 0, 1)
</div>

Copy this formula down the entire column. Do the same for Embarked using nested IFs or `SWITCH`.

---

### Step 3 — Create a parameters row

Above your data (say, in Row 1 if your header is in Row 2, or use a clearly labelled section at the top of the sheet), create **one cell per feature** (7 cells for 7 features). These are your model's learnable coefficients — what gradient descent will adjust.

Initialise them with small random values centred around zero:

**Excel:**
<div class="excel-cmd">
=RAND()-0.5
</div>

**OpenOffice/LibreOffice Calc:**
<div class="oo-cmd">
=RAND()-0.5
</div>

Name your parameter cells. In Excel: select them, then type a name in the Name Box (top-left, where the cell address shows). Call this range `params`. This makes your formulas readable.

<div class="callout">
⚠️ <strong>Important:</strong> Once you have entered the parameters, press <strong>F9</strong> (recalculate) once to lock in the random starting values, then <em>immediately copy the cells and paste as Values Only</em> (Paste Special → Values). This prevents the parameters from re-randomising every time the sheet recalculates. You want the Solver to change the values, not RAND() to keep resetting them.
</div>

---

## Part 2: Building the Linear Regression Model

### Step 4 — Compute predictions for each passenger

For each data row, you compute a prediction by taking the **dot product** of the parameters and that row's features. This is the heart of a linear model.

**Excel — in the Prediction column (e.g. column I), enter for row 2:**
<div class="excel-cmd">
=SUMPRODUCT($B$1:$H$1, B2:H2)
</div>

Where `$B$1:$H$1` is your parameters row (use absolute references so it doesn't move when you copy the formula down).

**OpenOffice/LibreOffice Calc — identical:**
<div class="oo-cmd">
=SUMPRODUCT($B$1:$H$1, B2:H2)
</div>

Copy this formula down for every passenger row. Column I now contains your raw model output for each passenger.

---

### Step 5 — Compute the loss

You need a single number that measures how wrong your predictions are. Jeremy uses **Mean Absolute Error (MAE)**: the average absolute difference between each prediction and the true survival value.

**Excel — in a dedicated cell (e.g. K1):**
<div class="excel-cmd">
=AVERAGE(ABS(I2:I892 - A2:A892))
</div>

**Important:** This is an **array formula**. In Excel, enter it with **Ctrl+Shift+Enter** (not just Enter), and you will see curly braces `{ }` appear around it automatically. In Excel 365 / Excel 2019+, you can press Enter normally — array formulas are automatic.

**OpenOffice/LibreOffice Calc:**
<div class="oo-cmd">
=AVERAGE(ABS(I2:I892 - A2:A892))
</div>

Also entered with **Ctrl+Shift+Enter** in LibreOffice to confirm as an array formula.

Label this cell clearly — e.g. put `Loss (MAE)` in the cell to the left. This is the number the Solver will minimise.

---

### Step 6 — Run Solver to train the model

This is gradient descent — the same optimisation that trains GPT, image classifiers, and every other neural network. The Solver finds parameter values that minimise your loss.

**In Microsoft Excel:**

1. Go to **Data** tab → **Solver** (if you don't see Solver: File → Options → Add-ins → Manage Excel Add-ins → tick Solver Add-in → OK)
2. **Set Objective:** click the cell containing your MAE loss (e.g. `$K$1`)
3. **To:** select **Min**
4. **By Changing Variable Cells:** select your parameters range (e.g. `$B$1:$H$1`)
5. Under **Select a Solving Method:** choose **GRG Nonlinear**
6. Click **Solve**
7. When Solver finishes, select **Keep Solver Solution** and click **OK**

**In LibreOffice Calc:**

1. Go to **Tools** → **Solver**
2. **Target Cell:** your MAE loss cell
3. **Optimize result to:** select **Minimum**
4. **By changing cells:** your parameters range
5. Click **OK** to run

Watch the loss cell decrease as Solver iterates. When it converges, your parameters have been trained. The model is now making better predictions than it did with random weights.

---

## Part 3: Building the Neural Network

A single linear model has a fundamental limitation — it can only draw a straight line (or flat hyperplane) through the data. Adding a non-linearity (ReLU) and a second linear unit gives the network the ability to learn curved, complex boundaries.

### Step 7 — Add a second set of parameters

Copy your parameters row to a new row directly below it (e.g. Row 2 if your first parameters were in Row 1). Again initialise with `=RAND()-0.5`, then paste as values. You now have two sets of coefficients.

Label them: `params_1` and `params_2`.

---

### Step 8 — Compute two predictions and apply ReLU

For each passenger, compute two raw predictions — one from each parameter row — then apply a **Rectified Linear Unit (ReLU)**: replace any negative value with zero. This is the non-linearity that gives neural networks their power.

**Excel — Raw prediction from params_1 (column J):**
<div class="excel-cmd">
=SUMPRODUCT($B$1:$H$1, B3:H3)
</div>

**Excel — ReLU of first prediction (column K):**
<div class="excel-cmd">
=MAX(J3, 0)
</div>

**Excel — Raw prediction from params_2 (column L):**
<div class="excel-cmd">
=SUMPRODUCT($B$2:$H$2, B3:H3)
</div>

**Excel — ReLU of second prediction (column M):**
<div class="excel-cmd">
=MAX(L3, 0)
</div>

**Excel — Final neural net output = sum of the two ReLU outputs (column N):**
<div class="excel-cmd">
=K3 + M3
</div>

**OpenOffice/LibreOffice Calc — all identical:**
<div class="oo-cmd">
=SUMPRODUCT($B$1:$H$1, B3:H3)    ← first raw pred
=MAX(J3, 0)                        ← ReLU
=SUMPRODUCT($B$2:$H$2, B3:H3)    ← second raw pred
=MAX(L3, 0)                        ← ReLU
=K3 + M3                           ← neural net output
</div>

Copy all five formulas down for every passenger row.

---

### Step 9 — Update the loss cell

Change your MAE formula to reference the neural net output column (N) instead of the old single-model column (I):

**Excel:**
<div class="excel-cmd">
=AVERAGE(ABS(N3:N892 - A3:A892))
</div>

**OpenOffice/LibreOffice Calc:**
<div class="oo-cmd">
=AVERAGE(ABS(N3:N892 - A3:A892))
</div>

(Adjust row numbers to match your data range.)

---

### Step 10 — Train the neural network with Solver

Run Solver again, this time with **both** parameter rows as the variable cells.

**Excel:**
1. Data → Solver
2. Set Objective: loss cell → Min
3. By Changing Variable Cells: select **both** parameter rows together, e.g. `$B$1:$H$2`
4. Method: GRG Nonlinear → Solve

**LibreOffice Calc:**
1. Tools → Solver
2. Target cell: loss → Minimum
3. By changing cells: both parameter rows

The loss should now be lower than before — the two-neuron network is more expressive than the single linear model.

---

## Part 4: Matrix Multiplication (Bonus)

Jeremy shows that once you have more than a handful of features or neurons, writing out SUMPRODUCT formulas for each row individually becomes tedious. **Matrix multiplication** (`MMULT`) computes all the dot products simultaneously.

### Step 11 — Compute all predictions at once with MMULT

**Excel:**
<div class="excel-cmd">
=MMULT(B3:H892, TRANSPOSE($B$1:$H$2))
</div>

This produces a matrix where each row is a passenger and each column is one neuron's raw output — the equivalent of all your SUMPRODUCT formulas at once.

**OpenOffice/LibreOffice Calc:**
<div class="oo-cmd">
=MMULT(B3:H892, TRANSPOSE($B$1:$H$2))
</div>

In both applications, enter this as an array formula (**Ctrl+Shift+Enter**) and select a destination range the right size (number of passengers × number of neurons) before entering.

<div class="callout">
💡 This is exactly what PyTorch's <code>@</code> operator or <code>torch.matmul()</code> does — and it is the reason GPUs are so effective at deep learning. They can perform enormous matrix multiplications (thousands of rows, thousands of columns) in parallel.
</div>

---

## What You've Just Built

| Component | Spreadsheet version | PyTorch equivalent |
|---|---|---|
| Parameters | Cells in a row | `torch.tensor(..., requires_grad=True)` |
| Prediction | `SUMPRODUCT(params, features)` | `params @ features` |
| Loss | `AVERAGE(ABS(preds - actuals))` | `(preds - actuals).abs().mean()` |
| ReLU | `MAX(x, 0)` | `F.relu(x)` |
| Training | Excel/LibreOffice Solver | `loss.backward(); params -= params.grad * lr` |
| All predictions at once | `MMULT(features, TRANSPOSE(params))` | `features @ params.T` |

Every concept in Chapter 4 of the book — stochastic gradient descent, the forward pass, the activation function, the loss — maps directly onto what you have done in this spreadsheet. The book just compresses it into clean Python, vectorised across thousands of images simultaneously.

---

## Doing It in Python (For the Ambitious)

If you want to go further before Chapter 4, translate every step above into NumPy:

```python
import numpy as np
import pandas as pd

# Load and encode data
df = pd.read_csv('titanic/train.csv')
df['sex'] = (df['Sex'] == 'female').astype(float)
df['embarked'] = df['Embarked'].map({'S': 0, 'C': 1, 'Q': 2}).fillna(0)
df['age'] = df['Age'].fillna(df['Age'].median())

features = df[['Pclass', 'sex', 'age', 'SibSp', 'Parch', 'Fare', 'embarked']].values
targets  = df['Survived'].values.reshape(-1, 1)

# Initialise random parameters (equivalent to RAND()-0.5)
params = np.random.rand(7, 2) - 0.5   # 7 features, 2 neurons

# Forward pass: MMULT equivalent
raw     = features @ params            # shape: (passengers, 2)
relus   = np.maximum(raw, 0)          # ReLU: MAX(x, 0)
preds   = relus.sum(axis=1, keepdims=True)  # sum the two neurons

# Loss: MAE
loss = np.abs(preds - targets).mean()
print(f"Initial loss: {loss:.4f}")
```

From here you would implement gradient descent manually — a fine exercise that will make Chapter 4's PyTorch autograd feel like a revelation rather than a mystery.

---

## Why This Exercise Is Worth Your Time

The fast.ai philosophy is top-down: you use the tools before you understand the internals. But at the Chapter 4 inflection point, the book inverts — it asks you to understand the internals before you can properly use the tools. The spreadsheet exercise bridges that inversion. It makes the internals concrete and tactile at the cost of only a couple of hours.

Jeremy has said this exercise is one of his strongest recommendations to students who find Chapter 4 difficult. Having built a neural network with your own hands — even a tiny one, even in a spreadsheet — permanently changes the way you read the Python code that follows.

Do it in Excel. Do it in LibreOffice. Or do it in Python. But do it before you open Chapter 4. And if you haven't yet worked through the Lesson 3 foundations, [start with the companion guide →](/post/2026-06-19-how-deep-neural-networks-really-work)

---

<div class="notebooklm-banner">
📚 <strong>NotebookLM companion resource:</strong><br/>
All slide material, mind maps, and audio overviews for this fast.ai series are available in the course NotebookLM notebook.<br/>
<a href="https://notebooklm.google.com/notebook/8e7184c3-a0c5-47a5-8992-85e90f8b5261" target="_blank">→ Open NotebookLM Notebook (Google account required)</a>
</div>

---

## Why Study with Dr. Neal Aggarwal?

Forty years of teaching information technology and artificial intelligence across academic, corporate, and individual-mentorship contexts confer a particular kind of understanding that no amount of self-study can replicate: the ability to recognise where a given student is stuck, why they're stuck there, and what angle of re-entry will unstick them.

The fast.ai curriculum is excellent. But it was designed for a specific learner archetype, and most learners are not that archetype. Working through the course with a guide who has led hundreds of learners through this material means those mismatches get resolved in real time, not after three weeks of stalling on a concept that could have been reframed in five minutes.

Students who study with Dr. Neal complete the fast.ai curriculum in half the median time, with substantially deeper practical understanding — and they leave with a project, not just a certificate.

[→ Contact Dr. Neal Aggarwal for 1-to-1 sessions, group workshops, and curriculum design](/about#contact)
