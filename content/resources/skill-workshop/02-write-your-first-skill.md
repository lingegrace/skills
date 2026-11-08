---
title: "Write your first skill: turning features into benefits"
summary: A complete walkthrough of building the value-proposition-writer skill, from the work problem to the finished SKILL.md.
time: 12 min read
order: 2
column: skill-workshop
status: published
---

In this lesson we'll build a real skill from scratch: **[value-proposition-writer](../../skills/value-proposition-writer/)**, which turns a product's feature list into a Feature → Advantage → Benefit (FAB) analysis. You can follow the same five steps for any skill.

## Step 1: Start from a pain in someone's working day

Every product manager writes PRDs. When the PRD has to explain *why the product matters*, most of them list features and stop:

> "AI summarization. Multi-language support. SSO."

That isn't value. Nobody buys "SSO"; they buy "IT signs off in a day instead of a month". The gap is that the writer never stopped to think about **who the audience is**, **what hurts for them**, and **what they'd use instead**.

So the job of the skill is clear: take the material people already have, make them think about audience and pain, then write real value.

- **Input people already have:** a PRD, a spec, a feature list, a landing page.
- **Output they need:** a value section for the PRD, a sales one-pager, launch copy.

## Step 2: Write down how an expert does it

Before writing any prompt, write the method as a human would explain it to a junior colleague:

1. Read what exists.
2. Ask what it's for, who it's for, and what they use today.
3. **Feature**: what the product *does*, in plain words.
4. **Advantage**: why that beats the alternatives. You have to name a competitor, or "doing nothing".
5. **Benefit**: what each audience *gets*, tied to their pain.
6. Write the value statement, and list what's still unproven.

That list *is* the skill. Everything after this is just writing it down carefully.

## Step 3: Make the clarifying step concrete

The most important step is number 2, asking before writing. A vague "ask the user for context" doesn't work. Name exactly what to ask:

```markdown
2. **Clarify in one message, with defaults.** Ask only what the material does not
   already answer, and give your best-guess default for each one:
   - **Goal:** what document is this for? *Default: <your guess>*
   - **Audience:** who buys, who uses, who signs off? *Default: …*
   - **Background and pain:** what made them look for a solution? *Default: …*
   - **Competitors:** what do customers compare against, including "do nothing"? *Default: …*

   Done when the user has confirmed or corrected the defaults. If they don't reply,
   proceed with the defaults and list them as Assumptions.
```

Notice the **defaults**. Our first version asked six open questions, and in testing the user didn't answer any of them. Giving defaults means people can reply "go with the defaults" in two seconds. (Lesson 4 covers how we found this.)

## Step 4: Build in honesty

The Advantage column is where AI loves to make things up: "faster than any competitor!" So we add a hard rule into the step itself:

```markdown
4. **Advantages.** Compare each feature with the named competitors. Search the web
   if available, and cite what you find. If there is no real advantage, write
   `PARITY` — don't invent one.
```

`PARITY` turns out to be one of the most useful words in the whole skill. It tells the product team where they *aren't* different, which is exactly what they need to know.

## Step 5: Give the output a shape

Finally, the template. A FAB matrix has a natural table shape:

```markdown
| Feature (what it does) | Advantage (vs. whom, and how) | Benefit for <audience A> | Evidence |
|---|---|---|---|
| ... | ... / PARITY | ... | source, user claim, or NEEDS PROOF |
```

…followed by a value statement per audience and a "gaps to fix before publishing" list.

## The finished skill

Put the four parts together (description, steps with "done when", template and rules) and you have a skill about 60 lines long. You can read the complete file on its [catalog card](../../skills/value-proposition-writer/).

## Try it yourself

Pick a task you do every week at work and answer:

1. What do I start from?
2. What do I hand in?
3. What are the 4–6 steps an expert follows in between?
4. What must never happen?

Write the answers into the four parts from Lesson 1, and you have a first draft. Then name it well (Lesson 3) and test it (Lesson 4).
