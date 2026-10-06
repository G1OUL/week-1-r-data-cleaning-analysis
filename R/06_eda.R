# =============================================================================
# Script 06: Exploratory Data Analysis (EDA)
# Project: Week 1 - Data Cleaning and Preliminary Analysis
# Dataset: UCI Adult/Census Income Dataset
# =============================================================================

library(dplyr)
library(ggplot2)
library(tidyr)
library(scales)

cat("=============================================================\n")
cat("  Script 06: Exploratory Data Analysis\n")
cat("=============================================================\n\n")

script_dir   <- tryCatch(dirname(sys.frame(1)), error = function(e) getwd())
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

adult <- readRDS(file.path(outputs_dir, "adult_post_outlier.rds"))
cat(sprintf("Loaded %d rows x %d columns\n\n", nrow(adult), ncol(adult)))

theme_custom <- theme_minimal(base_size = 13) +
  theme(
    plot.title       = element_text(face = "bold", hjust = 0.5, size = 14),
    plot.subtitle    = element_text(hjust = 0.5, color = "grey40"),
    axis.title       = element_text(face = "bold"),
    panel.grid.minor = element_blank()
  )

# --- Fig 1: Missing value visualization ---
cat("Generating Figure 1: Missing value visualization...\n")
adult_raw_local <- readRDS(file.path(outputs_dir, "adult_raw.rds"))
mv_df <- data.frame(
  Variable = names(adult_raw_local),
  Missing  = colSums(is.na(adult_raw_local)),
  Total    = nrow(adult_raw_local)
) %>% mutate(Pct = 100 * Missing / Total) %>% filter(Missing > 0)

if (nrow(mv_df) > 0) {
  p1 <- ggplot(mv_df, aes(x = reorder(Variable, -Pct), y = Pct, fill = Pct)) +
    geom_col(show.legend = FALSE) +
    geom_text(aes(label = sprintf("%.1f%%", Pct)), vjust = -0.4, size = 4) +
    scale_fill_gradient(low = "#f7ca18", high = "#e74c3c") +
    labs(title = "Figure 1. Missing Value Percentage by Variable",
         x = "Variable", y = "Missing (%)") +
    theme_custom
  ggsave(file.path(plots_dir, "06_fig1_missing_values.png"), p1, width = 7, height = 5, dpi = 150)
  cat("  Saved: 06_fig1_missing_values.png\n")
}

# --- Fig 2: Histogram of age ---
cat("Generating Figure 2: Age histogram...\n")
p2 <- ggplot(adult, aes(x = age)) +
  geom_histogram(bins = 30, fill = "#3498db", color = "white", alpha = 0.85) +
  labs(title = "Figure 2. Distribution of Age",
       x = "Age (years)", y = "Count") +
  theme_custom
ggsave(file.path(plots_dir, "06_fig2_age_hist.png"), p2, width = 7, height = 5, dpi = 150)
cat("  Saved: 06_fig2_age_hist.png\n")

# --- Fig 3: Histogram of hours_per_week ---
cat("Generating Figure 3: Hours-per-week histogram...\n")
p3 <- ggplot(adult, aes(x = hours_per_week)) +
  geom_histogram(bins = 30, fill = "#2ecc71", color = "white", alpha = 0.85) +
  labs(title = "Figure 3. Distribution of Hours per Week",
       x = "Hours per Week", y = "Count") +
  theme_custom
ggsave(file.path(plots_dir, "06_fig3_hours_hist.png"), p3, width = 7, height = 5, dpi = 150)
cat("  Saved: 06_fig3_hours_hist.png\n")

# --- Fig 4: Histogram of capital_gain (log scale) ---
cat("Generating Figure 4: Capital gain histogram...\n")
p4 <- ggplot(adult %>% filter(capital_gain > 0), aes(x = capital_gain)) +
  geom_histogram(bins = 30, fill = "#e67e22", color = "white", alpha = 0.85) +
  scale_x_log10(labels = comma) +
  labs(title = "Figure 4. Distribution of Capital Gain (Non-zero, Log Scale)",
       x = "Capital Gain (USD, log scale)", y = "Count") +
  theme_custom
ggsave(file.path(plots_dir, "06_fig4_capgain_hist.png"), p4, width = 7, height = 5, dpi = 150)
cat("  Saved: 06_fig4_capgain_hist.png\n")

# --- Fig 5: Boxplot of key numerical variables ---
cat("Generating Figure 5: Combined boxplots...\n")
num_cols <- c("age", "education_num", "hours_per_week")
adult_long <- adult %>%
  select(all_of(num_cols)) %>%
  pivot_longer(everything(), names_to = "Variable", values_to = "Value")
p5 <- ggplot(adult_long, aes(x = Variable, y = Value, fill = Variable)) +
  geom_boxplot(outlier.color = "#e74c3c", outlier.alpha = 0.4, outlier.size = 0.7) +
  scale_fill_brewer(palette = "Set2") +
  labs(title = "Figure 5. Boxplots of Key Numerical Variables",
       x = "Variable", y = "Value") +
  theme_custom +
  theme(legend.position = "none")
ggsave(file.path(plots_dir, "06_fig5_boxplots_num.png"), p5, width = 8, height = 5, dpi = 150)
cat("  Saved: 06_fig5_boxplots_num.png\n")

# --- Fig 6: Bar chart of education ---
cat("Generating Figure 6: Education bar chart...\n")
edu_counts <- adult %>%
  count(education) %>%
  arrange(desc(n)) %>%
  mutate(education = factor(education, levels = education))
p6 <- ggplot(edu_counts, aes(x = reorder(education, n), y = n, fill = n)) +
  geom_col(show.legend = FALSE) +
  scale_fill_gradient(low = "#74b9ff", high = "#0984e3") +
  coord_flip() +
  labs(title = "Figure 6. Distribution of Education Level",
       x = "Education Level", y = "Count") +
  theme_custom
ggsave(file.path(plots_dir, "06_fig6_education_bar.png"), p6, width = 8, height = 6, dpi = 150)
cat("  Saved: 06_fig6_education_bar.png\n")

# --- Fig 7: Bar chart of occupation ---
cat("Generating Figure 7: Occupation bar chart...\n")
occ_counts <- adult %>% count(occupation) %>% arrange(desc(n))
p7 <- ggplot(occ_counts, aes(x = reorder(occupation, n), y = n, fill = n)) +
  geom_col(show.legend = FALSE) +
  scale_fill_gradient(low = "#a29bfe", high = "#6c5ce7") +
  coord_flip() +
  labs(title = "Figure 7. Distribution of Occupation",
       x = "Occupation", y = "Count") +
  theme_custom
ggsave(file.path(plots_dir, "06_fig7_occupation_bar.png"), p7, width = 8, height = 6, dpi = 150)
cat("  Saved: 06_fig7_occupation_bar.png\n")

# --- Fig 8: Bar chart of marital status ---
cat("Generating Figure 8: Marital status bar chart...\n")
mar_counts <- adult %>% count(marital_status) %>% arrange(desc(n))
p8 <- ggplot(mar_counts, aes(x = reorder(marital_status, n), y = n, fill = n)) +
  geom_col(show.legend = FALSE) +
  scale_fill_gradient(low = "#fd79a8", high = "#e84393") +
  coord_flip() +
  labs(title = "Figure 8. Distribution of Marital Status",
       x = "Marital Status", y = "Count") +
  theme_custom
ggsave(file.path(plots_dir, "06_fig8_marital_bar.png"), p8, width = 8, height = 5, dpi = 150)
cat("  Saved: 06_fig8_marital_bar.png\n")

# --- Fig 9: Bar chart of income groups ---
cat("Generating Figure 9: Income distribution...\n")
inc_counts <- adult %>% count(income) %>% mutate(Pct = 100*n/sum(n))
p9 <- ggplot(inc_counts, aes(x = income, y = n, fill = income)) +
  geom_col(show.legend = FALSE, width = 0.5) +
  geom_text(aes(label = sprintf("%d\n(%.1f%%)", n, Pct)), vjust = -0.3, fontface = "bold") +
  scale_fill_manual(values = c("<=50K" = "#00b894", ">50K" = "#d63031")) +
  labs(title = "Figure 9. Distribution of Income Groups",
       x = "Income", y = "Count") +
  theme_custom
ggsave(file.path(plots_dir, "06_fig9_income_bar.png"), p9, width = 6, height = 5, dpi = 150)
cat("  Saved: 06_fig9_income_bar.png\n")

# --- Fig 10: Scatter plot age vs hours_per_week by income ---
cat("Generating Figure 10: Scatter plot...\n")
set.seed(42)
adult_sample <- adult %>% sample_n(min(3000, nrow(adult)))
p10 <- ggplot(adult_sample, aes(x = age, y = hours_per_week, color = income)) +
  geom_point(alpha = 0.4, size = 1.2) +
  scale_color_manual(values = c("<=50K" = "#00b894", ">50K" = "#d63031")) +
  labs(title = "Figure 10. Age vs Hours per Week by Income",
       x = "Age (years)", y = "Hours per Week", color = "Income") +
  theme_custom
ggsave(file.path(plots_dir, "06_fig10_scatter_age_hours.png"), p10, width = 8, height = 5, dpi = 150)
cat("  Saved: 06_fig10_scatter_age_hours.png\n")

# --- Fig 11: Comparison - age by income group ---
cat("Generating Figure 11: Age by income group...\n")
p11 <- ggplot(adult, aes(x = income, y = age, fill = income)) +
  geom_violin(alpha = 0.7, trim = FALSE) +
  geom_boxplot(width = 0.12, fill = "white", outlier.size = 0.5, alpha = 0.8) +
  scale_fill_manual(values = c("<=50K" = "#00b894", ">50K" = "#d63031")) +
  labs(title = "Figure 11. Age Distribution by Income Group",
       x = "Income", y = "Age (years)", fill = "Income") +
  theme_custom + theme(legend.position = "none")
ggsave(file.path(plots_dir, "06_fig11_age_by_income.png"), p11, width = 6, height = 6, dpi = 150)
cat("  Saved: 06_fig11_age_by_income.png\n")

# --- Fig 12: Hours per week by income ---
cat("Generating Figure 12: Hours by income...\n")
p12 <- ggplot(adult, aes(x = income, y = hours_per_week, fill = income)) +
  geom_violin(alpha = 0.7, trim = FALSE) +
  geom_boxplot(width = 0.12, fill = "white", outlier.size = 0.5, alpha = 0.8) +
  scale_fill_manual(values = c("<=50K" = "#00b894", ">50K" = "#d63031")) +
  labs(title = "Figure 12. Hours per Week by Income Group",
       x = "Income", y = "Hours per Week", fill = "Income") +
  theme_custom + theme(legend.position = "none")
ggsave(file.path(plots_dir, "06_fig12_hours_by_income.png"), p12, width = 6, height = 6, dpi = 150)
cat("  Saved: 06_fig12_hours_by_income.png\n")

# --- Fig 13: education_num by income ---
cat("Generating Figure 13: Education years by income...\n")
p13 <- ggplot(adult, aes(x = income, y = education_num, fill = income)) +
  geom_violin(alpha = 0.7, trim = FALSE) +
  geom_boxplot(width = 0.12, fill = "white", outlier.size = 0.5, alpha = 0.8) +
  scale_fill_manual(values = c("<=50K" = "#00b894", ">50K" = "#d63031")) +
  labs(title = "Figure 13. Education Years by Income Group",
       x = "Income", y = "Education (years)", fill = "Income") +
  theme_custom + theme(legend.position = "none")
ggsave(file.path(plots_dir, "06_fig13_education_by_income.png"), p13, width = 6, height = 6, dpi = 150)
cat("  Saved: 06_fig13_education_by_income.png\n")

cat("\nEDA complete. All figures saved.\n")
cat("=== Script 06 Complete ===\n")
