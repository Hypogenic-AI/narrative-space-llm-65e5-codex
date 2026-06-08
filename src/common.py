"""Shared utilities for the narrative-space experiment."""

from __future__ import annotations

import json
import random
import re
from pathlib import Path
from typing import Iterable

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SEED = 42


def set_seed(seed: int = SEED) -> None:
    """Set deterministic seeds for Python and NumPy."""
    random.seed(seed)
    np.random.seed(seed)


def ensure_dirs(*paths: Path) -> None:
    """Create output directories if needed."""
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def read_jsonl(path: Path) -> list[dict]:
    """Read newline-delimited JSON records."""
    records: list[dict] = []
    if not path.exists():
        return records
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records


def write_jsonl(path: Path, records: Iterable[dict]) -> None:
    """Write records as newline-delimited JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def append_jsonl(path: Path, record: dict) -> None:
    """Append one record to a JSONL file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def clean_text(text: str) -> str:
    """Normalize whitespace while preserving wording."""
    return re.sub(r"\s+", " ", str(text)).strip()


def word_tokens(text: str) -> list[str]:
    """Tokenize alphabetic words with simple apostrophe support."""
    return re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", text.lower())


def sentence_split(text: str) -> list[str]:
    """Split text into rough sentences."""
    parts = re.split(r"(?<=[.!?])\s+", clean_text(text))
    return [p.strip() for p in parts if p.strip()]


def truncate_words(text: str, max_words: int = 220) -> str:
    """Return a first-N-word excerpt with punctuation left intact where possible."""
    tokens = re.findall(r"\S+", clean_text(text))
    if len(tokens) <= max_words:
        return clean_text(text)
    return " ".join(tokens[:max_words])


def count_terms(tokens: list[str], terms: set[str]) -> int:
    """Count tokens that occur in a term set."""
    return sum(1 for tok in tokens if tok in terms)


def per_1000(count: float, n_words: int) -> float:
    """Normalize a count to per-1,000-token rate."""
    return 1000.0 * count / max(n_words, 1)
