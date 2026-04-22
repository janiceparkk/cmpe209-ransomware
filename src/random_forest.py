import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

LOCAL_PATH = "/Users/doro/Library/CloudStorage/OneDrive-Personal/SCHOOL/SJSU/Semester 4/CMPE 209/project/cmpe209-ransomware/"
INPUT_PATH = LOCAL_PATH + "data/processed"
X_TRAIN = pd.read_csv(INPUT_PATH + "/X_train.csv")
Y_TRAIN = pd.read_csv(INPUT_PATH + "/y_train.csv")

X_TEST = pd.read_csv(INPUT_PATH + "/X_test.csv")
Y_TEST = pd.read_csv(INPUT_PATH + "/y_test.csv")

# family = 0 means goodware | everything else is malware/ransomware
# can reduce dimensionality by summing API category counts, DLL category counts, 
    # suspicious capability flags, packing/obfuscation factors, ratios and summary stats

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

def random_forest_model(X_TRAIN, Y_TRAIN):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_TRAIN, Y_TRAIN)
    return model

def evaluate_model(model, X_TEST, Y_TEST):
    y_pred = model.predict(X_TEST)
    print(classification_report(Y_TEST, y_pred))
    print(confusion_matrix(Y_TEST, y_pred))
    print(accuracy_score(Y_TEST, y_pred))

def main():
    print ("extracting features here --------------------------------------------")
    
    X_TRAIN["num_file_apis"] = present_data(X_TRAIN, file_api_cols)
    X_TRAIN["num_crypto_apis"] = present_data(X_TRAIN, crypto_api_cols)
    X_TRAIN["num_registry_apis"] = present_data(X_TRAIN, registry_api_cols)
    X_TRAIN["num_network_apis"] = present_data(X_TRAIN, network_api_cols)

    X_TRAIN["has_crypto"] = (X_TRAIN["num_crypto_apis"] > 0).astype(int)
    X_TRAIN["has_file_access"] = (X_TRAIN["num_file_apis"] > 0).astype(int)
    X_TRAIN["has_network"] = (X_TRAIN["num_network_apis"] > 0).astype(int)
    
    if "SizeOfImage" in X_TRAIN.columns and "SizeOfCode" in X_TRAIN.columns:
        X_TRAIN["code_to_image_ratio"] = X_TRAIN["SizeOfCode"] / X_TRAIN["SizeOfImage"].replace(0,1)
    
    if "IMPORT_size" in X_TRAIN.columns and "SizeOfImage" in X_TRAIN.columns:
        X_TRAIN["import_to_image_ratio"] = X_TRAIN["IMPORT_size"] / X_TRAIN["SizeOfImage"].replace(0,1)
        
    packer_columns = [c for c in X_TRAIN.columns if c.lower() in {"upx0", "upx1", "upx2", ".aspack", ".mpress1", ".mpress2"}]
    if packer_columns:
        X_TRAIN["has_packer"] = (X_TRAIN[packer_columns].sum(axis=1) > 0).astype(int)
    else:
        X_TRAIN["has_packer"] = 0
        
    print("finished extracting features ------------------------------------------")
    
    print("training random forest model ------------------------------------------")
    rf_model = random_forest_model(X_TRAIN, Y_TRAIN)
    
    print("evaluating random forest model ------------------------------------------")
    evaluate_model(rf_model, X_TEST, Y_TEST)
    
    print("finished --------------------------------------------------------------")

if __name__ == "__main__":
    main()