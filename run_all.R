# =============================================================================
# run_all.R — Master script: runs all analysis scripts in order
# Project: Weeks 1, 2 & 3 - Data Cleaning, Analysis, Visualization, Modeling
# UCI Adult/Census Income Dataset
# =============================================================================

cat("=================================================================\n")
cat("  MASTER RUN SCRIPT - Weeks 1, 2 & 3: Adult Income Dataset\n")
cat("  Starting full pipeline...\n")
cat("=================================================================\n\n")

# Set working directory to project root
script_dir   <- tryCatch(dirname(sys.frame(1)), error = function(e) getwd())

# Install required packages for Weeks 1-3
required_packages <- c("dplyr", "ggplot2", "tidyr", "readr", "scales",
                       "corrplot", "reshape2", "fastDummies", "moments",
                       "knitr", "stringr", "lattice", "car", "glmnet", "pROC")
for (pkg in required_packages) {
  if (!require(pkg, character.only = TRUE, quietly = TRUE)) {
    install.packages(pkg, repos = "https://cran.rstudio.com/", quiet = TRUE)
    library(pkg, character.only = TRUE)
  }
}

# Week 1 scripts
scripts_w1 <- c("R/01_import.R", "R/02_quality_assessment.R", "R/03_cleaning.R",
                "R/04_outlier_analysis.R", "R/05_transformation.R",
                "R/06_eda.R", "R/07_final_analysis.R")

# Week 2 scripts
scripts_w2 <- c("R/08_week2_visualizations.R", "R/09_week2_analysis.R")

# Week 3 scripts
scripts_w3 <- c("R/10_week3_statistical_analysis.R",
                "R/11_week3_modeling.R",
                "R/12_week3_evaluation.R",
                "R/13_week3_report_generation.R")

scripts <- c(scripts_w1, scripts_w2, scripts_w3)

failed_scripts <- character()

for (s in scripts) {
  cat(sprintf("\n>>> Running: %s\n", s))
  cat(rep("-", 60), "\n", sep="")
  success <- tryCatch(
    {
      source(s, local = FALSE)
      TRUE
    },
    error = function(e) {
      cat(sprintf("\n[ERROR] Script failed: %s\nDetails: %s\n", s, conditionMessage(e)))
      FALSE
    }
  )
  if (!success) {
    failed_scripts <- c(failed_scripts, s)
  }
}

cat("\n=================================================================\n")
if (length(failed_scripts) == 0) {
  cat("  PIPELINE COMPLETE (Weeks 1 + 2 + 3) - ALL 13 SCRIPTS SUCCEEDED\n")
  cat("=================================================================\n")
} else {
  cat("  PIPELINE FINISHED WITH ERRORS\n")
  cat(sprintf("  The following %d script(s) encountered failures:\n", length(failed_scripts)))
  for (f in failed_scripts) {
    cat(sprintf("   - %s\n", f))
  }
  cat("=================================================================\n")
  stop("Pipeline execution terminated with errors in one or more scripts.")
}

# Note: To run only Week 3 (when Weeks 1 & 2 outputs already exist):
#   Rscript R/10_week3_statistical_analysis.R
#   Rscript R/11_week3_modeling.R
#   Rscript R/12_week3_evaluation.R
#   Rscript R/13_week3_report_generation.R
