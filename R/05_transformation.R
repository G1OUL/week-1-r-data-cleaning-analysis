# =============================================================================
# Script 05: Data Transformation (Normalization & Categorical Encoding)
# Project: Week 1 - Data Cleaning and Preliminary Analysis
# Dataset: UCI Adult/Census Income Dataset
# =============================================================================

library(dplyr)
library(fastDummies)

cat("=============================================================\n")
cat("  Script 05: Data Transformation\n")
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

# Load post-outlier data
adult <- readRDS(file.path(outputs_dir, "adult_post_outlier.rds"))
cat(sprintf("Loaded %d rows x %d columns\n\n", nrow(adult), ncol(adult)))

# =============================================================================
# 5.1 MIN-MAX NORMALIZATION
# =============================================================================
cat("--- 5.1 Min-Max Normalization ---\n")
cat("Method: Min-Max scales values to [0, 1].\n")
cat("Rationale: Appropriate for variables with skewed, non-Gaussian distributions.\n")
cat("           Preserves the shape of the original distribution.\n\n")

num_cols <- c("age", "fnlwgt", "education_num",
              "capital_gain", "capital_loss", "hours_per_week")

minmax_norm <- function(x) {
  rng <- range(x, na.rm = TRUE)
  if (rng[2] == rng[1]) return(rep(0, length(x)))
  (x - rng[1]) / (rng[2] - rng[1])
}

# Show BEFORE stats
cat("BEFORE normalization:\n")
before_stats <- data.frame(
  Variable = num_cols,
  Mean     = sapply(num_cols, function(c) round(mean(adult[[c]], na.rm=TRUE), 4)),
  SD       = sapply(num_cols, function(c) round(sd(adult[[c]], na.rm=TRUE), 4)),
  Min      = sapply(num_cols, function(c) round(min(adult[[c]], na.rm=TRUE), 4)),
  Max      = sapply(num_cols, function(c) round(max(adult[[c]], na.rm=TRUE), 4)),
  stringsAsFactors = FALSE
)
print(before_stats)

# Create normalized columns (with _norm suffix, preserving originals)
adult_transformed <- adult
for (col in num_cols) {
  new_col <- paste0(col, "_norm")
  adult_transformed[[new_col]] <- minmax_norm(adult[[col]])
}

cat("\nAFTER normalization (normalized columns):\n")
norm_cols <- paste0(num_cols, "_norm")
after_stats <- data.frame(
  Variable = norm_cols,
  Mean     = sapply(norm_cols, function(c) round(mean(adult_transformed[[c]], na.rm=TRUE), 4)),
  SD       = sapply(norm_cols, function(c) round(sd(adult_transformed[[c]], na.rm=TRUE), 4)),
  Min      = sapply(norm_cols, function(c) round(min(adult_transformed[[c]], na.rm=TRUE), 4)),
  Max      = sapply(norm_cols, function(c) round(max(adult_transformed[[c]], na.rm=TRUE), 4)),
  stringsAsFactors = FALSE
)
print(after_stats)

# =============================================================================
# 5.2 CATEGORICAL ENCODING (Dummy / One-Hot)
# =============================================================================
cat("\n--- 5.2 Categorical Encoding ---\n")
cat("Method: One-hot (dummy) encoding using fastDummies::dummy_cols()\n")
cat("Rationale: Converts nominal categoricals to binary 0/1 columns,\n")
cat("           required for correlation/ML analysis. Reference category\n")
cat("           dropped to avoid perfect multicollinearity.\n\n")

# Encode key categorical variables (excluding target for encoding purposes)
cat_to_encode <- c("workclass", "marital_status", "occupation",
                   "relationship", "race", "sex")

adult_encoded <- dummy_cols(
  adult_transformed,
  select_columns          = cat_to_encode,
  remove_first_dummy      = TRUE,
  remove_selected_columns = FALSE
)

# Report new columns added
original_ncols <- ncol(adult_transformed)
new_ncols      <- ncol(adult_encoded)
added_cols     <- new_ncols - original_ncols

cat(sprintf("Original columns : %d\n", original_ncols))
cat(sprintf("Added dummy cols : %d\n", added_cols))
cat(sprintf("Total columns    : %d\n\n", new_ncols))

for (col in cat_to_encode) {
  dummy_names <- grep(paste0("^", col, "_"), names(adult_encoded), value = TRUE)
  cat(sprintf("  %-20s : %d dummy columns\n", col, length(dummy_names)))
}

cat("\nReference categories (dropped first dummy):\n")
for (col in cat_to_encode) {
  ref <- levels(adult[[col]])[1]
  cat(sprintf("  %-20s : reference = '%s'\n", col, ref))
}

# =============================================================================
# 5.3 SAVE
# =============================================================================
saveRDS(adult_transformed, file.path(outputs_dir, "adult_normalized.rds"))
saveRDS(adult_encoded,     file.path(outputs_dir, "adult_encoded.rds"))
write.csv(adult_transformed, file.path(cleaned_dir, "adult_normalized.csv"), row.names = FALSE)

sink(file.path(outputs_dir, "05_transformation_report.txt"))
cat("TRANSFORMATION REPORT\n")
cat("=====================\n\n")
cat("Method: Min-Max Normalization\n")
cat("Normalized variables: age_norm, fnlwgt_norm, education_num_norm,\n")
cat("  capital_gain_norm, capital_loss_norm, hours_per_week_norm\n\n")
cat("BEFORE stats:\n"); print(before_stats)
cat("\nAFTER stats:\n"); print(after_stats)
cat("\nCategorical Encoding: One-hot dummy encoding\n")
cat(sprintf("Variables encoded: %s\n", paste(cat_to_encode, collapse=", ")))
cat(sprintf("Dummy columns added: %d\n", added_cols))
sink()

cat("\nTransformation complete.\n")
cat("=== Script 05 Complete ===\n")
