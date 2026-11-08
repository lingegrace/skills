---
title: "What actually happens when Claude uses a skill"
summary: "You'll understand the agent loop Claude runs on, why a written procedure makes it more reliable, and how a skill gets loaded into Claude's context only when it's needed."
time: "6 min read"
order: 1
column: how-skills-work
status: draft
---

When you install a skill, nothing about Claude itself changes. No new brain, no retraining. What changes is the *text* Claude can see at the right moment. Once you understand that, it becomes much clearer why some skills work beautifully and others are ignored.

This article walks through the machinery: the loop an AI agent runs in, why it still benefits from a written procedure, and how a skill gets into that loop.

## What is an "agent", really?

A large language model (LLM) on its own does one thing: it reads text and writes more text. An **agent** is what you get when you put that model inside a loop and give it **tools**: small programs it can ask to run, such as "read this file", "search the web" or "run this script".

The core idea fits in a few lines of pseudo-code:

```
while the task is not finished:
    the model looks at everything in its context and decides the next step
    if it decides to use a tool:
        run the tool, and add the result to the context
    else if it decides the task is done:
        give the final answer and stop
```

The **context** is everything the model can see at that moment: your instructions, the conversation so far, and the results of every tool it has used. Each time round the loop, more text gets added to it.

So an agent is not a mysterious autonomous mind. It is a model that keeps **thinking → acting → observing the result → thinking again**. In the research literature this pattern is called **ReAct**, short for *Reasoning + Acting*.

> 🖼 Diagram to add: a circular loop with four stops (Think, Act with a tool, Observe the result, Think again), with an arrow showing each tool result being appended to a growing "context" box.

Two things make this loop work. The model's reasoning decides whether it can work out a sensible next step. The tools are what let it turn that idea into an action in the world.

## Why does the context window matter so much?

Because every step adds text, the context grows as the agent works. The **context window** is the maximum amount of text the model can take in at once, measured in **tokens** (chunks of text, roughly a short word or part of a word each).

If the window is small, an agent that runs for many rounds fills it up. Older material gets cut off, and the model effectively "forgets" what happened earlier in the task. This is one reason model makers have pushed context windows up: some current models offer windows of up to a million tokens, which lets agents run for longer before they lose track.

## If the agent can figure things out, why tell it how?

It's a fair question. The model *can* explore on its own. But for complex tasks, improvising tends to be less reliable than following a set procedure.

Think about how organisations work. A capable new colleague could probably work out how to process a refund from scratch. But you'd still hand them the team's checklist, because the checklist captures decisions someone already made: which order to do things in, what to check, what never to do. The result is the same careful job every time, not a different improvisation each time.

That is exactly what a skill is for.

## So what is a skill, mechanically?

**A skill is the text of an operating manual, loaded into the agent's context.**

You take a workflow you use often, write it down as a document (`SKILL.md`), and hand it to the agent. Once that text is in its context, the agent can follow it step by step.

A skill folder can also include a `scripts/` directory of ready-made programs. Anthropic's PDF skill, for example, ships with scripts along these lines:

```
scripts/
├── extract_form_field_info.py   # pull out a form's fields
├── fill_fillable_fields.py      # fill in the fields
├── convert_pdf_to_images.py     # turn PDF pages into images
└── ...
```

After reading `SKILL.md`, the agent knows: to find out what fields a form has, run `extract_form_field_info.py`. To check the filled-in form looks right, run `convert_pdf_to_images.py` and look at the pictures. The manual tells it *what to do*; the scripts let it *do it the same way every time*.

## How does Claude know which skill to load?

If every skill's full text sat in the context from the start, a few dozen skills would crowd out everything else. Anthropic's answer is a design called **progressive disclosure**: reveal information in layers, only when it becomes relevant.

| When | What Claude sees |
|---|---|
| At the start of every session | Each skill's **name** and **one-line description**. Even dozens of skills take up little space. |
| When a task seems to match a skill | The full `SKILL.md` |
| When a step calls for it | Extra files in the folder, such as scripts or reference documents |

This is an engineering optimisation, not a new principle. The underlying mechanism is unchanged: it's still putting text into the context. Loading it on demand simply saves a great many tokens.

There's a quietly important consequence here, too. The description is the gatekeeper. Whoever writes those few words decides when the manual gets opened at all.

## What this means when you write a skill

- **Your description is all Claude sees first.** If it doesn't name the situations and inputs that should trigger the skill, the rest of your careful work never gets loaded.
- **Write steps, not vibes.** The agent loop runs one step at a time. A numbered procedure gives it a clear "next step" to pick each time round.
- **Move repeatable mechanics into scripts.** If a step is the same every time (converting a file, extracting fields), a script does it more reliably than asking the model to improvise it.
- **Keep the main file lean.** Put long reference material in separate files and tell Claude when to open them, so they only use up context when needed.

## Key takeaways

- An agent is an LLM in a loop: think, act with a tool, observe, repeat (ReAct). Every result is added to its context.
- For complex tasks, following a written procedure is usually more reliable than letting the model improvise.
- A skill is simply an operating manual (plus optional scripts) loaded into the context.
- Progressive disclosure means Claude starts with only each skill's name and description, and loads the full file when a task matches.

<!-- Notes for Grace:
1) "现在主流模型的上下文窗口几乎都到了 1M token" softened to "some current models offer windows of up to a million tokens" (overstated and time-sensitive).
2) Line 34 was cut off ("就像…") and had a typo ("他就能部就班" → 按部就班). I completed the thought with my own analogy (a team checklist for a new colleague); please check it fits what you intended.
3) I attributed the scripts/ example to Anthropic's PDF skill, since the script names match it. Please confirm that's your source.
4) Added a third layer to the progressive disclosure table (extra files/scripts loaded only when a step needs them). Your notes only describe two layers ("name + description" then "more content").
5) Dropped the cross-reference to "用 Skills 定制你的 AI 工作流" because that article doesn't exist on this site yet.
-->
