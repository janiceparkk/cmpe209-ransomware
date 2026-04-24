# RF_A.py This serves as a baseline model for the project. It is a simple Random Forest model that is used to test the data and the model.
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def read_data(INPUT_PATH):
    print("Reading data from processed folder ------------------------------------------")
    X_TRAIN = pd.read_csv(INPUT_PATH + "/X_train.csv")
    Y_TRAIN = pd.read_csv(INPUT_PATH + "/y_train.csv").squeeze()
    X_TEST = pd.read_csv(INPUT_PATH + "/X_test.csv")
    Y_TEST = pd.read_csv(INPUT_PATH + "/y_test.csv").squeeze()
    print("Finished reading data ------------------------------------------")
    return X_TRAIN, Y_TRAIN, X_TEST, Y_TEST

def run_random_forest_model(X_TRAIN, Y_TRAIN):
    print("Running random forest model ------------------------------------------")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_TRAIN, Y_TRAIN)
    print("Finished running random forest model ------------------------------------------")
    return rf_model

def evaluate_random_forest_model(rf_model, X_TEST, Y_TEST):
    print("Evaluating random forest model ------------------------------------------")
    y_pred = rf_model.predict(X_TEST)
    print("Printing classification report --------------------------------------------")
    print(classification_report(Y_TEST, y_pred))
    print("Printing confusion matrix --------------------------------------------")
    print(confusion_matrix(Y_TEST, y_pred))
    print("Printing accuracy score --------------------------------------------")
    print(accuracy_score(Y_TEST, y_pred))
    print("Finished evaluating random forest model ------------------------------------------")

def main():
    #LOCAL_PATH = "/Users/doro/Library/CloudStorage/OneDrive-Personal/SCHOOL/SJSU/Semester 4/CMPE 209/project/cmpe209-ransomware/"
    LOCAL_PATH = "/Users/yanpingli/Desktop/209proj/cmpe209-ransomware/"
    INPUT_PATH = LOCAL_PATH + "data/processed"

    print("Running RF_A Original Dataset Features ------------------------------------------")

    X_TRAIN, Y_TRAIN, X_TEST, Y_TEST = read_data(INPUT_PATH)
    rf_model = run_random_forest_model(X_TRAIN, Y_TRAIN)
    joblib.dump(rf_model, "saved_model/rf_a_baseline.pk1")
    evaluate_random_forest_model(rf_model, X_TEST, Y_TEST)
    print("Finished ------------------------------------------")

if __name__ == "__main__":
    main()
