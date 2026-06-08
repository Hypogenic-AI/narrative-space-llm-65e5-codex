"""Prepare matched human texts and LLM prompts for the experiment."""

from __future__ import annotations

import json
import random
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from datasets import load_from_disk
except ImportError:  # pragma: no cover
    load_from_disk = None

from common import ROOT, SEED, clean_text, ensure_dirs, set_seed, truncate_words, word_tokens, write_jsonl

SPATIAL_PROMPT_TERMS = {
    "room",
    "door",
    "hall",
    "hallway",
    "corridor",
    "stairs",
    "building",
    "house",
    "apartment",
    "floor",
    "walk",
    "walked",
    "left",
    "right",
    "inside",
}


def load_r2r_records() -> list[dict]:
    """Load all locally available R2R annotation splits."""
    raw = ROOT / "datasets" / "r2r_navigation" / "raw"
    records: list[dict] = []
    for split_path in sorted(raw.glob("R2R_*.json")):
        split_name = split_path.stem.replace("R2R_", "")
        data = json.loads(split_path.read_text(encoding="utf-8"))
        for item in data:
            item = dict(item)
            item["split"] = split_name
            records.append(item)
    return records


def make_route_prompt(item: dict) -> str:
    """Create the route-to-story generation prompt from R2R instructions."""
    instructions = [clean_text(x) for x in item["instructions"] if clean_text(x)]
    instruction_block = "\n".join(f"{idx + 1}. {text}" for idx, text in enumerate(instructions))
    return f"""You are writing a concise literary scene, not a list of directions.

Use the indoor route constraints below as the physical path for the scene.
Write a first-person micro-story of 160 to 220 words in which the narrator moves through the building.

Rules:
- Preserve the order of movement and the final stopping point.
- Keep the route physically navigable.
- Do not mention that you were given route instructions.
- Do not use bullet points, headings, or analysis.
- Return only the story.

Route constraints:
{instruction_block}"""


def make_writingprompt_prompt(prompt: str) -> str:
    """Create the matched WritingPrompts generation prompt."""
    return f"""Write a 160 to 220 word first-person story scene responding to the prompt below.
Make the scene centered on embodied movement through an indoor or built space when that fits the prompt.
Keep spatial movement easy to follow, but write natural prose rather than directions.
Return only the story.

Prompt:
{clean_text(prompt)}"""


def prepare_r2r(n_routes: int = 80) -> tuple[list[dict], list[dict]]:
    """Sample R2R routes and return human texts plus LLM prompts."""
    rng = random.Random(SEED)
    candidates = [
        item
        for item in load_r2r_records()
        if item.get("instructions") and len(item.get("path", [])) >= 2
    ]
    rng.shuffle(candidates)
    selected = candidates[:n_routes]

    human_rows: list[dict] = []
    prompt_rows: list[dict] = []
    for idx, item in enumerate(selected):
        instructions = [clean_text(x) for x in item["instructions"] if clean_text(x)]
        human_text = instructions[0]
        prompt_id = f"r2r_{idx:03d}_path{item['path_id']}"
        base_meta = {
            "prompt_id": prompt_id,
            "source": "r2r",
            "path_id": item["path_id"],
            "scan": item["scan"],
            "split": item["split"],
            "distance": item.get("distance"),
            "path_length_nodes": len(item.get("path", [])),
        }
        human_rows.append(
            {
                **base_meta,
                "doc_id": f"{prompt_id}_human",
                "author": "human",
                "text": human_text,
                "text_role": "r2r_human_instruction",
            }
        )
        prompt_rows.append(
            {
                **base_meta,
                "task": "r2r_route_story",
                "prompt": make_route_prompt(item),
                "route_seed_instructions": instructions,
                "model_target_words": "160-220",
            }
        )
    return human_rows, prompt_rows


def load_writingprompt_rows() -> list[dict]:
    """Load the spatial WritingPrompts sample JSONL."""
    path = ROOT / "datasets" / "writingprompts_spatial_sample" / "samples" / "spatial_filtered_500.jsonl"
    rows: list[dict] = []
    seen_prompts: set[str] = set()
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            prompt = clean_text(row.get("prompt", ""))
            if prompt in seen_prompts:
                continue
            seen_prompts.add(prompt)
            rows.append(row)
    return rows


def has_spatial_prompt_term(prompt: str) -> bool:
    """Return true if the prompt itself contains a built-space cue."""
    words = set(word_tokens(prompt))
    return bool(words & SPATIAL_PROMPT_TERMS)


def prepare_writingprompts() -> tuple[list[dict], list[dict]]:
    """Prepare all WritingPrompts records whose prompt text has spatial cues."""
    rows = [row for row in load_writingprompt_rows() if has_spatial_prompt_term(row.get("prompt", ""))]
    human_rows: list[dict] = []
    prompt_rows: list[dict] = []
    for idx, row in enumerate(rows):
        prompt_id = f"wp_{idx:03d}"
        prompt = clean_text(row.get("prompt", ""))
        story = truncate_words(row.get("story", ""), 220)
        base_meta = {
            "prompt_id": prompt_id,
            "source": "writingprompts",
            "original_prompt": prompt,
        }
        human_rows.append(
            {
                **base_meta,
                "doc_id": f"{prompt_id}_human",
                "author": "human",
                "text": story,
                "text_role": "writingprompts_human_story_excerpt",
            }
        )
        prompt_rows.append(
            {
                **base_meta,
                "task": "writingprompt_spatial_story",
                "prompt": make_writingprompt_prompt(prompt),
                "model_target_words": "160-220",
            }
        )
    return human_rows, prompt_rows


def prepare_longstory_external(max_records: int = 80) -> list[dict]:
    """Prepare a small external AI-story set for non-training inspection."""
    if load_from_disk is None:
        return []
    dataset_path = ROOT / "datasets" / "longstory_ai_generated"
    if not dataset_path.exists():
        return []
    ds = load_from_disk(str(dataset_path))["train"]
    rows: list[dict] = []
    for idx, row in enumerate(ds):
        messages = row.get("messages") or []
        if not messages:
            continue
        text = clean_text(messages[-1].get("content", ""))
        lower = text.lower()
        if not any(term in lower for term in SPATIAL_PROMPT_TERMS):
            continue
        rows.append(
            {
                "doc_id": f"longstory_{idx:05d}",
                "prompt_id": f"longstory_{idx:05d}",
                "author": "llm_external",
                "source": "longstory",
                "text": truncate_words(text, 220),
                "text_role": "external_ai_story_excerpt",
            }
        )
        if len(rows) >= max_records:
            break
    return rows


def gpu_status() -> str:
    """Capture GPU status for reproducibility documentation."""
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name,memory.total,memory.free", "--format=csv"],
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return out.strip()
    except Exception:
        return "NO_GPU"


def main() -> None:
    set_seed(SEED)
    ensure_dirs(
        ROOT / "results",
        ROOT / "results" / "prompts",
        ROOT / "results" / "model_outputs",
        ROOT / "results" / "evaluations",
        ROOT / "figures",
        ROOT / "logs",
    )

    r2r_human, r2r_prompts = prepare_r2r()
    wp_human, wp_prompts = prepare_writingprompts()
    external_ai = prepare_longstory_external()

    human_rows = r2r_human + wp_human
    prompt_rows = r2r_prompts + wp_prompts

    write_jsonl(ROOT / "results" / "human_corpus.jsonl", human_rows)
    write_jsonl(ROOT / "results" / "prompts" / "llm_prompts.jsonl", prompt_rows)
    write_jsonl(ROOT / "results" / "external_ai_corpus.jsonl", external_ai)

    config = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "seed": SEED,
        "python_version": sys.version,
        "n_human_r2r": len(r2r_human),
        "n_human_writingprompts": len(wp_human),
        "n_llm_prompts": len(prompt_rows),
        "n_external_longstory": len(external_ai),
        "gpu_status": gpu_status(),
        "primary_model": "gpt-5.4-mini",
        "model_temperature": 0.7,
        "model_max_output_tokens": 320,
    }
    (ROOT / "results" / "config.json").write_text(json.dumps(config, indent=2), encoding="utf-8")
    print(json.dumps(config, indent=2))


if __name__ == "__main__":
    main()
