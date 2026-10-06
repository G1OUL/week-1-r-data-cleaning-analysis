# =============================================================================
# Script 04: Outlier Detection and Treatment
# Project: Week 1 – Data Cleaning and Preliminary Analysis
# Dataset: UCI Adult/Census Income Dataset
# =============================================================================

library(dplyr)
library(ggplot2)

cat("=============================================================\n")
cat("  Script 04: Outlier Detection & Treatment\n")
cat("=============================================================\n\n")

# Paths
script_dir   <- tryCatch(dirname(sys.frame(1)$ofile), error = function(e) getwd())
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

# Load cleaned data
adult <- readRDS(file.path(outputs_dir, "adult_cleaned.rds"))
cat(sprintf("Loaded %d rows × %d columns\n\n", nrow(adult), ncol(adult)))

# Numerical columns to analyse
num_cols <- c("age", "fnlwgt", "education_num",
              "capital_gain", "capital_loss", "hours_per_week")

# =============================================================================
# 4.1 IQR-BASED OUTLIER DETECTION
# =============================================================================
cat("--- 4.1 IQR Outlier Analysis ---\n\n")

outlier_summary <- data.frame()

for (col in num_cols) {
  x    <- adult[[col]]
  q1   <- quantile(x, 0.25, na.rm = TRUE)
  q3   <- quantile(x, 0.75, na.rm = TRUE)
  iqr  <- q3 - q1
  lb   <- q1 - 1.5 * iqr
  ub   <- q3 + 1.5 * iqr
  n_out <- sum(x < lb | x > ub, na.rm = TRUE)
  pct_out <- round(100 * n_out / length(x), 2)

  cat(sprintf("%-20s : Q1=%.2f  Q3=%.2f  IQR=%.2f  LB=%.2f  UB=%.2f  Outliers=%d (%.2f%%)\n",
              col, q1, q3, iqr, lb, ub, n_out, pct_out))

  outlier_summary <- rbind(outlier_summary, data.frame(
    Variable     = col,
    Q1           = round(q1, 2),
    Q3           = round(q3, 2),
    IQR          = round(iqr, 2),
    Lower_Bound  = round(lb, 2),
    Upper_Bound  = round(ub, 2),
    N_Outliers   = n_out,
    Pct_Outliers = pct_out,
    stringsAsFactors = FALSE
  ))
}

print(outlier_summary)

# =============================================================================
# 4.2 BOXPLOTS — one per variable
# =============================================================================
cat("\n--- 4.2 Generating Boxplots ---\n")

for (col in num_cols) {
  p <- ggplot(adult, aes_string(y = col)) +
    geom_boxplot(fill = "#4e79a7", color = "#2c3e50", outlier.color = "#e74c3c",
                 outlier.alpha = 0.5, width = 0.4) +
    labs(
      title = paste("Figure: Boxplot of", col),
      y     = col,
      x     = ""
    ) +
    theme_minimal(base_size = 13) +
    theme(
      plot.title   = element_text(face = "bold", hjust = 0.5),
      axis.text.x  = element_blank(),
      axis.ticks.x = element_blank()
    )
  fname <- file.path(plots_dir, paste0("04_boxplot_", col, ".png"))
  ggsave(fname, p, width = 5, height = 6, dpi = 150)
  cat(sprintf("  Saved: %s\n", fname))
}

# Combined boxplot for the six numeric variables (scaled)
adult_long <- tidyr::pivot_longer(
  adult[ , num_cols],
  cols      = everything(),
  names_to  = "Variable",
  values_to = "Value"
)

p_combined <- ggplot(adult_long, aes(x = Variable, y = Value, fill = Variable)) +
  geom_boxplot(outlier.color = "#e74c3c", outlier.alpha = 0.3, outlier.size = 0.8) +
  labs(
    title = "Figure 4. Boxplots of Numerical Variables",
    x     = "Variable",
    y     = "Value"
  ) +
  theme_minimal(base_size = 12) +
  theme(
    plot.title  = element_text(face = "bold", hjust = 0.5),
    legend.position = "none",
    axis.text.x = element_text(angle = 30, hjust = 1)
  ) +
  scale_fill_brewer(palette = "Set2")

ggsave(file.path(plots_dir, "04_boxplots_combined.png"), p_combined,
       width = 10, height = 6, dpi = 150)
cat("  Saved: 04_boxplots_combined.png\n")

# =============================================================================
# 4.3 OUTLIER TREATMENT DECISION
# =============================================================================
cat("\n--- 4.3 Outlier Treatment Decisions ---\n")

# capital_gain / capital_loss:
#   Many individuals legitimately have zero capital gain/loss.
#   The high values are real financial events (stock sales, property).
#   Decision: RETAIN – these are genuine observations, not data errors.
#
# fnlwgt:
#   This is a census sampling weight; extreme values reflect underrepresented
#   subpopulations. Decision: RETAIN.
#
# age / hours_per_week / education_num:
#   IQR outliers are plausible real-world values (e.g., working 99 h/week
#   is unusual but possible, or someone studying for 16 years).
#   Decision: RETAIN — no invalid values detected.
#
# CONCLUSION: No observations are removed based on outlier detection.
# The extreme values appear to represent genuine population variation.

cat("Decision: ALL outliers retained — values represent genuine observations.\n")
cat("No observations removed in outlier treatment step.\n")

# Save summary
write.csv(outlier_summary, file.path(outputs_dir, "04_outlier_summary.csv"), row.names = FALSE)

sink(file.path(outputs_dir, "04_outlier_report.txt"))
cat("OUTLIER ANALYSIS REPORT\n")
cat("========================\n\n")
cat("Method: IQR (Tukey's Fences, 1.5×IQR)\n\n")
print(outlier_summary)
cat("\nTreatment Decision: Retain all outlier observations.\n")
cat("Rationale: All extreme values represent plausible real-world observations.\n")
sink()

# Save cleaned data (unchanged after outlier decision)
saveRDS(adult, file.path(outputs_dir, "adult_post_outlier.rds"))
cat("\n✓ Outlier analysis complete.\n")
cat("=== Script 04 Complete ===\n")
