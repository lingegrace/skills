---
title: "How Is GPT Trained? Pretraining, Fine-Tuning, RLHF and Inference Explained"
summary: "You will understand the stages that turn a raw text predictor into a helpful assistant (pretraining, supervised fine-tuning, LoRA, RLHF and DPO) and what happens at inference when you send a prompt."
time: "8 min read"
order: 4
column: llm-notebook
series: "How LLMs work"
status: published
---

A model that has only learned to predict the next word is not yet an assistant. Ask it a question and it might continue with three more questions, because that is what text on the internet often does. The journey from "text predictor" to "helpful assistant" happens in stages, and several of those stages involve people deciding what a good answer looks like.

## What kind of model is GPT?

GPT is a **pre-trained LLM** built on a **decoder-only Transformer** (see the previous article). In brief:

```
input text → tokens → embeddings + positional encoding
→ [ masked multi-head self-attention → feed-forward network → add & norm ] × N
→ probability of every possible next token
```

The **masking** means each token can only look at the tokens before it, never the ones after. That is exactly what next-token prediction needs. Training happens in the stages below.

## Stage 1: What is pretraining?

**Pretraining** means training the model on an enormous amount of text with one task: predict the next token. It takes up the large majority of the compute and data used to build the model.

The data is mostly raw text gathered at scale, much of it from the web, so its quality is uneven. It is split into tokens (**tokenization**) before training. For a sense of scale, GPT-3's dataset (OpenAI) was about 0.5 trillion tokens. OpenAI has not published the size of GPT-4's training data.

The result is a capable but unruly text completer. It has absorbed grammar, facts and styles, but it has not learned to follow instructions or to be helpful.

## Stage 2: What is supervised fine-tuning (SFT)?

**Supervised fine-tuning** trains the pre-trained model further on a smaller, labelled dataset of example prompts paired with good responses (or, for a translation model, sentence pairs). In full fine-tuning, all of the model's parameters are updated.

The aim is to teach the model to produce the kind of responses users are looking for. This is sometimes called **behavioural cloning**: the model learns to imitate the demonstrations. For InstructGPT, OpenAI had 40 labelers write around 13,000 (prompt, response) pairs.

That detail is worth pausing on. A few dozen people's sense of a "good answer" helped shape how a widely used model responds. Who those labelers are, what instructions they were given and which norms they bring all become part of the model's behaviour.

## What are PEFT and LoRA?

Updating every parameter of a huge model is expensive. **Parameter-efficient fine-tuning (PEFT)** updates only a small number of parameters instead.

The best-known method is **LoRA (low-rank adaptation)**. It freezes the original pre-trained weights and adds small, trainable matrices alongside them. Only those small additions are trained. You get much of the benefit of fine-tuning at a fraction of the cost, and you can swap different LoRA add-ons in and out for different tasks.

## Stage 3: What is RLHF?

**Reinforcement learning from human feedback (RLHF)** is a second alignment step. **Alignment** means making the model's behaviour match human preferences and values.

It works roughly like this:

1. The model generates several answers to the same prompt.
2. Human raters rank which answers they prefer.
3. A separate **reward model** is trained on those rankings, so it can score any new answer the way the raters would.
4. The language model is then optimised to earn higher reward scores, typically with an algorithm called **Proximal Policy Optimization (PPO)**.

**Direct Preference Optimization (DPO)** is a newer, simpler alternative. It trains the model directly on pairs of preferred and rejected answers, without building a separate reward model or running reinforcement learning.

Either way, "human preference" is a social fact, not a natural one. It reflects particular raters, guidelines and cultural assumptions.

## What happens at inference, when you send a prompt?

**Inference** means using the trained model to generate responses for real queries. Several things can happen here.

**Sampling.** The model produces a probability distribution over every token in its vocabulary and picks one (see the first article in this series):

- **Top-k sampling:** choose among the *k* most likely tokens.
- **Top-p sampling:** keep adding tokens, most likely first, until their combined probability reaches *p*, then choose among them.
- **Temperature:** higher temperature makes less common tokens more likely. It is often described as "creativity", but it mostly adds randomness.

**Retrieval (LLM + information retrieval).** The model can be connected to external sources, such as the web or a document collection. A retrieval module searches them (by keyword or by **vector search**, which finds passages with similar meaning) and adds what it finds to the prompt. This "augmented prompt" lets the model answer with information it was never trained on.

**Streaming.** Instead of waiting for the full answer, APIs send tokens as they are generated, using a streaming protocol such as SSE (server-sent events) or WebSockets over an HTTP connection. That is why you see answers appear word by word.

**Chain-of-thought reasoning.** Asking the model to work through intermediate steps before giving its answer often improves results on reasoning tasks. It began as a prompting technique and can be combined with any of the prompting styles below.

## What are zero-shot, few-shot and many-shot prompting?

| Style | What the user provides | Example |
|---|---|---|
| **Zero-shot** | A task instruction, no examples | "Translate this sentence into English." |
| **Few-shot** | A small number of input–output examples (about 1–5) | Three Chinese→English pairs, then the new sentence |
| **Many-shot** | Many examples, e.g. 50+ translation pairs | Strongly guides the output, a bit like fine-tuning inside the prompt |

Few-shot and many-shot prompting rely on **in-context learning**: the model picks up the pattern from examples in the prompt, without any change to its parameters. Beyond prompting, deployed models can also call external tools and APIs (**function calling** or **tool use**).

## What this means when you write a skill

- **A skill is in-context learning, not training.** Writing a skill does not change Claude's weights the way SFT or LoRA would. It works by putting instructions and examples into the context. That is why a good example or two inside a skill (few-shot) often does more than a paragraph of abstract rules.
- **The model is trained to be helpful, which can mean agreeable.** RLHF rewards answers that people prefer, and people tend to like confident, pleasing answers. So don't rely on simply asking the model "check your own work". Build checks into the harness: a script that validates the output, a test, or a fixed checklist step.
- **Retrieval beats memory for facts that change.** If a skill needs current or private information, have it read the file or search the source, rather than trusting what the model learned in pretraining.

## Key takeaways

- Pretraining on huge amounts of text, with the single task of next-token prediction, uses the large majority of the compute and produces a raw text completer.
- Supervised fine-tuning teaches it to imitate good responses; InstructGPT used about 13,000 pairs written by 40 labelers.
- LoRA is a cheap form of fine-tuning that freezes the original weights and trains small add-on matrices.
- RLHF (with a reward model and PPO) or DPO align the model with human preferences, and those preferences come from specific people.
- At inference, sampling, retrieval, streaming, chain-of-thought and zero/few/many-shot prompting shape what you actually see.
