# =============================================================================
# Script 01: Data Import and Initial Exploration
# Project: Week 1 – Data Cleaning and Preliminary Analysis
# Dataset: UCI Adult/Census Income Dataset
# Author:  Week 1 Assignment
# Date:    2024
# =============================================================================

# Install required packages if not present
required_packages <- c("dplyr", "ggplot2", "tidyr", "readr", "scales",
                       "corrplot", "reshape2", "fastDummies", "moments",
                       "knitr", "stringr")

for (pkg in required_packages) {
  if (!require(pkg, character.only = TRUE, quietly = TRUE)) {
    install.packages(pkg, repos = "https://cran.rstudio.com/", quiet = TRUE)
    library(pkg, character.only = TRUE)
  }
}

# =============================================================================
# 1. DEFINE PROJECT PATHS
# =============================================================================
# Determine script directory robustly
script_dir <- tryCatch(
  dirname(sys.frame(1)$ofile),
  error = function(e) getwd()
)
find_root <- function() {
  dirs <- c(getwd(), dirname(getwd()), file.path(getwd(), 'Week1_Adult_R_Analysis'))
  for (d in dirs) {
    if (file.exists(file.path(d, 'data', 'original', 'adult.data'))) return(d)
  }
  return(getwd())
}
project_root <- find_root()

data_original_dir <- file.path(project_root, "data", "original")
data_cleaned_dir  <- file.path(project_root, "data", "cleaned")
plots_dir         <- file.path(project_root, "plots")
outputs_dir       <- file.path(project_root, "outputs")

# Ensure directories exist
for (d in c(data_original_dir, data_cleaned_dir, plots_dir, outputs_dir)) {
  dir.create(d, showWarnings = FALSE, recursive = TRUE)
}

cat("=============================================================\n")
cat("  UCI Adult Income Dataset – Data Import & Initial Exploration\n")
cat("=============================================================\n\n")

# =============================================================================
# 2. DEFINE COLUMN NAMES (from adult.names documentation)
# =============================================================================
col_names <- c(
  "age", "workclass", "fnlwgt", "education",
  "education_num", "marital_status", "occupation",
  "relationship", "race", "sex",
  "capital_gain", "capital_loss", "hours_per_week",
  "native_country", "income"
)

# =============================================================================
# 3. IMPORT DATA — Convert '?' to NA, strip whitespace
# =============================================================================
cat("--- Importing adult.data ---\n")

raw_data_path <- file.path(data_original_dir, "adult.data")

# Read the raw file
adult_raw <- read.csv(
  raw_data_path,
  header        = FALSE,
  col.names     = col_names,
  na.strings    = c("?", " ?", "? "),
  strip.white   = TRUE,    # Remove leading/trailing whitespace from character fields
  stringsAsFactors = FALSE
)

cat("Import successful.\n\n")

# =============================================================================
# 4. BASIC EXPLORATION COMMANDS
# =============================================================================

cat("--- head() – First 6 rows ---\n")
print(head(adult_raw))

cat("\n--- tail() – Last 6 rows ---\n")
print(tail(adult_raw))

cat("\n--- dim() – Dimensions ---\n")
print(dim(adult_raw))

cat("\n--- names() – Column names ---\n")
print(names(adult_raw))

cat("\n--- str() – Structure ---\n")
str(adult_raw)

cat("\n--- summary() – Summary statistics ---\n")
print(summary(adult_raw))

# =============================================================================
# 5. SAVE HEAD/TAIL OUTPUT FOR REPORT
# =============================================================================
sink(file.path(outputs_dir, "01_head_output.txt"))
cat("head(adult_raw):\n")
print(head(adult_raw))
cat("\ntail(adult_raw):\n")
print(tail(adult_raw))
cat("\ndim(adult_raw):\n")
print(dim(adult_raw))
cat("\nnames(adult_raw):\n")
print(names(adult_raw))
cat("\nstr(adult_raw):\n")
str(adult_raw)
cat("\nsummary(adult_raw):\n")
print(summary(adult_raw))
sink()

cat("\n✓ Output saved to outputs/01_head_output.txt\n")

# =============================================================================
# 6. SAVE raw_data object for downstream scripts
# =============================================================================
saveRDS(adult_raw, file.path(outputs_dir, "adult_raw.rds"))
cat("✓ Raw data saved to outputs/adult_raw.rds\n")

cat("\n=== Script 01 Complete ===\n")
