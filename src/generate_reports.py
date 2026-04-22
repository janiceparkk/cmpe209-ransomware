#!/usr/bin/env python3
import argparse
import os
from datetime import datetime

import pandas as pd


TECH_TEMPLATE_PATH = "docs/templates/technical_report_template.md"
USER_TEMPLATE_PATH = "docs/templates/user_report_template.md"
OUTPUT_DIR = "docs/generated_reports"
DEFAULT_PREDICTION_REPORT = "results/prediction_report.csv"
DEFAULT_FEATURE_IMPORTANCE = "results/feature_importance.csv"


def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def save_text(path: str, text: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def to_yes_no(value) -> str:
    if isinstance(value, str):
        cleaned = value.strip().lower()
        if cleaned in {"yes", "y", "true", "1"}:
            return "Yes"
        if cleaned in {"no", "n", "false", "0"}:
            return "No"
    if isinstance(value, (int, float)):
        return "Yes" if value else "No"
    return str(value)


def safe_get(row: pd.Series, col: str, default: str = "N/A") -> str:
    if col in row.index and pd.notna(row[col]):
        return str(row[col])
    return default


def risk_to_confidence_text(probability: float) -> str:
    if probability >= 0.90:
        return "Very High"
    if probability >= 0.70:
        return "High"
    if probability >= 0.40:
        return "Medium"
    return "Low"


def probability_to_risk(probability: float) -> str:
    if probability >= 0.70:
        return "High"
    if probability >= 0.40:
        return "Medium"
    return "Low"


def probability_to_verdict(probability: float) -> str:
    if probability >= 0.70:
        return "Ransomware Likely"
    if probability >= 0.40:
        return "Suspicious"
    return "Benign"


def probability_to_prediction(probability: float) -> str:
    return "Ransomware" if probability >= 0.50 else "Goodware"


def format_bullets(items):
    if not items:
        return "- None provided"
    return "\n".join(f"- {item}" for item in items)


def format_numbered(items):
    if not items:
        return "1. None provided"
    return "\n".join(f"{i+1}. {item}" for i, item in enumerate(items))


def get_top_features(feature_importance_df: pd.DataFrame, top_n: int = 5):
    if "feature" not in feature_importance_df.columns or "importance" not in feature_importance_df.columns:
        return []
    top_df = feature_importance_df.sort_values("importance", ascending=False).head(top_n)
    return [
        f"{row['feature']} (importance={row['importance']:.6f})"
        for _, row in top_df.iterrows()
    ]


def choose_recommended_actions(risk_level: str):
    if risk_level == "High":
        return [
            "Do not execute this file outside the sandbox.",
            "Quarantine the sample immediately.",
            "Preserve logs, predictions, and related artifacts.",
            "Escalate to the team for deeper investigation.",
        ]
    if risk_level == "Medium":
        return [
            "Do not trust the file until additional review is completed.",
            "Keep the sample isolated in the sandbox environment.",
            "Review related artifacts and model explanations.",
            "Escalate for secondary analysis if needed.",
        ]
    return [
        "No immediate malicious verdict was assigned.",
        "Keep the file under observation if needed.",
        "Review artifacts if additional context is required.",
    ]


def choose_observations(risk_level: str, sandbox_tool: str):
    if risk_level == "High":
        return [
            f"Analysis was prepared for sandbox reporting using {sandbox_tool}.",
            "The ML system identified strong ransomware-like structural patterns.",
            "This sample should be treated as high risk until reviewed further.",
        ]
    if risk_level == "Medium":
        return [
            f"Analysis was prepared for sandbox reporting using {sandbox_tool}.",
            "The ML system identified suspicious but not definitive ransomware-like patterns.",
            "Further dynamic analysis is recommended.",
        ]
    return [
        f"Analysis was prepared for sandbox reporting using {sandbox_tool}.",
        "The ML system did not assign a strong ransomware likelihood.",
        "Dynamic analysis can still be used for additional verification.",
    ]


def choose_why_flagged(risk_level: str, top_features):
    feature_text = ", ".join([f.split(" (importance=")[0] for f in top_features[:3]]) if top_features else "model-selected structural indicators"
    if risk_level == "High":
        return [
            "The file showed strong similarity to ransomware samples in the training data.",
            f"The most influential indicators included {feature_text}.",
            "The assigned ransomware probability placed the sample in the high-risk range.",
        ]
    if risk_level == "Medium":
        return [
            "The file showed some suspicious similarity to ransomware samples.",
            f"Important indicators included {feature_text}.",
            "The assigned ransomware probability placed the sample in the medium-risk range.",
        ]
    return [
        "The file did not show strong ransomware similarity in the model output.",
        f"The model still relied on indicators such as {feature_text}.",
        "The assigned ransomware probability remained in the low-risk range.",
    ]


def build_replacements(sample_row: pd.Series, top_features, analysis_date: str, sandbox_tool: str, environment: str):
    probability = None

    if "ransomware_probability" in sample_row.index and pd.notna(sample_row["ransomware_probability"]):
        probability = float(sample_row["ransomware_probability"])
    elif "probability" in sample_row.index and pd.notna(sample_row["probability"]):
        probability = float(sample_row["probability"])
    else:
        predicted_rg = None
        if "predicted_RG" in sample_row.index and pd.notna(sample_row["predicted_RG"]):
            predicted_rg = int(sample_row["predicted_RG"])
        elif "RG" in sample_row.index and pd.notna(sample_row["RG"]):
            predicted_rg = int(sample_row["RG"])
        probability = 0.90 if predicted_rg == 1 else 0.10

    risk_level = safe_get(sample_row, "risk_level", probability_to_risk(probability))
    ml_prediction = probability_to_prediction(probability)
    overall_verdict = probability_to_verdict(probability)
    confidence_text = risk_to_confidence_text(probability)

    recommended_actions = choose_recommended_actions(risk_level)
    observations = choose_observations(risk_level, sandbox_tool)
    why_flagged = choose_why_flagged(risk_level, top_features)

    short_conclusion = (
        "Likely ransomware based on strong model confidence."
        if risk_level == "High"
        else "Suspicious and worth deeper investigation."
        if risk_level == "Medium"
        else "Currently appears lower risk based on available ML evidence."
    )

    static_assessment = (
        "The most influential structural indicators are strongly associated with ransomware-like samples."
        if risk_level == "High"
        else "Several structural indicators appear suspicious and may warrant further review."
        if risk_level == "Medium"
        else "Static indicators do not strongly suggest ransomware based on the current model output."
    )

    sandbox_assessment = (
        "Dynamic sandbox findings should be used to confirm file, process, registry, and network behavior."
    )

    combined_conclusion = (
        "The combined evidence supports a high-risk ransomware-oriented classification."
        if risk_level == "High"
        else "The combined evidence supports a suspicious classification pending dynamic confirmation."
        if risk_level == "Medium"
        else "The combined evidence does not currently support a high-risk ransomware conclusion."
    )

    final_statement = (
        f"{safe_get(sample_row, 'filename')} was classified as {ml_prediction.lower()} with {confidence_text.lower()} confidence and {risk_level.lower()} risk."
    )

    replacements = {
        "ID": safe_get(sample_row, "ID", "N/A"),
        "filename": safe_get(sample_row, "filename", "N/A"),
        "analysis_date": analysis_date,
        "sandbox_tool": sandbox_tool,
        "environment": environment,
        "overall_verdict": overall_verdict,
        "ml_prediction": ml_prediction,
        "ml_confidence": f"{probability:.4f}",
        "risk_level": risk_level,
        "short_conclusion": short_conclusion,
        "top_indicators_bullets": format_bullets([f.split(' (importance=')[0] for f in top_features]),
        "top_features_numbered": format_numbered(top_features),
        "process_count": safe_get(sample_row, "process_count", "Not provided"),
        "suspicious_child_processes": safe_get(sample_row, "suspicious_child_processes", "Not provided"),
        "command_line_anomalies": safe_get(sample_row, "command_line_anomalies", "Not provided"),
        "process_injection": safe_get(sample_row, "process_injection", "Not provided"),
        "process_patterns": safe_get(sample_row, "process_patterns", "Not provided"),
        "files_created": safe_get(sample_row, "files_created", "Not provided"),
        "files_modified": safe_get(sample_row, "files_modified", "Not provided"),
        "files_deleted": safe_get(sample_row, "files_deleted", "Not provided"),
        "dropped_files": safe_get(sample_row, "dropped_files", "Not provided"),
        "suspicious_extensions": safe_get(sample_row, "suspicious_extensions", "Not provided"),
        "encryption_behavior": safe_get(sample_row, "encryption_behavior", "Not provided"),
        "registry_created": safe_get(sample_row, "registry_created", "Not provided"),
        "registry_modified": safe_get(sample_row, "registry_modified", "Not provided"),
        "persistence_changes": safe_get(sample_row, "persistence_changes", "Not provided"),
        "startup_changes": safe_get(sample_row, "startup_changes", "Not provided"),
        "domains_contacted": safe_get(sample_row, "domains_contacted", "Not provided"),
        "ips_contacted": safe_get(sample_row, "ips_contacted", "Not provided"),
        "protocols_observed": safe_get(sample_row, "protocols_observed", "Not provided"),
        "dns_requests": safe_get(sample_row, "dns_requests", "Not provided"),
        "http_traffic": safe_get(sample_row, "http_traffic", "Not provided"),
        "suspicious_outbound": safe_get(sample_row, "suspicious_outbound", "Not provided"),
        "behavior_signatures_bullets": format_bullets(
            [
                safe_get(sample_row, "signature_1", ""),
                safe_get(sample_row, "signature_2", ""),
                safe_get(sample_row, "signature_3", ""),
            ]
        ),
        "screenshot_count": safe_get(sample_row, "screenshot_count", "Not provided"),
        "ui_behavior": safe_get(sample_row, "ui_behavior", "Not provided"),
        "ransom_note_observed": safe_get(sample_row, "ransom_note_observed", "Not provided"),
        "static_assessment": static_assessment,
        "sandbox_assessment": sandbox_assessment,
        "combined_conclusion": combined_conclusion,
        "recommended_actions_bullets": format_bullets(recommended_actions),
        "pcap_available": to_yes_no(safe_get(sample_row, "pcap_available", "No")),
        "memory_dump_available": to_yes_no(safe_get(sample_row, "memory_dump_available", "No")),
        "dropped_files_extracted": to_yes_no(safe_get(sample_row, "dropped_files_extracted", "No")),
        "screenshots_available": to_yes_no(safe_get(sample_row, "screenshots_available", "No")),
        "raw_json_available": to_yes_no(safe_get(sample_row, "raw_json_available", "No")),
        "confidence_text": confidence_text,
        "final_statement": final_statement,
        "why_flagged_bullets": format_bullets(why_flagged),
        "what_was_observed_bullets": format_bullets(observations),
    }

    return replacements


def render_template(template_text: str, replacements: dict) -> str:
    rendered = template_text
    for key, value in replacements.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", str(value))
    return rendered


def sanitize_filename(value: str) -> str:
    allowed = []
    for ch in value:
        if ch.isalnum() or ch in {"-", "_", "."}:
            allowed.append(ch)
        else:
            allowed.append("_")
    return "".join(allowed)


def main():
    parser = argparse.ArgumentParser(description="Generate technical and user-readable reports from prediction outputs.")
    parser.add_argument("--prediction-report", default=DEFAULT_PREDICTION_REPORT, help="Path to prediction_report.csv")
    parser.add_argument("--feature-importance", default=DEFAULT_FEATURE_IMPORTANCE, help="Path to feature_importance.csv")
    parser.add_argument("--sample-id", default=None, help="Optional sample ID to generate a report for one sample")
    parser.add_argument("--top-n", type=int, default=5, help="Number of top features to include")
    parser.add_argument("--sandbox-tool", default="Cuckoo/CAPE", help="Sandbox tool name shown in the report")
    parser.add_argument("--environment", default="Windows guest VM on isolated sandbox", help="Environment shown in the report")
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    prediction_df = pd.read_csv(args.prediction_report)
    feature_importance_df = pd.read_csv(args.feature_importance)

    if prediction_df.empty:
        raise ValueError("prediction_report.csv is empty.")

    if args.sample_id is not None:
        candidates = prediction_df[prediction_df["ID"].astype(str) == str(args.sample_id)]
        if candidates.empty:
            raise ValueError(f"No sample found with ID={args.sample_id}")
        prediction_df = candidates.head(1)

    tech_template = load_text(TECH_TEMPLATE_PATH)
    user_template = load_text(USER_TEMPLATE_PATH)
    top_features = get_top_features(feature_importance_df, top_n=args.top_n)
    analysis_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for _, row in prediction_df.iterrows():
        replacements = build_replacements(
            sample_row=row,
            top_features=top_features,
            analysis_date=analysis_date,
            sandbox_tool=args.sandbox_tool,
            environment=args.environment,
        )

        tech_report = render_template(tech_template, replacements)
        user_report = render_template(user_template, replacements)

        sample_id = replacements["ID"]
        filename = sanitize_filename(replacements["filename"])

        tech_output = os.path.join(OUTPUT_DIR, f"technical_report_{sample_id}_{filename}.md")
        user_output = os.path.join(OUTPUT_DIR, f"user_report_{sample_id}_{filename}.md")

        save_text(tech_output, tech_report)
        save_text(user_output, user_report)

        print(f"Generated: {tech_output}")
        print(f"Generated: {user_output}")


if __name__ == "__main__":
    main()
