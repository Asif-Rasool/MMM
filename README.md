# Signals and Sales: Modeling Incremental Revenue Impact of Marketing Channels (Prototype Version)

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#license)

**Developer:** Asif Rasool, Ph.D.
Business Research Center, College of Business
Southeastern Louisiana University
📧 [asif.rasool@southeastern.edu](mailto:asif.rasool@southeastern.edu)

---

## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Repository Structure](#repository-structure)
* [Installation](#installation)
* [Configuration](#configuration)
* [Running the App](#running-the-app)
* [Page Descriptions](#page-descriptions)
* [Folder Guide](#folder-guide)
* [License](#license)

---

## Overview

This repository hosts a prototype Streamlit web application designed to model and recommend optimal marketing strategies for small- to medium-sized businesses in Louisiana's Northshore region. It simulates campaign data, builds both linear and machine-learning models, and delivers an AI-driven recommendation engine.

## Features

* **Synthetic Data**: Simulated monthly records of marketing spend and sales outcomes.
* **Exploratory Data Analysis (EDA)**: Interactive distribution plots, crosstabs, and correlation heatmaps.
* **Modeling Suite**:

  * **Linear Regression** (pooled + segment-specific)
  * **Random Forest Regression** (pooled + segment-specific)
* **Evaluation & Selection**: Compare RMSE, R², CV metrics across ten model variants.
* **Recommendation System**:

  * Per‑dollar ROI dashboards for each client segment
  * Custom campaign budget allocator and ROI calculator
  * AI-driven insights via Vertex AI (Gemini) & LangChain chat interface
* **Deployment Ready**: Configured for local, Colab, and Google Cloud Run environments.

## Repository Structure

```
.
├── .streamlit/                          # Streamlit configuration
│   ├── config.toml                     # Theme, layout, favicon settings
│   └── secrets.toml                    # Secure Vertex AI credentials
├── Data/                                # Synthetic and raw datasets
│   └── Campaign-Data.csv
├── Figures/                             # Static images used in app pages
├── Outputs/                             # Model summaries, metrics, importances, marginals
├── pages/                               # Multipage Streamlit scripts
│   ├── 0_Background.py
│   ├── 1_Data.py
│   ├── 2_Exploratory_Data_Analysis_(EDA).py
│   ├── 3_Modeling_Strategy.py
│   ├── 4_Linear_Regressions.py
│   ├── 5_Random_Forest.py
│   ├── 6_Model_Evaluation_and_Selection.py
│   └── 7_Recommendation.py
├── main.ipynb                           # End‑to‑end analysis notebook
├── environment.yaml                     # Conda environment spec
├── requirements.txt                     # Python package dependencies
├── LICENSE                              # MIT License
└── README.md                            # Project overview and instructions
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Asif-Rasool/MMM.git
cd MMM
```

### 2. Set up the Python environment

**Option A: Using Conda**

```bash
conda env create -f environment.yaml
conda activate mmm-env
```

**Option B: Using pip**

```bash
pip install -r requirements.txt
```

## Configuration

1. **Streamlit Theme & Layout**

   * Edit `.streamlit/config.toml` for colors, fonts, and favicon.
2. **Vertex AI (Gemini) Access**

   * Populate `.streamlit/secrets.toml` with your GCP project and credentials:

   ```toml
   [google]
   project_id = "YOUR_PROJECT_ID"
   credentials = '''{ /* JSON credentials */ }'''
   ```
3. **Data Path**

   * Ensure `Data/Campaign-Data.csv` exists or update the path in `pages/1_Data.py`.

## Running the App

Launch the Streamlit multipage interface:

```bash
streamlit run pages/0_Background.py
```

Use the left sidebar to navigate between pages.

## Page Descriptions

* **0. Background**
  Introduction, objectives, and context for the Northshore marketing uplift analysis.

* **1. Data**
  Overview of the synthetic dataset, variable descriptions, sample snapshot, and CSV download.

* **2. Exploratory Data Analysis (EDA)**
  Distribution plots, competition vs. sales analysis, and correlation heatmaps (pooled + segment).

* **3. Modeling Strategy**
  High‑level description of the modeling pipeline: OLS baseline and Random Forest enhancements.

* **4. Linear Regression**
  Implementation and interpretation of pooled and segment‑specific OLS models with tables and bar charts.

* **5. Random Forest**
  Training and analysis of pooled and segment‑specific Random Forests; feature importances and marginal effects.

* **6. Model Evaluation and Selection**
  Comparison of ten model variants on key metrics and the rationale for selecting the final model.

* **7. Recommendation System**
  Per‑dollar ROI dashboards, custom campaign ROI calculator, and an AI chat interface for strategic insights.

## Folder Guide

* **Data/**: Raw and synthetic campaign data used by the app.
* **Figures/**: Static visual assets referenced across the pages.
* **Outputs/**: Intermediate model output files (CSV, JSON) ingested by the app.

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

*Feel free to open issues or submit pull requests. For questions, contact Asif Rasool at [asif.rasool@southeastern.edu](mailto:asif.rasool@southeastern.edu).*
