import pandas as pd
from datetime import datetime


# ============================================================
# AVIATION SAR - RESCUE TEAM DEPLOYMENT
# ============================================================

print("=" * 75)
print("             AVIATION SAR - RESCUE TEAM DEPLOYMENT")
print("=" * 75)


# ============================================================
# FILE PATHS
# ============================================================

DECISION_FILE = (
    r"D:\AviationSAR\dataset\flight"
    r"\rescue_decision_results.csv"
)

SEARCH_FILE = (
    r"D:\AviationSAR\dataset\flight"
    r"\uav_search_results.csv"
)

OUTPUT_FILE = (
    r"D:\AviationSAR\dataset\flight"
    r"\rescue_deployment_plan.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

print()
print("Loading rescue decision data...")

try:

    decision_df = pd.read_csv(
        DECISION_FILE
    )

except Exception as e:

    print("ERROR: Cannot load rescue decision file.")
    print(e)
    raise SystemExit


print(
    "Rescue decision data loaded successfully."
)


print()
print("Loading UAV search results...")

try:

    search_df = pd.read_csv(
        SEARCH_FILE
    )

except Exception as e:

    print("ERROR: Cannot load UAV search results.")
    print(e)
    raise SystemExit


print(
    "UAV search results loaded successfully."
)


# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

decision_columns = [

    "icao24",
    "callsign",
    "latitude",
    "longitude",
    "priority_score",
    "search_priority",
    "rescue_priority",
    "search_radius_km",
    "uav_id",
    "recommended_action",
    "estimated_search_time",
    "recommended_rescue_team"

]


search_columns = [

    "icao24",
    "callsign",
    "uav_id",
    "search_status"

]


missing_decision = [

    column

    for column in decision_columns

    if column not in decision_df.columns

]


missing_search = [

    column

    for column in search_columns

    if column not in search_df.columns

]


if missing_decision:

    print()
    print(
        "ERROR: Missing columns in rescue decision file:"
    )

    for column in missing_decision:

        print(
            "-",
            column
        )

    raise SystemExit


if missing_search:

    print()
    print(
        "ERROR: Missing columns in search result file:"
    )

    for column in missing_search:

        print(
            "-",
            column
        )

    raise SystemExit


# ============================================================
# CLEAN DATA
# ============================================================

decision_df["rescue_priority"] = (

    decision_df["rescue_priority"]
    .astype(str)
    .str.strip()
    .str.upper()

)


search_df["search_status"] = (

    search_df["search_status"]
    .astype(str)
    .str.strip()
    .str.upper()

)


decision_df["uav_id"] = pd.to_numeric(

    decision_df["uav_id"],

    errors="coerce"

)


decision_df["priority_score"] = pd.to_numeric(

    decision_df["priority_score"],

    errors="coerce"

)


decision_df["latitude"] = pd.to_numeric(

    decision_df["latitude"],

    errors="coerce"

)


decision_df["longitude"] = pd.to_numeric(

    decision_df["longitude"],

    errors="coerce"

)


decision_df = decision_df.dropna(

    subset=[
        "latitude",
        "longitude",
        "uav_id"
    ]

)


# ============================================================
# RESCUE PRIORITY ORDER
# ============================================================

priority_order = {

    "CRITICAL": 1,
    "MEDIUM": 2,
    "LOW": 3

}


# ============================================================
# CREATE RESCUE DEPLOYMENT PLAN
# ============================================================

deployment_results = []


print()
print("=" * 75)
print("                  RESCUE DEPLOYMENT")
print("=" * 75)


# Sort highest priority first

decision_df["priority_rank"] = (

    decision_df["rescue_priority"]
    .map(priority_order)
    .fillna(4)

)


decision_df = decision_df.sort_values(

    by=[
        "priority_rank",
        "priority_score"
    ],

    ascending=[
        True,
        False
    ]

)


# ============================================================
# PROCESS EACH AIRCRAFT
# ============================================================

for _, row in decision_df.iterrows():

    icao24 = str(
        row["icao24"]
    )

    callsign = str(
        row["callsign"]
    )

    latitude = float(
        row["latitude"]
    )

    longitude = float(
        row["longitude"]
    )

    priority = str(
        row["rescue_priority"]
    ).upper()

    score = float(
        row["priority_score"]
    )

    uav_id = int(
        row["uav_id"]
    )


    # --------------------------------------------------------
    # CHECK SEARCH STATUS
    # --------------------------------------------------------

    matching_search = search_df[

        search_df["icao24"]
        .astype(str)
        ==
        icao24

    ]


    if not matching_search.empty:

        search_status = str(

            matching_search.iloc[0][
                "search_status"
            ]

        ).upper()

    else:

        search_status = "NOT FOUND"


    # --------------------------------------------------------
    # DETERMINE DEPLOYMENT STATUS
    # --------------------------------------------------------

    if search_status == "SEARCH COMPLETED":

        deployment_status = (
            "READY FOR RESCUE"
        )

    else:

        deployment_status = (
            "WAITING FOR SEARCH"
        )


    # --------------------------------------------------------
    # RESCUE TEAM
    # --------------------------------------------------------

    rescue_team = str(

        row[
            "recommended_rescue_team"
        ]

    )


    # --------------------------------------------------------
    # RECOMMENDED ACTION
    # --------------------------------------------------------

    recommended_action = str(

        row[
            "recommended_action"
        ]

    )


    # --------------------------------------------------------
    # RESPONSE LEVEL
    # --------------------------------------------------------

    if priority == "CRITICAL":

        response_level = (
            "IMMEDIATE RESPONSE"
        )

        response_time = (
            "0-15 minutes"
        )

    elif priority == "MEDIUM":

        response_level = (
            "HIGH PRIORITY RESPONSE"
        )

        response_time = (
            "15-30 minutes"
        )

    else:

        response_level = (
            "NORMAL RESPONSE"
        )

        response_time = (
            "30-60 minutes"
        )


    # --------------------------------------------------------
    # RESCUE STATUS
    # --------------------------------------------------------

    rescue_status = (

        "DEPLOYMENT READY"

        if search_status
        ==
        "SEARCH COMPLETED"

        else

        "NOT READY"

    )


    # --------------------------------------------------------
    # TIMESTAMP
    # --------------------------------------------------------

    deployment_time = (

        datetime.now()
        .strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    )


    # --------------------------------------------------------
    # PRINT
    # --------------------------------------------------------

    print()

    print(
        f"Aircraft        : {callsign}"
    )

    print(
        f"Priority        : {priority}"
    )

    print(
        f"Priority Score  : {score:.0f}"
    )

    print(
        f"Location        : "
        f"{latitude:.4f}, "
        f"{longitude:.4f}"
    )

    print(
        f"Assigned UAV    : "
        f"UAV {uav_id:02d}"
    )

    print(
        f"Search Status   : "
        f"{search_status}"
    )

    print(
        f"Rescue Team     : "
        f"{rescue_team}"
    )

    print(
        f"Response Level  : "
        f"{response_level}"
    )

    print(
        f"Response Time   : "
        f"{response_time}"
    )

    print(
        f"Rescue Status   : "
        f"{rescue_status}"
    )


    # --------------------------------------------------------
    # SAVE RESULT
    # --------------------------------------------------------

    deployment_results.append({

        "icao24":
            icao24,

        "callsign":
            callsign,

        "latitude":
            latitude,

        "longitude":
            longitude,

        "priority_score":
            score,

        "rescue_priority":
            priority,

        "uav_id":
            uav_id,

        "search_status":
            search_status,

        "deployment_status":
            deployment_status,

        "response_level":
            response_level,

        "response_time":
            response_time,

        "recommended_action":
            recommended_action,

        "recommended_rescue_team":
            rescue_team,

        "rescue_status":
            rescue_status,

        "deployment_timestamp":
            deployment_time

    })


# ============================================================
# CREATE DATAFRAME
# ============================================================

deployment_df = pd.DataFrame(
    deployment_results
)


# ============================================================
# SAVE FILE
# ============================================================

deployment_df.to_csv(

    OUTPUT_FILE,

    index=False

)


# ============================================================
# SUMMARY
# ============================================================

total_targets = len(
    deployment_df
)


ready_targets = len(

    deployment_df[
        deployment_df[
            "rescue_status"
        ]
        ==
        "DEPLOYMENT READY"
    ]

)


critical_targets = len(

    deployment_df[
        deployment_df[
            "rescue_priority"
        ]
        ==
        "CRITICAL"
    ]

)


medium_targets = len(

    deployment_df[
        deployment_df[
            "rescue_priority"
        ]
        ==
        "MEDIUM"
    ]

)


low_targets = len(

    deployment_df[
        deployment_df[
            "rescue_priority"
        ]
        ==
        "LOW"
    ]

)


# ============================================================
# FINAL OUTPUT
# ============================================================

print()
print("=" * 75)
print("             RESCUE DEPLOYMENT COMPLETED")
print("=" * 75)

print()

print(
    f"Total Targets        : "
    f"{total_targets}"
)

print(
    f"Critical Targets     : "
    f"{critical_targets}"
)

print(
    f"Medium Targets       : "
    f"{medium_targets}"
)

print(
    f"Low Targets          : "
    f"{low_targets}"
)

print(
    f"Ready for Rescue     : "
    f"{ready_targets}"
)

print()

print(
    "Rescue deployment plan saved to:"
)

print(
    OUTPUT_FILE
)

print()
print("=" * 75)