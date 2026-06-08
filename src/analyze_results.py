"""Analyze narrative-space features and human-vs-LLM separability."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict, cross_val_score, permutation_test_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.multitest import multipletests

from common import ROOT, SEED, read_jsonl, set_seed, truncate_words, write_jsonl
from features import FEATURE_GROUPS, extract_features


def bootstrap_ci(values: np.ndarray, n_boot: int = 2000, seed: int = SEED) -> tuple[float, float]:
    """Bootstrap a 95% confidence interval for the mean."""
    values = np.asarray(values, dtype=float)
    if len(values) == 0:
        return float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    samples = rng.choice(values, size=(n_boot, len(values)), replace=True)
    means = samples.mean(axis=1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def cohens_d(a: np.ndarray, b: np.ndarray) -> float:
    """Cohen's d for independent groups."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if len(a) < 2 or len(b) < 2:
        return 0.0
    pooled = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    if pooled == 0 or np.isnan(pooled):
        return 0.0
    return float((a.mean() - b.mean()) / pooled)


def cliffs_delta(a: np.ndarray, b: np.ndarray) -> float:
    """Cliff's delta effect size; positive means group a is larger."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if len(a) == 0 or len(b) == 0:
        return 0.0
    diff = np.sign(a[:, None] - b[None, :])
    return float(diff.mean())


def load_main_dataframe(model: str) -> pd.DataFrame:
    """Load human and generated LLM corpora and attach features."""
    human = read_jsonl(ROOT / "results" / "human_corpus.jsonl")
    llm = read_jsonl(ROOT / "results" / "model_outputs" / f"{model}_outputs.jsonl")
    prompt_ids = {row["prompt_id"] for row in read_jsonl(ROOT / "results" / "prompts" / "llm_prompts.jsonl")}
    llm = [row for row in llm if row["prompt_id"] in prompt_ids]
    if len(llm) != len(prompt_ids):
        missing = sorted(prompt_ids - {row["prompt_id"] for row in llm})
        raise RuntimeError(f"Missing {len(missing)} LLM outputs, first missing IDs: {missing[:5]}")

    rows: list[dict] = []
    for row in human + llm:
        feats = extract_features(row["text"])
        rows.append(
            {
                "doc_id": row["doc_id"],
                "prompt_id": row["prompt_id"],
                "author": row["author"],
                "source": row["source"],
                "text_role": row.get("text_role", row.get("task", "")),
                "text": row["text"],
                **feats,
            }
        )
    return pd.DataFrame(rows)


def load_external_dataframe() -> pd.DataFrame:
    """Load optional external AI stories and attach features."""
    rows = read_jsonl(ROOT / "results" / "external_ai_corpus.jsonl")
    out = []
    for row in rows:
        out.append({**row, **extract_features(row["text"])})
    return pd.DataFrame(out)


def feature_descriptives(df: pd.DataFrame, feature_cols: list[str]) -> pd.DataFrame:
    """Compute grouped descriptive statistics with bootstrap CIs."""
    rows: list[dict] = []
    for (source, author), sub in df.groupby(["source", "author"]):
        for feature in feature_cols:
            values = sub[feature].to_numpy(dtype=float)
            low, high = bootstrap_ci(values, n_boot=1000)
            rows.append(
                {
                    "source": source,
                    "author": author,
                    "feature": feature,
                    "n": len(values),
                    "mean": float(np.mean(values)),
                    "std": float(np.std(values, ddof=1)) if len(values) > 1 else 0.0,
                    "median": float(np.median(values)),
                    "min": float(np.min(values)),
                    "max": float(np.max(values)),
                    "mean_ci_low": low,
                    "mean_ci_high": high,
                }
            )
    return pd.DataFrame(rows)


def feature_tests(df: pd.DataFrame, feature_cols: list[str]) -> pd.DataFrame:
    """Compare human and LLM feature values overall and within each source."""
    rows: list[dict] = []
    scopes = ["all"] + sorted(df["source"].unique().tolist())
    for scope in scopes:
        sub = df if scope == "all" else df[df["source"] == scope]
        human = sub[sub["author"] == "human"]
        llm = sub[sub["author"] == "llm"]
        if len(human) == 0 or len(llm) == 0:
            continue
        for feature in feature_cols:
            h = human[feature].to_numpy(dtype=float)
            l = llm[feature].to_numpy(dtype=float)
            if len(np.unique(np.concatenate([h, l]))) <= 1:
                mw_p = 1.0
                t_p = 1.0
                stat = 0.0
            else:
                stat, mw_p = stats.mannwhitneyu(h, l, alternative="two-sided")
                _, t_p = stats.ttest_ind(h, l, equal_var=False)
            rows.append(
                {
                    "scope": scope,
                    "feature": feature,
                    "human_mean": float(h.mean()),
                    "llm_mean": float(l.mean()),
                    "mean_diff_llm_minus_human": float(l.mean() - h.mean()),
                    "mannwhitney_u": float(stat),
                    "p_mannwhitney": float(mw_p),
                    "p_welch": float(t_p) if not np.isnan(t_p) else 1.0,
                    "cohens_d_human_minus_llm": cohens_d(h, l),
                    "cliffs_delta_human_minus_llm": cliffs_delta(h, l),
                    "n_human": len(h),
                    "n_llm": len(l),
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        _, qvals, _, _ = multipletests(out["p_mannwhitney"].to_numpy(), method="fdr_bh")
        out["q_mannwhitney_bh"] = qvals
    return out


def classifier_for(df: pd.DataFrame, feature_cols: list[str], n_splits: int = 5) -> dict:
    """Run stratified CV logistic regression for one feature family."""
    y = (df["author"] == "llm").astype(int).to_numpy()
    X = df[feature_cols].to_numpy(dtype=float)
    min_class = min(np.bincount(y))
    splits = max(2, min(n_splits, min_class))
    cv = StratifiedKFold(n_splits=splits, shuffle=True, random_state=SEED)
    clf = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=2000, solver="liblinear", random_state=SEED),
    )
    probs = cross_val_predict(clf, X, y, cv=cv, method="predict_proba")[:, 1]
    preds = (probs >= 0.5).astype(int)
    fold_acc = cross_val_score(clf, X, y, cv=cv, scoring="accuracy")
    acc_low, acc_high = bootstrap_ci(fold_acc, n_boot=2000)
    auc = roc_auc_score(y, probs) if len(np.unique(y)) == 2 else float("nan")
    return {
        "n": len(df),
        "n_features": len(feature_cols),
        "accuracy": float(accuracy_score(y, preds)),
        "f1": float(f1_score(y, preds)),
        "roc_auc": float(auc),
        "fold_accuracy_mean": float(fold_acc.mean()),
        "fold_accuracy_std": float(fold_acc.std(ddof=1)) if len(fold_acc) > 1 else 0.0,
        "fold_accuracy_ci_low": acc_low,
        "fold_accuracy_ci_high": acc_high,
        "y_true": y,
        "y_prob": probs,
        "y_pred": preds,
    }


def classification_ablation(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Run source-specific feature-family ablations and save predictions."""
    rows: list[dict] = []
    prediction_rows: list[dict] = []
    scopes = ["all"] + sorted(df["source"].unique().tolist())
    for scope in scopes:
        sub = df if scope == "all" else df[df["source"] == scope]
        if set(sub["author"]) != {"human", "llm"}:
            continue
        for family, features in FEATURE_GROUPS.items():
            result = classifier_for(sub, features)
            if scope == "all" and family in {"all", "all_no_length", "spatial"}:
                X = sub[features].to_numpy(dtype=float)
                y = result["y_true"]
                cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
                clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, solver="liblinear"))
                score, perm_scores, p_perm = permutation_test_score(
                    clf,
                    X,
                    y,
                    cv=cv,
                    n_permutations=100,
                    scoring="accuracy",
                    random_state=SEED,
                    n_jobs=1,
                )
            else:
                score, p_perm = np.nan, np.nan
            rows.append(
                {
                    "scope": scope,
                    "feature_family": family,
                    **{k: v for k, v in result.items() if not k.startswith("y_")},
                    "permutation_score": float(score) if not np.isnan(score) else np.nan,
                    "permutation_p": float(p_perm) if not np.isnan(p_perm) else np.nan,
                }
            )
            if scope == "all" and family == "all":
                for idx, (_, row) in enumerate(sub.reset_index(drop=True).iterrows()):
                    prediction_rows.append(
                        {
                            "doc_id": row["doc_id"],
                            "prompt_id": row["prompt_id"],
                            "source": row["source"],
                            "author": row["author"],
                            "predicted_author": "llm" if result["y_pred"][idx] == 1 else "human",
                            "llm_probability": float(result["y_prob"][idx]),
                            "correct": bool(result["y_pred"][idx] == result["y_true"][idx]),
                            "excerpt": truncate_words(row["text"], 70),
                        }
                    )
    return pd.DataFrame(rows), pd.DataFrame(prediction_rows)


def top_feature_tables(df: pd.DataFrame, feature_cols: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Fit full-data models for interpretable feature rankings."""
    y = (df["author"] == "llm").astype(int).to_numpy()
    X = df[feature_cols].to_numpy(dtype=float)
    pipe = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=2000, solver="liblinear", random_state=SEED),
    )
    pipe.fit(X, y)
    coef = pipe.named_steps["logisticregression"].coef_[0]
    coef_df = pd.DataFrame({"feature": feature_cols, "logistic_coef_llm": coef})
    coef_df["abs_coef"] = coef_df["logistic_coef_llm"].abs()
    coef_df = coef_df.sort_values("abs_coef", ascending=False)

    forest = RandomForestClassifier(n_estimators=500, random_state=SEED, class_weight="balanced")
    forest.fit(X, y)
    importance = permutation_importance(forest, X, y, n_repeats=30, random_state=SEED, scoring="accuracy")
    rf_df = pd.DataFrame(
        {
            "feature": feature_cols,
            "permutation_importance_mean": importance.importances_mean,
            "permutation_importance_std": importance.importances_std,
        }
    ).sort_values("permutation_importance_mean", ascending=False)
    return coef_df, rf_df


def score_external(df: pd.DataFrame, external: pd.DataFrame, feature_cols: list[str]) -> pd.DataFrame:
    """Score external AI stories with a classifier trained on the main corpus."""
    if external.empty:
        return pd.DataFrame()
    y = (df["author"] == "llm").astype(int).to_numpy()
    X = df[feature_cols].to_numpy(dtype=float)
    model = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=2000, solver="liblinear", random_state=SEED),
    )
    model.fit(X, y)
    probs = model.predict_proba(external[feature_cols].to_numpy(dtype=float))[:, 1]
    out = external[["doc_id", "source", "text"]].copy()
    out["llm_probability"] = probs
    out["predicted_llm"] = probs >= 0.5
    out["excerpt"] = out["text"].map(lambda t: truncate_words(t, 60))
    return out.drop(columns=["text"])


def make_plots(df: pd.DataFrame, metrics: pd.DataFrame, coef_df: pd.DataFrame) -> None:
    """Create publication-friendly summary plots."""
    sns.set_theme(style="whitegrid")
    fig_dir = ROOT / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 5))
    plot_metrics = metrics.copy()
    order = ["length_only", "generic", "spatial", "narrative", "all_no_length", "all"]
    sns.barplot(data=plot_metrics, x="scope", y="accuracy", hue="feature_family", hue_order=order)
    plt.axhline(0.5, color="black", linestyle="--", linewidth=1)
    plt.ylim(0.35, 1.05)
    plt.title("Human-vs-LLM classification accuracy by feature family")
    plt.ylabel("Cross-validated accuracy")
    plt.xlabel("Evaluation scope")
    plt.legend(title="Feature family", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(fig_dir / "classification_accuracy.png", dpi=200)
    plt.close()

    key_features = [
        "imperative_sentence_share",
        "first_person_per_1000",
        "motion_per_1000",
        "landmark_per_1000",
        "sequence_per_1000",
        "formulaic_phrase_per_1000",
    ]
    fig, axes = plt.subplots(2, 3, figsize=(13, 7))
    for ax, feature in zip(axes.ravel(), key_features):
        sns.boxplot(data=df, x="source", y=feature, hue="author", ax=ax)
        ax.set_title(feature)
        ax.set_xlabel("")
    handles, labels = axes.ravel()[0].get_legend_handles_labels()
    for ax in axes.ravel():
        legend = ax.get_legend()
        if legend:
            legend.remove()
    fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.5, 0.0), ncol=2)
    fig.suptitle("Key spatial-narrative features", y=0.99)
    plt.tight_layout(rect=(0, 0.06, 1, 0.94))
    plt.savefig(fig_dir / "key_feature_distributions.png", dpi=200)
    plt.close()

    top = coef_df.head(15).copy()
    top = top.sort_values("logistic_coef_llm")
    plt.figure(figsize=(9, 6))
    colors = ["#5b8c5a" if x > 0 else "#b85c5c" for x in top["logistic_coef_llm"]]
    plt.barh(top["feature"], top["logistic_coef_llm"], color=colors)
    plt.axvline(0, color="black", linewidth=1)
    plt.title("Top standardized logistic coefficients (positive = LLM)")
    plt.xlabel("Coefficient")
    plt.tight_layout()
    plt.savefig(fig_dir / "top_logistic_coefficients.png", dpi=200)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gpt-5.4-mini")
    args = parser.parse_args()
    set_seed(SEED)

    out_dir = ROOT / "results" / "evaluations"
    out_dir.mkdir(parents=True, exist_ok=True)

    df = load_main_dataframe(args.model)
    feature_cols = FEATURE_GROUPS["all"]
    df.to_csv(ROOT / "results" / "features.csv", index=False)

    descriptives = feature_descriptives(df, feature_cols)
    descriptives.to_csv(out_dir / "feature_descriptives.csv", index=False)

    tests = feature_tests(df, feature_cols)
    tests.to_csv(out_dir / "feature_tests.csv", index=False)

    metrics, predictions = classification_ablation(df)
    metrics.to_csv(out_dir / "classification_metrics.csv", index=False)
    predictions.to_csv(out_dir / "classification_predictions.csv", index=False)
    write_jsonl(out_dir / "misclassified_examples.jsonl", predictions[~predictions["correct"]].to_dict("records"))

    coef_df, rf_df = top_feature_tables(df, feature_cols)
    coef_df.to_csv(out_dir / "top_logistic_features.csv", index=False)
    rf_df.to_csv(out_dir / "random_forest_permutation_importance.csv", index=False)

    external = load_external_dataframe()
    if not external.empty:
        ext_scores = score_external(df, external, feature_cols)
        ext_scores.to_csv(out_dir / "external_longstory_scores.csv", index=False)

    make_plots(df, metrics, coef_df)

    source_counts = [
        {"source": source, "author": author, "n": int(n)}
        for (source, author), n in df.groupby(["source", "author"]).size().items()
    ]
    summary = {
        "n_main_texts": int(len(df)),
        "n_human": int((df["author"] == "human").sum()),
        "n_llm": int((df["author"] == "llm").sum()),
        "sources": source_counts,
        "best_classification": metrics.sort_values("accuracy", ascending=False).head(5).to_dict("records"),
        "top_llm_features": coef_df.head(10).to_dict("records"),
    }
    (out_dir / "analysis_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
