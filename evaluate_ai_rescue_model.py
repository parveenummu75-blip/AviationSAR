import pandas as pd
import numpy as np

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

print("=" * 70)
print("       AVIATION SAR - AI RESCUE MODEL EVALUATION")
print("=" * 70)

# ------------------------------------------------------------
# 1. LOAD DATA
# ------------------------------------------------------------

FILE = r"D:\AviationSAR\dataset\flight\rescue_outcome_predictions.csv"

df = pd.read_csv(FILE)

print("\nPrediction dataset loaded successfully.")
print("Total records:", len(df))

# ------------------------------------------------------------
# 2. CHECK REQUIRED COLUMNS
# ------------------------------------------------------------

required_columns = [
    "rescue_outcome",
    "rescue_success_probability"
]

for column in required_columns:

    if column not in df.columns:

        print("\nERROR: Missing column:", column)
        print("\nAvailable columns:")
        print(df.columns.tolist())

        raise SystemExit

# ------------------------------------------------------------
# 3. ACTUAL OUTCOME
# ------------------------------------------------------------

y_true = df["rescue_outcome"].astype(int)

# ------------------------------------------------------------
# 4. CONVERT SUCCESS PROBABILITY TO PREDICTION
# ------------------------------------------------------------

# 50% threshold

y_pred = (
    df["rescue_success_probability"] >= 50
).astype(int)

# ------------------------------------------------------------
# 5. CALCULATE METRICS
# ------------------------------------------------------------

accuracy = accuracy_score(y_true, y_pred)

precision = precision_score(
    y_true,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_true,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_true,
    y_pred,
    zero_division=0
)

cm = confusion_matrix(
    y_true,
    y_pred
)

# ------------------------------------------------------------
# 6. DISPLAY RESULTS
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("AI MODEL PERFORMANCE")
print("-" * 70)

print(
    f"Accuracy  : {accuracy * 100:.2f}%"
)

print(
    f"Precision : {precision * 100:.2f}%"
)

print(
    f"Recall    : {recall * 100:.2f}%"
)

print(
    f"F1 Score  : {f1 * 100:.2f}%"
)

# ------------------------------------------------------------
# 7. CONFUSION MATRIX
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("CONFUSION MATRIX")
print("-" * 70)

print("Rows    = Actual")
print("Columns = Predicted")

print("\n", cm)

# ------------------------------------------------------------
# 8. CLASSIFICATION REPORT
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("CLASSIFICATION REPORT")
print("-" * 70)

print(
    classification_report(
        y_true,
        y_pred,
        target_names=[
            "Unsuccessful Rescue",
            "Successful Rescue"
        ],
        zero_division=0
    )
)

# ------------------------------------------------------------
# 9. PREDICTION DISTRIBUTION
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("PREDICTION DISTRIBUTION")
print("-" * 70)

print(
    "Predicted Successful :",
    int(y_pred.sum())
)

print(
    "Predicted Unsuccessful:",
    int((y_pred == 0).sum())
)

print(
    "Actual Successful    :",
    int(y_true.sum())
)

print(
    "Actual Unsuccessful  :",
    int((y_true == 0).sum())
)

# ------------------------------------------------------------
# 10. SAVE EVALUATION RESULTS
# ------------------------------------------------------------

results = pd.DataFrame({
    "Metric": [
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score"
    ],
    "Score_Percent": [
        accuracy * 100,
        precision * 100,
        recall * 100,
        f1 * 100
    ]
})

OUTPUT = (
    r"D:\AviationSAR\dataset\flight"
    r"\ai_rescue_model_evaluation.csv"
)

results.to_csv(
    OUTPUT,
    index=False
)

print("\nEvaluation results saved to:")
print(OUTPUT)

print("\n" + "=" * 70)
print("       AI RESCUE MODEL EVALUATION COMPLETED")
print("=" * 70)