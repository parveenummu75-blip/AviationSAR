import pandas as pd
import os
import math

# ==========================================
# AVIATION SAR - UAV SEARCH PLANNING
# ==========================================

print("=" * 50)
print("AVIATION SAR - UAV SEARCH PLANNING")
print("=" * 50)

# ------------------------------------------
# Input dataset
# ------------------------------------------

input_file = r"D:\AviationSAR\dataset\flight\aircraft_last_known_positions.csv"

print("\nLoading aircraft last-known positions...")

df = pd.read_csv(input_file)

print("Total aircraft:", len(df))

# ------------------------------------------
# Select airborne aircraft
# ------------------------------------------

if "on_ground" in df.columns:
    df = df[df["on_ground"] == False].copy()

print("Airborne aircraft:", len(df))

# ------------------------------------------
# Remove invalid coordinates
# ------------------------------------------

df = df.dropna(subset=["latitude", "longitude"])

df = df[
    (df["latitude"] >= -90) &
    (df["latitude"] <= 90) &
    (df["longitude"] >= -180) &
    (df["longitude"] <= 180)
].copy()

# ------------------------------------------
# Calculate search priority
# ------------------------------------------

def calculate_priority(row):

    altitude = row["baro_altitude"]
    velocity = row["velocity"]

    score = 0

    # Lower altitude = higher search priority
    if altitude < 3000:
        score += 40
    elif altitude < 6000:
        score += 25
    elif altitude < 9000:
        score += 10

    # Abnormal/low velocity
    if velocity < 100:
        score += 40
    elif velocity < 180:
        score += 20

    return score


df["priority_score"] = df.apply(calculate_priority, axis=1)

# ------------------------------------------
# Assign UAV priority
# ------------------------------------------

def assign_priority(score):

    if score >= 60:
        return "HIGH"
    elif score >= 30:
        return "MEDIUM"
    else:
        return "LOW"


df["search_priority"] = df["priority_score"].apply(assign_priority)

# ------------------------------------------
# Estimate search radius
# ------------------------------------------

def search_radius(priority):

    if priority == "HIGH":
        return 10

    elif priority == "MEDIUM":
        return 20

    else:
        return 30


df["search_radius_km"] = df["search_priority"].apply(search_radius)

# ------------------------------------------
# UAV assignment
# ------------------------------------------

df = df.sort_values(
    by="priority_score",
    ascending=False
).reset_index(drop=True)

df["uav_id"] = (df.index % 5) + 1

# ------------------------------------------
# Save results
# ------------------------------------------

output_file = r"D:\AviationSAR\dataset\flight\uav_search_plan.csv"

df[
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
        "search_radius_km",
        "uav_id"
    ]
].to_csv(output_file, index=False)

# ------------------------------------------
# Display summary
# ------------------------------------------

print("\n==========================================")
print("UAV SEARCH PLANNING RESULTS")
print("==========================================")

print("\nPriority distribution:")

print(
    df["search_priority"].value_counts()
)

print("\nTop 10 search locations:")

print(
    df[
        [
            "callsign",
            "latitude",
            "longitude",
            "priority_score",
            "search_priority",
            "search_radius_km",
            "uav_id"
        ]
    ].head(10).to_string(index=False)
)

print("\n==========================================")
print("UAV SEARCH PLANNING COMPLETED")
print("==========================================")

print("\nOutput saved to:")
print(output_file)

print("==========================================")