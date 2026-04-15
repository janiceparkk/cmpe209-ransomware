import os
import pandas as pd

INPUT_PATH = "data/raw/combined_without_3gram.csv"
OUTPUT_DIR = "data/processed"

META_COLS = ["ID", "filename", "RG", "family"]

def build_train_test_masks(df: pd.DataFrame):
    train_mask = (
        ((df["family"] == 0) & (df["ID"] <= 11133)) |
        (df["family"].between(1, 25))
    )

    test_mask = (
        ((df["family"] == 0) & (df["ID"] >= 12000)) |
        (df["family"].between(26, 40))
    )

    return train_mask, test_mask

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = pd.read_csv(INPUT_PATH)

    required_cols = {"ID", "filename", "RG", "family"}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    print("Loaded dataset:", df.shape)

    duplicates = int(df.duplicated().sum())
    print("Duplicate rows:", duplicates)

    total_missing = int(df.isnull().sum().sum())
    print("Total missing values:", total_missing)

    train_mask, test_mask = build_train_test_masks(df)

    train_df = df[train_mask].copy()
    test_df = df[test_mask].copy()

    feature_cols = [c for c in df.columns if c not in META_COLS]

    X_train = train_df[feature_cols].copy()
    X_test = test_df[feature_cols].copy()

    y_train = train_df[["RG"]].copy()
    y_test = test_df[["RG"]].copy()

    meta_train = train_df[META_COLS].copy()
    meta_test = test_df[META_COLS].copy()

    train_df.to_csv(f"{OUTPUT_DIR}/train_full.csv", index=False)
    test_df.to_csv(f"{OUTPUT_DIR}/test_full.csv", index=False)

    X_train.to_csv(f"{OUTPUT_DIR}/X_train.csv", index=False)
    X_test.to_csv(f"{OUTPUT_DIR}/X_test.csv", index=False)

    y_train.to_csv(f"{OUTPUT_DIR}/y_train.csv", index=False)
    y_test.to_csv(f"{OUTPUT_DIR}/y_test.csv", index=False)

    meta_train.to_csv(f"{OUTPUT_DIR}/meta_train.csv", index=False)
    meta_test.to_csv(f"{OUTPUT_DIR}/meta_test.csv", index=False)

    print("\n=== EXPORTED FILES ===")
    print("train_full.csv:", train_df.shape)
    print("test_full.csv:", test_df.shape)
    print("X_train.csv:", X_train.shape)
    print("X_test.csv:", X_test.shape)
    print("y_train.csv:", y_train.shape)
    print("y_test.csv:", y_test.shape)
    print("meta_train.csv:", meta_train.shape)
    print("meta_test.csv:", meta_test.shape)

if __name__ == "__main__":
    main()
