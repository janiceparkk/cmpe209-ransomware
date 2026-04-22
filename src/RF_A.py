#!/usr/bin/env python3
# RF_A.py This serves as a baseline model for the project. It is a simple Random Forest model that is used to test the data and the model.
import os
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, precision_score, recall_score, f1_score

def read_data(INPUT_PATH):
    print("Reading data from processed folder ------------------------------------------")
    X_TRAIN = pd.read_csv(INPUT_PATH + "/X_train.csv")
    Y_TRAIN = pd.read_csv(INPUT_PATH + "/y_train.csv").squeeze()
    X_TEST = pd.read_csv(INPUT_PATH + "/X_test.csv")
    Y_TEST = pd.read_csv(INPUT_PATH + "/y_test.csv").squeeze()
    meta_test = pd.read_csv(INPUT_PATH + "/meta_test.csv")
    print("Finished reading data ------------------------------------------")
    return X_TRAIN, Y_TRAIN, X_TEST, Y_TEST, meta_test

def run_random_forest_model(X_TRAIN, Y_TRAIN):
    print("Running random forest model ------------------------------------------")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_TRAIN, Y_TRAIN)
    print("Finished running random forest model ------------------------------------------")
    return rf_model

def evaluate_random_forest_model(rf_model, X_TEST, Y_TEST):
    print("Evaluating random forest model ------------------------------------------")
    y_pred = rf_model.predict(X_TEST)

    if hasattr(rf_model, "predict_proba"):
        y_proba = rf_model.predict_proba(X_TEST)[:, 1]
    else:
        y_proba = y_pred.astype(float)

    print("Printing classification report --------------------------------------------")
    print(classification_report(Y_TEST, y_pred))
    print("Printing confusion matrix --------------------------------------------")
    cm = confusion_matrix(Y_TEST, y_pred)
    print(cm)
    print("Printing accuracy score --------------------------------------------")
    acc = accuracy_score(Y_TEST, y_pred)
    print(acc)
    print("Finished evaluating random forest model ------------------------------------------")
    metrics = {
        "accuracy": acc,
        "precision": precision_score(Y_TEST, y_pred),
        "recall": recall_score(Y_TEST, y_pred),
        "f1_score": f1_score(Y_TEST, y_pred),
        "tn": int(cm[0][0]),
        "fp": int(cm[0][1]),
        "fn": int(cm[1][0]),
        "tp": int(cm[1][1]),
    }

    return y_pred, y_proba, metrics

def risk_level(p):
    if p >= 0.70:
        return "High"
    if p >= 0.40:
        return "Medium"
    return "Low"

def save_outputs(model_name, rf_model, X_test, meta_test, y_pred, y_proba, metrics):
    os.makedirs("results", exist_ok=True)
    os.makedirs("saved_model", exist_ok=True)

    prediction_report = meta_test.copy()
    prediction_report["predicted_RG"] = y_pred
    prediction_report["ransomware_probability"] = y_proba
    prediction_report["risk_level"] = prediction_report["ransomware_probability"].apply(risk_level)
    prediction_report["model_name"] = model_name
    prediction_report["feature_strategy"] = "Original processed features"

    prediction_report.to_csv(f"results/{model_name}_prediction_report.csv", index=False)

    feature_importance = pd.DataFrame({
        "feature": X_test.columns,
        "importance": rf_model.feature_importances_
    }).sort_values(by="importance", ascending=False)
    feature_importance.to_csv(f"results/{model_name}_feature_importance.csv", index=False)

    metrics_df = pd.DataFrame([metrics])
    metrics_df["model_name"] = model_name
    metrics_df.to_csv(f"results/{model_name}_metrics.csv", index=False)

    joblib.dump(rf_model, f"saved_model/{model_name}.pk1")

    print(f"Saved: results/{model_name}_prediction_report.csv")
    print(f"Saved: results/{model_name}_feature_importance.csv")
    print(f"Saved: results/{model_name}_metrics.csv")
    print(f"Saved: saved_model/{model_name}.pk1")

def main():
    INPUT_PATH = "data/processed"
    model_name = "rf_a_baseline"

    print("Running RF_A Original Dataset Features ------------------------------------------")
    X_TRAIN, Y_TRAIN, X_TEST, Y_TEST, meta_test = read_data(INPUT_PATH)
    rf_model = run_random_forest_model(X_TRAIN, Y_TRAIN)

    y_pred, y_proba, metrics = evaluate_random_forest_model(rf_model, X_TEST, Y_TEST)
    save_outputs(model_name, rf_model, X_TEST, meta_test, y_pred, y_proba, metrics)
    print("Finished ------------------------------------------")

if __name__ == "__main__":
    main()
