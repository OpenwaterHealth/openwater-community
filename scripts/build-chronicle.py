#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from typing import Dict, List
from urllib.parse import quote
from xml.sax.saxutils import escape as xml_escape

BASE_URL = "https://openwaterhealth.github.io/openwater-community"
SITE_TITLE = "Openwater Community Garden Chronicle"
TAGLINE = "What took root. What grew. What needs tending."
DEFAULT_HERO = "/openwater-community/assets/chronicle/community-garden-chronicle.png"

REQUIRED_FIELDS = {
    "issue", "date", "title", "subject",
    "summary", "status", "hero_image"
}

CSS = """
:root {
  --deep-navy:#0A2540; --ocean-blue:#164E63; --teal:#0891B2;
  --cyan:#06B6D4; --aqua:#22D3EE; --light:#F0F9FF;
  --text:#0F172A; --muted:#64748B; --border:#E0F2FE;
  --garden:#F7FAF4; --white:#FFFFFF;
}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;
line-height:1.65;color:var(--text);background:var(--white)}
a{color:var(--teal)}
a:hover{color:var(--ocean-blue)}
header{border-bottom:1px solid var(--border);background:rgba(255,255,255,.97)}
.nav{max-width:1120px;margin:auto;padding:14px 22px;display:flex;align-items:center;gap:22px}
.nav img{height:30px;display:block}
.nav-links{margin-left:auto;display:flex;align-items:center;gap:18px;flex-wrap:wrap;font-size:.92rem}
.nav-links>a,.community-menu>summary{text-decoration:none;font-weight:650;color:var(--deep-navy);cursor:pointer}
.community-menu{position:relative}
.community-menu summary{list-style:none}
.community-menu summary::-webkit-details-marker{display:none}
.community-menu summary::after{content:" ▾";font-size:.72em}
.community-menu[open] .community-dropdown{
  position:absolute;top:30px;left:-12px;z-index:100;min-width:260px;
  background:#fff;border:1px solid var(--border);border-radius:10px;
  box-shadow:0 14px 40px rgba(10,37,64,.14);padding:8px
}
.community-dropdown a{
  display:block;padding:10px 12px;border-radius:7px;text-decoration:none;
  color:var(--deep-navy);font-weight:600
}
.community-dropdown a:hover,.community-dropdown a.active{background:var(--light);color:var(--teal)}
.community-dropdown small{display:block;color:var(--muted);font-weight:500;margin-top:2px}
.hero{background:linear-gradient(180deg,var(--garden),#fff)}
.hero-inner{max-width:1120px;margin:auto;padding:56px 22px;display:grid;grid-template-columns:1fr 1fr;gap:44px;align-items:center}
.hero h1,.article h1{color:var(--deep-navy);line-height:1.05;letter-spacing:-.03em}
.hero h1{font-size:clamp(2.5rem,5vw,4.2rem);margin:0 0 14px}
.hero p{font-size:1.13rem;color:#475569}
.hero img,.article img.hero-image{width:100%;border-radius:18px;box-shadow:0 18px 50px rgba(10,37,64,.14)}
.eyebrow{display:inline-block;color:var(--teal);font-weight:800;text-transform:uppercase;letter-spacing:.08em;font-size:.78rem;margin-bottom:10px}
.container{max-width:900px;margin:auto;padding:46px 22px 78px}
.latest,.empty{border:1px solid var(--border);border-radius:16px;padding:28px;margin-bottom:46px}
.latest h2{margin:0 0 6px;color:var(--deep-navy)}
.meta{color:var(--muted);font-size:.9rem;margin-bottom:14px}
.button{display:inline-block;background:var(--teal);color:#fff;text-decoration:none;font-weight:750;padding:10px 16px;border-radius:8px}
.archive{border-top:1px solid var(--border)}
.archive-item{display:grid;grid-template-columns:120px 1fr auto;gap:20px;padding:20px 0;border-bottom:1px solid var(--border)}
.archive-item time{color:var(--muted);font-size:.9rem}
.archive-item h3{margin:0 0 4px;color:var(--deep-navy);font-size:1.08rem}
.archive-item p{margin:0;color:#475569;font-size:.94rem}
.article{max-width:780px;margin:auto;padding:48px 22px 84px}
.article h1{font-size:clamp(2.2rem,5vw,3.5rem);margin-bottom:8px}
.article h2{color:var(--deep-navy);font-size:1.65rem;margin-top:2.5rem}
.article h3{color:var(--ocean-blue);margin-top:1.7rem}
.article p,.article li{font-size:1.03rem}
.article blockquote{border-left:4px solid var(--aqua);padding-left:18px;color:#475569;margin:28px 0}
.article hr{border:0;border-top:1px solid var(--border);margin:38px 0}
.article code{background:#EEF6F8;padding:2px 5px;border-radius:4px}
.back{display:inline-block;margin-bottom:20px;text-decoration:none;font-weight:700}
.draft{background:#FFF6CE;border:1px solid #E7C85D;border-radius:10px;padding:12px 15px;margin:20px 0;font-weight:750;color:#5B4814}
footer{background:var(--deep-navy);color:rgba(255,255,255,.86);padding:32px 22px;font-size:.88rem}
footer .inner{max-width:1120px;margin:auto}
footer a{color:var(--aqua)}
footer p{margin:5px 0}
.disclaimer{color:rgba(255,255,255,.7);margin-top:16px!important;max-width:880px}
@media(max-width:800px){
  .hero-inner{grid-template-columns:1fr}
  .archive-item{grid-template-columns:1fr;gap:4px}
}
"""

@dataclass
class Issue:
    source: Path
    meta: Dict[str, str]
    body: str

    @property
    def number(self) -> int:
        return int(self.meta["issue"])

    @property
    def published(self) -> bool:
        return self.meta["status"].lower() == "published"

    @property
    def date_obj(self) -> datetime:
        return datetime.strptime(self.meta["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)

    @property
    def slug(self) -> str:
        return self.source.stem

    @property
    def url(self) -> str:
        return f"{BASE_URL}/chronicle/{quote(self.slug)}/"

    @property
    def hero_url(self) -> str:
        value = self.meta.get("hero_image", DEFAULT_HERO)
        if value.startswith("http://") or value.startswith("https://"):
            return value
        if value.startswith("/"):
            return "https://openwaterhealth.github.io" + value
        return BASE_URL + "/" + value.lstrip("/")


def parse_issue(path: Path) -> Issue:
    raw = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    if not raw.startswith("---\n"):
        raise ValueError(f"{path}: missing front matter")
    end = raw.find("\n---\n", 4)
    if end == -1:
        raise ValueError(f"{path}: front matter is not closed with ---")

    meta: Dict[str, str] = {}
    for line in raw[4:end].splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, sep, value = line.partition(":")
        if not sep:
            raise ValueError(f"{path}: invalid front matter line: {line}")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        meta[key.strip()] = value

    missing = REQUIRED_FIELDS - set(meta)
    if missing:
        raise ValueError(f"{path}: missing fields: {', '.join(sorted(missing))}")

    if meta["status"].lower() not in {"draft", "published"}:
        raise ValueError(f"{path}: status must be draft or published")

    int(meta["issue"])
    datetime.strptime(meta["date"], "%Y-%m-%d")

    body = raw[end + 5:].strip()
    return Issue(path, meta, body)


def inline_md(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)

    def link_repl(match):
        label = match.group(1)
        url = html.escape(match.group(2), quote=True)
        return f'<a href="{url}">{label}</a>'

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_repl, text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"(?<!_)_([^_]+)_(?!_)", r"<em>\1</em>", text)
    return text


def markdown_to_html(markdown: str) -> str:
    out: List[str] = []
    paragraph: List[str] = []
    list_type = None

    def flush_paragraph():
        nonlocal paragraph
        if paragraph:
            out.append("<p>" + inline_md(" ".join(paragraph)) + "</p>")
            paragraph = []

    def close_list():
        nonlocal list_type
        if list_type:
            out.append(f"</{list_type}>")
            list_type = None

    for raw in markdown.splitlines():
        line = raw.rstrip()
        stripped = line.strip()

        if not stripped:
            flush_paragraph()
            close_list()
            continue

        if stripped == "---":
            flush_paragraph()
            close_list()
            out.append("<hr>")
            continue

        m = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if m:
            flush_paragraph()
            close_list()
            level = len(m.group(1))
            out.append(f"<h{level}>{inline_md(m.group(2))}</h{level}>")
            continue

        if stripped.startswith("> "):
            flush_paragraph()
            close_list()
            out.append(f"<blockquote>{inline_md(stripped[2:])}</blockquote>")
            continue

        m = re.match(r"^[-*]\s+(.+)$", stripped)
        if m:
            flush_paragraph()
            if list_type != "ul":
                close_list()
                out.append("<ul>")
                list_type = "ul"
            out.append(f"<li>{inline_md(m.group(1))}</li>")
            continue

        m = re.match(r"^\d+\.\s+(.+)$", stripped)
        if m:
            flush_paragraph()
            if list_type != "ol":
                close_list()
                out.append("<ol>")
                list_type = "ol"
            out.append(f"<li>{inline_md(m.group(1))}</li>")
            continue

        paragraph.append(stripped)

    flush_paragraph()
    close_list()
    return "\n".join(out)


def navigation() -> str:
    return f"""
<header>
  <nav class="nav" aria-label="Main navigation">
    <a href="{BASE_URL}/"><img src="{BASE_URL}/OpenwaterLogo.png" alt="Openwater"></a>
    <div class="nav-links">
      <a href="{BASE_URL}/">Home</a>
      <a href="{BASE_URL}/developers.html">Developers</a>
      <a href="{BASE_URL}/get-started.html">Get Started</a>

      <details class="community-menu">
        <summary>Community</summary>
        <div class="community-dropdown">
          <a href="{BASE_URL}/community.html">Community Hub</a>
          <a class="active" href="{BASE_URL}/chronicle/">Chronicle</a>
          <a href="{BASE_URL}/licensing.html">
            Licensing
            <small>AGPL core · Apache extensions</small>
          </a>
        </div>
      </details>

      <a href="{BASE_URL}/model-commons.html">Model Commons</a>
      <a href="https://docs.openwater.health/">Docs</a>
    </div>
  </nav>
</header>
"""

def footer() -> str:
    return """
<footer>
  <div class="inner">
    <p><strong>Openwater</strong></p>
    <p>Open Source. Always.</p>
    <p>733 Front Street, Suite C1A, San Francisco, CA 94111</p>
    <p><a href="mailto:community@openwater.health">community@openwater.health</a></p>
    <p>© 2026 Openwater Health. AGPL 3.0 Licensed.</p>
    <p class="disclaimer">Openwater's platform is exclusively intended for research purposes and is not cleared or approved by the FDA for clinical use.</p>
  </div>
</footer>
"""

def shell(title: str, description: str, content: str, extra_head: str = "") -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} | Openwater</title>
<meta name="description" content="{html.escape(description, quote=True)}">
<link rel="alternate" type="application/rss+xml" title="{html.escape(SITE_TITLE)}" href="{BASE_URL}/chronicle/feed.xml">
{extra_head}
<style>{CSS}</style>
</head>
<body>
{navigation()}
{content}
{footer()}
</body>
</html>
"""


def date_label(issue: Issue) -> str:
    d = issue.date_obj
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def build_index(issues: List[Issue], output_dir: Path) -> None:
    if issues:
        latest = issues[0]
        latest_block = f"""
<section class="latest">
  <span class="eyebrow">Latest Issue</span>
  <h2>{html.escape(latest.meta["title"])}</h2>
  <div class="meta">{date_label(latest)} · Issue #{latest.number:03d}</div>
  <p>{html.escape(latest.meta["summary"])}</p>
  <a class="button" href="./{quote(latest.slug)}/">Read the latest Chronicle →</a>
</section>"""
    else:
        latest_block = """
<section class="empty">
  <span class="eyebrow">Coming Soon</span>
  <h2>The first issue is being cultivated.</h2>
  <p>The Chronicle will share what changed, what we learned, and where the community can participate.</p>
</section>"""

    rows = []
    for issue in issues:
        rows.append(f"""
<div class="archive-item">
  <time datetime="{issue.meta['date']}">{issue.date_obj.strftime('%b')} {issue.date_obj.day}, {issue.date_obj.year}</time>
  <div>
    <h3>{html.escape(issue.meta["title"])}</h3>
    <p>{html.escape(issue.meta["summary"])}</p>
  </div>
  <a href="./{quote(issue.slug)}/">Read →</a>
</div>""")
    archive = "\n".join(rows) if rows else "<p>No published issues yet.</p>"

    hero_src = "https://openwaterhealth.github.io" + DEFAULT_HERO
    content = f"""
<section class="hero">
  <div class="hero-inner">
    <div>
      <span class="eyebrow">Openwater Community</span>
      <h1>Community Garden Chronicle</h1>
      <p><strong>{TAGLINE}</strong></p>
      <p>A weekly field note from the people cultivating open-source medical technology.</p>
    </div>
    <img src="{hero_src}" alt="Community Garden Chronicle illustration">
  </div>
</section>
<main class="container">
  {latest_block}
  <span class="eyebrow">Archive</span>
  <h2>From the Garden</h2>
  <div class="archive">{archive}</div>
</main>"""

    (output_dir / "index.html").write_text(
        shell(SITE_TITLE, "Weekly field notes from the Openwater open-source community.", content),
        encoding="utf-8"
    )


def build_issue_page(issue: Issue, output_dir: Path) -> None:
    issue_dir = output_dir / issue.slug
    issue_dir.mkdir(parents=True, exist_ok=True)
    draft_banner = ""
    if not issue.published:
        draft_banner = '<div class="draft">DRAFT PREVIEW — this issue is not published and will not appear in RSS.</div>'

    content = f"""
<main class="article">
  <a class="back" href="../">← Chronicle archive</a>
  <span class="eyebrow">Issue #{issue.number:03d}</span>
  <h1>{html.escape(issue.meta["title"])}</h1>
  <div class="meta">{date_label(issue)} · {html.escape(issue.meta.get("author", "Openwater Community"))}</div>
  {draft_banner}
  <img class="hero-image" src="{html.escape(issue.hero_url, quote=True)}" alt="Community Garden Chronicle illustration">
  {markdown_to_html(issue.body)}
</main>"""

    canonical = f'<link rel="canonical" href="{html.escape(issue.url, quote=True)}">'
    (issue_dir / "index.html").write_text(
        shell(issue.meta["title"], issue.meta["summary"], content, canonical),
        encoding="utf-8"
    )


def build_rss(all_issues: List[Issue], output_dir: Path) -> None:
    # Safety rule: drafts can never enter RSS.
    published = [issue for issue in all_issues if issue.published][:20]
    items = []

    for issue in published:
        summary_html = (
            f'<p><img src="{html.escape(issue.hero_url, quote=True)}" '
            f'alt="Community Garden Chronicle" style="max-width:100%;height:auto;"></p>'
            f'<p>{html.escape(issue.meta["summary"])}</p>'
        )
        pub_date = issue.date_obj.replace(hour=12)

        items.append(f"""
    <item>
      <title>{xml_escape(issue.meta["title"])}</title>
      <link>{xml_escape(issue.url)}</link>
      <guid isPermaLink="true">{xml_escape(issue.url)}</guid>
      <pubDate>{format_datetime(pub_date)}</pubDate>
      <description><![CDATA[{summary_html}]]></description>
      <content:encoded><![CDATA[{markdown_to_html(issue.body)}]]></content:encoded>
    </item>""")

    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
     xmlns:atom="http://www.w3.org/2005/Atom"
     xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>{xml_escape(SITE_TITLE)}</title>
    <link>{BASE_URL}/chronicle/</link>
    <description>{xml_escape(TAGLINE)} Weekly field notes from the Openwater open-source community.</description>
    <language>en-us</language>
    <atom:link href="{BASE_URL}/chronicle/feed.xml" rel="self" type="application/rss+xml" />
{''.join(items)}
  </channel>
</rss>
"""
    (output_dir / "feed.xml").write_text(rss, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--include-drafts",
        action="store_true",
        help="Build draft issue pages for preview. Drafts are still excluded from RSS."
    )
    parser.add_argument(
        "--output-dir",
        default="chronicle",
        help="Output directory relative to repository root."
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    content_dir = repo_root / "content" / "chronicle"
    output_dir = repo_root / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    source_files = sorted(
        p for p in content_dir.glob("*.md")
        if not p.name.startswith("_") and p.name.lower() != "readme.md"
    )

    all_issues = [parse_issue(path) for path in source_files]
    all_issues.sort(key=lambda issue: (issue.date_obj, issue.number), reverse=True)

    public_issues = [issue for issue in all_issues if issue.published]
    visible_issues = all_issues if args.include_drafts else public_issues

    build_index(visible_issues, output_dir)
    for issue in visible_issues:
        build_issue_page(issue, output_dir)
    build_rss(all_issues, output_dir)

    print(f"Built Chronicle in: {output_dir}")
    print(f"Published issues: {len(public_issues)}")
    if args.include_drafts:
        print(f"Preview issue pages: {len(visible_issues)}")
    print("RSS safety: drafts excluded")


if __name__ == "__main__":
    main()
