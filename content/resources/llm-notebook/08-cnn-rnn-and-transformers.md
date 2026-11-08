---
title: "CNN vs RNN vs Transformer: how neural networks read text"
summary: "You'll understand, step by step, how a convolutional network classifies a sentence, why it only sees local patterns while a Transformer sees the whole text, and how an RNN-based chatbot like Microsoft's XiaoIce generated replies."
time: "7 min read"
order: 8
column: llm-notebook
series: "Beyond the basics"
status: published
---

Transformers power today's chatbots, but they weren't the first neural networks to read text. Looking at the older designs, convolutional and recurrent networks, makes it much clearer what the Transformer changed. It also explains a famous pre-ChatGPT chatbot, Microsoft's XiaoIce (小冰), which millions of people talked to.

## What is a neural network, in one paragraph?

A **neural network** is layers of connected nodes ("neurons"). Data goes in one end, passes through the layers, and an output comes out the other. During training, the network adjusts its **weights** (the strengths of the connections) to make its **loss**, the measure of how wrong it is, as small as possible. The main families are feedforward networks, **convolutional neural networks (CNNs)**, **recurrent neural networks (RNNs)** and **Transformers**.

## How does a CNN read a sentence?

CNNs were made famous by image processing, where they scan a picture for edges and shapes. The same idea works for text: slide a small window along the sentence and look for meaningful phrases. In short: **convolution, non-linearity, pooling, linear layer, softmax.**

Let's follow one sentence, "I like the cat on a mat", through a sentiment classifier that decides positive or negative.

**Step 1: Tokenise.** Split the text into tokens, padded at both ends:

```
["<pad>", "I", "like", "the", "cat", "on", "a", "mat", "<eos>", "<pad>"]
```

**Step 2: Embed.** Each token becomes a vector, a list of numbers. Say "I" = [0.1, 0.2, …, 0.3] and "like" = [0.4, 0.5, …, 0.6]. Ten tokens with 300 numbers each give a matrix of shape (10, 300). Embeddings capture relationships: "cat" ends up close to "dog" but far from "mat".

**Step 3: Slide filters.** A **filter** is a small grid of learnable weights that covers a few words at once, for example 3 words × 300 numbers for three-word phrases (*trigrams*). It slides along the sentence one step at a time, computing a score at each position. A strong score means "this pattern is here". A real model uses many filters (say 100) of different widths (2, 3 or 4 words) to catch different phrases, such as "like the cat" as a positive one.

Crucially, the filter uses the **same weights at every position**. If it learns to detect "like the" in one place, it detects it anywhere, like using the same ruler to measure different parts of a line.

**Step 4: ReLU.** The scores pass through **ReLU**, which turns negatives into zero: ReLU(x) = max(0, x). A row of scores like

```
[-0.1, 0.8, -0.2, 1.5, 0.3]  →  [0, 0.8, 0, 1.5, 0.3]
```

Weak matches (on "on a", say, which says little about sentiment) are switched off, while strong ones like "the cat" stay. This *non-linearity* lets the network learn more complex patterns.

**Step 5: Max-pool.** Each filter's row of scores is shrunk to one number, its maximum: here, 1.5. We don't care *where* the cat is, only that a strong match exists somewhere. This gives a fixed-size result whatever the sentence length.

**Step 6: Concatenate.** The pooled values from all filters are joined into one vector, *h*, a fixed-size summary of the whole text. A linear (dense) layer then converts *h* into one score per class.

**Step 7: Softmax.** **Softmax** turns scores into probabilities that add up to 1. With scores [3.2, −1.5] for [positive, negative]:

```
P(positive) = e^3.2 / (e^3.2 + e^-1.5) ≈ 24.5 / 24.8 ≈ 0.99
P(negative) ≈ 0.01
```

Prediction: positive sentiment.

> 🖼 Diagram to add: the seven CNN steps for "I like the cat on a mat", showing a 3-word filter sliding over the embedding matrix, the ReLU and max-pool, and the final softmax bar.

## Local CNN vs global Transformer: what's the difference?

A CNN is **local**. Each filter only sees a small, fixed window: "like the" (two words) or "the cat on" (three words). It never considers the whole sentence at once. Stacking layers widens the view a little, but long-range links stay hard.

A Transformer is **global**. Its self-attention mechanism lets every word look at every other word in the input, so "it" at the end of a paragraph can be linked to the noun it refers to at the start. That wider coverage is a large part of why Transformers took over language tasks.

| | CNN | Transformer |
|---|---|---|
| What each unit sees | A small window of neighbouring words | The whole input |
| Good at | Short phrases, fast classification | Long-range meaning, generation |
| Word order | Mostly lost after pooling | Kept via position information |

## What does an RNN do differently?

An **RNN** reads text one word at a time, in order, carrying a running summary called the **hidden state**. At each step it combines the new word with the hidden state from the previous step:

```
h_t = tanh(W · x_t + U · h_(t-1) + b)
output_t = softmax(V · h_t + c)
```

Here *x_t* is the current word and *h_(t-1)* is the memory of everything before it. That makes RNNs natural for sequences, but the memory fades over long texts. Improved versions, the **LSTM** and the **GRU** (*gated recurrent unit*), add "gates" that decide what to keep and what to forget.

## How did XiaoIce generate its replies?

Microsoft's **XiaoIce** (小冰) was a social chatbot designed for companionship and long, emotionally engaged conversations rather than just answering questions. Its reply system drew candidates from three sources:

1. **A GRU-based RNN neural generator**, trained on a paired database (message-and-reply pairs) to learn to simulate human conversation and write new replies word by word.
2. **A retrieval-based generator using paired data**, which looks up existing human replies to similar messages.
3. **A retrieval-based generator using unpaired data**, which finds suitable sentences in text that wasn't originally part of a conversation.

The data came from human conversations on the internet and from people's conversations with XiaoIce itself, which, according to the notes, amounted to **more than 30 billion conversation pairs since May 2018**.

That second source matters. XiaoIce learned partly from its own users, so the people who talked to it most shaped how it spoke to everyone. For a social scientist, a companion chatbot raises questions that a sentiment classifier doesn't: who is it designed to keep talking, and what does it learn from them?

> 🖼 Diagram to add: XiaoIce's reply architecture, a user message feeding three candidate generators (GRU neural, retrieval on paired data, retrieval on unpaired data) and a response chosen from the candidates.

## What this means when you write a skill

- **Claude reads globally, so structure helps.** A Transformer can link any part of your `SKILL.md` to any other, but clear headings and numbered steps make the important links easy to find.
- **Mix generation and retrieval, as XiaoIce did.** Let Claude write freely where judgement is needed, and point it to fixed reference files (templates, approved wording) where consistency matters.
- **Be explicit about the end decision.** Like the final softmax picking a class, a skill works best when it says exactly what output to produce and in what format.

## Key takeaways

- A CNN classifies text by sliding shared filters over word embeddings, then applying ReLU, max-pooling, a linear layer and softmax.
- CNNs see local windows; Transformers use attention to see the whole input at once.
- RNNs read word by word, carrying a hidden state; GRUs and LSTMs help them remember longer.
- XiaoIce combined a GRU-based generator with two retrieval-based generators, trained partly on its own users' conversations.
