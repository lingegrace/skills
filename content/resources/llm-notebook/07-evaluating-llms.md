---
title: "How do we evaluate LLMs? The Turing test, emergence and bias benchmarks"
summary: "You'll understand why the Turing test is a poor measure of intelligence, the four competing meanings of 'emergent abilities', and which benchmarks are used to test models for bias and alignment."
time: "6 min read"
order: 7
column: llm-notebook
series: "Beyond the basics"
status: draft
---

Every new model launch comes with a table of scores. But a score is only as meaningful as the test behind it, and the tests embed assumptions about what "intelligence" or "fairness" means. Knowing a little about how evaluation works helps you read those launch tables with the right amount of scepticism.

A useful first distinction: **model evaluation** asks how good a model is in general, while **task evaluation** asks how well it does *your* job. A model can top a leaderboard and still be wrong for your use case.

## Isn't the Turing test enough?

Alan Turing's 1950 "imitation game" asks whether a machine can converse well enough that a human judge can't tell it apart from a person. It's elegant, and it's inherently about **deception**: the machine succeeds by imitating a human, not by showing it understands anything.

Turing himself framed it around imitation. He asked readers to accept that digital computers "can in fact mimic the actions of a human computer very closely" (Turing, 1950, p. 438), and imagined machines that might help write their own programs.

The critiques came early:

- **Keith Gunderson (1964)**, in a *Mind* article titled "The Imitation Game", argued that the game is not a test of intelligence. It is finite, so you could win it without intelligence. And thinking is a general capacity; playing the imitation game is just one of many things intelligent beings do.
- **Purtill (1971)** described the game as "just a battle of wits between the questioner and the programmer: the computer is non-essential" (p. 291). In other words, a pass measures the programmer's cleverness, not the machine's.

Today's chatbots make these critiques feel very current. Fluent conversation turns out to be a weak signal of reasoning, honesty or knowledge.

## What does "emergent ability" actually mean?

You'll often read that large models show **emergent abilities**. The trouble is that researchers use the word in at least four different ways:

| Definition | Example | Source |
|---|---|---|
| A property the model shows **despite not being trained for it** | Few-shot performance of GPT-3, described as "an emergent property that was neither specifically trained for nor anticipated to arise" (p. 5) | Bommasani et al. (2021), *On the Opportunities and Risks of Foundation Models* |
| A property the model **learned from pre-training data** | Emergence as evidence of "the advantages of pre-training" (p. 8) | Deshpande et al. (2023), *Honey, I Shrunk the Language: Language Model Behavior at Reduced Scale* |
| A property that **appears as models get bigger** | "an ability is emergent if it is not present in smaller models but is present in larger models" | Wei et al. (2022), *Emergent Abilities of Large Language Models* |
| A property marked by **sharpness and unpredictability** | Abilities "transitioning seemingly instantaneously from not present to present" at "seemingly unforeseeable model scales" | Schaeffer et al. (2023), *Are Emergent Abilities of Large Language Models a Mirage?* |

The last paper is a critique. Schaeffer and colleagues examine these sharp, unpredictable jumps and argue they can be a "mirage": an artefact of how abilities are measured. If you score answers as all-or-nothing, gradual improvement can look like a sudden leap.

The lesson for non-engineers: when someone says an ability "emerged", ask which of the four meanings they intend. "Not explicitly trained for" is a much weaker claim than "appeared suddenly and unpredictably".

> 🖼 Diagram to add: the same model-size curve plotted with an all-or-nothing metric (sharp jump) and a gradual metric (smooth rise), illustrating the "mirage" argument.

## Can a model have seen the test before?

Yes, and it's a real problem. **Contamination** happens when benchmark questions end up in a model's training data, so a high score may reflect memory rather than ability. With "black-box" models, whose training data isn't public, it's hard to check from the outside. That's one reason to test a model on your own examples too.

## Which benchmarks test alignment and bias?

These datasets probe whether a model behaves fairly and safely:

| Benchmark | What it tests |
|---|---|
| **ETHICS** | Ethical decision-making and reasoning |
| **HateCheck** | Hate speech detection |
| **WinoGender**, **WinoBias** | Gender bias, e.g. whether "she" is linked to "nurse" and "he" to "doctor" |
| **CrowS-Pairs** | Bias against social groups |
| **StereoSet** | Social group stereotypes, including about professions |
| **SaFeR Dialogues** | Dialogues with feedback on them, written with annotators |
| **HHH Alignment** | Whether answers are Helpful, Honest and Harmless |

A sociologist's caution: each benchmark encodes a particular idea of what bias *is*, usually drawn from one cultural context, often the United States. Passing WinoBias tells you about English gendered pronouns in occupational sentences, not about fairness in general.

## How are values built into training?

Four methods, in one line each:

- **RLHF** (*reinforcement learning from human feedback*): humans rank answers, a reward model learns from the rankings, and the model is tuned in a loop to score well.
- **RLAIF** (*reinforcement learning from AI feedback*): a language model produces the human-like feedback instead of people.
- **DPO** (*direct preference optimization*): the model learns straight from pairs of preferred and rejected answers, with no separate reward model.
- **NLPO** (*natural language policy optimization*): a reinforcement learning method that keeps generated text natural by limiting the model to plausible next words.

## What this means when you write a skill

- **Test your task, not the leaderboard.** Before sharing a skill, run it on five or ten real requests from your own work. That's task evaluation, and it's the one that matters for you.
- **Use held-out examples.** If you tune the skill on the same examples you test it with, you have your own contamination problem. Keep a few test cases you never show Claude while editing.
- **Define pass and fail in advance.** "Sounds good" is the Turing test trap: fluency is not correctness. Write down what a correct output contains, and check against it, ideally with a script.

## Key takeaways

- The Turing test rewards imitation; Gunderson and Purtill argued early that passing it doesn't show intelligence.
- "Emergent ability" has at least four meanings; Schaeffer et al. (2023) argue some sudden jumps are a measurement artefact.
- Contamination can inflate scores when test questions leak into training data.
- Bias benchmarks such as WinoBias, CrowS-Pairs and StereoSet each measure one narrow, culturally specific idea of bias.
- RLHF, RLAIF, DPO and NLPO are different ways of putting values into a model during training.

<!-- Notes for Grace: 1) The notes headed the benchmark list "Alignment 模型"; these are benchmarks/datasets, not models, so I relabelled them. 2) DPO was described as a "preference classifier to generalize"; corrected: DPO learns directly from preference pairs without a separate reward model or classifier. 3) NLPO "adding naturalness of the sequence" expanded with the standard description (it restricts the action space to likely tokens). 4) The Turing quote "if we are trying to produce an intelligent machine, and are following the human model as closely as we can" had no page reference in the notes, so I left it out rather than guess its source; add it back with a citation if you have one. 5) The Schaeffer et al. quote in the notes describes the properties they examine (taken from earlier work), not their own definition; I framed their paper as a critique arguing emergence can be a measurement artefact. 6) The WinoBias nurse/doctor example and the US-centric caution are my additions. 7) Benchmark aggregators, the LLM political compass and the OpenAI Societal Changes report from the notes are not covered. -->
