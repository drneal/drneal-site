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

TAG_URLS = {
    "Claude API":           "https://www.anthropic.com/api",
    "OpenAI":               "https://en.wikipedia.org/wiki/OpenAI",
    "Gemini":               "https://en.wikipedia.org/wiki/Gemini_(language_model)",
    "RAG":                  "https://en.wikipedia.org/wiki/Retrieval-augmented_generation",
    "tool use":             "https://en.wikipedia.org/wiki/Prompt_engineering",
    "prompt engineering":   "https://en.wikipedia.org/wiki/Prompt_engineering",
    "Claude Code":          "https://www.anthropic.com/claude-code",
    "multi-agent":          "https://en.wikipedia.org/wiki/Multi-agent_system",
    "MCP":                  "https://modelcontextprotocol.io/introduction",
    "autonomous execution": "https://en.wikipedia.org/wiki/Autonomous_agent",
    "agent SDKs":           "https://en.wikipedia.org/wiki/Software_development_kit",
    "tool servers":         "https://modelcontextprotocol.io/docs/concepts/tools",
    "connectors":           "https://modelcontextprotocol.io/docs/concepts/resources",
    "local + remote":       "https://modelcontextprotocol.io/docs/concepts/transports",
    "PyTorch":              "https://en.wikipedia.org/wiki/PyTorch",
    "TensorFlow":           "https://en.wikipedia.org/wiki/TensorFlow",
    "transformers":         "https://en.wikipedia.org/wiki/Transformer_(deep_learning_architecture)",
    "LoRA":                 "https://en.wikipedia.org/wiki/Fine-tuning_(deep_learning)",
    "PEFT":                 "https://en.wikipedia.org/wiki/Fine-tuning_(deep_learning)",
    "HuggingFace":          "https://en.wikipedia.org/wiki/Hugging_Face",
    "scikit-learn":         "https://en.wikipedia.org/wiki/Scikit-learn",
    "XGBoost":              "https://en.wikipedia.org/wiki/XGBoost",
    "statsmodels":          "https://www.statsmodels.org",
    "scipy":                "https://en.wikipedia.org/wiki/SciPy",
    "R":                    "https://en.wikipedia.org/wiki/R_(programming_language)",
    "spaCy":                "https://en.wikipedia.org/wiki/SpaCy",
    "NLTK":                 "https://en.wikipedia.org/wiki/Natural_Language_Toolkit",
    "BERT":                 "https://en.wikipedia.org/wiki/BERT_(language_model)",
    "clinical NLP":         "https://en.wikipedia.org/wiki/Natural_language_processing",
    "embeddings":           "https://en.wikipedia.org/wiki/Word_embedding",
    "vector search":        "https://en.wikipedia.org/wiki/Nearest_neighbor_search",
    "diagnostic AI":        "https://en.wikipedia.org/wiki/Artificial_intelligence_in_healthcare",
    "risk models":          "https://en.wikipedia.org/wiki/Risk_assessment",
    "FHIR":                 "https://en.wikipedia.org/wiki/Fast_Healthcare_Interoperability_Resources",
    "HL7":                  "https://en.wikipedia.org/wiki/Health_Level_7",
    "DICOM":                "https://en.wikipedia.org/wiki/DICOM",
    "pandas":               "https://en.wikipedia.org/wiki/Pandas_(software)",
    "data pipelines":       "https://en.wikipedia.org/wiki/Pipeline_(computing)",
    "anonymisation":        "https://en.wikipedia.org/wiki/Data_anonymization",
    "Arduino":              "https://en.wikipedia.org/wiki/Arduino",
    "ESP32":                "https://en.wikipedia.org/wiki/ESP32",
    "ESP-IDF":              "https://docs.espressif.com/projects/esp-idf/en/latest/",
    "Raspberry Pi":         "https://en.wikipedia.org/wiki/Raspberry_Pi",
    "LoRa":                 "https://en.wikipedia.org/wiki/LoRa",
    "I2C/SPI":              "https://en.wikipedia.org/wiki/I%C2%B2C",
    "Python":               "https://en.wikipedia.org/wiki/Python_(programming_language)",
    "Flask":                "https://en.wikipedia.org/wiki/Flask_(web_framework)",
    "FastAPI":              "https://en.wikipedia.org/wiki/FastAPI",
    "C/C++":                "https://en.wikipedia.org/wiki/C%2B%2B",
    "LISP":                 "https://en.wikipedia.org/wiki/Lisp_(programming_language)",
    "EMACS":                "https://en.wikipedia.org/wiki/Emacs",
    "MQL5":                 "https://www.mql5.com/en/articles",
    "MetaTrader":           "https://en.wikipedia.org/wiki/MetaTrader_4",
    "quant finance":        "https://en.wikipedia.org/wiki/Quantitative_analysis_(finance)",
    "neural nets":          "https://en.wikipedia.org/wiki/Artificial_neural_network",
    "backtesting":          "https://en.wikipedia.org/wiki/Backtesting",
    "Bitcoin":              "https://en.wikipedia.org/wiki/Bitcoin",
    "Ethereum":             "https://en.wikipedia.org/wiki/Ethereum",
    "Solidity":             "https://en.wikipedia.org/wiki/Solidity",
    "Cardano":              "https://en.wikipedia.org/wiki/Cardano_(blockchain_platform)",
    "cryptography":         "https://en.wikipedia.org/wiki/Cryptography",
}

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
    return render_template("skills.html", skills=data, tag_urls=TAG_URLS)


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
