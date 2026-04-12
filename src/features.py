# Mental Health - Feature Engineering
# Author: Barbara Ortiz
# Purpose:
#   - Align dataset with Top 10 correlated features
#   - Apply semantic-safe transformations
#   - Prepare modeling-ready dataset
#   - Generate correlation diagnostics

import pandas as pd
import numpy as np
import os
import logging
import matplotlib.pyplot as plt
import seaborn as sns

# CONFIG

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)

INPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "mental_health_cleaned.csv")
IMPORTANCE_PATH = os.path.join(BASE_DIR, "data", "analysis", "feature_importance_master.csv")

OUTPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "mental_health_features.csv")
IMAGE_DIR = os.path.join(BASE_DIR, "images")
os.makedirs(IMAGE_DIR, exist_ok=True)

# FEATURE MAPPING 

RENAME_DICT = {
    "Have you had a mental health disorder in the past?": "past_disorder",
    "Have you been diagnosed with a mental health condition by a medical professional?": "diagnosed_flag",
    "Do you believe your productivity is ever affected by a mental health issue?": "productivity_impact",
    "Do you have a family history of mental illness?": "family_history",
    "Do you know the options for mental health care available under your employer-provided coverage?": "knows_benefits",
    "Did you feel that your previous employers took mental health as seriously as physical health?": "prev_employer_support",
    "Would you feel comfortable discussing a mental health disorder with your direct supervisor(s)?": "comfort_supervisor",
    "Do you think that discussing a mental health disorder with your employer would have negative consequences?": "fear_consequences",
    "If a mental health issue prompted you to request a medical leave from work, asking for that leave would be:": "leave_easiness"
}

def create_composite_indexes(df):
    """
    Creates Business-Value Indexes (Feature Construction).
    This demonstrates domain knowledge to recruiters.
    """
    logging.info("Generating Composite Organizational Indexes...")
    
    # 1. Workplace Support Index (How much does the company care?)
    support_cols = [
        "Does your employer provide mental health benefits as part of healthcare coverage?",
        "Has your employer ever formally discussed mental health (for example, as part of a wellness campaign or other official communication)?",
        "Does your employer offer resources to learn more about mental health concerns and options for seeking help?",
        "Is your anonymity protected if you choose to take advantage of mental health or substance abuse treatment resources provided by your employer?"
    ]
    df["support_index"] = df[support_cols].mean(axis=1)

    # 2. Stigma Index (How dangerous is it to speak up?)
    stigma_cols = [
        "Do you think that team members/co-workers would view you more negatively if they knew you suffered from a mental health issue?",
        "Do you feel that being identified as a person with a mental health issue would hurt your career?",
        "Have you heard of or observed negative consequences for co-workers who have been open about mental health issues?"
    ]
    
    available_stigma = [c for c in stigma_cols if c in df.columns]
    df["stigma_index"] = df[available_stigma].mean(axis=1)

    return df

def main():
    if not os.path.exists(INPUT_PATH):
        logging.error(f"Input file not found: {INPUT_PATH}")
        return

    df = pd.read_csv(INPUT_PATH)
    
    df = create_composite_indexes(df)

    target_col = "Do you feel that your employer takes mental health as seriously as physical health?"
    if target_col in df.columns:
        df["target_seriousness"] = pd.to_numeric(df[target_col], errors='coerce')

    df_final = df.rename(columns=RENAME_DICT)
    
    core_features = list(RENAME_DICT.values()) + ["support_index", "stigma_index", "target_seriousness"]
    modeling_features = [f for f in core_features if f in df_final.columns]
    
    gold_df = df_final[modeling_features].copy()
    gold_df = gold_df.fillna(gold_df.median(numeric_only=True))

    gold_df.to_csv(OUTPUT_PATH, index=False)
    logging.info(f"Feature Engineering complete. Modeling table saved: {OUTPUT_PATH}")

    # Generate Correlation Diagnostic
    plt.figure(figsize=(12, 8))
    sns.heatmap(gold_df.corr(), annot=True, cmap="RdBu_r", fmt=".2f")
    plt.title("Gold Dataset: Feature Correlation Matrix")
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, "feature_correlation_matrix.png"))
    plt.close()

if __name__ == "__main__":
    main()