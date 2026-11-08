---
title: "Features, Labels and Data Quality in Machine Learning"
summary: "You will understand how raw data is turned into features, what makes a good label, how inter-rater agreement fits in, and how to handle imbalanced classes."
time: "8 min read"
order: 11
column: llm-notebook
series: "ML Crash Course notes"
status: published
---

A model can only learn from what it is shown, in the form it is shown. Most of the real work in machine learning is not picking an algorithm. It is deciding how to represent the world as numbers, and deciding what counts as the right answer.

That second part should feel familiar to anyone trained in the social sciences. This part of my Machine Learning Crash Course notes is about data: features, labels, quality and balance.

## What is feature engineering?

A **feature** is an input the model uses, such as an email's length or the number of links in it. The **feature vector** is the full list of features for one example.

**Feature engineering** means finding the best way to represent raw dataset values as trainable values in the feature vector. Feature vectors seldom use raw values directly. You usually transform them into something the model can learn from more easily.

Three common techniques follow.

## Why normalize features?

**Normalization** puts features on a similar scale. Imagine one feature is age (0 to 100) and another is income (0 to 1,000,000). Without scaling, the bigger numbers dominate.

![Normalization techniques and when to use each](../../assets/articles/fig-36.png)
*Normalization techniques and when to use each. Source: Google, [Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course), CC BY 4.0.*

Normalization:

- Helps models **converge faster** during training.
- Helps models **make better predictions**. When features have very different ranges, predictions can be less useful.
- Helps avoid the **"NaN trap"**: when values get very large, calculations can exceed what the computer can represent and turn into NaN ("not a number"), which then spreads through the model.
- Helps the model **learn appropriate weights** for each feature, instead of over-weighting features just because their numbers are big.

## What is binning?

**Binning** (also called **bucketing**) groups a numerical range into sub-ranges. Instead of using exact age, you might use buckets: 18–24, 25–34, 35–44 and so on.

This helps when the relationship is not a straight line. Being 30 versus 31 may not matter, but being in a different life stage might. Social scientists do this all the time with age bands and income brackets.

## What are synthetic features and feature crosses?

A simple linear model can only draw straight-line relationships. To capture curves and interactions, you can create new features from existing ones.

- **Synthetic features** are built from other features (for example, multiplying two features together, or squaring one). Fed into a linear model, they let it represent non-linear relationships.
- **Feature crosses** are a kind of synthetic feature made by crossing (taking the Cartesian product of) two or more categorical or bucketed features. Like polynomial transforms, they let linear models handle non-linearity, and they encode **interactions** between features.

Example: cross "country" with "time of day". A purchase at 3 a.m. may mean something different in one country than another. The cross lets the model learn each combination separately.

![A synthetic feature (y = x²) lets a linear model separate classes that a straight line cannot](../../assets/articles/fig-38.png)
*A synthetic feature (y = x²) lets a linear model separate classes that a straight line cannot. Source: Google, [Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course), CC BY 4.0.*

## What makes a good label?

The **label** is the answer the model learns to predict.

- A **direct label** is identical to the prediction you want. If you want to predict whether someone will subscribe, "did they subscribe?" is direct.
- A **proxy label** stands in for what you can't measure directly. If you want to predict whether a reader *enjoyed* an article, you might use "did they share it?". Proxy labels are always a compromise: an imperfect approximation of the direct label.

Social scientists know this as the gap between a concept and its operationalization. A proxy builds your assumptions into the model.

### Human labels vs machine labels

- **Human labels** (from human raters) are often called **golden** labels: the best available standard.
- **Machine labels** (produced by another model) are often called **silver** labels: cheaper and faster, but less trustworthy.

### When humans disagree: inter-rater agreement

Even golden labels are not perfect, because people disagree. ML borrows the same tools that social scientists use to check coding reliability:

| Metric | Typically used for |
|---|---|
| **Cohen's kappa** (and variants) | Agreement between two raters on categories, correcting for chance |
| **Intra-class correlation (ICC)** | Agreement on continuous ratings or scores |
| **Krippendorff's alpha** | Flexible: many raters, different data types, missing ratings |

If you have ever coded interview transcripts with a colleague and calculated kappa, you already know how ML teams check their labels.

## What undermines data quality?

Common problems to look for:

![Common problems that undermine data quality, with examples](../../assets/articles/fig-37.png)
*Common problems that undermine data quality, with examples. Source: Google, [Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course), CC BY 4.0.*

- **Omitted values**: missing entries.
- **Duplicate examples**: the same case appearing more than once.
- **Bad feature values**: typos, wrong units, impossible numbers.
- **Bad labels**: wrong answers in the training data.
- **Bad sections of data**: a whole chunk that is corrupt or unrepresentative.

## What do you do with imbalanced classes?

In a **class-imbalanced** dataset, one class is much more common than the other: the **majority class** and the **minority class**. Think of fraud: almost all transactions are legitimate.

If the minority class is rare, many training batches contain almost no examples of it, and the model never learns it properly. A two-step fix:

```
1. Downsample: train on fewer majority-class examples
   → each batch now contains enough minority examples
2. Upweight: give each remaining majority example more weight,
   by the same factor you downsampled
   → corrects the bias you just introduced
```

Why step 2? Downsampling shows the model an artificial world where the classes are more balanced than in reality, which creates prediction bias. Upweighting by the same factor (downsample by 10, upweight by 10) restores the real-world proportions in the loss.

## What this means when you write a skill

When you test a skill, your expected outputs are your labels. Write them down before you test, and if possible ask a colleague to judge a few outputs independently. If the two of you disagree often, the problem may be your criteria, not the skill. And make sure your test cases include the rare, awkward inputs, not only the common easy ones.

## Key takeaways

- **Feature engineering** turns raw data into inputs a model can learn from: normalization, binning and feature crosses are core tools.
- **Direct labels** match what you want to predict; **proxy labels** are always a compromise.
- Human (**golden**) labels beat machine (**silver**) labels, but humans disagree too, so measure **inter-rater agreement** (Cohen's kappa, ICC, Krippendorff's alpha).
- Watch for missing values, duplicates, bad values, bad labels and bad sections of data.
- For **class imbalance**, downsample the majority class, then upweight it by the same factor.
