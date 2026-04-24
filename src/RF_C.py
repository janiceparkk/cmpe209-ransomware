import pandas as pd
import RF_A as rf_a
import RF_B as rf_b
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def select_top_features(X_train, y_train, k=50):
    temp_model = RandomForestClassifier(n_estimators=100, random_state=42)
    temp_model.fit(X_train, y_train)

    importances = pd.Series(temp_model.feature_importances_, index=X_train.columns)
    importances = importances.sort_values(ascending=False)

    top_features = importances.head(k).index.tolist()
    return top_features, importances

def main():
    LOCAL_PATH = "/Users/yanpingli/Desktop/209proj/cmpe209-ransomware/"
    INPUT_PATH = LOCAL_PATH + "data/processed"

    print("Running RF with top-k feature selection --------------------------------")

    X_TRAIN, Y_TRAIN, X_TEST, Y_TEST = rf_a.read_data(INPUT_PATH)

    X_train_fe = rf_b.engineer_features(X_TRAIN)
    X_test_fe = rf_b.engineer_features(X_TEST)

    X_test_fe = X_test_fe.reindex(columns=X_train_fe.columns, fill_value=0)

    for k in [10, 20, 50, 100, 200]:
        top_features, importances = select_top_features(X_train_fe, Y_TRAIN, k=k)
        X_train_top = X_train_fe[top_features]
        X_test_top = X_test_fe[top_features]
        rf_model = rf_a.run_random_forest_model(X_train_top, Y_TRAIN)
        joblib.dump(rf_model, f"saved_model/rf_c_top{k}.pk1")
        joblib.dump(top_features, f"saved_model/rf_c_{k}_features.pk1")
        print(f"\nTop{k} features")
        rf_a.evaluate_random_forest_model(rf_model, X_test_top, Y_TEST)

    print("Finished --------------------------------")


if __name__ == "__main__":
    main()