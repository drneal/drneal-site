#!/bin/bash
#
# upload-media-s3.command — fallback uploader for static/audio and static/video
#
# Does the same job as upload-media.command, but over R2's S3-compatible API
# using the R2_* credentials already in .env, instead of wrangler. Differences
# that matter for large files:
#
#   * multipart upload in 16 MB chunks, 4 in parallel — a dropped connection
#     costs you one chunk, not the whole file
#   * live progress, so you can tell the difference between slow and hung
#   * sets Content-Type properly (wrangler guesses)
#
# It shares .r2-uploaded with upload-media.command, so whichever you run, the
# other will skip files already done.
#
# Double-click in Finder, or: bash upload-media-s3.command

cd "$(dirname "$0")" || exit 1

if ! python3 -c "import boto3" >/dev/null 2>&1; then
  echo "Installing boto3 (one-time)…"
  python3 -m pip install --quiet boto3 || {
    echo "✗ Could not install boto3."; read -n 1 -p "Press any key to close…"; exit 1; }
fi

python3 - <<'PY'
import os, re, sys, threading, mimetypes
import boto3
from boto3.s3.transfer import TransferConfig

if not os.path.exists('.env'):
    sys.exit("✗ .env not found — run this from the repo root.")
env = dict(re.findall(r'^\s*(\w+)\s*=\s*(.*?)\s*$', open('.env').read(), flags=re.M))
need = ('R2_ENDPOINT', 'R2_ACCESS_KEY_ID', 'R2_SECRET_ACCESS_KEY', 'R2_BUCKET', 'R2_PUBLIC_URL')
missing = [k for k in need if not env.get(k)]
if missing:
    sys.exit("✗ .env is missing: " + ", ".join(missing))

BUCKET   = env['R2_BUCKET']
PUBLIC   = env['R2_PUBLIC_URL'].rstrip('/')
MANIFEST = '.r2-uploaded'

s3 = boto3.client(
    's3',
    endpoint_url=env['R2_ENDPOINT'],
    aws_access_key_id=env['R2_ACCESS_KEY_ID'],
    aws_secret_access_key=env['R2_SECRET_ACCESS_KEY'],
    region_name='auto',
)

cfg = TransferConfig(
    multipart_threshold=16 * 1024 * 1024,
    multipart_chunksize=16 * 1024 * 1024,
    max_concurrency=4,
    use_threads=True,
)

CTYPE = {'.m4a': 'audio/mp4', '.mp3': 'audio/mpeg', '.mp4': 'video/mp4',
         '.wav': 'audio/wav',  '.ogg': 'audio/ogg',  '.webm': 'video/webm'}

open(MANIFEST, 'a').close()
done = set(l.strip() for l in open(MANIFEST) if l.strip())

class Progress:
    def __init__(self, total, label):
        self.total, self.label, self.seen = total, label, 0
        self.lock = threading.Lock()
    def __call__(self, n):
        with self.lock:
            self.seen += n
            pct = self.seen / self.total * 100
            bar = '█' * int(pct // 4) + '·' * (25 - int(pct // 4))
            sys.stdout.write(f"\r  [{bar}] {pct:5.1f}%  "
                             f"{self.seen/1048576:.0f}/{self.total/1048576:.0f} MB")
            sys.stdout.flush()

print("── R2 media uploader (S3 multipart) ──────────────────")
uploaded = skipped = failed = 0

for folder in ('audio', 'video'):
    d = os.path.join('static', folder)
    if not os.path.isdir(d):
        continue
    for name in sorted(os.listdir(d)):
        path = os.path.join(d, name)
        if name.startswith('.') or not os.path.isfile(path):
            continue
        size = os.path.getsize(path)
        sig = f"{folder}/{name}|{size}"
        if sig in done:
            skipped += 1
            continue
        key = f"{folder}/{name}"
        ext = os.path.splitext(name)[1].lower()
        ctype = CTYPE.get(ext) or mimetypes.guess_type(name)[0] or 'application/octet-stream'
        print(f"↑ {key}  ({size/1048576:.0f} MB, {ctype})")
        try:
            s3.upload_file(path, BUCKET, key,
                           ExtraArgs={'ContentType': ctype},
                           Config=cfg, Callback=Progress(size, key))
            head = s3.head_object(Bucket=BUCKET, Key=key)
            print()
            if head['ContentLength'] != size:
                raise RuntimeError(
                    f"size mismatch: local {size}, remote {head['ContentLength']}")
            # keep the manifest in sync with upload-media.command
            lines = [l for l in open(MANIFEST).read().splitlines()
                     if not l.startswith(f"{folder}/{name}|")]
            lines.append(sig)
            open(MANIFEST, 'w').write("\n".join(lines) + "\n")
            print(f"  ✓ {PUBLIC}/{key}")
            uploaded += 1
        except Exception as e:
            print(f"\n  ✗ FAILED: {key}\n    {e}")
            failed += 1

print("──────────────────────────────────────────────────────")
print(f"Done: {uploaded} uploaded, {skipped} already up to date, {failed} failed.")
PY

read -n 1 -p "Press any key to close…"
