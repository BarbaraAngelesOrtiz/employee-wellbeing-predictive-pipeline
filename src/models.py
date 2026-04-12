# Mental Health Analytics - Predictive Modeling Pipeline
# Author: Barbara Ortiz
# Purpose: Supervised Learning to predict employee comfort/risk

import pandas as pd
import numpy as np
import os
import joblib
import logging
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

# CONFIGURATION 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_PATH = globals().get('FEATURE_PATH', os.path.join(BASE_DIR, "data", "processed", "mental_health_features.csv"))

MODEL_PATH = os.path.join(BASE_DIR, "data", "models", "best_model.joblib")
IMAGE_DIR = globals().get('IMAGE_DIR', os.path.join(BASE_DIR, "images"))
os.makedirs(IMAGE_DIR, exist_ok=True)

def run_modeling_pipeline():
   
    if not os.path.exists(INPUT_PATH):
        logging.error(f"Input Gold file not found at: {INPUT_PATH}")
        return
    df = pd.read_csv(INPUT_PATH)
    
    # Target: comfort_supervisor 
    target = "comfort_supervisor"
    if target not in df.columns:
        logging.error(f"Target '{target}' not found in Gold features.")
        return

    X = df.drop(columns=[target, "target_seriousness"], errors='ignore')
    y = df[target].astype(int)

    # TRAIN/TEST SPLIT (80/20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # MODEL BENCHMARKING 
    models = {
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42),
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42)
    }

    results = {}
    reports = {}
    matrices = {}
    
    best_score = 0
    best_model = None
    best_name = ""

    print("\n📊 Benchmarking Models...")
    for name, model in models.items():

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        report_dict = classification_report(y_test, y_pred, output_dict=True)
        cm = confusion_matrix(y_test, y_pred)
        
        results[name] = acc
        reports[name] = report_dict
        matrices[name] = cm
        
        print(f" - {name} Accuracy: {acc:.4f}")

        if acc > best_score:
            best_score = acc
            best_model = model
            best_name = name

    print(f"\n🏆 Winner: {best_name} (Accuracy: {best_score:.4f})")
    
    y_pred_final = best_model.predict(X_test)
    print("\nClassification Report for Winner:")
    print(classification_report(y_test, y_pred_final))

    # BENCHMARKING DASHBOARD
    logging.info("Generating comparison visualizations...")

    # 1: Model Accuracy Score Comparison (Bar Chart)
    plt.figure(figsize=(8, 5))
    sns.barplot(x=list(results.keys()), y=list(results.values()), palette="viridis")
    
    for i, val in enumerate(results.values()):
        plt.text(i, val + 0.01, f'{val:.4f}', ha='center', fontweight='bold', fontsize=11)
        
    plt.title("Model Accuracy Score Comparison", fontsize=14, pad=15)
    plt.ylabel("Accuracy", fontsize=12)
    plt.ylim(0, 1.0) 
    plt.savefig(os.path.join(IMAGE_DIR, "compare_accuracy.png"), bbox_inches="tight")
    plt.show() 

    # 2: F1-Score Comparison per Class (Grouped Bar Chart) 
    
    f1_data = []
    for model_name, report in reports.items():
        f1_data.append({"Model": model_name, "Class": "Comfortable (0)", "F1-Score": report['0']['f1-score']})
        f1_data.append({"Model": model_name, "Class": "At-Risk (1)", "F1-Score": report['1']['f1-score']})
    f1_df = pd.DataFrame(f1_data)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=f1_df, x="Model", y="F1-Score", hue="Class", palette="pastel")
    
    plt.title("F1-Score Comparison per Class (Generalization Power)", fontsize=14, pad=15)
    plt.ylabel("F1-Score", fontsize=12)
    plt.ylim(0, 1.0) 
    plt.legend(title="Class Status", fontsize=10)
    plt.savefig(os.path.join(IMAGE_DIR, "compare_f1_score.png"), bbox_inches="tight")
    plt.show() 

    # 3: Confusion Matrices side-by-side (Heatmaps) 
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Matrix 1: Random Forest
    sns.heatmap(matrices["Random Forest"], annot=True, fmt='d', cmap='Blues', ax=axes[0], cbar=False)
    axes[0].set_title("Confusion Matrix: Random Forest", fontsize=13)
    axes[0].set_xlabel("Predicted Label", fontsize=11)
    axes[0].set_ylabel("Actual Label", fontsize=11)

    # Matrix 2: Logistic Regression 
    sns.heatmap(matrices["Logistic Regression"], annot=True, fmt='d', cmap='Blues', ax=axes[1])
    axes[1].set_title(f"Confusion Matrix: Logistic Regression ({best_name})", fontsize=13)
    axes[1].set_xlabel("Predicted Label", fontsize=11)
    axes[1].set_ylabel("Actual Label", fontsize=11)

    plt.suptitle("Side-by-Side Confusion Matrix Comparison", fontsize=15, y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, "compare_confusion_matrices.png"), bbox_inches="tight")
    plt.show() 

    # 4: Comparison of Top Predictive Drivers (Magnitude) 

    # Attribute Importance of Random Forest (Sum 1.0)
    rf_imp = pd.Series(models["Random Forest"].feature_importances_, index=X.columns)
    
    # Absolute Logistic Regression Coefficients (Magnitude of influence)
    lr_coef = pd.Series(np.abs(models["Logistic Regression"].coef_[0]), index=X.columns)

    drivers_df = pd.DataFrame({
        "Feature": X.columns,
        "Random Forest Importance": rf_imp,
        "Logistic Regression Coefficient (Abs)": lr_coef
    })

    #  Top Drivers 
    top_drivers_features = drivers_df.nlargest(7, "Logistic Regression Coefficient (Abs)")["Feature"].tolist()
    drivers_subset = drivers_df[drivers_df["Feature"].isin(top_drivers_features)].set_index("Feature")
    
    order = ['stigma_index', 'support_index', 'knows_benefits', 'leave_easiness', 
             'comfort_supervisor', 'comfort_coworkers', 'diagnosed_flag']
    drivers_subset = drivers_subset.reindex(order).dropna()

    # Plotting grouped horizontal bar chart
    drivers_subset.plot(kind='barh', color=['#41b6c4', '#225ea8'], width=0.8, figsize=(12, 8))
    
    plt.title("Top 7 Predictive Drivers: Comparison of Influence Magnitude", fontsize=14, pad=20)
    plt.xlabel("Predictive Influence (Normalized RF Importance / Abs LR Coefficient)", fontsize=12)
    plt.ylabel("Key Engineered Feature Names", fontsize=12)
    plt.gca().invert_yaxis() 
    plt.legend(title="Model Metric", fontsize=11)
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.savefig(os.path.join(IMAGE_DIR, "compare_predictive_drivers.png"), dpi=300, bbox_inches="tight")
    plt.show() 

    logging.info(f"Saving best model ({best_name}) to: {MODEL_PATH}")
    joblib.dump(best_model, MODEL_PATH)
    print(f"\n✅ Pipeline completed successfully. Best model saved.")

if __name__ == "__main__":
    run_modeling_pipeline()