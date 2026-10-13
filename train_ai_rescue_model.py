import pandas as pd
import numpy as np
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib


# ============================================================
# AVIATION SAR - AI RESCUE OUTCOME PREDICTION
# ============================================================

INPUT_FILE = r"D:\AviationSAR\dataset\flight\ai_rescue_training_data.csv"

MODEL_FILE = r"D:\AviationSAR\dataset\flight\ai_rescue_model.pkl"


print("=" * 70)
print("       AVIATION SAR - AI RESCUE OUTCOME PREDICTION")
print("=" * 70)


# ============================================================
# LOAD DATA
# ============================================================

if not os.path.exists(INPUT_FILE):

    print("\nERROR: AI training dataset not found:")
    print(INPUT_FILE)

    exit()


df = pd.read_csv(INPUT_FILE)


print("\nAI training dataset loaded successfully.")

print("Total records:", len(df))


# ============================================================
# FEATURES
# ============================================================

features = [

    "priority_score",

    "uav_assigned",

    "search_completed",

    "response_level_score",

    "response_time_score",

    "medical_team",

    "ground_rescue",

    "rescue_priority_score",

    "deployment_ready"

]


target = "rescue_outcome"


# ============================================================
# CHECK COLUMNS
# ============================================================

missing_columns = [

    column

    for column in features + [target]

    if column not in df.columns

]


if missing_columns:

    print("\nERROR: Missing columns:")

    for column in missing_columns:

        print("-", column)

    exit()


# ============================================================
# PREPARE DATA
# ============================================================

X = df[features]

y = df[target]


print("\nFeatures used by AI:")

for feature in features:

    print("-", feature)


print("\nTarget variable:")

print("-", target)


# ============================================================
# DATA DISTRIBUTION
# ============================================================

print("\nTarget distribution:")

print(
    y.value_counts()
    .sort_index()
    .to_string()
)


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42,

    stratify=y

)


print("\nTraining samples:", len(X_train))

print("Testing samples :", len(X_test))


# ============================================================
# CREATE RANDOM FOREST MODEL
# ============================================================

model = RandomForestClassifier(

    n_estimators=100,

    max_depth=6,

    random_state=42

)


print("\nTraining AI model...")

model.fit(

    X_train,

    y_train

)


print("Training completed successfully.")


# ============================================================
# PREDICTION
# ============================================================

y_pred = model.predict(X_test)


# ============================================================
# ACCURACY
# ============================================================

accuracy = accuracy_score(

    y_test,

    y_pred

)


print("\n" + "-" * 70)

print("MODEL PERFORMANCE")

print("-" * 70)


print(

    f"\nTest Accuracy: "
    f"{accuracy * 100:.2f}%"

)


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

print("\nClassification Report:")

print(

    classification_report(

        y_test,

        y_pred,

        zero_division=0

    )

)


# ============================================================
# CONFUSION MATRIX
# ============================================================

print("\nConfusion Matrix:")

print(

    confusion_matrix(

        y_test,

        y_pred

    )

)


# ============================================================
# FEATURE IMPORTANCE
# ============================================================

importance = pd.DataFrame({

    "Feature": features,

    "Importance": model.feature_importances_

})


importance = importance.sort_values(

    by="Importance",

    ascending=False

)


print("\nFeature Importance:")

print(

    importance.to_string(index=False)

)


# ============================================================
# SAVE MODEL
# ============================================================

joblib.dump(

    model,

    MODEL_FILE

)


print("\n" + "=" * 70)

print("AI RESCUE MODEL TRAINING COMPLETED")

print("=" * 70)


print("\nModel saved to:")

print(MODEL_FILE)


print("\nNext step:")

print("Use the trained AI model to predict rescue decisions.")