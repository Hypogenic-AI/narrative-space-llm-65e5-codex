# Downloaded Papers

Primary paper PDFs are stored directly in this directory. Chunked PDFs for detailed reading are in `papers/pages/`.

## Papers

1. [Vision-and-Language Navigation: Interpreting visually-grounded navigation instructions in real environments](1711.07280_vision_language_navigation_r2r.pdf)
   - Authors: Peter Anderson, Qi Wu, Damien Teney, Jake Bruce, Mark Johnson, Niko Sunderhauf, Ian Reid, Stephen Gould, Anton van den Hengel
   - Year: 2018
   - Source: arXiv/CVPR
   - Why relevant: Introduces the R2R dataset of human-written indoor navigation instructions and standard VLN evaluation.

2. [Hierarchical Neural Story Generation](1805.04833_learning_to_generate_long_form_stories.pdf)
   - Authors: Angela Fan, Mike Lewis, Yann Dauphin
   - Year: 2018
   - Source: ACL/arXiv
   - Why relevant: Foundational neural story-generation paper using WritingPrompts; motivates planning and long-range coherence measures.

3. [Speaker-Follower Models for Vision-and-Language Navigation](1806.02724_speaker_follower_vln.pdf)
   - Authors: Daniel Fried, Ronghang Hu, Volkan Cirik, Anna Rohrbach, Jacob Andreas, Louis-Philippe Morency, Taylor Berg-Kirkpatrick, Kate Saenko, Dan Klein, Trevor Darrell
   - Year: 2018
   - Source: NeurIPS/arXiv
   - Why relevant: Establishes generated navigation-instruction baselines and pragmatic reasoning on R2R.

4. [Plan-And-Write: Towards Better Automatic Storytelling](1811.05701_plan_and_write_storytelling.pdf)
   - Authors: Lili Yao, Nanyun Peng, Ralph Weischedel, Kevin Knight, Dongyan Zhao, Rui Yan
   - Year: 2018/2019
   - Source: AAAI/arXiv
   - Why relevant: Shows explicit storyline planning improves coherence, diversity, and topicality in generated stories.

5. [Room-Across-Room: Multilingual Vision-and-Language Navigation with Dense Spatiotemporal Grounding](2010.07954_room_across_room_vln.pdf)
   - Authors: Alexander Ku, Peter Anderson, Roma Patel, Eugene Ie, Jason Baldridge
   - Year: 2020
   - Source: EMNLP/arXiv
   - Why relevant: Extends R2R with larger multilingual instructions and word-to-pose grounding.

6. [The Curious Decline of Linguistic Diversity: Training Language Models on Synthetic Text](2311.09807_synthetic_text_linguistic_diversity.pdf)
   - Authors: Yanzhu Guo, Guokan Shang, Michalis Vazirgiannis, Chloe Clavel
   - Year: 2023
   - Source: arXiv
   - Why relevant: Provides lexical, syntactic, and semantic diversity metrics for model-generated text collapse.

7. [Mind's Eye of LLMs: Visualization-of-Thought Elicits Spatial Reasoning in Large Language Models](2404.03622_visualization_of_thought_spatial_reasoning.pdf)
   - Authors: Wenshan Wu, Shaoguang Mao, Yadong Zhang, Yan Xia, Li Dong, Lei Cui, Furu Wei
   - Year: 2024
   - Source: arXiv
   - Why relevant: Tests LLM spatial reasoning on navigation/tiling tasks and introduces visualization-of-thought prompting.

8. [Tag Map: A Text-Based Map for Spatial Reasoning and Navigation with Large Language Models](2409.15451_tag_map_text_based_map_llm_navigation.pdf)
   - Authors: Mike Zhang, Kaixian Qu, Vaishakh Patil, Cesar Cadena, Marco Hutter
   - Year: 2024
   - Source: CoRL/arXiv
   - Why relevant: Demonstrates text-based spatial maps as LLM-readable scene context for navigation plans.

9. [Do LLMs write like humans? Variation in grammatical and rhetorical styles](2410.16107_llms_write_like_humans_styles.pdf)
   - Authors: Alex Reinhart, David West Brown, Ben Markey, Michael Laudenbach, Kachatad Pantusen, Ronald Yurko, Gordon Weinberg
   - Year: 2024/2025
   - Source: arXiv/PNAS
   - Why relevant: Directly supports measuring systematic LLM-vs-human grammar and rhetorical differences.

10. [Foundation Models for Geospatial Reasoning: Assessing the Capabilities of Large Language Models in Understanding Geometries and Topological Spatial Relations](2505.17136_geospatial_reasoning_llms.pdf)
    - Authors: Yuhan Ji, Song Gao, Ying Nie, Ivan Majic, Krzysztof Janowicz
    - Year: 2025
    - Source: arXiv
    - Why relevant: Evaluates LLM handling of natural-language and formal spatial/topological relations.

11. [Spatial Representation of Large Language Models in 2D Scene](wu_2025_spatial_representation_llms_2d_scene.pdf)
    - Authors: Wenya Wu, Weihong Deng
    - Year: 2025
    - Source: ACL GEM Workshop
    - Why relevant: Compares LLM spatial-preposition behavior with human spatial-representation patterns.

12. [Narrative Theory-Driven LLM Methods for Automatic Story Generation and Understanding: A Survey](2602.15851_narrative_theory_llm_survey.pdf)
    - Authors: David Y. Liu, Aditya Joshi, Paul Dawson
    - Year: 2026
    - Source: arXiv
    - Why relevant: Recent survey connecting LLM narrative methods with narratology and theory-driven metrics.

13. [The Rise of Verbal Tics in Large Language Models: A Systematic Analysis Across Frontier Models](2604.19139_verbal_tics_llms.pdf)
    - Authors: Shuai Wu, Xue Li, Yanna Feng, Yufang Li, Zhijun Wang, Ran Wang
    - Year: 2026
    - Source: arXiv technical report
    - Why relevant: Emerging evidence for repetitive, formulaic model-specific language patterns. Treat cautiously because it is a preprint/technical report.

14. [StoryAlign: Evaluating and Training Reward Models for Story Generation](2605.04831_storyalign_story_reward_models.pdf)
    - Authors: Haotian Xia, Hao Peng, Yunjia Qi, Xiaozhi Wang, Bin Xu, Lei Hou, Juanzi Li
    - Year: 2026
    - Source: ICLR/arXiv
    - Why relevant: Recent story-preference benchmark showing LLM stories still diverge from human-authored narratives.

## Access Notes

- The Taylor & Francis article "Evaluating and enhancing spatial cognition abilities of large language models" was reviewed from the web full-text page, but the PDF endpoint returned HTTP 403 from command-line download attempts. It is therefore referenced in `literature_review.md` and `resources.md` but not stored as a PDF here.
- Primary PDFs were validated with `pypdf`; all 14 downloaded files parsed successfully.
