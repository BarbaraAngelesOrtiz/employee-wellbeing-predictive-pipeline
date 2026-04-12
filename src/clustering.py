# Mental Health Hackathon - Clustering
# Author: Barbara Ortiz
# Purpose:
#   - Profile identification via K-Means & Agglomerative Clustering
#   - Hyperparameter optimization (Silhouette Analysis)
#   - Dimensionality reduction and profile visualization

import pandas as pd
import numpy as np
import os
import logging
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

#  CONFIGURATION 
os.environ["OMP_NUM_THREADS"] = "1"
warnings.filterwarnings("ignore", category=RuntimeWarning)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)

INPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "mental_health_features.csv")
CLUSTER_OUTPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "clusters.csv")
SUMMARY_OUTPUT_PATH = os.path.join(BASE_DIR, "data", "analysis", "cluster_summary.csv")
IMAGE_DIR = os.path.join(BASE_DIR, "images")

# DATA LOADING & FEATURE SELECTION  
df = pd.read_csv(INPUT_PATH)
logging.info(f"Loaded Gold Dataset: {df.shape}")

features = df.select_dtypes(include=[np.number]).columns.tolist()
logging.info(f"Clustering features: {features}")

X = df[features].copy()
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# OPTIMAL K SELECTION (SCIENTIFIC VALIDATION) 
silhouette_scores = {}
for k in range(2, 6): 
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=20)
    labels = kmeans.fit_predict(X_scaled)
    silhouette_scores[k] = silhouette_score(X_scaled, labels)

best_k = max(silhouette_scores, key=silhouette_scores.get)
logging.info(f"Optimal K identified: {best_k} (Silhouette: {silhouette_scores[best_k]:.4f})")

#  MODEL COMPARISON 
# KMeans
km_labels = KMeans(n_clusters=best_k, random_state=42, n_init=20).fit_predict(X_scaled)
sil_km = silhouette_score(X_scaled, km_labels)

# Agglomerative
agg_labels = AgglomerativeClustering(n_clusters=best_k).fit_predict(X_scaled)
sil_agg = silhouette_score(X_scaled, agg_labels)

# Select best performing model
if sil_km >= sil_agg:
    selected_labels = km_labels
    selected_name = "KMeans"
    logging.info(f"Selected Model: KMeans (Sil: {sil_km:.4f})")
else:
    selected_labels = agg_labels
    selected_name = "Agglomerative"
    logging.info(f"Selected Model: Agglomerative (Sil: {sil_agg:.4f})")

df["cluster"] = selected_labels

# CLUSTER PROFILING & INTERPRETATION

cluster_summary = df.groupby("cluster")[features].mean()

def assign_person(row):
    if row['support_index'] > 0.6 and row['stigma_index'] < 0.4:
        return "Protected Advocates"
    elif row['stigma_index'] > 0.5:
        return "Silent Risk Group"
    else:
        return "Unsupported Neutral"

df['person'] = cluster_summary.apply(assign_person, axis=1).reindex(df['cluster']).values
df.to_csv(CLUSTER_OUTPUT_PATH, index=False)
cluster_summary.to_csv(SUMMARY_OUTPUT_PATH)

# 5. VISUALIZATIONS 

# PCA Projection
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
plt.figure(figsize=(10, 7))
sns.scatterplot(x=X_pca[:,0], y=X_pca[:,1], hue=df["person"], palette="viridis", alpha=0.7)
plt.title("Employee Segmentation - PCA Projection", fontsize=14)
plt.savefig(os.path.join(IMAGE_DIR, "Cluster_PCA.png"), bbox_inches="tight")

# Standardized Heatmap
cluster_z = (cluster_summary - df[features].mean()) / df[features].std()
plt.figure(figsize=(12, 6))
sns.heatmap(cluster_z, annot=True, cmap="RdBu_r", center=0)
plt.title("Person Fingerprints (Z-Scores vs Global Mean)")
plt.savefig(os.path.join(IMAGE_DIR, "Cluster_Heatmap_Z.png"), bbox_inches="tight")

# Radar Plots (Consolidated)
from math import pi
def make_radar(row, title, color):
    categories = list(cluster_summary.columns)
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    
    ax = plt.subplot(1, best_k, row.name + 1, polar=True)
    values = row.values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, color=color, linewidth=2)
    ax.fill(angles, values, color=color, alpha=0.1)
    plt.xticks(angles[:-1], categories, size=7)
    plt.title(title, size=11, color=color, y=1.1)

plt.figure(figsize=(16, 5))
colors = sns.color_palette("Set2", best_k)
for i, (idx, row) in enumerate(cluster_summary.iterrows()):
    make_radar(row, f"Cluster {idx}", colors[i])
plt.tight_layout()
plt.savefig(os.path.join(IMAGE_DIR, "Cluster_Radar_Consolidated.png"))

logging.info("Pipeline completed successfully.")