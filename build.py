#!/usr/bin/env python3
"""Static site builder for brianragle.com.

Reads Markdown posts from posts/ (YAML frontmatter) and renders them
with Jinja2 templates into dist/. No frameworks, no trackers.

Usage:  python3 build.py
"""

import re
import shutil
from datetime import datetime
from pathlib import Path

import yaml
import markdown
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).parent
POSTS_DIR = ROOT / "posts"
TEMPLATES_DIR = ROOT / "templates"
ASSETS_DIR = ROOT / "assets"
DIST_DIR = ROOT / "dist"

SITE_URL = "https://brianragle.com"

SOCIALS = [
    {"name": "Instagram", "handle": "@brianragle", "url": "https://www.instagram.com/brianragle"},
    {"name": "Threads", "handle": "@brianragle", "url": "https://www.threads.com/@brianragle"},
    {"name": "Bluesky", "handle": "@brianragle.bsky.social", "url": "https://bsky.app/profile/brianragle.bsky.social"},
    {"name": "Mastodon", "handle": "@brianragle@mastodon.social", "url": "https://mastodon.social/@brianragle"},
    {"name": "TikTok", "handle": "@brianragle", "url": "https://www.tiktok.com/@brianragle"},
    {"name": "LinkedIn", "handle": "/in/brianragle", "url": "https://www.linkedin.com/in/brianragle/"},
    {"name": "YouTube", "handle": "@BrianRagle", "url": "https://www.youtube.com/@BrianRagle"},
    {"name": "Medium", "handle": "@brian.ragle", "url": "https://medium.com/@brian.ragle"},
    {"name": "Facebook", "handle": "brianmragle", "url": "https://www.facebook.com/brianmragle"},
    {"name": "Substack", "handle": "Brian Ragle", "url": "https://brianmragle.substack.com"},
]

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.S)


def parse_post(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        raise ValueError(f"{path}: missing YAML frontmatter")
    meta = yaml.safe_load(m.group(1)) or {}
    body = m.group(2).strip()

    date = meta.get("date")
    if isinstance(date, datetime):
        date = date.date().isoformat()
    date = str(date)
    slug = path.stem
    slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", slug) or slug

    return {
        "title": meta.get("title", slug),
        "date": date,
        "date_str": datetime.strptime(date, "%Y-%m-%d").strftime("%B %d, %Y"),
        "type": meta.get("type", "blurb"),
        "image": meta.get("image"),
        "video_url": meta.get("video_url"),
        "link_url": meta.get("link_url"),
        "excerpt": meta.get("excerpt", ""),
        "slug": slug,
        "html": markdown.markdown(body, extensions=["extra"]),
    }


def main() -> None:
    posts = sorted(
        (parse_post(p) for p in POSTS_DIR.glob("*.md")),
        key=lambda p: p["date"],
        reverse=True,
    )

    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True)
    shutil.copytree(ASSETS_DIR, DIST_DIR / "assets")

    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=True)

    def render(template_name, out_path, root, **ctx):
        tmpl = env.get_template(template_name)
        html = tmpl.render(root=root, socials=SOCIALS, site_url=SITE_URL, **ctx)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8")

    render("home.html", DIST_DIR / "index.html", "", active="home", posts=posts)
    render("archive.html", DIST_DIR / "posts" / "index.html", "../", active="posts", posts=posts)
    render("about.html", DIST_DIR / "about" / "index.html", "../", active="about")
    for post in posts:
        render(
            "post.html",
            DIST_DIR / "posts" / post["slug"] / "index.html",
            "../../",
            active="posts",
            post=post,
        )

    print(f"Built {len(posts)} posts -> {DIST_DIR}")


if __name__ == "__main__":
    main()
