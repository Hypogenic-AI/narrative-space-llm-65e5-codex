# Cloned Repositories

## Matterport3D Simulator

- URL: https://github.com/peteanderson80/Matterport3DSimulator
- Location: `code/matterport3d_simulator/`
- Purpose: Simulator, R2R dataset tooling, baseline VLN agent code, and evaluation scripts.
- Key files:
  - `tasks/R2R/README.md`
  - `tasks/R2R/eval.py`
  - `tasks/R2R/train.py`
  - `tasks/R2R/utils.py`
- Notes: Full simulator use requires Matterport3D data access and substantial rendering dependencies. The R2R annotations downloaded under `datasets/r2r_navigation/` can be used for text-only analysis without building the simulator.

## Tag Map

- URL: https://github.com/leggedrobotics/tagmap
- Location: `code/tagmap/`
- Purpose: Text-based semantic map construction and LLM-grounded navigation planning.
- Key files:
  - `tag_mapping/requirements.txt`
  - `tag_mapping/setup.py`
  - `demos/build_tag_map.ipynb`
  - `demos/localization.ipynb`
  - `evaluation/README.md`
- Notes: Requires PyTorch and Recognize Anything Model checkpoints. Most useful here as a reference for text-map representations and spatial-query APIs.

## StoryAlign

- URL: https://github.com/THU-KEG/StoryAlign
- Location: `code/storyalign/`
- Purpose: Advertised code/data home for the StoryAlign paper.
- Key files:
  - `README.md`
- Notes: Repository is currently a placeholder with only a one-line README. The paper also advertises `THU-KEG/StoryReward`, but that repository was not public at collection time.

## StoryWriter

- URL: https://github.com/THU-KEG/StoryWriter
- Location: `code/storywriter/`
- Purpose: Multi-agent long-story generation framework from the same group as LongStory.
- Key files:
  - `README.md`
- Notes: Useful as a story-generation baseline design: outline agent, planning agent, and writing agent. The associated `THU-KEG/LongStory` dataset was downloaded under `datasets/longstory_ai_generated/`.

## pseudobibeR

- URL: https://github.com/browndw/pseudobibeR
- Location: `code/pseudobiber/`
- Purpose: Extracts Biber-style lexicogrammatical and rhetorical features used in human-vs-LLM style analysis.
- Key files:
  - `R/parse_functions.R`
  - `R/data.R`
  - `man/biber.Rd`
  - `data/word_lists.rda`
- Notes: R package. It does not parse raw text by itself; it consumes spaCy or udpipe parses. For this project, it is the most direct route to feature families such as nominalizations, passives, participial clauses, and coordination patterns.

## interwhen

- URL: https://github.com/microsoft/interwhen
- Location: `code/interwhen/`
- Purpose: Test-time verification framework with maze and SpatialMap examples.
- Key files:
  - `examples/TTSwithVerification/interwhen/spatialmap_example.py`
  - `examples/TTSwithVerification/metaPrompt/spatialmeta.py`
  - `examples/EarlyStopping/spatialmap_example.py`
  - `interwhen/monitors/`
- Notes: Relevant for checking whether generated navigation narratives obey explicit spatial constraints. Requires an LLM server for full examples.
