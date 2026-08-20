"""Reconstruct the CleanVul dataset at a given confidence threshold.

The released dataset is stored as one CSV per VulSifter score (0-4), already
heuristic-filtered (test-related changes removed). CleanVul at "threshold t" is
the union of all function pairs scored >= t; this script concatenates the
relevant per-score files into a single CSV.

Resulting sizes match the paper (with-heuristics column):
  t=4 -> 6,051    t=3 -> 8,092    t=2 -> 10,536    t=1 -> 21,187

Usage:
  python build_cleanvul_dataset.py --threshold 3 --out cleanvul_threshold3.csv
  python build_cleanvul_dataset.py --threshold 4 --data_dir .. --out cleanvul_t4.csv
"""

import argparse
import os

import pandas as pd


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--threshold", type=int, default=3, choices=[1, 2, 3, 4],
                    help="Keep pairs with VulSifter score >= threshold (default: 3).")
    ap.add_argument("--data_dir", default=".",
                    help="Directory containing vulnerability_score_*.csv (default: current dir).")
    ap.add_argument("--out", default=None,
                    help="Output CSV path (default: cleanvul_threshold<t>.csv).")
    args = ap.parse_args()

    parts = []
    for s in range(args.threshold, 5):
        f = os.path.join(args.data_dir, f"vulnerability_score_{s}.csv")
        df = pd.read_csv(f)
        parts.append(df)
        print(f"  score={s}: {len(df):>6} pairs  ({f})")

    combined = pd.concat(parts, ignore_index=True)
    out = args.out or f"cleanvul_threshold{args.threshold}.csv"
    combined.to_csv(out, index=False)
    print(f"\nCleanVul (score >= {args.threshold}): {len(combined)} function pairs -> {out}")


if __name__ == "__main__":
    main()
