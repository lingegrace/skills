---
title: The anatomy of a skill people actually use
summary: A tour of the most popular skills on GitHub, what each one does well, and the patterns you can borrow for your own.
time: 9 min read
order: 3
column: skill-workshop
status: published
---

The fastest way to learn to write skills is to read good ones. Thousands of skills are now public, and a handful have been installed hundreds of thousands of times. They aren't popular because they're long or clever. They're popular because each one makes a few strong decisions.

Here are six worth studying, and the pattern each one teaches.

## The most popular skill collections

Star counts are from GitHub in November 2026, and install counts from the [skills.sh](https://skills.sh/) leaderboard. Both change daily, so read them as a sense of scale.

| Collection | Stars | What it is |
|---|---|---|
| [mattpocock/skills](https://github.com/mattpocock/skills) | ~318k | Matt Pocock's skills for planning, coding and learning: `grill-me`, `tdd`, `teach`, `handoff` |
| [obra/superpowers](https://github.com/obra/superpowers) | ~314k | A full software-development method as skills: brainstorming, writing plans, TDD, systematic debugging |
| [anthropics/skills](https://github.com/anthropics/skills) | ~189k | Anthropic's official examples: documents (Word, Excel, PowerPoint, PDF), `frontend-design`, `skill-creator` |
| [blader/humanizer](https://github.com/blader/humanizer) | ~66k | One skill that removes the tell-tale patterns of AI writing |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | ~59k | 50+ marketing skills, from copywriting to pricing |

## 1. `grill-me`: one sharp job

`grill-me` is one of the most-installed skills on skills.sh, and it's only a few lines long. Its job is simple: interview you relentlessly about a plan or design until it holds up.

**The pattern: one clear job, one clear behaviour.** You don't need pages of instructions when the job is sharp. If you can't say what your skill does in one sentence, split it.

## 2. `humanizer`: a catalogue of patterns, plus a loop

`humanizer` rewrites AI-sounding text so it reads like a person wrote it. Its core is a numbered list of AI-writing patterns (staged contrasts, forced triads, inflated claims), each with a before-and-after example, based on Wikipedia's "Signs of AI writing" guide. Then it gives a working loop: **mark the tells → draft the rewrite → check what still sounds like AI → write the final version.**

**The pattern: concrete examples beat abstract advice.** "Write naturally" changes nothing. Dozens of named patterns with examples change everything. It also has strict rules about meaning: keep every fact, add none.

## 3. `superpowers`: a whole method, split into small skills

`superpowers` doesn't try to do everything in one file. It encodes a software-development method as a set of small skills that hand off to each other: `brainstorming` → `writing-plans` → `executing-plans`, with `test-driven-development`, `systematic-debugging` and `verification-before-completion` along the way. It even has `writing-skills`, a skill about writing skills.

**The pattern: a method is a chain of small skills.** Each skill stays short and focused, and the method lives in how they connect. This library does the same thing: `research-question-grill` → `sociology-deep-research` → `interview-guide` → `thematic-analysis` → `fact-check-draft`.

## 4. Anthropic's document skills: scripts for what must be exact

The official Word, Excel, PowerPoint and PDF skills ship with `scripts/` folders: code for the fragile parts, like filling form fields or validating a document's structure. The `SKILL.md` tells Claude *when* to run each script, and Claude runs them without reading the code into its context.

**The pattern: don't ask the model to do what code can do reliably.** If a step must be exactly right every time, give it a script and have Claude check the script's output.

## 5. `frontend-design`: give Claude a point of view

`frontend-design` doesn't list CSS rules. It opens by casting Claude as the design lead at a studio known for distinctive work, for a client who "has already rejected proposals that felt cliché or templated." Then it explains *why* to ground design choices in the subject.

**The pattern: for judgement-heavy work, set the standard, not the steps.** Where many answers are valid, tell Claude what good looks like and why, then trust it.

## 6. `marketingskills`: shared context across many skills

Corey Haines' collection has one skill, `product-marketing`, that creates a single context document about your product, audience and positioning. Every other marketing skill reads it first, so you never explain your product twice.

**The pattern: when skills share facts, store them once.** If several of your skills need the same background (your company, your style guide, your research question), put it in one file they all read.

## What they all have in common

Across all six, the same few things show up again and again:

1. **A description that says what and when.** Every one names the situations it's for, in the words people actually use.
2. **One job per skill.** Big methods are split into small skills that hand off.
3. **Examples or named patterns, not vague advice.**
4. **A clear finish line**: a template, a checklist or a verification step.
5. **Rules that protect the user**: keep facts, don't invent, check before claiming success.

## How to study a skill yourself

Pick any skill on GitHub and read it with these questions:

- From the description alone, would I know when to use it?
- Can I find the steps in ten seconds?
- How does it know it's done?
- What does it refuse to do?
- What would break if I deleted half of it?

Then read one of your own drafts with the same questions. To see how these patterns look in practice here, browse this library's [catalog](../../skills/).

## Key takeaways

- The most-used skills are short, focused and opinionated.
- Concrete examples and named patterns beat general advice.
- Split a big method into small skills that hand off to each other.
- Use scripts where results must be exact; use a point of view where judgement matters.
- Store shared context once, and let every skill read it.
