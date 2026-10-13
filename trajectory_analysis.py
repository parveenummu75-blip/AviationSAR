import pandas as pd

# ============================================================
# MODULE 3: FLIGHT TRAJECTORY ANALYSIS
# ============================================================

file_path = r"D:\AviationSAR\dataset\flight\opensky_cleaned.csv"

print("\nLoading cleaned flight data...")

df = pd.read_csv(file_path)

# Convert timestamp
df["time_position"] = pd.to_datetime(df["time_position"])

# Sort by aircraft and time
df = df.sort_values(
    ["icao24", "time_position"]
)

print("\nTotal flight records:", len(df))

# Number of unique aircraft
print("Unique aircraft:", df["icao24"].nunique())


# ------------------------------------------------------------
# Find aircraft with multiple trajectory points
# ------------------------------------------------------------

trajectory_counts = df.groupby("icao24").size()

print("\nTrajectory statistics:")
print(trajectory_counts.describe())


# Keep aircraft having at least 5 position records
valid_aircraft = trajectory_counts[
    trajectory_counts >= 5
].index

trajectory_df = df[
    df["icao24"].isin(valid_aircraft)
].copy()


# ------------------------------------------------------------
# Save trajectory dataset
# ------------------------------------------------------------

output_file = r"D:\AviationSAR\dataset\flight\flight_trajectories.csv"

trajectory_df.to_csv(
    output_file,
    index=False
)


# ------------------------------------------------------------
# Display sample trajectory
# ------------------------------------------------------------

if len(valid_aircraft) > 0:

    aircraft_id = valid_aircraft[0]

    sample = trajectory_df[
        trajectory_df["icao24"] == aircraft_id
    ]

    print("\n==========================================")
    print("SAMPLE FLIGHT TRAJECTORY")
    print("==========================================")

    print("Aircraft ID:", aircraft_id)

    print(
        sample[
            [
                "icao24",
                "callsign",
                "time_position",
                "longitude",
                "latitude",
                "baro_altitude",
                "velocity",
                "true_track",
                "vertical_rate"
            ]
        ].head(10).to_string(index=False)
    )

    print("\nTrajectory points:", len(sample))

else:

    print("\nNo aircraft has enough trajectory points.")


print("\n==========================================")
print("TRAJECTORY ANALYSIS COMPLETED")
print("==========================================")

print("Trajectory dataset saved to:")
print(output_file)

print("==========================================")