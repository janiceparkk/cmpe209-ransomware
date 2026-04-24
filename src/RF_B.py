# RF_B.py This is a random forest model with feature engineering by summing API category counts, DLL category counts, 
# suspicious capability flags, packing/obfuscation factors, ratios and summary stats
import pandas as pd
import numpy as np
import RF_A as rf_a
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# family = 0 means goodware | everything else is malware/ransomware
# ransomware behavior usually combines: file discovery, encryption, file rewrite/rename/delete, 
# persistence or privilege use, optional C2 communication, occasional backup disablement

# columns that are related to file API calls
file_api_cols = [
    "createfilea", "readfile", "writefile", "findfirstfilea",
    "findnextfilea", "copyfilea", "movefilea", "deletefilea",
    "setfileattributesa", "setendoffile"
]

# columns that are related to crypto API calls
crypto_api_cols = [
    "bcryptencrypt", "bcryptopenalgorithmprovider",
    "bcryptgeneratesymmetrickey", "cryptacquirecontexta",
    "cryptcreatehash", "cryptencrypt", "cryptgenkey",
    "cryptimportkey", "crypthashdata"
]

# columns that are related to registry API calls
registry_api_cols = [
    "regopenkeya", "regsetkeyvaluew", "regdeletekeya",
    "regdeletevaluea", "regnotifychangekeyvalue"
]

# columns that are related to network API calls
network_api_cols = [
    "internetopena", "internetopenurla", "internetreadfile",
    "httpopenrequesta", "httpsendrequesta", "winhttpopen",
    "winhttpconnect", "socket"
]

def present_data(df, cols):
    cols = [c for c in cols if c in df.columns]
    if not cols:
        return pd.Series(0, index=df.index)
    return df[cols].sum(axis=1)

def engineer_features(df):
    df = df.copy()
    df["num_file_apis"] = present_data(df, file_api_cols)
    df["num_crypto_apis"] = present_data(df, crypto_api_cols)
    df["num_registry_apis"] = present_data(df, registry_api_cols)
    df["num_network_apis"] = present_data(df, network_api_cols)
    df["has_crypto"] = (df["num_crypto_apis"] > 0).astype(int)
    df["has_file_access"] = (df["num_file_apis"] > 0).astype(int)
    df["has_network"] = (df["num_network_apis"] > 0).astype(int)

    if "SizeOfImage" in df.columns and "SizeOfCode" in df.columns:
        df["code_to_image_ratio"] = df["SizeOfCode"] / df["SizeOfImage"].replace(0,1)
    else:
        df["code_to_image_ratio"] = 0
    if "IMPORT_size" in df.columns and "SizeOfImage" in df.columns:
        df["import_to_image_ratio"] = df["IMPORT_size"] / df["SizeOfImage"].replace(0,1)
    else:
        df["import_to_image_ratio"] = 0
        
    packer_columns = [c for c in df.columns if c.lower() in {"upx0", "upx1", "upx2", ".aspack", ".mpress1", ".mpress2"}]
    if packer_columns:
        df["has_packer"] = (df[packer_columns].sum(axis=1) > 0).astype(int)
    else:
        df["has_packer"] = 0

    return df

def main():
    #LOCAL_PATH = "/Users/doro/Library/CloudStorage/OneDrive-Personal/SCHOOL/SJSU/Semester 4/CMPE 209/project/cmpe209-ransomware/"
    LOCAL_PATH = "/Users/yanpingli/Desktop/209proj/cmpe209-ransomware/"
    INPUT_PATH = LOCAL_PATH + "data/processed"

    print("Running random forest with feature engineering ------------------------------------------")

    X_TRAIN, Y_TRAIN, X_TEST, Y_TEST = rf_a.read_data(INPUT_PATH)

    print ("Start Feature Engineering --------------------------------------------")
    
    X_train_fe = engineer_features(X_TRAIN)
    X_test_fe = engineer_features(X_TEST)

    X_test_fe = X_test_fe.reindex(columns=X_train_fe.columns, fill_value=0)
        
    print("Finish Feature Engineering ------------------------------------------")
    
    print("Training random forest model with Feature Engineering ------------------------------------------")
    rf_model = rf_a.run_random_forest_model(X_train_fe, Y_TRAIN)
    joblib.dump(rf_model, "saved_model/rf_b_feature_engineer.pk1")
    joblib.dump(X_train_fe.columns.tolist(), "saved_model/rf_b_feature_col.pk1")
    rf_a.evaluate_random_forest_model(rf_model, X_test_fe, Y_TEST)
    
    print("Finished --------------------------------------------------------------")

if __name__ == "__main__":
    main()