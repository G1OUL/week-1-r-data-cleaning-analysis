# =============================================================================
# Script 07: Descriptive Statistics, Correlation Analysis & Final Analysis
# Project: Week 1 - Data Cleaning and Preliminary Analysis
# Dataset: UCI Adult/Census Income Dataset
# =============================================================================

library(dplyr)
library(ggplot2)
library(reshape2)
library(corrplot)

cat("=============================================================\n")
cat("  Script 07: Final Analysis\n")
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
adult_raw <- readRDS(file.path(outputs_dir, "adult_raw.rds"))
cat(sprintf("Loaded %d rows x %d columns\n\n", nrow(adult), ncol(adult)))

theme_custom <- theme_minimal(base_size = 13) +
  theme(
    plot.title    = element_text(face = "bold", hjust = 0.5, size = 14),
    axis.title    = element_text(face = "bold"),
    panel.grid.minor = element_blank()
  )

# =============================================================================
# 7.1 DESCRIPTIVE STATISTICS - NUMERICAL VARIABLES
# =============================================================================
cat("--- 7.1 Descriptive Statistics: Numerical Variables ---\n")

num_cols <- c("age", "fnlwgt", "education_num",
              "capital_gain", "capital_loss", "hours_per_week")

desc_stats <- data.frame(
  Variable  = num_cols,
  Mean      = sapply(num_cols, function(c) round(mean(adult[[c]], na.rm=TRUE), 2)),
  Median    = sapply(num_cols, function(c) round(median(adult[[c]], na.rm=TRUE), 2)),
  SD        = sapply(num_cols, function(c) round(sd(adult[[c]], na.rm=TRUE), 2)),
  Min       = sapply(num_cols, function(c) round(min(adult[[c]], na.rm=TRUE), 2)),
  Max       = sapply(num_cols, function(c) round(max(adult[[c]], na.rm=TRUE), 2)),
  Q1        = sapply(num_cols, function(c) round(quantile(adult[[c]], 0.25, na.rm=TRUE), 2)),
  Q3        = sapply(num_cols, function(c) round(quantile(adult[[c]], 0.75, na.rm=TRUE), 2)),
  stringsAsFactors = FALSE
)
print(desc_stats)
write.csv(desc_stats, file.path(outputs_dir, "07_descriptive_stats.csv"), row.names = FALSE)

# =============================================================================
# 7.2 DESCRIPTIVE STATISTICS - CATEGORICAL VARIABLES
# =============================================================================
cat("\n--- 7.2 Descriptive Statistics: Categorical Variables ---\n")

cat_cols_report <- c("workclass", "education", "marital_status",
                     "occupation", "race", "sex", "income")

cat_stats_list <- list()
for (col in cat_cols_report) {
  tbl <- table(adult[[col]])
  pct <- round(100 * prop.table(tbl), 2)
  df  <- data.frame(
    Variable = col,
    Category = names(tbl),
    Count    = as.integer(tbl),
    Pct      = as.numeric(pct),
    stringsAsFactors = FALSE
  )
  cat_stats_list[[col]] <- df
  cat(sprintf("\n%s:\n", col))
  print(df)
}
all_cat_stats <- do.call(rbind, cat_stats_list)
rownames(all_cat_stats) <- NULL
write.csv(all_cat_stats, file.path(outputs_dir, "07_categorical_stats.csv"), row.names = FALSE)

# =============================================================================
# 7.3 CORRELATION ANALYSIS
# =============================================================================
cat("\n--- 7.3 Correlation Analysis ---\n")

num_data <- adult[, num_cols]
cor_matrix <- cor(num_data, use = "complete.obs", method = "pearson")
cat("\nCorrelation Matrix:\n")
print(round(cor_matrix, 4))
write.csv(as.data.frame(cor_matrix), file.path(outputs_dir, "07_correlation_matrix.csv"))

# Fig 14: Correlation heatmap (corrplot)
cat("\nGenerating Figure 14: Correlation heatmap...\n")
png(file.path(plots_dir, "06_fig14_correlation_heatmap.png"),
    width = 800, height = 700, res = 120)
corrplot(cor_matrix,
         method   = "color",
         type     = "upper",
         order    = "hclust",
         addCoef.col = "black",
         tl.col   = "black",
         tl.srt   = 45,
         col      = colorRampPalette(c("#d63031", "white", "#0984e3"))(200),
         title    = "Figure 14. Correlation Matrix of Numerical Variables",
         mar      = c(0, 0, 2, 0))
dev.off()
cat("  Saved: 06_fig14_correlation_heatmap.png\n")

# Fig 15: Education num vs age scatter by income
cat("Generating Figure 15: Education vs Age scatter by income...\n")
set.seed(42)
adult_sample <- adult %>% sample_n(min(3000, nrow(adult)))
p15 <- ggplot(adult_sample, aes(x = education_num, y = age, color = income)) +
  geom_point(alpha = 0.4, size = 1.2) +
  scale_color_manual(values = c("<=50K" = "#00b894", ">50K" = "#d63031")) +
  labs(title = "Figure 15. Education Years vs Age by Income",
       x = "Education (years)", y = "Age", color = "Income") +
  theme_custom
ggsave(file.path(plots_dir, "06_fig15_edu_age_scatter.png"), p15, width = 8, height = 5, dpi = 150)
cat("  Saved: 06_fig15_edu_age_scatter.png\n")

# =============================================================================
# 7.4 BEFORE vs AFTER COMPREHENSIVE SUMMARY
# =============================================================================
cat("\n--- 7.4 Before vs After Cleaning Summary ---\n")

bva_comprehensive <- data.frame(
  Metric = c(
    "Total Rows",
    "Total Columns",
    "Total Missing Values",
    "Missing: workclass",
    "Missing: occupation",
    "Missing: native_country",
    "Duplicate Rows",
    "Numerical Variables",
    "Categorical Variables (factor)",
    "Normalized Variables Added",
    "Dummy Encoded Variables"
  ),
  Before_Cleaning = c(
    nrow(adult_raw),
    ncol(adult_raw),
    sum(is.na(adult_raw)),
    sum(is.na(adult_raw$workclass)),
    sum(is.na(adult_raw$occupation)),
    sum(is.na(adult_raw$native_country)),
    sum(duplicated(adult_raw)),
    6, 8, 0, 0
  ),
  After_Cleaning = c(
    nrow(adult),
    ncol(adult),
    sum(is.na(adult)),
    sum(is.na(adult$workclass)),
    sum(is.na(adult$occupation)),
    sum(is.na(adult$native_country)),
    sum(duplicated(adult)),
    6, 9, 6, 36
  ),
  stringsAsFactors = FALSE
)
print(bva_comprehensive)
write.csv(bva_comprehensive, file.path(outputs_dir, "07_before_after_summary.csv"), row.names = FALSE)

# =============================================================================
# 7.5 SAVE FULL ANALYSIS REPORT
# =============================================================================
sink(file.path(outputs_dir, "07_final_analysis_report.txt"))
cat("FINAL ANALYSIS REPORT\n")
cat("=====================\n\n")
cat("DESCRIPTIVE STATISTICS - NUMERICAL\n")
cat("-----------------------------------\n")
print(desc_stats)
cat("\n\nDESCRIPTIVE STATISTICS - CATEGORICAL\n")
cat("--------------------------------------\n")
for (col in cat_cols_report) {
  cat(sprintf("\n%s:\n", col))
  print(cat_stats_list[[col]])
}
cat("\n\nCORRELATION MATRIX\n")
cat("------------------\n")
print(round(cor_matrix, 4))
cat("\n\nBEFORE vs AFTER CLEANING\n")
cat("------------------------\n")
print(bva_comprehensive)
sink()

cat("\nFinal analysis complete.\n")
cat("=== Script 07 Complete ===\n")
