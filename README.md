# 🧠 Employee Wellbeing & Mental Health Analytics

### *A Predictive and Generative Data Product Pipeline*

## 📌 Project Overview

This project delivers an end-to-end analytical framework designed to quantify and predict psychological safety and mental health trends within corporate environments. Unlike traditional descriptive reports, this system functions as a **Data Product**, transitioning from raw survey data to a predictive engine that feeds a **Generative AI** creative layer for personalized HR interventions.

## 🏗️ Technical Architecture

The project follows a **Medallion Data Architecture** to ensure scalability and reproducibility:

  * **Silver Layer:** Standardized cleaning and normalization of raw survey entries.
  * **Gold Layer:** High-value features, including composite indices and technical slugs.
  * **Analysis Layer:** Statistical artifacts, model benchmarks, and GenAI-ready metadata.

-----

## 🚀 Key Features & Methodology

### 1\. Statistical Target Ranking

Before modeling, we performed a **Quality Benchmark** on multiple candidate targets. Using **Mutual Information (MI)** and balance scores, we identified `comfort_supervisor` as the most reliable indicator of workplace trust.

### 2\. Advanced Feature Engineering (Composite Indices)

We moved beyond individual survey questions by constructing latent organizational constructs:

  * **Support Index:** Quantifies benefits awareness and organizational resources.
  * **Stigma Index:** Measures the "Silence Cost" and perceived career risk of disclosure.

### 3\. Archetypal Discovery (Unsupervised Learning)

Using **K-Means (Optimized via Silhouette Analysis)**, we identified two critical personas:

  * **Protected Advocates:** High trust, high awareness, low perceived stigma.
  * **Silent Risk Group:** 93.3% history of disorders but lowest disclosure rates due to high perceived stigma.

### 4\. Supervised Benchmarking (Logistic Regression vs. Random Forest)

We implemented a competitive modeling pipeline. **Logistic Regression** emerged as the winner with **80.14% Accuracy**, demonstrating a strong linear relationship between structural workplace drivers and individual comfort.

### 5\. GenAI-Ready Handover Pipeline

The backend culminates in an automated export of **JSON artifacts**. This kit bridges the gap between predictive logic and Generative AI, providing semantic prompts and predictive weights for automated communication campaigns.

-----

## 📊 Performance Metrics

| Metric | Logistic Regression (Winner) | Random Forest |
| :--- | :--- | :--- |
| **Accuracy** | **80.14%** | 78.75% |
| **F1-Score (Weighted)** | **0.79** | 0.77 |
| **Primary Drivers** | Stigma Index, Support Index | Stigma Index, Leave Easiness |

-----

## 📁 Repository Structure

```bash
├── data/
│   ├── raw/               # Original survey data
│   ├── processed/         # Silver (Cleaned) & Gold (Features) layers
│   ├── analysis/          # Statistical reports
│   ├── models/            # Model artifacts (.pkl)
│   └── for_genai/         # JSON metadata for Generative AI integration
├── images/                # Benchmarking plots and persona visualizations
├── src/                   # Modular Python scripts (Cleaning, Clustering, Features, Modeling, Export)
├── requirements. txt      # Libraries
└── notebooks/main.ipynb   # Main orchestration notebook
```

-----

## 🛠 Technical Stack

* Python
* Pandas
* NumPy
* Scikit-learn
* KMeans Clustering
* Logistic Regression
* Random Forest
* Silhouette Analysis

-----

## 🧮 Outputs

The pipeline generates a set of production-ready artifacts used for decision-making and downstream integration:

- **Cleaned Dataset:** A standardized Silver Layer version of the raw survey data.

- **Feature-Engineered Dataset:** The Gold Layer containing composite indices ready for modeling.

- **Cluster Metrics:** Statistical summaries and fingerprints of the identified employee personas.

- **Model Prediction Files:** Probabilistic predictions of employee comfort levels.

- **Serialized Artifacts:** High-performance .pkl models and serialized thresholds for real-time inference.


-----

## 🔄 Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/mental-health-analytics.git
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the Pipeline:**
    Open `main_notebook.ipynb` and execute all cells to reproduce the cleaning, clustering, modeling, and export phases.

-----

## 🏆 Business Impact

  * **Proactive Intervention:** Identifies "Silent Risk" employees before burnout or turnover occurs.
  * **Data-Driven Culture:** Provides HR with quantifiable "Stigma" and "Support" metrics to measure the ROI of wellness initiatives.
  * **Personalization at Scale:** The GenAI bridge allows for the automated generation of tailored support messages based on individual predictive profiles.

-----

## 🎯 Final Reflection

The journey through this project highlights a fundamental shift in HR analytics: moving from clinical symptoms to organizational systems. By prioritizing the "Stigma Index" and "Supervisor Comfort" as primary predictive drivers, the model proves that psychological safety is not an individual trait but an environmental outcome. The integration with Generative AI marks the next frontier for this work—not just predicting risk, but automating the empathy and communication needed to mitigate it. This project stands as a testament to how data science can be both mathematically rigorous and profoundly human-centric.

-----

## Author

**Bárbara Ángeles Ortiz**

<img src="https://github.com/user-attachments/assets/30ea0d40-a7a9-4b19-a835-c474b5cc50fb" width="115">

[LinkedIn](https://www.linkedin.com/in/barbaraangelesortiz/) | [GitHub](https://github.com/BarbaraAngelesOrtiz)

![Status](https://img.shields.io/badge/Status-Completed-success) 
![Reproducible](https://img.shields.io/badge/Reproducible-Yes-brightgreen)

![WAI Ireland](https://img.shields.io/badge/WAI%20Challenge-yellow) 📅 April 2026

![ML Project](https://img.shields.io/badge/Machine%20Learning-Project-purple)
![Feature Engineering](https://img.shields.io/badge/Feature%20Engineering-Advanced-blueviolet)
![Clustering](https://img.shields.io/badge/Clustering-Worker%20Profiling-teal)
![Explainable AI](https://img.shields.io/badge/Explainable-AI-important)
![Data Cleaning](https://img.shields.io/badge/Data%20Cleaning-ETL-lightgrey)

![Python](https://img.shields.io/badge/python-3.10-blue)
![NumPy](https://img.shields.io/badge/numpy-1.26.0-blue)
![Pandas](https://img.shields.io/badge/pandas-2.1.0-blue)

![Matplotlib](https://img.shields.io/badge/matplotlib-3.8.0-blue)
![Seaborn](https://img.shields.io/badge/seaborn-0.13.0-blue)
![Jupyter](https://img.shields.io/badge/jupyter-notebook-orange)

![KMeans](https://img.shields.io/badge/Clustering-KMeans-green)
![Logistic Regression](https://img.shields.io/badge/Model-Logistic%20Regression-success)
![Random Forest](https://img.shields.io/badge/Model-Random%20Forest-success)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3.0-orange)

