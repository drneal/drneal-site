"""
Dr Neal Aggarwal — AI Engineering Site
Flask application. All content lives in data/ (JSON) and content/posts/ (Markdown).
To add a post: drop a .md file in content/posts/ with YAML frontmatter.
To update the library or skills: edit data/library.json or data/skills.json.
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime

import markdown
from flask import Flask, render_template, abort, request

app = Flask(__name__)

BASE = Path(__file__).parent
POSTS_DIR = BASE / "content" / "posts"
DATA_DIR = BASE / "data"


# ── helpers ──────────────────────────────────────────────────────────────────

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Extract YAML-style frontmatter from a markdown file."""
    meta: dict = {}
    body = text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            fm_block = text[3:end].strip()
            body = text[end + 4:].strip()
            for line in fm_block.splitlines():
                if ":" in line:
                    k, _, v = line.partition(":")
                    meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, body


def load_posts(limit: int = None) -> list[dict]:
    posts = []
    for path in sorted(POSTS_DIR.glob("*.md"), reverse=True):
        raw = path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(raw)
        # Generate excerpt — first non-empty paragraph
        excerpt_src = re.split(r'\n\n', body.strip(), maxsplit=3)
        excerpt = ""
        for chunk in excerpt_src:
            stripped = chunk.strip().lstrip("#").strip()
            if stripped and not stripped.startswith("!["):
                excerpt = stripped[:300]
                if len(stripped) > 300:
                    excerpt += "…"
                break
        posts.append({
            "slug": path.stem,
            "title": meta.get("title", path.stem.replace("-", " ").title()),
            "date": meta.get("date", ""),
            "category": meta.get("category", "AI"),
            "tags": [t.strip() for t in meta.get("tags", "").split(",") if t.strip()],
            "level": meta.get("level", ""),
            "read_time": meta.get("read_time", ""),
            "summary": meta.get("summary", excerpt),
            "featured": meta.get("featured", "false").lower() == "true",
        })
    if limit:
        return posts[:limit]
    return posts


def load_post(slug: str) -> dict | None:
    path = POSTS_DIR / f"{slug}.md"
    if not path.exists():
        return None
    raw = path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(raw)
    html = markdown.markdown(
        body,
        extensions=["fenced_code", "tables", "toc", "nl2br", "attr_list"],
    )
    return {
        "slug": slug,
        "title": meta.get("title", slug.replace("-", " ").title()),
        "date": meta.get("date", ""),
        "category": meta.get("category", "AI"),
        "tags": [t.strip() for t in meta.get("tags", "").split(",") if t.strip()],
        "level": meta.get("level", ""),
        "read_time": meta.get("read_time", ""),
        "summary": meta.get("summary", ""),
        "content": html,
    }


def load_json(filename: str) -> dict | list:
    path = DATA_DIR / filename
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


# ── routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    posts = load_posts()
    featured = [p for p in posts if p["featured"]][:1]
    recent = [p for p in posts if not p["featured"]][:8]
    return render_template("index.html", posts=posts, featured=featured, recent=recent)


@app.route("/post/<slug>")
def post(slug):
    p = load_post(slug)
    if not p:
        abort(404)
    all_posts = load_posts()
    idx = next((i for i, x in enumerate(all_posts) if x["slug"] == slug), None)
    prev_post = all_posts[idx + 1] if idx is not None and idx + 1 < len(all_posts) else None
    next_post = all_posts[idx - 1] if idx is not None and idx > 0 else None
    return render_template("post.html", post=p, prev_post=prev_post, next_post=next_post)


@app.route("/skills")
def skills():
    data = load_json("skills.json")
    return render_template("skills.html", skills=data)


@app.route("/library")
def library():
    data = load_json("library.json")
    category = request.args.get("cat", "all")
    author = request.args.get("author", "all")
    items = data.get("items", [])
    if category != "all":
        items = [i for i in items if i.get("type") == category]
    if author != "all":
        items = [i for i in items if author.lower() in i.get("author", "").lower()]
    authors = sorted(set(i.get("author", "") for i in data.get("items", [])))
    return render_template("library.html", items=items, authors=authors,
                           current_cat=category, current_author=author)


@app.route("/demos")
def demos():
    data = load_json("demos.json")
    return render_template("demos.html", demos=data.get("demos", []))


@app.route("/about")
def about():
    return render_template("about.html")


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
