---
title: "Inference-time tricks and AI agents, explained in plain English"
summary: "You'll understand what can be done to a model's answer after training is over, from chain-of-thought and self-consistency to tool use, and what actually turns a language model into an agent."
time: "7 min read"
order: 5
column: llm-notebook
series: "Beyond the basics"
status: draft
---

A lot of what makes an AI tool feel smart happens in the seconds after you press enter. This stage is called **inference**: the moment a trained model is used to produce an answer. Much of the progress you notice as a user, such as models that "think", search the web or book a meeting, comes from what engineers do at inference time, not from a new model.

## What can you change once a model is trained?

The model's weights (the numbers it learned in training) are fixed. What you *can* change is how you ask, how many times you ask, and what you do with the answer. Grace's notes list the main moves:

| Move | What it means |
|---|---|
| Multiple runs (self-consistency) | Ask the same question several times and keep the most common answer |
| Prompt pipelines | Break a job into a sequence of prompts, each one a step in a workflow |
| Advanced prompting | Tree-of-Thought, Graph-of-Thought and similar ways of exploring several lines of reasoning |
| External data (RAG) | Fetch relevant documents and put them in front of the model before it answers |
| Style guides, policies, constitutions | Give the model written rules to follow |
| Long documents | Split texts that are longer than the model's context window into pieces |
| Tools (function calling) | Let the model ask a program to fetch data or take an action |
| Quality checks | Score the answer and retry or rephrase if it's weak |
| Reflection | Have a second model (or a second pass) critique the first answer |
| Multi-agent workflows | Several model-based or code-based agents passing work between them |

None of these touches the model itself. They are all about the system *around* the model.

## How do chain-of-thought and self-consistency work?

**Chain-of-thought (CoT)** prompting asks the model to show its reasoning step by step before giving an answer. The classic way is to include a few worked examples (called *few-shot exemplars*) in the prompt, each with its reasoning written out. Because a model predicts one word at a time, writing out the steps gives it more "room" to get to the right answer.

**Self-consistency** builds on this. Instead of taking one chain of reasoning, you sample several, each a little different, and pick the answer most of them agree on. If you ask a model 「中国的首都是」 five times and four runs say 北京, you trust 北京 more than any single run.

**Tree-of-Thought** goes further: the model explores several possible next steps and abandons the dead ends.

## What is ReAct, and why does it help with made-up answers?

A model reasoning on its own can confidently build on a wrong fact, and the error carries through every later step. **ReAct** (short for *Reasoning + Acting*) interleaves thinking with doing. The model writes a thought, takes an action (in the original research, querying a simple Wikipedia API), reads the result, and thinks again.

```
Thought: I need the population of the city in the question.
Action: search("Lyon population")
Observation: [the search result, with the figure]
Thought: Now I can compare it with...
```

Checking facts against an outside source as it goes reduces hallucination (confidently invented content). It also leaves a readable trail, so a human can see *why* the model answered as it did.

## What is function calling?

**Function calling** (also called *tool use*) lets a model ask an outside program to do something. It covers two jobs:

1. **Fetch data**, for example retrieving documents (this is how RAG, *retrieval-augmented generation*, is often wired up) or checking today's weather for 「今天天气」.
2. **Take actions**, such as sending an email, running code or updating a spreadsheet.

The model doesn't run the tool itself. It writes a structured request ("call `get_weather` with city = Beijing"), your code runs it, and the result goes back to the model. In Anthropic's approach, developers define the tools Claude can call on their side, so Claude can be adapted to a much wider range of tasks. Benchmarks such as the Berkeley Function Calling Leaderboard compare how reliably different models do this.

## Does prompt wording change accuracy?

Somewhat. Research on **EmotionPrompts** tested adding emotional phrases to the end of a prompt, such as *"This is very important to my career."* The authors reported that some of these phrases improved scores on many of their tasks, and that combining certain phrases scored well. Treat it as an interesting finding rather than a rule: effects vary between models and tasks.

A more dependable habit for reducing hallucination is to give the model explicit permission not to know:

> Answer as truthfully as possible, and if you're unsure of the answer, say "Sorry, I don't know".

Asking for **concise** answers may help too. One explanation practitioners give is simple: the fewer words a model has to generate, the fewer chances it has to make something up.

## So what is an agent?

Grace's notes give a clean definition:

> An agent is an LLM equipped with **tools**, **memory**, and some **orchestration code** (to call tools, manage memory and run the agentic loop).

The loop looks like this:

```
1. Read the goal and what's in memory
2. Decide: answer now, or use a tool?
3. If a tool: call it, read the result, save what matters to memory
4. Go back to step 2 until the goal is met
```

ReAct is one way to run this loop. A specialised example is **ChemCrow**, which connects a language model to chemistry tools so it can plan and check chemistry tasks rather than guess. Frameworks such as AutoGPT, GPT-Engineer and BabyAGI package this loop so people can automate repetitive tasks or generate whole code projects.

> 🖼 Diagram to add: the agent loop, with LLM at the centre and arrows to Tools, Memory and Orchestration code.

## What about many agents working together?

A **multi-agent system** is a group of agents, each with its own role (a personality or skill set) and its own capabilities (model, tools, objectives), collaborating on one task. One might research, another write, a third check the result. Frameworks for building these include **LangGraph** (with LangGraph Studio for visualising the flow), **CrewAI** and **AutoAgents**.

The most famous social experiment is Stanford's **Generative Agents**: a small simulated town of 25 agents that users can talk to in natural language. Each agent keeps a *memory stream*. It retrieves relevant past events, reflects on them to draw higher-level conclusions, and uses those conclusions to plan both its next move and its longer-term behaviour.

For a social scientist, simulated agents are becoming a laboratory for social behaviour; platforms such as Epitome present themselves as experimental environments for AI and social science. The question to keep in view: whose behaviour, and whose assumptions, are these simulated people built from?

## What this means when you write a skill

- **A skill is an inference-time method.** It doesn't retrain Claude. It changes the instructions and steps Claude follows, which is exactly the kind of lever this article describes.
- **Write steps, not hopes.** A numbered workflow in `SKILL.md` works like a prompt pipeline: each step narrows what comes next.
- **Give Claude an exit.** Telling it to say "I don't know" or to flag missing information beats asking it to "be accurate".
- **Check with a tool, not with trust.** Asking the model to re-read its own answer is weak reflection. A script that validates the output, such as a test or a word-count check, is a harness, and harnesses catch what self-checks miss.

## Key takeaways

- Inference is when a trained model answers; much of today's progress happens here, not in training.
- Chain-of-thought gives the model room to reason; self-consistency votes across several attempts.
- ReAct and function calling ground answers in outside data and let models act, which reduces hallucination.
- An agent is an LLM plus tools, memory and orchestration code running a loop.
- Multi-agent systems split work between roles, and simulations like Generative Agents raise real questions for social science.

<!-- Notes for Grace: 1) "Functional calling" corrected to "function calling" throughout. 2) "Berkey Function Calling Leaderboard" corrected to "Berkeley". 3) Notes said "CoT reasoning: improve Self-Consistency"; it's the other way round: self-consistency improves chain-of-thought by sampling several reasoning paths and voting. 4) ReAct "overcomes hallucination" softened to "reduces". 5) EmotionPrompt results described neutrally and attributed to the paper's authors; I left out the specific EP-number rankings (EP01+EP04, EP02 most effective) since they're hard to read without the paper's table; add back if you want. 6) "Concise answers reduce hallucination" softened to "may help". 7) "Anthropic Approach - Functional Call defined by users" rephrased: developers define tools on their side (client tools). 8) Epitome's "world's first" claim reported as how the platform presents itself, not as fact. 9) The ReAct trace (Lyon population) is my illustration, not from your notes; swap in your own if you prefer. 10) Jamba-1.5, Consensus, Scite.AI, Elicit and WebArena from the notes are not covered here. -->
