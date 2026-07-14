#!/bin/bash
#
# upload-media.command — sync local media to Cloudflare R2 (drneal-media bucket)
#
# Double-click this file in Finder to run it.
# First run: installs Wrangler if needed, then opens a browser window —
# click "Allow" to authorise Wrangler with your Cloudflare account (OAuth,
# no API token to copy or store).
#
# What it does: uploads any NEW or CHANGED files in static/audio/ and
# static/video/ to the matching folder in the drneal-media R2 bucket.
# Already-uploaded files are skipped (tracked in .r2-uploaded).
#
# After uploading, files are served at:
#   https://pub-f57cd770c3d9448dafde9725cbc874b9.r2.dev/audio/<filename>
#   https://pub-f57cd770c3d9448dafde9725cbc874b9.r2.dev/video/<filename>

cd "$(dirname "$0")" || exit 1
BUCKET="drneal-media"
MANIFEST=".r2-uploaded"

echo "── R2 media uploader ─────────────────────────────────"

# 1. Wrangler installed?
if ! command -v wrangler >/dev/null 2>&1; then
  echo "Wrangler not found — installing via npm (one-time)…"
  if ! command -v npm >/dev/null 2>&1; then
    echo "✗ npm not found. Install Node.js first: https://nodejs.org"
    read -n 1 -p "Press any key to close…"; exit 1
  fi
  npm install -g wrangler || { echo "✗ install failed"; read -n 1 -p "Press any key to close…"; exit 1; }
fi

# 2. Logged in? (first run opens the browser for OAuth)
if ! wrangler whoami >/dev/null 2>&1; then
  echo "Not logged in — your browser will open. Click 'Allow'."
  wrangler login || { echo "✗ login failed"; read -n 1 -p "Press any key to close…"; exit 1; }
fi

# 3. Sync audio/ and video/
touch "$MANIFEST"
uploaded=0
skipped=0
failed=0

for dir in audio video; do
  [ -d "static/$dir" ] || continue
  for f in static/"$dir"/*; do
    [ -f "$f" ] || continue
    name=$(basename "$f")
    case "$name" in .*) continue ;; esac          # skip hidden files
    size=$(stat -f%z "$f")
    sig="$dir/$name|$size"
    if grep -qxF "$sig" "$MANIFEST"; then
      skipped=$((skipped+1))
      continue
    fi
    echo "↑ uploading $dir/$name ($((size/1024/1024)) MB)…"
    if wrangler r2 object put "$BUCKET/$dir/$name" --file "$f" --remote; then
      grep -vF "$dir/$name|" "$MANIFEST" > "$MANIFEST.tmp" 2>/dev/null
      mv "$MANIFEST.tmp" "$MANIFEST"
      echo "$sig" >> "$MANIFEST"
      echo "  ✓ https://pub-f57cd770c3d9448dafde9725cbc874b9.r2.dev/$dir/$name"
      uploaded=$((uploaded+1))
    else
      echo "  ✗ FAILED: $f"
      failed=$((failed+1))
    fi
  done
done

echo "──────────────────────────────────────────────────────"
echo "Done: $uploaded uploaded, $skipped already up to date, $failed failed."
read -n 1 -p "Press any key to close…"
