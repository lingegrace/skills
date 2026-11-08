---
title: "Overfitting, Generalization and Regularization, Explained"
summary: "You will understand why models need separate training, validation and test data, what overfitting is, and how regularization and early stopping keep a model useful on new data."
time: "7 min read"
order: 12
column: llm-notebook
series: "ML Crash Course notes"
status: published
---

A model that scores perfectly on the data it trained on can still fail the moment it meets the real world. That gap between "works in the lab" and "works out there" is one of the most important ideas in machine learning.

This last part of my Machine Learning Crash Course notes covers how to test a model honestly, what overfitting is, and how regularization keeps a model from memorizing instead of learning.

## Why split data into training, validation and test sets?

You can't judge a model on the same examples it learned from. That would be like marking students on the exact questions they practised. So the data is divided:

| Set | Used for |
|---|---|
| **Training set** | The model learns its weights from this |
| **Validation set** | You check progress and tune settings (like learning rate) during development |
| **Test set** | A final, untouched check at the end |

Dividing examples between these sets is a zero-sum game. Every example you put in the test set is one the model can't learn from, and vice versa. That is the central trade-off.

### What makes a good test (or validation) set?

It should meet all of these:

- **Large enough** to give statistically significant results.
- **Representative of the dataset as a whole.** Don't pick a test set with different characteristics from the training set.
- **Representative of the real-world data** the model will meet in actual use.
- **Zero duplicates** of examples in the training set. Otherwise the model is just recalling answers it has already seen.

## What is overfitting?

**Overfitting** means building a model that matches (memorizes) the training set so closely that it fails to make correct predictions on new data. It is like an invention that performs well in the lab but is worthless in the real world.

**Generalization** is the opposite: a model that makes good predictions on new data it hasn't seen.

> 🖼 Diagram to add: training loss and validation loss over iterations; training loss keeps falling while validation loss starts rising, marking where overfitting begins.

### When can a model generalize?

Generalization rests on three conditions:

1. **Examples are independently and identically distributed.** They are drawn the same way and don't influence each other.
2. **The dataset is stationary.** It doesn't change significantly over time.
3. **The partitions share the same distribution.** Training, validation, test and real-world examples are statistically similar.

Social scientists will recognize these as sampling assumptions, and will know how often the social world breaks them. Language shifts, behaviour changes, and the people in your data may not be the people the model is later used on. A model trained on one population and deployed on another breaks condition 3.

## How does regularization fight overfitting?

Instead of only minimizing loss, a regularized model minimizes:

```
loss + complexity
```

The idea: a simpler model that fits slightly worse often generalizes better than a complex one that fits the training data perfectly.

### L2 regularization

One way to measure complexity is **L2 regularization**: complexity is the sum of the squares of the model's weights. Big weights are penalized heavily, so the model is pushed to keep weights small unless a feature really earns its influence.

### The regularization rate (lambda)

Model developers control how much complexity matters by multiplying it by a number called the **regularization rate**, written λ (lambda):

```
minimize:  loss + λ × complexity
```

- **High λ:** strong push towards simple models. Too high, and the model is oversimplified (this is one cause of prediction bias).
- **Low λ:** weak push. Too low, and overfitting returns.

### Early stopping

**Early stopping** is a regularization method that doesn't calculate complexity at all. You simply end training after a limited number of steps, while loss is still falling, before the model has fully converged. The model stops before it has had time to memorize the training data.

The trade-off is that the model never fully converges on the training data, which is the point.

## How do learning rate and regularization rate interact?

These two settings tend to pull weights in opposite directions:

- A **high learning rate** often pulls weights away from zero.
- A **high regularization rate** pulls weights towards zero.

Tuning a model means finding the balance point between the two, where the model learns enough from the data without memorizing it.

## What this means when you write a skill

A skill can overfit too. If you only test it on the three examples you used while writing it, you are grading it on its training set. Keep a separate set of test prompts you never look at while editing, and include messy, real-world requests unlike your examples. If the skill passes your favourites but fails the new ones, it has memorized your examples rather than learned the task. Long lists of very specific rules are the skill equivalent of high complexity; a few clear principles often generalize better.

## Key takeaways

- Use separate **training, validation and test sets**; a good test set is large, representative and has no duplicates of training data.
- **Overfitting** is memorizing the training data; **generalization** is doing well on new data.
- Generalization assumes independent, identically distributed, stationary data with matching partitions.
- **Regularization** minimizes loss plus complexity; **L2** penalizes large weights, scaled by the **regularization rate λ**; **early stopping** halts training before full convergence.
- Learning rate and regularization rate pull in opposite directions, so tune them together.
