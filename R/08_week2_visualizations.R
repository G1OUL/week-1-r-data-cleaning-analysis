# =============================================================================
# Script 08: Week 2 Visualizations — Data Visualization & Insight Communication
# Project: Week 2 - Data Visualization and Insight Communication using R
# Dataset: UCI Adult/Census Income Dataset (Cleaned from Week 1)
# =============================================================================

suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
  library(tidyr)
  library(scales)
  library(corrplot)
  library(reshape2)
})

cat("=============================================================\n")
cat("  Script 08: Week 2 Visualizations (ggplot2)\n")
cat("=============================================================\n\n")

# 1. SETUP PATHS (Relative paths only)
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
data_dir     <- file.path(project_root, "data", "cleaned")

dir.create(plots_dir, showWarnings = FALSE, recursive = TRUE)
dir.create(outputs_dir, showWarnings = FALSE, recursive = TRUE)

# Load cleaned dataset from Week 1
rds_path <- file.path(outputs_dir, "adult_cleaned.rds")
csv_path <- file.path(data_dir, "adult_cleaned.csv")

if (file.exists(rds_path)) {
  adult <- readRDS(rds_path)
} else if (file.exists(csv_path)) {
  adult <- read.csv(csv_path, stringsAsFactors = TRUE)
} else {
  stop("Cleaned dataset not found in outputs/ or data/cleaned/")
}

cat(sprintf("Loaded cleaned dataset: %d rows x %d columns\n\n", nrow(adult), ncol(adult)))

# Standardized publication theme
theme_academic <- theme_minimal(base_size = 12) +
  theme(
    plot.title         = element_text(face = "bold", size = 14, color = "#1B365D", hjust = 0),
    plot.subtitle      = element_text(size = 10.5, color = "#465C7A", margin = margin(b = 10)),
    plot.caption       = element_text(size = 8.5, color = "#6C757D", hjust = 1, margin = margin(t = 8)),
    axis.title.x       = element_text(face = "bold", size = 11, color = "#212529", margin = margin(t = 8)),
    axis.title.y       = element_text(face = "bold", size = 11, color = "#212529", margin = margin(r = 8)),
    axis.text          = element_text(size = 10, color = "#212529"),
    panel.grid.major.x = element_line(color = "#E9ECEF", linewidth = 0.5),
    panel.grid.major.y = element_line(color = "#E9ECEF", linewidth = 0.5),
    panel.grid.minor   = element_blank(),
    legend.position    = "bottom",
    legend.title       = element_text(face = "bold", size = 10, color = "#1B365D"),
    legend.text        = element_text(size = 9.5),
    legend.background  = element_rect(fill = "#FAFAFA", color = NA),
    plot.background    = element_rect(fill = "white", color = NA),
    panel.background   = element_rect(fill = "white", color = NA)
  )

# Colors
col_low  <- "#2B5C8F"  # Navy for <=50K
col_high <- "#D9534F"  # Coral Red for >50K

# -----------------------------------------------------------------------------
# VISUALIZATION 1: Income Distribution (Bar Chart)
# -----------------------------------------------------------------------------
cat("1. Generating week2_01_income_distribution.png...\n")
df_inc <- adult %>%
  count(income) %>%
  mutate(
    pct = n / sum(n) * 100,
    label = sprintf("%s\n(%.1f%%)", format(n, big.mark = ","), pct)
  )

p1 <- ggplot(df_inc, aes(x = income, y = n, fill = income)) +
  geom_col(width = 0.52, show.legend = FALSE, color = "#1B365D", linewidth = 0.3) +
  geom_text(aes(label = label), vjust = -0.3, fontface = "bold", size = 4.2, color = "#212529") +
  scale_fill_manual(values = c("<=50K" = col_low, ">50K" = col_high)) +
  scale_y_continuous(labels = comma, limits = c(0, 28000), expand = expansion(mult = c(0, 0.08))) +
  labs(
    title = "Figure 1. Distribution of Annual Income Thresholds",
    subtitle = "Severe class imbalance: 75.9% of survey respondents earn <=$50,000 annually",
    x = "Annual Income Category",
    y = "Number of Individuals",
    caption = "Source: UCI Adult Dataset (1994 US Census Bureau CPS) | N = 32,537"
  ) +
  theme_academic

ggsave(file.path(plots_dir, "week2_01_income_distribution.png"), p1, width = 7.5, height = 5.2, dpi = 300)

# -----------------------------------------------------------------------------
# VISUALIZATION 2: Age Distribution (Histogram)
# -----------------------------------------------------------------------------
cat("2. Generating week2_02_age_distribution.png...\n")
age_median <- median(adult$age)
age_mean   <- mean(adult$age)

p2 <- ggplot(adult, aes(x = age)) +
  geom_histogram(binwidth = 2, fill = "#3498DB", color = "white", linewidth = 0.3, alpha = 0.85) +
  geom_vline(xintercept = age_median, color = "#C0392B", linetype = "dashed", linewidth = 1) +
  annotate("text", x = age_median + 2, y = 2400, label = sprintf("Median: %d yrs\nMean: %.1f yrs", age_median, age_mean),
           color = "#C0392B", fontface = "bold", hjust = 0, size = 3.8) +
  scale_x_continuous(breaks = seq(15, 90, 10)) +
  scale_y_continuous(labels = comma, expand = expansion(mult = c(0, 0.05))) +
  labs(
    title = "Figure 2. Distribution of Worker Age",
    subtitle = "Right-skewed unimodal distribution concentrated between ages 25 and 45 (IQR: 28–48)",
    x = "Age (Years)",
    y = "Count of Observations",
    caption = "Source: UCI Adult Dataset | N = 32,537 | Skewness = +0.56"
  ) +
  theme_academic

ggsave(file.path(plots_dir, "week2_02_age_distribution.png"), p2, width = 8, height = 5.2, dpi = 300)

# -----------------------------------------------------------------------------
# VISUALIZATION 3: Education Distribution (Horizontal Bar Chart)
# -----------------------------------------------------------------------------
cat("3. Generating week2_03_education_distribution.png...\n")
df_edu <- adult %>%
  count(education, education_num) %>%
  arrange(education_num) %>%
  mutate(
    pct = n / sum(n) * 100,
    education = factor(education, levels = education)
  )

p3 <- ggplot(df_edu, aes(x = education, y = n, fill = education_num)) +
  geom_col(width = 0.72, show.legend = FALSE) +
  geom_text(aes(label = sprintf("%s (%.1f%%)", format(n, big.mark = ","), pct)),
            hjust = -0.1, size = 3.5, color = "#212529") +
  scale_fill_gradient(low = "#85C1E9", high = "#1B4F72") +
  scale_y_continuous(labels = comma, limits = c(0, 12500), expand = expansion(mult = c(0, 0.12))) +
  coord_flip() +
  labs(
    title = "Figure 3. Distribution of Highest Educational Attainment",
    subtitle = "Workforce qualification hierarchy: HS-grad (32.3%) and Some-college (22.4%) dominate",
    x = "Educational Qualification (Ascending Level)",
    y = "Number of Individuals",
    caption = "Source: UCI Adult Dataset | N = 32,537 | Ordered by years of education"
  ) +
  theme_academic

ggsave(file.path(plots_dir, "week2_03_education_distribution.png"), p3, width = 8.5, height = 6.2, dpi = 300)

# -----------------------------------------------------------------------------
# VISUALIZATION 4: Education vs Income (Proportional Stacked Bar Chart)
# -----------------------------------------------------------------------------
cat("4. Generating week2_04_education_vs_income.png...\n")
df_edu_inc <- adult %>%
  group_by(education, education_num, income) %>%
  summarise(n = n(), .groups = "drop") %>%
  group_by(education) %>%
  mutate(
    total = sum(n),
    pct   = n / total * 100
  ) %>%
  ungroup() %>%
  arrange(education_num) %>%
  mutate(education = factor(education, levels = unique(education)))

df_labels_edu <- df_edu_inc %>%
  filter(income == ">50K")

p4 <- ggplot(df_edu_inc, aes(x = education, y = pct, fill = income)) +
  geom_col(position = "fill", width = 0.72) +
  geom_text(data = df_labels_edu,
            aes(x = education, y = 1 - (pct / 200), label = sprintf("%.1f%%", pct)),
            color = "white", fontface = "bold", size = 3.4) +
  scale_y_continuous(labels = percent_format(accuracy = 1), expand = expansion(mult = c(0, 0))) +
  scale_fill_manual(values = c("<=50K" = col_low, ">50K" = col_high), name = "Income Group:") +
  coord_flip() +
  labs(
    title = "Figure 4. Proportional Income Distribution by Educational Attainment",
    subtitle = "Monotonic positive association: High-income proportion escalates from 0% (Preschool) to 74.1% (Doctorate)",
    x = "Educational Level (Ascending Hierarchy)",
    y = "Observed Proportion within Category",
    caption = "Source: UCI Adult Dataset | N = 32,537 | White labels display observed % earning >$50K"
  ) +
  theme_academic +
  theme(legend.position = "top")

ggsave(file.path(plots_dir, "week2_04_education_vs_income.png"), p4, width = 8.8, height = 6.4, dpi = 300)

# -----------------------------------------------------------------------------
# VISUALIZATION 5: Workclass vs Income (Proportional Stacked Bar Chart)
# -----------------------------------------------------------------------------
cat("5. Generating week2_05_workclass_vs_income.png...\n")
df_wc_inc <- adult %>%
  group_by(workclass, income) %>%
  summarise(n = n(), .groups = "drop") %>%
  group_by(workclass) %>%
  mutate(
    total = sum(n),
    pct   = n / total * 100
  ) %>%
  ungroup()

# Order workclass by >50K percentage
wc_order <- df_wc_inc %>%
  filter(income == ">50K") %>%
  arrange(pct) %>%
  pull(workclass)
# Add any workclasses with 0% >50K
wc_zero <- setdiff(unique(adult$workclass), wc_order)
wc_levels <- c(as.character(wc_zero), as.character(wc_order))

df_wc_inc <- df_wc_inc %>%
  mutate(workclass = factor(workclass, levels = wc_levels))

df_labels_wc <- df_wc_inc %>%
  filter(income == ">50K", pct > 2)

p5 <- ggplot(df_wc_inc, aes(x = workclass, y = pct, fill = income)) +
  geom_col(position = "fill", width = 0.7) +
  geom_text(data = df_labels_wc,
            aes(x = workclass, y = 1 - (pct / 200), label = sprintf("%.1f%%", pct)),
            color = "white", fontface = "bold", size = 3.5) +
  scale_y_continuous(labels = percent_format(accuracy = 1), expand = expansion(mult = c(0, 0))) +
  scale_fill_manual(values = c("<=50K" = col_low, ">50K" = col_high), name = "Income Category:") +
  coord_flip() +
  labs(
    title = "Figure 5. Proportional Income Distribution Across Workclass Sectors",
    subtitle = "Self-Employed Incorporated (55.7%) and Federal Government (38.7%) display highest high-income rates",
    x = "Employment Sector (Workclass)",
    y = "Observed Proportion within Workclass",
    caption = "Source: UCI Adult Dataset | N = 32,537 | Sorted by observed % earning >$50K"
  ) +
  theme_academic +
  theme(legend.position = "top")

ggsave(file.path(plots_dir, "week2_05_workclass_vs_income.png"), p5, width = 8.5, height = 5.8, dpi = 300)

# -----------------------------------------------------------------------------
# VISUALIZATION 6: Age vs Income (Hybrid Violin + Boxplot)
# -----------------------------------------------------------------------------
cat("6. Generating week2_06_age_vs_income.png...\n")
age_stats <- adult %>%
  group_by(income) %>%
  summarise(
    q1 = quantile(age, 0.25),
    med = median(age),
    q3 = quantile(age, 0.75),
    mean = mean(age),
    .groups = "drop"
  )

p6 <- ggplot(adult, aes(x = income, y = age, fill = income)) +
  geom_violin(alpha = 0.5, trim = FALSE, color = "#2C3E50", linewidth = 0.4) +
  geom_boxplot(width = 0.18, fill = "white", color = "#1B365D", outlier.size = 0.8, outlier.alpha = 0.3) +
  stat_summary(fun = mean, geom = "point", shape = 23, size = 3.5, fill = "#F39C12", color = "#1B365D") +
  annotate("text", x = 1, y = 88, label = sprintf("Median: %d | IQR: [%d, %d]\nMean: %.1f yrs",
                                                   age_stats$med[1], age_stats$q1[1], age_stats$q3[1], age_stats$mean[1]),
           size = 3.8, fontface = "bold", color = col_low) +
  annotate("text", x = 2, y = 88, label = sprintf("Median: %d | IQR: [%d, %d]\nMean: %.1f yrs",
                                                   age_stats$med[2], age_stats$q1[2], age_stats$q3[2], age_stats$mean[2]),
           size = 3.8, fontface = "bold", color = col_high) +
  scale_fill_manual(values = c("<=50K" = col_low, ">50K" = col_high), guide = "none") +
  scale_y_continuous(breaks = seq(10, 90, 10)) +
  labs(
    title = "Figure 6. Age Distribution Contrasted by Income Group",
    subtitle = "Higher earners exhibit a substantially older demographic profile (Median: 44 vs 34 yrs; +10 year shift)",
    x = "Annual Income Group",
    y = "Age (Years)",
    caption = "Source: UCI Adult Dataset | Orange diamonds denote group means; center line denotes median"
  ) +
  theme_academic

ggsave(file.path(plots_dir, "week2_06_age_vs_income.png"), p6, width = 7.5, height = 5.8, dpi = 300)

# -----------------------------------------------------------------------------
# VISUALIZATION 7: Hours per Week Distribution (Histogram)
# -----------------------------------------------------------------------------
cat("7. Generating week2_07_hours_distribution.png...\n")
exact_40_pct <- mean(adult$hours_per_week == 40) * 100

p7 <- ggplot(adult, aes(x = hours_per_week)) +
  geom_histogram(binwidth = 2, fill = "#16A085", color = "white", linewidth = 0.3, alpha = 0.85) +
  geom_vline(xintercept = 40, color = "#C0392B", linetype = "dashed", linewidth = 1) +
  annotate("rect", xmin = 38, xmax = 42, ymin = 0, ymax = 16000, alpha = 0.15, fill = "#E74C3C") +
  annotate("text", x = 44, y = 14500, label = sprintf("Modal Spike at 40 Hours/Week\n%s workers (%.1f%% of sample)",
                                                      format(sum(adult$hours_per_week == 40), big.mark = ","), exact_40_pct),
           color = "#C0392B", fontface = "bold", hjust = 0, size = 3.8) +
  scale_x_continuous(breaks = seq(0, 100, 10)) +
  scale_y_continuous(labels = comma, expand = expansion(mult = c(0, 0.05))) +
  labs(
    title = "Figure 7. Distribution of Weekly Working Hours",
    subtitle = "Pronounced institutional clustering at the statutory 40-hour full-time workweek (46.7% of total workforce)",
    x = "Hours Worked per Week",
    y = "Number of Observations",
    caption = "Source: UCI Adult Dataset | N = 32,537 | Range: 1 to 99 hours/week"
  ) +
  theme_academic

ggsave(file.path(plots_dir, "week2_07_hours_distribution.png"), p7, width = 8, height = 5.2, dpi = 300)

# -----------------------------------------------------------------------------
# VISUALIZATION 8: Hours per Week vs Income (Comparative Violin + Boxplot)
# -----------------------------------------------------------------------------
cat("8. Generating week2_08_hours_vs_income.png...\n")
hours_stats <- adult %>%
  group_by(income) %>%
  summarise(
    q1 = quantile(hours_per_week, 0.25),
    med = median(hours_per_week),
    q3 = quantile(hours_per_week, 0.75),
    mean = mean(hours_per_week),
    .groups = "drop"
  )

p8 <- ggplot(adult, aes(x = income, y = hours_per_week, fill = income)) +
  geom_violin(alpha = 0.5, trim = FALSE, color = "#2C3E50", linewidth = 0.4) +
  geom_boxplot(width = 0.18, fill = "white", color = "#1B365D", outlier.size = 0.8, outlier.alpha = 0.3) +
  stat_summary(fun = mean, geom = "point", shape = 23, size = 3.5, fill = "#F39C12", color = "#1B365D") +
  annotate("text", x = 1, y = 96, label = sprintf("Median: %d | IQR: [%d, %d]\nMean: %.1f hrs/wk",
                                                   hours_stats$med[1], hours_stats$q1[1], hours_stats$q3[1], hours_stats$mean[1]),
           size = 3.8, fontface = "bold", color = col_low) +
  annotate("text", x = 2, y = 96, label = sprintf("Median: %d | IQR: [%d, %d]\nMean: %.1f hrs/wk",
                                                   hours_stats$med[2], hours_stats$q1[2], hours_stats$q3[2], hours_stats$mean[2]),
           size = 3.8, fontface = "bold", color = col_high) +
  scale_fill_manual(values = c("<=50K" = col_low, ">50K" = col_high), guide = "none") +
  scale_y_continuous(breaks = seq(0, 100, 10)) +
  labs(
    title = "Figure 8. Weekly Hours Worked Compared Between Income Categories",
    subtitle = "Higher earners work substantially longer schedules on average (Mean: 45.5 vs 38.8 hrs; Q3 extends to 50 hrs)",
    x = "Annual Income Group",
    y = "Hours Worked per Week",
    caption = "Source: UCI Adult Dataset | Orange diamonds represent category means"
  ) +
  theme_academic

ggsave(file.path(plots_dir, "week2_08_hours_vs_income.png"), p8, width = 7.5, height = 5.8, dpi = 300)

# -----------------------------------------------------------------------------
# VISUALIZATION 9: Age vs Hours per Week (Scatter Plot)
# -----------------------------------------------------------------------------
cat("9. Generating week2_09_age_vs_hours_scatter.png...\n")
set.seed(42)
adult_sample <- adult %>% sample_n(min(4000, nrow(adult)))

p9 <- ggplot(adult_sample, aes(x = age, y = hours_per_week, color = income)) +
  geom_point(alpha = 0.35, size = 1.3) +
  geom_smooth(method = "loess", se = TRUE, linewidth = 1.1) +
  scale_color_manual(values = c("<=50K" = col_low, ">50K" = col_high), name = "Income Group:") +
  scale_x_continuous(breaks = seq(15, 90, 10)) +
  scale_y_continuous(breaks = seq(0, 100, 20)) +
  labs(
    title = "Figure 9. Bivariate Relationship: Worker Age vs Weekly Working Hours",
    subtitle = "Heavy horizontal concentration along 40 hrs; >$50K individuals sustain higher weekly hours across prime career ages (35–55)",
    x = "Age (Years)",
    y = "Hours Worked per Week",
    caption = "Source: UCI Adult Dataset | Random sample n = 4,000 for visual clarity | Loess trend lines overlaid"
  ) +
  theme_academic +
  theme(legend.position = "top")

ggsave(file.path(plots_dir, "week2_09_age_vs_hours_scatter.png"), p9, width = 8.5, height = 5.8, dpi = 300)

# -----------------------------------------------------------------------------
# VISUALIZATION 10: Capital Gain Distribution (Log-Scale & Zero Handling)
# -----------------------------------------------------------------------------
cat("10. Generating week2_10_capital_gain_distribution.png...\n")
cg_nonzero <- adult %>% filter(capital_gain > 0)
zero_count <- sum(adult$capital_gain == 0)
zero_pct   <- mean(adult$capital_gain == 0) * 100
nonzero_count <- nrow(cg_nonzero)
nonzero_pct   <- 100 - zero_pct
cap_max_count <- sum(adult$capital_gain == 99999)

p10 <- ggplot(cg_nonzero, aes(x = capital_gain)) +
  geom_histogram(bins = 35, fill = "#E67E22", color = "white", linewidth = 0.3, alpha = 0.85) +
  geom_vline(xintercept = median(cg_nonzero$capital_gain), color = "#900C3F", linetype = "dashed", linewidth = 1) +
  geom_vline(xintercept = 99999, color = "#C0392B", linetype = "dotted", linewidth = 1) +
  scale_x_log10(labels = dollar_format()) +
  annotate("text", x = 150, y = 250,
           label = sprintf("Zero-Value Foundation:\n- %s individuals (%.1f%%) report $0 gain\n- Only %s (%.1f%%) report positive gain\n- Non-Zero Median: $%s\n- Top-Code Ceiling: 159 hit $99,999",
                           format(zero_count, big.mark = ","), zero_pct,
                           format(nonzero_count, big.mark = ","), nonzero_pct,
                           format(median(cg_nonzero$capital_gain), big.mark = ",")),
           hjust = 0, size = 3.7, fontface = "bold", color = "#1B365D",
           bbox = list(boxstyle = "round,pad=0.5", fc = "#F8F9FA", ec = "#CED4DA")) +
  labs(
    title = "Figure 10. Distribution of Positive Capital Gains (Log10 Scale)",
    subtitle = "Zero values (91.7% of population) isolated; positive gains span 3 orders of magnitude with $99,999 top-code spike",
    x = "Capital Gain (USD, Log10 Scale)",
    y = "Count of Positive Observations",
    caption = "Source: UCI Adult Dataset | N_positive = 2,712 | Excludes 29,825 zero-gain records to enable valid log transform"
  ) +
  theme_academic

ggsave(file.path(plots_dir, "week2_10_capital_gain_distribution.png"), p10, width = 8.5, height = 5.8, dpi = 300)

# -----------------------------------------------------------------------------
# VISUALIZATION 11: Correlation Heatmap
# -----------------------------------------------------------------------------
cat("11. Generating week2_11_correlation_heatmap.png...\n")
num_cols <- c("age", "fnlwgt", "education_num", "capital_gain", "capital_loss", "hours_per_week")
clean_labels <- c("Age", "Sample Weight\n(fnlwgt)", "Education Years\n(num)", "Capital Gain", "Capital Loss", "Hours / Week")

cor_mat <- cor(adult[, num_cols])
colnames(cor_mat) <- clean_labels
rownames(cor_mat) <- clean_labels

cor_melted <- melt(cor_mat)

p11 <- ggplot(cor_melted, aes(x = Var1, y = Var2, fill = value)) +
  geom_tile(color = "white", linewidth = 0.8) +
  geom_text(aes(label = sprintf("%.3f", value)), size = 3.8, fontface = "bold",
            color = ifelse(abs(cor_melted$value) > 0.45, "white", "#212529")) +
  scale_fill_gradient2(low = "#2980B9", mid = "#FFFFFF", high = "#C0392B",
                       midpoint = 0, limit = c(-1, 1), name = "Pearson Correlation (r)") +
  labs(
    title = "Figure 11. Pearson Correlation Matrix of Continuous Census Features",
    subtitle = "Weak-to-moderate pairwise linear associations (|r| <= 0.148); sampling weight has virtually zero collinearity",
    x = "", y = "",
    caption = "CAUTION: Correlation measures linear statistical association; it does NOT demonstrate causal mechanisms."
  ) +
  theme_academic +
  theme(
    axis.text.x = element_text(angle = 30, hjust = 1, face = "bold"),
    axis.text.y = element_text(face = "bold"),
    legend.position = "right",
    legend.key.height = unit(1.5, "cm")
  )

ggsave(file.path(plots_dir, "week2_11_correlation_heatmap.png"), p11, width = 8, height = 6.2, dpi = 300)

# -----------------------------------------------------------------------------
# VISUALIZATION 12: Creative Visualization (Occupation vs Income Proportions)
# -----------------------------------------------------------------------------
cat("12. Generating week2_12_occupation_vs_income.png...\n")
df_occ_inc <- adult %>%
  group_by(occupation, income) %>%
  summarise(n = n(), .groups = "drop") %>%
  group_by(occupation) %>%
  mutate(
    total = sum(n),
    pct   = n / total * 100
  ) %>%
  ungroup()

# Order occupation by >50K percentage
occ_order <- df_occ_inc %>%
  filter(income == ">50K") %>%
  arrange(pct) %>%
  pull(occupation)

df_occ_inc <- df_occ_inc %>%
  mutate(occupation = factor(occupation, levels = occ_order))

df_labels_occ <- df_occ_inc %>%
  filter(income == ">50K")

p12 <- ggplot(df_occ_inc, aes(x = occupation, y = pct, fill = income)) +
  geom_col(position = "fill", width = 0.72) +
  geom_text(data = df_labels_occ,
            aes(x = occupation, y = 1 - (pct / 200), label = sprintf("%.1f%%", pct)),
            color = "white", fontface = "bold", size = 3.3) +
  scale_y_continuous(labels = percent_format(accuracy = 1), expand = expansion(mult = c(0, 0))) +
  scale_fill_manual(values = c("<=50K" = col_low, ">50K" = col_high), name = "Income Category:") +
  coord_flip() +
  labs(
    title = "Figure 12. Creative Visualization: Proportional Income Disparity Across Occupations",
    subtitle = "Sharp economic cleavage: Executive-Managerial (48.4%) and Professional-Specialty (34.3%) vs Service Roles (<5%)",
    x = "Occupational Category",
    y = "Observed Proportion within Occupation",
    caption = "Source: UCI Adult Dataset | N = 32,537 | White labels display % earning >$50,000"
  ) +
  theme_academic +
  theme(legend.position = "top")

ggsave(file.path(plots_dir, "week2_12_occupation_vs_income.png"), p12, width = 9, height = 6.4, dpi = 300)

# -----------------------------------------------------------------------------
# SUPPLEMENTARY VISUALIZATION 13: Age Cohort Profile (Line Chart Decision Context)
# -----------------------------------------------------------------------------
cat("13. Generating week2_13_age_cohort_income_trend.png...\n")
adult_cohort <- adult %>%
  mutate(
    age_cohort = cut(
      age,
      breaks = c(16, 25, 35, 45, 55, 65, 100),
      labels = c("17–25", "26–35", "36–45", "46–55", "56–65", "66+"),
      right = TRUE
    )
  ) %>%
  group_by(age_cohort) %>%
  summarise(
    n = n(),
    pct_high_income = mean(income == ">50K") * 100,
    mean_hours = mean(hours_per_week),
    .groups = "drop"
  )

p13 <- ggplot(adult_cohort, aes(x = age_cohort, y = pct_high_income, group = 1)) +
  geom_line(color = "#1B365D", linewidth = 1.3) +
  geom_point(color = "#D9534F", size = 4) +
  geom_text(aes(label = sprintf("%.1f%%", pct_high_income)), vjust = -0.9, fontface = "bold", size = 3.8) +
  scale_y_continuous(limits = c(0, 48), labels = function(x) paste0(x, "%")) +
  labs(
    title = "Figure 13. Life-Cycle Cohort Trend: High-Income Rate Across Age Brackets",
    subtitle = "Analytical demonstration: Inverted U-curve peaking in the 46–55 cohort (40.0%), declining in retirement ages (66+)",
    x = "Cross-Sectional Age Cohort (Lifespan Bracket)",
    y = "Proportion Earning >$50,000 (%)",
    caption = "NOTE: Represents synthetic cross-sectional age cohorts, NOT a longitudinal time-series."
  ) +
  theme_academic

ggsave(file.path(plots_dir, "week2_13_age_cohort_income_trend.png"), p13, width = 8, height = 5.2, dpi = 300)

cat("\nAll 13 Week 2 visualizations generated successfully and saved to plots/\n")
cat("=== Script 08 Complete ===\n")
