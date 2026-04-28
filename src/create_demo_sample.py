#!/usr/bin/env python3
import argparse
import os
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description="Create a single demo sample from the held-out test set.")
    parser.add_argument("--label", type=int, choices=[0, 1], default=1, help="0 = goodware, 1 = ransomware")
    parser.add_argument("--row-index", type=int, default=0, help="Which matching sample to select")
    parser.add_argument("--data-dir", default="data/processed", help="Directory containing processed CSV files")
    parser.add_argument("--output-dir", default="demo", help="Directory to save demo sample files")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    x_test = pd.read_csv(f"{args.data_dir}/X_test.csv")
    y_test = pd.read_csv(f"{args.data_dir}/y_test.csv").squeeze()
    meta_test = pd.read_csv(f"{args.data_dir}/meta_test.csv")

    matching_idx = y_test[y_test == args.label].index.tolist()

    if not matching_idx:
        raise ValueError(f"No samples found with label={args.label}")

    if args.row_index >= len(matching_idx):
        raise ValueError(f"row-index {args.row_index} is out of range. Found only {len(matching_idx)} matching samples.")

    idx = matching_idx[args.row_index]

    demo_x = x_test.iloc[[idx]].copy()
    demo_y = pd.DataFrame({"RG": [int(y_test.iloc[idx])]})
    demo_meta = meta_test.iloc[[idx]].copy()

    demo_x.to_csv(f"{args.output_dir}/demo_X.csv", index=False)
    demo_y.to_csv(f"{args.output_dir}/demo_y.csv", index=False)
    demo_meta.to_csv(f"{args.output_dir}/demo_meta.csv", index=False)

    print("Created demo sample files:")
    print(f"{args.output_dir}/demo_X.csv")
    print(f"{args.output_dir}/demo_y.csv")
    print(f"{args.output_dir}/demo_meta.csv")
    print("\nSelected sample:")
    print(demo_meta.to_string(index=False))
    print("\nTrue label:")
    print(demo_y.to_string(index=False))


if __name__ == "__main__":
    main()
