# =============================================================================
# Script 11: Week 3 Predictive Modeling — Logistic Regression & Cross-Validation
# Project: Week 3 - Statistical Analysis and Predictive Modeling using R
# Dataset: UCI Adult / Census Income Dataset (Cleaned)
# =============================================================================

suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
  library(scales)
  library(car)
  library(glmnet)
  library(pROC)
})

cat("=============================================================\n")
cat("  Script 11: Week 3 Predictive Modeling (Logistic Regression)\n")
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
outputs_dir  <- file.path(project_root, "outputs")
model_dir    <- file.path(outputs_dir, "week3_model")
plots_dir    <- file.path(project_root, "plots", "week3")
data_dir     <- file.path(project_root, "data", "cleaned")

dir.create(model_dir, showWarnings = FALSE, recursive = TRUE)
dir.create(plots_dir, showWarnings = FALSE, recursive = TRUE)

# 2. LOAD DATASET
csv_path <- file.path(data_dir, "adult_cleaned.csv")
rds_path <- file.path(outputs_dir, "adult_cleaned.rds")

if (file.exists(rds_path)) {
  adult <- readRDS(rds_path)
} else if (file.exists(csv_path)) {
  adult <- read.csv(csv_path, stringsAsFactors = TRUE)
} else {
  stop("Cleaned dataset not found.")
}

# Ensure income is formatted with <=50K as reference and >50K as target (1)
adult$income <- factor(as.character(adult$income), levels = c("<=50K", ">50K"))
adult$target <- ifelse(adult$income == ">50K", 1, 0)

# Feature selection for modeling
# We include age, workclass, education_num, marital_status, occupation, relationship, race, sex,
# capital_gain, capital_loss, hours_per_week.
# We exclude 'fnlwgt' (survey weight) and 'education' (redundant with education_num).
# For native_country, group into US vs Non-US to avoid extreme sparsity.
adult$native_region <- factor(ifelse(adult$native_country == "United-States", "United-States", "Non-US"))

# Clean categorical factors to remove unused levels
cat_cols <- c("workclass", "marital_status", "occupation", "relationship", "race", "sex", "native_region")
for (cc in cat_cols) {
  adult[[cc]] <- as.factor(as.character(adult[[cc]]))
}

# 3. STRATIFIED TRAIN / TEST SPLIT (80% Train, 20% Test)
cat("\n--- 3. Creating Stratified 80/20 Train/Test Split ---\n")
set.seed(2026)

# Stratify on income target
idx_0 <- which(adult$target == 0)
idx_1 <- which(adult$target == 1)

train_idx_0 <- sample(idx_0, size = round(0.80 * length(idx_0)))
train_idx_1 <- sample(idx_1, size = round(0.80 * length(idx_1)))
train_idx   <- sort(c(train_idx_0, train_idx_1))
test_idx    <- setdiff(seq_len(nrow(adult)), train_idx)

train_data <- adult[train_idx, ]
test_data  <- adult[test_idx, ]

cat(sprintf("Training Set: %d observations (<=50K: %d [%.1f%%], >50K: %d [%.1f%%])\n",
            nrow(train_data), sum(train_data$target == 0), mean(train_data$target == 0)*100,
            sum(train_data$target == 1), mean(train_data$target == 1)*100))
cat(sprintf("Testing Set:  %d observations (<=50K: %d [%.1f%%], >50K: %d [%.1f%%])\n",
            nrow(test_data), sum(test_data$target == 0), mean(test_data$target == 0)*100,
            sum(test_data$target == 1), mean(test_data$target == 1)*100))

# 4. FIVE-FOLD CROSS-VALIDATION ON TRAINING SET
cat("\n--- 4. Setting Up 5-Fold Stratified Cross-Validation ---\n")
set.seed(2026)
k_folds <- 5
train_data$fold <- 0

# Stratified fold assignment
fold_assign_0 <- sample(rep(1:k_folds, length.out = length(train_idx_0)))
fold_assign_1 <- sample(rep(1:k_folds, length.out = length(train_idx_1)))
train_data$fold[train_data$target == 0] <- fold_assign_0
train_data$fold[train_data$target == 1] <- fold_assign_1

formula_baseline <- target ~ age + workclass + education_num + marital_status + 
                             occupation + relationship + race + sex + 
                             capital_gain + capital_loss + hours_per_week + native_region

cv_auc_scores <- numeric(k_folds)
cv_acc_scores <- numeric(k_folds)

for (k in 1:k_folds) {
  cv_train <- train_data[train_data$fold != k, ]
  cv_val   <- train_data[train_data$fold == k, ]
  
  fit_cv <- glm(formula_baseline, data = cv_train, family = binomial(link = "logit"))
  preds_val <- predict(fit_cv, newdata = cv_val, type = "response")
  
  roc_val <- pROC::roc(cv_val$target, preds_val, quiet = TRUE)
  cv_auc_scores[k] <- as.numeric(roc_val$auc)
  
  pred_class <- ifelse(preds_val >= 0.5, 1, 0)
  cv_acc_scores[k] <- mean(pred_class == cv_val$target)
  
  cat(sprintf("  Fold %d: Accuracy = %.4f | AUC = %.4f\n", k, cv_acc_scores[k], cv_auc_scores[k]))
}

cat(sprintf("5-Fold CV Baseline: Mean Accuracy = %.4f (SD = %.4f) | Mean AUC = %.4f (SD = %.4f)\n",
            mean(cv_acc_scores), sd(cv_acc_scores), mean(cv_auc_scores), sd(cv_auc_scores)))

# 5. FIT MODEL 1: FULL BASELINE LOGISTIC REGRESSION
cat("\n--- 5. Fitting Full Baseline Logistic Regression Model ---\n")
model1 <- glm(formula_baseline, data = train_data, family = binomial(link = "logit"))

# Save Model 1 Summary to text file
summary_file <- file.path(model_dir, "logistic_regression_summary.txt")
sink(summary_file)
cat("=========================================================================\n")
cat("  MODEL 1: BASELINE LOGISTIC REGRESSION SUMMARY\n")
cat("  Target: income (>50K = 1, <=50K = 0)\n")
cat("  Training Sample: N = 26,030 observations\n")
cat("=========================================================================\n\n")
print(summary(model1))
cat("\n=========================================================================\n")
cat(sprintf("Null Deviance:     %.2f on %d degrees of freedom\n", model1$null.deviance, model1$df.null))
cat(sprintf("Residual Deviance: %.2f on %d degrees of freedom\n", model1$deviance, model1$df.residual))
cat(sprintf("AIC:               %.2f\n", model1$aic))
cat(sprintf("5-Fold CV Mean AUC: %.4f\n", mean(cv_auc_scores)))
cat("=========================================================================\n")
sink()
cat("Saved logistic_regression_summary.txt\n")

# Coefficients table
coef_mat <- summary(model1)$coefficients
coef_df <- data.frame(
  Term = rownames(coef_mat),
  Estimate = round(coef_mat[, "Estimate"], 4),
  Std_Error = round(coef_mat[, "Std. Error"], 4),
  Z_Value = round(coef_mat[, "z value"], 3),
  P_Value = format.pval(coef_mat[, "Pr(>|z|)"], eps = 0.0001),
  stringsAsFactors = FALSE
)
write.csv(coef_df, file.path(model_dir, "logistic_coefficients.csv"), row.names = FALSE)
cat("Saved logistic_coefficients.csv\n")

# Odds Ratios with 95% Confidence Intervals
# Wald CI: beta +/- 1.96 * SE
or_vals <- exp(coef_mat[, "Estimate"])
ci_lower <- exp(coef_mat[, "Estimate"] - 1.96 * coef_mat[, "Std. Error"])
ci_upper <- exp(coef_mat[, "Estimate"] + 1.96 * coef_mat[, "Std. Error"])

odds_ratios_df <- data.frame(
  Predictor = rownames(coef_mat),
  Odds_Ratio = round(or_vals, 4),
  CI_95_Lower = round(ci_lower, 4),
  CI_95_Upper = round(ci_upper, 4),
  P_Value = format.pval(coef_mat[, "Pr(>|z|)"], eps = 0.0001),
  Interpretation = ifelse(or_vals > 1, "Higher modeled odds of >50K", "Lower modeled odds of >50K"),
  stringsAsFactors = FALSE
)
# Filter out Intercept for clean presentation
write.csv(odds_ratios_df, file.path(model_dir, "odds_ratios.csv"), row.names = FALSE)
cat("Saved odds_ratios.csv\n")

# 6. MULTICOLLINEARITY (VIF / GVIF ANALYSIS)
cat("\n--- 6. Multicollinearity Assessment (Generalized VIF) ---\n")
vif_vals <- car::vif(model1)
vif_df <- as.data.frame(vif_vals)
vif_df$Variable <- rownames(vif_df)

# If GVIF^(1/(2*Df)) is present, use it as standardized metric
if ("GVIF^(1/(2*Df))" %in% colnames(vif_df)) {
  vif_df$Standardized_GVIF <- round(vif_df[["GVIF^(1/(2*Df))"]], 4)
  vif_df$Multicollinearity_Status <- ifelse(vif_df$Standardized_GVIF < 2.0, "Low / Acceptable", "Moderate / High")
} else {
  vif_df$Standardized_GVIF <- round(sqrt(vif_df$GVIF), 4)
  vif_df$Multicollinearity_Status <- ifelse(vif_df$GVIF < 5.0, "Low / Acceptable", "High")
}
write.csv(vif_df, file.path(model_dir, "vif_results.csv"), row.names = FALSE)
cat("Saved vif_results.csv\n")

# 7. MODEL 2: OPTIMIZED REGULARIZED LOGISTIC REGRESSION (GLMNET / ELASTIC NET)
cat("\n--- 7. Training Model 2: Regularized Logistic Regression (L2 / Ridge-Elastic Net) ---\n")
# Create model matrix (one-hot encoded)
x_train <- model.matrix(formula_baseline, data = train_data)[, -1]
y_train <- train_data$target

x_test <- model.matrix(formula_baseline, data = test_data)[, -1]
y_test <- test_data$target

# Cross-validated lambda selection (alpha = 0.5 for Elastic Net)
set.seed(2026)
cv_glmnet <- cv.glmnet(x_train, y_train, family = "binomial", alpha = 0.5, nfolds = 5, type.measure = "auc")
best_lambda <- cv_glmnet$lambda.1se
cat(sprintf("Optimal Lambda (1SE): %.6f (AUC at best lambda: %.4f)\n", best_lambda, max(cv_glmnet$cvm)))

model2 <- glmnet(x_train, y_train, family = "binomial", alpha = 0.5, lambda = best_lambda)

# 8. TEST SET PREDICTIONS
cat("\n--- 8. Generating Test Set Predictions ---\n")
prob_m1 <- predict(model1, newdata = test_data, type = "response")
pred_m1 <- ifelse(prob_m1 >= 0.5, ">50K", "<=50K")

prob_m2 <- as.numeric(predict(model2, newx = x_test, type = "response"))
pred_m2 <- ifelse(prob_m2 >= 0.5, ">50K", "<=50K")

predictions_df <- data.frame(
  actual = as.character(test_data$income),
  actual_target = test_data$target,
  prob_model1 = round(prob_m1, 4),
  pred_model1 = pred_m1,
  prob_model2 = round(prob_m2, 4),
  pred_model2 = pred_m2,
  stringsAsFactors = FALSE
)

write.csv(predictions_df, file.path(model_dir, "test_predictions.csv"), row.names = FALSE)
saveRDS(list(model1 = model1, model2 = model2, test_data = test_data, train_data = train_data,
             cv_auc_scores = cv_auc_scores, cv_acc_scores = cv_acc_scores),
        file.path(model_dir, "week3_models.rds"))
cat("Saved test_predictions.csv and week3_models.rds\n")

cat("\n=== Script 11 Completed Successfully ===\n")
