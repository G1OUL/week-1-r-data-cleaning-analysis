# Week 1 & Week 2: Data Cleaning, Analysis, and Visualization with R
## UCI Adult/Census Income Dataset

### Project Overview
This repository contains a two-week academic data analytics project using the UCI Adult (Census Income) Dataset in R.

- **Week 1:** Complete data cleaning, preprocessing, feature transformation, and exploratory data analysis (R scripts 01–07).
- **Week 2:** Comprehensive data visualization and insight communication using ggplot2 (R scripts 08–09), with a professional DOCX report.

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
│   ├── 08_week2_visualizations.R     # Week 2: 13 publication-quality ggplot2 charts
│   └── 09_week2_analysis.R           # Week 2: Evidence-based insights & statistics
├── plots/
│   ├── 04_*.png                      # Week 1 outlier boxplots
│   ├── 06_*.png                      # Week 1 EDA charts (13 figures)
│   └── week2_*.png                   # Week 2 visualizations (13 charts, 300 DPI)
├── outputs/                          # CSV and RDS output files, text reports
├── report/
│   ├── generate_report.py            # Week 1 DOCX builder
│   ├── generate_week2_report.py      # Week 2 DOCX builder
│   ├── Week1_Adult_Analysis_Report.docx  # Week 1 academic report
│   └── Week2_Data_Visualization_Report.docx  # Week 2 academic report
├── run_all.R                         # Master execution script (Week 1 + Week 2)
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
Week 2 extends the cleaned Week 1 dataset into a comprehensive visualization and insight communication project. All charts were produced using ggplot2 at 300 DPI with a consistent professional academic theme.

### Visualizations Produced (13 Charts)

| Figure | Title | Chart Type |
|--------|-------|-----------|
| 1 | Income Distribution | Bar Chart |
| 2 | Age Distribution | Histogram |
| 3 | Education Distribution | Horizontal Bar Chart |
| 4 | Education vs Income | Proportional Stacked Bar |
| 5 | Workclass vs Income | Proportional Stacked Bar |
| 6 | Age vs Income | Violin + Boxplot |
| 7 | Hours per Week Distribution | Histogram |
| 8 | Hours per Week vs Income | Violin + Boxplot |
| 9 | Age vs Hours per Week | Scatter Plot |
| 10 | Capital Gain Distribution | Histogram (Log Scale) |
| 11 | Correlation Heatmap | Heatmap |
| 12 | Occupation vs Income (Creative) | Proportional Stacked Bar |
| 13 | Age Cohort Income Trend (Supplementary) | Line Chart (ordered cohort) |

### R Scripts
- **R/08_week2_visualizations.R** — All ggplot2 visualizations (Figures 1–13).
- **R/09_week2_analysis.R** — All analytical computations (11 evidence-based insights, descriptive statistics, correlation analysis).

### Week 2 Report
`report/Week2_Data_Visualization_Report.docx` — A professional academic DOCX report (~50+ pages) containing:
- Title page and table of contents
- Dataset overview and connection to Week 1
- Visualization design strategy
- All 12 visualizations with Purpose, Why This Chart, R Code, Output, Interpretation, and Key Insight sections
- Line chart design decision (with explanation of why no time-series chart was produced)
- 11 evidence-based insights (Finding / Evidence / Interpretation / Caution format)
- Non-technical communication summary
- Limitations, Conclusion, References
- Appendix with complete R code

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
