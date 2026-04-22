#!/usr/bin/env bash
set -e

echo "============================================================"
echo "Starting full ransomware ML demo pipeline"
echo "============================================================"

echo
echo "[1/11] Activating virtual environment"
source venv/bin/activate

echo
echo "[2/11] Running dataset inspection"
python3 src/inspect_dataset.py

echo
echo "[3/11] Preparing processed train/test files"
python3 src/prepare_data.py

echo
echo "[4/11] Training RF_A baseline model"
python3 src/RF_A.py

echo
echo "[5/11] Training RF_B feature-engineered model"
python3 src/RF_B.py

echo
echo "[6/11] Training RF_C top-k models"
python3 src/RF_C.py

echo
echo "[7/11] Summarizing model metrics"
python3 src/summarize_model_metrics.py

echo
echo "[8/11] Creating ransomware demo sample"
python3 src/create_demo_sample.py --label 1 --row-index 0

echo
echo "[9/11] Predicting ransomware demo sample with RF_B"
python3 src/predict_demo_sample.py \
  --model-path saved_model/rf_b_feature_engineer.pk1 \
  --feature-cols saved_model/rf_b_feature_engineer_feature_cols.pk1 \
  --engineer

echo
echo "[10/11] Generating RF_B report for ransomware demo sample"
RANSOMWARE_ID=$(python3 -c "import pandas as pd; print(pd.read_csv('demo/demo_meta.csv').iloc[0]['ID'])")
python3 src/generate_reports.py \
  --input results/rf_b_feature_engineer_prediction_report.csv \
  --feature-importance results/rf_b_feature_engineer_feature_importance.csv \
  --model-name RF_B \
  --feature-strategy 'Feature-engineered grouped API and IOC indicators' \
  --sample-id "$RANSOMWARE_ID"

echo
echo "[11/11] Creating goodware demo sample"
python3 src/create_demo_sample.py --label 0 --row-index 0

echo
echo "[12/12] Predicting goodware demo sample with RF_C top-50"
python3 src/predict_demo_sample.py \
  --model-path saved_model/rf_c_top50.pk1 \
  --feature-cols saved_model/rf_c_top50_feature_cols.pk1 \
  --engineer

echo
echo "[13/13] Generating RF_C top-50 report for goodware demo sample"
GOODWARE_ID=$(python3 -c "import pandas as pd; print(pd.read_csv('demo/demo_meta.csv').iloc[0]['ID'])")
python3 src/generate_reports.py \
  --input results/rf_c_top50_prediction_report.csv \
  --feature-importance results/rf_c_top50_feature_importance.csv \
  --model-name RF_C_top50 \
  --feature-strategy 'Top-50 selected features after feature engineering' \
  --sample-id "$GOODWARE_ID"

echo
echo "============================================================"
echo "Pipeline complete"
echo "============================================================"
echo
echo "Key outputs:"
echo " - results/model_comparison_summary.csv"
echo " - results/demo_prediction_report.csv"
echo " - docs/generated_reports/"
echo
