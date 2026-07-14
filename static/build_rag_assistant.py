"""
build_rag_assistant.py — companion script to Lesson 8, "The Capstone"
https://drnealaggarwal.info/post/2026-07-12-build-a-grounded-assistant

A complete, local retrieval assistant over a folder of your own documents
(.txt and .md files). Retrieval runs entirely on your machine; grounded
answering uses a chat-model API only if you provide a key.

Setup:
    pip install sentence-transformers numpy
    pip install anthropic            # optional, for grounded answers
    export ANTHROPIC_API_KEY=...     # optional

Usage:
    python build_rag_assistant.py docs/                       # interactive
    python build_rag_assistant.py docs/ --ask "your question"
    python build_rag_assistant.py docs/ --eval eval.tsv       # recall@k

eval.tsv format (tab-separated, one test per line):
    question<TAB>filename_that_contains_the_answer
"""

import os
import sys
import glob
import argparse

import numpy as np

# ── configuration ─────────────────────────────────────────────────────────────
CHUNK_CHARS   = 1200   # ~250-300 tokens per chunk
OVERLAP_CHARS = 200    # consecutive chunks share this much text
TOP_K         = 5      # passages retrieved per question
EMBED_MODEL   = "all-MiniLM-L6-v2"   # small, fast, runs locally


# ── step 1: load and chunk the corpus (Lesson 8, "Chunking") ─────────────────
def load_chunks(folder):
    """Read every .txt/.md file and split into overlapping chunks."""
    chunks = []
    paths = sorted(glob.glob(os.path.join(folder, "**", "*.txt"), recursive=True)
                   + glob.glob(os.path.join(folder, "**", "*.md"), recursive=True))
    if not paths:
        sys.exit(f"No .txt or .md files found under {folder!r}")
    for path in paths:
        text = open(path, encoding="utf-8", errors="ignore").read()
        source = os.path.relpath(path, folder)
        step = CHUNK_CHARS - OVERLAP_CHARS
        for start in range(0, max(len(text), 1), step):
            piece = text[start : start + CHUNK_CHARS].strip()
            if len(piece) > 100:                    # skip trivial fragments
                chunks.append({"text": piece, "source": source, "pos": start})
    print(f"{len(paths)} files → {len(chunks)} chunks")
    return chunks


# ── step 2: embed everything locally (Lesson 7, "Meaning as geometry") ───────
def embed_chunks(chunks):
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(EMBED_MODEL)
    vecs = model.encode([c["text"] for c in chunks],
                        normalize_embeddings=True,       # unit length → dot = cosine
                        show_progress_bar=True)
    return model, np.asarray(vecs)


# ── step 3: retrieval (Lesson 7's twenty lines, verbatim in spirit) ──────────
def retrieve(question, model, vecs, chunks, k=TOP_K):
    q = model.encode([question], normalize_embeddings=True)[0]
    sims = vecs @ q                                       # cosine similarity
    top = np.argsort(sims)[-k:][::-1]
    return [(chunks[i], float(sims[i])) for i in top]


# ── step 4: grounded answering (Lesson 6's assistant + Lesson 7's grounding) ─
PROMPT = """Answer the question using ONLY the passages below.
Cite the source in [brackets] after every claim.
If the passages do not contain the answer, say exactly that — do not guess.

{context}

Question: {question}"""


def grounded_answer(question, passages):
    try:
        import anthropic
    except ImportError:
        return None
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return None
    context = "\n\n".join(f"[{c['source']}] {c['text']}" for c, _ in passages)
    client = anthropic.Anthropic()
    msg = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=800,
        messages=[{"role": "user",
                   "content": PROMPT.format(context=context, question=question)}],
    )
    return msg.content[0].text


def ask(question, model, vecs, chunks):
    passages = retrieve(question, model, vecs, chunks)
    print("\n── retrieved passages ─────────────────────────────")
    for c, sim in passages:
        preview = c["text"][:120].replace("\n", " ")
        print(f"  {sim:.3f}  [{c['source']}]  {preview}…")
    answer = grounded_answer(question, passages)
    if answer:
        print("\n── grounded answer ────────────────────────────────")
        print(answer)
    else:
        print("\n(no API key found — showing retrieval only, which is the "
              "half of the system most worth studying anyway)")


# ── step 5: honest evaluation (Lesson 8, "Measure the stages separately") ────
def evaluate(eval_path, model, vecs, chunks, k=TOP_K):
    """recall@k: for each test question, did any top-k chunk come from
    the file known to contain the answer?"""
    tests = []
    for line in open(eval_path, encoding="utf-8"):
        if "\t" in line:
            q, expected = line.rstrip("\n").split("\t")[:2]
            tests.append((q, expected))
    if not tests:
        sys.exit(f"No tab-separated test lines found in {eval_path!r}")
    hits = 0
    for q, expected in tests:
        passages = retrieve(q, model, vecs, chunks, k)
        found = any(expected in c["source"] for c, _ in passages)
        hits += found
        print(f"  {'✓' if found else '✗'}  {q[:70]}")
    print(f"\nrecall@{k}: {hits}/{len(tests)} = {hits/len(tests):.0%}")
    print("Every ✗ above is a question your assistant would have answered "
          "from the wrong evidence — or from none. Investigate each one.")


# ── main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", help="folder of .txt/.md documents")
    ap.add_argument("--ask", help="ask a single question and exit")
    ap.add_argument("--eval", dest="eval_path", help="run recall@k over eval.tsv")
    args = ap.parse_args()

    chunks = load_chunks(args.folder)
    model, vecs = embed_chunks(chunks)

    if args.eval_path:
        evaluate(args.eval_path, model, vecs, chunks)
    elif args.ask:
        ask(args.ask, model, vecs, chunks)
    else:
        print("\nInteractive mode — Ctrl-C to quit")
        while True:
            try:
                q = input("\nquestion> ").strip()
            except (KeyboardInterrupt, EOFError):
                print()
                break
            if q:
                ask(q, model, vecs, chunks)
