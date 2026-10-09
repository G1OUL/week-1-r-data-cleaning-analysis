# =============================================================================
# Script 13: Week 3 Master Academic Report Generation & Verification
# Project: Week 3 - Statistical Analysis and Predictive Modeling using R
# Dataset: UCI Adult / Census Income Dataset (Cleaned)
# Deliverable: report/Week3_Statistical_Analysis_Predictive_Modeling.docx
# =============================================================================

cat("=============================================================\n")
cat("  Script 13: Week 3 Master Academic Report Generation\n")
cat("=============================================================\n\n")

# 1. SETUP PATHS
find_root <- function() {
  dirs <- c(getwd(), dirname(getwd()), file.path(getwd(), 'Week1_Adult_R_Analysis'))
  for (d in dirs) {
    if (file.exists(file.path(d, 'data', 'cleaned', 'adult_cleaned.csv'))) return(d)
  }
  return(getwd())
}
project_root <- find_root()
report_dir   <- file.path(project_root, "report")
docx_path    <- file.path(report_dir, "Week3_Statistical_Analysis_Predictive_Modeling.docx")
py_script    <- file.path(report_dir, "generate_week3_report.py")

cat(sprintf("Project Root: %s\n", project_root))
cat(sprintf("Target DOCX:  %s\n", docx_path))

# 2. VERIFY PREREQUISITE ARTIFACTS
required_outputs <- c(
  file.path(project_root, "outputs", "week3_statistics", "descriptive_statistics.csv"),
  file.path(project_root, "outputs", "week3_statistics", "hypothesis_tests.csv"),
  file.path(project_root, "outputs", "week3_model", "evaluation_metrics.csv"),
  file.path(project_root, "outputs", "week3_model", "odds_ratios.csv"),
  file.path(project_root, "outputs", "week3_model", "vif_results.csv"),
  file.path(project_root, "outputs", "week3_model", "calibration_deciles.csv")
)

missing_artifacts <- required_outputs[!file.exists(required_outputs)]
if (length(missing_artifacts) > 0) {
  stop(sprintf("Cannot compile report: Missing prerequisite artifacts:\n%s",
               paste(missing_artifacts, collapse = "\n")))
}

cat("All statistical and modeling prerequisite artifacts are verified.\n\n")

# 3. TRIGGER REPORT BUILDER
cat("Invoking Python DOCX report compiler...\n")
py_cmd <- sprintf('python "%s"', py_script)
exit_code <- system(py_cmd)

if (exit_code != 0) {
  # Fallback to python3 if python returned non-zero
  py_cmd_alt <- sprintf('python3 "%s"', py_script)
  exit_code <- system(py_cmd_alt)
}

if (exit_code != 0) {
  stop(sprintf("Report generation failed with exit code %d. Ensure python and python-docx are installed.", exit_code))
}

# 4. VERIFY COMPILED REPORT
if (file.exists(docx_path)) {
  file_info <- file.info(docx_path)
  file_size_mb <- file_info$size / (1024 * 1024)
  cat(sprintf("\n[SUCCESS] Master Word Report compiled successfully!\n"))
  cat(sprintf("  File: %s\n", docx_path))
  cat(sprintf("  Size: %.2f MB (%d bytes)\n", file_size_mb, file_info$size))
  cat(sprintf("  Last Modified: %s\n", file_info$mtime))
} else {
  stop("Report file not found after generation attempt.")
}

cat("\n=== Script 13 Completed Successfully ===\n")
