---
title: Name it so people find it
summary: Why we renamed "product-value-fab" to "value-proposition-writer", and how to choose names and descriptions that both Claude and people searching can understand.
time: 5 min read
order: 3
column: skill-workshop
status: published
---

A skill has two audiences, and both judge it by its name and description:

1. **Claude**, which reads the description to decide whether to load the skill.
2. **People**, who search GitHub, skill directories and Google for something that solves their problem.

## A real mistake: "product-value-fab"

The first version of our features-to-benefits skill was called `product-value-fab`. It made perfect sense to us. FAB (Feature, Advantage, Benefit) is a classic sales framework, and the skill is about product value.

But almost nobody searches for "product value fab". People who need this skill think in their own words:

- "how do I write a **value proposition**"
- "turn **features into benefits**"
- "product **messaging**"

So we renamed it to **`value-proposition-writer`**. We kept "FAB" in the description, for the people who do know the term.

## Rules for names

- **Use the words of the job, not the method.** "value-proposition-writer" beats "fab-analyzer"; "thematic-analysis" beats "braun-clarke-coder". (The method can go in the description.)
- **Lowercase, hyphenated, two or three words.** That's the convention, and it reads well in a command: `/plugin install …`.
- **Check for collisions.** Search skill directories for the name first. We found someone already had a `research-analyst`, so ours became `content-research-analyst`. That's also more specific about who it's for.
- **Look at what already ranks.** Among research skills, the most common names are `deep-research`, `literature-review` and `market-research`. Using the established words helps people find you; inventing new jargon hides you.

## Rules for descriptions

The description is a few sentences that do three jobs:

```markdown
description: <What it does, in plain words>. Use when <who> needs <which output>,
  or has <which input>. <One line on what makes it different.>
```

- **Name the inputs people already have** ("a PRD, spec or feature list"). That's what they'll mention when they ask Claude for help.
- **Name the outputs they need** ("a value proposition, the why-it-matters section of a PRD, sales one-pager copy").
- **Include the synonyms people use:** value proposition, features and benefits, FAB, messaging.
- **Don't pad it.** A list of 40 keywords reads as spam to people and helps Claude less than one clear sentence.

## A quick test

Hand your skill's name to a colleague who has never seen it and ask: *"What do you think this does?"* If they can't answer in one sentence, rename it.
