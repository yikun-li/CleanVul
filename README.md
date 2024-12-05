# CleanVul: Automatic Function-Level Vulnerability Detection in Code Commits Using LLM Heuristics

<p align="left">
    <a href="https://arxiv.org/abs/2411.17274"><img src="https://img.shields.io/badge/arXiv-2411.17274-b31b1b.svg?style=for-the-badge"></a>
    <a href="https://opensource.org/license/mit/"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge"></a>
</p>

<p align="left">
    📜 &nbsp;<a href="#-overview">Overview</a>
    | 📚&nbsp;<a href="#-cleanvul-dataset">Dataset</a>
    | 📝&nbsp;<a href="#-citation">Citation</a>
</p>

* (2024-11-26) We released our paper and dataset for reproducibility.

## 📜 Overview

VulSifter is a novel methodology that leverages Large Language Models (LLMs) with heuristic enhancement to 
automatically identify vulnerability-fixing changes from vulnerability-fixing commits (VFCs). Using this methodology, 
the authors developed CleanVul, a high-quality dataset containing 11,632 functions that achieves 90.6% correctness, 
comparable to established datasets like SVEN (94.0%) and PrimeVul (86.0%). The methodology addresses the significant 
noise (40-75%) in existing vulnerability datasets caused by indiscriminate labeling of all modifications in VFCs as 
vulnerability-related.

### Vulnerability Fix Identification in VFC

* ✨ **LLM-Based Analysis**: Uses state-of-the-art LLMs to comprehend code semantics and contextual information for
  identifying genuine vulnerability fixes
* ✨ **Heuristic Enhancement**: Custom filtering rules to eliminate test-related changes
* ✨ **High Accuracy**: Achieves F1-score of 0.82 in identifying genuine vulnerability fixes

### Better Vulnerability Dataset

* ✨ **High Quality**: 90.6% correctness rate for identifying genuine vulnerability fixes, comparable to manually curated
  datasets
* ✨ **Scale**: Contains 11,632 function pairs across multiple programming languages
* ✨ **Language Coverage**: Includes Java, Python, C, JavaScript, C#, and C++ code
* ✨ **Diverse Sources**: Derived from analysis of 5.3M commits across 127K GitHub repositories

## 📚 CleanVul Dataset

### Dataset Statistics

The dataset provides different versions based on confidence thresholds:

| Threshold | With Heuristics | Without Heuristics | Correctness (With Heuristics) | Correctness (Without Heuristics) |
|-----------|-----------------|--------------------|-------------------------------|----------------------------------|
| 1         | 36,543          | 41,327             | 43.1%                         | 37.5%                            |
| 2         | 23,070          | 25,789             | 57.7%                         | 49.4%                            |
| 3         | 11,632          | 12,847             | 90.6%                         | 76.5%                            |
| 4         | 8,337           | 9,235              | 97.3%                         | 78.0%                            |## 💻 Experiments

## 📝 Citation

```bibtex
@article{li2024cleanvul,
  title={CleanVul: Automatic Function-Level Vulnerability Detection in Code Commits Using LLM Heuristics},
  author={Li, Yikun and Zhang, Ting and Widyasari, Ratnadira and Tun, Yan Naing and Nguyen, Huu Hung and Bui, Tan and Irsan, Ivana Clairine and Cheng, Yiran and Lan, Xiang and Ang, Han Wei and others},
  journal={arXiv preprint arXiv:2411.17274},
  year={2024}
}
```
