# Grace's Skill Library

Source for **[lingegrace.github.io/skills](https://lingegrace.github.io/skills/)**, a card catalog of evidence-first Claude skills for academic, content and product work.

The skills themselves live in [lingegrace/claude-research-skills](https://github.com/lingegrace/claude-research-skills). This repo only builds the website.

## How it updates

A GitHub Action (`.github/workflows/build.yml`) rebuilds the site on every push and once a day:

- **Catalog:** read from the skills repo (each skill's `SKILL.md` and `README.md`).
- **Insights:** newsletter issues, read from the personal site's `newsletter.json`.
- **Resources:** lessons in `content/resources/*.md`. Add a file to add a lesson.
- **Pro:** plans, prices, checkout links and FAQ in `data/pro.yaml`.

## Build locally

```bash
pip install markdown==3.7 pyyaml==6.0.2
git clone https://github.com/lingegrace/claude-research-skills.git skills-src
python build.py            # writes _site/
```
