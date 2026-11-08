---
title: "Harness: don't ask the model to check what code can check"
summary: "You'll understand what a harness is, the difference between before-the-fact constraints and after-the-fact feedback, and how to design a skill whose steps can be checked by code rather than by Claude's own judgement."
time: "6 min read"
order: 4
column: how-skills-work
status: published
---

Asking a model "did you do this correctly?" is a bit like asking a student to mark their own exam. Sometimes it works. But if there's an answer key, why not use it?

That's the idea behind a **harness**: the code around an AI agent that checks and constrains what it does. This article explains the two kinds of harness and how to use the same thinking when you design a skill.

## What is a harness?

The rule is simple:

> **If something can be checked by a deterministic program, don't rely on the model's own judgement.**

A **deterministic** program gives the same answer every time for the same input. A test either passes or fails. A file either exists or doesn't. A model, by contrast, predicts text based on probabilities. It's very good at judgement calls, but it can be confidently wrong, and it can't always notice its own mistakes.

A harness hands the checkable parts to code, so the model can spend its effort on the parts that genuinely need judgement.

> 🖼 Diagram to add: the agent loop (think → act → observe) with a "harness" layer wrapped around it, showing a gate before actions (constraints) and a checkpoint after actions (feedback).

There are two kinds.

## Before the fact: constraints

A constraint stops a mistake before it happens, by limiting what the model *can* do.

Claude Code has a good example. Its Edit and Write tools refuse to change a file that the model hasn't read first. If the model tries to edit a file blind, the tool returns an error. This isn't a polite request in the instructions ("please read files before editing them"). It's enforced in code, so it holds every time, however long and complicated the session gets.

```
Model: edit report.md
Tool:  Error. You haven't read report.md yet. Read it first.
Model: read report.md   → now it sees the real contents
Model: edit report.md   → allowed
```

A sociologist would recognise this as the difference between a norm and a rule built into the environment. A sign saying "please don't walk on the grass" relies on people choosing to comply. A fence doesn't.

## After the fact: feedback

Feedback lets the model act, then checks the result and shows it what went wrong.

The classic example is code. The agent writes some code, the harness automatically runs the tests, and if they fail, the error messages are put back into the context. The model reads them and fixes its own work. Now it's correcting against real evidence rather than its own impression.

In Claude Code, **hooks** make this possible. A hook is a script you set up to run automatically at a particular moment in the agent's work, for example before or after it uses a tool, or when it's about to finish. A hook that fires when the agent wants to stop can force a verification step: run the tests, check the output, and send back any failures before the task is marked done.

| | Constraint (before) | Feedback (after) |
|---|---|---|
| When it acts | Before an action happens | After an action, on the result |
| What it does | Blocks actions that break a rule | Checks the result and returns errors to the model |
| Example | Can't edit a file you haven't read | Run the tests; send failures back |
| Best for | Mistakes that are costly or hard to undo | Mistakes that are easy to detect and fix |

## How do you design a skill with checkable steps?

You don't need to be an engineer to think this way. When you write a skill, go through each step and ask: **how would anyone know this step was done correctly?**

There are three possible answers.

1. **Code can check it.** "The output file exists", "the table has exactly five columns", "every source has a URL". Make this an explicit check, ideally with a script.
2. **A clear condition can check it.** "Done when every feature is written as one concrete capability." Claude can check this reliably because the condition is specific.
3. **Only judgement can check it.** "The tone is warm but professional." Leave this to Claude, but give an example of what good looks like.

The more steps you can move from (3) to (2), and from (2) to (1), the more reliable your skill becomes.

## When should a skill include a script?

Add a script to the skill's `scripts/` folder when a step is:

- **Mechanical and repeatable**, like converting a PDF to images, counting words, or extracting form fields.
- **Easy to get subtly wrong by eye**, like checking that every citation in a list appears in the text.
- **A check that should never be skipped**, like validating a file's format before handing it over.

Then make the step say exactly when to run it and what to do with the result:

```markdown
4. **Check the references.** Run `scripts/check_refs.py draft.md`.
   If it reports any missing references, fix them and run it again.
   Done when the script reports no errors.
```

Notice the shape: the script is the answer key, and its output goes back into Claude's context as feedback. That's a small harness inside your skill.

Don't overdo it. If a step is genuinely a matter of judgement, a script can't help, and a forced numerical check can make the output worse.

## What this means when you write a skill

- **Turn "be careful" into a check.** "Make sure the numbers are right" is a hope. "Every number must appear in the source file; run the checker" is a harness.
- **Give every step a "done when".** A specific finishing condition is a check Claude can actually apply.
- **Put mechanical work in scripts.** Code does repetitive, exact work more reliably than a model improvising it.
- **Ask Claude to judge only what needs judgement.** That's where its strengths are.

## Key takeaways

- A harness is the code around an agent that constrains and checks it, so the model doesn't have to mark its own work.
- Constraints act before the fact (you can't edit a file you haven't read); feedback acts after (failed tests go back into the context).
- In Claude Code, hooks can trigger checks automatically, for example when the agent is about to stop.
- When designing a skill, make steps checkable, and add a script when a check is mechanical or must never be skipped.
