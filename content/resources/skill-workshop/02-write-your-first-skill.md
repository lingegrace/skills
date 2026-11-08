---
title: "Write your first skill: turning a research method into a skill"
summary: How I turned the way sociologists do research into sociology-deep-research, and why knowing a method is what lets you see the problems a skill should fix.
time: 12 min read
order: 2
column: skill-workshop
status: published
---

The best skills don't come from clever prompts. They come from a **method**: a way of doing a job that a field has worked out over years. If you know a method well, you can see exactly where AI goes wrong without it. That gap is your skill.

This lesson walks through a real example: how I turned the way sociologists do research into [sociology-deep-research](../../skills/sociology-deep-research/). You can follow the same five steps with any method you know: a reporting standard, an editing process, a sales playbook, a clinical checklist.

## Why start from a method you know?

I trained as a sociologist. Research methods training teaches you to ask questions most people skip: *Who did this study actually look at? Does this source really support that claim, or just mention the topic? Is this a correlation dressed up as a cause?*

When I started using AI for "deep research", I kept seeing the same problems, and I could see them **because** of that training:

| What AI research tends to do | What a trained researcher does instead |
|---|---|
| Cites a source that exists, and assumes it supports the claim | Checks two things separately: is the source real, and does it actually say this? |
| Turns "associated with" into "causes" | Matches the strength of the claim to the study design |
| Counts five articles reporting the same study as five pieces of evidence | Groups sources that share the same underlying data |
| Summarises authors one by one | Maps the literature as a debate: who agrees, who disagrees, what's missing |
| Answers whatever question it was given | Asks first whether the question is answerable at all |
| Sounds certain throughout | Separates observation, interpretation and speculation, and says what's unknown |

None of these are failures of intelligence. They're the absence of a method. That's good news: a method can be written down.

> The full story of how this started is in my essay [I Turned My Research Workflow into an AI Skill](https://www.linkedin.com/pulse/i-turned-my-research-workflow-ai-skill-linge-guo-hezfc).

## Step 1: Name the common problems

Before writing a single instruction, list the problems your method exists to prevent. Mine were the six rows above. Each one becomes a rule or a step in the skill.

This is the step people skip, and it's the most important. A skill that says "do good research" changes nothing. A skill that says "check source identity and claim support as separate steps, and never mark a claim verified just because the source exists" changes every answer.

## Step 2: Write the method as stages

Next, write down how a careful researcher actually works, in order. For social science research, that's roughly:

```
A  Brief        → turn the topic into an answerable question, with scope and assumptions
B  Scoping scan → first search; map the literature as a debate
H  Checkpoint   → stop and let the human choose the direction
C  Retrieval    → build a source ledger: what each study actually studied
D  Evidence     → check each central claim against what the source really says
E  Argument     → map premises → conclusion; run an adversarial critique
F  Synthesis    → grade every insight by how well the evidence supports it
```

Each stage has a **gate**: a condition that must be met before moving on. Gate A, for example, is "the scope is explicit." This is the research version of "Done when", and it's what stops the model from skipping ahead.

## Step 3: Build in a human checkpoint

Stage H is my favourite part of the skill. After the scoping scan, the skill **must stop** and give the user a short decision brief: what the scan suggests, two to four directions to choose from, and the trade-offs. Only then does the deep research start.

This comes straight from how supervisors work with students: you agree the direction before months of work, not after. For an AI it saves even more, because it stops the model from confidently researching the wrong question.

## Step 4: Turn your field's vocabulary into labels

Methods come with precise vocabulary. Put it in the skill as labels the model must use. sociology-deep-research uses two sets.

**Is the source real?** `VERIFIED` · `PARTLY_VERIFIED` · `UNVERIFIED` · `CONTRADICTED_LIKELY_FABRICATED`

**Does it support the claim?** `DIRECT` · `PARTIAL` · `CONTRADICTS` · `NO_SUPPORT` · `NOT_TESTED`

And a rule connecting them: *a VERIFIED source never implies DIRECT support.*

Labels do two jobs. They force the model to make a judgement instead of hedging, and they make the output easy to check: you can scan for every `NOT_TESTED` claim in seconds.

The skill does the same for the type of claim. A descriptive claim needs an accurate measure and population; a causal claim needs a design that handles timing, confounding and selection; a mechanism needs evidence of the process itself. A cross-sectional correlation alone can't support a causal claim, so the skill won't let it.

## Step 5: Decide what "good" means, and what would fail it

Finally, write down how you'd judge the result. sociology-deep-research ends with a scorecard (question quality, literature synthesis, evidence, causal discipline, reflexivity and more) and a **critical-fail list**. If any of these happen, the dossier is marked `PROVISIONAL — NOT VALIDATED`:

- a fabricated or contradicted central citation
- a central claim marked verified when it was never tested
- a causal claim without a defensible identification check
- counterevidence suppressed
- the human checkpoint skipped without permission

The skill is also honest about its limits. It never claims to be "hallucination-free", only "audited for the checks listed".

## Scaling: don't use a sledgehammer for a nail

A full dossier for every question would be exhausting. So the skill has **modes**:

| Mode | When | What it produces |
|---|---|---|
| `SCOPING` | A quick map of a topic | Brief, scan, checkpoint, short synthesis |
| `SYNTHESIS` (default) | A real literature synthesis | Every stage and table |
| `PROTOCOL` | A plan to run later | Brief, scan, checkpoint, written protocol |
| `AUDIT` | Checking someone else's report | Evidence and argument stages only |

If your method has light and heavy versions, give your skill modes too, and say when to use each.

## What this looks like for your field

The same five steps work for any method you know well:

1. **Name the common problems** the method prevents.
2. **Write the method as stages**, each with a gate.
3. **Add a human checkpoint** where direction matters.
4. **Turn the field's vocabulary into labels** the model must use.
5. **Define good, and define fail.**

A journalist might start from verification standards. A UX researcher from interview analysis. A teacher from how they diagnose misconceptions. Your expertise isn't made redundant by AI; it's exactly what the AI is missing.

Read the full skill on its [catalog card](../../skills/sociology-deep-research/), then try [Lesson 1](../how-to-create-a-skill/) for the general process, or use [skill-creator](../../skills/skill-creator/) to draft your own.

## Key takeaways

- A good skill starts from a method, not a prompt.
- Knowing a method lets you see exactly where AI goes wrong without it. Those gaps become your rules.
- Write the method as stages with gates, and stop for the human where direction matters.
- Turn your field's vocabulary into labels the model must use.
- Define what good looks like, and what counts as a fail.
