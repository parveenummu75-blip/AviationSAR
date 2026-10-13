import pandas as pd
import numpy as np
import os


# ============================================================
# AVIATION SAR - RESCUE OUTCOME PREDICTION
# ============================================================

INPUT_FILE = (
    r"D:\AviationSAR\dataset\flight"
    r"\final_ai_rescue_decisions.csv"
)

OUTPUT_FILE = (
    r"D:\AviationSAR\dataset\flight"
    r"\rescue_outcome_predictions.csv"
)


print("=" * 70)
print("          AVIATION SAR - RESCUE OUTCOME PREDICTION")
print("=" * 70)


# ============================================================
# CHECK INPUT FILE
# ============================================================

if not os.path.exists(INPUT_FILE):

    print("\nERROR: Final AI decision file not found.")

    print(INPUT_FILE)

    exit()


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(INPUT_FILE)


print("\nFinal AI decision dataset loaded successfully.")

print("Total records:", len(df))


# ============================================================
# REQUIRED COLUMN CHECK
# ============================================================

required_columns = [

    "priority_score",
    "uav_assigned",
    "search_completed",
    "response_level_score",
    "response_time_score",
    "medical_team",
    "ground_rescue",
    "rescue_priority_score",
    "deployment_ready",
    "ai_prediction",
    "ai_confidence_percent",
    "weather_risk_score",
    "weather_risk_level",
    "final_rescue_decision"

]


missing_columns = [

    column

    for column in required_columns

    if column not in df.columns

]


if missing_columns:

    print("\nERROR: Missing columns:")

    for column in missing_columns:

        print("-", column)

    exit()


# ============================================================
# RESCUE SUCCESS SCORE
# ============================================================

def calculate_success_score(row):

    score = 0.0


    # --------------------------------------------------------
    # AI prediction
    # --------------------------------------------------------

    if row["ai_prediction"] == 1:

        score += 20


    # --------------------------------------------------------
    # Search completed
    # --------------------------------------------------------

    if row["search_completed"] == 1:

        score += 20


    # --------------------------------------------------------
    # UAV assigned
    # --------------------------------------------------------

    if row["uav_assigned"] > 0:

        score += 15


    # --------------------------------------------------------
    # Rescue priority
    # --------------------------------------------------------

    score += (

        float(row["rescue_priority_score"]) / 3

    ) * 10


    # --------------------------------------------------------
    # Deployment readiness
    # --------------------------------------------------------

    if row["deployment_ready"] == 1:

        score += 15


    # --------------------------------------------------------
    # Medical team
    # --------------------------------------------------------

    if row["medical_team"] == 1:

        score += 5


    # --------------------------------------------------------
    # Ground rescue
    # --------------------------------------------------------

    if row["ground_rescue"] == 1:

        score += 5


    # --------------------------------------------------------
    # Weather impact
    # --------------------------------------------------------

    weather_risk = float(
        row["weather_risk_score"]
    )


    score -= weather_risk * 2


    # --------------------------------------------------------
    # Limit score
    # --------------------------------------------------------

    score = max(
        0,
        min(100, score)
    )


    return round(score, 2)


df["rescue_success_score"] = df.apply(

    calculate_success_score,

    axis=1

)


# ============================================================
# RESCUE SUCCESS PROBABILITY
# ============================================================

df["rescue_success_probability"] = (

    df["rescue_success_score"]

    .round(2)

)


# ============================================================
# RESCUE RISK SCORE
# ============================================================

df["rescue_risk_score"] = (

    100

    - df["rescue_success_probability"]

).round(2)


# ============================================================
# OUTCOME CLASSIFICATION
# ============================================================

def classify_outcome(probability):

    if probability >= 75:

        return "HIGH SUCCESS PROBABILITY"

    elif probability >= 50:

        return "MODERATE SUCCESS PROBABILITY"

    else:

        return "HIGH RESCUE RISK"


df["predicted_rescue_outcome"] = (

    df["rescue_success_probability"]

    .apply(classify_outcome)

)


# ============================================================
# OPERATIONAL RECOMMENDATION
# ============================================================

def operational_action(row):

    outcome = row[
        "predicted_rescue_outcome"
    ]

    weather = row[
        "weather_risk_level"
    ]


    if (

        outcome == "HIGH SUCCESS PROBABILITY"

        and weather == "LOW"

    ):

        return (
            "Proceed with planned rescue deployment"
        )


    elif (

        outcome == "HIGH SUCCESS PROBABILITY"

        and weather == "MEDIUM"

    ):

        return (
            "Proceed with rescue and monitor weather"
        )


    elif weather == "HIGH":

        return (
            "Use weather precautions and "
            "review UAV deployment"
        )


    elif outcome == "HIGH RESCUE RISK":

        return (
            "Escalate rescue planning and "
            "assign additional resources"
        )


    else:

        return (
            "Continue rescue operation with monitoring"
        )


df["operational_recommendation"] = df.apply(

    operational_action,

    axis=1

)


# ============================================================
# SAVE RESULTS
# ============================================================

df.to_csv(

    OUTPUT_FILE,

    index=False

)


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "-" * 70)

print("RESCUE OUTCOME SUMMARY")

print("-" * 70)


print(
    "\nTotal targets:",
    len(df)
)


print(
    "\nAverage rescue success probability:",
    f"{df['rescue_success_probability'].mean():.2f}%"
)


print(
    "Average rescue risk score:",
    f"{df['rescue_risk_score'].mean():.2f}"
)


# ============================================================
# OUTCOME DISTRIBUTION
# ============================================================

print("\nPredicted rescue outcomes:")

print(

    df[
        "predicted_rescue_outcome"
    ]
    .value_counts()
    .to_string()

)


# ============================================================
# SAMPLE RESULTS
# ============================================================

print("\nSample rescue outcome predictions:")

print("-" * 70)


display_columns = [

    "priority_score",
    "uav_assigned",
    "weather_risk_level",
    "weather_risk_score",
    "ai_prediction",
    "ai_confidence_percent",
    "rescue_success_probability",
    "rescue_risk_score",
    "predicted_rescue_outcome",
    "operational_recommendation"

]


print(

    df[display_columns]
    .head(10)
    .to_string(index=False)

)


# ============================================================
# COMPLETED
# ============================================================

print("\n" + "=" * 70)

print("       RESCUE OUTCOME PREDICTION COMPLETED")

print("=" * 70)


print("\nPrediction file saved to:")

print(OUTPUT_FILE)


print("\nNext step:")

print(
    "Integrate rescue outcome predictions "
    "into the dashboard."
)