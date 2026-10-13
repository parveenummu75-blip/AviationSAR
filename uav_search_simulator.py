import pandas as pd
import math
from datetime import datetime


# ============================================================
# AVIATION SAR - UAV SEARCH SIMULATOR
# ============================================================

print("=" * 75)
print("                 AVIATION SAR - UAV SEARCH SIMULATOR")
print("=" * 75)


# ============================================================
# FILE PATHS
# ============================================================

MISSION_FILE = (
    r"D:\AviationSAR\dataset\flight"
    r"\uav_mission_plan.csv"
)

ROUTE_FILE = (
    r"D:\AviationSAR\dataset\flight"
    r"\uav_routes.csv"
)

OUTPUT_FILE = (
    r"D:\AviationSAR\dataset\flight"
    r"\uav_search_results.csv"
)


# ============================================================
# LOAD FILES
# ============================================================

print()
print("Loading UAV mission plan...")

try:

    mission_df = pd.read_csv(
        MISSION_FILE
    )

except Exception as e:

    print()
    print("ERROR: Cannot load UAV mission plan.")
    print(e)

    raise SystemExit


print("Mission plan loaded successfully.")


print()
print("Loading UAV routes...")

try:

    route_df = pd.read_csv(
        ROUTE_FILE
    )

except Exception as e:

    print()
    print("ERROR: Cannot load UAV route file.")
    print(e)

    raise SystemExit


print("Route file loaded successfully.")


# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

required_mission_columns = [
    "icao24",
    "callsign",
    "latitude",
    "longitude",
    "priority_score",
    "rescue_priority",
    "search_radius_km",
    "uav_id"
]


required_route_columns = [
    "uav_id",
    "route_order",
    "icao24",
    "callsign",
    "latitude",
    "longitude",
    "rescue_priority"
]


missing_mission = [
    column
    for column in required_mission_columns
    if column not in mission_df.columns
]


missing_route = [
    column
    for column in required_route_columns
    if column not in route_df.columns
]


if missing_mission:

    print()
    print("ERROR: Missing columns in mission plan:")

    for column in missing_mission:
        print("-", column)

    raise SystemExit


if missing_route:

    print()
    print("ERROR: Missing columns in route file:")

    for column in missing_route:
        print("-", column)

    raise SystemExit


# ============================================================
# CLEAN DATA
# ============================================================

mission_df["uav_id"] = pd.to_numeric(
    mission_df["uav_id"],
    errors="coerce"
)

mission_df["latitude"] = pd.to_numeric(
    mission_df["latitude"],
    errors="coerce"
)

mission_df["longitude"] = pd.to_numeric(
    mission_df["longitude"],
    errors="coerce"
)

mission_df["priority_score"] = pd.to_numeric(
    mission_df["priority_score"],
    errors="coerce"
)

mission_df["search_radius_km"] = pd.to_numeric(
    mission_df["search_radius_km"],
    errors="coerce"
)


route_df["uav_id"] = pd.to_numeric(
    route_df["uav_id"],
    errors="coerce"
)

route_df["route_order"] = pd.to_numeric(
    route_df["route_order"],
    errors="coerce"
)

route_df["latitude"] = pd.to_numeric(
    route_df["latitude"],
    errors="coerce"
)

route_df["longitude"] = pd.to_numeric(
    route_df["longitude"],
    errors="coerce"
)


mission_df["rescue_priority"] = (
    mission_df["rescue_priority"]
    .astype(str)
    .str.strip()
    .str.upper()
)


route_df["rescue_priority"] = (
    route_df["rescue_priority"]
    .astype(str)
    .str.strip()
    .str.upper()
)


mission_df = mission_df.dropna(
    subset=[
        "uav_id",
        "latitude",
        "longitude"
    ]
)


route_df = route_df.dropna(
    subset=[
        "uav_id",
        "route_order",
        "latitude",
        "longitude"
    ]
)


# ============================================================
# HAVERSINE DISTANCE
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
# SEARCH COVERAGE CALCULATION
# ============================================================

def search_area(radius_km):

    return math.pi * (
        radius_km ** 2
    )


# ============================================================
# SEARCH TIME ESTIMATION
# ============================================================

def estimate_search_time(
    priority,
    radius_km
):

    if priority == "CRITICAL":

        base_time = 15

    elif priority == "MEDIUM":

        base_time = 25

    else:

        base_time = 40


    additional_time = (
        radius_km * 2
    )


    return round(
        base_time + additional_time,
        1
    )


# ============================================================
# UAV SEARCH SIMULATION
# ============================================================

uav_ids = sorted(
    route_df["uav_id"]
    .astype(int)
    .unique()
)


search_results = []


print()
print("Active UAVs:", len(uav_ids))


for uav_id in uav_ids:

    print()
    print("=" * 75)
    print(
        f"UAV {uav_id:02d} SEARCH MISSION"
    )
    print("=" * 75)


    # --------------------------------------------------------
    # GET ROUTE FOR CURRENT UAV
    # --------------------------------------------------------

    uav_route = route_df[
        route_df["uav_id"].astype(int)
        == int(uav_id)
    ].copy()


    uav_route = uav_route.sort_values(
        by="route_order"
    )


    if uav_route.empty:

        print(
            "No assigned targets."
        )

        continue


    # --------------------------------------------------------
    # SEARCH EACH TARGET
    # --------------------------------------------------------

    previous_latitude = None
    previous_longitude = None


    total_travel_distance = 0.0
    total_search_area = 0.0
    total_search_time = 0.0


    for _, route_row in uav_route.iterrows():

        route_order = int(
            route_row["route_order"]
        )


        icao24 = str(
            route_row["icao24"]
        )


        callsign = str(
            route_row["callsign"]
        )


        latitude = float(
            route_row["latitude"]
        )


        longitude = float(
            route_row["longitude"]
        )


        priority = str(
            route_row["rescue_priority"]
        ).upper()


        # ----------------------------------------------------
        # FIND ORIGINAL MISSION DATA
        # ----------------------------------------------------

        matching = mission_df[
            (
                mission_df["icao24"]
                .astype(str)
                == icao24
            )
            &
            (
                mission_df["uav_id"].astype(int)
                == int(uav_id)
            )
        ]


        if not matching.empty:

            mission_row = matching.iloc[0]

            priority_score = float(
                mission_row["priority_score"]
            )

            radius_km = float(
                mission_row["search_radius_km"]
            )

        else:

            priority_score = 0.0

            radius_km = 10.0


        # ----------------------------------------------------
        # CALCULATE DISTANCE FROM PREVIOUS TARGET
        # ----------------------------------------------------

        if previous_latitude is None:

            distance_from_previous = 0.0

        else:

            distance_from_previous = haversine(

                previous_latitude,

                previous_longitude,

                latitude,

                longitude

            )


        total_travel_distance += (
            distance_from_previous
        )


        # ----------------------------------------------------
        # SEARCH AREA
        # ----------------------------------------------------

        area_km2 = search_area(
            radius_km
        )


        total_search_area += area_km2


        # ----------------------------------------------------
        # SEARCH TIME
        # ----------------------------------------------------

        search_time_minutes = (
            estimate_search_time(
                priority,
                radius_km
            )
        )


        total_search_time += (
            search_time_minutes
        )


        # ----------------------------------------------------
        # SEARCH STATUS
        # ----------------------------------------------------

        search_status = "SEARCH COMPLETED"


        search_timestamp = (
            datetime.now()
            .strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )


        # ----------------------------------------------------
        # PRINT SEARCH INFORMATION
        # ----------------------------------------------------

        print()

        print(
            f"Search Stop       : {route_order}"
        )

        print(
            f"Aircraft          : {callsign}"
        )

        print(
            f"Priority          : {priority}"
        )

        print(
            f"Priority Score    : {priority_score:.0f}"
        )

        print(
            f"Latitude          : {latitude:.4f}"
        )

        print(
            f"Longitude         : {longitude:.4f}"
        )

        print(
            f"Search Radius     : {radius_km:.2f} km"
        )

        print(
            f"Search Area       : {area_km2:.2f} km²"
        )

        print(
            f"Travel Distance   : "
            f"{distance_from_previous:.2f} km"
        )

        print(
            f"Estimated Search  : "
            f"{search_time_minutes:.1f} minutes"
        )

        print(
            f"Status            : {search_status}"
        )


        # ----------------------------------------------------
        # SAVE RESULT
        # ----------------------------------------------------

        search_results.append({

            "uav_id":
                int(uav_id),

            "route_order":
                route_order,

            "icao24":
                icao24,

            "callsign":
                callsign,

            "latitude":
                latitude,

            "longitude":
                longitude,

            "priority_score":
                priority_score,

            "rescue_priority":
                priority,

            "search_radius_km":
                radius_km,

            "search_area_km2":
                round(
                    area_km2,
                    2
                ),

            "distance_from_previous_km":
                round(
                    distance_from_previous,
                    2
                ),

            "estimated_search_time_min":
                search_time_minutes,

            "search_status":
                search_status,

            "search_timestamp":
                search_timestamp

        })


        previous_latitude = latitude

        previous_longitude = longitude


    # --------------------------------------------------------
    # UAV SUMMARY
    # --------------------------------------------------------

    print()
    print(
        "-" * 75
    )

    print(
        f"UAV {uav_id:02d} SEARCH COMPLETED"
    )

    print(
        f"Targets searched      : "
        f"{len(uav_route)}"
    )

    print(
        f"Travel distance       : "
        f"{total_travel_distance:.2f} km"
    )

    print(
        f"Search area covered   : "
        f"{total_search_area:.2f} km²"
    )

    print(
        f"Estimated search time : "
        f"{total_search_time:.1f} minutes"
    )


# ============================================================
# CREATE OUTPUT DATAFRAME
# ============================================================

results_df = pd.DataFrame(
    search_results
)


# ============================================================
# SAVE SEARCH RESULTS
# ============================================================

results_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print()
print("=" * 75)
print("                 UAV SEARCH COMPLETED")
print("=" * 75)

print()

print(
    "Total UAVs:",
    results_df["uav_id"].nunique()
)

print(
    "Total targets searched:",
    len(results_df)
)

print(
    "Total search area:",
    round(
        results_df["search_area_km2"].sum(),
        2
    ),
    "km²"
)

print(
    "Total travel distance:",
    round(
        results_df[
            "distance_from_previous_km"
        ].sum(),
        2
    ),
    "km"
)

print()

print(
    "Search results saved to:"
)

print(
    OUTPUT_FILE
)

print()

print("=" * 75)