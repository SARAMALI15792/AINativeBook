"""Standalone RAG book content ingestion script (synchronous).

Reads canonical markdown files from intellistack/content/docs/, chunks them,
generates Google Gemini embeddings, and upserts into the Qdrant Cloud
`intellistack_content` collection.  DB-independent — no SQLAlchemy needed.

Uses synchronous clients throughout to avoid httpcore/anyio SSL issues with
cloud endpoints; Gemini sync API + qdrant-client sync QdrantClient.

Usage (from intellistack/backend/):
    GEMINI_API_KEY=... QDRANT_HOST=... QDRANT_API_KEY=... QDRANT_USE_HTTPS=true \\
        python scripts/ingest_book_content.py

Environment variables:
    GEMINI_API_KEY   Required — Google Gemini API key
    QDRANT_HOST      Qdrant hostname (default: localhost)
    QDRANT_PORT      Qdrant REST port (default: 6333)
    QDRANT_API_KEY   Qdrant Cloud API key (optional for local)
    QDRANT_USE_HTTPS Set to "true" for Qdrant Cloud (default: false)
"""

import hashlib
import logging
import os
import sys
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add backend src/ to import path
sys.path.insert(0, str(Path(__file__).parents[1]))

from google import genai
from google.genai import types as genai_types
from qdrant_client import QdrantClient, models

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

EMBEDDING_MODEL  = "models/gemini-embedding-001"
EMBEDDING_DIMS   = 3072
COLLECTION_NAME  = "intellistack_content"
BATCH_SIZE       = 20   # chunks per embedding batch

# ── Canonical content structure (mirrors seed_content_items.py) ───────────────
CONTENT_STRUCTURE: Dict[str, Dict] = {
    "stage-1": {
        "name": "Foundations",
        "items": [
            {"title": "Introduction to Stage 1",  "path": "stage-1/intro"},
            {"title": "Linux Theory",              "path": "stage-1/linux/1-1-linux-theory"},
            {"title": "File Systems",              "path": "stage-1/linux/1-2-file-systems"},
            {"title": "Process Management",        "path": "stage-1/linux/1-3-process-management"},
            {"title": "Python Axioms",             "path": "stage-1/python/1-2-python-axioms"},
            {"title": "Async Theory",              "path": "stage-1/python/1-3-async-theory"},
            {"title": "Linear Algebra",            "path": "stage-1/math/1-4-linear-algebra"},
            {"title": "Calculus & Dynamics",       "path": "stage-1/math/1-5-calculus-dynamics"},
            {"title": "Git History",               "path": "stage-1/git/1-6-git-history"},
            {"title": "Bash Shell",                "path": "stage-1/linux/1-7-bash-shell"},
        ],
    },
    "stage-2": {
        "name": "ROS 2 & Simulation",
        "items": [
            {"title": "Introduction to Stage 2",   "path": "stage-2/intro"},
            {"title": "Distributed Mind",          "path": "stage-2/graph-theory/2-1-distributed-mind"},
            {"title": "Pub/Sub Pattern",           "path": "stage-2/middleware/2-2-pub-sub"},
            {"title": "Services & Actions",        "path": "stage-2/services/2-3-services-actions"},
            {"title": "Coordinate Frames",         "path": "stage-2/tf2/2-4-coordinate-frames"},
            {"title": "ROS 2 Setup",               "path": "stage-2/ros2-setup"},
            {"title": "Gazebo Simulation",         "path": "stage-2/gazebo-simulation"},
        ],
    },
    "stage-3": {
        "name": "Perception & Planning",
        "items": [
            {"title": "Introduction to Stage 3",   "path": "stage-3/intro"},
            {"title": "Computer Vision",           "path": "stage-3/computer-vision"},
        ],
    },
    "stage-4": {
        "name": "AI Integration",
        "items": [
            {"title": "Introduction to Stage 4",   "path": "stage-4/intro"},
            {"title": "Machine Learning Basics",   "path": "stage-4/machine-learning-basics"},
        ],
    },
    "stage-5": {
        "name": "Capstone",
        "items": [
            {"title": "Introduction to Stage 5",   "path": "stage-5/intro"},
            {"title": "Project Guidelines",        "path": "stage-5/project-guidelines"},
        ],
    },
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            return text[end + 3:].lstrip("\n")
    return text


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def chunk_tokens(text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
    """Token-based chunking using tiktoken (replicates TextChunker logic)."""
    import tiktoken
    try:
        enc = tiktoken.encoding_for_model("gpt-4o")
    except Exception:
        enc = tiktoken.get_encoding("cl100k_base")

    tokens = enc.encode(text)
    if len(tokens) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))
        chunks.append(enc.decode(tokens[start:end]))
        start += chunk_size - overlap
    return chunks


def make_content_id(content_path: str) -> str:
    return content_path.replace("/", "_").replace("-", "_")


def make_point_id(content_id: str, chunk_index: int) -> str:
    """Deterministic UUID5 — Qdrant requires UUID-format or int point IDs."""
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"{content_id}_chunk_{chunk_index}"))


# ── Gemini embeddings (sync) ───────────────────────────────────────────────────

def embed_batch(gemini_client: genai.Client, texts: List[str]) -> List[List[float]]:
    """Embed a batch of texts synchronously using Gemini."""
    response = gemini_client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=texts,
        config=genai_types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
    )
    return [e.values for e in response.embeddings]


# ── Qdrant collection setup ────────────────────────────────────────────────────

def ensure_collection(qdrant: QdrantClient) -> None:
    if not qdrant.collection_exists(COLLECTION_NAME):
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=EMBEDDING_DIMS,
                distance=models.Distance.COSINE,
            ),
        )
        logger.info("Created Qdrant collection: %s (%d dims)", COLLECTION_NAME, EMBEDDING_DIMS)
    else:
        logger.info("Collection already exists: %s", COLLECTION_NAME)


# ── Main ingestion ─────────────────────────────────────────────────────────────

def ingest_all(docs_base: Path, gemini_client: genai.Client, qdrant: QdrantClient) -> None:
    ensure_collection(qdrant)

    stage_summary: List[Tuple[str, str, int, int, List[str]]] = []
    total_files = total_chunks = 0

    for stage_id, stage_info in CONTENT_STRUCTURE.items():
        stage_name: str = stage_info["name"]
        stage_files = stage_chunks = 0
        missing: List[str] = []

        logger.info("── %s  (%s) ──────────────────────────", stage_id, stage_name)

        for item in stage_info["items"]:
            content_path: str = item["path"]
            title: str = item["title"]
            file_path = docs_base / f"{content_path}.md"

            if not file_path.exists():
                missing.append(content_path)
                logger.warning("  SKIP  %s  (not found)", content_path)
                continue

            raw = file_path.read_text(encoding="utf-8")
            text = strip_frontmatter(raw)
            file_hash = sha256(text)

            if not text.strip():
                logger.warning("  SKIP  %s  (empty)", content_path)
                continue

            content_id = make_content_id(content_path)
            text_chunks = chunk_tokens(text)

            # Embed in batches
            all_embeddings: List[List[float]] = []
            for i in range(0, len(text_chunks), BATCH_SIZE):
                batch = text_chunks[i : i + BATCH_SIZE]
                all_embeddings.extend(embed_batch(gemini_client, batch))

            # Build Qdrant points
            points = [
                models.PointStruct(
                    id=make_point_id(content_id, idx),
                    vector=embedding,
                    payload={
                        "content_id":    content_id,
                        "stage_id":      stage_id,
                        "stage_name":    stage_name,
                        "content_title": title,
                        "chunk_index":   idx,
                        "text":          chunk_text,
                        "tokens":        len(chunk_text.split()),
                        "metadata": {
                            "source_file":      str(file_path.relative_to(docs_base.parent.parent)),
                            "source_file_hash": file_hash,
                        },
                    },
                )
                for idx, (chunk_text, embedding) in enumerate(zip(text_chunks, all_embeddings))
            ]

            qdrant.upsert(collection_name=COLLECTION_NAME, points=points)

            n = len(points)
            stage_files += 1
            stage_chunks += n
            logger.info("  OK    %-42s  %d chunks", title, n)

        total_files  += stage_files
        total_chunks += stage_chunks
        stage_summary.append((stage_id, stage_name, stage_files, stage_chunks, missing))

    # ── Summary ──────────────────────────────────────────────────────────────
    print()
    print("=" * 66)
    print("  INGESTION SUMMARY")
    print("=" * 66)
    for sid, sname, files, chunks, miss in stage_summary:
        print(f"  {sid}  ({sname})")
        print(f"    {files} files  →  {chunks} chunks")
        for m in miss:
            print(f"    ⚠  Missing: {m}")
    print("─" * 66)
    print(f"  Total: {total_files} files  →  {total_chunks} chunks ingested")
    print("=" * 66)

    # Verify
    info = qdrant.get_collection(COLLECTION_NAME)
    print(f"\n  Qdrant points_count: {info.points_count}  status: {info.status}")
    host = os.getenv("QDRANT_HOST", "localhost")
    print(f"  Dashboard: https://{host}/dashboard")
    print()


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        print("ERROR: GEMINI_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)

    script_dir = Path(__file__).parent
    docs_base  = script_dir.parents[1] / "content" / "docs"
    if not docs_base.exists():
        print(f"ERROR: Docs directory not found: {docs_base}", file=sys.stderr)
        sys.exit(1)

    # Build Qdrant client (sync — uses requests, not httpx/anyio)
    qdrant_host  = os.getenv("QDRANT_HOST",    "localhost")
    qdrant_port  = int(os.getenv("QDRANT_PORT", "6333"))
    qdrant_key   = os.getenv("QDRANT_API_KEY")
    use_https    = os.getenv("QDRANT_USE_HTTPS", "false").lower() == "true"

    qdrant = QdrantClient(
        host=qdrant_host,
        port=qdrant_port,
        api_key=qdrant_key,
        https=use_https,
        timeout=60,
    )

    gemini_client = genai.Client(api_key=gemini_key)

    print(f"Content directory : {docs_base}")
    print(f"Qdrant            : {'https' if use_https else 'http'}://{qdrant_host}:{qdrant_port}")
    print(f"Embedding model   : {EMBEDDING_MODEL}  ({EMBEDDING_DIMS} dims)")
    print()

    ingest_all(docs_base, gemini_client, qdrant)
