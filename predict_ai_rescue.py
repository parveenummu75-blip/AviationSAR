import pandas as pd
import joblib
import os


# ============================================================
# AVIATION SAR - AI RESCUE PREDICTION
# ============================================================

DATA_FILE = r"D:\AviationSAR\dataset\flight\ai_rescue_training_data.csv"

MODEL_FILE = r"D:\AviationSAR\dataset\flight\ai_rescue_model.pkl"

OUTPUT_FILE = r"D:\AviationSAR\dataset\flight\ai_rescue_predictions.csv"


print("=" * 70)
print("          AVIATION SAR - AI RESCUE PREDICTION")
print("=" * 70)


# ============================================================
# CHECK FILES
# ============================================================

if not os.path.exists(DATA_FILE):

    print("\nERROR: Training data not found.")

    print(DATA_FILE)

    exit()


if not os.path.exists(MODEL_FILE):

    print("\nERROR: AI model not found.")

    print(MODEL_FILE)

    exit()


# ============================================================
# LOAD MODEL AND DATA
# ============================================================

model = joblib.load(MODEL_FILE)

df = pd.read_csv(DATA_FILE)


print("\nAI model loaded successfully.")

print("Input records:", len(df))


# ============================================================
# AI FEATURES
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


X = df[features]


# ============================================================
# AI PREDICTION
# ============================================================

prediction = model.predict(X)

probability = model.predict_proba(X)


# ============================================================
# ADD PREDICTION
# ============================================================

df["ai_prediction"] = prediction


df["ai_confidence_percent"] = (

    probability.max(axis=1) * 100

).round(2)


# ============================================================
# AI RECOMMENDATION
# ============================================================

def recommendation(value):

    if value == 1:

        return "PRIORITIZE RESCUE"

    else:

        return "NORMAL MONITORING"


df["ai_recommendation"] = (

    df["ai_prediction"]
    .apply(recommendation)

)


# ============================================================
# SAVE RESULTS
# ============================================================

df.to_csv(

    OUTPUT_FILE,

    index=False

)


# ============================================================
# DISPLAY SUMMARY
# ============================================================

print("\n" + "-" * 70)

print("AI RESCUE PREDICTION SUMMARY")

print("-" * 70)


high_priority = (

    df["ai_prediction"] == 1

).sum()


normal_priority = (

    df["ai_prediction"] == 0

).sum()


print("\nTotal aircraft:", len(df))

print("AI Priority Rescue:", high_priority)

print("AI Normal Monitoring:", normal_priority)


# ============================================================
# DISPLAY FIRST 10 RESULTS
# ============================================================

print("\nAI Prediction Results:")

print("-" * 70)


display_columns = [

    "priority_score",

    "uav_assigned",

    "rescue_priority_score",

    "ai_prediction",

    "ai_confidence_percent",

    "ai_recommendation"

]


print(

    df[display_columns]
    .head(10)
    .to_string(index=False)

)


# ============================================================
# SAVE
# ============================================================

print("\n" + "=" * 70)

print("AI RESCUE PREDICTION COMPLETED")

print("=" * 70)


print("\nPrediction file saved to:")

print(OUTPUT_FILE)


print("\nNext step:")

print("Integrate AI predictions into the SAR dashboard.")