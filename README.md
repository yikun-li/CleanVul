# CleanVul: Automatic Function-Level Vulnerability Detection in Code Commits Using LLM Heuristics

<p align="left">
    <a href="https://opensource.org/license/mit/"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge"></a>
</p>

<p align="left">
    📜 &nbsp;<a href="#-overview">Overview</a>
    | 📚&nbsp;<a href="#-cleanvul-dataset">Dataset</a>
</p>

## 📜 Overview

CleanVul introduces VulSifter, an innovative methodology that combines Large Language Models (LLMs) with heuristic to automatically detect vulnerability-fixing changes within vulnerability-fixing commits (VFCs). This approach has enabled us to create two high-quality datasets: the primary CleanVul dataset containing 8,092 functions with 90.6% correctness, and a more precise variant comprising 6,051 functions with 97.3% correctness. Both datasets demonstrate quality comparable to or exceeding established benchmarks such as SVEN (94.0%) and PrimeVul (86.0%).

Our approach addresses the significant noise (40-75%) in existing vulnerability datasets caused by indiscriminate labeling of all modifications in vulnerability-fixing commits as vulnerability-related.

### Vulnerability Fix Identification in VFC

* ✨ **LLM-Based Analysis**: Uses state-of-the-art LLMs to comprehend code semantics and contextual information for identifying genuine vulnerability fixes
* ✨ **Heuristic Enhancement**: Custom filtering rules to eliminate test-related changes
* ✨ **High Accuracy**: Achieves F1-score of 0.77 in identifying genuine vulnerability fixes

### Better Vulnerability Dataset

* ✨ **High Quality**: Maximal 97.3% correctness rate for identifying genuine vulnerability fixes, comparable to manually curated datasets
* ✨ **Scale**: Contains over 6,051 function pairs across multiple programming languages
* ✨ **Language Coverage**: Includes Java, Python, C, JavaScript, C#, and C++ code
* ✨ **Diverse Sources**: Derived from analysis of 5.3M commits across 127K GitHub repositories

## 📚 CleanVul Dataset

### Dataset Statistics

The dataset provides different versions based on confidence thresholds:

| Threshold | With Heuristics | Without Heuristics | Correctness (With Heuristics) | Correctness (Without Heuristics) |
|-----------|-----------------|--------------------|-------------------------------|----------------------------------|
| 1         | 21,187          | 23,652             | 43.1%                         | 37.5%                            |
| 2         | 10,536          | 11,745             | 49.4%                         | 57.7%                            |
| 3         | 8,092           | 8,979              | 90.6%                         | 76.5%                            |
| 4         | 6,051           | 6,616              | 97.3%                         | 78.0%                            |

### Understanding Thresholds

The thresholds represent confidence levels in our VulSifter methodology:

* **Threshold 1**: Lowest confidence level, capturing the broadest set of potential vulnerability fixes but with the highest false positive rate (43.1% correctness with heuristics)
* **Threshold 2**: Moderate confidence level, offering a balance between dataset size and accuracy (49.4% correctness with heuristics)
* **Threshold 3**: High confidence level, recommended for most applications, providing excellent balance between dataset size and quality (90.6% correctness with heuristics)
* **Threshold 4**: Highest confidence level, prioritizing precision over recall, offering near-perfect correctness (97.3% with heuristics) but with a smaller dataset size

The "With Heuristics" versions apply additional filtering rules to remove test-related changes and other non-vulnerability modifications, resulting in significantly higher correctness rates compared to versions without these heuristics.

**Important detail about Threshold:**

* In the dataset, pairs are stored separately by score:
  * `vulnerability_score_3.csv` contains pairs with score = 3.
  * `vulnerability_score_4.csv` contains pairs with score = 4.
* To reconstruct Threshold 3 (score ≥ 3), you need to combine `vulnerability_score_3.csv` and `vulnerability_score_4.csv`, giving a total of 8,092 items (with heuristic filtering).
* We keep them separate in the dataset to avoid duplication and to let users choose between strict (score=4 only) or inclusive (score ≥ 3) subsets.
