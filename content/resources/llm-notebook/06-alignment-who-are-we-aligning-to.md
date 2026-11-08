---
title: "AI alignment explained: who are we aligning models to?"
summary: "You'll understand how models are tuned to human preferences (RLHF, PPO, DPO and its variants), what that costs, and why the question of whose preferences count is still open."
time: "7 min read"
order: 6
column: llm-notebook
series: "Beyond the basics"
status: draft
---

A freshly pre-trained model can complete sentences, but it isn't yet a helpful assistant. **Alignment** is the stage where it's tuned to behave the way people want: answering the question asked, declining harmful requests, being honest about uncertainty. The technical question is *how*. The more interesting question, for anyone who studies society, is *whose wants*.

## Who did InstructGPT align to?

InstructGPT, the OpenAI model that paved the way for ChatGPT, is unusually candid about this. Its authors said the model was aligned to:

1. **The training labelers**, who wrote demonstrations and ranked answers;
2. **The researchers** who designed the study, and by proxy OpenAI as an organisation;
3. **Customers**, meaning what API users (and in some cases their end users) found valuable.

That's a short list. A team of contracted labelers, one company's researchers and its paying customers stand in for "human preferences". This isn't a scandal; someone has to decide. But it's a reminder that "aligned" always means aligned *to someone*.

**Constitutional AI**, Anthropic's approach for Claude, makes part of that choice explicit. Instead of relying only on human rankings, the model is given a written set of principles (a "constitution"), critiques and revises its own answers against them, and AI-generated feedback based on those principles is used in training. The values are written down where people can read and argue with them.

## How does learning from human preferences work?

People find it much easier to compare two things than to rank a hundred. It's easier to say which of two wines you prefer than to order a whole cellar. The **Bradley-Terry model** is a statistical model built on this idea: from many observed pairwise comparisons ("A beat B"), it infers a score for each item.

That's a natural fit for human feedback. Labelers see two answers to the same prompt and pick the better one. A **reward model** learns, Bradley-Terry style, to give higher scores to answers people tend to choose.

Then **PPO** (*Proximal Policy Optimization*) takes over. PPO is a reinforcement learning algorithm, used when there's no single "correct label", only a reward signal. It nudges the model (the *policy*) towards high-reward answers while keeping each update small and stable, balancing trying new responses against repeating ones that already score well. Together this pipeline is called **RLHF**, reinforcement learning from human feedback.

PPO's drawbacks, according to the notes:

- it needs a reward model or ongoing human labelling;
- it may need a lot of data to converge;
- its settings (hyperparameters) are not straightforward to tune.

> 🖼 Diagram to add: RLHF pipeline (pairwise human rankings → Bradley-Terry reward model → PPO updates the model) next to DPO (pairwise rankings → model updated directly).

## What is DPO, and why did it catch on?

**DPO** (*Direct Preference Optimization*) skips the separate reward model. It trains the model directly on preference pairs: for each prompt, a *chosen* answer and a *rejected* one. It has become widely used, especially for open models, because it is simpler and cheaper than running PPO.

If you fine-tune with DPO, you'll see two numbers in the training logs:

| Metric | What it measures |
|---|---|
| `rewards/chosen` | How much more likely the model now finds the chosen answers than the original (reference) model does, scaled by a setting called beta |
| `rewards/rejected` | The same, for the rejected answers |

What should happen? **They should move apart.** As training works, the model favours preferred answers more and rejected answers less.

DPO isn't free of problems. It tends to overfit (learning the training pairs too literally), good preference data is hard to collect, and it still needs substantial computing power.

## What are IPO, KTO and ORPO?

Several variants try to fix DPO's weak spots:

| Method | Full name | Motivation | Idea |
|---|---|---|---|
| **IPO** | Identity Preference Optimisation | DPO overfits | Adds a regularisation term (a penalty that keeps learning in check) to the DPO loss |
| **KTO** | Kahneman-Tversky Optimisation | Reduce biases and generalise how preference is learned | Borrows from prospect theory in behavioural economics, which explains why people don't always maximise expected value; it maximises the *utility* of answers rather than the likelihood of preferences, and can learn from simple "good" or "bad" labels instead of pairs |
| **ORPO** | Odds Ratio Preference Optimisation | Simplify the pipeline | Combines ordinary fine-tuning and preference learning in one step, without a reference model |

Hugging Face's **TRL** (*Transformer Reinforcement Learning*) library and its **Alignment Handbook** provide working recipes for these methods.

## What makes alignment hard in practice?

- **Resources.** Fully training an 8-billion-parameter model such as Llama 3 can take more than 60 GB of GPU memory. Parameter-efficient methods help: **LoRA** (*Low-Rank Adaptation*) freezes the original weights and trains two small extra matrices, often around 1% of the parameters or fewer, which can be merged back in so the model runs no slower.
- **Catastrophic forgetting.** Tuning on new data can erase what the model knew. Remedies: track performance on general-knowledge benchmarks, use regularisation (such as DeepMind's *elastic weight consolidation*), and mix general data in with your specialised data.
- **Alignment tax.** Aligning to preferences can hurt performance on other tasks. InstructGPT's authors saw some drops but judged PPO a low-tax method.
- **Data quality.** Make sure the data matches your real users, include edge cases, filter out texts that are too short, too long or off-topic, and remove near-duplicates. High-quality synthetic data from strong models (as in Stanford's Alpaca) is one option.
- **Evaluation.** Building a custom way to judge whether alignment worked is itself complex.

## Is alignment the same as censorship? The debate

Advocates of so-called **"uncensored models"**, mostly from the open-source community, make four arguments:

1. **Narrow values.** Aligned models carry one fairly uniform value system, with little representation of other cultures.
2. **Over-refusal.** Models are often taught to avoid whole topics rather than answer well, so alignment slides into managing corporate risk.
3. **Software freedom.** In the spirit of Richard Stallman's free-software principles: if it's my model on my machine, I should be able to change it.
4. **A base to build on.** To design your own alignment, you need an unaligned instruction-tuned model to start from.

The other side argues that removing safeguards makes misuse easier, and that refusals on some topics reflect real harms, not only corporate caution. Both sides agree on one thing: someone's values end up in the model. The disagreement is about who should get to choose them.

## What this means when you write a skill

- **You are aligning, on a small scale.** A skill tells Claude whose standards to follow for one job. Name them: "the APA 7th edition", "our style guide", "the reviewer's checklist".
- **Write principles down, constitution-style.** Explicit rules in `SKILL.md` are easier to inspect and fix than taste you hope Claude will infer.
- **Show chosen and rejected examples.** A good-versus-bad pair teaches more than a description, the same reason preference pairs work in DPO.
- **Watch for your own alignment tax.** Strict rules for one task can make outputs worse elsewhere, so keep the skill's scope narrow.

## Key takeaways

- Alignment always answers the question "aligned to whom?"; InstructGPT named labelers, researchers and customers.
- RLHF learns a reward model from pairwise choices (Bradley-Terry) and optimises with PPO.
- DPO learns from preference pairs directly; IPO, KTO and ORPO address its weak spots.
- Practical costs include memory, forgetting, an alignment tax and data quality.
- The "uncensored models" debate is ultimately about who chooses the values.

<!-- Notes for Grace: 1) "KPO" corrected to "KTO" (Kahneman-Tversky Optimisation). 2) ORPO was only named in the notes; I added a one-line standard description. 3) The KTO line about learning from single good/bad labels is a well-established property I added for clarity. 4) "DPO is a default today for a lot of modern LLMs" softened to "widely used, especially for open models". 5) Notes say DPO's "compute requirements are exhaustive"; DPO is cheaper than PPO, so I wrote "still needs substantial computing power". 6) The 60 GB figure for an 8B model is kept but framed as "can take more than", since it depends on setup. 7) LoRA/PEFT folded into the resources point; "LoRa" corrected to "LoRA"; "usually only 1%" softened to "often around 1% or fewer" (your PEFT code example shows 0.19%). 8) "Uncensored models" presented as a debate attributed to open-source advocates, with the counter-argument added. The notes don't name the source; the four points match Eric Hartford's 2023 blog post "Uncensored Models", worth checking and citing. In point 4 "inconsistent base" seems to mean "unaligned base", and "resolvability" likely means "composability" (Hartford's term). 9) Constitutional AI explanation added from general knowledge since the notes only name it. -->
