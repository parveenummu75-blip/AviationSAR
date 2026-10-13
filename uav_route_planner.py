import pandas as pd
import math


# ============================================================
# AVIATION SAR - UAV ROUTE PLANNER
# ============================================================

print("=" * 70)
print("             AVIATION SAR - UAV ROUTE PLANNER")
print("=" * 70)


# ============================================================
# 1. LOAD UAV MISSION PLAN
# ============================================================

INPUT_FILE = (
    r"D:\AviationSAR\dataset\flight"
    r"\uav_mission_plan.csv"
)

df = pd.read_csv(INPUT_FILE)


print()
print("UAV mission plan loaded successfully.")
print("Total assigned targets:", len(df))


# ============================================================
# 2. CHECK REQUIRED COLUMNS
# ============================================================

required_columns = [
    "icao24",
    "callsign",
    "latitude",
    "longitude",
    "priority_score",
    "rescue_priority",
    "uav_id"
]


missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]


if missing_columns:

    print()
    print("ERROR: Missing columns:")

    for column in missing_columns:
        print("-", column)

    raise SystemExit


# ============================================================
# 3. CLEAN DATA
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

df["uav_id"] = pd.to_numeric(
    df["uav_id"],
    errors="coerce"
)


df["rescue_priority"] = (
    df["rescue_priority"]
    .astype(str)
    .str.strip()
    .str.upper()
)


df = df.dropna(
    subset=[
        "latitude",
        "longitude",
        "uav_id"
    ]
)


# ============================================================
# 4. HAVERSINE DISTANCE
# ============================================================

def haversine(
    lat1,
    lon1,
    lat2,
    lon2
):

    earth_radius = 6371.0


    lat1 = math.radians(lat1)

    lon1 = math.radians(lon1)

    lat2 = math.radians(lat2)

    lon2 = math.radians(lon2)


    dlat = lat2 - lat1

    dlon = lon2 - lon1


    a = (
        math.sin(dlat / 2) ** 2
        +
        math.cos(lat1)
        *
        math.cos(lat2)
        *
        math.sin(dlon / 2) ** 2
    )


    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )


    return earth_radius * c


# ============================================================
# 5. PRIORITY RANK
# ============================================================

priority_rank = {

    "CRITICAL": 1,

    "MEDIUM": 2,

    "LOW": 3

}


df["priority_rank"] = (
    df["rescue_priority"]
    .map(priority_rank)
    .fillna(4)
)


# ============================================================
# 6. GET UAV LIST
# ============================================================

uav_ids = sorted(
    df["uav_id"]
    .astype(int)
    .unique()
)


print()
print("Active UAVs:", len(uav_ids))


# ============================================================
# 7. ROUTE PLANNING
# ============================================================

all_routes = []


for uav_id in uav_ids:

    print()
    print("-" * 70)
    print(
        f"UAV {uav_id:02d} ROUTE"
    )
    print("-" * 70)


    uav_targets = df[
        df["uav_id"].astype(int)
        == int(uav_id)
    ].copy()


    # --------------------------------------------------------
    # START WITH HIGHEST PRIORITY TARGET
    # --------------------------------------------------------

    uav_targets = uav_targets.sort_values(
        by=[
            "priority_rank",
            "priority_score"
        ],
        ascending=[
            True,
            False
        ]
    )


    unvisited = (
        uav_targets
        .index
        .tolist()
    )


    if not unvisited:

        continue


    # Start at highest priority target

    current_index = unvisited.pop(0)


    route_order = 1

    total_distance = 0.0


    while True:

        current_row = df.loc[
            current_index
        ]


        # Save current target

        all_routes.append({

            "uav_id":
                int(uav_id),

            "route_order":
                route_order,

            "icao24":
                current_row["icao24"],

            "callsign":
                current_row["callsign"],

            "latitude":
                current_row["latitude"],

            "longitude":
                current_row["longitude"],

            "priority_score":
                current_row["priority_score"],

            "rescue_priority":
                current_row["rescue_priority"],

            "distance_from_previous_km":
                0.0 if route_order == 1
                else distance_to_next

        })


        print(
            f"{route_order}. "
            f"{current_row['callsign']} | "
            f"{current_row['rescue_priority']} | "
            f"Lat: {current_row['latitude']:.4f} | "
            f"Lon: {current_row['longitude']:.4f}"
        )


        if not unvisited:

            break


        # ----------------------------------------------------
        # FIND NEXT TARGET
        # ----------------------------------------------------

        best_index = None

        best_distance = float("inf")


        for candidate_index in unvisited:

            candidate_row = df.loc[
                candidate_index
            ]


            distance = haversine(

                current_row["latitude"],

                current_row["longitude"],

                candidate_row["latitude"],

                candidate_row["longitude"]

            )


            # Priority has higher importance

            current_priority = priority_rank.get(
                current_row["rescue_priority"],
                4
            )

            candidate_priority = priority_rank.get(
                candidate_row["rescue_priority"],
                4
            )


            # Prefer higher-priority targets.
            # If same priority, choose nearest.

            if candidate_priority < current_priority:

                if best_index is None:

                    best_index = candidate_index

                    best_distance = distance

                elif candidate_priority < priority_rank.get(
                    df.loc[best_index]["rescue_priority"],
                    4
                ):

                    best_index = candidate_index

                    best_distance = distance

                elif (
                    candidate_priority
                    ==
                    priority_rank.get(
                        df.loc[best_index]["rescue_priority"],
                        4
                    )
                    and distance < best_distance
                ):

                    best_index = candidate_index

                    best_distance = distance


            elif candidate_priority == current_priority:

                if distance < best_distance:

                    best_index = candidate_index

                    best_distance = distance


        # ----------------------------------------------------
        # IF NO SAME/HIGHER PRIORITY TARGET FOUND
        # SELECT NEAREST REMAINING TARGET
        # ----------------------------------------------------

        if best_index is None:

            for candidate_index in unvisited:

                candidate_row = df.loc[
                    candidate_index
                ]


                distance = haversine(

                    current_row["latitude"],

                    current_row["longitude"],

                    candidate_row["latitude"],

                    candidate_row["longitude"]

                )


                if distance < best_distance:

                    best_index = candidate_index

                    best_distance = distance


        distance_to_next = best_distance

        total_distance += best_distance


        # Remove selected target

        unvisited.remove(
            best_index
        )


        current_index = best_index

        route_order += 1


    print()
    print(
        "Total Route Distance:",
        round(total_distance, 2),
        "km"
    )


# ============================================================
# 8. CREATE ROUTE DATAFRAME
# ============================================================

route_df = pd.DataFrame(
    all_routes
)


# ============================================================
# 9. SAVE ROUTES
# ============================================================

OUTPUT_FILE = (
    r"D:\AviationSAR\dataset\flight"
    r"\uav_routes.csv"
)


route_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# 10. UAV ROUTE SUMMARY
# ============================================================

route_summary = []


for uav_id in uav_ids:

    uav_route = route_df[
        route_df["uav_id"].astype(int)
        == int(uav_id)
    ]


    total_targets = len(
        uav_route
    )


    total_distance = (
        uav_route[
            "distance_from_previous_km"
        ]
        .sum()
    )


    route_summary.append({

        "UAV ID":
            int(uav_id),

        "Targets":
            total_targets,

        "Route Distance km":
            round(
                total_distance,
                2
            )

    })


route_summary_df = pd.DataFrame(
    route_summary
)


SUMMARY_FILE = (
    r"D:\AviationSAR\dataset\flight"
    r"\uav_route_summary.csv"
)


route_summary_df.to_csv(
    SUMMARY_FILE,
    index=False
)


# ============================================================
# 11. FINAL OUTPUT
# ============================================================

print()
print("=" * 70)
print("             UAV ROUTE PLANNING COMPLETED")
print("=" * 70)

print()

print(
    "Route file saved to:"
)

print(
    OUTPUT_FILE
)

print()

print(
    "Route summary saved to:"
)

print(
    SUMMARY_FILE
)

print()

print(
    route_summary_df.to_string(
        index=False
    )
)

print()
print("=" * 70)