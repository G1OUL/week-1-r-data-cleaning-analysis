# =============================================================================
# Script 03: Data Cleaning
# Project: Week 1 – Data Cleaning and Preliminary Analysis
# Dataset: UCI Adult/Census Income Dataset
# =============================================================================

library(dplyr)
library(stringr)

cat("=============================================================\n")
cat("  Script 03: Data Cleaning\n")
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
cleaned_dir  <- file.path(project_root, "data", "cleaned")

# Load raw data
adult_raw <- readRDS(file.path(outputs_dir, "adult_raw.rds"))
adult     <- adult_raw  # work on copy

cat(sprintf("Starting rows: %d\n\n", nrow(adult)))

# =============================================================================
# 3.A MISSING VALUES – BEFORE
# =============================================================================
cat("--- 3.A Missing Values BEFORE Treatment ---\n")
mv_before <- colSums(is.na(adult))
print(mv_before[mv_before > 0])

# Columns with missing values: workclass, occupation, native_country
cat("\nMissing value counts by column (all cols):\n")
print(colSums(is.na(adult)))

# ----
# Strategy decisions:
#   workclass     → Mode imputation (most frequent = "Private")
#   occupation    → Mode imputation (most frequent category)
#   native_country→ Mode imputation (most frequent = "United-States")
#
# Rationale: These are MCAR/MAR with <6% missing. Mode imputation for
# categorical variables preserves the most likely category without
# introducing new dummy categories.  Dataset size means < 2500 rows lost
# if list-deleted, which is material for imbalanced class learning.
# ----

# Helper: compute mode (most frequent non-NA value)
get_mode <- function(x) {
  tbl <- sort(table(x[!is.na(x)]), decreasing = TRUE)
  names(tbl)[1]
}

# 3.A.1  workclass
mode_workclass <- get_mode(adult$workclass)
cat(sprintf("\nMode of workclass : '%s'\n", mode_workclass))
adult$workclass[is.na(adult$workclass)] <- mode_workclass

# 3.A.2  occupation
mode_occupation <- get_mode(adult$occupation)
cat(sprintf("Mode of occupation: '%s'\n", mode_occupation))
adult$occupation[is.na(adult$occupation)] <- mode_occupation

# 3.A.3  native_country
mode_country <- get_mode(adult$native_country)
cat(sprintf("Mode of native_country: '%s'\n", mode_country))
adult$native_country[is.na(adult$native_country)] <- mode_country

cat("\n--- 3.A Missing Values AFTER Treatment ---\n")
mv_after <- colSums(is.na(adult))
print(mv_after)

# =============================================================================
# 3.B DUPLICATE ROWS
# =============================================================================
cat("\n--- 3.B Duplicate Rows ---\n")
n_before <- nrow(adult)
n_dup    <- sum(duplicated(adult))
cat(sprintf("Rows before  : %d\n", n_before))
cat(sprintf("Duplicates   : %d\n", n_dup))

# Decision: Remove duplicates (they add no information)
adult <- adult[!duplicated(adult), ]
cat(sprintf("Rows after   : %d\n", nrow(adult)))
cat(sprintf("Rows removed : %d\n", n_before - nrow(adult)))

# =============================================================================
# 3.C DATA TYPE CONVERSION
# =============================================================================
cat("\n--- 3.C Data Type Conversion ---\n")

# Numerical columns (already numeric from read.csv – verify)
num_cols <- c("age", "fnlwgt", "education_num", "capital_gain",
              "capital_loss", "hours_per_week")
for (col in num_cols) {
  adult[[col]] <- as.numeric(adult[[col]])
}

# Ordered factor for education_num is redundant (numerical); keep as numeric.
# Ordered factor for education level:
edu_order <- c("Preschool","1st-4th","5th-6th","7th-8th","9th","10th",
                "11th","12th","HS-grad","Some-college","Assoc-voc",
                "Assoc-acdm","Bachelors","Masters","Prof-school","Doctorate")
adult$education <- factor(adult$education, levels = edu_order, ordered = TRUE)

# Nominal factors for remaining categoricals
cat_cols <- c("workclass", "marital_status", "occupation",
              "relationship", "race", "sex", "native_country")
for (col in cat_cols) {
  adult[[col]] <- as.factor(adult[[col]])
}

# =============================================================================
# 3.D TARGET VARIABLE CLEANING
# =============================================================================
cat("\n--- 3.D Target Variable: income ---\n")
cat("Before cleaning:\n")
print(table(adult$income, useNA = "ifany"))

# Standardise income to ">50K" / "<=50K" (strip trailing period if any)
adult$income <- gsub("\\.$", "", trimws(adult$income))
adult$income <- factor(adult$income, levels = c("<=50K", ">50K"))

cat("After cleaning:\n")
print(table(adult$income))

# =============================================================================
# 3.E CATEGORICAL CONSISTENCY CHECK
# =============================================================================
cat("\n--- 3.E Categorical Consistency (levels check) ---\n")
for (col in names(adult)[sapply(adult, is.factor)]) {
  cat(sprintf("%-20s : %d levels\n", col, nlevels(adult[[col]])))
}

# =============================================================================
# 3.F BEFORE vs AFTER SUMMARY
# =============================================================================
cat("\n--- Before vs. After Cleaning Summary ---\n")
bva <- data.frame(
  Metric             = c("Total Rows", "Missing: workclass",
                         "Missing: occupation", "Missing: native_country",
                         "Total Missing Values", "Duplicate Rows"),
  Before             = c(nrow(adult_raw),
                         sum(is.na(adult_raw$workclass)),
                         sum(is.na(adult_raw$occupation)),
                         sum(is.na(adult_raw$native_country)),
                         sum(is.na(adult_raw)),
                         sum(duplicated(adult_raw))),
  After              = c(nrow(adult),
                         sum(is.na(adult$workclass)),
                         sum(is.na(adult$occupation)),
                         sum(is.na(adult$native_country)),
                         sum(is.na(adult)),
                         0),
  stringsAsFactors   = FALSE
)
print(bva)

# =============================================================================
# 3.G SAVE CLEANED DATA
# =============================================================================
saveRDS(adult, file.path(outputs_dir, "adult_cleaned.rds"))
write.csv(adult, file.path(cleaned_dir, "adult_cleaned.csv"), row.names = FALSE)
write.csv(bva,   file.path(outputs_dir, "03_before_after_cleaning.csv"), row.names = FALSE)

sink(file.path(outputs_dir, "03_cleaning_report.txt"))
cat("CLEANING REPORT\n")
cat("===============\n\n")
cat(sprintf("Rows (raw)    : %d\n", nrow(adult_raw)))
cat(sprintf("Rows (clean)  : %d\n", nrow(adult)))
cat(sprintf("Missing (raw) : %d\n", sum(is.na(adult_raw))))
cat(sprintf("Missing (clean): %d\n", sum(is.na(adult))))
cat(sprintf("Modes used — workclass: %s | occupation: %s | country: %s\n",
            mode_workclass, mode_occupation, mode_country))
cat("\nBefore vs After Table:\n")
print(bva)
cat("\nFinal str():\n")
str(adult)
sink()

cat("\n✓ Cleaned dataset saved.\n")
cat("=== Script 03 Complete ===\n")
