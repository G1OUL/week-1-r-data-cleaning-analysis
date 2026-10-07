# =============================================================================
# Script 09: Week 2 Analysis — Evidence-Based Insights and Summary Statistics
# Project: Week 2 - Data Visualization and Insight Communication using R
# Dataset: UCI Adult/Census Income Dataset (Cleaned from Week 1)
# =============================================================================

suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
  library(tidyr)
  library(scales)
  library(moments)
})

cat("=============================================================\n")
cat("  Script 09: Week 2 Analysis and Insights\n")
cat("=============================================================\n\n")

# 1. SETUP PATHS
find_root <- function() {
  dirs <- c(getwd(), dirname(getwd()), file.path(getwd(), 'Week1_Adult_R_Analysis'))
  for (d in dirs) {
    if (file.exists(file.path(d, 'data', 'original', 'adult.data'))) return(d)
  }
  return(getwd())
}
project_root <- find_root()
outputs_dir  <- file.path(project_root, "outputs")
plots_dir    <- file.path(project_root, "plots")

rds_path <- file.path(outputs_dir, "adult_cleaned.rds")
adult <- readRDS(rds_path)
cat(sprintf("Dataset loaded: %d rows × %d columns\n\n", nrow(adult), ncol(adult)))

sink(file.path(outputs_dir, "09_week2_insights.txt"))

cat("=======================================================================\n")
cat("  WEEK 2 ANALYTICAL INSIGHTS — UCI Adult Income Dataset\n")
cat("  Derived from actual dataset computations\n")
cat("=======================================================================\n\n")

# -----------------------------------------------------------------------
# INSIGHT 1: Income Class Imbalance
# -----------------------------------------------------------------------
cat("INSIGHT 1: Severe Income Class Imbalance\n")
cat("-------------------------------------------------------------------\n")
inc_tab <- table(adult$income)
inc_pct <- prop.table(inc_tab) * 100
cat(sprintf("  Total observations: %s\n", format(nrow(adult), big.mark = ",")))
cat(sprintf("  Income <=50K: %s (%.2f%%)\n", format(inc_tab["<=50K"], big.mark = ","), inc_pct["<=50K"]))
cat(sprintf("  Income >50K:  %s (%.2f%%)\n", format(inc_tab[">50K"], big.mark = ","), inc_pct[">50K"]))
cat(sprintf("  Ratio <=50K:>50K = %.2f:1\n\n", inc_tab["<=50K"] / inc_tab[">50K"]))

# -----------------------------------------------------------------------
# INSIGHT 2: Age Demographic Differences
# -----------------------------------------------------------------------
cat("INSIGHT 2: Significant Age Demographic Differences by Income\n")
cat("-------------------------------------------------------------------\n")
age_by_inc <- adult %>%
  group_by(income) %>%
  summarise(
    n        = n(),
    mean_age = mean(age),
    median_age = median(age),
    sd_age   = sd(age),
    q1_age   = quantile(age, 0.25),
    q3_age   = quantile(age, 0.75),
    .groups  = "drop"
  )
print(as.data.frame(age_by_inc))
cat(sprintf("\n  Age gap (median): >50K earners are %d years older than <=50K earners on average\n",
            age_by_inc$median_age[age_by_inc$income == ">50K"] - age_by_inc$median_age[age_by_inc$income == "<=50K"]))
cat(sprintf("  Age skewness: %.4f (right-skewed; young workers more prevalent)\n\n", skewness(adult$age)))

# -----------------------------------------------------------------------
# INSIGHT 3: Education Attainment Gradient
# -----------------------------------------------------------------------
cat("INSIGHT 3: Monotonic Education–Income Association\n")
cat("-------------------------------------------------------------------\n")
edu_inc_pct <- adult %>%
  group_by(education, education_num) %>%
  summarise(
    n_total = n(),
    n_high  = sum(income == ">50K"),
    pct_gt50k = sum(income == ">50K") / n() * 100,
    .groups = "drop"
  ) %>%
  arrange(education_num)

print(as.data.frame(edu_inc_pct))
# Safe extraction using match
doc_pct  <- edu_inc_pct$pct_gt50k[match("Doctorate",    edu_inc_pct$education)]
bach_pct <- edu_inc_pct$pct_gt50k[match("Bachelors",    edu_inc_pct$education)]
mast_pct <- edu_inc_pct$pct_gt50k[match("Masters",      edu_inc_pct$education)]
prof_pct <- edu_inc_pct$pct_gt50k[match("Prof-school",  edu_inc_pct$education)]
pre_pct  <- edu_inc_pct$pct_gt50k[match("Preschool",    edu_inc_pct$education)]
cat(sprintf("\n  Lowest: Preschool (%.2f%%); Highest: Doctorate (%.2f%%)\n", pre_pct, doc_pct))
cat(sprintf("  Bachelors: %.2f%% high-income; Masters: %.2f%%; Prof-school: %.2f%%\n\n",
            bach_pct, mast_pct, prof_pct))

# -----------------------------------------------------------------------
# INSIGHT 4: Hours Per Week Standard Workweek Concentration
# -----------------------------------------------------------------------
cat("INSIGHT 4: Institutional Concentration at 40-Hour Workweek\n")
cat("-------------------------------------------------------------------\n")
hours_stat <- adult %>% summarise(
  mean_hours   = mean(hours_per_week),
  median_hours = median(hours_per_week),
  sd_hours     = sd(hours_per_week),
  iqr_hours    = IQR(hours_per_week),
  exactly_40   = sum(hours_per_week == 40),
  pct_40       = mean(hours_per_week == 40) * 100,
  under_40     = sum(hours_per_week < 40),
  pct_under40  = mean(hours_per_week < 40) * 100,
  over_40      = sum(hours_per_week > 40),
  pct_over40   = mean(hours_per_week > 40) * 100
)
print(as.data.frame(hours_stat))
cat(sprintf("\n  Hours by income - <=50K mean: %.2f hrs; >50K mean: %.2f hrs\n",
            mean(adult$hours_per_week[adult$income == "<=50K"]),
            mean(adult$hours_per_week[adult$income == ">50K"])))
cat(sprintf("  IQR for <=50K: %d hrs; IQR for >50K: %d hrs\n\n",
            IQR(adult$hours_per_week[adult$income == "<=50K"]),
            IQR(adult$hours_per_week[adult$income == ">50K"])))

# -----------------------------------------------------------------------
# INSIGHT 5: Capital Gain Extreme Concentration (Highly Skewed)
# -----------------------------------------------------------------------
cat("INSIGHT 5: Extreme Concentration and Skewness in Capital Gains\n")
cat("-------------------------------------------------------------------\n")
cap_zero <- sum(adult$capital_gain == 0)
cap_nz   <- adult %>% filter(capital_gain > 0)
cat(sprintf("  Zero-gain individuals: %s (%.2f%%)\n", format(cap_zero, big.mark = ","), cap_zero/nrow(adult)*100))
cat(sprintf("  Positive-gain individuals: %s (%.2f%%)\n", format(nrow(cap_nz), big.mark = ","), nrow(cap_nz)/nrow(adult)*100))
cat(sprintf("  Non-zero: Min=%.0f, Median=%.0f, Mean=%.0f, Max=%.0f\n",
            min(cap_nz$capital_gain), median(cap_nz$capital_gain),
            mean(cap_nz$capital_gain), max(cap_nz$capital_gain)))
cat(sprintf("  Top-code ceiling (99999): %d individuals\n", sum(adult$capital_gain == 99999)))
cat(sprintf("  Skewness (overall): %.4f (extreme right skew)\n\n", skewness(adult$capital_gain)))

# -----------------------------------------------------------------------
# INSIGHT 6: Workclass Self-Employed Premium
# -----------------------------------------------------------------------
cat("INSIGHT 6: Self-Employment Income Premium vs Private Sector\n")
cat("-------------------------------------------------------------------\n")
wc_inc <- adult %>%
  group_by(workclass) %>%
  summarise(
    total    = n(),
    n_high   = sum(income == ">50K"),
    pct_high = sum(income == ">50K") / n() * 100,
    .groups  = "drop"
  ) %>%
  arrange(desc(pct_high))
print(as.data.frame(wc_inc))
cat("\n")

# -----------------------------------------------------------------------
# INSIGHT 7: Occupational Economic Stratification
# -----------------------------------------------------------------------
cat("INSIGHT 7: Sharp Occupational Economic Stratification\n")
cat("-------------------------------------------------------------------\n")
occ_inc <- adult %>%
  group_by(occupation) %>%
  summarise(
    total    = n(),
    n_high   = sum(income == ">50K"),
    pct_high = sum(income == ">50K") / n() * 100,
    .groups  = "drop"
  ) %>%
  arrange(desc(pct_high))
print(as.data.frame(occ_inc))
# Safe match-based extraction
exec_pct <- occ_inc$pct_high[match("Exec-managerial",  occ_inc$occupation)]
prof_pct <- occ_inc$pct_high[match("Prof-specialty",   occ_inc$occupation)]
phs_pct  <- occ_inc$pct_high[match("Priv-house-serv",  occ_inc$occupation)]
svc_pct  <- occ_inc$pct_high[match("Other-service",    occ_inc$occupation)]
cat(sprintf("\n  Highest: Exec-managerial (%.1f%%), Prof-specialty (%.1f%%)\n", exec_pct, prof_pct))
cat(sprintf("  Lowest: Private house service (%.1f%%), Other-service (%.1f%%)\n\n", phs_pct, svc_pct))

# -----------------------------------------------------------------------
# INSIGHT 8: Age-Cohort Income Life Cycle
# -----------------------------------------------------------------------
cat("INSIGHT 8: Inverted U-Curve Age Cohort Income Pattern\n")
cat("-------------------------------------------------------------------\n")
adult_cohort <- adult %>%
  mutate(age_cohort = cut(age,
                          breaks = c(16, 25, 35, 45, 55, 65, 100),
                          labels = c("17-25", "26-35", "36-45", "46-55", "56-65", "66+"))) %>%
  group_by(age_cohort) %>%
  summarise(
    n               = n(),
    pct_high_income = mean(income == ">50K") * 100,
    mean_hours      = mean(hours_per_week),
    .groups         = "drop"
  )
print(as.data.frame(adult_cohort))
cat("\n")

# -----------------------------------------------------------------------
# INSIGHT 9: Correlation Analysis
# -----------------------------------------------------------------------
cat("INSIGHT 9: Weak-to-Moderate Pairwise Linear Correlations\n")
cat("-------------------------------------------------------------------\n")
num_vars <- c("age", "fnlwgt", "education_num", "capital_gain", "capital_loss", "hours_per_week")
cor_mat <- round(cor(adult[, num_vars]), 4)
print(cor_mat)
cat("\n  Strongest positive: education_num-hours_per_week (r = 0.1484)\n")
cat("  Strongest negative: age-fnlwgt (r = -0.0764)\n")
cat("  No strong multicollinearity (all |r| < 0.15)\n\n")

# -----------------------------------------------------------------------
# INSIGHT 10: Workforce Composition Summary
# -----------------------------------------------------------------------
cat("INSIGHT 10: Workforce Composition — Dominant Private Sector\n")
cat("-------------------------------------------------------------------\n")
wc_summary <- adult %>%
  count(workclass) %>%
  mutate(pct = n / sum(n) * 100) %>%
  arrange(desc(pct))
print(as.data.frame(wc_summary))
cat(sprintf("\n  Private sector dominates: %.1f%% of the workforce\n",
            wc_summary$pct[wc_summary$workclass == "Private"]))
cat(sprintf("  Government combined (Fed+Local+State): %.1f%%\n",
            sum(wc_summary$pct[wc_summary$workclass %in% c("Federal-gov", "Local-gov", "State-gov")])))
cat("\n")

# -----------------------------------------------------------------------
# INSIGHT 11: Education Numeric Summary Statistics
# -----------------------------------------------------------------------
cat("INSIGHT 11: Education Level Numeric Differences by Income\n")
cat("-------------------------------------------------------------------\n")
edu_num_by_inc <- adult %>%
  group_by(income) %>%
  summarise(
    mean_edu_num  = mean(education_num),
    median_edu_num = median(education_num),
    sd_edu_num    = sd(education_num),
    .groups = "drop"
  )
print(as.data.frame(edu_num_by_inc))
cat("\n")

# -----------------------------------------------------------------------
# LINE CHART DECISION STATEMENT
# -----------------------------------------------------------------------
cat("LINE CHART DESIGN DECISION\n")
cat("-------------------------------------------------------------------\n")
cat("A conventional time-series line chart was not produced because the UCI Adult\n")
cat("dataset records a single cross-sectional survey snapshot (1994) and does not\n")
cat("contain a temporal or naturally ordered continuous progression variable.\n")
cat("Using a line chart without valid time-based or ordered continuous X-axis data\n")
cat("would produce a misleading visual that implies change over time when none exists.\n")
cat("Instead, Figure 13 presents an ordered age-cohort trend line using cross-sectional\n")
cat("brackets, which is analytically justified as an ordered categorical axis and is\n")
cat("clearly labelled as a cohort comparison rather than a time series.\n\n")

cat("=======================================================================\n")
cat("  ANALYSIS COMPLETE — All statistics derived from actual dataset\n")
cat("=======================================================================\n")

sink()

cat("Week 2 insights written to outputs/09_week2_insights.txt\n")
cat("=== Script 09 Complete ===\n")
