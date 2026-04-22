# Ransomware ML Project

This project uses the Mendeley `combined_without_3gram.csv` dataset for ransomware vs goodware classification.
https://data.mendeley.com/datasets/yzhcvn7sj5/3

The main deliverable is a **user-readable ransomware analysis report** that combines:
- model prediction
- confidence / risk level
- top influential indicators

## Installation Requirements 
```
$ pip install -r requirements.txt 
```

## Dataset location
```data/raw/combined_without_3gram.csv```

## Main columns
- ID
- filename
- RG (target label)
- family

## Label meaning
- RG = 1 -> ransomware
- RG = 0 -> goodware

## Official split used
Training:
- goodware with ID <= 11133
- ransomware families 1 to 25

Testing:
- goodware with ID >= 12000
- ransomware families 26 to 40

This split approach is able to test on new/unencountered ransomware. This reduces overfitting to specific ransomware families and the model learns general ransomwar patterns. This approach also simulates real deployment scenarios for future/unknown families.

## Run order
1. inspect_dataset.py
2. prepare_data.py
3. RF_A.py
4. RF_B.py
5. RF_C.py
6. summarize_model_metrics.py - this creates results/model_comparison_summary.csv

## Random Forest
1. RF_A.py - Baseline random forest model with all original feautres
2. RF_B.py - Random forest with original and engineered features based on ransomware behavior counts.
3. RF_C.py - Random forest with only engineered top k features.
**Modify variable PATH based on your own local path if necessary
**All models and corresponding feature list is saved in `/saved_model`

## Creating and Running a Demo Sample
1. Create a Ransomware Sample
```
python3 src/create_demo_sample.py --label 1 --row-index 0
```

2. Create a Goodware Sample
```
python3 src/create_demo_sample.py --label 0 --row-index 0
```

3. Make sure these files are created after running 1. & 2.
```
demo/demo_X.csv
demo/demo_y.csv
demo/demo_meta.csv
```

4. Run the Demo with RF_A
```
python3 src/predict_demo_sample.py \
  --model-path saved_model/rf_a_baseline.pk1
```

5. Run the Demo with RF_B
```
python3 src/predict_demo_sample.py \
  --model-path saved_model/rf_b_feature_engineer.pk1 \
  --feature-cols saved_model/rf_b_feature_engineer_feature_cols.pk1 \
  --engineer
```

6. Run the Demo with RF_C with Top 50 (customizable)
```
python3 src/predict_demo_sample.py \
  --model-path saved_model/rf_c_top50.pk1 \
  --feature-cols saved_model/rf_c_top50_feature_cols.pk1 \
  --engineer
```

7. Then check the prediction results in: 
```
results/demo_prediction_report.csv
```

## Generating a Report
There are two kinds of reports: a technical and a user-friendly report. A technical report is more thorough and assumes the reader has some cybersecurity knowledge. A user-friendly report is a more comphrensive analysis for anyone, regardless of technical background.

These steps generate both a technical and user-friendly report.
You must pass in:
1. The model-specific prediction report CSV
2. The matching model-specific feature importance CSV

1. Generating Reports for RF_A
```
python3 src/generate_reports.py \
  --input results/rf_a_baseline_prediction_report.csv \
  --feature-importance results/rf_a_baseline_feature_importance.csv \
  --model-name RF_A \
  --feature-strategy "Original processed features"
```

2. Generating Reports for RF_B
```
python3 src/generate_reports.py \
  --input results/rf_b_feature_engineer_prediction_report.csv \
  --feature-importance results/rf_b_feature_engineer_feature_importance.csv \
  --model-name RF_B \
  --feature-strategy "Feature-engineered grouped API and IOC indicators"
```

3. Generating Reports for RF_C Top 50
```
python3 src/generate_reports.py \
  --input results/rf_c_top50_prediction_report.csv \
  --feature-importance results/rf_c_top50_feature_importance.csv \
  --model-name RF_C_top50 \
  --feature-strategy "Top-50 selected features after feature engineering"
```

4. Generating Reports for One Sample Only
```
python3 src/generate_reports.py \
  --input results/rf_b_feature_engineer_prediction_report.csv \
  --feature-importance results/rf_b_feature_engineer_feature_importance.csv \
  --model-name RF_B \
  --feature-strategy "Feature-engineered grouped API and IOC indicators" \
  --sample-id 12000
```

## To run the full pipeline including report generation and demo creation please run:
```
chmod +x ./run_full_demo.sh
./run_full_demo.sh
```

## Expected Outputs

### Processed Data
```
data/processed/X_train.csv
data/processed/X_test.csv
data/processed/y_train.csv
data/processed/y_test.csv
```

### Model Outputs
```
results/rf_a_baseline_prediction_report.csv
results/rf_a_baseline_feature_importance.csv
results/rf_a_baseline_metrics.csv

results/rf_b_feature_engineer_prediction_report.csv
results/rf_b_feature_engineer_feature_importance.csv
results/rf_b_feature_engineer_metrics.csv

results/rf_c_top50_prediction_report.csv
results/rf_c_top50_feature_importance.csv
results/rf_c_top50_selected_features.csv
results/rf_c_top50_metrics.csv
```

### Demo Outputs
```
demo/demo_X.csv
demo/demo_y.csv
demo/demo_meta.csv
results/demo_prediction_report.csv
```

### Report Outputs
```
docs/generated_reports/*.md
```
