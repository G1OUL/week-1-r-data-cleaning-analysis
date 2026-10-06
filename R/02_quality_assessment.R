# =============================================================================
# Script 02: Data Quality Assessment
# Project: Week 1 – Data Cleaning and Preliminary Analysis
# Dataset: UCI Adult/Census Income Dataset
# =============================================================================

library(dplyr)
library(tidyr)
library(stringr)

cat("=============================================================\n")
cat("  Script 02: Data Quality Assessment\n")
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

# Load raw data
adult_raw <- readRDS(file.path(outputs_dir, "adult_raw.rds"))
cat(sprintf("Loaded %d rows × %d columns\n\n", nrow(adult_raw), ncol(adult_raw)))

# =============================================================================
# 2.1 MISSING VALUES
# =============================================================================
cat("--- 2.1 Missing Value Assessment ---\n")

missing_counts <- colSums(is.na(adult_raw))
missing_pct    <- round(100 * missing_counts / nrow(adult_raw), 2)
n_unique       <- sapply(adult_raw, function(x) length(unique(x)))

# Data types
dtypes <- sapply(adult_raw, class)

# Numerical summaries
num_cols <- c("age", "fnlwgt", "education_num", "capital_gain",
              "capital_loss", "hours_per_week")

col_min <- sapply(adult_raw, function(x) if (is.numeric(x)) min(x, na.rm=TRUE) else NA)
col_max <- sapply(adult_raw, function(x) if (is.numeric(x)) max(x, na.rm=TRUE) else NA)

quality_table <- data.frame(
  Column         = names(adult_raw),
  DataType       = as.character(dtypes),
  MissingCount   = as.integer(missing_counts),
  MissingPct     = missing_pct,
  UniqueValues   = as.integer(n_unique),
  Min            = round(col_min, 2),
  Max            = round(col_max, 2),
  stringsAsFactors = FALSE
)
rownames(quality_table) <- NULL

print(quality_table)

# =============================================================================
# 2.2 DUPLICATE ROWS
# =============================================================================
cat("\n--- 2.2 Duplicate Row Assessment ---\n")
n_dup <- sum(duplicated(adult_raw))
cat(sprintf("Total rows          : %d\n", nrow(adult_raw)))
cat(sprintf("Duplicate rows      : %d\n", n_dup))
cat(sprintf("Unique rows         : %d\n", nrow(adult_raw) - n_dup))

# =============================================================================
# 2.3 WHITESPACE CHECK
# =============================================================================
cat("\n--- 2.3 Whitespace Check (character columns) ---\n")
char_cols <- names(adult_raw)[sapply(adult_raw, is.character)]
for (col in char_cols) {
  vals <- adult_raw[[col]]
  has_ws <- any(vals != trimws(vals), na.rm = TRUE)
  cat(sprintf("  %-20s : whitespace issues = %s\n", col, has_ws))
}

# =============================================================================
# 2.4 CATEGORICAL UNIQUE VALUES
# =============================================================================
cat("\n--- 2.4 Unique Categorical Values ---\n")
for (col in char_cols) {
  cat(sprintf("\n%s:\n", col))
  tbl <- sort(table(adult_raw[[col]], useNA = "ifany"))
  print(tbl)
}

# =============================================================================
# 2.5 NUMERICAL RANGE CHECK
# =============================================================================
cat("\n--- 2.5 Numerical Variable Ranges ---\n")
for (col in num_cols) {
  x <- adult_raw[[col]]
  cat(sprintf("%-20s : min=%g  max=%g  mean=%.2f  negative=%d\n",
              col, min(x,na.rm=T), max(x,na.rm=T),
              mean(x,na.rm=T), sum(x<0, na.rm=T)))
}

# =============================================================================
# 2.6 SAVE QUALITY TABLE
# =============================================================================
write.csv(quality_table, file.path(outputs_dir, "02_quality_table.csv"), row.names = FALSE)

sink(file.path(outputs_dir, "02_quality_report.txt"))
cat("DATA QUALITY ASSESSMENT REPORT\n")
cat("=================================\n\n")
cat(sprintf("Total Rows    : %d\n", nrow(adult_raw)))
cat(sprintf("Total Columns : %d\n", ncol(adult_raw)))
cat(sprintf("Duplicate Rows: %d\n\n", n_dup))
cat("Column-Level Quality Summary:\n")
print(quality_table)
cat("\n\nCategorical Unique Values:\n")
for (col in char_cols) {
  cat(sprintf("\n%s:\n", col))
  print(table(adult_raw[[col]], useNA = "ifany"))
}
sink()

cat("\n✓ Quality report saved.\n")
cat("=== Script 02 Complete ===\n")
