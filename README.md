# Week 1: Data Cleaning and Preliminary Analysis with R
## UCI Adult/Census Income Dataset

### Project Overview
This project performs comprehensive data cleaning, preprocessing, feature transformation, and exploratory data analysis on the UCI Adult (Census Income) dataset using R. It completely fulfills the Week 1 academic data analytics assignment requirements.

### Dataset Provenance
- **Source**: UCI Machine Learning Repository / U.S. Census Bureau 1994 Current Population Survey
  - Citation: Kohavi, R., & Becker, B. (1996). Adult Dataset. UCI Machine Learning Repository. https://doi.org/10.24432/C5XW20
- **Primary file**: `data/original/adult.data` (32,561 records, 15 attributes)
- **Documentation**: `data/original/adult.names`
- **Optional/Test file**: `data/original/adult.test` (16,281 records)
- **Target Variable**: Annual income threshold classification (`<=50K` vs. `>50K`)

---

### Project Repository Structure
```
Week1_Adult_R_Analysis/
├── data/
│   ├── original/                     # Original unmodified dataset files (adult.data, adult.names, adult.test)
│   └── cleaned/                      # Cleaned and normalized datasets
│       ├── adult_cleaned.csv         # 32,537 rows × 15 columns (imputed, deduplicated, standardized)
│       └── adult_normalized.csv      # 32,537 rows × 57 columns (with normalized & dummy features)
├── R/
│   ├── 01_import.R                   # Ingestion, NA parsing, dimension checks
│   ├── 02_quality_assessment.R       # Data quality audit & missingness assessment
│   ├── 03_cleaning.R                 # Mode imputation, deduplication, factor conversions
│   ├── 04_outlier_analysis.R         # Tukey IQR outlier detection & boxplots
│   ├── 05_transformation.R           # Min-Max normalization & fastDummies encoding
│   ├── 06_eda.R                      # Exploratory visualizations (13 figures)
│   └── 07_final_analysis.R           # Descriptive statistics, correlations & summary
├── plots/                            # 22 publication-quality PNG charts & boxplots
├── outputs/                          # Output tables (CSV) and serialized objects (RDS)
├── report/
│   ├── generate_report.py            # Automated DOCX academic report builder
│   └── Week1_Adult_Analysis_Report.docx # Comprehensive 35+ page academic report
├── run_all.R                         # Master R execution script
└── README.md                         # Reproduction guide & documentation
```

---

### Reproducing the Analysis

#### 1. Execution via R Master Script
To execute the entire 7-stage analytical pipeline from start to finish:
```powershell
cd c:\Users\black\Downloads\adult\Week1_Adult_R_Analysis
& "C:\Users\black\R\app\bin\x64\Rscript.exe" run_all.R
```
*(Or simply `Rscript run_all.R` if R is mapped to system `PATH`)*

#### 2. Generating the Academic DOCX Report
To rebuild the formatted academic Microsoft Word report:
```powershell
cd c:\Users\black\Downloads\adult\Week1_Adult_R_Analysis
python report\generate_report.py
```

---

### Key Empirical Results Summary
- **Baseline Sample**: 32,561 observations, 15 variables.
- **Missing Values**: 4,262 total cells with `?` (1,836 in `workclass`, 1,843 in `occupation`, 583 in `native_country`). All resolved via mode imputation.
- **Duplicate Rows**: Exactly 24 duplicate records identified and pruned (post-cleaning rows = 32,537).
- **Outlier Fences**: Tukey IQR fences calculated for all 6 continuous variables. All 32,537 records retained as genuine domain observations.
- **Normalization**: Min-Max scaling to [0, 1] implemented for all continuous features.
- **Encoding**: One-hot dummy encoding added 36 binary indicators with reference categories dropped.
- **Target Distribution**: 24,698 (75.91%) earn `<=50K`; 7,839 (24.09%) earn `>50K`.
