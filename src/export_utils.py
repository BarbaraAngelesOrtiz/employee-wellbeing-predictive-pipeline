# Mental Health - GenAI Handover Pipeline
# Author: Barbara Ortiz
# Purpose:
#   - Automate the extraction of machine learning artifacts and statistical metadata.
#   - Bridge the gap between predictive backend logic and Generative AI (GenAI) creative layers.
#   - Standardize persona-based profiles to facilitate automated prompt engineering.
#   - Export model coefficients as business-logic weights for personalized HR interventions.

import pandas as pd
import json
import joblib
import os

# CONFIG
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "data", "models", "best_model.pkl")
SUMMARY_PATH = os.path.join(BASE_DIR, "data", "analysis", "cluster_summary.csv")
EXPORT_DIR = os.path.join(BASE_DIR, "data", "for_genai")

os.makedirs(EXPORT_DIR, exist_ok=True)

def export_handover_kit():
    # 1. Load the winning model
    model = joblib.load(MODEL_PATH)
    
    # 2. Export Feature Importance (Coefficients for GenAI Context)
    feature_names = model.feature_names_in_
    coefficients = model.coef_[0]
    
    importance_dict = {
        name: round(float(coef), 4) 
        for name, coef in zip(feature_names, coefficients)
    }
    
    with open(os.path.join(EXPORT_DIR, "feature_importance.json"), "w") as f:
        json.dump(importance_dict, f, indent=4)

    # 3. Export Persona Descriptions (The "Prompt Base")
    persona_descriptions = {
        "Protected Advocates": {
            "traits": "High supervisor trust, high benefit awareness, low perceived stigma.",
            "visual_keywords": "Open communication, supportive environment, bright, collaborative.",
            "risk_level": "Low"
        },
        "Silent Risk Group": {
            "traits": "High stigma index, high fear of consequences, history of mental health disorders but low disclosure.",
            "visual_keywords": "Hidden barriers, isolation, corporate pressure, transitioning to support.",
            "risk_level": "Critical"
        }
    }
    
    with open(os.path.join(EXPORT_DIR, "persona_profiles.json"), "w") as f:
        json.dump(persona_descriptions, f, indent=4)

    print(f"✅ Handover kit exported to: {EXPORT_DIR}")

if __name__ == "__main__":
    export_handover_kit()