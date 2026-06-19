# Deployment Guide — drnealaggarwal.info

## Local development

```bash
cd drneal-site
pip install -r requirements.txt
python app.py
# → http://localhost:5000
```

## Adding a blog post

Drop a `.md` file into `content/posts/` named `YYYY-MM-DD-slug-here.md`.

Required frontmatter at the top (between `---` markers):

```yaml
---
title: "Your Post Title"
date: "June 19, 2026"
category: "AI Engineering"        # shown as badge
tags: "AI, LLM, agents"          # comma-separated
level: "Intermediate"             # Easy / Intermediate / Advanced
read_time: "10 minutes"
featured: false                   # set true for ONE post to pin it at top
summary: "One-paragraph summary shown on the card."
---
```

Then write normal Markdown below the closing `---`. Fenced code blocks, tables, and links all render correctly.

## Updating the Library

Edit `data/library.json`. Each item:

```json
{
  "title": "Paper / Video Title",
  "author": "Author Name",
  "year": "2025",
  "type": "paper",          // paper | video | post | talk
  "description": "Why this matters.",
  "url": "https://...",
  "tags": ["tag1", "tag2"]
}
```

## Updating Skills

Edit `data/skills.json`. Skill level is 0–100 (drives the progress bar animation).

## Updating Demos

Edit `data/demos.json`. Set `"status": "live"` and add a `"url"` when a demo is ready.

## Production deployment (VPS / Ubuntu)

```bash
# Install
sudo apt update && sudo apt install python3-pip nginx
pip3 install -r requirements.txt

# Run with gunicorn (systemd service)
gunicorn -w 4 -b 127.0.0.1:5000 app:app

# Nginx reverse proxy → point drnealaggarwal.info to 127.0.0.1:5000
# Use certbot for HTTPS: sudo certbot --nginx -d drnealaggarwal.info
```

A ready-made `systemd` unit file:

```ini
[Unit]
Description=Dr Neal Aggarwal site
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/drneal-site
ExecStart=/usr/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

## Alternatively — deploy to Railway / Render / Fly.io (zero-config)

All three platforms detect Flask apps automatically. Push the repo; they handle the rest.
Set the start command to: `gunicorn app:app`
