---
title: "How Does an LLM Predict the Next Word? Probability, Temperature and Sampling Explained"
summary: "You will understand that a large language model writes by repeatedly predicting the next token from a probability distribution, and how temperature, top-k and top-p change which token it picks."
time: "6 min read"
order: 1
column: llm-notebook
series: "How LLMs work"
status: published
---

When ChatGPT or Claude answers you, it can feel like talking to someone who understands. Underneath, the machine is doing something much simpler, over and over: guessing the next small piece of text. Once you see that, a lot of LLM behaviour makes sense, from why the same question gets different answers to why some settings make a model "more creative".

## What is a large language model, at its core?

A large language model (LLM) is, at heart, a **probability model**. In more technical terms, it estimates the probability of a sequence of **tokens**.

A **token** is the unit of text the model works with. It might be a whole word, part of a word, a single Chinese character or a punctuation mark. For simplicity, this article treats tokens as "words" or "characters".

So the model's job is not to "know the answer". Its job is to answer one question very well: *given everything written so far, how likely is each possible next token?*

## What happens when you type 「今天天气」?

Say you type 「今天天气」 ("today's weather"). The model calculates a probability for every token in its vocabulary as the next one. With made-up numbers for illustration:

| Next character | Probability |
|---|---|
| 真 (really) | 30% |
| 不 (not) | 20% |
| 很 (very) | 15% |
| … thousands of others | the remaining 35% |

This list is called a **probability distribution**: every option gets a share, and the shares add up to 100%.

The model then picks one character, adds it to the end of the input, and predicts again. Written as a loop:

```
text = "今天天气"
repeat:
    probabilities = model(text)        # a score for every possible next token
    next_token = choose(probabilities) # pick one
    text = text + next_token           # append it
until the answer is finished
```

That is the whole generation process. A long, fluent answer is just this loop running hundreds of times. This style of model is called **autoregressive**: each new token depends on the ones it has already produced.

## Why does guessing the next word look like understanding?

The key is **scale**. When a model has tens or hundreds of billions of **parameters** (the adjustable numbers inside it that are tuned during training), and it has been trained on an enormous amount of text, this "probability prediction" becomes remarkably accurate. Accurate enough that it feels as if the model really understands what you are saying.

Take 「中国的首都是」 ("the capital of China is"). A model that has seen this pattern countless times will give 「北」 (the first character of 北京, Beijing) a very high probability. It has not looked anything up. The answer is simply the most likely continuation of everything it was trained on.

Whether this counts as "understanding" is still debated. As a sociologist, I find it useful to remember what the model is actually reflecting: the patterns in the text it was trained on. Whose writing made it into that data, and whose did not, shapes what counts as "likely".

## What does temperature do?

Once the model has its probability distribution, it still has to choose. **Temperature** is a setting that controls how adventurous that choice is.

- **Temperature 0 (the lowest):** the model always picks the most probable token. The output is the most predictable. This suits work that needs precision, such as programming.
- **Higher temperature:** the model is more willing to pick lower-probability tokens. The output is more varied and can feel more creative, but it is also less controllable. This is often used for creative tasks.

Technically, temperature reshapes the distribution before sampling. A low temperature sharpens it, so the top choice dominates. A high temperature flattens it, so unlikely tokens get a bigger share.

One caution: "higher temperature = more creativity" is a convenient shorthand, not a law. Research on story generation suggests temperature is only weakly linked to how novel the output is, and more clearly linked to the output becoming incoherent. Turning it up mostly adds randomness, not originality.

## What are top-k and top-p sampling?

**Sampling** means picking the next token at random, but in proportion to its probability. Two common methods limit which tokens are even allowed into the draw:

| Method | How it works | Example |
|---|---|---|
| **Top-k sampling** | Keep only the *k* most likely tokens, then sample among them. | With k = 3 after 「今天天气」, only 真, 不 and 很 are allowed. |
| **Top-p sampling** (also called nucleus sampling) | Keep adding tokens, from most to least likely, until their combined probability reaches *p*. Sample among those. | With p = 0.65: 真 (30%) + 不 (20%) + 很 (15%) = 65%, so those three are kept. |

Top-p adapts to the situation. When the model is confident, a handful of tokens already reaches *p*, so the pool is small. When it is unsure, the pool grows. In practice, temperature and top-p or top-k are often used together.

## What this means when you write a skill

- **The model continues text; it does not obey a hidden rulebook.** Everything you put in a skill (the description, the steps, the examples) becomes part of the "text so far" that the next prediction is based on. Clear, specific wording makes the right continuation more likely.
- **Expect variation.** Because output is sampled, the same skill can produce slightly different results on different runs. That is why you should test a skill several times, not once.
- **Put certainty where you need it in structure, not in hope.** If a step must be exact (a file name, a JSON format, a fixed sequence), spell it out precisely, give an example, or have a script do it. Don't rely on the model happening to pick the right token every time.

## Key takeaways

- An LLM is a probability model: it predicts how likely each possible next token is, given the text so far.
- Generation is a loop: predict, pick one token, append it, predict again.
- Scale (many parameters and huge amounts of training text) is what makes these predictions accurate enough to feel like understanding.
- Temperature controls how adventurous the choice is; 0 is the most predictable, higher values add variety and risk.
- Top-k and top-p limit the pool of candidate tokens before the model samples from it.
