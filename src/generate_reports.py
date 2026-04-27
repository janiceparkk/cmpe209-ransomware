import argparse
import os
from datetime import datetime

import pandas as pd


TECH_TEMPLATE_PATH = "docs/templates/technical_report_template.md"
USER_TEMPLATE_PATH = "docs/templates/user_report_template.md"
OUTPUT_DIR = "docs/generated_reports"


def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def save_text(path: str, text: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


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


def probability_to_verdict(probability: float) -> str:
    if probability >= 0.70:
        return "Ransomware Likely"
    if probability >= 0.40:
        return "Suspicious"
    return "Benign"


def probability_to_prediction(probability: float) -> str:
    return "Ransomware" if probability >= 0.50 else "Goodware"


def format_bullets(items):
    cleaned = []
    for x in items:
        s = str(x).strip()
        if s and s.lower() not in {"none", "none provided", "not provided", "nan", "n/a"}:
            cleaned.append(s)
    if not cleaned:
        return "- None provided"
    return "\n".join(f"- {item}" for item in cleaned)


def format_numbered(items):
    cleaned = [str(x).strip() for x in items if str(x).strip()]
    if not cleaned:
        return "1. None provided"
    return "\n".join(f"{i+1}. {item}" for i, item in enumerate(cleaned))


def get_top_features(feature_importance_df: pd.DataFrame, top_n: int = 5):
    if "feature" not in feature_importance_df.columns or "importance" not in feature_importance_df.columns:
        return []
    top_df = feature_importance_df.sort_values("importance", ascending=False).head(top_n)
    return [
        f"{row['feature']} (importance={row['importance']:.6f})"
        for _, row in top_df.iterrows()
    ]


def sanitize_filename(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in {"-", "_", "."} else "_" for ch in str(value))


def choose_recommended_actions(risk_level: str):
    if risk_level == "High":
        return [
            "Do not trust or execute this file in a normal environment.",
            "Quarantine the sample immediately.",
            "Preserve the report and prediction results for review.",
            "Escalate to the team for deeper investigation.",
        ]
    if risk_level == "Medium":
        return [
            "Keep the file isolated pending deeper analysis.",
            "Review the top indicators and model explanation.",
            "Do not trust the sample until additional review is complete.",
        ]
    return [
        "No strong ransomware verdict was assigned.",
        "Keep the report for reference and review if needed.",
    ]


def choose_why_flagged(probability: float, top_indicator_names, model_name: str, feature_strategy: str):
    indicator_text = ", ".join(top_indicator_names[:3]) if top_indicator_names else "no indicators provided"

    if probability >= 0.70:
        return [
            f"The {model_name} model classified this sample as ransomware-like.",
            f"The feature strategy used was: {feature_strategy}.",
            f"Top indicators included {indicator_text}.",
        ]
    if probability >= 0.40:
        return [
            f"The {model_name} model found suspicious ransomware-like patterns.",
            f"The feature strategy used was: {feature_strategy}.",
            f"Important indicators included {indicator_text}.",
        ]
    return [
        f"The {model_name} model did not assign a strong ransomware likelihood.",
        f"The feature strategy used was: {feature_strategy}.",
        f"The most influential indicators included {indicator_text}.",
    ]


def choose_observed_text(model_name: str, feature_strategy: str, risk_level: str):
    observations = [
        f"This report is based on the {model_name} machine learning pipeline.",
        f"The feature strategy used was: {feature_strategy}.",
    ]

    if risk_level == "High":
        observations.append("The model found a strong ransomware-like structural pattern.")
    elif risk_level == "Medium":
        observations.append("The model found suspicious structural indicators that merit review.")
    else:
        observations.append("The model did not find a strong ransomware-like structural pattern.")

    return observations


def build_replacements(
    sample_row: pd.Series,
    top_features,
    analysis_date: str,
    override_model_name: str = None,
    override_feature_strategy: str = None,
):
    if "ransomware_probability" in sample_row.index and pd.notna(sample_row["ransomware_probability"]):
        probability = float(sample_row["ransomware_probability"])
    else:
        predicted_rg = int(float(sample_row.get("predicted_RG", 0)))
        probability = 0.90 if predicted_rg == 1 else 0.10

    risk_level = safe_get(sample_row, "risk_level", "Low")
    ml_prediction = probability_to_prediction(probability)
    overall_verdict = probability_to_verdict(probability)
    confidence_text = risk_to_confidence_text(probability)

    model_name = override_model_name or safe_get(sample_row, "model_name", "Unknown_Model")
    feature_strategy = override_feature_strategy or safe_get(sample_row, "feature_strategy", "Not provided")

    top_indicator_names = [x.split(" (importance=")[0] for x in top_features]

    static_assessment = (
        "The model relied on structural indicators associated with ransomware-like samples."
        if probability >= 0.70
        else "The model identified some suspicious indicators but not a strong ransomware pattern."
        if probability >= 0.40
        else "The model did not identify a strong ransomware-like static pattern."
    )

    combined_conclusion = (
        "The available static evidence supports a ransomware-likely verdict."
        if probability >= 0.70
        else "The available static evidence supports a suspicious classification that needs further review."
        if probability >= 0.40
        else "The available static evidence does not currently support a high-risk ransomware verdict."
    )

    final_statement = (
        f"{safe_get(sample_row, 'filename')} was classified as {ml_prediction.lower()} "
        f"with {confidence_text.lower()} confidence and {risk_level.lower()} risk."
    )

    short_conclusion = f"{model_name} classified this sample using {feature_strategy}."

    replacements = {
        "ID": safe_get(sample_row, "ID", "N/A"),
        "filename": safe_get(sample_row, "filename", "N/A"),
        "analysis_date": analysis_date,
        "model_name": model_name,
        "feature_strategy": feature_strategy,
        "overall_verdict": overall_verdict,
        "ml_prediction": ml_prediction,
        "ml_confidence": f"{probability:.4f}",
        "risk_level": risk_level,
        "short_conclusion": short_conclusion,
        "top_indicators_bullets": format_bullets(top_indicator_names),
        "top_features_numbered": format_numbered(top_features),
        "static_assessment": static_assessment,
        "combined_conclusion": combined_conclusion,
        "recommended_actions_bullets": format_bullets(choose_recommended_actions(risk_level)),
        "confidence_text": confidence_text,
        "final_statement": final_statement,
        "why_flagged_bullets": format_bullets(
            choose_why_flagged(probability, top_indicator_names, model_name, feature_strategy)
        ),
        "what_was_observed_bullets": format_bullets(
            choose_observed_text(model_name, feature_strategy, risk_level)
        ),
    }

    return replacements


def render_template(template_text: str, replacements: dict) -> str:
    rendered = template_text
    for key, value in replacements.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", str(value))
    return rendered


def main():
    parser = argparse.ArgumentParser(description="Generate markdown reports from model-specific prediction outputs.")
    parser.add_argument("--input", required=True, help="Prediction report CSV")
    parser.add_argument("--feature-importance", required=True, help="Feature importance CSV")
    parser.add_argument("--sample-id", default=None, help="Optional sample ID to generate only one report")
    parser.add_argument("--top-n", type=int, default=5, help="Number of top features to include")
    parser.add_argument("--model-name", default=None, help="Optional override for model name in the report")
    parser.add_argument("--feature-strategy", default=None, help="Optional override for feature strategy in the report")
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = pd.read_csv(args.input)
    fi_df = pd.read_csv(args.feature_importance)

    if args.sample_id is not None:
        df = df[df["ID"].astype(str) == str(args.sample_id)]
        if df.empty:
            raise ValueError(f"No sample found with ID={args.sample_id}")

    tech_template = load_text(TECH_TEMPLATE_PATH)
    user_template = load_text(USER_TEMPLATE_PATH)
    top_features = get_top_features(fi_df, top_n=args.top_n)
    analysis_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for _, row in df.iterrows():
        replacements = build_replacements(
            sample_row=row,
            top_features=top_features,
            analysis_date=analysis_date,
            override_model_name=args.model_name,
            override_feature_strategy=args.feature_strategy,
        )

        tech_text = render_template(tech_template, replacements)
        user_text = render_template(user_template, replacements)

        sample_id = replacements["ID"]
        filename = sanitize_filename(replacements["filename"])
        model_label = sanitize_filename(replacements["model_name"])

        tech_path = os.path.join(OUTPUT_DIR, f"{model_label}_technical_report_{sample_id}_{filename}.md")
        user_path = os.path.join(OUTPUT_DIR, f"{model_label}_user_report_{sample_id}_{filename}.md")

        save_text(tech_path, tech_text)
        save_text(user_path, user_text)

        print(f"Generated: {tech_path}")
        print(f"Generated: {user_path}")


if __name__ == "__main__":
    main()
