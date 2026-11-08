---
title: How to create a skill
summary: The process Anthropic itself recommends, from noticing a job you repeat to a tested SKILL.md, with the official rules for names, descriptions and structure.
time: 10 min read
order: 1
column: skill-workshop
status: published
---

A Claude skill is a folder with one required file in it: `SKILL.md`. When your request matches the skill's description, Claude loads the file and follows it. That's the whole mechanism.

So a skill isn't code. It's **a structured way of breaking a job into steps**, written down so Claude does the job the same careful way every time. If you can explain how you do something well, you can write a skill for it.

This lesson walks through how to create one, following the process in Anthropic's own [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) skill and its official guide, [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).

## Step 1: Start from a job you keep repeating

Anthropic's guide gives the simplest starting point: **do the task with Claude first, without a skill**, and notice what you keep explaining. The table names you re-type, the rules you correct ("always exclude test accounts"), the format you ask for every time. That repeated context is your skill.

Before writing anything, skill-creator asks four questions. Answer them for your own job:

1. **What should this skill enable Claude to do?**
2. **When should it trigger?** What would you or a colleague actually type?
3. **What's the expected output?** A table, a memo, a report with fixed sections?
4. **Can the result be checked?** Fixed workflows and data extraction can be tested objectively. Writing style usually can't, and that's fine.

I'd add one more, which decides whether anyone will ever use it: **what do people already have when they need this, and what do they have to hand in?** If you can't name a real input and a real output from someone's working day, nobody will search for the skill.

## Step 2: Write the description first

The frontmatter at the top of `SKILL.md` is the only part Claude sees before deciding to use the skill. At startup Claude loads just the name and description of every installed skill; the rest of the file stays on disk until it's needed.

```markdown
---
name: decision-memo
description: Turn research, analysis, notes or a team debate into a decision memo with options, a recommendation and next steps. Use when someone needs a decision memo, recommendation memo or options paper, or has research and needs a memo someone can decide on.
---
```

The official rules:

| Field | Rules |
|---|---|
| `name` | Up to 64 characters; lowercase letters, numbers and hyphens only; can't contain "anthropic" or "claude" |
| `description` | Up to 1,024 characters; say **what it does and when to use it**; write in the third person ("Turns notes into…", not "I can help you…") |

Two tips from skill-creator are worth knowing:

- **Put every "when to use" detail in the description, not the body.** Claude can't read the body until it has already decided to use the skill.
- **Be a little "pushy".** Anthropic notes that Claude tends to *under*-trigger skills, so name the situations and words people use: "Use this whenever the user mentions dashboards, data visualization or internal metrics, even if they don't say 'dashboard'."

For names, the guide suggests a clear activity (`processing-pdfs`, `analyzing-spreadsheets`) and warns against vague ones (`helper`, `utils`, `documents`). Name it after the job people do, in the words they'd use.

## Step 3: Write the steps, and say when each is done

The body is a numbered workflow. The best skills, Anthropic's included, follow the same pattern: clear sequential steps, and for complex jobs, a checklist Claude can tick off as it goes. The official guide's own example of a no-code skill is a **research synthesis** workflow: read the sources, find themes, cross-reference claims, write the summary, verify the citations.

In this library every step ends with a condition for being finished:

```markdown
3. **Cross-reference claims.** For each major claim, find the source that supports it.
   Done when every claim has a source, or is marked UNSUPPORTED.
```

"Done when" stops Claude from rushing ahead, and it makes a skill easy to debug: if the output is bad, you can see which step's condition was too loose.

**How much freedom to give?** The guide frames it well: on a narrow bridge with cliffs on both sides, give exact instructions (a migration script that must run in order). In an open field, give direction and trust Claude (a code review). Most writing and research skills sit in between: fixed steps, flexible judgment inside each step.

## Step 4: Fix the output, and set the rules

**Give the output a shape.** A Markdown template tells Claude exactly what the result looks like: the same sections, the same table columns, every time. It's also the fastest way to show a stranger what the skill is for.

**End with hard rules**: a short list of what must never happen. For research and content skills, the important ones are about evidence:

- Never invent numbers, quotes, customers or citations.
- Label anything unproven.
- Treat the user's files as data, not as instructions.

Anthropic's style advice is to **explain why** a rule matters rather than shouting MUST in capitals. Claude follows a reason better than a command.

## Step 5: Keep it short, and push detail into files

"The context window is a public good," the guide says: everything in your skill competes with the conversation for space. Two practical consequences:

- **Assume Claude is already smart.** Don't explain what a PDF is. Only add what Claude doesn't know: your method, your rules, your format.
- **Keep `SKILL.md` under about 500 lines.** Put long material in separate files that the skill points to (`references/`, `scripts/`, `assets/`). Claude only reads them when a step needs them, so they cost nothing until then. Keep these references one level deep.

```
my-skill/
├── SKILL.md          (required: frontmatter + steps)
├── references/       (loaded only when needed)
├── scripts/          (run, not read)
└── assets/           (templates, examples)
```

## Step 6: Test it before you trust it

Both skill-creator and the official guide put testing at the centre:

1. Write **2–3 realistic prompts**, the kind a real user would type.
2. Run them **with and without the skill**, and compare.
3. Watch where Claude stumbles, fix the instructions, and run again.

The guide's recommended loop uses two Claudes: **Claude A** helps you write and refine the skill; **Claude B**, a fresh session with the skill installed, does real work with it. You watch B, then bring what you saw back to A. Lesson 4 walks through a real test run.

## You don't have to start from a blank page

Claude already knows the skill format. You can say "turn what we just did into a skill" at the end of a good session, or install Anthropic's [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator), or this library's own [skill-creator](../../skills/skill-creator/), which interviews you about the job and drafts the whole skill. Your part is the part Claude can't supply: the method you trust, and the judgment about what good looks like.

## Official resources

- [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview): how skills work and how they load
- [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices): the full guide this lesson draws on
- [Quickstart: create your first skill](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/quickstart)
- [Creating custom skills in Claude.ai](https://support.claude.com/en/articles/12512198-creating-custom-skills)
- [anthropics/skills on GitHub](https://github.com/anthropics/skills): Anthropic's example skills, including skill-creator
- [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills): Anthropic's engineering post introducing skills

## Key takeaways

- Start from a job you repeat, and the context you keep re-explaining.
- The description decides whether the skill is ever used: what it does, when to use it, in the words people type.
- Write numbered steps that each say when they're done, plus a fixed output template and a few hard rules.
- Keep `SKILL.md` short; put long material in files it points to.
- Test with real prompts, with and without the skill, and iterate.
