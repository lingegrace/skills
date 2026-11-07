"""Build the Skill Library site.

Reads:
  - skills from a local checkout of github.com/lingegrace/claude-research-skills (SKILLS_DIR)
  - newsletter issues from the personal site's newsletter.json (falls back to data/newsletter.json)
  - tutorials from content/resources/*.md
  - paid skills from data/pro.yaml
Writes a static site to OUT_DIR (default: _site), with every page under BASE (default: /skills/).

Usage:  SKILLS_DIR=../research-skills python build.py
"""
import datetime as dt
import html
import json
import os
import pathlib
import re
import shutil
import urllib.request

import markdown
import yaml

ROOT = pathlib.Path(__file__).resolve().parent
SKILLS_DIR = pathlib.Path(os.environ.get("SKILLS_DIR", ROOT / "skills-src"))
OUT = pathlib.Path(os.environ.get("OUT_DIR", ROOT / "_site"))
BASE = os.environ.get("BASE", "/skills/")
SITE_URL = "https://lingegrace.github.io" + BASE.rstrip("/")
REPO = "lingegrace/claude-research-skills"
MARKETPLACE = "lingegrace-research-skills"
PERSONAL_SITE = "https://lingegrace.github.io/work-from-home-/"
NEWSLETTER_JSON = PERSONAL_SITE + "newsletter.json"
NEWSLETTER_URL = "https://www.linkedin.com/newsletters/7422191016994217984/"
SUBSCRIBE_URL = "https://www.linkedin.com/build-relation/newsletter-follow?entityUrn=7422191016994217984"
EMAIL = "graceguo2004@outlook.com"

# Repo folder → catalog field. Order = order on the site (academic and content first).
FIELDS = [
    {"key": "sociology", "code": "AC", "slug": "academic", "name": "Academic",
     "blurb": "Research questions, interviews, thematic and quantitative analysis, literature reviews."},
    {"key": "research", "code": "CR", "slug": "content", "name": "Content & Research",
     "blurb": "Research briefs from sources, and fact-checking before you publish."},
    {"key": "product-marketing", "code": "PM", "slug": "product-marketing", "name": "Product & Marketing",
     "blurb": "Value propositions, positioning, personas, launches, case studies, competitor analysis."},
]
FIELD_BY_KEY = {f["key"]: f for f in FIELDS}
PLUGIN_BY_FIELD = {"sociology": "sociology-research-skills", "research": "research-writing-skills",
                   "product-marketing": "product-marketing-skills"}
FEATURED = ["value-proposition-writer", "thematic-analysis", "fact-check-draft"]
# Workflow order inside each field (anything not listed goes last, alphabetically).
ORDER = ["research-question-grill", "sociology-deep-research", "interview-guide", "thematic-analysis",
         "quantitative-analysis", "content-research-analyst", "fact-check-draft", "value-proposition-writer",
         "positioning-messaging", "user-persona-builder", "customer-review-mining", "competitive-market-research",
         "feature-launch-kit", "customer-case-study", "ai-product-audit"]

e = html.escape
md = lambda text: markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])


def url(path=""):
    return BASE + path.lstrip("/")


# ─────────────────────────── data ───────────────────────────

def read_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return {}, text
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def load_skills():
    skills = []
    for skill_md in sorted(SKILLS_DIR.glob("skills/*/*/SKILL.md")):
        folder = skill_md.parent
        key = folder.parent.name
        if key not in FIELD_BY_KEY:
            continue
        meta, body = read_frontmatter(skill_md.read_text(encoding="utf-8"))
        readme = (folder / "README.md").read_text(encoding="utf-8") if (folder / "README.md").exists() else ""
        lines = [l.strip() for l in readme.splitlines()]
        tagline, summary, give, get, terms = "", "", "", "", ""
        if lines:
            m = re.match(r"#\s*[^:]+:\s*(.+)", lines[0])
            tagline = m.group(1).strip() if m else ""
            summary = next((l for l in lines[1:] if l and not l.startswith(("#", "|"))), "")
        for l in lines:
            row = re.match(r"\|\s*\*\*(You give it|You get back|Search terms)\*\*\s*\|\s*(.+?)\s*\|$", l)
            if row:
                label, val = row.groups()
                if label == "You give it":
                    give = val
                elif label == "You get back":
                    get = val
                else:
                    terms = val
        clean = lambda s: re.sub(r"[*_`]", "", re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s))
        field = FIELD_BY_KEY[key]
        skills.append({
            "name": meta.get("name", folder.name), "field": field, "tagline": clean(tagline),
            "summary": clean(summary), "give": clean(give), "get": clean(get), "terms": clean(terms),
            "description": meta.get("description", ""), "body": body,
            "github": f"https://github.com/{REPO}/tree/main/skills/{key}/{folder.name}",
            "zip": f"https://github.com/{REPO}/raw/main/dist/{folder.name}.zip",
            "plugin": PLUGIN_BY_FIELD[key], "access": "free",
        })
    rank = lambda s: ORDER.index(s["name"]) if s["name"] in ORDER else len(ORDER)
    skills.sort(key=lambda s: ([f["key"] for f in FIELDS].index(s["field"]["key"]), rank(s), s["name"]))
    counters = {}
    for s in skills:
        c = s["field"]["code"]
        counters[c] = counters.get(c, 0) + 1
        s["call"] = f"{c}-{counters[c]:02d}"
    return skills


def load_pro():
    p = ROOT / "data" / "pro.yaml"
    data = yaml.safe_load(p.read_text(encoding="utf-8")) if p.exists() else {}
    return data or {}


def load_newsletter():
    try:
        req = urllib.request.Request(NEWSLETTER_JSON, headers={"User-Agent": "lingegrace-skill-library"})
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read().decode("utf-8"))
        (ROOT / "data" / "newsletter.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except Exception as ex:
        print(f"newsletter: using cached copy ({ex})")
        p = ROOT / "data" / "newsletter.json"
        data = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"issues": []}
    return [i for i in data.get("issues", []) if str(i.get("url", "")).startswith("https://www.linkedin.com/pulse/")]


def load_resources():
    items = []
    for p in sorted((ROOT / "content" / "resources").glob("*.md")):
        meta, body = read_frontmatter(p.read_text(encoding="utf-8"))
        meta["slug"] = p.stem.split("-", 1)[1] if re.match(r"\d+-", p.stem) else p.stem
        meta["body"] = body
        items.append(meta)
    items.sort(key=lambda r: r.get("order", 99))
    return items


def fmt_date(d):
    if not d:
        return ""
    try:
        return dt.date.fromisoformat(d).strftime("%b %-d, %Y")
    except ValueError:
        return d


# ─────────────────────────── layout ───────────────────────────

NAV = [("skills/", "Catalog"), ("insights/", "Insights"), ("resources/", "Resources"), ("pro/", "Pro"), ("about/", "About")]


def page(path, title, description, body, active=""):
    canonical = SITE_URL + "/" + path
    nav = "".join(
        f'<a href="{url(href)}"{" aria-current=page" if active == href else ""}>{label}</a>' for href, label in NAV)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#F4ECDD">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect x='8' y='18' width='84' height='64' rx='6' fill='%23FBF6EC' stroke='%231A0F07' stroke-width='6'/><line x1='22' y1='42' x2='78' y2='42' stroke='%23C4562A' stroke-width='6'/><line x1='22' y1='60' x2='62' y2='60' stroke='%231A0F07' stroke-width='5'/></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{url('assets/style.css')}">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <a class="brand" href="{url()}"><span class="brand-mark" aria-hidden="true"></span><span>grace's <em>skill library</em></span></a>
  <nav class="nav" aria-label="Main">{nav}<a class="nav-out" href="{PERSONAL_SITE}">Grace ↗</a></nav>
</header>
<main id="main">
{body}
</main>
<footer class="foot">
  <div class="foot-cols">
    <div><div class="foot-brand">grace's <em>skill library</em></div><p>Evidence-first Claude skills for academic, content and product work. Free and open source.</p></div>
    <div><b>Library</b><a href="{url('skills/')}">Catalog</a><a href="{url('insights/')}">Insights</a><a href="{url('resources/')}">Resources</a><a href="{url('pro/')}">Pro</a></div>
    <div><b>Elsewhere</b><a href="{PERSONAL_SITE}">Personal site</a><a href="https://github.com/{REPO}">GitHub</a><a href="{NEWSLETTER_URL}">Newsletter</a><a href="mailto:{EMAIL}">Email</a></div>
    <div><b>Help</b><a href="{url('pro/#faq')}">FAQ</a><a href="{url('pro/#refunds')}">Refunds</a><a href="{url('resources/')}">How to write a skill</a></div>
  </div>
  <p class="foot-note">© {dt.date.today().year} Linge (Grace) Guo · Skills are MIT-licensed · Built from <a href="https://github.com/{REPO}">{REPO}</a></p>
</footer>
<script src="{url('assets/app.js')}" defer></script>
</body>
</html>
"""


def card(s, compact=False):
    f = s["field"]
    stamp = '<span class="stamp stamp-free">Free</span>' if s["access"] == "free" else '<span class="stamp stamp-pro">Pro</span>'
    terms = " ".join(t.strip() for t in s["terms"].split(","))
    return f"""<a class="card" href="{url('skills/' + s['name'] + '/')}" data-field="{f['slug']}" data-access="{s['access']}" data-search="{e((s['name'] + ' ' + s['tagline'] + ' ' + s['summary'] + ' ' + terms).lower())}">
  <span class="card-hole" aria-hidden="true"></span>
  <span class="card-top"><span class="call">{s['call']}</span><span class="card-field">{e(f['name'])}</span>{stamp}</span>
  <span class="card-title">{e(s['name'])}</span>
  <span class="card-tag">{e(s['tagline'])}</span>
  {'' if compact else f'<span class="card-sum">{e(s["summary"])}</span>'}
  <span class="card-lines"><span><b>Give</b>{e(s['give'])}</span><span><b>Get</b>{e(s['get'])}</span></span>
</a>"""


def install_block(s):
    return f"""<div class="install">
  <div class="install-tabs" role="tablist">
    <button role="tab" aria-selected="true" data-tab="cc">Claude Code</button>
    <button role="tab" aria-selected="false" data-tab="web">Claude.ai / desktop</button>
    <button role="tab" aria-selected="false" data-tab="manual">Manual</button>
  </div>
  <div class="install-pane" data-pane="cc">
    <p>Add the library once, then install this skill's drawer ({e(s['field']['name'])}):</p>
    <pre><code>/plugin marketplace add {REPO}
/plugin install {s['plugin']}@{MARKETPLACE}</code></pre>
    <button class="copy" data-copy="/plugin marketplace add {REPO}&#10;/plugin install {s['plugin']}@{MARKETPLACE}">Copy</button>
  </div>
  <div class="install-pane" data-pane="web" hidden>
    <ol><li><a href="{s['zip']}">Download {e(s['name'])}.zip</a></li><li>In Claude, open <b>Settings → Capabilities → Skills</b> and click <b>Upload skill</b>.</li><li>Turn it on, and start with one of your own files.</li></ol>
  </div>
  <div class="install-pane" data-pane="manual" hidden>
    <pre><code>git clone https://github.com/{REPO}.git
cp -R claude-research-skills/skills/{s['field']['key']}/{s['name']} ~/.claude/skills/</code></pre>
  </div>
</div>"""


# ─────────────────────────── pages ───────────────────────────

def build_home(skills, issues, resources, pro):
    by = {f["key"]: [s for s in skills if s["field"]["key"] == f["key"]] for f in FIELDS}
    drawers = "".join(f"""<a class="drawer" href="{url('skills/?field=' + f['slug'])}">
  <span class="drawer-plate"><span class="drawer-code">{f['code']}</span><span class="drawer-name">{e(f['name'])}</span></span>
  <span class="drawer-count">{len(by[f['key']])} cards</span>
  <span class="drawer-blurb">{e(f['blurb'])}</span>
  <span class="drawer-pull" aria-hidden="true"></span>
</a>""" for f in FIELDS)
    featured = "".join(card(s) for s in skills if s["name"] in FEATURED)
    latest_issues = "".join(f"""<li><a href="{e(i['url'])}" target="_blank" rel="noopener"><span class="ins-date">{fmt_date(i.get('date'))}</span><span class="ins-title">{e(i['title'])}</span><span class="ins-arrow">↗</span></a></li>""" for i in issues[:4])
    tutorials = "".join(f"""<a class="lesson" href="{url('resources/' + r['slug'] + '/')}"><span class="lesson-no">Lesson {r.get('order', '')}</span><span class="lesson-title">{e(r['title'])}</span><span class="lesson-sum">{e(r.get('summary', ''))}</span></a>""" for r in resources[:3])
    free = sum(1 for s in skills if s["access"] == "free")
    body = f"""
<section class="hero">
  <div class="hero-text">
    <p class="eyebrow">A card catalog of Claude skills</p>
    <h1>Skills for the work <em>around</em> the code.</h1>
    <p class="lede">Literature reviews, interview analysis, research briefs, fact-checks, value propositions. Each skill asks what you're trying to do, works in clear steps, and never makes things up.</p>
    <div class="hero-cta"><a class="btn btn-ink" href="{url('skills/')}">Browse the catalog</a><a class="btn btn-line" href="{url('resources/')}">Learn to write one</a></div>
  </div>
  <div class="hero-stack" aria-hidden="true">
    <div class="hcard hcard-3"></div><div class="hcard hcard-2"></div>
    <div class="hcard hcard-1"><span class="call">AC-04</span><span class="hc-title">thematic-analysis</span><span class="hc-line">Braun &amp; Clarke, six phases</span><span class="hc-line">Give: transcripts</span><span class="hc-line">Get: codebook, themes, quotes</span><span class="stamp stamp-free">Free</span></div>
  </div>
</section>

<section class="stats" aria-label="Library at a glance">
  <div><b>{len(skills)}</b><span>skills in the catalog</span></div>
  <div><b>{free}</b><span>free &amp; open source</span></div>
  <div><b>{len(FIELDS)}</b><span>drawers: academic, content, product</span></div>
  <div><b>0</b><span>invented citations allowed</span></div>
</section>

<section class="block">
  <div class="block-head"><h2>Open a drawer</h2><a href="{url('skills/')}">All {len(skills)} skills →</a></div>
  <div class="drawers">{drawers}</div>
</section>

<section class="block">
  <div class="block-head"><h2>On the reading desk</h2><span class="muted">Three skills to start with</span></div>
  <div class="cards cards-3">{featured}</div>
</section>

<section class="block how">
  <div class="block-head"><h2>Every card works the same way</h2></div>
  <ol class="how-steps">
    <li><b>Starts from what you have.</b><span>A PRD, transcripts, a draft, a dataset, a pile of reviews.</span></li>
    <li><b>Asks before it writes.</b><span>Your goal, the document you need, your audience and their pain points, each with a sensible default.</span></li>
    <li><b>Works in fixed steps.</b><span>Each step says when it's done, and the output follows a fixed template.</span></li>
    <li><b>Shows its evidence.</b><span>Every claim points to your material, or is labeled as an assumption or "needs proof".</span></li>
  </ol>
</section>

<section class="block split">
  <div>
    <div class="block-head"><h2>Reading room</h2><a href="{url('insights/')}">All insights →</a></div>
    <p class="muted">Weekly essays on AI, society and markets from my newsletter, <em>Signals Across Markets</em>.</p>
    <ul class="ins-list">{latest_issues}</ul>
  </div>
  <div>
    <div class="block-head"><h2>Workshop</h2><a href="{url('resources/')}">All lessons →</a></div>
    <p class="muted">How to write a skill people actually use, taught with real examples from this library.</p>
    <div class="lessons">{tutorials}</div>
  </div>
</section>

<section class="block pro-teaser">
  <div><p class="eyebrow">Special collections</p><h2>Pro skills are coming.</h2><p>Deeper, done-for-you workflows for academic and content work, built on the free catalog.</p></div>
  <a class="btn btn-ink" href="{url('pro/')}">See what's planned</a>
</section>
"""
    return page("", "Grace's Skill Library · Claude skills for academic, content & product work",
                f"{len(skills)} free, evidence-first Claude skills: literature review, thematic analysis, interview guides, fact-checking, value propositions, positioning and more.",
                body)


def build_catalog(skills):
    chips = "".join(f'<button class="chip" data-filter-field="{f["slug"]}" aria-pressed="false">{e(f["name"])} <span>{sum(1 for s in skills if s["field"]["key"] == f["key"])}</span></button>' for f in FIELDS)
    sections = ""
    for f in FIELDS:
        items = [s for s in skills if s["field"]["key"] == f["key"]]
        sections += f"""<section class="drawer-section" data-section="{f['slug']}">
  <div class="drawer-label"><span class="drawer-code">{f['code']}</span><h2>{e(f['name'])}</h2><span class="muted">{e(f['blurb'])}</span></div>
  <div class="cards">{''.join(card(s) for s in items)}</div>
</section>"""
    body = f"""
<section class="page-head">
  <p class="eyebrow">The catalog</p>
  <h1>{len(skills)} skills, filed by field.</h1>
  <p class="lede">Free and MIT-licensed. Every card says what you give it and what you get back.</p>
</section>
<div class="filters">
  <label class="search"><span class="sr-only">Search skills</span><input id="q" type="search" placeholder="Search: literature review, personas, fact-check…" autocomplete="off"></label>
  <div class="chips"><button class="chip" data-filter-field="all" aria-pressed="true">All <span>{len(skills)}</span></button>{chips}</div>
</div>
<p class="empty" id="empty" hidden>No card matches that. Try another word, or <a href="mailto:{EMAIL}?subject=Skill%20request">request a skill</a>.</p>
{sections}
"""
    return page("skills/", "Skill catalog · Grace's Skill Library",
                "Browse free Claude skills for literature reviews, thematic analysis, interview guides, survey analysis, fact-checking, value propositions, positioning, personas and launches.",
                body, active="skills/")


def build_skill(s, skills):
    related = [x for x in skills if x["field"]["key"] == s["field"]["key"] and x["name"] != s["name"]][:3]
    body_html = md(s["body"])
    body = f"""
<nav class="crumbs" aria-label="Breadcrumb"><a href="{url('skills/')}">Catalog</a> / <a href="{url('skills/?field=' + s['field']['slug'])}">{e(s['field']['name'])}</a> / <span>{e(s['name'])}</span></nav>
<article class="skill">
  <header class="skill-card">
    <span class="card-hole" aria-hidden="true"></span>
    <div class="card-top"><span class="call">{s['call']}</span><span class="card-field">{e(s['field']['name'])}</span><span class="stamp stamp-free">Free</span></div>
    <h1>{e(s['name'])}</h1>
    <p class="skill-tag">{e(s['tagline'])}</p>
    <p class="skill-sum">{e(s['summary'])}</p>
    <dl class="skill-lines"><div><dt>You give it</dt><dd>{e(s['give'])}</dd></div><div><dt>You get back</dt><dd>{e(s['get'])}</dd></div></dl>
    <div class="skill-actions"><a class="btn btn-ink" href="#install">Install</a><a class="btn btn-line" href="{s['github']}">View on GitHub ↗</a></div>
  </header>
  <section id="install" class="skill-sec"><h2>Install</h2>{install_block(s)}</section>
  <section class="skill-sec"><h2>The full instructions</h2><p class="muted">This is exactly what Claude reads. Nothing hidden.</p><div class="prose skill-md">{body_html}</div></section>
  {f'<section class="skill-sec"><h2>Search terms</h2><p class="muted">{e(s["terms"])}</p></section>' if s['terms'] else ''}
  <section class="skill-sec"><h2>Same drawer</h2><div class="cards cards-3">{''.join(card(r, compact=True) for r in related)}</div></section>
</article>
"""
    return page(f"skills/{s['name']}/", f"{s['name']}: {s['tagline']} · Claude skill",
                (s["summary"] + " Free Claude skill for Claude Code and Claude.ai.")[:300], body, active="skills/")


def build_insights(issues):
    if issues:
        lead, rest = issues[0], issues[1:]
        items = "".join(f"""<li><a href="{e(i['url'])}" target="_blank" rel="noopener"><span class="ins-date">{fmt_date(i.get('date'))}</span><span class="ins-title">{e(i['title'])}</span><span class="ins-arrow">↗</span></a></li>""" for i in rest)
        lead_html = f"""<a class="ins-lead" href="{e(lead['url'])}" target="_blank" rel="noopener"><span class="eyebrow">Latest · {fmt_date(lead.get('date'))}</span><span class="ins-lead-title">{e(lead['title'])}</span><span class="btn btn-line">Read on LinkedIn ↗</span></a>"""
    else:
        items, lead_html = "", '<p class="muted">New issues appear here automatically.</p>'
    body = f"""
<section class="page-head">
  <p class="eyebrow">Reading room</p>
  <h1>Insights</h1>
  <p class="lede">From <em>Signals Across Markets</em>, my weekly newsletter on macro forces, technology, society and AI, written from a humanistic perspective. New issues appear here automatically.</p>
  <div class="hero-cta"><a class="btn btn-ink" href="{SUBSCRIBE_URL}">Subscribe on LinkedIn</a><a class="btn btn-line" href="{NEWSLETTER_URL}">All issues ↗</a></div>
</section>
<section class="block">{lead_html}<ul class="ins-list ins-list-big">{items}</ul></section>
"""
    return page("insights/", "Insights · Grace's Skill Library",
                "Insights on AI, society and markets from Linge (Grace) Guo's LinkedIn newsletter, Signals Across Markets.",
                body, active="insights/")


def build_resources(resources):
    lessons = "".join(f"""<a class="lesson lesson-big" href="{url('resources/' + r['slug'] + '/')}"><span class="lesson-no">Lesson {r.get('order', '')} · {e(r.get('time', ''))}</span><span class="lesson-title">{e(r['title'])}</span><span class="lesson-sum">{e(r.get('summary', ''))}</span></a>""" for r in resources)
    body = f"""
<section class="page-head">
  <p class="eyebrow">Workshop</p>
  <h1>Learn to write skills people actually use.</h1>
  <p class="lede">Short lessons built from real skills in this library: what a good skill is made of, how to write one, how to name it so people find it, and how to test it before you ship.</p>
</section>
<section class="block"><div class="lessons lessons-grid">{lessons}</div></section>
<section class="block">
  <div class="block-head"><h2>Further reading</h2></div>
  <a class="ins-lead" href="https://www.linkedin.com/pulse/i-turned-my-research-workflow-ai-skill-linge-guo-hezfc" target="_blank" rel="noopener"><span class="eyebrow">Essay · Oct 14, 2026</span><span class="ins-lead-title">I Turned My Research Workflow into an AI Skill</span><span class="muted">How a sociologist's research routine became a reusable skill, and what changed in the process.</span><span class="btn btn-line">Read on LinkedIn ↗</span></a>
</section>
"""
    return page("resources/", "Resources: how to write a Claude skill · Grace's Skill Library",
                "Step-by-step lessons on writing Claude skills (SKILL.md): anatomy, a worked features-to-benefits example, naming for discovery, and testing.",
                body, active="resources/")


def build_lesson(r, resources):
    i = resources.index(r)
    prev_l = resources[i - 1] if i > 0 else None
    next_l = resources[i + 1] if i + 1 < len(resources) else None
    pager = '<nav class="pager">' + (f'<a href="{url("resources/" + prev_l["slug"] + "/")}">← {e(prev_l["title"])}</a>' if prev_l else "<span></span>") + (f'<a href="{url("resources/" + next_l["slug"] + "/")}">{e(next_l["title"])} →</a>' if next_l else "") + "</nav>"
    body = f"""
<nav class="crumbs" aria-label="Breadcrumb"><a href="{url('resources/')}">Workshop</a> / <span>Lesson {r.get('order', '')}</span></nav>
<article class="lesson-page">
  <header><p class="eyebrow">Lesson {r.get('order', '')} · {e(r.get('time', ''))}</p><h1>{e(r['title'])}</h1><p class="lede">{e(r.get('summary', ''))}</p></header>
  <div class="prose">{md(r['body'])}</div>
  {pager}
</article>
"""
    return page(f"resources/{r['slug']}/", f"{r['title']} · Workshop", r.get("summary", "")[:300], body, active="resources/")


def build_pro(pro):
    plans = pro.get("plans", [])
    plan_html = "".join(f"""<div class="plan{' plan-hi' if p.get('highlight') else ''}">
  <p class="eyebrow">{e(p['name'])}</p><p class="price">{e(p['price'])}</p><p class="muted">{e(p.get('note', ''))}</p>
  <ul>{''.join(f'<li>{e(x)}</li>' for x in p.get('includes', []))}</ul>
  {f'<a class="btn btn-ink" href="{e(p["checkout_url"])}">{e(p.get("cta", "Buy"))}</a>' if p.get('checkout_url') else f'<a class="btn btn-line" href="mailto:{EMAIL}?subject={e(p["name"])}%20waitlist">Join the waitlist</a>'}
</div>""" for p in plans)
    skills = pro.get("skills", [])
    skill_html = "".join(f"""<div class="card card-static"><span class="card-hole" aria-hidden="true"></span><span class="card-top"><span class="call">SC-{n:02d}</span><span class="card-field">{e(x.get('field', ''))}</span><span class="stamp stamp-pro">{e(x.get('status', 'Coming soon'))}</span></span><span class="card-title">{e(x['name'])}</span><span class="card-sum">{e(x.get('summary', ''))}</span></div>""" for n, x in enumerate(skills, 1))
    faq = "".join(f"<details><summary>{e(q['q'])}</summary><p>{e(q['a'])}</p></details>" for q in pro.get("faq", []))
    body = f"""
<section class="page-head">
  <p class="eyebrow">Special collections</p>
  <h1>Pro</h1>
  <p class="lede">{e(pro.get('intro', ''))}</p>
</section>
<section class="block"><div class="plans">{plan_html}</div></section>
{f'<section class="block"><div class="block-head"><h2>In the special collection</h2></div><div class="cards cards-3">{skill_html}</div></section>' if skills else ''}
<section class="block" id="faq"><div class="block-head"><h2>Questions</h2></div><div class="faq">{faq}</div></section>
<section class="block" id="refunds"><div class="block-head"><h2>Refunds</h2></div><p>{e(pro.get('refunds', ''))}</p></section>
"""
    return page("pro/", "Pro skills · Grace's Skill Library", "Pro Claude skills for academic and content work.", body, active="pro/")


def build_about(skills):
    body = f"""
<section class="page-head">
  <p class="eyebrow">About the librarian</p>
  <h1>Hi, I'm Grace.</h1>
  <p class="lede">I'm a sociologist (UCL; MSc Sociology, Oxford) who studies how AI and digital technologies reshape the way we know, work and live, and how AI companions, AI deception and platform governance work in practice.</p>
</section>
<section class="block prose about">
  <p>This library started with my own research workflow. I turned the way I do literature reviews into a Claude skill, and then kept going. Each skill here encodes a method I trust: Braun &amp; Clarke for thematic analysis, careful claim-checking for research briefs, and Feature → Advantage → Benefit for product value.</p>
  <p>Every skill follows the same rule I hold myself to as a researcher: <strong>show your evidence, and say what you don't know.</strong> They ask before they write, work in steps, and never invent a citation, a number or a customer.</p>
  <p>There are {len(skills)} skills so far, all free. More are on the way, along with lessons on how to write your own.</p>
  <p><a class="btn btn-ink" href="{PERSONAL_SITE}">Visit my personal site ↗</a> <a class="btn btn-line" href="mailto:{EMAIL}">Email me</a></p>
</section>
"""
    return page("about/", "About · Grace's Skill Library", "About Linge (Grace) Guo, the sociologist behind Grace's Skill Library.", body, active="about/")


def build_404():
    body = f"""<section class="page-head"><p class="eyebrow">Card not found</p><h1>This card isn't in the catalog.</h1><p class="lede">It may have been refiled. Try the <a href="{url('skills/')}">catalog</a>.</p></section>"""
    return page("404.html", "Not found · Grace's Skill Library", "Page not found.", body)


# ─────────────────────────── write ───────────────────────────

def write(path, content):
    p = OUT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def main():
    skills = load_skills()
    if not skills:
        raise SystemExit(f"No skills found in {SKILLS_DIR}. Set SKILLS_DIR to a checkout of {REPO}.")
    issues = load_newsletter()
    resources = load_resources()
    pro = load_pro()
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "assets", OUT / "assets")
    write("index.html", build_home(skills, issues, resources, pro))
    write("skills/index.html", build_catalog(skills))
    for s in skills:
        write(f"skills/{s['name']}/index.html", build_skill(s, skills))
    write("insights/index.html", build_insights(issues))
    write("resources/index.html", build_resources(resources))
    for r in resources:
        write(f"resources/{r['slug']}/index.html", build_lesson(r, resources))
    write("pro/index.html", build_pro(pro))
    write("about/index.html", build_about(skills))
    write("404.html", build_404())
    # machine-readable catalog + sitemap
    write("skills.json", json.dumps([{k: s[k] for k in ("name", "call", "tagline", "summary", "give", "get", "github", "zip", "access")} | {"field": s["field"]["name"]} for s in skills], ensure_ascii=False, indent=2))
    pages = ["", "skills/", "insights/", "resources/", "pro/", "about/"] + [f"skills/{s['name']}/" for s in skills] + [f"resources/{r['slug']}/" for r in resources]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE_URL}/{p}</loc></url>\n" for p in pages) + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    print(f"Built {len(pages)} pages: {len(skills)} skills, {len(issues)} insights, {len(resources)} lessons → {OUT}")


if __name__ == "__main__":
    main()
