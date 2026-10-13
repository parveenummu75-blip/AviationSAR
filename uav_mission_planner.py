import pandas as pd
import math


# ============================================================
# AVIATION SAR - UAV MISSION PLANNER
# ============================================================

print("=" * 70)
print("        AVIATION SAR - UAV MISSION PLANNER")
print("=" * 70)


# ============================================================
# 1. LOAD DATASET
# ============================================================

DATA_FILE = r"D:\AviationSAR\dataset\flight\rescue_decision_results.csv"

df = pd.read_csv(DATA_FILE)

print()
print("Dataset loaded successfully.")
print("Total aircraft:", len(df))


# ============================================================
# 2. CHECK REQUIRED COLUMNS
# ============================================================

required_columns = [
    "icao24",
    "callsign",
    "longitude",
    "latitude",
    "priority_score",
    "search_priority",
    "rescue_priority",
    "search_radius_km",
    "uav_id",
    "recommended_action",
    "estimated_search_time",
    "recommended_rescue_team"
]


missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]


if missing_columns:

    print()
    print("ERROR: Required columns are missing:")

    for column in missing_columns:
        print(" -", column)

    raise SystemExit


# ============================================================
# 3. CLEAN NUMERICAL DATA
# ============================================================

df["latitude"] = pd.to_numeric(
    df["latitude"],
    errors="coerce"
)

df["longitude"] = pd.to_numeric(
    df["longitude"],
    errors="coerce"
)

df["priority_score"] = pd.to_numeric(
    df["priority_score"],
    errors="coerce"
)

df["search_radius_km"] = pd.to_numeric(
    df["search_radius_km"],
    errors="coerce"
)

df["uav_id"] = pd.to_numeric(
    df["uav_id"],
    errors="coerce"
)


# Remove rows without essential information

df = df.dropna(
    subset=[
        "latitude",
        "longitude",
        "priority_score",
        "search_radius_km",
        "uav_id"
    ]
)


# ============================================================
# 4. STANDARDIZE PRIORITY
# ============================================================

df["rescue_priority"] = (
    df["rescue_priority"]
    .astype(str)
    .str.strip()
    .str.upper()
)


df["search_priority"] = (
    df["search_priority"]
    .astype(str)
    .str.strip()
    .str.upper()
)


# ============================================================
# 5. CALCULATE SEARCH AREA
# ============================================================

def calculate_search_area(radius_km):

    return math.pi * (radius_km ** 2)


df["search_area_km2"] = (
    df["search_radius_km"]
    .apply(calculate_search_area)
)


# ============================================================
# 6. PRIORITY ORDER
# ============================================================

priority_order = {
    "CRITICAL": 1,
    "MEDIUM": 2,
    "LOW": 3
}


df["priority_order"] = (
    df["rescue_priority"]
    .map(priority_order)
    .fillna(4)
)


# ============================================================
# 7. SORT AIRCRAFT
# ============================================================

df = df.sort_values(
    by=[
        "priority_order",
        "priority_score"
    ],
    ascending=[
        True,
        False
    ]
)


# ============================================================
# 8. COUNT RESCUE PRIORITIES
# ============================================================

total_aircraft = len(df)


critical_df = df[
    df["rescue_priority"] == "CRITICAL"
].copy()


medium_df = df[
    df["rescue_priority"] == "MEDIUM"
].copy()


low_df = df[
    df["rescue_priority"] == "LOW"
].copy()


critical_count = len(critical_df)

medium_count = len(medium_df)

low_count = len(low_df)


# ============================================================
# 9. UAV INFORMATION
# ============================================================

uav_ids = (
    df["uav_id"]
    .astype(int)
    .unique()
)


uav_ids = sorted(uav_ids)

total_uavs = len(uav_ids)


# ============================================================
# 10. MISSION SUMMARY
# ============================================================

print()
print("-" * 70)
print("MISSION SUMMARY")
print("-" * 70)

print(
    "Total Aircraft       :",
    total_aircraft
)

print(
    "Critical Targets     :",
    critical_count
)

print(
    "Medium Targets       :",
    medium_count
)

print(
    "Low Targets          :",
    low_count
)

print(
    "Active UAVs           :",
    total_uavs
)


# ============================================================
# 11. UAV MISSION ALLOCATION
# ============================================================

print()
print("-" * 70)
print("UAV MISSION ALLOCATION")
print("-" * 70)


uav_summary = []


for uav_id in uav_ids:

    uav_data = df[
        df["uav_id"].astype(int) == int(uav_id)
    ].copy()


    uav_critical = len(
        uav_data[
            uav_data["rescue_priority"]
            == "CRITICAL"
        ]
    )


    uav_medium = len(
        uav_data[
            uav_data["rescue_priority"]
            == "MEDIUM"
        ]
    )


    uav_low = len(
        uav_data[
            uav_data["rescue_priority"]
            == "LOW"
        ]
    )


    total_targets = len(uav_data)


    # Determine UAV mission

    if uav_critical > 0:

        mission = "CRITICAL SEARCH & RESCUE"

    elif uav_medium > 0:

        mission = "MEDIUM PRIORITY SEARCH"

    else:

        mission = "ROUTINE SURVEILLANCE"


    uav_summary.append({

        "UAV ID": int(uav_id),

        "Total Targets": total_targets,

        "Critical": uav_critical,

        "Medium": uav_medium,

        "Low": uav_low,

        "Mission": mission

    })


    print(
        f"UAV {int(uav_id):02d} | "
        f"Targets: {total_targets:02d} | "
        f"Critical: {uav_critical:02d} | "
        f"Medium: {uav_medium:02d} | "
        f"Low: {uav_low:02d} | "
        f"Mission: {mission}"
    )


uav_summary_df = pd.DataFrame(
    uav_summary
)


# ============================================================
# 12. CRITICAL RESCUE TARGETS
# ============================================================

print()
print("-" * 70)
print("CRITICAL RESCUE TARGETS")
print("-" * 70)


if critical_count == 0:

    print(
        "No critical rescue targets found."
    )

else:

    for number, (_, row) in enumerate(
        critical_df.iterrows(),
        start=1
    ):

        print()
        print(
            f"Target {number}"
        )

        print(
            "Aircraft ID       :",
            row["icao24"]
        )

        print(
            "Callsign          :",
            row["callsign"]
        )

        print(
            "Latitude          :",
            row["latitude"]
        )

        print(
            "Longitude         :",
            row["longitude"]
        )

        print(
            "Priority Score    :",
            row["priority_score"]
        )

        print(
            "Search Priority   :",
            row["search_priority"]
        )

        print(
            "Rescue Priority   :",
            row["rescue_priority"]
        )

        print(
            "Search Radius     :",
            row["search_radius_km"],
            "km"
        )

        print(
            "Search Area       :",
            round(
                row["search_area_km2"],
                2
            ),
            "km²"
        )

        print(
            "Assigned UAV      :",
            int(row["uav_id"])
        )

        print(
            "Search Time       :",
            row["estimated_search_time"]
        )

        print(
            "Recommended Action:",
            row["recommended_action"]
        )

        print(
            "Rescue Team       :",
            row["recommended_rescue_team"]
        )


# ============================================================
# 13. SEARCH ZONE INFORMATION
# ============================================================

print()
print("-" * 70)
print("SEARCH ZONE INFORMATION")
print("-" * 70)


total_search_area = (
    df["search_area_km2"]
    .sum()
)


critical_search_area = (
    critical_df["search_area_km2"]
    .sum()
)


medium_search_area = (
    medium_df["search_area_km2"]
    .sum()
)


low_search_area = (
    low_df["search_area_km2"]
    .sum()
)


print(
    "Total Search Area    :",
    round(
        total_search_area,
        2
    ),
    "km²"
)


print(
    "Critical Search Area :",
    round(
        critical_search_area,
        2
    ),
    "km²"
)


print(
    "Medium Search Area   :",
    round(
        medium_search_area,
        2
    ),
    "km²"
)


print(
    "Low Search Area      :",
    round(
        low_search_area,
        2
    ),
    "km²"
)


# ============================================================
# 14. CREATE UAV MISSION PLAN
# ============================================================

mission_plan = df[
    [
        "icao24",
        "callsign",
        "latitude",
        "longitude",
        "priority_score",
        "search_priority",
        "rescue_priority",
        "search_radius_km",
        "search_area_km2",
        "uav_id",
        "recommended_action",
        "estimated_search_time",
        "recommended_rescue_team"
    ]
].copy()


# ============================================================
# 15. SAVE UAV MISSION PLAN
# ============================================================

OUTPUT_FILE = (
    r"D:\AviationSAR\dataset\flight\uav_mission_plan.csv"
)


mission_plan.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# 16. SAVE UAV SUMMARY
# ============================================================

UAV_SUMMARY_FILE = (
    r"D:\AviationSAR\dataset\flight\uav_summary.csv"
)


uav_summary_df.to_csv(
    UAV_SUMMARY_FILE,
    index=False
)


# ============================================================
# 17. FINAL RESULT
# ============================================================

print()
print("=" * 70)
print("        UAV MISSION PLANNING COMPLETED")
print("=" * 70)

print()

print(
    "Mission plan saved to:"
)

print(
    OUTPUT_FILE
)

print()

print(
    "UAV summary saved to:"
)

print(
    UAV_SUMMARY_FILE
)

print()

print(
    "Total UAVs        :",
    total_uavs
)

print(
    "Total Targets     :",
    total_aircraft
)

print(
    "Critical Targets  :",
    critical_count
)

print(
    "Medium Targets    :",
    medium_count
)

print(
    "Low Targets       :",
    low_count
)

print()

print("=" * 70)