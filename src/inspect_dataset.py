import pandas as pd

INPUT_PATH = "data/raw/combined_without_3gram.csv"

def main():
    df = pd.read_csv(INPUT_PATH)

    print("\n=== DATASET OVERVIEW ===")
    print("Shape:", df.shape)
    print("\nFirst 10 columns:")
    print(df.columns[:10].tolist())

    print("\n=== LABEL COUNTS (RG) ===")
    if "RG" in df.columns:
        print(df["RG"].value_counts().sort_index())
    else:
        print("Column 'RG' not found.")

    print("\n=== FAMILY COUNTS (first 20 shown) ===")
    if "family" in df.columns:
        print(df["family"].value_counts().sort_index().head(20))
    else:
        print("Column 'family' not found.")

    print("\n=== MISSING VALUES ===")
    missing = df.isnull().sum()
    print("Total missing values:", int(missing.sum()))

    print("\n=== DUPLICATES ===")
    print("Duplicate rows:", int(df.duplicated().sum()))

    print("\n=== DATA TYPES (first 20 shown) ===")
    print(df.dtypes.head(20))

if __name__ == "__main__":
    main()
