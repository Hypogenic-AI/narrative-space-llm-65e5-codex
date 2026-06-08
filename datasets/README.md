# Downloaded Datasets

This directory contains datasets for the research project. Data files are not intended to be committed to git; `datasets/.gitignore` excludes them while preserving documentation and small samples.

## Dataset 1: R2R Navigation Instructions

### Overview
- Source: Matterport3DSimulator R2R download links
- Location: `datasets/r2r_navigation/`
- Size: 7,189 paths and 21,582 instructions across train/validation/test annotation files
- Format: JSON
- Task: Human-written indoor route instructions for navigation through real buildings
- Splits: train 14,039 instructions; val_seen 1,021; val_unseen 2,349; test 4,173
- Sample: `datasets/r2r_navigation/samples/r2r_samples.json`

### Download Instructions

```bash
mkdir -p datasets/r2r_navigation/raw
curl -L 'https://www.dropbox.com/s/hh5qec8o5urcztn/R2R_train.json?dl=1' -o datasets/r2r_navigation/raw/R2R_train.json
curl -L 'https://www.dropbox.com/s/8ye4gqce7v8yzdm/R2R_val_seen.json?dl=1' -o datasets/r2r_navigation/raw/R2R_val_seen.json
curl -L 'https://www.dropbox.com/s/p6hlckr70a07wka/R2R_val_unseen.json?dl=1' -o datasets/r2r_navigation/raw/R2R_val_unseen.json
curl -L 'https://www.dropbox.com/s/w4pnbwqamwzdwd1/R2R_test.json?dl=1' -o datasets/r2r_navigation/raw/R2R_test.json
```

### Loading

```python
import json
from pathlib import Path

train = json.loads(Path("datasets/r2r_navigation/raw/R2R_train.json").read_text())
```

## Dataset 2: Human-AI Parallel Corpus

### Overview
- Source: Hugging Face `browndw/human-ai-parallel-corpus`
- Location: `datasets/human_ai_parallel_corpus/`
- Size: 66,320 rows, about 183 MB saved to disk
- Format: Hugging Face Dataset
- Task: Compare human and LLM-generated text using linguistic/rhetorical features
- Sample: `datasets/human_ai_parallel_corpus/samples/sample.json`

### Download Instructions

```python
from datasets import load_dataset

dataset = load_dataset("browndw/human-ai-parallel-corpus")
dataset.save_to_disk("datasets/human_ai_parallel_corpus")
```

### Loading

```python
from datasets import load_from_disk

dataset = load_from_disk("datasets/human_ai_parallel_corpus")
```

## Dataset 3: bAbI Positional Reasoning

### Overview
- Source: Hugging Face `RawthiL/babi_tasks`, config `task_17-positional_reasoning`
- Location: `datasets/babi_positional_reasoning/`
- Size: train 904, validation 96, test 1,000
- Format: Hugging Face Dataset
- Task: Controlled text spatial-relation reasoning
- Sample: `datasets/babi_positional_reasoning/samples/sample.json`

### Download Instructions

```python
from datasets import load_dataset

dataset = load_dataset("RawthiL/babi_tasks", "task_17-positional_reasoning")
dataset.save_to_disk("datasets/babi_positional_reasoning")
```

## Dataset 4: bAbI Path Finding

### Overview
- Source: Hugging Face `RawthiL/babi_tasks`, config `task_19-path_finding`
- Location: `datasets/babi_path_finding/`
- Size: train 900, validation 100, test 1,000
- Format: Hugging Face Dataset
- Task: Controlled route/path reasoning from text descriptions
- Sample: `datasets/babi_path_finding/samples/sample.json`

### Download Instructions

```python
from datasets import load_dataset

dataset = load_dataset("RawthiL/babi_tasks", "task_19-path_finding")
dataset.save_to_disk("datasets/babi_path_finding")
```

## Dataset 5: WritingPrompts Spatial Sample

### Overview
- Source: Hugging Face `euclaise/writingprompts`
- Location: `datasets/writingprompts_spatial_sample/`
- Size: 500 sampled train records filtered by spatial-navigation keywords
- Format: JSONL sample
- Task: Human-authored fiction-like prompts/stories likely to include spatial movement or built environments
- Sample: `datasets/writingprompts_spatial_sample/samples/spatial_filtered_500.jsonl`

### Download Instructions

The full dataset can be streamed and filtered without downloading everything:

```python
from datasets import load_dataset
import json

keywords = {"room", "door", "hall", "stairs", "building", "walked", "left", "right"}
stream = load_dataset("euclaise/writingprompts", split="train", streaming=True)
rows = []
for row in stream:
    text = " ".join(str(v) for v in row.values()).lower()
    if any(keyword in text for keyword in keywords):
        rows.append(row)
    if len(rows) >= 500:
        break

with open("datasets/writingprompts_spatial_sample/samples/spatial_filtered_500.jsonl", "w") as f:
    for row in rows:
        f.write(json.dumps(row) + "\n")
```

## Dataset 6: LongStory AI-Generated Stories

### Overview
- Source: Hugging Face `THU-KEG/LongStory`
- Location: `datasets/longstory_ai_generated/`
- Size: 5,279 generated long stories, about 185 MB saved to disk
- Format: Hugging Face Dataset
- Task: AI-generated long-story comparison corpus
- Sample: `datasets/longstory_ai_generated/samples/sample.json`

### Download Instructions

```python
from datasets import load_dataset

dataset = load_dataset("THU-KEG/LongStory")
dataset.save_to_disk("datasets/longstory_ai_generated")
```

### Notes

- R2R is the best primary source for human spatial-navigation language.
- WritingPrompts gives human narrative prose but is not spatially labeled; the included sample is keyword-filtered for likely spatial movement.
- LongStory is AI-generated and useful for contrast, but it is not specific to spatial navigation.
- bAbI tasks are synthetic and should be used as controlled probes rather than ecological narrative data.
