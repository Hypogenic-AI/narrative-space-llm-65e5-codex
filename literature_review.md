# Literature Review: Narrative Space in LLMs

## Review Scope

### Research Question

Do large language models produce spatial-navigation narratives with structural patterns that differ from human spatial narratives, and can those differences be measured as a distinct LLM "grammar" of narrative space?

### Inclusion Criteria

- Papers on LLM or neural spatial reasoning, navigation, route instructions, or spatial cognition.
- Papers on story generation, story planning, narrative preference, or narrative theory for LLMs.
- Papers providing measurable human-vs-LLM linguistic, rhetorical, lexical, syntactic, or diversity features.
- Papers or datasets that can support automated experiments on human and LLM spatial narratives.

### Exclusion Criteria

- Pure robotics navigation papers without language analysis.
- General LLM reasoning papers without spatial, narrative, or style relevance.
- Very large datasets requiring unavailable gated media unless text annotations are usable independently.

### Search Log

| Date | Query | Source | Results | Notes |
|------|-------|--------|---------|-------|
| 2026-06-08 | "large language models spatial narratives navigation story generation" | paper-finder | stalled | Process did not return; manual search used. |
| 2026-06-08 | "LLM spatial reasoning navigation text-based environments paper arXiv 2024" | web/arXiv | multiple | Found VoT, Tag Map, spatial cognition work. |
| 2026-06-08 | "Do LLMs write like humans Variation in grammatical and rhetorical styles" | web/arXiv/PNAS | direct hit | Key feature-based human-vs-LLM style paper. |
| 2026-06-08 | "Room-to-Room Vision-and-Language Navigation paper PDF arXiv" | web/arXiv/GitHub | direct hits | Found R2R paper, data, simulator. |
| 2026-06-08 | "Plan-And-Write Towards Better Automatic Storytelling arXiv" | web/arXiv | direct hit | Story planning baseline. |
| 2026-06-08 | "StoryAlign reward models story generation human preferences" | web/arXiv/GitHub/HF | direct hit | Recent story-preference benchmark and LongStory dataset. |

## Key Papers

### Vision-and-Language Navigation: Interpreting visually-grounded navigation instructions in real environments

- Authors: Anderson et al.
- Year: 2018
- Key contribution: Introduces Matterport3D Simulator and R2R, a benchmark of human-written indoor navigation instructions.
- Methodology: Crowdworkers wrote three navigation instructions for each sampled route through real Matterport3D indoor scenes.
- Datasets used: Matterport3D and R2R.
- Results: R2R contains 7,189 paths and roughly 21.5k instructions; baseline seq2seq agents substantially trail oracle/shortest-path performance, especially in unseen environments.
- Relevance: Primary human spatial-language source. The instructions encode how people lexicalize room transitions, landmarks, turning, stopping, and goal descriptions.

### Speaker-Follower Models for Vision-and-Language Navigation

- Authors: Fried et al.
- Year: 2018
- Key contribution: Uses a learned speaker model to synthesize navigation instructions and improve an instruction-following agent.
- Methodology: Speaker-driven data augmentation, pragmatic reasoning over candidate trajectories, panoramic action space.
- Datasets used: R2R.
- Results: More than doubled success over earlier baselines in the R2R setting.
- Relevance: Provides a precedent for comparing human and model-generated navigation instructions.

### Room-Across-Room

- Authors: Ku et al.
- Year: 2020
- Key contribution: Larger multilingual VLN dataset with dense word-to-pose grounding.
- Methodology: Multilingual route-instruction collection with synchronized pose traces.
- Datasets used: RxR plus R2R.
- Relevance: Useful future extension if experiments need time-aligned route language; not downloaded here because R2R is sufficient and lighter.

### Mind's Eye of LLMs: Visualization-of-Thought

- Authors: Wu et al.
- Year: 2024
- Key contribution: Proposes prompting LLMs to visualize state after reasoning steps.
- Methodology: Tests GPT-4 variants on natural-language navigation, visual navigation, and visual tiling in 2D grids.
- Datasets used: Generated square-map and tiling tasks.
- Results: VoT improves GPT-4 over CoT across tasks, for example visual navigation 40.77 vs 37.02 and visual tiling 14.72 vs 9.48, but state visualization accuracy remains low.
- Relevance: Strong evidence that verbal reasoning alone is brittle for spatial tasks; suggests experiments should look for whether LLM stories maintain an implicit map.

### Tag Map

- Authors: Zhang et al.
- Year: 2024
- Key contribution: Builds explicit text-based maps that can ground LLM planning.
- Methodology: Uses image-tagging models to create localized semantic tag maps and lets GPT-4 query the map through function calls.
- Datasets used: Matterport3D/OpenScene-style scene data and real-robot data.
- Results: Tag maps achieved competitive object localization precision/recall with much lower memory than embedding maps; real-robot demos showed task-grounded navigation.
- Relevance: Provides a representation idea for evaluating narratives: convert generated stories into explicit location/object/transition graphs.

### Spatial Representation of LLMs in 2D Scene

- Authors: Wu and Deng
- Year: 2025
- Key contribution: Compares LLM spatial preposition behavior with human spatial-representation data.
- Methodology: Spatial generation and rating tasks over 2D scenes; compared GPT-4, GPT-3.5, Qwen, Llama, and others to human data.
- Results: LLMs resemble humans in preferring vertical spatial terms, but do not reproduce human axis-specific representation patterns; GPT-4 is stronger on above/below/left than right.
- Relevance: Supports the hypothesis that LLM spatial language can be superficially human-like while diverging in deeper representation.

### Evaluating and Enhancing Spatial Cognition Abilities of LLMs

- Authors: Yang et al.
- Year: 2025
- Key contribution: Benchmarks landmark, route, and survey knowledge in LLMs and proposes Hybrid Mind.
- Methodology: 105 manually crafted spatial cognition questions across seven categories; tool-augmented mental-map builder with deterministic GIS algorithms.
- Results: Mainstream LLMs performed poorly across most tasks, especially route and survey knowledge; GPT-4-turbo answered fewer than one-quarter correctly, while Hybrid Mind reached 70.48%.
- Relevance: Directly frames navigation language as landmark-route-survey transformations. PDF download was blocked, but the article full text was accessible.

### Do LLMs write like humans?

- Authors: Reinhart et al.
- Year: 2024/2025
- Key contribution: Measures grammatical and rhetorical style differences between humans, GPT-4o, and Llama 3 variants.
- Methodology: Parallel human/LLM corpora; Biber-style features; random forest classification.
- Datasets used: Human-AI Parallel English corpus and COCA AI Parallel corpus.
- Results: LLMs systematically overuse features such as present participial clauses, subject that-clauses, nominalizations, and phrasal coordination; instruction-tuned models differ more from humans than base Llama models.
- Relevance: Supplies the core measurement framework for an "LLM grammar" of spatial narrative.

### StoryAlign

- Authors: Xia et al.
- Year: 2026
- Key contribution: Evaluates and trains reward models for story preferences.
- Methodology: STORYRMB benchmark with 1,133 human-verified prompt/story preference instances across coherence, creativity, characterization, fluency, and relevance; builds about 100k preference pairs.
- Results: Existing reward models struggle; best general model reached 66.3% while StoryReward-Qwen reached 75.0% average.
- Relevance: Confirms that LLM stories diverge from human preferences on narrative structure, not just grammar.

### Narrative Theory-Driven LLM Methods Survey

- Authors: Liu, Joshi, Dawson
- Year: 2026
- Key contribution: Surveys narrative-theory-driven LLM methods and argues against a single generic narrative-quality benchmark.
- Relevance: Supports using theory-specific metrics: spatial deixis, route continuity, landmark introduction, discourse order, map consistency, and narrative perspective.

## Common Methodologies

- Feature-based corpus comparison: Use Biber/pseudobibeR-style grammatical and rhetorical counts, lexical diversity, syntactic complexity, and classifier feature importance.
- Route graph extraction: Extract entities, places, landmarks, turns, and transitions from text; evaluate graph/map consistency.
- Controlled spatial QA: Use bAbI path and positional tasks or generated map tasks to isolate spatial reasoning failures.
- Human vs model parallel prompts: Hold prompts fixed and compare human-authored or human-continuation text against LLM completions.
- Preference and human evaluation: Rate stories by coherence, relevance, creativity, characterization, and fluency.

## Standard Baselines

- Human corpus baseline: R2R human route instructions and spatially filtered WritingPrompts.
- LLM generation baseline: Generate stories from identical building-navigation prompts across multiple models/settings.
- Text-only feature baseline: Biber features, lexical diversity, sentence length, POS/dependency patterns.
- Spatial consistency baseline: Deterministic path parser or graph validator over extracted locations and transitions.
- Story-quality baseline: Coherence/relevance/fluency metrics plus StoryAlign-style preference criteria.

## Evaluation Metrics

- Linguistic features: nominalizations, participial clauses, passives, coordination, prepositional phrases, type-token ratios, lexical repetition.
- Spatial narrative features: count/order of landmarks, place introductions, deixis, turn verbs, directional terms, revisits, impossible transitions, route closure, perspective shifts.
- Classification metrics: human-vs-LLM accuracy, F1, ROC-AUC, feature importance.
- Spatial correctness: path validity, graph consistency, percentage of resolvable transitions, landmark-route-survey transformations.
- Narrative quality: coherence, creativity, characterization, fluency, relevance, human preference accuracy.

## Datasets in the Literature and Workspace

- R2R: Human indoor route instructions. Best primary dataset for human spatial-navigation language.
- RxR: Larger multilingual extension with word-pose alignments. Useful later, not downloaded now.
- Human-AI Parallel Corpus: Human/LLM text pairs for feature baselines.
- WritingPrompts: Human fiction prompts and stories; workspace includes a 500-record spatial keyword sample.
- LongStory: AI-generated long stories from StoryWriter; useful for AI story contrast.
- bAbI tasks 17 and 19: Controlled positional and path-finding text reasoning.

## Gaps and Opportunities

- Existing VLN datasets are instructions, not full literary stories; experiments should distinguish route-instruction grammar from narrative-prose grammar.
- Story-generation benchmarks rarely focus on spatial consistency or navigable built environments.
- LLM spatial-language outputs may look fluent while failing survey-map consistency; this should be measured directly.
- Human-vs-LLM style studies are mostly genre-level, not spatial-narrative-specific.
- Existing reward models for story generation may reward fluency/verbosity more than coherent spatial narrative structure.

## Recommendations for Our Experiment

- Primary human spatial baseline: R2R instructions, supplemented by spatially filtered WritingPrompts for more narrative prose.
- Primary AI comparison data: Generate matched spatial-navigation stories from current LLMs; also use LongStory as a general AI-story background corpus.
- Core hypothesis test: Extract linguistic features and spatial-route graphs from human and LLM texts, then test whether model outputs form a separable cluster.
- Recommended feature families:
  - Biber/pseudobibeR grammatical features.
  - Spatial preposition and direction-term distributions.
  - Landmark introduction/reuse patterns.
  - Transition graph validity and revisits.
  - Discourse ordering: egocentric route order vs survey/map-like summaries.
- Recommended baselines:
  - Human R2R vs LLM-rewritten R2R route stories.
  - Human WritingPrompts spatial sample vs LLM completions from same prompts.
  - Controlled bAbI path/position probes for spatial consistency sanity checks.
- Recommended metrics:
  - Human-vs-LLM classifier performance with feature ablation.
  - Spatial graph consistency score.
  - Lexical/syntactic diversity.
  - StoryAlign-style human preference dimensions if human or LLM-judge evaluation is added.
