# Resources Catalog

## Summary

This document catalogs resources gathered for the research project "Narrative Space in LLMs." The focus is on human spatial-navigation language, LLM spatial reasoning, story generation, and measurable human-vs-LLM style differences.

## Papers

Total primary PDFs downloaded: 14

| Title | Authors | Year | File | Key Info |
|-------|---------|------|------|----------|
| Vision-and-Language Navigation | Anderson et al. | 2018 | `papers/1711.07280_vision_language_navigation_r2r.pdf` | R2R human indoor route instructions. |
| Hierarchical Neural Story Generation | Fan et al. | 2018 | `papers/1805.04833_learning_to_generate_long_form_stories.pdf` | WritingPrompts story generation baseline. |
| Speaker-Follower Models for VLN | Fried et al. | 2018 | `papers/1806.02724_speaker_follower_vln.pdf` | Synthetic navigation instructions and pragmatic reasoning. |
| Plan-And-Write | Yao et al. | 2018/2019 | `papers/1811.05701_plan_and_write_storytelling.pdf` | Explicit storyline planning. |
| Room-Across-Room | Ku et al. | 2020 | `papers/2010.07954_room_across_room_vln.pdf` | Multilingual VLN with word-pose grounding. |
| Curious Decline of Linguistic Diversity | Guo et al. | 2023 | `papers/2311.09807_synthetic_text_linguistic_diversity.pdf` | Lexical/syntactic/semantic diversity metrics. |
| Mind's Eye of LLMs | Wu et al. | 2024 | `papers/2404.03622_visualization_of_thought_spatial_reasoning.pdf` | Visualization-of-thought for spatial reasoning. |
| Tag Map | Zhang et al. | 2024 | `papers/2409.15451_tag_map_text_based_map_llm_navigation.pdf` | Text-map grounding for LLM navigation. |
| Do LLMs write like humans? | Reinhart et al. | 2024/2025 | `papers/2410.16107_llms_write_like_humans_styles.pdf` | Biber-style human-vs-LLM feature analysis. |
| Foundation Models for Geospatial Reasoning | Ji et al. | 2025 | `papers/2505.17136_geospatial_reasoning_llms.pdf` | LLM topological spatial relation reasoning. |
| Spatial Representation of LLMs in 2D Scene | Wu and Deng | 2025 | `papers/wu_2025_spatial_representation_llms_2d_scene.pdf` | Human-vs-LLM spatial-preposition behavior. |
| Narrative Theory-Driven LLM Methods | Liu et al. | 2026 | `papers/2602.15851_narrative_theory_llm_survey.pdf` | Narrative theory and LLM methods survey. |
| Rise of Verbal Tics in LLMs | Wu et al. | 2026 | `papers/2604.19139_verbal_tics_llms.pdf` | Emerging formulaic style analysis; treat cautiously. |
| StoryAlign | Xia et al. | 2026 | `papers/2605.04831_storyalign_story_reward_models.pdf` | Story preference reward benchmark. |

Additional reviewed but not downloaded:

- Yang et al. 2025, "Evaluating and enhancing spatial cognition abilities of large language models." The full article page was accessible, but the PDF endpoint returned HTTP 403 to command-line download.

See `papers/README.md` for detailed descriptions.

## Datasets

Total datasets downloaded or sampled: 6

| Name | Source | Size | Task | Location | Notes |
|------|--------|------|------|----------|-------|
| R2R Navigation Instructions | Matterport3DSimulator Dropbox links | 7,189 paths; 21,582 instructions | Human route language | `datasets/r2r_navigation/` | Primary human spatial-navigation corpus. |
| Human-AI Parallel Corpus | `browndw/human-ai-parallel-corpus` | 66,320 rows; 183 MB | Human-vs-LLM style | `datasets/human_ai_parallel_corpus/` | Directly tied to Reinhart et al. |
| bAbI Positional Reasoning | `RawthiL/babi_tasks` | 2,000 rows | Controlled spatial relations | `datasets/babi_positional_reasoning/` | Synthetic sanity-check probe. |
| bAbI Path Finding | `RawthiL/babi_tasks` | 2,000 rows | Controlled route reasoning | `datasets/babi_path_finding/` | Synthetic path reasoning probe. |
| WritingPrompts Spatial Sample | `euclaise/writingprompts` | 500 sampled rows | Human narrative prose | `datasets/writingprompts_spatial_sample/` | Keyword-filtered for spatial terms. |
| LongStory | `THU-KEG/LongStory` | 5,279 rows; 185 MB | AI-generated long stories | `datasets/longstory_ai_generated/` | General AI-story contrast corpus. |

See `datasets/README.md` for download and loading instructions.

## Code Repositories

Total repositories cloned: 6

| Name | URL | Purpose | Location | Notes |
|------|-----|---------|----------|-------|
| Matterport3D Simulator | https://github.com/peteanderson80/Matterport3DSimulator | R2R/VLN tools | `code/matterport3d_simulator/` | Full simulator requires gated Matterport data. |
| Tag Map | https://github.com/leggedrobotics/tagmap | Text-map grounding | `code/tagmap/` | Requires RAM checkpoints and PyTorch for full use. |
| StoryAlign | https://github.com/THU-KEG/StoryAlign | StoryAlign release placeholder | `code/storyalign/` | Currently only a README stub. |
| StoryWriter | https://github.com/THU-KEG/StoryWriter | Multi-agent story generation | `code/storywriter/` | Associated LongStory dataset downloaded. |
| pseudobibeR | https://github.com/browndw/pseudobibeR | Biber-style feature extraction | `code/pseudobiber/` | R package; consumes spaCy/udpipe parses. |
| interwhen | https://github.com/microsoft/interwhen | Test-time spatial/maze verification | `code/interwhen/` | Useful for spatial consistency validators. |

See `code/README.md` for details.

## Resource Gathering Notes

### Search Strategy

The paper-finder service was attempted first in diligent mode for "large language models spatial narratives navigation story generation" but did not return output and had to be terminated. Manual search then covered arXiv, ACL Anthology, Hugging Face papers/datasets, GitHub, and publisher pages using focused queries for spatial reasoning, VLN, story generation, narrative theory, and LLM writing style.

### Selection Criteria

- Direct relevance to spatial narration, navigation, or spatial cognition.
- Availability of text datasets or measurable features.
- Coverage of both human-language baselines and LLM-generation behavior.
- Practical usefulness for downstream experiments.

### Challenges Encountered

- Taylor & Francis PDF download for Yang et al. 2025 returned HTTP 403 despite a browser-like request; the full article page was reviewed instead.
- `facebook/babi_qa` cannot be loaded by current Hugging Face `datasets` because dataset scripts are no longer supported; `RawthiL/babi_tasks` was used as a no-code mirror.
- The StoryAlign paper advertises `THU-KEG/StoryReward`, but that GitHub repository was not public. `THU-KEG/StoryAlign` exists but is currently a placeholder.

### Gaps and Workarounds

- No existing dataset directly pairs human and LLM stories about the same indoor route. Recommended workaround: prompt LLMs to rewrite R2R routes as stories and compare with human route instructions plus WritingPrompts spatial prose.
- R2R is instruction-style rather than literary narrative. WritingPrompts spatial samples partially address prose style but lack explicit route labels.
- Full Matterport images were not downloaded because access is gated and unnecessary for text-only narrative analysis.

## Recommendations for Experiment Design

1. Primary datasets: Use R2R for human route language, WritingPrompts spatial sample for human narrative prose, and generated LLM outputs from matched prompts for the main comparison.
2. Baseline methods: Use pseudobibeR/Biber features, lexical diversity, and spatial graph consistency. Add bAbI path/position probes as controlled sanity checks.
3. Evaluation metrics: Human-vs-LLM classifier accuracy, feature ablation, route graph validity, landmark reuse, directional term distributions, and StoryAlign-style narrative dimensions.
4. Code to reuse: `code/pseudobiber` for feature definitions, `code/matterport3d_simulator/tasks/R2R` for data format/evaluation concepts, `code/interwhen` for verifier design, and `code/storywriter` as a story-generation architecture reference.

## Research Execution Artifacts

The automated execution completed the recommended primary experiment using real GPT-5.4-mini API outputs.

### Created During Execution

| Artifact | Location | Description |
|---|---|---|
| Research plan | `planning.md` | Motivation, novelty, hypotheses, and preregistered analysis plan. |
| Human comparison corpus | `results/human_corpus.jsonl` | 80 R2R human instructions and 34 WritingPrompts human excerpts. |
| LLM prompt set | `results/prompts/llm_prompts.jsonl` | Exact 114 prompts sent to GPT-5.4-mini. |
| Raw LLM outputs | `results/model_outputs/gpt-5.4-mini_outputs.jsonl` | 114 real model generations plus token usage metadata. |
| Feature table | `results/features.csv` | Extracted generic, spatial, and narrative features. |
| Statistical tests | `results/evaluations/feature_tests.csv` | Mann-Whitney U tests, BH q-values, and effect sizes. |
| Classifier metrics | `results/evaluations/classification_metrics.csv` | Cross-validated human-vs-LLM ablations. |
| Figures | `figures/` | Accuracy, feature-distribution, and coefficient plots. |
| Final report | `REPORT.md` | Main research deliverable with actual results. |

### Execution Summary

- Model: `gpt-5.4-mini`
- API parameters: temperature 0.7, max output tokens 320
- Generated outputs: 114
- Main corpus: 228 texts, balanced human vs LLM
- External sanity-check corpus: 80 LongStory AI excerpts
- Token usage: 20,316 input tokens, 29,078 output tokens, 49,394 total tokens
- Key result: all non-length features classified human vs LLM at 96.5% accuracy; spatial-only features classified at 87.7% aggregate accuracy and 83.8% on the WritingPrompts prose-control subset.
