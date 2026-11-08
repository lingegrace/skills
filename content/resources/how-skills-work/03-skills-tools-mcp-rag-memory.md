---
title: "Skills, tools, MCP, RAG and memory: what's the difference?"
summary: "You'll be able to tell skills, function calling, MCP, RAG and memory apart by asking one question of each: what text does it put into the model's context, and when?"
time: "7 min read"
order: 3
column: how-skills-work
status: draft
---

Skills, tools, MCP, RAG, memory: the AI world keeps adding new names, and they're often described as if each were a different kind of magic. They aren't. Almost all of them are ways of getting the right text into the model's context at the right time.

Once you see that, choosing between them gets much easier. This article takes each in turn and ends with a side-by-side comparison.

## The one idea underneath all of them

A language model only knows what's in its **context**: the text it can see when it writes its next word. It can't browse your files, remember yesterday, or look anything up unless something puts that information into the context for it.

So for each technique below, ask two questions: **what does it load into the context, and when?**

## Function calling: letting the model "act"

On its own, a model can only produce text. **Function calling** (also called *tool use*) lets it ask for something to be done.

The developer describes a tool to the model, for example a weather lookup:

```
name: get_weather
description: Get the current weather for a city
input: city (text)
```

When a user asks "Do I need an umbrella in London?", the model doesn't guess. It writes out a structured request, roughly `get_weather(city="London")`. The surrounding program runs the real weather lookup and puts the result back into the context. The model then reads it and answers.

The model never runs anything itself. It writes a request; code carries it out; the result comes back as text.

## MCP: a standard plug for tools

Here's the snag. The same weather tool has to be described one way for OpenAI's API and a different way for Anthropic's. Every tool, connected to every app, needed its own custom wiring.

**MCP** (the *Model Context Protocol*) is an open standard, introduced by Anthropic, for describing and connecting tools. A service like a calendar, a database or a design tool can offer an "MCP server" once, and any app that speaks MCP can plug into it. A useful comparison is a universal power socket: the appliance and the wall no longer need to be made for each other.

MCP doesn't make the model smarter. It makes tools easier to connect, so more of them can reach the context.

## RAG: looking things up before answering

**RAG** stands for *Retrieval-Augmented Generation*. The idea is in the name: **retrieve** relevant passages from a collection of documents, put them into the context, then **generate** an answer based on them.

Why not just search for matching words? Because exact string matching misses meaning. Suppose a user asks 「怎么开通高级版」 ("How do I get the premium plan?"), and the help document says 「Pro 订阅的购买流程」 ("How to buy a Pro subscription"). The two share no words at all, so a plain text search finds nothing.

This is where **embeddings** come in. An **embedding model** turns a piece of text into a list of numbers (a *vector*) that represents its meaning. The useful property: texts with similar meanings produce vectors that sit close together.

A typical RAG setup works like this:

1. **In advance:** split your documents into passages, turn each into a vector, and store them in a database.
2. **When someone asks a question:** turn the question into a vector too.
3. **Search:** find the stored vectors closest to the question's vector. Those are the most relevant passages.
4. **Answer:** put those passages into the context and let the model answer from them.

"Premium plan" and "Pro subscription" end up near each other, so the right passage is found.

> 🖼 Diagram to add: documents turned into dots in a 2D "meaning space", with the question's dot landing next to the "Pro subscription" passage and far from unrelated passages.

## Memory: carrying things across conversations

Each new conversation starts with an empty context. A **memory system** stores information that's worth keeping across sessions, and loads it into the context when a new session starts.

The simplest version is a document you maintain by hand: your preferences, your project's conventions. **Auto memory** works the same way, but the agent does the upkeep. After a conversation, it picks out what seems worth remembering (preferences you mentioned, project rules, mistakes it shouldn't repeat), writes them into a memory file, and that file is loaded at the start of the next session.

It's worth knowing what your tool has decided to remember about you, and checking it now and then. The agent is making judgement calls about what matters.

## Skills: the operating manual

A **skill** loads a written procedure into the context: how to do a particular job, step by step, sometimes with scripts to run. At the start, Claude only sees each skill's name and one-line description. The full manual is loaded when a task matches.

## Side by side

| | What it loads into context | When | Use it when… |
|---|---|---|---|
| **Function calling** | The result of an action (weather, a file, a calculation) | When the model asks for a tool | The model needs fresh data or needs to *do* something |
| **MCP** | Same as tools: their descriptions and results | When a connected tool is used | You want to connect existing services without custom wiring |
| **RAG** | Relevant passages from your documents | When a question is asked | The answer lives in a large body of documents |
| **Memory** | Facts about you or your project | At the start of each session | Things should carry over between conversations |
| **Skill** | A procedure: how to do a task | When the task matches its description | You want a job done the same careful way every time |

These are often combined. A skill might tell Claude which tools to call, and in what order.

## What this means when you write a skill

- **A skill is for "how", not "what".** If you find yourself pasting large reference documents into `SKILL.md`, that's knowledge, and it may belong in a separate file the skill opens on demand, or in a RAG system.
- **Name the tools in your steps.** If a step needs a tool or MCP connector, say which one and what to do with the result.
- **Don't use a skill as memory.** Personal preferences that apply to everything belong in memory or project instructions, not in one task's manual.
- **Your description is your retrieval.** Like RAG, skill loading depends on a match between the request and a short text. Write the description in the words people actually use.

## Key takeaways

- Nearly every technique here is a way of putting the right text into the model's context at the right time.
- Function calling lets the model request actions; MCP standardises how tools are connected.
- RAG uses embeddings to find passages by meaning, not exact words, then answers from them.
- Memory carries information across sessions; skills carry procedures for specific tasks.

<!-- Notes for Grace:
1) Function calling and MCP were headings only in the notes (plus "the weather tool is written differently in OpenAI vs Anthropic APIs"). I added brief standard explanations, the get_weather example in pseudo-code, and the "universal power socket" analogy. Please check they match what you'd have written.
2) Described MCP as "an open standard, introduced by Anthropic". Not in the notes, but well established; no date given.
3) RAG: the notes present embeddings as the core of RAG. In practice RAG can also use keyword search or a mix of both; I kept embeddings as the focus but framed it as "a typical RAG setup".
4) The notes repeat the RAG definition twice (lines 43 and 46); merged into one explanation.
5) Added a short comparison table and an English translation of the 高级版 / Pro 订阅 example.
-->
