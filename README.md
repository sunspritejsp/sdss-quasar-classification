# SDSS Quasar Classifier

[![Status: WIP](https://img.shields.io/badge/Status-In%20Development-yellow.svg)](#-project-status--roadmap)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)

A machine learning project designed to classify astronomical objects Quasars vs Stars using real photometric observations from the Sloan Digital Sky Survey Data Release 16.

---

## Context

In optical sky surveys, quasars (distant Active Galactic Nuclei) and foreground Milky Way stars appear almost identical as unresolved point sources. Classifying them photometrically, without needing expensive spectroscopic follow up, is a big challenge in astronomy.

While both look like points of light, their underlying physics are very distinct:
* **Stars** are thermal emitters within our galaxy. Their spectra are regulated by surface temperature, forming a predictable sequence from hot O/B stars down to cool M dwarfs.
* **Quasars** are supermassive black holes actively accreting matter in distant galaxies. Their spectra are non-thermal, characterized by strong ultraviolet emission and cosmic redshift ($z$) that shifts emission lines across optical wavelengths.

SDSS captures this light across a 5-band filter system:
* **`u`**: Ultraviolet
* **`g`**: Green
* **`r`**: Red
* **`i`**: Near-Infrared
* **`z`**: Far-Infrared

### Feature Engineering: Color Indices
Apparent brightness alone cannot classify an object because distance and luminosity are entangled—a faint reading could mean an object is inherently dim or simply billions of light-years away.

To remove distance dependence and capture spectral shape, the pipeline computes astronomical color indices by taking magnitude differences between adjacent filters:
$$\Delta \text{color} \in \{ (u - g), (g - r), (r - i), (i - z) \}$$

In color space, the populations separate cleanly:
* Stellar Locus: normal stars trace a distinct, tight sequence determined by stellar temperatures.
* Quasar Region: quasars break away from this locus due to their characteristic UV excess and redshifted emission lines, allowing classification models to learn effective decision boundaries.
<p align="center">
  <img src="reports/figures/color_color_u_g_vs_g_r.png" alt="SDSS Color-Color Diagram: u-g vs g-r" width="550"/>
</p>


---

## Project Structure

```text
sdss-quasar-classification/
├── data/
│   ├── raw/                            # Raw extracted SDSS DR16 data (sdss_raw.csv)
│   └── processed/                      # Cleaned datasets and engineered feature matrices
├── models/                             # Serialized Scikit-Learn pipelines (.joblib, git-ignored)
├── notebooks/
│   ├── 01_exploratory_audit.ipynb      # Initial exploratory inspection
│   ├── 02_feature_engineering.ipynb    # Feature prototyping & validation
│   ├── 03_eda_visualizations.ipynb     # Color-color diagrams & distribution comparisons
│   └── 04_baseline_models.ipynb        # Baseline model training & evaluation
├── reports/
│   └── figures/                        # Exported publication-ready plots (.png)
├── src/
│   ├── data/                           # Data download and sanitization scripts
│   └── features/                       # Feature extraction & encoding pipeline
├── environment.yml                     # Conda environment configuration
├── requirements.txt                    # Pip dependencies specification
└── README.md
```

---

## Project Status & Roadmap

- [x] **Data Ingestion & Extraction** (Issue #1: SDSS DR16 SQL query via Astroquery: 50,000 stars & 50,000 QSOs)
- [x] **Data Cleaning** (Issue #2: Filtered `-9999` sentinels, faint magnitudes $> 30$, and inconsistent redshifts)
- [x] **Feature Engineering** (Issue #3: Computed adjacent color indices with metadata strictly segregated)
- [x] **Exploratory Data Analysis (EDA)** (Issue #4: Color-color diagrams, correlation matrices, and distribution analysis)
- [x] **Model Training** (Issue #5: Scikit-Learn pipelines for Logistic Regression and Random Forest)
- [ ] **Evaluation & Error Analysis** (Issue #6: In-depth metrics, feature importances, and misclassified star/quasar inspection)
- [ ] **Documentation & Final Release** (Issue #7: Comprehensive documentation, dependency audit, and v1.0.0 release)

---

## Baseline Model Benchmarks

Models were evaluated on a held-out stratified test set (20%, $N = 19,992$, `random_state=13`). Metrics report Quasar (`QSO`) classification performance:

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Key Characteristics |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Dummy Classifier** | 50.0% | 0.50 | 0.50 | 0.50 | 0.50 | Uniform random baseline |
| **Gaussian Naive Bayes** | 72.7% | 0.67 | 0.90 | 0.77 | 0.91 | Fast baseline; high recall, high star contamination |
| **Logistic Regression** | 91.3% | 0.91 | 0.92 | 0.91 | 0.93 | Standardized linear decision boundary |
| **Random Forest (100 trees)** | **95.7%** | **0.96** | **0.96** | **0.96** | **0.99** | Non-linear ensemble resolving stellar locus curvature |

<p align="center">
  <img src="reports/figures/roc_curves_baseline.png" alt="Multi-Model ROC Curves" width="48%"/>
</p>

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
# 1. Query SDSS DR16 via Astroquery to fetch raw data
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
