"""Feature extraction for spatial-narrative grammar analysis."""

from __future__ import annotations

import math
import re
from collections import Counter

from common import count_terms, per_1000, sentence_split, word_tokens

DIRECTION_TERMS = {
    "left",
    "right",
    "straight",
    "forward",
    "back",
    "backward",
    "up",
    "down",
    "upstairs",
    "downstairs",
    "north",
    "south",
    "east",
    "west",
    "around",
    "across",
    "through",
    "into",
    "out",
    "toward",
    "towards",
    "past",
    "along",
    "beside",
    "behind",
    "between",
    "near",
    "inside",
    "outside",
    "ahead",
}

CARDINAL_TERMS = {"north", "south", "east", "west", "northern", "southern", "eastern", "western"}
EGOCENTRIC_TERMS = {"left", "right", "ahead", "behind", "forward", "back", "straight", "near"}

LANDMARK_TERMS = {
    "room",
    "rooms",
    "hall",
    "halls",
    "hallway",
    "hallways",
    "corridor",
    "corridors",
    "stairs",
    "stair",
    "stairwell",
    "steps",
    "landing",
    "door",
    "doors",
    "doorway",
    "entry",
    "entrance",
    "exit",
    "kitchen",
    "bathroom",
    "bedroom",
    "office",
    "lobby",
    "elevator",
    "window",
    "windows",
    "table",
    "chair",
    "painting",
    "rail",
    "railing",
    "column",
    "columns",
    "closet",
    "floor",
    "wall",
    "walls",
    "archway",
    "courtyard",
    "atrium",
    "basement",
    "foyer",
}

MOTION_TERMS = {
    "walk",
    "walked",
    "walking",
    "step",
    "stepped",
    "move",
    "moved",
    "pass",
    "passed",
    "enter",
    "entered",
    "cross",
    "crossed",
    "turn",
    "turned",
    "climb",
    "climbed",
    "descend",
    "descended",
    "ascend",
    "ascended",
    "go",
    "went",
    "head",
    "headed",
    "continue",
    "continued",
    "stop",
    "stopped",
    "exit",
    "exited",
    "approach",
    "approached",
    "follow",
    "followed",
    "leave",
    "left",
}

SEQUENCE_TERMS = {
    "then",
    "next",
    "after",
    "before",
    "until",
    "once",
    "finally",
    "while",
    "when",
    "meanwhile",
    "eventually",
}

FIRST_PERSON = {"i", "me", "my", "mine", "myself", "we", "us", "our", "ours"}
SECOND_PERSON = {"you", "your", "yours", "yourself"}
DEICTIC_TERMS = {"here", "there", "near", "nearby", "ahead", "behind", "inside", "outside", "beside", "around"}

SENSORY_TERMS = {
    "saw",
    "seen",
    "heard",
    "hear",
    "sound",
    "smell",
    "scent",
    "touch",
    "felt",
    "feel",
    "light",
    "shadow",
    "glow",
    "dark",
    "bright",
    "cold",
    "warm",
    "dust",
}

AFFECT_TERMS = {
    "fear",
    "afraid",
    "relief",
    "heart",
    "wonder",
    "strange",
    "uneasy",
    "anxious",
    "hope",
    "dread",
    "panic",
    "calm",
    "lonely",
    "alone",
}

CLOSURE_TERMS = {"stop", "stopped", "end", "ended", "finally", "arrived", "reached", "there", "still"}

IMPERATIVE_STARTS = {
    "walk",
    "go",
    "turn",
    "head",
    "continue",
    "stop",
    "take",
    "make",
    "proceed",
    "enter",
    "exit",
    "move",
}

FORMULAIC_PHRASES = [
    "couldn't help but",
    "could not help but",
    "little did",
    "as if",
    "for a moment",
    "in that moment",
    "i realized",
    "i could feel",
    "the air was thick",
    "a chill ran",
    "heart pounding",
    "took a deep breath",
]


FEATURE_GROUPS = {
    "length_only": [
        "word_count",
        "sentence_count",
        "mean_sentence_len",
    ],
    "generic": [
        "type_token_ratio",
        "hapax_ratio",
        "bigram_repetition",
        "mean_sentence_len",
        "nominalization_per_1000",
        "participial_ing_per_1000",
        "coordination_per_1000",
        "that_per_1000",
        "passive_like_per_1000",
        "dialogue_mark_density",
    ],
    "spatial": [
        "direction_per_1000",
        "cardinal_per_1000",
        "egocentric_per_1000",
        "landmark_per_1000",
        "motion_per_1000",
        "sequence_per_1000",
        "deictic_per_1000",
        "route_step_density",
        "survey_route_ratio",
        "landmark_reuse_ratio",
        "left_right_imbalance",
        "closure_per_1000",
        "imperative_sentence_share",
    ],
    "narrative": [
        "first_person_per_1000",
        "second_person_per_1000",
        "sensory_per_1000",
        "affect_per_1000",
        "formulaic_phrase_per_1000",
        "narrative_route_ratio",
    ],
}
FEATURE_GROUPS["all"] = sorted({feature for features in FEATURE_GROUPS.values() for feature in features})
FEATURE_GROUPS["all_no_length"] = sorted(set(FEATURE_GROUPS["all"]) - set(FEATURE_GROUPS["length_only"]))


def count_phrases(text_lower: str, phrases: list[str]) -> int:
    """Count literal phrase occurrences."""
    return sum(text_lower.count(phrase) for phrase in phrases)


def count_passive_like(text_lower: str) -> int:
    """Approximate passive clauses with be-auxiliary plus an -ed/-en token."""
    return len(
        re.findall(
            r"\b(?:am|is|are|was|were|be|been|being)\s+(?:\w+\s+){0,2}?\w+(?:ed|en)\b",
            text_lower,
        )
    )


def count_nominalizations(tokens: list[str]) -> int:
    """Count common nominalization suffixes."""
    suffixes = ("tion", "sion", "ment", "ness", "ity", "ance", "ence")
    return sum(1 for tok in tokens if len(tok) > 5 and tok.endswith(suffixes))


def bigram_repetition(tokens: list[str]) -> float:
    """Return the repeated-bigram share."""
    if len(tokens) < 3:
        return 0.0
    bigrams = list(zip(tokens, tokens[1:]))
    return 1.0 - (len(set(bigrams)) / len(bigrams))


def landmark_reuse(tokens: list[str]) -> float:
    """Estimate how often landmark terms are reused rather than introduced once."""
    landmarks = [tok for tok in tokens if tok in LANDMARK_TERMS]
    if not landmarks:
        return 0.0
    counts = Counter(landmarks)
    repeated = sum(count - 1 for count in counts.values() if count > 1)
    return repeated / len(landmarks)


def imperative_share(sentences: list[str]) -> float:
    """Approximate instruction-like imperatives by sentence-initial verbs."""
    if not sentences:
        return 0.0
    starts = 0
    for sentence in sentences:
        toks = word_tokens(sentence)
        if toks and toks[0] in IMPERATIVE_STARTS:
            starts += 1
    return starts / len(sentences)


def extract_features(text: str) -> dict[str, float]:
    """Extract interpretable grammar and spatial-narrative features."""
    text_lower = text.lower()
    tokens = word_tokens(text)
    sentences = sentence_split(text)
    n_words = len(tokens)
    n_sentences = len(sentences)
    token_counts = Counter(tokens)

    direction = count_terms(tokens, DIRECTION_TERMS)
    cardinal = count_terms(tokens, CARDINAL_TERMS)
    egocentric = count_terms(tokens, EGOCENTRIC_TERMS)
    landmarks = count_terms(tokens, LANDMARK_TERMS)
    motion = count_terms(tokens, MOTION_TERMS)
    sequence = count_terms(tokens, SEQUENCE_TERMS)
    deictic = count_terms(tokens, DEICTIC_TERMS)
    first_person = count_terms(tokens, FIRST_PERSON)
    second_person = count_terms(tokens, SECOND_PERSON)
    sensory = count_terms(tokens, SENSORY_TERMS)
    affect = count_terms(tokens, AFFECT_TERMS)
    closure = count_terms(tokens, CLOSURE_TERMS)
    formulaic = count_phrases(text_lower, FORMULAIC_PHRASES)
    left_count = token_counts.get("left", 0)
    right_count = token_counts.get("right", 0)
    route_base = direction + motion + sequence

    features: dict[str, float] = {
        "word_count": float(n_words),
        "sentence_count": float(n_sentences),
        "mean_sentence_len": float(n_words / max(n_sentences, 1)),
        "type_token_ratio": float(len(set(tokens)) / max(n_words, 1)),
        "hapax_ratio": float(sum(1 for c in token_counts.values() if c == 1) / max(len(token_counts), 1)),
        "bigram_repetition": bigram_repetition(tokens),
        "nominalization_per_1000": per_1000(count_nominalizations(tokens), n_words),
        "participial_ing_per_1000": per_1000(sum(1 for tok in tokens if len(tok) > 4 and tok.endswith("ing")), n_words),
        "coordination_per_1000": per_1000(count_terms(tokens, {"and", "but", "or"}), n_words),
        "that_per_1000": per_1000(token_counts.get("that", 0), n_words),
        "passive_like_per_1000": per_1000(count_passive_like(text_lower), n_words),
        "dialogue_mark_density": float(text.count('"') + text.count("`")) / max(len(text), 1),
        "direction_per_1000": per_1000(direction, n_words),
        "cardinal_per_1000": per_1000(cardinal, n_words),
        "egocentric_per_1000": per_1000(egocentric, n_words),
        "landmark_per_1000": per_1000(landmarks, n_words),
        "motion_per_1000": per_1000(motion, n_words),
        "sequence_per_1000": per_1000(sequence, n_words),
        "deictic_per_1000": per_1000(deictic, n_words),
        "route_step_density": per_1000(route_base, n_words),
        "survey_route_ratio": float((cardinal + 1) / max(egocentric + direction, 1)),
        "landmark_reuse_ratio": landmark_reuse(tokens),
        "left_right_imbalance": float(abs(left_count - right_count) / max(left_count + right_count, 1)),
        "closure_per_1000": per_1000(closure, n_words),
        "imperative_sentence_share": imperative_share(sentences),
        "first_person_per_1000": per_1000(first_person, n_words),
        "second_person_per_1000": per_1000(second_person, n_words),
        "sensory_per_1000": per_1000(sensory, n_words),
        "affect_per_1000": per_1000(affect, n_words),
        "formulaic_phrase_per_1000": per_1000(formulaic, n_words),
        "narrative_route_ratio": float((first_person + sensory + affect + formulaic + 1) / max(route_base, 1)),
    }

    for key, value in list(features.items()):
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            features[key] = 0.0
    return features
