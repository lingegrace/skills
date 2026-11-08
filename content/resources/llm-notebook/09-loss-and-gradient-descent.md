---
title: "Loss, Gradient Descent and Learning Rate, Explained Simply"
summary: "You will understand how a model measures its own mistakes (loss) and how it reduces them step by step through gradient descent, learning rate and batch size."
time: "7 min read"
order: 9
column: llm-notebook
series: "ML Crash Course notes"
status: published
---

Every model you use, from a spam filter to Claude, learned by doing one thing over and over: making a guess, measuring how wrong it was, and nudging itself to be a little less wrong. If you understand that loop, a lot of AI jargon stops being mysterious.

These are my notes from Google's Machine Learning Crash Course, rewritten for people who don't write code for a living. This first part covers loss and gradient descent: how a model measures its mistakes and how it improves.

## What is "loss"?

**Loss** is a number that says how far the model's predictions are from the true answers. Lower is better. Training a model means searching for the settings that make loss as small as possible.

The simplest model in the course is a straight line: a **weight** (how steep the line is) and a **bias** (where it starts). In the course's interactive exercise, you drag a Weight slider and a Bias slider and watch the loss go up or down. Training is that same slider-dragging, done automatically.

There are different ways to add up the errors. Two common ones:

| Loss function | How it works | What it does with outliers |
|---|---|---|
| **MSE** (mean squared error) | Squares each error, then averages | The model is pulled closer to the outliers, and further from most other points |
| **MAE** (mean absolute error) | Takes the size of each error, then averages | The model stays closer to most points and further from the outliers |

Why the difference? Squaring makes big errors count much more. An error of 10 becomes 100, while an error of 2 becomes only 4. So under MSE, a few unusual data points can drag the whole line towards them.

This is a choice, not a technical detail. Deciding whether the unusual cases should shape the model is a decision about whose data counts most.

## How does gradient descent work?

**Gradient descent** is the iterative process that finds the weight and bias that minimise loss. Each round (an **iteration**) goes like this:

```
repeat:
    1. make predictions with the current weight and bias
    2. calculate the loss
    3. work out which direction would lower the loss (the "gradient")
    4. move the weight and bias a small step in that direction
until the loss stops improving
```

If you plot it, iterations go on the x-axis and loss on the y-axis. A healthy curve drops steeply at first, then flattens out.

![Machine Learning Crash Course exercise: moving the weight and bias sliders to fit a line with the lowest loss](../../assets/articles/fig-26.png)
*Machine Learning Crash Course exercise: moving the weight and bias sliders to fit a line with the lowest loss. Source: Google, [Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course), CC BY 4.0.*

A model has **converged** when more training won't improve it. The curve is flat and stays flat.

## What does the learning rate do?

The **learning rate** (written α, "alpha") controls how big each step is.

- **Too small:** the steps are tiny. Loss stays high and trends downward, but only slowly. You wait a long time for little progress.
- **Too large:** the steps overshoot the lowest point, and the loss can bounce around or even grow instead of settling.
- **About right:** the model converges quickly and stably.

The learning rate is a **hyperparameter**: a setting you choose before training, rather than something the model learns.

### My experiment

In the course exercise, I set a learning rate of 0.03. The model converged after about 30 seconds, with an MSE of just under 3, a weight of –2.08 and a bias of 23.098. Quick, stable convergence like this is the sign of a good learning rate.

## What is batch size?

A model rarely looks at all the data before each update. Instead, it works in **batches**:

![Full batch, a single mini-batch, and one epoch made of ten mini-batches](../../assets/articles/fig-25.png)
*Full batch, a single mini-batch, and one epoch made of ten mini-batches. Source: Google, [Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course), CC BY 4.0.*

- The model picks a batch of examples at random, averages their gradients, and then updates the weight and bias once per iteration.
- **Batch size** is the hyperparameter for how many examples it processes before each update.

### Stochastic gradient descent (SGD)

"Stochastic" means randomly selected. **Stochastic gradient descent** in its strictest form uses a batch size of one: a single example per iteration. Given enough iterations it works, but it is very noisy.

**Noise** here means variation during training that makes the loss go up instead of down in some iterations. One example can be unrepresentative, so the step it suggests may point the wrong way.

Noise is not purely bad. A bit of randomness can help a model avoid settling too early and can help it generalise to new data. A common compromise is **mini-batch** gradient descent: batches bigger than one but much smaller than the full dataset.

| Approach | Examples per update | Trade-off |
|---|---|---|
| Full batch | All of them | Stable but slow and memory-hungry |
| Mini-batch | e.g. 10 to 1,000 | Usual middle ground |
| SGD (batch of 1) | One | Fast steps, very noisy |

## Beware the false sense of convergence

In deep learning, loss sometimes stays flat, or nearly flat, for many iterations before it finally drops again. During a long plateau it is easy to believe the model has converged and stop training too early.

The lesson: a flat curve over a short window is not proof that the model has finished learning. Look at a longer stretch before you call it done.

## What this means when you write a skill

The same loop applies when you improve a Claude skill. You need a "loss": a clear way to say how wrong an output is, such as a short checklist you score each test output against. Then you change one thing at a time (your step) and check again. Big rewrites are like a learning rate that's too high: you overshoot and can't tell what helped. And if two rounds of edits show no improvement, try a few more varied test cases before deciding the skill is "done".

## Key takeaways

- **Loss** measures how wrong a model is. MSE punishes big errors heavily, so it is pulled towards outliers; MAE is less affected by them.
- **Gradient descent** lowers loss step by step, and a model **converges** when more training no longer helps.
- The **learning rate** sets the step size: too small is slow, too large is unstable.
- **Batch size** sets how many examples feed each update; SGD (batch of one) is noisy, and some noise can help.
- A long flat stretch of loss can be a **false sense of convergence**, not the end of learning.
