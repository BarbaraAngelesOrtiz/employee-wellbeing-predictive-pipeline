# Mental Health - Target & Feature Analysis
# Author: Barbara Ortiz
# Purpose:
#   - Analyze multiple targets
#   - Rank them statistically
#   - Detect redundancy / overlap
#   - Understand predictive structure
#   - Prepare features for clustering

import pandas as pd
import numpy as np
import os
import seaborn as sns
import textwrap
import warnings
import matplotlib.pyplot as plt
from sklearn.feature_selection import mutual_info_classif
from sklearn.preprocessing import LabelEncoder

warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# CONFIG
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)

OUTPUT_DIR = os.path.join(BASE_DIR, "data", "analysis")
IMAGE_DIR = os.path.join(BASE_DIR, "images")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

INPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "mental_health_cleaned.csv")
MISSING_SUMMARY_PATH = os.path.join(BASE_DIR, "data", "analysis", "missing_summary.csv")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

# LOAD DATA 
df = pd.read_csv(INPUT_PATH)

print("=" * 80)
print("DATASET OVERVIEW")
print("=" * 80)
print(f"Shape: {df.shape}")
print(f"Overall missing ratio: {round(df.isna().mean().mean(), 4)}")

# MISSING VALUES SUMMARY

UNKNOWN_VALUES = [-1, -2]

missing_summary = pd.DataFrame({
    "column": df.columns,
    "missing_ratio": df.isna().mean() + df.isin(UNKNOWN_VALUES).mean(),
    "missing_count": df.isna().sum() + df.isin(UNKNOWN_VALUES).sum(),
    "dtype": df.dtypes.values

}).sort_values("missing_ratio", ascending=False)

missing_summary.to_csv(MISSING_SUMMARY_PATH, index=False)
print("\nTop 15 columns by missing ratio:")
print(missing_summary.head(15))

# TARGET CANDIDATES 
CANDIDATE_TARGETS = [
    "Would you feel comfortable discussing a mental health disorder with your direct supervisor(s)?",
    "Would you feel comfortable discussing a mental health disorder with your coworkers?",
    "Do you think that discussing a mental health disorder with your employer would have negative consequences?",
    "Do you feel that your employer takes mental health as seriously as physical health?",
    "Has your employer ever formally discussed mental health (for example, as part of a wellness campaign or other official communication)?"
]

# TARGET STATISTICAL RANKING 
def evaluate_target_quality(df, target):
    series = df[target]
    dist_ratio = series.value_counts(dropna=False, normalize=True)
    max_class_ratio = dist_ratio.max()
    
    return {
        "target": target,
        "missing_ratio": round(series.isna().mean(), 3),
        "balance_score": round(1 - max_class_ratio, 3), # Higher is better balanced
        "rows_available": series.notna().sum()
    }

target_eval = pd.DataFrame([evaluate_target_quality(df, t) for t in CANDIDATE_TARGETS])
target_eval = target_eval.sort_values(by="balance_score", ascending=False)

target_eval.to_csv(os.path.join(OUTPUT_DIR, "target_ranking.csv"), index=False)

print("\n" + "=" * 80)
print("TARGET EVALUATION RANKING")
print("=" * 80)
print(target_eval)

# FEATURE ENCODING 
df_encoded = df.copy()
for col in df_encoded.columns:
    if df_encoded[col].dtype == "object":
        le = LabelEncoder()
        df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))

# CONSOLIDATED FEATURE IMPORTANCE PIPELINE 
importance_records = []

for target in CANDIDATE_TARGETS:
    if target not in df_encoded.columns:
        continue
    
    print(f"\nAnalyzing Importance for Target: {target[:50]}...")

    df_target_subset = df_encoded.dropna(subset=[target]).copy()
    
    X = df_target_subset.drop(columns=CANDIDATE_TARGETS, errors='ignore')
    X = X.select_dtypes(include=[np.number]) 
    y = df_target_subset[target].astype(int)
    
    column_medians = X.median(numeric_only=True)
    X = X.fillna(column_medians)
    
    X = X.dropna(axis=1, how='any')
    
    if X.empty:
        print(f"Skipping {target}: No valid features remaining.")
        continue
    
    # Calculate Statistical Scores
    pearson_corr = X.corrwith(y).abs()
    mi_scores = mutual_info_classif(X, y, random_state=42)
    
    # Collect results
    for i, feature_name in enumerate(X.columns):
        importance_records.append({
            "target_variable": target,
            "feature_name": feature_name,
            "pearson_abs_corr": round(pearson_corr[feature_name], 4),
            "mutual_info_score": round(mi_scores[i], 4)
        })

master_importance_df = pd.DataFrame(importance_records)
master_importance_df.to_csv(os.path.join(OUTPUT_DIR, "feature_importance_master.csv"), index=False)

# COLLINEARITY CHECK 
best_target = target_eval.iloc[0]["target"]
print("\n" + "=" * 80)
print(f"COLLINEARITY CHECK FOR BEST TARGET: {best_target}")
print("=" * 80)

# Get top 10 features by Pearson for the best target
top_feature_names = master_importance_df[master_importance_df["target_variable"] == best_target]\
                    .nlargest(10, "pearson_abs_corr")["feature_name"].tolist()

corr_matrix_top = df_encoded[top_feature_names].corr().abs()
high_corr_pairs = []

for i in range(len(corr_matrix_top.columns)):
    for j in range(i + 1, len(corr_matrix_top.columns)):
        if corr_matrix_top.iloc[i, j] > 0.8:
            high_corr_pairs.append((
                corr_matrix_top.columns[i],
                corr_matrix_top.columns[j],
                round(corr_matrix_top.iloc[i, j], 3)
            ))

if high_corr_pairs:
    print("\n⚠️ High Collinearity Detected (Potential Redundancy):")
    for pair in high_corr_pairs: print(pair)
else:
    print("✅ No severe collinearity detected.")

# VISUALIZATIONS 

# Top Predictors Barplot
top_features_data = master_importance_df[master_importance_df["target_variable"] == best_target]\
                    .nlargest(10, "mutual_info_score")

if not top_features_data.empty:
    plt.figure(figsize=(12, 7))
    
    sns.barplot(data=top_features_data, x="mutual_info_score", y="feature_name", palette="viridis")
    
    wrapped_title = "\n".join(textwrap.wrap(f"Top 10 Predictors for: {best_target}", width=60))
    
    plt.title(wrapped_title, fontsize=14, pad=20)
    plt.xlabel("Mutual Information Score (Importance)", fontsize=12)
    plt.ylabel("Feature Name", fontsize=12)
    plt.tight_layout()
    
    plt.savefig(os.path.join(IMAGE_DIR, "top_feature_importance.png"), dpi=300, bbox_inches="tight")
    plt.close()

# Target Distributions
fig, axes = plt.subplots(nrows=len(CANDIDATE_TARGETS), ncols=1, figsize=(10, 4 * len(CANDIDATE_TARGETS)))
if len(CANDIDATE_TARGETS) == 1: axes = [axes]

for ax, target in zip(axes, CANDIDATE_TARGETS):
    df[target].value_counts(dropna=False).plot(kind="bar", ax=ax, color='skyblue')
    ax.set_title(f"Distribution: {target[:80]}...")
    ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig(os.path.join(IMAGE_DIR, "candidate_target_distributions.png"))
plt.close()

# SAVE ENRICHED DATASET 
df.to_csv(os.path.join(PROCESSED_DIR, "mental_health_enriched.csv"), index=False)

print("\n" + "=" * 80)
print("PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 80)