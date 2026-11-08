---
title: "Logistic Regression, Precision, Recall and AUC: A Plain-English Guide"
summary: "You will understand how a model turns a score into a yes/no decision, and how to judge that decision with a confusion matrix, precision, recall, ROC and AUC."
time: "8 min read"
order: 10
column: llm-notebook
series: "ML Crash Course notes"
status: published
---

Many AI systems don't just predict a number. They decide: spam or not spam, fraud or not fraud, flag this post or leave it. Every one of those decisions hides a choice about which mistakes we are willing to live with.

This part of my Machine Learning Crash Course notes covers how a model produces a probability, how that becomes a yes/no answer, and how to tell whether the answers are any good.

## How does logistic regression produce a probability?

**Logistic regression** is a model that outputs a probability: a value always between 0 and 1.

Take a spam classifier. If it reads an email and outputs 0.932, that means a 93.2% probability that the email is spam.

The trick is the **sigmoid function** ("sigmoid" means s-shaped). The model first calculates an ordinary linear equation, which can give any number from very negative to very positive. That number then goes into the sigmoid, which squashes it into the range 0 to 1.

```
z = bias + weight1 × feature1 + weight2 × feature2 + ...
probability = sigmoid(z) = 1 / (1 + e^(−z))
```

> 🖼 Diagram to add: the S-shaped sigmoid curve, with z on the x-axis and probability (0 to 1) on the y-axis.

### Odds and log-odds

**Odds** is the probability of success divided by the probability of failure: p / (1 − p). If an event has a 90% chance of success and a 10% chance of failure, the odds are 0.9 / 0.1 = 9, or "9 to 1".

**Log-odds** is simply the logarithm of the odds. (The base can be any number greater than 1; the natural log is usual.) The log-odds function is the inverse of the sigmoid. Put another way, the linear part of the model, z, is predicting the log-odds.

### Log loss

Logistic regression does not use squared loss. It uses **log loss**, which looks at the logarithm of the predicted probability for the true answer, not just the distance between prediction and data. The effect: a model that is confidently wrong (says 0.99 spam when the email is fine) is punished very heavily.

## How does a probability become a yes/no answer?

**Classification** is the task of predicting which class (category) an example belongs to. To turn a probability into a class, you pick a **classification threshold**.

Say the threshold is 0.75. Any email scoring above 0.75 is labelled "spam" (the **positive class**); everything else is "not spam" (the **negative class**). Our 0.932 email is spam.

The threshold is set by people, not learned by the model. Move it and you change who gets flagged.

## What is a confusion matrix?

Once the model makes yes/no calls, we compare them with the **ground truth** (the real answers). There are four possible outcomes:

| | Actually spam | Actually not spam |
|---|---|---|
| **Predicted spam** | True positive (TP) | False positive (FP): a false alarm |
| **Predicted not spam** | False negative (FN): a miss | True negative (TN) |

From these four counts come the main metrics.

## Accuracy, precision or recall?

| Metric | Formula | Question it answers |
|---|---|---|
| **Accuracy** | (TP + TN) / all | What share of all calls were right? |
| **Precision** | TP / (TP + FP) | When the model says "spam", how often is it right? |
| **Recall** (true positive rate) | TP / (TP + FN) | Of all real spam, how much did the model catch? |

Accuracy sounds like the obvious choice, but it misleads on **imbalanced data**. If only 1% of cases are positive, a model that always says "no" is 99% accurate and completely useless. When actual positives are rare, recall is the more meaningful metric, because it measures whether the model finds them.

Precision improves as false positives go down; recall improves as false negatives go down. The two often pull against each other: raise the threshold and precision usually rises while recall falls, and the reverse.

## What do ROC and AUC show?

The **ROC curve** (receiver operating characteristic) plots the true positive rate against the **false positive rate** (FPR, the share of real negatives wrongly flagged) at every possible threshold. **AUC** is the area under that curve.

- AUC of 0.5 means the model does no better than chance.
- AUC closer to 1.0 means better separation of the two classes.
- AUC is useful for comparing two models, as long as the dataset is roughly balanced. The model with the larger area is generally better.

> 🖼 Diagram to add: an ROC curve with three marked points A (low FPR, lower TPR), B (balanced) and C (highest TPR, higher FPR).

### Choosing a threshold: points A, B and C

Each point on the curve is a threshold. Which one you choose depends on what mistakes cost:

- **Point A** (low FPR, lower TPR): choose this when false alarms are very costly, even though you will miss some real positives.
- **Point C** (highest TPR): choose this when false alarms are cheap but misses are very costly.
- **Point B**: when the two costs are roughly equal, it offers a balance.

This is where a sociologist's eye helps. "Costly" for whom? A false positive in fraud detection might freeze an innocent person's account; a false negative might cost a bank money. Choosing the threshold is choosing who bears the error.

## What causes prediction bias?

**Prediction bias** means the average of the model's predictions differs from the average of the real labels. If 5% of emails are spam but the model predicts 15% on average, something is off. Common causes:

- Biases or noise in the data, including biased sampling for the training set
- Too-strong regularization, so the model is oversimplified and loses necessary complexity
- Bugs in the training pipeline
- Features that are not sufficient for the task

## What this means when you write a skill

When you test a skill, decide which mistake matters more. For a skill that flags risky contract clauses, a miss (false negative) is worse than an extra flag, so aim for recall. For a skill that auto-sends emails, a wrong send (false positive) is worse, so aim for precision. Write that priority into the skill's instructions and into your test checklist.

## Key takeaways

- Logistic regression passes a linear equation through a **sigmoid** to get a probability between 0 and 1; it is trained with **log loss**.
- A human-chosen **threshold** turns that probability into a class.
- **Accuracy** misleads on imbalanced data; **precision** and **recall** tell you which kind of mistake the model makes.
- **ROC/AUC** compare models across all thresholds; picking point A, B or C depends on the cost of each error.
- **Prediction bias** often points back to the data, the features, the pipeline or over-regularization.
