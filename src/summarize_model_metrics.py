import glob
import pandas as pd

files = sorted(glob.glob("results/*_metrics.csv"))

if not files:
    raise ValueError("No metrics files found in results/")

dfs = [pd.read_csv(f) for f in files]
summary = pd.concat(dfs, ignore_index=True)

cols = ["model_name", "accuracy", "precision", "recall", "f1_score", "tn", "fp", "fn", "tp"]
summary = summary[cols]

summary.to_csv("results/model_comparison_summary.csv", index=False)
print(summary.to_string(index=False))
print("\nSaved to results/model_comparison_summary.csv")
