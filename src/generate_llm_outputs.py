"""Generate real LLM spatial narratives with OpenAI Responses API."""

from __future__ import annotations

import argparse
import os
import time
from datetime import datetime, timezone
from typing import Any

from openai import OpenAI
from tqdm import tqdm

from common import ROOT, append_jsonl, read_jsonl


def response_text(response: Any) -> str:
    """Extract text from a Responses API object."""
    text = getattr(response, "output_text", None)
    if text:
        return str(text).strip()
    chunks: list[str] = []
    for item in getattr(response, "output", []) or []:
        for content in getattr(item, "content", []) or []:
            if getattr(content, "type", None) in {"output_text", "text"}:
                chunks.append(getattr(content, "text", ""))
    return "\n".join(chunks).strip()


def usage_dict(response: Any) -> dict:
    """Extract token usage if the SDK provides it."""
    usage = getattr(response, "usage", None)
    if usage is None:
        return {}
    if hasattr(usage, "model_dump"):
        return usage.model_dump()
    if isinstance(usage, dict):
        return usage
    return {
        name: getattr(usage, name)
        for name in ["input_tokens", "output_tokens", "total_tokens"]
        if hasattr(usage, name)
    }


def call_with_retry(
    client: OpenAI,
    *,
    model: str,
    prompt: str,
    temperature: float,
    max_output_tokens: int,
    attempts: int = 5,
) -> Any:
    """Call the API with exponential backoff."""
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            return client.responses.create(
                model=model,
                input=prompt,
                temperature=temperature,
                max_output_tokens=max_output_tokens,
            )
        except Exception as exc:  # pragma: no cover - external API path
            last_error = exc
            sleep_for = min(2**attempt, 30)
            print(f"API call failed on attempt {attempt + 1}/{attempts}: {exc}")
            time.sleep(sleep_for)
    raise RuntimeError(f"OpenAI call failed after {attempts} attempts: {last_error}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gpt-5.4-mini")
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--max-output-tokens", type=int, default=320)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is not set; cannot run real LLM generation.")

    prompts_path = ROOT / "results" / "prompts" / "llm_prompts.jsonl"
    output_path = ROOT / "results" / "model_outputs" / f"{args.model}_outputs.jsonl"
    prompts = read_jsonl(prompts_path)
    if args.limit is not None:
        prompts = prompts[: args.limit]

    cached = {row["prompt_id"]: row for row in read_jsonl(output_path)}
    pending = [row for row in prompts if row["prompt_id"] not in cached]
    print(f"Prompts: {len(prompts)}; cached: {len(cached)}; pending: {len(pending)}")

    client = OpenAI(api_key=api_key)
    for row in tqdm(pending, desc="Generating"):
        response = call_with_retry(
            client,
            model=args.model,
            prompt=row["prompt"],
            temperature=args.temperature,
            max_output_tokens=args.max_output_tokens,
        )
        text = response_text(response)
        if not text:
            raise RuntimeError(f"Empty output for {row['prompt_id']}")
        record = {
            **{k: v for k, v in row.items() if k != "prompt"},
            "doc_id": f"{row['prompt_id']}_{args.model}",
            "author": "llm",
            "model": args.model,
            "temperature": args.temperature,
            "max_output_tokens": args.max_output_tokens,
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "text": text,
            "usage": usage_dict(response),
        }
        append_jsonl(output_path, record)

    print(f"Wrote outputs to {output_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
