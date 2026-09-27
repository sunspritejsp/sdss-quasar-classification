# SDSS Quasar Classifier

[![Status: WIP](https://img.shields.io/badge/Status-In%20Development-yellow.svg)](#-project-status--roadmap)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)

A machine learning project designed to classify astronomical objects (**Quasars** vs. **Stars**) using real photometric observations from the **Sloan Digital Sky Survey (SDSS DR16)**.

---

## Context

Differentiating common stars from quasars (distant, supermassive active galactic nuclei) is a foundational challenge in observational astrophysics. Due to the cosmological expansion of the universe, light emitted by quasars undergoes redshift ($z$), shifting key emission lines and spectral continuum slopes across photometric passbands. 

This pipeline uses classification algorithms to learn these distinct spectral distributions across the SDSS 5-band photometric filter system:
* **`u`**: Ultraviolet
* **`g`**: Green
* **`r`**: Red
* **`i`**: Near-Infrared
* **`z`**: Far-Infrared

### Feature Engineering
To capture spectral slopes independently of total apparent brightness or distance, the pipeline computes adjacent **astronomical color indices**:
$$\Delta \text{color} \in \{ (u - g), (g - r), (r - i), (i - z) \}$$
These color differentials help separate quasar redshift tracks from the stellar locus in multi-dimensional color space.

---

## Project Structure

```text
sdss-quasar-classification/
├── data/
│   ├── raw/                    # Raw extracted SDSS DR16 data (sdss_raw.csv)
│   └── processed/              # Cleaned datasets and engineered feature matrices
├── notebooks/
│   ├── 01_exploratory_audit.ipynb      # Initial exploratory inspection
│   └── 02_feature_engineering.ipynb    # Feature prototyping & validation
├── src/
│   ├── data/
│   │   ├── download_data.py    # Astroquery SDSS DR16 SQL extractor
│   │   └── clean_data.py       # Data validation & outlier filtering
│   └── features/
│       └── build_features.py   # CLI pipeline for color indices & target encoding
├── environment.yml             # Conda environment configuration
├── requirements.txt            # Pip dependencies specification
└── README.md
```

---

## Project Status & Roadmap

- [x] **Data Ingestion & Extraction** (SDSS DR16 balanced SQL query: 50,000 stars & 50,000 QSOs with `clean = 1` and `zWarning = 0`)
- [x] **Data Cleaning** (Filtered sentinel `-9999` values, faint magnitudes $> 30$, and inconsistent QSO redshifts)
- [x] **Feature Engineering** (Computed adjacent color indices and binary target encoding; metadata is strictly excluded to prevent data leakage)
- [ ] **Exploratory Data Analysis (EDA)** (Color-color diagrams and distribution comparisons)
- [ ] **Modeling** (Baseline classifiers, Decision Trees / Random Forests, Gradient Boosting)
- [ ] **Evaluation & Diagnostics** (ROC-AUC, Precision-Recall, Confusion Matrices, and error analysis)
- [ ] **Documentation & Polishing**

---

## Getting Started

### 1. Environment Setup

Clone the repository and set up the environment using either **Conda** or **pip**:

**Using Conda (Recommended):**
```bash
git clone git@github.com:sunspritejsp/sdss-quasar-classification.git
cd sdss-quasar-classification
conda env create -f environment.yml
conda activate sdss-classifier
```

**Using Pip:**
```bash
git clone git@github.com:sunspritejsp/sdss-quasar-classification.git
cd sdss-quasar-classification
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Running the Data Pipeline

The pipeline scripts can be run sequentially from the project root:

```bash
# 1. (Optional) Query SDSS DR16 via Astroquery to fetch raw data
python src/data/download_data.py

# 2. Clean data and apply quality filters (outputs to data/processed/sdss_clean.csv)
python src/data/clean_data.py

# 3. Build color features and encode targets (outputs to data/processed/sdss_features.csv)
python src/features/build_features.py --input data/processed/sdss_clean.csv --output data/processed/sdss_features.csv
```

---

## Technologies Used

* **Language:** Python 3.10+
* **Package Management:** Conda / pip
* **Astronomical Querying:** Astroquery, Astropy, SDSS DR16 CasJobs
* **Data Processing:** Pandas, NumPy
* **Visualization:** Matplotlib, Seaborn
* **Machine Learning & Metrics:** Scikit-Learn
* **Interactive Prototyping:** JupyterLab, IPykernel
