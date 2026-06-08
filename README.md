# Narrative Space in LLMs

This workspace contains a completed experiment on whether LLM-generated spatial-navigation stories differ from human spatial narratives. The study compares human R2R route instructions and spatial WritingPrompts stories against 114 real GPT-5.4-mini generations.

## Key Findings

- Human-vs-LLM classification reached 97.4% accuracy with all features and 96.5% after removing length features.
- Spatial-only features reached 87.7% aggregate accuracy and 83.8% on the WritingPrompts prose-control subset.
- GPT-5.4-mini used more sensory language, formulaic phrases, first-person framing, route-step language, and landmark reuse.
- R2R results are strongly genre-confounded because human texts are short route instructions; WritingPrompts gives the cleaner but smaller prose-control result.
- See `REPORT.md` for full methodology, tables, figures, and limitations.

## Reproduce

```bash
source .venv/bin/activate
python src/prepare_corpora.py
python src/generate_llm_outputs.py --model gpt-5.4-mini --temperature 0.7 --max-output-tokens 320
python src/analyze_results.py --model gpt-5.4-mini
```

The generation script is cached. If `results/model_outputs/gpt-5.4-mini_outputs.jsonl` already contains all prompt IDs, it will make no new API calls.

## Files

- `planning.md`: preregistered motivation, hypotheses, and analysis plan.
- `REPORT.md`: primary research report with actual results.
- `src/`: data preparation, generation, feature extraction, and analysis code.
- `results/prompts/`: exact LLM prompts used for generation.
- `results/model_outputs/`: raw GPT-5.4-mini outputs and token usage metadata.
- `results/evaluations/`: feature tests, classifier metrics, predictions, and feature importances.
- `figures/`: summary visualizations used in the report.
- `literature_review.md` and `resources.md`: pre-gathered literature and resource catalog.

## Environment

The project uses the isolated `.venv` in this workspace and dependencies tracked in `pyproject.toml`/`uv.lock`. Python 3.12.8 was used. The machine had four NVIDIA RTX A6000 GPUs available, but this experiment was API/CPU-bound and did not use GPU acceleration.
