# Ransomware Analysis Report

## 1. Sample Information
- **Sample ID:** {{ID}}
- **Filename:** {{filename}}
- **Analysis Date:** {{analysis_date}}
- **Model Name:** {{model_name}}
- **Feature Strategy:** {{feature_strategy}}
- **Sandbox Tool:** {{sandbox_tool}}
- **Environment:** {{environment}}

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

## 4. Dynamic Sandbox Findings
### 4.1 Process Activity
- Number of processes created: {{process_count}}
- Suspicious child processes observed: {{suspicious_child_processes}}
- Command-line anomalies: {{command_line_anomalies}}
- Unexpected process injection behavior: {{process_injection}}
- Process termination or spawning patterns: {{process_patterns}}

### 4.2 File System Activity
- Files created: {{files_created}}
- Files modified: {{files_modified}}
- Files deleted: {{files_deleted}}
- Dropped files: {{dropped_files}}
- Suspicious file extensions or renaming behavior: {{suspicious_extensions}}
- Evidence of encryption-like behavior: {{encryption_behavior}}

### 4.3 Registry Activity
- Registry keys created: {{registry_created}}
- Registry keys modified: {{registry_modified}}
- Persistence-related changes: {{persistence_changes}}
- Startup/run key changes: {{startup_changes}}

### 4.4 Network Activity
- Domains contacted: {{domains_contacted}}
- IP addresses contacted: {{ips_contacted}}
- Protocols observed: {{protocols_observed}}
- DNS requests: {{dns_requests}}
- HTTP/HTTPS traffic: {{http_traffic}}
- Suspicious outbound communication: {{suspicious_outbound}}

### 4.5 Behavioral Signatures
{{behavior_signatures_bullets}}

### 4.6 Screenshots / UI Evidence
- Screenshot count: {{screenshot_count}}
- Notable user-facing behavior: {{ui_behavior}}
- Ransom note observed: {{ransom_note_observed}}

---

## 5. Machine Learning Output
- **Predicted Class:** {{ml_prediction}}
- **Probability of Ransomware:** {{ml_confidence}}
- **Assigned Risk Level:** {{risk_level}}

### Top Influential Features
{{top_features_numbered}}

### Interpretation
The model classified this sample based on the structural indicators listed above. These features were the most influential in the final prediction.

---

## 6. Combined Assessment
- **Static assessment:** {{static_assessment}}

### Why it was flagged
{{why_flagged_bullets}}

---

## 7. Recommended Action
{{recommended_actions_bullets}}

---

## 8. Artifact Summary
- **PCAP available:** {{pcap_available}}
- **Memory dump available:** {{memory_dump_available}}
- **Dropped files extracted:** {{dropped_files_extracted}}
- **Screenshots available:** {{screenshots_available}}

---

## 9. Final Verdict
**Final Classification:** {{overall_verdict}}  
**Confidence:** {{confidence_text}}  
**Risk Level:** {{risk_level}}  
**Short Final Statement:** {{final_statement}}
