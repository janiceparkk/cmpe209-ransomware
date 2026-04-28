#!/usr/bin/env python3
import argparse
import os
import joblib
import pandas as pd

def engineer_features(df):
    file_api_cols = [
        "createfilea", "readfile", "writefile", "findfirstfilea",
        "findnextfilea", "copyfilea", "movefilea", "deletefilea",
        "setfileattributesa", "setendoffile"
    ]

    crypto_api_cols = [
        "bcryptencrypt", "bcryptopenalgorithmprovider",
        "bcryptgeneratesymmetrickey", "cryptacquirecontexta",
        "cryptcreatehash", "cryptencrypt", "cryptgenkey",
        "cryptimportkey", "crypthashdata"
    ]

    registry_api_cols = [
        "regopenkeya", "regsetkeyvaluew", "regdeletekeya",
        "regdeletevaluea", "regnotifychangekeyvalue"
    ]

    network_api_cols = [
        "internetopena", "internetopenurla", "internetreadfile",
        "httpopenrequesta", "httpsendrequesta", "winhttpopen",
        "winhttpconnect", "socket"
    ]

    def present_data(local_df, cols):
        cols = [c for c in cols if c in local_df.columns]
        if not cols:
            return pd.Series(0, index=local_df.index)
        return local_df[cols].sum(axis=1)

    df = df.copy()
    df["num_file_apis"] = present_data(df, file_api_cols)
    df["num_crypto_apis"] = present_data(df, crypto_api_cols)
    df["num_registry_apis"] = present_data(df, registry_api_cols)
    df["num_network_apis"] = present_data(df, network_api_cols)
    df["has_crypto"] = (df["num_crypto_apis"] > 0).astype(int)
    df["has_file_access"] = (df["num_file_apis"] > 0).astype(int)
    df["has_network"] = (df["num_network_apis"] > 0).astype(int)

    if "SizeOfImage" in df.columns and "SizeOfCode" in df.columns:
        df["code_to_image_ratio"] = df["SizeOfCode"] / df["SizeOfImage"].replace(0, 1)
    else:
        df["code_to_image_ratio"] = 0

    if "IMPORT_size" in df.columns and "SizeOfImage" in df.columns:
        df["import_to_image_ratio"] = df["IMPORT_size"] / df["SizeOfImage"].replace(0, 1)
    else:
        df["import_to_image_ratio"] = 0

    packer_columns = [c for c in df.columns if c.lower() in {"upx0", "upx1", "upx2", ".aspack", ".mpress1", ".mpress2"}]
    if packer_columns:
        df["has_packer"] = (df[packer_columns].sum(axis=1) > 0).astype(int)
    else:
        df["has_packer"] = 0

    return df


def risk_level(p):
    if p >= 0.70:
        return "High"
    if p >= 0.40:
        return "Medium"
    return "Low"


def main():
    parser = argparse.ArgumentParser(description="Predict one demo sample using a saved model.")
    parser.add_argument("--model-path", required=True, help="Path to saved model .pkl/.pk1/.joblib")
    parser.add_argument("--demo-x", default="demo/demo_X.csv", help="Path to demo_X.csv")
    parser.add_argument("--demo-meta", default="demo/demo_meta.csv", help="Path to demo_meta.csv")
    parser.add_argument("--feature-cols", default=None, help="Optional saved feature column list for RF_B or RF_C")
    parser.add_argument("--engineer", action="store_true", help="Apply engineered features before prediction")
    args = parser.parse_args()

    model = joblib.load(args.model_path)
    X = pd.read_csv(args.demo_x)
    meta = pd.read_csv(args.demo_meta)

    if args.engineer:
        X = engineer_features(X)

    if args.feature_cols:
        feature_cols = joblib.load(args.feature_cols)
        X = X.reindex(columns=feature_cols, fill_value=0)

    y_pred = model.predict(X)[0]

    if hasattr(model, "predict_proba"):
        y_proba = model.predict_proba(X)[0][1]
    else:
        y_proba = float(y_pred)

    output = meta.copy()
    output["predicted_RG"] = int(y_pred)
    output["ransomware_probability"] = float(y_proba)
    output["risk_level"] = risk_level(y_proba)

    os.makedirs("results", exist_ok=True)
    output.to_csv("results/demo_prediction_report.csv", index=False)

    print("Demo prediction result:")
    print(output.to_string(index=False))
    print("\nSaved to results/demo_prediction_report.csv")


if __name__ == "__main__":
    main()
