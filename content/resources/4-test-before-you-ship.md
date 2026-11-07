---
title: Test a skill before you ship it
summary: A real dry run of the value-proposition-writer on our own skill library, what it got right, and the one change it forced.
time: 7 min read
order: 4
---

A skill can read perfectly and still fail in use. The only way to know is to run it on real material, not a made-up example, and watch where it stumbles.

Here's how we tested the [value-proposition-writer](../../skills/value-proposition-writer/), using this library itself as the "product".

## 1. Pick real material you know well

We ran the skill on the skill library: its README, its 15 skill files and its install instructions. Testing on something you know well matters, because you can tell immediately when the output is wrong.

## 2. Follow the skill literally

Do exactly what the file says, step by step, without "helping". If the skill says ask in one message, ask in one message. You're testing the instructions, not your own judgment.

## 3. Watch for these failure points

**Did the clarifying step work?** Our first version asked six open questions at once, and the user didn't answer any of them. The fallback rule ("if the user can't answer, record it as an assumption and continue") saved the run, but the lesson was clear: **six open questions is too much friction.** We changed the step so each question comes with a default answer. Now people can reply "go with the defaults".

**Did the honesty rules hold?** This is where the skill earned its keep. To fill the Advantage column, we compared against the most popular marketing skill packs. The honest result was `PARITY` for most of the product-marketing skills: other packs already cover personas, review mining and competitor research well. The real differences turned out to be narrower: a dedicated FAB workflow, evidence labels across every skill, and social-science methods in the same library.

A skill that told us "you're better at everything" would have been useless. One that says `PARITY` is one you can trust.

**Is the output the shape you promised?** Check the result against the template, column by column. If you keep wanting to add a column, add it to the template.

## 4. Change one thing at a time

After the run, we made exactly one change: defaults on the clarifying questions. Then we ran it again. If you change five things at once, you won't know which one helped.

## A testing checklist

- [ ] Run on real material, not a toy example.
- [ ] Follow the file literally.
- [ ] Note every place you had to guess what the file meant. Those are the unclear instructions.
- [ ] Check the honesty rules: did it invent anything? Did it label what it couldn't prove?
- [ ] Compare the output with the template.
- [ ] Fix one thing, then run again.

> That's the workshop. Now browse the [catalog](../../skills/) for skills to learn from, or write your own and send it over.
