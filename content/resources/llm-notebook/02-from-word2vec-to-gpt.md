---
title: "From word2vec to GPT: A Short History of Language Models, Deep Learning and the Transformer"
summary: "You will understand the key steps from word2vec to GPT-4, what deep learning and neural networks are, and why the Transformer replaced the RNN."
time: "7 min read"
order: 2
column: llm-notebook
series: "How LLMs work"
status: published
---

ChatGPT seemed to arrive out of nowhere in late 2022, but it sits at the end of about a decade of steady ideas. Knowing that short history helps you separate what is genuinely new from what is marketing. It also explains one word you will see everywhere: Transformer.

## What are the key milestones?

| Year | Milestone | Why it mattered |
|---|---|---|
| 2013 | **word2vec** | Turned words into lists of numbers that capture meaning. |
| ~2014 | **RNNs** for language (recurrent neural networks) | Read text one word at a time, carrying a memory forward. RNNs are older, but around this time they became the standard tool for tasks like translation. |
| 2015 | **Attention mechanism** | Let a model look back at the most relevant words instead of relying only on a compressed memory. |
| 2017 | **Transformer** | Built a whole architecture around attention, and processed words in parallel. |
| 2018 | **BERT and GPT** | The first widely known large *pre-trained* Transformer models. |
| 2023 | **GPT-4** | A much larger, more capable model in the same family. |

## What did word2vec do?

Computers cannot do maths with the word "cat". word2vec (2013) solved this by turning each word into a **vector**: a list of decimal numbers, such as `[0.21, -0.73, 0.05, …]`. These are often called **embeddings**.

The clever part is how the numbers are learned. Words used in similar contexts end up with similar vectors, so they sit close together in a high-dimensional space. "Cat" lands near "dog"; "Paris" lands near "London". Distance between vectors becomes a measure of how related two words are.

That made embeddings useful for word similarity, text classification (for example, a spam classifier) and translation. Every modern LLM still starts by turning tokens into vectors like these.

## What is deep learning, and what is a neural network?

**Machine learning (ML)** is a way of building programs that learn patterns from data rather than following hand-written rules. **Deep learning** is a type of machine learning that uses **neural networks with many processing layers**. Each layer learns a more abstract representation of the data than the one before.

Why are all these models called neural networks? Because they share three traits:

1. **They are built from the same basic blocks.** Linear transformations (multiplying by a matrix of weights), **activation functions** (simple non-linear functions that let the network model curves rather than only straight lines), and a layered structure.
2. **They are trained end to end.** The whole model is one differentiable calculation. Data flows forward to produce a prediction, the error flows backward, and **gradient descent** nudges every parameter to reduce the error.
3. **They learn their own features.** Instead of a human deciding which features matter, the feature extractor is itself part of the network and is learned from data.

A handy summary from my notes:

> Deep learning = neural networks + architecture + training method + large-scale data

## What is the difference between a shallow and a deep network?

Here is a **shallow** neural network for sentiment classification:

```
Input:   hand-crafted features (e.g. 1,000 numbers)
         = [bag-of-words vector, TF-IDF scores, sentence length, count of emotion words, ...]
Hidden:  1 layer, 50 neurons
Output:  [positive, negative, neutral]
```

Notice that a person chose the input features: word counts, sentence length and so on. The network only learns how to combine them.

A **deep** network would take the raw text (as embeddings) and pass it through many layers. Early layers might pick up word-level patterns, later ones phrases, and later still the tone of a whole sentence. Nobody hand-designs those features; the layers learn them.

## How is an RNN different from a Transformer?

| | RNN | Transformer |
|---|---|---|
| **Processing** | Sequential: one token after another | Parallel: all tokens at once |
| **Core mechanism** | A recurrent hidden state passed from step to step | Self-attention: every token looks at every other token |
| **Examples** | LSTM, GRU | BERT, GPT |

An RNN keeps a running memory called the **hidden state**. When it reads the token at position *t*, it takes two inputs: the current token's embedding, and the hidden state from the previous step, *t−1*.

```
input  = [x_t, h_{t-1}]          # current token + previous memory
h_t    = tanh(W · input + b)     # update the memory
output = softmax(V · h_t + c)    # probabilities for the next token
```

This works, but it has two problems. It is slow, because step *t* cannot start until step *t−1* is done. And information from early in a long sentence tends to fade as it is passed along.

Real products were built this way. Microsoft's chatbot XiaoIce (小冰), for example, combined a GRU-based RNN generator, trained on paired human conversations, with a retrieval-based generator that picked suitable replies from a large database of conversations.

The Transformer's **self-attention** removes the step-by-step chain. Every token can directly "look at" every other token in the sentence and decide how much each one matters. Because nothing waits for a previous step, the whole sentence can be processed in parallel on modern chips. That is what made it practical to train models on vastly more data, which led to BERT, GPT and everything since.

## What this means when you write a skill

- **Meaning is closeness, not keywords.** Because models represent words as vectors, "summarise", "sum up" and "give me the gist" land near each other. In a skill description, describe the *situations* where it should be used in natural language, rather than relying on one exact trigger word.
- **Everything in context can matter at once.** Self-attention lets the model relate any part of the prompt to any other. A rule buried in the middle of a long skill file can still affect the output, and so can a contradictory example. Keep instructions consistent from top to bottom.

## Key takeaways

- Modern LLMs grew out of a decade of ideas: word2vec (2013), RNNs, attention (2015), the Transformer (2017), BERT and GPT (2018), GPT-4 (2023).
- word2vec turned words into vectors, so similar meanings sit close together.
- Deep learning means neural networks with many layers that learn their own features from data, trained with gradient descent.
- RNNs read text one step at a time with a hidden state; Transformers use self-attention to read all tokens in parallel, which is why they scaled.
