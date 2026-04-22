# Ransomware Analysis Report

## 1. Sample Information
- **Sample ID:** {{ID}}
- **Filename:** {{filename}}
- **Analysis Date:** {{analysis_date}}
- **Sandbox Tool:** {{sandbox_tool}}
- **Environment:** {{environment}}

---

## 2. Executive Summary
- **Overall Verdict:** {{overall_verdict}}
- **ML Prediction:** {{ml_prediction}}
- **ML Confidence Score:** {{ml_confidence}}
- **Risk Level:** {{risk_level}}

### Summary for User
This sample was analyzed using a machine learning pipeline and a sandbox-oriented report template. The sample appears to be:

**{{short_conclusion}}**

---

## 3. Static Indicators
### Important Structural Indicators
{{top_indicators_bullets}}

### Notes
These indicators come from the structural feature dataset used for classification. They represent important model-selected indicators associated with ransomware or benign software.

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
The model classified this sample based on the influential structural indicators listed above. A higher ransomware probability suggests stronger similarity to ransomware samples in the training data.

---

## 6. Combined Assessment
### Why it was flagged
- Static indicators suggest: {{static_assessment}}
- Sandbox behavior suggests: {{sandbox_assessment}}
- Combined conclusion: {{combined_conclusion}}

### Analyst Note
This report combines:
1. Static ML classification
2. Dynamic sandbox behavior placeholders or observations
3. A readable explanation for the user

---

## 7. Recommended Action
{{recommended_actions_bullets}}

---

## 8. Artifact Summary
- **PCAP available:** {{pcap_available}}
- **Memory dump available:** {{memory_dump_available}}
- **Dropped files extracted:** {{dropped_files_extracted}}
- **Screenshots available:** {{screenshots_available}}
- **Raw sandbox JSON available:** {{raw_json_available}}

---

## 9. Final Verdict
**Final Classification:** {{overall_verdict}}  
**Confidence:** {{confidence_text}}  
**Risk Level:** {{risk_level}}  
**Short Final Statement:** {{final_statement}}
