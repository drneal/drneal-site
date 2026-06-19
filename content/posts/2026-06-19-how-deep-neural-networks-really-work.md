---
title: "How Deep Neural Networks Really Work: A Developer's Guide to fast.ai Lesson 3"
date: 2026-06-19
category: Deep Learning
tags: deep learning, neural networks, fast.ai, gradient descent, PyTorch, ReLU
level: Intermediate
read_time: 14 min
summary: Jeremy Howard's fast.ai Lesson 3 reconstructed in full — from a manually-tuned quadratic on a toy dataset all the way to the matrix-algebra skeleton of a multi-layer neural network — at the level of detail an experienced developer needs to actually internalize.
featured: false
---

*Based on Jeremy Howard's fast.ai Practical Deep Learning for Coders 2022 · Lesson 3: Neural Net Foundations*

Jeremy Howard's fast.ai Lesson 3 is where the course transitions from "use the library" to "understand what the library is doing." This post reconstructs Howard's argument in full — from a manually-tuned quadratic on a toy dataset all the way to the matrix-algebra skeleton of a multi-layer neural network — at the level of detail an experienced developer needs to actually internalize, not just nod along to.

## The Central Question Howard Poses

Howard opens the computational core of the lesson by asking something deceptively simple: what are the weights in a trained model, and how can numbers figure out something important about the world? This is the right question to anchor around, because it forces you to unpack three distinct concerns that the deep learning literature often muddles together:

1. **The function family.** What class of mathematical function is expressive enough to represent the mapping you care about?
2. **The loss.** How do you quantify the gap between predictions and ground truth in a way that's differentiable?
3. **The optimisation algorithm.** Given the loss and its gradient, how do you search the parameter space efficiently?

Howard's pedagogical move is to answer all three questions concretely, building each from scratch before introducing the abstractions that fast.ai and PyTorch provide.

## Step 1 — Fitting a Function by Hand

Howard begins with a general quadratic:

```
f(x) = a·x² + b·x + c
```

The point is not the specific function — it's the parameterisation. By exposing three free parameters (`a`, `b`, `c`), a single function template can realise any specific quadratic by fixing those parameters. Howard demonstrates this with an interactive Jupyter widget, manually dragging sliders to minimise the visual distance between the curve and a randomly generated dataset.

This immediately surfaces a core insight: **fitting a model is a search problem in parameter space.** The widget approach works for three parameters on a 2D toy dataset, but it is obviously unscalable. This is the deliberate setup for everything that follows.

## Step 2 — Introducing Loss (MSE)

Rather than relying on visual intuition, Howard introduces a scalar summary of "how wrong the current parameters are." For a regression problem the natural choice is Mean Squared Error:

```
L = (1/n) · Σ (ŷᵢ − yᵢ)²
```

MSE has two properties that matter here. First, it's everywhere differentiable — there are no kinks to worry about. Second, squaring penalises large residuals super-linearly, which makes the optimiser concentrate on the worst-fitting examples. Howard is deliberate about presenting the loss as a design choice, not a fact of nature; later lessons swap in cross-entropy for classification tasks.

> **Key insight:** The loss collapses the entire dataset's prediction quality into a single number. Optimisation then becomes: decrease this number by adjusting the parameters. Everything else in training is mechanics around that one idea.

## Step 3 — Gradients and the Chain Rule (No Calculus Required)

Howard's treatment of derivatives is deliberately minimal. You don't need to hand-compute a Jacobian. You need to know one thing: for a given set of parameter values, PyTorch can tell you the slope of the loss with respect to each parameter — i.e., if you nudge parameter `a` upward by one unit, does the loss go up or down, and by approximately how much?

In code, the workflow is:

```python
# Store parameters as a tensor requiring gradients
params = torch.tensor([a, b, c], requires_grad=True)

# Compute predictions and loss
preds = params[0]*x**2 + params[1]*x + params[2]
loss  = ((preds - y)**2).mean()

# Ask PyTorch to back-propagate
loss.backward()

# Inspect the gradients
print(params.grad)  # tensor([da, db, dc])
```

`params.grad[0]` answers: "by how much does the loss increase per unit increase in `a`?" A positive gradient means increasing `a` makes things worse; a negative gradient means increasing `a` helps. This is the entire information content you need for the next step.

## Step 4 — Gradient Descent

With gradients in hand, the update rule is:

```
θ ← θ − lr · ∇L(θ)
```

Subtract a small multiple of the gradient from each parameter. If the gradient for `a` is positive (loss rises with `a`), decreasing `a` reduces the loss. Do this iteratively and you descend toward a local minimum. Howard implements a manual loop to make this concrete:

```python
lr = 1e-3

for _ in range(100):
    loss = mse(quadratic(params, x), y)
    loss.backward()
    with torch.no_grad():
        params -= lr * params.grad
        params.grad.zero_()   # must clear or gradients accumulate
```

The call to `params.grad.zero_()` is the single most commonly forgotten line in introductory PyTorch code — and Howard flags it explicitly. PyTorch accumulates gradients by default, which is a feature for certain architectures (e.g., gradient checkpointing), but a footgun for a simple training loop.

### Learning Rate: Why Size Matters

Howard visualises the loss landscape as a bowl (a quadratic approximation is locally valid near any smooth minimum). A large learning rate causes the optimiser to overshoot the bottom of the bowl, potentially diverging. A learning rate that's too small means thousands of iterations to converge. Howard's practical heuristic at this stage: start around `1e-3`, watch the loss curve, and halve it if the curve oscillates.

> **Gradient interpretation in units:** Howard makes a point that experienced ML engineers often skip: the gradient is in units of (loss units / parameter units). If your "Fare" column is in dollars and the loss is in squared probability-of-survival, the raw gradient magnitude is not directly comparable across columns. This motivates normalisation — covered in the Titanic spreadsheet section below.

## Step 5 — Why Quadratics Are Not Enough

Having established the full gradient descent loop, Howard pivots to the expressiveness problem. A quadratic can model one hump. Real-world mappings — image pixels to class labels, text tokens to sentiment — require functions of effectively arbitrary complexity. You could try higher-degree polynomials, but they are numerically unstable and hard to control.

The key question is: **is there a simple building block that can be composed into arbitrarily complex functions?**

## Step 6 — The Rectified Linear Unit (ReLU)

Howard's answer is the ReLU:

```
ReLU(x) = max(0, x)
```

This function is about as simple as a nonlinear function can be — it's zero for negative inputs and linear for positive inputs. Two parameters control a shifted, scaled version:

```
f(x) = max(0, w·x + b)
```

A single ReLU is nearly useless. But the universal approximation theorem guarantees that a sum of enough ReLUs can approximate any continuous function on a compact domain to arbitrary precision. Howard demonstrates this interactively by stacking two ReLUs and showing how four parameters produce a more complex shape than any single parabola could. The pattern generalises: a network with millions of ReLUs — each controlled by learned weights and biases — can represent virtually any input-output mapping.

> **The "two circles to an owl" summary:** Howard's compressed version of deep learning is: (1) start with a parameterised family of functions (ReLU stacks); (2) define a loss; (3) compute gradients; (4) take a small step downhill; (5) repeat. That's it. Everything else — batch normalisation, residual connections, attention — is engineering that makes this core loop work better in practice.

## Step 7 — Matrix Multiplication as the Computational Substrate

When your network has millions of ReLUs, computing predictions naively (one ReLU at a time) is prohibitively slow. Howard introduces the key linear-algebra insight: a layer of neurons computing `w₁x₁ + w₂x₂ + ... + wₙxₙ + b` for each of `m` neurons simultaneously is exactly a matrix multiplication.

If `X` is the input matrix (batch × features) and `W` is the weight matrix (features × neurons), then:

```
Z = X · W + b
```

This is a single BLAS call. GPUs are designed to execute billions of these floating-point multiply-accumulate operations in parallel — which is the entire reason deep learning became practical on commodity hardware. Howard is emphatic: you don't need deep linear algebra knowledge; you need to understand what matrix multiplication does (dot products of rows against columns) and why it maps onto neural network computations.

```python
# A single linear layer in pure PyTorch
W = torch.randn(n_inputs, n_hidden, requires_grad=True)
b = torch.zeros(n_hidden,           requires_grad=True)

def linear(x): return x @ W + b
def relu(x):   return x.clamp(min=0)

# One hidden layer
def model(x): return linear(relu(linear(x)))
```

## Step 8 — Building a Neural Network in a Spreadsheet (Titanic)

To cement these concepts Howard walks through a spreadsheet implementation of gradient descent on the Kaggle Titanic dataset. This is a deliberately unglamorous exercise — the point is to see every operation in isolation without library abstractions hiding it.

The key preprocessing decisions Howard walks through are worth cataloguing:

**1. Dummy-encode categoricals.** Sex, Pclass, and Embarked become binary columns. Howard notes you only need k−1 dummy variables for a k-category feature (the dropped category becomes the reference level). Getting this wrong is a common source of rank-deficient design matrices.

**2. Normalise continuous features.** Age and Fare are on very different scales. A gradient computed against raw Fare (hundreds of dollars) is orders of magnitude larger than a gradient computed against Age (tens of years). This means the same learning rate can simultaneously be too large for one feature and too small for another. The fix: subtract the mean and divide by standard deviation.

**3. Apply log to Fare.** Fare is right-skewed — a few first-class tickets cost vastly more than the median. A log transform compresses the tail, making the distribution roughly symmetric and ensuring the gradient signal from extreme values is proportional to the feature's information content rather than its raw magnitude.

**4. Build two linear layers with ReLU.** The first linear layer maps the feature matrix to a hidden representation. Howard applies a ReLU (`MAX(0, cell)` in spreadsheet terms), then passes the result through a second linear layer to produce a scalar prediction. That's a minimal two-layer neural network.

**5. Compute MSE and iterate.** Parameters for both layers are initialised to small random values, the loss is computed, and a manual gradient descent loop runs.

> **The critical conceptual point:** a neural network with one hidden layer is just two regression models stacked, with the output of the first passed through a nonlinearity before being fed to the second. There is no mysticism — it is additive function composition over a parameterised function family.

## Step 9 — What's Actually Stored in a Trained Model

Howard returns to the original question: what are the weights? After running gradient descent to convergence, the parameter tensors `W₁`, `b₁`, `W₂`, `b₂` contain numbers that, when matrix-multiplied against an input, produce a useful output. There is no explicit rule stored. The model's "knowledge" is entirely encoded in the geometry of those high-dimensional parameter matrices.

Inspecting those matrices is instructive. Howard shows how to drill into the layers of a pretrained fastai `vision_learner`:

```python
learn = vision_learner(dls, resnet34, metrics=error_rate)

# Access the underlying PyTorch module
learn.model

# Inspect the first convolution layer's weights
# Shape: (out_channels, in_channels, kernel_h, kernel_w)
learn.model[0][0].weight.shape

# The actual numbers — initially random, learned after training
learn.model[0][0].weight.data[:2]
```

Those numbers started as Gaussian noise and evolved into detectors for edges, textures, and eventually semantic concepts — all through the gradient descent loop Howard just walked through from scratch.

## Step 10 — Model Selection and the Comparison Chart

The lesson opens with a survey of image model architectures — Howard's Kaggle notebook benchmarking dozens of models on top-1 accuracy, inference speed, and parameter count. His framework for using that chart is worth internalising:

The wrong approach is to always pick the highest-accuracy model. The right approach is to identify the **Pareto frontier** — models where no other model is simultaneously faster and more accurate — then pick based on your deployment constraints. For a latency-sensitive API endpoint, a smaller EfficientNet variant may dominate a more accurate but slower ViT. For an offline batch pipeline, the ranking flips.

Howard also makes a point about data quantity that the industry consistently gets wrong: the dominant mistake is collecting more labelled data when the model is already bottlenecked on something else. Before commissioning a labelling campaign, fit a model on what you have, examine the failure modes, and decide whether the errors are data-limited or architecture-limited. If the model trains to near-zero loss but generalises poorly, you have a regularisation problem. If it cannot even fit the training set, you likely need a better architecture or more capacity.

## Key Takeaways for Practitioners

Having absorbed this lesson, the following should be intuitive rather than rote facts:

**Gradient descent is parameter search guided by local slope information.** The loss surface is high-dimensional and non-convex, but local gradient information is sufficient to make progress because the surface is smooth enough in practice that short steps in the downhill direction rarely get stuck catastrophically.

**ReLUs are not the only activation function, but they are the canonical example of why nonlinearity is necessary.** A stack of purely linear layers collapses to a single linear transformation regardless of depth. The nonlinearity at each layer is what gives depth its expressive power.

**Matrix multiplication is not an implementation detail** — it is the reason deep learning runs on GPUs and scales to billion-parameter models. Understanding that a forward pass is a sequence of matrix multiplications interleaved with elementwise nonlinearities is sufficient to reason about computational cost, memory footprint, and parallelisation.

**Normalisation and log-transforming skewed features are not preprocessing niceties.** They directly affect the condition number of the gradient updates. A poorly conditioned input can make gradient descent effectively single-dimensional even in a high-dimensional parameter space.

## What Comes Next

Lesson 3 closes with a brief preview of Natural Language Processing via Hugging Face Transformers — demonstrating that the same conceptual machinery (parameterised function family, loss, gradient descent) scales to sequence-to-sequence tasks with no fundamental change in the algorithm. The architecture changes; the optimisation loop does not.

The homework Howard assigns is to work through the Titanic spreadsheet independently and attempt the Kaggle Titanic competition. The practical value is not the leaderboard position — it's the experience of making every data cleaning and feature engineering decision yourself, without a wrapper function to paper over the choices.

---

## Primary Resources Referenced in This Lesson

- [How does a neural net really work? (Kaggle notebook)](https://www.kaggle.com/code/jhoward/how-does-a-neural-net-really-work)
- [Which image models are best? (Kaggle notebook)](https://www.kaggle.com/code/jhoward/which-image-models-are-best/)
- [Lesson 3 official page — fast.ai](https://course.fast.ai/Lessons/lesson3.html)
- [Chapter 4 — fastbook (MNIST basics, Jupyter notebook)](https://github.com/fastai/fastbook/blob/master/04_mnist_basics.ipynb)
- [Lesson 3 video — YouTube](https://www.youtube.com/watch?v=hBBOjCiFcuo)

*Based on fast.ai Practical Deep Learning for Coders 2022 · Lesson 3: Neural Net Foundations · Jeremy Howard*
