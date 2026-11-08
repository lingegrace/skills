---
title: "Inside the Transformer: Encoder, Decoder and Attention Explained Step by Step"
summary: "You will be able to follow one sentence, 我有一只猫 → \"I have a cat\", through a Transformer's encoder and decoder, see how attention and the loss work, and know the three main Transformer variants."
time: "9 min read"
order: 3
column: llm-notebook
series: "How LLMs work"
status: published
---

"Transformer" is the T in GPT, and almost every major language model today is built on it. Its diagrams look intimidating, but it is easier to follow one sentence all the way through. We will train a translation model on a single example: 我有一只猫 → "I have a cat".

## What are the building blocks?

The original Transformer has two halves, each a stack of *N* identical layers:

- **Encoder layers** read the input sentence. Each contains multi-head self-attention, a feed-forward network, and "add & norm" steps.
- **Decoder layers** write the output sentence. Each contains masked self-attention, cross-attention, a feed-forward network, and add & norm steps.

Each layer in the stack learns features at a different level of complexity.

To keep track, I will label the key matrices **A** to **E**. A **matrix** here is simply a table of numbers: one row per token, one column per dimension of its vector.

> 🖼 Diagram to add: the full encoder-decoder diagram with matrices A–E marked at the points where they appear.

## Step 1: How does the input become numbers?

The Chinese sentence 我有一只猫 is split into tokens and each token becomes an embedding vector (a list of numbers that captures its meaning; see the previous article).

But the Transformer reads all tokens at once, so on its own it has no idea which came first. **Positional encoding** fixes this by adding a position signal to each vector. The result is **Matrix A**: one row per token, each carrying both meaning and position.

## Step 2: What does the encoder do?

**Multi-head self-attention.** For each token, the encoder looks at every other word in the sentence and decides how relevant each one is. When it processes 猫 (cat), it can pay attention to 一只 (a, with the classifier for animals) and 有 (have).

Each token gets three learned projections: a **Query** ("what am I looking for?"), a **Key** ("what do I contain?") and a **Value** ("what do I pass on?"). Each Query is compared with every Key, and the scores decide how much of each Value to blend in.

"Multi-head" means this runs several times in parallel, with different learned projections. Different heads can pick up different kinds of relationship, for example grammatical or semantic ones.

**Feed-forward network (a "feature enhancer").** A small neural network applied to each position independently:

```
input → linear layer 1 (expand dimensions) → ReLU activation → linear layer 2 (shrink back) → output
```

Attention gathers information from across the sentence; the feed-forward network then processes it more deeply, token by token.

**Add & norm.** Two stabilisers wrap each sub-step:

- **Add (residual connection):** add the layer's input to its output, so the network never loses the lower-level information while learning new features.
- **Norm (layer normalisation):** rescale each token's vector to have mean 0 and variance 1, which keeps training stable.

After *N* encoder layers, we get **Matrix B = Encoder(Matrix A)**: a context-rich representation of the whole Chinese sentence. Think of it as the knowledge base for the source sentence. The decoder will turn it into **Keys and Values** (through learned projections) and query it in the cross-attention layer, not in the first, masked layer.

## Step 3: What goes into the decoder during training?

At the same time, the decoder gets the correct English answer, shifted one place to the right with a start token:

```
<Begin>, I, have, a, cat
```

These five tokens become embeddings plus positional encoding: **Matrix C**. (The extra token is `<Begin>`.) Feeding in the correct answer during training is called **teacher forcing**.

## Step 4: Why is the decoder's self-attention "masked"?

To stop cheating. When the decoder predicts the token at position *i*, it may only see tokens 1 to *i*, never the ones after.

When it is working out what comes after "I", it can see `<Begin>` and `I`, but not `have`, `a` or `cat`. It must answer the question "what follows I?" without peeking.

The masked self-attention keeps what has been generated so far coherent and produces **Matrix D**, which supplies the **Queries** for the next layer.

## Step 5: How does cross-attention connect the two languages?

This is where English meets Chinese:

| Role | Comes from |
|---|---|
| **Query** | Matrix D (decoder: "what English word do I need next?") |
| **Key** | Matrix B (encoder output) |
| **Value** | Matrix B (encoder output) |

The decoder's Queries search the encoded Chinese sentence for relevant information. The output is **Matrix E**.

## Step 6: How does the model produce probabilities?

```
Matrix E → feed-forward → linear layer → logits → softmax → probability matrix P
```

The **linear layer** gives each position a raw score (a **logit**) for every vocabulary word, and **softmax** turns those into probabilities that add up to 1. For example, at the position after "I":

```
[..., "have": 0.60, "am": 0.20, "love": 0.15, ...]   ← should predict "have"
```

## Step 7: How is the loss calculated?

Training compares P with the true answers, Y, using **cross-entropy loss**: for each position, take the probability the model gave to the correct word, and compute −log of it. Here are three of the target words:

| Target word | Vocabulary index | Probability given | Loss = −log(p) |
|---|---|---|---|
| "I" | 24 | 0.65 | ≈ 0.43 |
| "have" | 137 | 0.60 | ≈ 0.51 |
| "cat" | 589 | 0.70 | ≈ 0.36 |

```
Average loss = (0.43 + 0.51 + 0.36) / 3 ≈ 0.43
```

If the model is confident and right (say it gives "I" 0.95), the loss is −log(0.95) ≈ 0.05: tiny. A low probability for the right word means a large loss.

Then comes **backpropagation**: the error is sent backwards through the network, and **gradient descent** adjusts every trainable parameter a little to reduce the loss. Repeat this across millions of examples until extra training no longer helps; the model has then **converged**.

## What are the three Transformer variants?

| Variant | Example | Typical uses |
|---|---|---|
| **Encoder-only** | BERT | Classifying sentences (e.g. a spam classifier), filling in masked words |
| **Decoder-only** | GPT | Generating text, predicting the next token (a "causal" language model) |
| **Encoder-decoder** | The original 2017 Transformer | Sequence-to-sequence tasks such as translation |

GPT keeps only the decoder half, without cross-attention: masked self-attention, feed-forward and add & norm, stacked many times. There is no separate source sentence; your prompt is simply the beginning of the text it continues.

## What this means when you write a skill

- **A chat model only sees backwards.** A decoder-only model like Claude reads your skill and the conversation as one sequence and predicts what follows. It cannot "look ahead" to a rule you put later in the output. So put the instructions that should shape the answer *before* the point where the answer starts.
- **Attention is relevance-weighted, not perfectly even.** The model decides how much each part of the context matters. Clear headings, short steps and consistent terms make it easier for the right instruction to receive attention when it counts.

## Key takeaways

- A Transformer turns tokens into vectors plus position (Matrix A), and the encoder builds a context-rich representation (Matrix B).
- The decoder uses masked self-attention so it cannot peek ahead (Matrix D), then cross-attention to query the source using Keys and Values derived from Matrix B (Matrix E).
- A linear layer and softmax turn this into a probability for every vocabulary word; cross-entropy loss (−log of the correct word's probability) measures the error.
- Backpropagation and gradient descent adjust the parameters to reduce the loss.
- Encoder-only (BERT) suits classification, decoder-only (GPT) suits generation, encoder-decoder suits translation.
