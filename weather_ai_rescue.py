import pandas as pd
import os


# ============================================================
# AVIATION SAR - WEATHER + AI RESCUE DECISION
# ============================================================

AI_FILE = r"D:\AviationSAR\dataset\flight\ai_rescue_predictions.csv"

WEATHER_FILE = r"D:\AviationSAR\dataset\flight\weather_data.csv"

OUTPUT_FILE = r"D:\AviationSAR\dataset\flight\final_ai_rescue_decisions.csv"


print("=" * 70)
print("       AVIATION SAR - WEATHER + AI RESCUE DECISION")
print("=" * 70)


# ============================================================
# CHECK FILES
# ============================================================

if not os.path.exists(AI_FILE):

    print("\nERROR: AI prediction file not found:")
    print(AI_FILE)
    exit()


if not os.path.exists(WEATHER_FILE):

    print("\nERROR: Weather file not found:")
    print(WEATHER_FILE)
    exit()


# ============================================================
# LOAD DATA
# ============================================================

ai_df = pd.read_csv(AI_FILE)

weather_df = pd.read_csv(WEATHER_FILE)


print("\nAI prediction data loaded.")

print("Weather data loaded.")

print("\nAI columns:")

print(ai_df.columns.tolist())

print("\nWeather columns:")

print(weather_df.columns.tolist())


print("\nAircraft records:", len(ai_df))

print("Weather records:", len(weather_df))


# ============================================================
# ADD WEATHER DATA BY ROW
# ============================================================
#
# Both files contain exactly 57 records and were generated
# from the same aircraft dataset.
#
# Therefore we safely combine them row-by-row.
# ============================================================

weather_columns = [

    "temperature_c",

    "wind_speed_kmh",

    "visibility_km",

    "precipitation_mm",

    "weather_condition",

    "weather_risk_score",

    "weather_risk_level"

]


for column in weather_columns:

    if column not in weather_df.columns:

        print("\nERROR: Missing weather column:")

        print(column)

        exit()


# Reset indexes before combining

ai_df = ai_df.reset_index(drop=True)

weather_df = weather_df.reset_index(drop=True)


# Combine weather information

df = pd.concat(

    [
        ai_df,
        weather_df[weather_columns]
    ],

    axis=1

)


# ============================================================
# FINAL RESCUE DECISION
# ============================================================

def final_decision(row):

    ai_prediction = int(row["ai_prediction"])

    weather_risk = int(row["weather_risk_score"])

    rescue_priority = int(row["rescue_priority_score"])


    # HIGH AI PRIORITY + HIGH WEATHER RISK

    if ai_prediction == 1 and weather_risk >= 6:

        return "IMMEDIATE RESCUE - HIGH WEATHER RISK"


    # HIGH AI PRIORITY + MEDIUM WEATHER RISK

    elif ai_prediction == 1 and weather_risk >= 3:

        return "PRIORITY RESCUE - WEATHER CAUTION"


    # HIGH AI PRIORITY + LOW WEATHER RISK

    elif ai_prediction == 1:

        return "IMMEDIATE RESCUE"


    # HIGH RESCUE PRIORITY + HIGH WEATHER RISK

    elif rescue_priority >= 3 and weather_risk >= 6:

        return "RESCUE REVIEW - HIGH WEATHER RISK"


    # NORMAL

    else:

        return "NORMAL MONITORING"


df["final_rescue_decision"] = df.apply(

    final_decision,

    axis=1

)


# ============================================================
# FINAL RECOMMENDED ACTION
# ============================================================

def final_action(decision):

    if decision == "IMMEDIATE RESCUE - HIGH WEATHER RISK":

        return (
            "Deploy rescue team immediately "
            "with weather precautions"
        )


    elif decision == "PRIORITY RESCUE - WEATHER CAUTION":

        return (
            "Deploy rescue team and "
            "monitor weather"
        )


    elif decision == "IMMEDIATE RESCUE":

        return (
            "Deploy UAV + Ground Rescue "
            "+ Medical Team"
        )


    elif decision == "RESCUE REVIEW - HIGH WEATHER RISK":

        return (
            "Review UAV deployment "
            "before rescue"
        )


    else:

        return "Continue monitoring"


df["final_recommended_action"] = (

    df["final_rescue_decision"]

    .apply(final_action)

)


# ============================================================
# SAVE FINAL DATA
# ============================================================

df.to_csv(

    OUTPUT_FILE,

    index=False

)


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "-" * 70)

print("FINAL AI RESCUE DECISION SUMMARY")

print("-" * 70)


print("\nTotal aircraft:", len(df))


print("\nWeather risk distribution:")

print(

    df["weather_risk_level"]

    .value_counts()

    .to_string()

)


print("\nFinal rescue decision distribution:")

print(

    df["final_rescue_decision"]

    .value_counts()

    .to_string()

)


# ============================================================
# SAMPLE RESULTS
# ============================================================

print("\nSample final decisions:")

print("-" * 70)


display_columns = [

    "priority_score",

    "uav_assigned",

    "weather_condition",

    "weather_risk_score",

    "weather_risk_level",

    "ai_prediction",

    "ai_confidence_percent",

    "final_rescue_decision",

    "final_recommended_action"

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

print("       WEATHER + AI RESCUE DECISION COMPLETED")

print("=" * 70)


print("\nFinal decision file saved to:")

print(OUTPUT_FILE)


print("\nNext step:")

print("Integrate final AI rescue decisions into the dashboard.")