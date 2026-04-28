# Ransomware Analysis Report

## 1. Sample Information
- **Sample ID:** {{ID}}
- **Filename:** {{filename}}
- **Analysis Date:** {{analysis_date}}
- **Model Name:** {{model_name}}
- **Feature Strategy:** {{feature_strategy}}

---

## 2. Executive Summary
- **Overall Verdict:** {{overall_verdict}}
- **ML Prediction:** {{ml_prediction}}
- **ML Confidence Score:** {{ml_confidence}}
- **Risk Level:** {{risk_level}}

### Summary for User
This sample was analyzed using the **{{model_name}}** model.

**{{short_conclusion}}**

---

## 3. Static ML Analysis
### Model Used
- **Model Name:** {{model_name}}
- **Feature Strategy:** {{feature_strategy}}

### Important Structural Indicators
{{top_indicators_bullets}}

### Notes
These indicators represent the most influential model-selected features associated with the prediction.

---

## 4. Machine Learning Output
- **Predicted Class:** {{ml_prediction}}
- **Probability of Ransomware:** {{ml_confidence}}
- **Assigned Risk Level:** {{risk_level}}

### Top Influential Features
{{top_features_numbered}}

### Interpretation
The model classified this sample based on the structural indicators listed above. These features were the most influential in the final prediction.

---

## 5. Assessment
- **Static assessment:** {{static_assessment}}
- **Combined conclusion:** {{combined_conclusion}}

### Why it was flagged
{{why_flagged_bullets}}

---

## 6. Recommended Action
{{recommended_actions_bullets}}

---

## 7. Final Verdict
**Final Classification:** {{overall_verdict}}  
**Confidence:** {{confidence_text}}  
**Risk Level:** {{risk_level}}  
**Short Final Statement:** {{final_statement}}
