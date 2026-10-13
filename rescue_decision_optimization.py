import pandas as pd
import os

# ============================================================
# AVIATION SAR - RESCUE DECISION OPTIMIZATION
# ============================================================

print("=" * 60)
print("AVIATION SAR - RESCUE DECISION OPTIMIZATION")
print("=" * 60)

# ------------------------------------------------------------
# 1. File paths
# ------------------------------------------------------------

uav_file = r"D:\AviationSAR\dataset\flight\uav_search_plan_india.csv"

output_file = (
    r"D:\AviationSAR\dataset\flight\rescue_decision_results.csv"
)

# ------------------------------------------------------------
# 2. Load UAV search plan
# ------------------------------------------------------------

print("\nLoading UAV search plan...")

df = pd.read_csv(uav_file)

print(f"Total aircraft records: {len(df)}")

# ------------------------------------------------------------
# 3. Rescue priority
# ------------------------------------------------------------

def determine_rescue_priority(row):

    score = row["priority_score"]
    priority = row["search_priority"]

    if priority == "HIGH" and score >= 60:
        return "CRITICAL"

    elif priority == "HIGH":
        return "HIGH"

    elif priority == "MEDIUM":
        return "MEDIUM"

    else:
        return "LOW"


df["rescue_priority"] = df.apply(
    determine_rescue_priority,
    axis=1
)

# ------------------------------------------------------------
# 4. Rescue action
# ------------------------------------------------------------

def determine_action(priority):

    if priority == "CRITICAL":
        return "Immediate UAV Search and Rescue Deployment"

    elif priority == "HIGH":
        return "Priority UAV Search"

    elif priority == "MEDIUM":
        return "Scheduled UAV Search"

    else:
        return "Routine Monitoring"


df["recommended_action"] = df["rescue_priority"].apply(
    determine_action
)

# ------------------------------------------------------------
# 5. Estimated search time
# ------------------------------------------------------------

def estimate_search_time(radius):

    if radius <= 10:
        return "15-30 minutes"

    elif radius <= 20:
        return "30-60 minutes"

    else:
        return "60+ minutes"


df["estimated_search_time"] = df["search_radius_km"].apply(
    estimate_search_time
)

# ------------------------------------------------------------
# 6. Rescue team recommendation
# ------------------------------------------------------------

def recommend_team(priority):

    if priority == "CRITICAL":
        return "UAV + Ground Rescue + Medical Team"

    elif priority == "HIGH":
        return "UAV + Ground Rescue Team"

    elif priority == "MEDIUM":
        return "UAV Search Team"

    else:
        return "Monitoring Team"


df["recommended_rescue_team"] = df["rescue_priority"].apply(
    recommend_team
)

# ------------------------------------------------------------
# 7. Create final decision table
# ------------------------------------------------------------

result = df[
    [
        "icao24",
        "callsign",
        "time_position",
        "longitude",
        "latitude",
        "baro_altitude",
        "velocity",
        "true_track",
        "priority_score",
        "search_priority",
        "rescue_priority",
        "search_radius_km",
        "uav_id",
        "recommended_action",
        "estimated_search_time",
        "recommended_rescue_team"
    ]
].copy()

# ------------------------------------------------------------
# 8. Sort by rescue priority
# ------------------------------------------------------------

priority_order = {
    "CRITICAL": 1,
    "HIGH": 2,
    "MEDIUM": 3,
    "LOW": 4
}

result["priority_order"] = result["rescue_priority"].map(
    priority_order
)

result = result.sort_values(
    by=["priority_order", "priority_score"],
    ascending=[True, False]
)

result = result.drop(columns=["priority_order"])

# ------------------------------------------------------------
# 9. Save result
# ------------------------------------------------------------

result.to_csv(
    output_file,
    index=False
)

# ------------------------------------------------------------
# 10. Display summary
# ------------------------------------------------------------

print("\n==========================================")
print("RESCUE DECISION SUMMARY")
print("==========================================")

print("\nRescue priority distribution:")
print(result["rescue_priority"].value_counts())

print("\nRecommended actions:")
print(result["recommended_action"].value_counts())

print("\nTop 10 rescue decisions:")
print(
    result.head(10).to_string(index=False)
)

print("\n==========================================")
print("RESCUE DECISION OPTIMIZATION COMPLETED")
print("==========================================")

print("\nOutput saved to:")
print(output_file)

print("==========================================")