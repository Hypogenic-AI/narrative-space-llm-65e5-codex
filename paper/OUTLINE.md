# Outline: Spatial Narrative Fingerprints in LLM-Generated Built-Space Stories

## Title
- Spatial Narrative Fingerprints in LLM-Generated Built-Space Stories
- Main claim: LLM spatial stories are separable from human spatial texts by interpretable spatial and narrative features.

## Abstract
- Motivate synthetic spatial stories and route-like text.
- State paired corpus: 114 human texts and 114 GPT-5.4-mini outputs from R2R and WritingPrompts.
- Report main metrics: 97.4% all-feature accuracy, 96.5% no-length accuracy, 87.7% spatial-only accuracy, and WritingPrompts control results.
- Qualify interpretation as a prompt- and genre-conditioned textual fingerprint.

## Introduction
- Hook: fluent spatial text can still encode biased route structure.
- Importance: synthetic data, interactive fiction, and embodied-agent traces.
- Gap: VLN work studies human route instructions; LLM style work studies general text, not spatial narrative grammar.
- Approach: paired corpora, regex feature families, statistical tests, classifier ablations, external LongStory sanity check.
- Preview: strong separability beyond length and interpretable LLM profile.
- Contributions:
  - propose spatial-narrative feature profile,
  - build balanced corpus and GPT-5.4-mini generation set,
  - test separability and ablations,
  - qualify limits with prose control and external AI check.

## Related Work
- Human navigation language: R2R, Speaker-Follower, RxR.
- LLM spatial reasoning: Visualization-of-Thought, Tag Map, spatial representation in 2D scenes, Hybrid Mind.
- Human-vs-LLM style and story generation: Reinhart et al., WritingPrompts, StoryAlign, narrative-theory survey.

## Methodology
- Problem formulation: classify author class from transparent features.
- Datasets: R2R 80 pairs, WritingPrompts 34 pairs, LongStory 80 external excerpts.
- Generation: GPT-5.4-mini, temperature 0.7, max output tokens 320, 114 calls, cached prompts.
- Features: length/generic, spatial grammar, narrative embellishment.
- Evaluation: Mann-Whitney U, BH correction, Cohen's d, Cliff's delta, 5-fold stratified logistic regression, permutation tests.
- Baselines: chance, length-only, generic, spatial-only, narrative-only, all without length, all features.

## Results
- Corpus balance table.
- Classification and ablation table with confidence intervals.
- Figures: classification accuracy, key feature distributions, top coefficients.
- Feature differences table for full corpus and WritingPrompts control.
- External LongStory check: weak transfer.

## Discussion
- Interpretation: GPT-5.4-mini converts spatial movement into first-person sensory scenes with landmark reuse and closure.
- Why the prose control matters.
- Limits: R2R genre confound, small WritingPrompts subset, single model, first-person prompt, regex features, no human coherence judgments, API drift.
- Broader implications for synthetic data and embodied-agent evaluation.

## Conclusion
- Restate measurable but qualified fingerprint.
- Future work: human-written matched first-person navigation stories, spatial graph consistency annotations, multi-model comparison.
