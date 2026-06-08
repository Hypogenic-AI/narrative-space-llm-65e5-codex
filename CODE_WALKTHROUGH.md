# Code Walkthrough

## Structure

- `src/common.py`: shared paths, JSONL helpers, text cleanup, tokenization, and seeding.
- `src/prepare_corpora.py`: samples R2R and WritingPrompts records, writes human texts, writes exact LLM prompts, and records environment metadata.
- `src/generate_llm_outputs.py`: calls the OpenAI Responses API with cache/resume behavior and saves raw model outputs.
- `src/features.py`: extracts interpretable generic, spatial, and narrative features.
- `src/analyze_results.py`: runs feature tests, classifier ablations, feature importance, external LongStory scoring, and plot generation.

## Data Flow

Raw datasets -> `prepare_corpora.py` -> `results/human_corpus.jsonl` and `results/prompts/llm_prompts.jsonl`

Prompts -> `generate_llm_outputs.py` -> `results/model_outputs/gpt-5.4-mini_outputs.jsonl`

Human plus LLM texts -> `analyze_results.py` -> `results/features.csv`, `results/evaluations/`, and `figures/`

## Reproduction

```bash
source .venv/bin/activate
python src/prepare_corpora.py
python src/generate_llm_outputs.py --model gpt-5.4-mini --temperature 0.7 --max-output-tokens 320
python src/analyze_results.py --model gpt-5.4-mini
```

The generation step reads `OPENAI_API_KEY`. It is safe to rerun because completed prompt IDs are cached in the output JSONL.

## Expected Outputs

- `results/config.json`
- `results/human_corpus.jsonl`
- `results/prompts/llm_prompts.jsonl`
- `results/model_outputs/gpt-5.4-mini_outputs.jsonl`
- `results/features.csv`
- `results/evaluations/classification_metrics.csv`
- `results/evaluations/feature_tests.csv`
- `figures/classification_accuracy.png`
- `figures/key_feature_distributions.png`
- `figures/top_logistic_coefficients.png`

On the completed run, the generation step took 6 minutes 33 seconds and analysis took about 1 minute on CPU.
