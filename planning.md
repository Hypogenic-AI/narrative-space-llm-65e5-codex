# Narrative Space in LLMs: Research Plan

## Motivation & Novelty Assessment

### Why This Research Matters
LLM stories are increasingly used as synthetic narrative data, interactive-fiction content, and planning traces for embodied agents. If model-generated spatial narratives follow a distinct grammar, they may sound fluent while encoding different assumptions about routes, landmarks, perspective, and movement than human-authored spatial language.

### Gap in Existing Work
The gathered literature shows strong work on human route instructions (R2R), LLM spatial reasoning failures, and broad human-vs-LLM stylistic fingerprints. What is missing is a targeted corpus experiment that asks whether human and LLM texts about moving through built space are separable by spatial-narrative features, not only by generic synthetic-text style.

### Our Novel Contribution
This study will build a small matched spatial-narrative benchmark from existing human data and new real GPT-5.4-mini generations. It will test a proposed "spatial grammar" feature set: direction terms, landmark introductions, route-sequence markers, egocentric perspective, survey-language use, movement density, narrative closure, and repetition/templating.

### Experiment Justification
- Experiment 1: R2R route transformation. Needed to test whether an LLM asked to narrativize a concrete indoor route differs from human route language over the same kind of spatial path.
- Experiment 2: WritingPrompts spatial prose. Needed to reduce the route-instruction vs fiction confound by comparing human prose to LLM prose generated from the same spatial prompts.
- Experiment 3: Feature-family ablation. Needed to determine whether spatial features add explanatory signal beyond generic lexical/style features.
- Experiment 4: Error and validity analysis. Needed to identify whether classifier separation reflects spatial grammar, genre artifacts, length, or prompt leakage.

## Research Question
When current LLMs are asked to write stories involving movement through built space, do their spatial narratives diverge measurably from human spatial narratives, and can those divergences be described as a distinct spatial-narrative grammar?

## Background and Motivation
R2R provides human indoor navigation instructions, while WritingPrompts gives human fiction-like prose with spatial cues. Prior work shows LLMs have recognizable linguistic tics and often struggle with spatial representation, but no pre-gathered paper directly tests the spatial structure of LLM narrative prose against human spatial texts. A feature-based corpus study can provide an initial, reproducible answer.

## Hypothesis Decomposition
- H1: Human and LLM spatial texts are classifiable above chance using engineered narrative-space features.
- H2: Spatial feature families alone classify better than chance and improve over generic style features.
- H3: LLM spatial narratives use more formulaic sequencing, explicit closure, sensory/affective embellishment, and first-person route framing than human route instructions.
- H4: LLM prose differs from human spatial prose even when prompts are matched, though effects may be weaker than in R2R because genre is more controlled.

Independent variables are author class (human vs LLM), source corpus (R2R vs WritingPrompts), and feature family (generic, spatial, narrative, all). Dependent variables are feature values, classifier accuracy/F1/ROC-AUC, and per-feature effect sizes. Alternative explanations include genre mismatch, length differences, prompt-induced style, and LLM copying of route seed text.

## Proposed Methodology

### Approach
Create two paired corpora. For R2R, sample 80 routes and generate one GPT-5.4-mini first-person micro-story from the route instructions. Pair each with one human R2R instruction. For WritingPrompts, use all prompts whose prompt text contains spatial/built-environment terms and generate GPT-5.4-mini stories from the same prompt; compare with the corresponding human story excerpt. Extract interpretable features and evaluate both statistical differences and supervised separability.

### Experimental Steps
1. Validate datasets and sample fixed records with seed 42, preserving IDs and source labels.
2. Generate LLM outputs with the OpenAI API using `gpt-5.4-mini`, temperature 0.7, max output tokens 320, and cached JSONL outputs.
3. Normalize human and LLM texts to comparable excerpts where needed, without altering lexical content.
4. Extract feature families: generic style, spatial terms, route grammar, and narrative embellishment.
5. Run descriptive EDA, group comparisons, feature ablations, and classifiers.
6. Inspect top coefficients and misclassified examples to assess whether spatial grammar rather than length or genre dominates.

### Baselines
- Chance baseline: 50% balanced human-vs-LLM classification.
- Generic-style baseline: lexical/sentence/formulaic features without spatial features.
- Spatial-only baseline: direction, landmark, motion, route-order, and perspective features.
- Source-specific baselines: R2R only and WritingPrompts only to expose genre sensitivity.

### Evaluation Metrics
- Descriptive feature statistics: mean, standard deviation, medians, and bootstrap confidence intervals.
- Statistical tests: Mann-Whitney U for non-normal independent groups; Welch tests as sensitivity checks for approximately normal features.
- Effect sizes: Cohen's d and Cliff's delta for key feature differences.
- Classification: stratified 5-fold cross-validated accuracy, F1, ROC-AUC, and permutation-test p-value where feasible.
- Feature importance: standardized logistic regression coefficients and random forest impurity/permutation importances.

### Statistical Analysis Plan
Use alpha = 0.05 with Benjamini-Hochberg correction over the planned feature comparisons. Because text-feature distributions are often skewed, Mann-Whitney U is primary. Classification performance will be reported with fold-level means and 95% bootstrap confidence intervals. Ablations will be compared descriptively and, when fold pairing permits, with paired tests across cross-validation folds.

## Expected Outcomes
Evidence for the hypothesis would include above-chance classification, spatial-only features above chance, and large corrected effects in route-sequencing or perspective features. Evidence against it would be weak classification after controlling for length/source or spatial features adding little beyond generic style.

## Timeline and Milestones
- Setup and resource validation: 10 minutes.
- Planning and preregistration: 20 minutes.
- Implementation: 60 minutes.
- LLM generation and experiment execution: 60-90 minutes depending on API latency.
- Analysis and visualization: 30-45 minutes.
- Report and reproducibility validation: 30 minutes.

## Potential Challenges
- API failures or rate limits: cache every response, retry with exponential backoff, and document any missing outputs.
- Genre confound: report R2R and WritingPrompts separately and include generic-feature ablations.
- Unequal lengths: use normalized per-1,000-token features and include length-only checks.
- Feature validity: keep features interpretable and label approximate regex-based measures honestly.
- Small WritingPrompts prompt-spatial subset: treat it as a prose control rather than the sole basis for broad claims.

## Success Criteria
The research succeeds if it produces a reproducible corpus, real LLM outputs, interpretable feature tables, statistical comparisons, classifier/ablation results, visualizations, and a REPORT.md that gives a clear, qualified answer to the research question.
