#!/usr/bin/env python3
import os
import pandas as pd
import RF_A as rf_a
import RF_B as rf_b
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def select_top_features(X_train, y_train, k=50):
    temp_model = RandomForestClassifier(n_estimators=100, random_state=42)
    temp_model.fit(X_train, y_train)

    importances = pd.Series(temp_model.feature_importances_, index=X_train.columns).sort_values(ascending=False)
    top_features = importances.head(k).index.tolist()
    return top_features, importances

def save_outputs(model_name, rf_model, X_test_top, meta_test, y_pred, y_proba, metrics, top_features, importances):
    os.makedirs("results", exist_ok=True)
    os.makedirs("saved_model", exist_ok=True)

    prediction_report = meta_test.copy()
    prediction_report["predicted_RG"] = y_pred
    prediction_report["ransomware_probability"] = y_proba
    prediction_report["risk_level"] = prediction_report["ransomware_probability"].apply(rf_a.risk_level)
    prediction_report["model_name"] = model_name
    prediction_report["feature_strategy"] = f"Top-{len(top_features)} selected features after feature engineering"

    prediction_report.to_csv(f"results/{model_name}_prediction_report.csv", index=False)

    feature_importance = pd.DataFrame({
        "feature": X_test_top.columns,
        "importance": rf_model.feature_importances_
    }).sort_values(by="importance", ascending=False)
    feature_importance.to_csv(f"results/{model_name}_feature_importance.csv", index=False)

    selected_importances = importances.loc[top_features].reset_index()
    selected_importances.columns = ["feature", "preselection_importance"]
    selected_importances.to_csv(f"results/{model_name}_selected_features.csv", index=False)

    metrics_df = pd.DataFrame([metrics])
    metrics_df["model_name"] = model_name
    metrics_df.to_csv(f"results/{model_name}_metrics.csv", index=False)

    joblib.dump(rf_model, f"saved_model/{model_name}.pk1")
    joblib.dump(top_features, f"saved_model/{model_name}_feature_cols.pk1")

    print(f"Saved: results/{model_name}_prediction_report.csv")
    print(f"Saved: results/{model_name}_feature_importance.csv")
    print(f"Saved: results/{model_name}_selected_features.csv")
    print(f"Saved: results/{model_name}_metrics.csv")
    print(f"Saved: saved_model/{model_name}.pk1")
    print(f"Saved: saved_model/{model_name}_feature_cols.pk1")

def main():
    INPUT_PATH = "data/processed"

    print("Running RF with top-k feature selection --------------------------------")

    X_TRAIN, Y_TRAIN, X_TEST, Y_TEST, meta_test = rf_a.read_data(INPUT_PATH)

    X_train_fe = rf_b.engineer_features(X_TRAIN)
    X_test_fe = rf_b.engineer_features(X_TEST)

    X_test_fe = X_test_fe.reindex(columns=X_train_fe.columns, fill_value=0)

    for k in [10, 20, 50, 100, 200]:
        model_name = f"rf_c_top{k}"
        print(f"\nSelecting top-{k} features --------------------------------")
        top_features, importances = select_top_features(X_train_fe, Y_TRAIN, k=k)
        X_train_top = X_train_fe[top_features]
        X_test_top = X_test_fe[top_features]
        rf_model = rf_a.run_random_forest_model(X_train_top, Y_TRAIN)
        y_pred, y_proba, metrics = rf_a.evaluate_random_forest_model(rf_model, X_test_top, Y_TEST)
        save_outputs(model_name, rf_model, X_test_top, meta_test, y_pred, y_proba, metrics, top_features, importances)

    print("Finished --------------------------------")


if __name__ == "__main__":
    main()
