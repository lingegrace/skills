"""Build Grace's Skill Library.

Reads:
  - free skills from a checkout of github.com/lingegrace/claude-research-skills (SKILLS_DIR)
  - newsletter issues from the personal site's newsletter.json (falls back to data/newsletter.json)
  - lessons from content/resources/*.md
  - Pro plans, Pro skill listings and FAQ from data/pro.yaml
  - site settings (form endpoint, personas) from data/site.yaml
Writes a static site to OUT_DIR (default: _site), every page under BASE (default: /skills/).

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
LINKEDIN = "https://www.linkedin.com/in/lingeguo2004/"

# Repo folder → catalog field (one drawer each). Order = order on the site.
FIELDS = [
    {"key": "social-science", "code": "SS", "slug": "social-science", "name": "Social Science Research",
     "blurb": "Research questions, literature reviews, interviews, thematic and quantitative analysis.", "color": "#3E6B8A"},
    {"key": "market-research", "code": "MR", "slug": "market-research", "name": "Market Research",
     "blurb": "Deep research, market sizing, competitors, trends and topics, with sources you can check.", "color": "#8A4E6E"},
    {"key": "writing", "code": "WR", "slug": "writing", "name": "Writing, Editing & Social Media",
     "blurb": "Research briefs, fact-checks, your own voice, LinkedIn, newsletters and academic writing.", "color": "#6E7F3E"},
    {"key": "work", "code": "WK", "slug": "work", "name": "Meetings, Memos & Reports",
     "blurb": "Meetings, reports, memos and SOPs, without the busywork.", "color": "#8A6A2E"},
    {"key": "learning", "code": "LN", "slug": "learning", "name": "Learning & Exam Prep",
     "blurb": "Tutors, active recall, exam prep and interview practice.", "color": "#7A4E8A"},
    {"key": "marketing", "code": "MK", "slug": "marketing", "name": "Marketing",
     "blurb": "Customer research, positioning, SEO, landing pages, launches.", "color": "#C4562A"},
    {"key": "product", "code": "PD", "slug": "product", "name": "Product Management",
     "blurb": "Discovery, PRDs, specs and critiques, grounded in user research.", "color": "#2E7A6E"},
    {"key": "skill-engineering", "code": "SE", "slug": "skill-engineering", "name": "Build Your Own Skills",
     "blurb": "Write, review and test your own skills.", "color": "#5A5A5A"},
]
FIELD_BY_KEY = {f["key"]: f for f in FIELDS}
ALL_PLUGIN = "research-skills"

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


def load_yaml(name):
    p = ROOT / "data" / name
    return (yaml.safe_load(p.read_text(encoding="utf-8")) or {}) if p.exists() else {}


def parse_readme(text):
    lines = [l.strip() for l in text.splitlines()]
    out = {"tagline": "", "summary": "", "give": "", "get": "", "method": "", "terms": ""}
    if lines:
        m = re.match(r"#\s*[^:]+:\s*(.+)", lines[0])
        out["tagline"] = m.group(1).strip() if m else ""
        out["summary"] = next((l for l in lines[1:] if l and not l.startswith(("#", "|"))), "")
    keys = {"You give it": "give", "You get back": "get", "Method": "method", "Search terms": "terms"}
    for l in lines:
        row = re.match(r"\|\s*\*\*(You give it|You get back|Method|Search terms)\*\*\s*\|\s*(.+?)\s*\|$", l)
        if row:
            out[keys[row.group(1)]] = row.group(2)
    clean = lambda s: re.sub(r"[*_`]", "", re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s))
    return {k: clean(v) for k, v in out.items()}


def load_skills(site):
    order = site.get("order", [])
    skills = []
    for skill_md in sorted(SKILLS_DIR.glob("skills/*/*/SKILL.md")):
        folder = skill_md.parent
        key = folder.parent.name
        if key not in FIELD_BY_KEY:
            continue
        meta, body = read_frontmatter(skill_md.read_text(encoding="utf-8"))
        readme = (folder / "README.md").read_text(encoding="utf-8") if (folder / "README.md").exists() else ""
        info = parse_readme(readme)
        skills.append(dict(info, **{
            "name": meta.get("name", folder.name), "field": FIELD_BY_KEY[key],
            "description": meta.get("description", ""), "body": body,
            "github": f"https://github.com/{REPO}/tree/main/skills/{key}/{folder.name}",
            "zip": f"https://github.com/{REPO}/raw/main/dist/{folder.name}.zip",
            "plugin": site.get("plugins", {}).get(key, ALL_PLUGIN), "access": "free",
        }))
    rank = lambda s: order.index(s["name"]) if s["name"] in order else len(order)
    keys = [f["key"] for f in FIELDS]
    skills.sort(key=lambda s: (keys.index(s["field"]["key"]), rank(s), s["name"]))
    counters = {}
    for s in skills:
        c = s["field"]["code"]
        counters[c] = counters.get(c, 0) + 1
        s["call"] = f"{c}-{counters[c]:02d}"
    return skills


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


def load_resources(site):
    """Articles live in content/resources/<column>/<NN>-<slug>.md. Columns come from site.yaml."""
    cols = [c["key"] for c in site.get("resource_columns", [])]
    items = []
    for p in sorted((ROOT / "content" / "resources").rglob("*.md")):
        meta, body = read_frontmatter(p.read_text(encoding="utf-8"))
        meta["slug"] = p.stem.split("-", 1)[1] if re.match(r"\d+-", p.stem) else p.stem
        meta.setdefault("column", p.parent.name if p.parent.name != "resources" else "skill-workshop")
        # private review notes for Grace never reach the page
        meta["body"] = re.sub(r"<!--\s*Notes for Grace.*?-->", "", body, flags=re.S)
        items.append(meta)
    col_rank = lambda r: cols.index(r["column"]) if r["column"] in cols else len(cols)
    items.sort(key=lambda r: (col_rank(r), r.get("order", 99)))
    slugs = [r["slug"] for r in items]
    dupes = {s for s in slugs if slugs.count(s) > 1}
    if dupes:
        raise SystemExit(f"Duplicate article slugs: {dupes}")
    return items


def fmt_date(d):
    if not d:
        return ""
    try:
        return dt.date.fromisoformat(d).strftime("%b %-d, %Y")
    except ValueError:
        return d


# ─────────────────────────── shared pieces ───────────────────────────

NAV = [("", "Home"), ("skills/", "Catalog"), ("insights/", "Insights"), ("resources/", "Skill Workshop"), ("pro/", "Pro"), ("about/", "About")]


def lamp(site):
    """Pull-cord feedback lamp, on every page."""
    gf = site.get("google_form") or {}
    gf_attr = e(json.dumps(gf)) if gf.get("action") else ""
    return f"""<div class="lamp" id="lamp" data-endpoint="{e(site.get('form_endpoint', ''))}" data-gform="{gf_attr}">
  <div class="lamp-wire" aria-hidden="true"></div>
  <div class="lamp-shade" aria-hidden="true"><span class="lamp-bulb"></span></div>
  <button class="lamp-cord" id="lampCord" aria-expanded="false" aria-controls="lampPanel" title="Pull for feedback"><span class="lamp-string"></span><span class="lamp-knob"></span><span class="lamp-label">feedback</span></button>
  <div class="lamp-glow" aria-hidden="true"></div>
  <form class="lamp-panel" id="lampPanel" hidden data-form="feedback">
    <p class="lamp-title">Tell me what you think</p>
    <p class="lamp-sub">What's useful, what's confusing, what's missing. It comes straight to me.</p>
    <label class="sr-only" for="fbMsg">Your feedback</label>
    <textarea id="fbMsg" name="message" rows="4" required placeholder="This page / skill would be better if…"></textarea>
    <label class="sr-only" for="fbEmail">Email (optional)</label>
    <input id="fbEmail" name="email" type="email" placeholder="Email, if you'd like a reply (optional)">
    <button class="btn btn-ink" type="submit">Send it my way 💌</button>
    <p class="form-note" role="status"></p>
  </form>
</div>"""


def envelope():
    return """<div class="envelope" aria-hidden="true"><div class="env-back"></div><div class="env-letter"></div><div class="env-front"></div><div class="env-flap"></div></div>"""


def page(path, title, description, body, site, active="", extra_head=""):
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
<link rel="icon" type="image/png" href="{url('assets/grace-cat-64.png')}">
<link rel="apple-touch-icon" href="{url('assets/grace-cat.png')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{url('assets/style.css')}">
{extra_head}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <a class="brand" href="{url()}"><span class="brand-mark" aria-hidden="true"></span><span>grace's <em>skill library</em></span></a>
  <nav class="nav" aria-label="Main">{nav}<a class="nav-out" href="{PERSONAL_SITE}">Grace ↗</a></nav>
</header>
{lamp(site)}
<main id="main">
{body}
</main>
<footer class="foot">
  <div class="foot-cols">
    <div><div class="foot-brand">grace's <em>skill library</em></div><p>Claude skills that package the method inside your work. Free and open source.</p></div>
    <div><b>Library</b><a href="{url('skills/')}">Catalog</a><a href="{url('insights/')}">Insights</a><a href="{url('resources/')}">Skill Workshop</a><a href="{url('pro/')}">Pro</a></div>
    <div><b>Elsewhere</b><a href="{PERSONAL_SITE}">Personal site</a><a href="https://github.com/{REPO}">GitHub</a><a href="{NEWSLETTER_URL}">Newsletter</a></div>
    <div><b>Help</b><a href="{url('pro/#faq')}">FAQ</a><a href="{url('pro/#refunds')}">Refunds</a><a href="{url('skills/#request')}">Request a skill</a></div>
  </div>
  <p class="foot-note">© {dt.date.today().year} Linge (Grace) Guo · Free skills are open source under the MIT license · <a href="https://github.com/{REPO}">{REPO}</a></p>
</footer>
<script src="{url('assets/app.js')}" defer></script>
</body>
</html>
"""


def card(s, compact=False):
    f = s["field"]
    stamp = '<span class="stamp stamp-free">Free</span>' if s["access"] == "free" else '<span class="stamp stamp-pro">Pro</span>'
    return f"""<a class="card" href="{url('skills/' + s['name'] + '/')}" data-field="{f['slug']}" data-name="{e(s['name'])}" style="--c:{f['color']}">
  <span class="card-hole" aria-hidden="true"></span>
  <span class="card-top"><span class="call">{s['call']}</span><span class="card-field">{e(f['name'])}</span>{stamp}</span>
  <span class="card-title">{e(s['name'])}</span>
  <span class="card-tag">{e(s['tagline'])}</span>
  {'' if compact else f'<span class="card-sum">{e(s["summary"])}</span>'}
  <span class="card-lines"><span><b>Input</b>{e(s['give'])}</span><span><b>Output</b>{e(s['get'])}</span></span>
</a>"""


def request_form(prefill_label="What skill do you wish existed?"):
    return f"""<form class="request" id="request" data-form="request">
  <div class="request-paper">
    <p class="eyebrow">Request a skill</p>
    <h2>Can't find it? Ask for it.</h2>
    <p class="muted">Describe the task you want help with. Your request comes straight to me.</p>
    <label class="sr-only" for="reqMsg">{e(prefill_label)}</label>
    <textarea id="reqMsg" name="message" rows="3" required placeholder="e.g. Turn my lecture notes into exam questions…"></textarea>
    <label class="sr-only" for="reqEmail">Email (optional)</label>
    <input id="reqEmail" name="email" type="email" placeholder="Email, if you'd like to hear when it's ready (optional)">
    <button class="btn btn-accent" type="submit">Send request</button>
    <p class="form-note" role="status"></p>
  </div>
  {envelope()}
</form>"""


def install_block(s):
    return f"""<div class="install">
  <div class="install-tabs" role="tablist">
    <button role="tab" aria-selected="true" data-tab="cc">Claude Code</button>
    <button role="tab" aria-selected="false" data-tab="web">Claude.ai / desktop</button>
    <button role="tab" aria-selected="false" data-tab="manual">Manual</button>
  </div>
  <div class="install-pane" data-pane="cc">
    <p>Add the library once, then install this folder ({e(s['field']['name'])}):</p>
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


def search_index(skills):
    rows = [{"n": s["name"], "t": s["tagline"], "s": s["summary"], "g": s["give"], "o": s["get"], "m": s["method"],
             "k": s["terms"], "f": s["field"]["name"]} for s in skills]
    return '<script type="application/json" id="skill-index">' + json.dumps(rows, ensure_ascii=False).replace("</", "<\\/") + "</script>"


# ─────────────────────────── pages ───────────────────────────

def build_home(skills, issues, resources, site):
    by_name = {s["name"]: s for s in skills}
    # hero card stack
    stack = [by_name[n] for n in site.get("hero_stack", []) if n in by_name][:6]
    stack_html = "".join(f"""<div class="scard" style="--c:{s['field']['color']}" data-href="{url('skills/' + s['name'] + '/')}">
  <span class="card-top"><span class="call">{s['call']}</span><span class="card-field">{e(s['field']['name'])}</span><span class="stamp stamp-free">Free</span></span>
  <span class="scard-title">{e(s['name'])}</span><span class="scard-tag">{e(s['tagline'])}</span>
  <span class="scard-line"><b>Input</b>{e(s['give'])}</span><span class="scard-line"><b>Output</b>{e(s['get'])}</span>
  <a class="scard-open" href="{url('skills/' + s['name'] + '/')}">Open this card →</a>
</div>""" for s in stack)
    # personas
    personas = site.get("personas", [])
    def heading(p):
        h = p.get("heading") or ["I'm a", p["label"]]
        return h[0], h[1]
    p_chips = "".join(
        '<button class="who-chip" data-who="%d" data-pre="%s" data-word="%s" aria-pressed="%s">%s</button>'
        % (i, e(heading(p)[0]), e(heading(p)[1]), "true" if i == 0 else "false", e(p["label"]))
        for i, p in enumerate(personas))
    h0 = heading(personas[0]) if personas else ("I'm a", "…")
    p_groups = ""
    for i, p in enumerate(personas):
        items = [by_name[n] for n in p.get("skills", []) if n in by_name][:6]
        line_html = ('<p class="who-line">' + e(p["line"]) + '</p>') if p.get("line") else ""
        p_groups += f'<div class="who-group" data-who-group="{i}"{"" if i == 0 else " hidden"}>{line_html}<div class="cards cards-3">{"".join(card(s, compact=True) for s in items)}</div></div>'
    # folders: one tab per type of work, its skills as sheets inside
    tabs_html, panels = "", ""
    first = True
    for f in FIELDS:
        items = [s for s in skills if s["field"]["key"] == f["key"]]
        if not items:
            continue
        tabs_html += f"""<button class="ftab" role="tab" id="ftab-{f['slug']}" aria-controls="fpanel-{f['slug']}" aria-selected="{'true' if first else 'false'}" tabindex="{'0' if first else '-1'}" data-folder="{f['slug']}" style="--c:{f['color']}"><span class="ftab-code">{f['code']}</span><span class="ftab-name">{e(f['name'])}</span><span class="ftab-n">{len(items)}</span></button>"""
        sheets = "".join(f"""<a class="sheet" href="{url('skills/' + s['name'] + '/')}" style="--i:{i}"><span class="sheet-call">{s['call']}</span><span class="sheet-name">{e(s['name'])}</span><span class="sheet-tag">{e(s['tagline'])}</span><span class="sheet-give"><b>Give</b> {e(s['give'])}</span></a>""" for i, s in enumerate(items))
        panels += f"""<div class="folder" role="tabpanel" id="fpanel-{f['slug']}" aria-labelledby="ftab-{f['slug']}" data-panel="{f['slug']}" style="--c:{f['color']}"{'' if first else ' hidden'}>
  <div class="folder-head"><div><h3>{e(f['name'])}</h3><p>{e(f['blurb'])}</p></div><a class="btn btn-line" href="{url('skills/?field=' + f['slug'])}">Open in the catalog</a></div>
  <div class="sheets">{sheets}</div>
</div>"""
        first = False
    methods = site.get("methods", [])
    method_chips = "".join(f"<span>{e(m)}</span>" for m in methods)
    latest = "".join(f"""<li><a href="{e(i['url'])}" target="_blank" rel="noopener"><span class="ins-date">{fmt_date(i.get('date'))}</span><span class="ins-title">{e(i['title'])}</span><span class="ins-arrow">↗</span></a></li>""" for i in issues[:3])
    lessons = "".join(f"""<a class="lesson" href="{url('resources/' + r['slug'] + '/')}"><span class="lesson-no">{e(r.get('time', ''))}</span><span class="lesson-title">{e(r['title'])}</span></a>""" for r in [x for x in resources if x['column'] in ('skill-workshop', 'how-skills-work')][:4])
    body = f"""
<section class="hero">
  <div class="hero-text">
    <p class="eyebrow">Claude skills for research, writing and everyday work</p>
    <h1>AI is good at output.<br><em>But input is the work.</em></h1>
    <p class="lede">These skills don't automate your job. They package the work inside it: the right questions to ask first, a proven method to follow, and evidence for every claim.</p>
    <div class="hero-cta"><a class="btn btn-ink" href="#who">Find skills for me</a><a class="btn btn-line" href="{url('skills/')}">See the whole catalog</a></div>
  </div>
  <div class="hero-stack" id="stack" aria-label="Sample skill cards. Swipe a card up to see the next one.">
    <div class="stack-cards">{stack_html}</div>
    <div class="stack-hint" aria-hidden="true"><span class="hint-hand">☝</span><span>Swipe a card up</span></div>
    <button class="stack-next" type="button">Next card ↑</button>
  </div>
</section>

<section class="block" id="who">
  <p class="eyebrow">Start from who you are</p>
  <div class="block-head"><h2 class="who-head" aria-live="polite"><span class="who-pre">{e(h0[0])}</span> <span class="who-word">{e(h0[1])}</span><span class="who-caret" aria-hidden="true"></span></h2></div>
  <div class="who-chips" role="group" aria-label="Choose who you are">{p_chips}</div>
  {p_groups}
</section>

<section class="block">
  <a class="cat-cta" href="{url('skills/')}" aria-label="Open the whole catalog">
    <span class="cta-text">
      <span class="eyebrow">Or browse by type of work</span>
      <span class="cta-title">Every skill, filed by field</span>
      <span class="cta-fields">{' · '.join(e(f['name']) for f in FIELDS)}</span>
    </span>
    <span class="cat-click"><span class="bubble">Click me!</span><img src="{url('assets/grace-cat-cutout-480.png')}" alt="" width="120" height="183"></span>
  </a>
</section>

<section class="block principles">
  <div class="block-head"><h2>Built on the same principles</h2></div>
  <ol class="how-steps">
    <li><b>Grounded in real methods.</b><span>Each skill encodes a named method from research, editing, learning science or product practice, not vague "best practices".</span></li>
    <li><b>Input first.</b><span>It starts from what you already have, and asks your goal, audience and constraints before writing, with sensible defaults.</span></li>
    <li><b>Steps you can check.</b><span>Every step says when it's done, and the result follows a fixed template you can reuse.</span></li>
    <li><b>Evidence, not guesses.</b><span>Claims point back to your material, or are labeled as assumptions. Nothing is invented.</span></li>
  </ol>
</section>

<section class="block duo">
  <div class="duo-col">
    <p class="eyebrow">Reading room</p>
    <div class="block-head"><h2>Insights</h2><a href="{url('insights/')}">All insights →</a></div>
    <p class="muted">Essays from my newsletter, <em>Signals Across Markets</em>, on AI, society and markets.</p>
    <ul class="ins-list">{latest}</ul>
  </div>
  <div class="duo-col">
    <p class="eyebrow">Skill Workshop</p>
    <div class="block-head"><h2>Write your own skill</h2><a href="{url('resources/')}">All lessons →</a></div>
    <p class="muted">How to create skills that actually work, plus my LLM notebook and reading notes.</p>
    <div class="lessons">{lessons}</div>
  </div>
</section>

<section class="block pro-teaser">
  <div><p class="eyebrow">Pro &amp; custom skills</p><h2>Need a skill built around your own work?</h2><p>Pro skills run whole workflows end to end. Or I can build one around your team's process.</p></div>
  <a class="btn btn-accent" href="{url('pro/')}">See Pro</a>
</section>
"""
    return page("", "Grace's Skill Library · Claude skills for research, writing and everyday work",
                f"{len(skills)} free Claude skills for students and professionals: deep research, literature reviews, writing in your own voice, meeting actions, decision memos, learning and exam practice, marketing and product work.",
                body, site)


def build_catalog(skills, site):
    chips = "".join(f'<button class="chip" data-filter-field="{f["slug"]}" aria-pressed="false" style="--c:{f["color"]}">{e(f["name"])}</button>' for f in FIELDS if any(s["field"]["key"] == f["key"] for s in skills))
    sections = ""
    for f in FIELDS:
        items = [s for s in skills if s["field"]["key"] == f["key"]]
        if not items:
            continue
        sections += f"""<section class="drawer-section" data-section="{f['slug']}">
  <div class="drawer-label" style="--c:{f['color']}"><span class="drawer-code">{f['code']}</span><h2>{e(f['name'])}</h2><span class="muted">{e(f['blurb'])}</span></div>
  <div class="cards">{''.join(card(s) for s in items)}</div>
</section>"""
    body = f"""
<section class="page-head">
  <p class="eyebrow">The catalog</p>
  <h1>Filed by field.</h1>
  <p class="lede">Every card shows the input it needs and the output you get. Search in your own words, in English or Chinese.</p>
</section>
<div class="filters">
  <label class="search"><span class="sr-only">Search skills</span><input id="q" type="search" placeholder="What do you need help with? e.g. sociological interviews, 周报, IELTS essay…" autocomplete="off"></label>
  <div class="chips"><button class="chip" data-filter-field="all" aria-pressed="true">All</button>{chips}</div>
</div>
<section class="results" id="results" hidden><div class="results-head"><h2 id="resultsTitle">Best matches</h2></div><div class="cards" id="resultsCards"></div></section>
{sections}
<section class="block" id="requestWrap">{request_form()}</section>
{search_index(skills)}
"""
    return page("skills/", "Skill catalog · Grace's Skill Library",
                "Browse free Claude skills by field: research, writing, work documents, learning and exam practice, marketing, product and skill engineering.",
                body, site, active="skills/")


def build_skill(s, skills, site):
    related = [x for x in skills if x["field"]["key"] == s["field"]["key"] and x["name"] != s["name"]][:3]
    body = f"""
<nav class="crumbs" aria-label="Breadcrumb"><a href="{url('skills/')}">Catalog</a> / <a href="{url('skills/?field=' + s['field']['slug'])}">{e(s['field']['name'])}</a> / <span>{e(s['name'])}</span></nav>
<article class="skill">
  <header class="skill-card" style="--c:{s['field']['color']}">
    <span class="card-hole" aria-hidden="true"></span>
    <div class="card-top"><span class="call">{s['call']}</span><span class="card-field">{e(s['field']['name'])}</span><span class="stamp stamp-free">Free</span></div>
    <h1>{e(s['name'])}</h1>
    <p class="skill-tag">{e(s['tagline'])}</p>
    <p class="skill-sum">{e(s['summary'])}</p>
    <dl class="skill-lines"><div><dt>Input</dt><dd>{e(s['give'])}</dd></div><div><dt>Output</dt><dd>{e(s['get'])}</dd></div>{f'<div><dt>Method</dt><dd>{e(s["method"])}</dd></div>' if s['method'] else ''}</dl>
    <div class="skill-actions"><a class="btn btn-ink" href="#install">Install</a><a class="btn btn-line" href="{s['github']}">View on GitHub ↗</a></div>
  </header>
  <section id="install" class="skill-sec"><h2>Install</h2>{install_block(s)}</section>
  <section class="skill-sec"><h2>The full instructions</h2><p class="muted">This is exactly what Claude reads. Nothing hidden.</p><div class="prose skill-md">{md(s['body'])}</div></section>
  {f'<section class="skill-sec"><h2>Search terms</h2><p class="muted">{e(s["terms"])}</p></section>' if s['terms'] else ''}
  {f'<section class="skill-sec"><h2>In the same folder</h2><div class="cards cards-3">{"".join(card(r, compact=True) for r in related)}</div></section>' if related else ''}
</article>
"""
    return page(f"skills/{s['name']}/", f"{s['name']}: {s['tagline']} · Claude skill",
                (s["summary"] + " Free Claude skill for Claude Code and Claude.ai.")[:300], body, site, active="skills/")


def cache_covers(issues):
    """Download each issue's cover into the site so we never depend on LinkedIn's image links."""
    import hashlib
    d = OUT / "assets" / "covers"
    d.mkdir(parents=True, exist_ok=True)
    for i in issues:
        src = i.get("cover")
        if not src:
            continue
        name = hashlib.sha1(src.split("?")[0].encode()).hexdigest()[:16] + ".jpg"
        try:
            req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130 Safari/537.36"})
            with urllib.request.urlopen(req, timeout=20) as r:
                (d / name).write_bytes(r.read())
            i["cover"] = url("assets/covers/" + name)
        except Exception as ex:
            print(f"cover: keeping remote link ({ex})")


def build_insights(issues, site):
    def cover(i, cls="ins-cover"):
        return f'<img class="{cls}" src="{e(i["cover"])}" alt="" loading="lazy" referrerpolicy="no-referrer">' if i.get("cover") else f'<span class="{cls} ins-cover-empty"></span>'
    lead = issues[0] if issues else None
    lead_html = f"""<a class="ins-feature" href="{e(lead['url'])}" target="_blank" rel="noopener">{cover(lead, 'ins-feature-img')}<span class="ins-feature-text"><span class="eyebrow">Latest issue · {fmt_date(lead.get('date'))}</span><span class="ins-feature-title">{e(lead['title'])}</span><span class="ins-read">Read on LinkedIn ↗</span></span></a>""" if lead else '<p class="muted">New issues appear here automatically.</p>'
    grid = "".join(f"""<a class="ins-card" href="{e(i['url'])}" target="_blank" rel="noopener">{cover(i)}<span class="ins-card-body"><span class="ins-date">{fmt_date(i.get('date'))}</span><span class="ins-card-title">{e(i['title'])}</span></span></a>""" for i in issues[1:])
    body = f"""
<section class="page-head nl-head">
  <img class="nl-logo" src="{url('assets/signals-cat.png')}" alt="A sleeping calico cat, the mascot of Signals Across Markets" width="207" height="110">
  <div>
    <p class="eyebrow">Insights · from my LinkedIn newsletter</p>
    <h1>Signals Across Markets</h1>
    <p class="lede">One signal a week, from AI, technology, society or the economy, and what it means for the people living through it. Written by <a href="{url('about/')}">Linge (Grace) Guo</a>, a sociologist who studies how AI reshapes work and everyday life. New issues appear here automatically.</p>
  </div>
</section>
<section class="block">{lead_html}</section>
<section class="block"><div class="block-head"><h2>Earlier issues</h2><a href="{NEWSLETTER_URL}" target="_blank" rel="noopener">Every issue on LinkedIn ↗</a></div><div class="ins-grid">{grid}</div></section>
"""
    return page("insights/", "Signals Across Markets · Insights · Grace's Skill Library",
                "Signals Across Markets: Linge (Grace) Guo's weekly LinkedIn newsletter on AI, society and markets, mirrored here.",
                body, site, active="insights/")


def article_card(r, big=True):
    draft = '<span class="draft-chip">Draft</span>' if r.get("status") == "draft" else ""
    return f"""<a class="lesson{' lesson-big' if big else ''}" href="{url('resources/' + r['slug'] + '/')}"><span class="lesson-no">{e(r.get('time', ''))}{draft}</span><span class="lesson-title">{e(r['title'])}</span><span class="lesson-sum">{e(r.get('summary', ''))}</span></a>"""


def build_resources(resources, site):
    columns = [c for c in site.get("resource_columns", []) if any(r["column"] == c["key"] for r in resources)]
    nav = "".join((f'<span class="guide-wrap"><span class="guide-tip" aria-hidden="true">Start here ↓</span><a class="col-chip col-chip-guide" href="#{c["key"]}">{e(c["name"])}</a></span>' if c["key"] == "how-skills-work" else f'<a class="col-chip" href="#{c["key"]}">{e(c["name"])}</a>') for c in columns)
    sections = ""
    for c in columns:
        items = [r for r in resources if r["column"] == c["key"]]
        series_order = c.get("series", [])
        groups = {}
        for r in items:
            groups.setdefault(r.get("series", ""), []).append(r)
        keys = sorted(groups, key=lambda s: series_order.index(s) if s in series_order else (len(series_order) if s else -1))
        inner = ""
        for s in keys:
            head = f'<h3 class="series-title">{e(s)}</h3>' if s else ""
            inner += f'{head}<div class="lessons lessons-grid">{"".join(article_card(r) for r in groups[s])}</div>'
        sections += f"""<section class="block col-section" id="{c['key']}">
  <p class="eyebrow">{e(c.get('kicker', ''))}</p>
  <div class="block-head"><h2>{e(c['name'])}</h2><span class="muted">{len(items)} articles</span></div>
  <p class="muted col-blurb">{e(c.get('blurb', ''))}</p>
  {inner}
</section>"""
    upcoming = "".join(f"<li>{e(t)}</li>" for t in site.get("upcoming_lessons", []))
    body = f"""
<section class="page-head">
  <p class="eyebrow">Skill Workshop</p>
  <h1>How to create skills that actually work</h1>
  <p class="lede">Everything I've learned about building with AI, in one place: step-by-step lessons on creating Claude skills, what happens inside Claude when a skill runs, my LLM notebook (how models predict, train, align and get evaluated, plus Google's ML Crash Course), reading notes on AI, startups and growth, and short, sourced summaries of AI governance.</p>
  <nav class="col-nav" aria-label="Sections">{nav}</nav>
</section>
{sections}
{f'<section class="block"><div class="block-head"><h2>Coming next</h2></div><ul class="upcoming">{upcoming}</ul></section>' if upcoming else ''}
<section class="block">
  <div class="block-head"><h2>Further reading</h2></div>
  <a class="ins-lead" href="https://www.linkedin.com/pulse/i-turned-my-research-workflow-ai-skill-linge-guo-hezfc" target="_blank" rel="noopener"><span class="eyebrow">Essay · Oct 14, 2026</span><span class="ins-lead-title">I Turned My Research Workflow into an AI Skill</span><span class="muted">How a sociologist's research routine became a reusable skill, and what changed along the way.</span><span class="btn btn-line">Read on LinkedIn ↗</span></a>
</section>
"""
    return page("resources/", "Skill Workshop: learn to write Claude skills · Grace's Skill Library",
                "Step-by-step lessons on writing Claude skills (SKILL.md) that improve your work: anatomy, a worked example, naming for discovery, and testing.",
                body, site, active="resources/")


def build_lesson(r, resources, site):
    col = next((c for c in site.get("resource_columns", []) if c["key"] == r["column"]), {"key": r["column"], "name": r["column"]})
    same = [x for x in resources if x["column"] == r["column"]]
    i = same.index(r)
    prev_l = same[i - 1] if i > 0 else None
    next_l = same[i + 1] if i + 1 < len(same) else None
    pager = '<nav class="pager">' + (f'<a href="{url("resources/" + prev_l["slug"] + "/")}">← {e(prev_l["title"])}</a>' if prev_l else "<span></span>") + (f'<a href="{url("resources/" + next_l["slug"] + "/")}">{e(next_l["title"])} →</a>' if next_l else "") + "</nav>"
    series = f" · {e(r['series'])}" if r.get("series") else ""
    draft = '<p class="draft-note">Draft: this article is still being reviewed.</p>' if r.get("status") == "draft" else ""
    body = f"""
<nav class="crumbs" aria-label="Breadcrumb"><a href="{url('resources/')}">Skill Workshop</a> / <a href="{url('resources/#' + col['key'])}">{e(col['name'])}</a>{(' / <span>' + e(r['series']) + '</span>') if r.get('series') else ''}</nav>
<article class="lesson-page">
  <header><p class="eyebrow">{e(col['name'])}{series} · {e(r.get('time', ''))}</p><h1>{e(r['title'])}</h1><p class="lede">{e(r.get('summary', ''))}</p>{draft}</header>
  <div class="prose">{md(r['body'])}</div>
  {pager}
</article>
"""
    return page(f"resources/{r['slug']}/", f"{r['title']} · Skill Workshop", r.get("summary", "")[:300], body, site, active="resources/")


def build_pro(pro, site):
    def plan(p):
        if p.get("checkout_url"):
            cta = f'<a class="btn btn-ink" href="{e(p["checkout_url"])}">{e(p.get("cta", "Buy"))}</a>'
        elif p.get("form"):
            cta = f'<button class="btn btn-accent" type="button" data-open-form="consult">{e(p.get("cta", "Get in touch"))}</button>'
        else:
            cta = f'<button class="btn btn-line" type="button" data-open-form="waitlist" data-plan="{e(p["name"])}">Join the waitlist</button>'
        guide = '<span class="plan-guide" aria-hidden="true">Need something specific? ↓</span>' if p.get("form") else ""
        return f"""<div class="plan{' plan-hi' if p.get('highlight') else ''}{' plan-custom' if p.get('form') else ''}">{guide}
  <p class="eyebrow">{e(p['name'])}</p><p class="price">{e(p['price'])}</p><p class="muted">{e(p.get('note', ''))}</p>
  <ul>{''.join(f'<li>{e(x)}</li>' for x in p.get('includes', []))}</ul>{cta}</div>"""
    skills_html = "".join(f"""<div class="card card-static"><span class="corner-badge">In Library Pass</span><span class="card-hole" aria-hidden="true"></span><span class="card-top"><span class="call">SC-{n:02d}</span><span class="card-field">{e(x.get('field', ''))}</span><span class="stamp stamp-pro">{e(x.get('status', 'Coming soon'))}</span></span><span class="card-title">{e(x['name'])}</span><span class="card-tag">{e(x.get('tagline', ''))}</span><span class="card-sum">{e(x.get('summary', ''))}</span>{f'<span class="card-stages">{e(x["stages"])}</span>' if x.get('stages') else ''}</div>""" for n, x in enumerate(pro.get("skills", []), 1))
    faq = "".join(f"<details><summary>{e(q['q'])}</summary><p>{e(q['a'])}</p></details>" for q in pro.get("faq", []))
    body = f"""
<section class="page-head">
  <p class="eyebrow">Special collections</p>
  <h1>Pro</h1>
  <div class="pro-intro">{''.join(f'<p>{e(x)}</p>' for x in (pro.get('intro') or '').split(chr(10)+chr(10)) if x.strip())}</div>
</section>
<section class="block"><div class="plans">{''.join(plan(p) for p in pro.get('plans', []))}</div></section>
{f'<section class="block"><div class="block-head"><h2>In the special collection <span class="h-note">Whole workflows, end to end</span></h2></div><div class="cards cards-3">{skills_html}</div></section>' if skills_html else ''}
<section class="block" id="consult">
  <form class="request" data-form="consult">
    <div class="request-paper">
      <p class="eyebrow">Custom skill</p>
      <h2>Tell me about the work you want packaged.</h2>
      <p class="muted">What's the job, what do you start from, and what do you need to hand in? I'll reply with how I'd build it.</p>
      <textarea name="message" rows="4" required placeholder="e.g. Every month we turn 30 customer interviews into a product insights report…"></textarea>
      <input name="email" type="email" required placeholder="Your email">
      <button class="btn btn-accent" type="submit">Send</button>
      <p class="form-note" role="status"></p>
    </div>
    {envelope()}
  </form>
</section>
<section class="block" id="faq"><div class="block-head"><h2>Questions</h2></div><div class="faq">{faq}</div></section>
<section class="block" id="refunds"><div class="block-head"><h2>Refunds</h2></div><p>{e(pro.get('refunds', ''))}</p></section>
"""
    return page("pro/", "Pro & custom skills · Grace's Skill Library",
                "Pro Claude skills that run whole workflows end to end, and custom skills built around your team's work.",
                body, site, active="pro/")


def build_about(skills, site):
    body = f"""
<section class="page-head about-head">
  <div>
    <p class="eyebrow">About the librarian</p>
    <h1>Hi, I'm Grace.</h1>
    <p class="lede">I'm a sociologist (UCL; MSc Sociology, Oxford) who studies how AI and digital technologies reshape the way we know, work and live.</p>
    <div class="hero-cta"><a class="btn btn-boba" href="{LINKEDIN}">Connect with me on LinkedIn</a><a class="btn btn-line" href="{PERSONAL_SITE}">Visit my personal site ↗</a></div>
  </div>
  <img class="about-cat" src="{url('assets/grace-cat-cutout-480.png')}" alt="Grace's avatar: a calico cat drinking bubble tea" width="300" height="457">
</section>
<section class="block prose about">
  <p>This library started with my own research workflow. I turned the way I do research into a Claude skill, and kept going. Every skill here packages a method I trust: Braun &amp; Clarke for thematic analysis, the Minto Pyramid for executive writing, retrieval practice for learning, Feature → Advantage → Benefit for product value.</p>
  <p>The idea behind all of them: <strong>AI is good at output, but input is the work.</strong> A good result depends on asking the right questions first and following a real method. So the skills ask before they write, work in steps you can check, and never invent a citation, a number or a customer.</p>
  <p>They're for students and for people at work. Most are free; Pro skills run whole workflows end to end, and I build custom skills for teams.</p>
</section>
"""
    return page("about/", "About · Grace's Skill Library", "About Linge (Grace) Guo, the sociologist behind Grace's Skill Library.", body, site, active="about/")


def build_404(site):
    body = f"""<section class="page-head"><img class="lost-cat" src="{url('assets/grace-cat.png')}" alt="" width="160" height="160"><p class="eyebrow">Card not found</p><h1>This card isn't in the catalog.</h1><p class="lede">It may have been refiled. Try the <a href="{url('skills/')}">catalog</a>.</p></section>"""
    return page("404.html", "Not found · Grace's Skill Library", "Page not found.", body, site)


# ─────────────────────────── write ───────────────────────────

def write(path, content):
    p = OUT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def main():
    site = load_yaml("site.yaml")
    pro = load_yaml("pro.yaml")
    skills = load_skills(site)
    if not skills:
        raise SystemExit(f"No skills found in {SKILLS_DIR}. Set SKILLS_DIR to a checkout of {REPO}.")
    issues = load_newsletter()
    resources = load_resources(site)
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "assets", OUT / "assets")
    write("index.html", build_home(skills, issues, resources, site))
    write("skills/index.html", build_catalog(skills, site))
    for s in skills:
        write(f"skills/{s['name']}/index.html", build_skill(s, skills, site))
    cache_covers(issues)
    write("insights/index.html", build_insights(issues, site))
    write("resources/index.html", build_resources(resources, site))
    for r in resources:
        write(f"resources/{r['slug']}/index.html", build_lesson(r, resources, site))
    write("pro/index.html", build_pro(pro, site))
    write("about/index.html", build_about(skills, site))
    write("404.html", build_404(site))
    write("skills.json", json.dumps([dict({k: s[k] for k in ("name", "call", "tagline", "summary", "give", "get", "method", "github", "zip", "access")}, field=s["field"]["name"]) for s in skills], ensure_ascii=False, indent=2))
    pages = ["", "skills/", "insights/", "resources/", "pro/", "about/"] + [f"skills/{s['name']}/" for s in skills] + [f"resources/{r['slug']}/" for r in resources]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE_URL}/{p}</loc></url>\n" for p in pages) + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    print(f"Built {len(pages)} pages: {len(skills)} skills, {len(issues)} insights, {len(resources)} lessons → {OUT}")


if __name__ == "__main__":
    main()
