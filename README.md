# Weeks 1–4: Comprehensive Data Cleaning, Analysis, Visualization, Statistical Modeling, and Synthesis with R
## UCI Adult/Census Income Dataset

### Project Overview
This repository contains an end-to-end, four-week academic data science project using the UCI Adult (Census Income) Dataset in R.

- **Week 1:** Complete data cleaning, preprocessing, feature transformation, and exploratory data analysis (R scripts 01–07).
- **Week 2:** Comprehensive data visualization and insight communication using **ggplot2, lattice, and Base R** (R scripts 08–09), with a professional DOCX report.
- **Week 3:** Parametric & non-parametric hypothesis testing, binary classification modeling (Logistic Regression & Elastic Net), and diagnostics (R scripts 10–13), with a professional DOCX report.
- **Week 4:** Comprehensive final integrated monograph (`report/Week4_Comprehensive_Data_Analysis_Final_Report.docx`) synthesizing Weeks 1–3 into one 16-section publication-quality document.

All work is reproducible from the original `adult.data` file using `run_all.R`.

### Dataset Provenance
- **Source**: UCI Machine Learning Repository / U.S. Census Bureau 1994 Current Population Survey
  - Citation: Kohavi, R., & Becker, B. (1996). Adult Dataset. UCI Machine Learning Repository. https://doi.org/10.24432/C5XW20
- **Primary file**: `data/original/adult.data` (32,561 records, 15 attributes)
- **Documentation**: `data/original/adult.names`
- **Target Variable**: Annual income threshold (`<=50K` vs. `>50K`)

---

### Repository Structure
```
week-1-r-data-cleaning-analysis/
├── data/
│   ├── original/                     # Original unmodified dataset (adult.data, adult.names, adult.test)
│   └── cleaned/                      # Cleaned and normalized datasets
│       ├── adult_cleaned.csv         # 32,537 rows × 15 columns (imputed, deduplicated)
│       └── adult_normalized.csv      # 32,537 rows × 57 columns (normalized + dummy features)
├── R/
│   ├── 01_import.R                   # Ingestion, NA parsing, dimension checks
│   ├── 02_quality_assessment.R       # Data quality audit & missingness assessment
│   ├── 03_cleaning.R                 # Mode imputation, deduplication, factor conversions
│   ├── 04_outlier_analysis.R         # Tukey IQR outlier detection & boxplots
│   ├── 05_transformation.R           # Min-Max normalization & fastDummies encoding
│   ├── 06_eda.R                      # Week 1 EDA visualizations (13 figures)
│   ├── 07_final_analysis.R           # Descriptive statistics, correlations & summary
│   ├── 08_week2_visualizations.R     # Week 2: 15 visualization charts (ggplot2, lattice, Base R)
│   ├── 09_week2_analysis.R           # Week 2: Evidence-based insights & statistics
│   ├── 10_week3_statistical_analysis.R # Week 3: Hypothesis testing & correlation matrices
│   ├── 11_week3_modeling.R           # Week 3: Logistic Regression & Elastic Net (5-fold CV)
│   ├── 12_week3_evaluation.R         # Week 3: ROC/PR curves, calibration, influence diagnostics
│   └── 13_week3_report_generation.R  # Week 3: Pipeline verification & report driver
├── plots/
│   ├── 04_*.png                      # Week 1 outlier boxplots
│   ├── 06_*.png                      # Week 1 EDA charts (13 figures)
│   ├── week2_*.png                   # Week 2 visualizations (15 charts, 300 DPI)
│   └── week3/                        # Week 3 model & inference diagnostics (15+ charts)
├── outputs/                          # CSV and RDS output files, text reports
│   ├── week3_statistics/             # Hypothesis test results, descriptive statistics
│   └── week3_model/                  # Odds ratios, evaluation metrics, VIF, calibration
├── evidence/week3/                   # Full reproducibility evidence outputs
├── report/
│   ├── generate_report.py            # Week 1 DOCX builder
│   ├── generate_week2_report.py      # Week 2 DOCX builder
│   ├── generate_week3_report.py      # Week 3 DOCX builder
│   ├── generate_week4_report.py      # Week 4 comprehensive DOCX builder
│   ├── Week1_Adult_Analysis_Report.docx  # Week 1 academic report
│   ├── Week2_Data_Visualization_Report.docx  # Week 2 academic report
│   ├── Week3_Statistical_Analysis_Predictive_Modeling.docx  # Week 3 academic report
│   └── Week4_Comprehensive_Data_Analysis_Final_Report.docx  # Week 4 comprehensive report
├── run_all.R                         # Master execution script (Weeks 1–3)
├── .gitignore
└── README.md
```

---

## Week 1: Data Cleaning and Preliminary Analysis

### What Was Done
1. **Data Import** (01_import.R): Raw CSV with 32,561 records; `?` values parsed as NA; column types assigned.
2. **Quality Assessment** (02_quality_assessment.R): Identified 4,262 missing values across 3 variables.
3. **Cleaning** (03_cleaning.R): Mode imputation of missing values; 24 duplicate rows removed; factors encoded.
4. **Outlier Analysis** (04_outlier_analysis.R): Tukey IQR fences computed; all 32,537 records retained as genuine observations.
5. **Transformation** (05_transformation.R): Min-Max normalization; one-hot dummy encoding (36 binary columns added).
6. **EDA** (06_eda.R): 13 publication-quality charts covering income, age, education, occupation, and bivariate relationships.
7. **Final Analysis** (07_final_analysis.R): Descriptive statistics tables; correlation matrix; before/after cleaning comparison.

### Key Week 1 Results
- **Baseline Sample**: 32,561 observations, 15 variables.
- **Missing Values**: 4,262 total cells (workclass: 1,836; occupation: 1,843; native_country: 583). All resolved via mode imputation.
- **Duplicate Rows**: 24 exact duplicate records removed (post-cleaning N = 32,537).
- **Outlier Fences**: Tukey IQR fences computed for 6 continuous variables. All records retained as legitimate observations.
- **Target Distribution**: 24,698 (75.91%) earn `<=50K`; 7,839 (24.09%) earn `>50K`.

---

## Week 2: Data Visualization and Insight Communication

### Objective
Week 2 extends the cleaned Week 1 dataset into a comprehensive visualization and insight communication project using **ggplot2, lattice, and Base R**. The 15 charts combine multiple visualization styles while maintaining a consistent professional academic presentation.

### Visualizations Produced (15 Charts Across ggplot2, lattice, and Base R)

| Figure | Title | Chart Type | Engine / Framework |
|--------|-------|-----------|--------------------|
| 1 | Income Distribution | Bar Chart | `ggplot2` |
| 2 | Age Distribution | Histogram | `ggplot2` |
| 3 | Education Distribution | Horizontal Bar Chart | `ggplot2` |
| 4 | Education vs Income | Proportional Stacked Bar | `ggplot2` |
| 5 | Workclass vs Income | Proportional Stacked Bar | `ggplot2` |
| 6 | Age vs Income | Violin + Boxplot | `ggplot2` |
| 7 | Hours per Week Distribution | Histogram | `ggplot2` |
| 8 | Hours per Week vs Income | Violin + Boxplot | `ggplot2` |
| 9 | Age vs Hours per Week | Scatter Plot with Loess Smooth | `ggplot2` |
| 10 | Capital Gain Distribution | Histogram (Log10 Scale) | `ggplot2` |
| 11 | Correlation Heatmap | Heatmap | `ggplot2` / `reshape2` |
| 12 | Occupation vs Income (Creative) | Proportional Stacked Bar | `ggplot2` |
| 13 | Age Cohort Income Trend (Supplementary) | Ordered Cohort Trend Line Chart | `ggplot2` |
| 14 | Weekly Hours vs Age by Income (Supplementary) | Trellis Conditioning Scatter Plot | `lattice` |
| 15 | Age Distribution (Supplementary) | Native Frequency Histogram | `Base R` |

### R Scripts
- **R/08_week2_visualizations.R** — Generates all 15 figures utilizing **ggplot2**, **lattice** (`xyplot`), and **Base R** graphics (`hist`, `abline`).
- **R/09_week2_analysis.R** — All analytical computations (11 evidence-based insights, descriptive statistics, correlation analysis).

### Week 2 Report
`report/Week2_Data_Visualization_Report.docx` — A professional academic DOCX report (~50+ pages) containing:
- Title page and table of contents
- Dataset overview and connection to Week 1
- Visualization design strategy and chart selection rationale
- All 15 visualizations with Purpose, Why This Chart, R Code, Output, Interpretation, and Key Insight sections
- Line chart design decision (explaining why no artificial time-series was created on cross-sectional data)
- Supplementary sections for **lattice** (Figure 14) and **Base R** (Figure 15)
- 11 evidence-based insights (Finding / Evidence / Interpretation / Caution format)
- Non-technical communication summary
- Limitations, Conclusion, References
- Appendix with complete Week 2 R code

---

### Reproducing the Analysis

#### Full Pipeline (Week 1 + Week 2)
```powershell
cd c:\Users\Microsoft\week\week-1-r-data-cleaning-analysis
Rscript run_all.R
```
*(Or use the full path: `& "C:\Users\Microsoft\R\bin\Rscript.exe" run_all.R`)*

#### Week 2 Only (assumes Week 1 outputs already exist)
```powershell
Rscript R/08_week2_visualizations.R
Rscript R/09_week2_analysis.R
```

#### Regenerate Week 2 DOCX Report
```powershell
python report\generate_week2_report.py
```

#### Regenerate Week 1 DOCX Report
```powershell
python report\generate_report.py
```

---

### Key Empirical Results Summary (Both Weeks)
- **Baseline Sample**: 32,561 observations, 15 variables.
- **Cleaned Dataset**: 32,537 rows × 15 columns (post-imputation and deduplication).
- **Income Distribution**: 24,698 (75.91%) earn `<=50K`; 7,839 (24.09%) earn `>50K`.
- **Age**: Median 37 yrs overall; >50K earners median 44 yrs vs <=50K median 34 yrs.
- **Education**: Positive monotonic association with high income (0% Preschool → 74.1% Doctorate).
- **Hours Worked**: 46.7% work exactly 40 hours/week; >50K earners mean 45.5 vs 38.8 hrs.
- **Capital Gain**: 91.7% report zero gains; 8.3% positive with extreme right skew.
- **Occupation**: Highest high-income rate: Exec-managerial (48.4%); Lowest: Priv-house-serv (0.7%).
- **Correlations**: All pairwise |r| < 0.15 among continuous variables (no strong multicollinearity).

---

### Limitations
The dataset reflects 1994 U.S. Census Bureau data. Results should not be generalized to contemporary conditions. All observed relationships are associational (not causal). Missing values were resolved via mode imputation. See the Week 2 report for a complete limitations discussion.

---

## Week 3: Statistical Analysis and Predictive Modeling

### Objectives
- Conduct formal parametric and non-parametric hypothesis testing across demographic and human capital dimensions
- Develop a reproducible binary classification pipeline predicting annual income >$50K
- Evaluate models using held-out test set performance and diagnostic integrity checks
- Compile a publication-quality academic Word report (~25 pages, 18 embedded figures, 16 tables)

### New Scripts and Outputs

| Script | Description |
|--------|-------------|
| `R/10_week3_statistical_analysis.R` | Descriptive statistics, normality diagnostics, Pearson/Spearman correlation matrices, 9 hypothesis tests with Bonferroni & BH-FDR corrections |
| `R/11_week3_modeling.R` | Stratified 80/20 train/test split, 5-fold cross-validation, standard logistic regression, Elastic Net (glmnet) |
| `R/12_week3_evaluation.R` | Confusion matrix, ROC-AUC, PR-AUC, calibration curve, Cook's distance residuals, odds ratios forest plot, 10+ visualizations |
| `R/13_week3_report_generation.R` | Verifies prerequisites and invokes Python DOCX compiler |
| `report/generate_week3_report.py` | Produces `Week3_Statistical_Analysis_Predictive_Modeling.docx` (2.05 MB, 18 figures) |

**New output directories:**
- `outputs/week3_statistics/` — Descriptive stats, correlation matrices, hypothesis test CSV and TXT
- `outputs/week3_model/` — Logistic coefficients, odds ratios, VIF, calibration, confusion matrices, predictions
- `plots/week3/` — 18 high-resolution PNG figures (300 DPI)
- `evidence/week3/` — Reproducibility evidence (CSV outputs, text reports, R package versions)

### Required R Packages (Week 3)

```r
install.packages(c("dplyr", "ggplot2", "tidyr", "scales", "corrplot",
                   "reshape2", "moments", "car", "glmnet", "pROC"))
```

Python (for report generation): `pip install python-docx pandas`

### Running Week 3

#### Full Pipeline (Weeks 1 + 2 + 3)
```powershell
Rscript run_all.R
```

#### Week 3 Scripts Only (assumes Week 1 cleaned dataset exists)
```powershell
Rscript R/10_week3_statistical_analysis.R
Rscript R/11_week3_modeling.R
Rscript R/12_week3_evaluation.R
Rscript R/13_week3_report_generation.R
```

#### Regenerate Week 3 DOCX Report Directly
```powershell
python report\generate_week3_report.py
```

### Week 3 Key Findings

**Hypothesis Tests (all N = 32,537, α = 0.05, Bonferroni & BH-FDR corrected):**
- **Age vs Income:** Welch t = 50.24, p < 0.0001, Cohen's d = 0.563 — High earners average 44.25 yrs vs 36.79 yrs
- **Weekly Hours vs Income:** Welch t = 45.10, p < 0.0001, Cohen's d = 0.552 — High earners work 45.5 vs 38.8 hrs/week
- **Education vs Income:** Chi-square = 4,428.4, df = 15, p < 0.0001, Cramer's V = 0.369 (moderate effect)
- **Occupation vs Income:** Chi-square = 3,197.6, df = 13, p < 0.0001, Cramer's V = 0.314
- **Workclass vs Income:** Chi-square = 922.4, df = 7, p < 0.0001, Cramer's V = 0.168

**Predictive Modeling (Test Set N = 6,508):**

| Model | Accuracy | ROC-AUC | F1-Score | Recall |
|-------|----------|---------|----------|--------|
| Baseline (Majority Class) | 75.91% | 0.500 | 0.000 | 0.0% |
| Logistic Regression (GLM) | **84.76%** | **0.905** | **0.655** | 60.1% |
| Elastic Net (alpha=0.5) | 84.10% | 0.900 | 0.625 | 55.0% |

**Cross-Validation (Training N = 26,029):** 5-fold CV Mean AUC = 0.9047 ± 0.0053, Mean Accuracy = 85.10% ± 0.29%

**Diagnostics:** All predictors GVIF^(1/(2·Df)) < 1.73 (no collinearity). Max Cook's D = 0.0330. Calibration error < 3% across all probability deciles.

### Week 3 Report
`report/Week3_Statistical_Analysis_Predictive_Modeling.docx` (2.05 MB)
- 18 embedded publication-quality figures (300 DPI)
- 16 formatted academic tables including odds ratios, VIF, calibration, and multi-metric evaluation
- Complete hypothesis test battery with effect sizes, assumption checks, and plain-English conclusions
- Odds ratio forest plot with 95% Wald confidence intervals for key predictors

### Environment Limitations
- Random seed `set.seed(2026)` ensures full reproducibility of train/test split, CV folds, and Elastic Net tuning
- The `glm.fit: fitted probabilities numerically 0 or 1 occurred` warning is expected due to near-perfect separation in sparse categories (e.g., `workclassNever-worked` and `workclassWithout-pay`). Elastic Net regularization stabilizes these coefficients.
- Report generation requires Python 3 with `python-docx >= 1.0` and `pandas`

---

## Week 4: Comprehensive Data Analysis Reporting and Presentation

### Objective and Scope
Week 4 completes the engagement by integrating all previous three weeks of work—data cleaning (Week 1), visualization (Week 2), and statistical modeling (Week 3)—into a single, professionally designed, 16-section academic and professional monograph:
`report/Week4_Comprehensive_Data_Analysis_Final_Report.docx`.

The report unifies data hygiene, exploratory graphical insight, parametric and non-parametric hypothesis testing, and regularized predictive modeling into an evidence-based narrative without relying on ungrounded claims or post-hoc data fabrication.

### Final Deliverable Details
- **File Path**: `report/Week4_Comprehensive_Data_Analysis_Final_Report.docx`
- **File Size**: ~2.29 MB (2,295,908 bytes)
- **Estimated Length**: ~28–32 formatted pages (8,481 words, 247 paragraphs)
- **Embedded Figures**: 15 authentic high-resolution charts across data cleaning, EDA, lattice conditioning, inference diagnostics, and ROC/PR performance curves
- **Embedded Tables**: 17 structured tables (metadata schema, before/after cleaning metrics, Tukey outlier bounds, hypothesis tests registry, odds ratios, GVIF multicollinearity, consolidated model comparison, confusion matrix breakdown, calibration deciles, cross-week integration matrix, and R package versions)
- **Code Listings**: Annotated R code blocks highlighting real implementations from `01_import.R`, `03_cleaning.R`, `10_week3_statistical_analysis.R`, and `11_week3_modeling.R`

### Structure of the 16-Section Integrated Report
1. **Section 1 — Title Page**: Official title, subtitle, repository URL, local path, metadata block, and reproducibility declaration.
2. **Section 2 — Executive Summary**: Synthesis of data cleaning achievements, visual discoveries, statistical test results, and predictive metrics.
3. **Section 3 — Introduction and Objectives**: Theoretical context, human capital problem formulation, and the 8-stage data science lifecycle.
4. **Section 4 — Dataset Description and Data Source**: Provenance (1994 U.S. Census CPS), 15-variable schema dictionary, missingness profile, and data types.
5. **Section 5 — Week 1: Data Cleaning and Preliminary Analysis**: Mode imputation (4,262 cells), duplicate purging (24 rows), Tukey IQR outlier screening, and transformations.
6. **Section 6 — Week 2: Data Visualization and Insight Communication**: Tufte graphical principles, class imbalance (3.15:1), age divergence (10-yr median gap), 40-hr spike, and lattice conditioning.
7. **Section 7 — Week 3: Statistical Analysis and Hypothesis Testing**: Formal verification confirming exactly 8 tests across 5 research questions (all p < 0.0001 under Bonferroni & BH-FDR), effect sizes (Cramer's V, Cohen's d), and assumption audits.
8. **Section 8 — Week 3: Predictive Modeling**: Stratified 80/20 train/test split (seed 2026), 5-fold CV, Baseline vs. Logistic Regression vs. Elastic Net, odds ratios (marriage OR = 7.16, education OR = 1.35), and GVIF (< 1.73).
9. **Section 9 — Model Evaluation and Diagnostics**: Multi-metric evaluation (GLM Accuracy: 84.76%, ROC-AUC: 0.9047, PR-AUC: 0.7271), confusion matrix trade-offs, decile calibration, and Cook's distance influence diagnostics.
10. **Section 10 — Integrated Findings Across Weeks 1–3**: Comprehensive stage-to-insight synthesis matrix mapping data hygiene to exploratory and predictive milestones.
11. **Section 11 — Discussion and Practical Implications**: Human capital returns, labor market segmentation, non-causality of observational data, and Title VII algorithmic fairness constraints.
12. **Section 12 — Challenges Encountered and Lessons Learned**: Verified project hurdles (non-standard '?' missing tokens, capital gain zero-inflation, class imbalance, p-value sample size sensitivity).
13. **Section 13 — Recommendations and Future Work**: Cost-sensitive decision threshold optimization, non-linear ensemble models (XGBoost/SHAP), contemporary ACS benchmarking, and disparate impact audits.
14. **Section 14 — Conclusion**: Final verdict on the power of an evidence-based, reproducible analytical workflow.
15. **Section 15 — Reproducibility and Technical Appendix**: Directory tree, script inventory, software versions (R 4.6.1, tidyverse, car, glmnet, pROC), execution instructions, and statistical glossary.
16. **Section 16 — References**: Complete academic bibliography (Becker, Mincer, Tufte, Benjamini-Hochberg, Friedman et al., Kohavi & Becker).

### Regenerating the Week 4 Report
To regenerate the Week 4 final report from the command line:
```powershell
python report\generate_week4_report.py
```
*(Requires Python 3 with `python-docx >= 1.0` and `pandas`)*

