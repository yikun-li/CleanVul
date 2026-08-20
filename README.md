# CleanVul: Toward High-Quality Function-Level Vulnerability Datasets via LLM-Based Noise Reduction

Replication package for the paper. It contains **(i) the released CleanVul dataset**, **(ii) the VulSifter implementation** (LLM scorer + heuristic filter) that produced it, and **(iii) the downstream fine-tuning / cross-dataset evaluation code**.

## Overview

VulSifter combines an LLM with a heuristic filter to identify genuine vulnerability-fixing changes inside vulnerability-fixing commits (VFCs). Applying it to 5.35M commits from 127K GitHub repositories yields **CleanVul**: 8,092 function pairs at 90.6% correctness (threshold 3), or 6,051 at 97.3% correctness (threshold 4), across Java, Python, C, C++, C#, and JavaScript.

## Repository structure (file → role → paper)

| Path | What it is | Paper location |
|---|---|---|
| `vulnerability_score_0.csv` … `vulnerability_score_4.csv` | **The released CleanVul dataset.** One file per VulSifter confidence score (0–4). Each row is a `(func_before, func_after)` pair. These are the **heuristic-filtered** (test-related changes already removed) versions. Combine by threshold to get the dataset used in the paper (see below). | Dataset (RQ1) |
| `src/vulnerability_fix_detector.py` | **VulSifter — the core approach.** LLM analysis that scores each VFC change 0–4 (Claude Opus 4.6) from `func_before`, `func_after`, commit message, and other functions in the same commit. | §Approach, *LLM Analysis* |
| `src/test_related_identifier.py` | **The heuristic filter.** Detects test functions/files (JUnit, pytest, GoogleTest, NUnit/xUnit, Jest/Mocha, …) so test-related changes can be removed. Produces the `is_test` flag. | §Approach, *Heuristics* |
| `src/build_cleanvul_dataset.py` | Helper: reconstruct the CleanVul dataset at a chosen threshold from the per-score CSVs (one command). | Dataset (RQ1) |
| `src/dataset_converter.py` | Converts a paired `(func_before, func_after)` CSV into the `(code, label)` long format (vulnerable = 1, fixed = 0) used to train detectors. | Data prep for RQ2/RQ3 |
| `src/vulnerability_detection_trainer.py` | **Downstream evaluation.** Fine-tunes transformer detectors and runs cross-dataset evaluation (train on one dataset, test on the others). Reports Accuracy/Precision/Recall/F1. | RQ2 (cross-dataset), RQ3 (cleaning impact) |

## The CleanVul dataset

Each `vulnerability_score_*.csv` has these columns:

| Column | Description |
|---|---|
| `func_before` | Vulnerable version of the function (before the fix). |
| `func_after` | Fixed/benign version of the function (after the fix). |
| `commit_msg`, `commit_url` | Commit message and URL of the VFC. |
| `cve_id`, `cwe_id` | CVE/CWE identifiers when available. |
| `file_name`, `extension` | Source file and its extension (language). |
| `vulnerability_score` | VulSifter score 0–4 (equals the file's number). |
| `is_test` | Heuristic test flag (all rows here are `False`, i.e., already filtered). |
| `date` | Commit date. |

### Reconstructing the paper's dataset (matches the paper exactly)

CleanVul at "threshold *t*" is the union of all pairs scored **≥ *t***. Because the files are split by exact score, combine them as follows (counts are the **with-heuristics** column in the paper):

| Threshold | Files to combine | Function pairs | Correctness |
|---|---|---|---|
| ≥ 4 | `score_4` | **6,051** | 97.3% |
| ≥ 3 (default) | `score_3` + `score_4` | 2,041 + 6,051 = **8,092** | 90.6% |
| ≥ 2 | `score_2` + `score_3` + `score_4` | **10,536** | 49.4% |
| ≥ 1 | `score_1` … `score_4` | **21,187** | 43.1% |

One command:

```bash
# Threshold 3 (the primary CleanVul dataset, 8,092 pairs):
python src/build_cleanvul_dataset.py --threshold 3 --out cleanvul_threshold3.csv
# Threshold 4 (highest quality, 6,051 pairs):
python src/build_cleanvul_dataset.py --threshold 4 --out cleanvul_threshold4.csv
```

## Reproducing the study end to end

**Step 1 — VulSifter scoring (§Approach, produces the scores).**
Score raw VFC changes 0–4 with the LLM:
```bash
export ANTHROPIC_API_KEY=...      # Claude
python src/vulnerability_fix_detector.py --input_file changes.jsonl --model_name claude
```
Input is JSONL of code changes (`commit_id`, `file_name`, `commit_message`, `original_function`, `new_function`); output is a CSV with a `vulnerability_score` column. *(The released `vulnerability_score_*.csv` are the output of this step over the full crawl.)*

**Step 2 — Heuristic filtering (§Approach).**
`src/test_related_identifier.py` flags test functions/files; rows flagged as tests are removed to form the "with-heuristics" dataset (the released CSVs already have this applied, `is_test = False`).

**Step 3 — Build the dataset (RQ1).** Use `build_cleanvul_dataset.py` (above) to get the threshold-*t* CleanVul CSV.

**Step 4 — Convert to training format (data prep for RQ2/RQ3).**
```bash
python src/dataset_converter.py --input cleanvul_threshold4.csv --output cleanvul_t4_long.csv
```
Turns each pair into two labeled rows (`code`, `label`: 1 = vulnerable, 0 = fixed).

**Step 5 — Fine-tune and cross-dataset evaluation (RQ2, RQ3).**
```bash
python src/vulnerability_detection_trainer.py \
  --train_datasets cleanvul primevul sven \
  --test_datasets  cleanvul primevul sven \
  --models  roberta graphcodebert Qwen/Qwen2.5-Coder-1.5B
```
Trains each model on each training set and evaluates on every test set, printing the Accuracy/Precision/Recall/F1 table used for the cross-dataset (RQ2) and cleaning-impact (RQ3) results. (Adjust flags to your paths; run `-h` for the full list.)

## Requirements

- Python 3.9+, `pandas`, `scikit-learn`, PyTorch, and Hugging Face `transformers` (for Steps 4–5).
- An LLM API key for Step 1 (`ANTHROPIC_API_KEY` for Claude).

Install:
```bash
pip install pandas scikit-learn torch transformers
```
