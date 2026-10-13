import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

print("=" * 60)
print("AVIATION SAR - FINAL RESCUE DECISION MAP")
print("=" * 60)

# ---------------------------------------------------------
# File paths
# ---------------------------------------------------------

map_file = r"D:\AviationSAR\dataset\map\southern-zone.gpkg"

rescue_file = (
    r"D:\AviationSAR\dataset\flight\rescue_decision_results.csv"
)

output_file = r"D:\AviationSAR\final_rescue_decision_map.png"

# ---------------------------------------------------------
# Load India administrative boundaries
# ---------------------------------------------------------

print("\nLoading administrative boundaries...")

admin = gpd.read_file(
    map_file,
    layer="gis_osm_adminareas_a_free"
)

print("Administrative features:", len(admin))

# ---------------------------------------------------------
# Load rescue decisions
# ---------------------------------------------------------

print("\nLoading rescue decision data...")

df = pd.read_csv(rescue_file)

print("Total rescue records:", len(df))

# ---------------------------------------------------------
# Convert aircraft positions to GeoDataFrame
# ---------------------------------------------------------

points = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(
        df["longitude"],
        df["latitude"]
    ),
    crs="EPSG:4326"
)

# ---------------------------------------------------------
# Restrict to India map region
# ---------------------------------------------------------

india_region = points.cx[
    71.5:94.3,
    6.7:19.95
]

print(
    "Aircraft inside mapped region:",
    len(india_region)
)

# ---------------------------------------------------------
# Generate map
# ---------------------------------------------------------

print("\nGenerating final rescue decision map...")

fig, ax = plt.subplots(
    figsize=(12, 10)
)

admin.plot(
    ax=ax,
    facecolor="none",
    edgecolor="gray",
    linewidth=0.4
)

# ---------------------------------------------------------
# Plot LOW priority
# ---------------------------------------------------------

low = india_region[
    india_region["rescue_priority"] == "LOW"
]

ax.scatter(
    low["longitude"],
    low["latitude"],
    s=30,
    label="LOW",
    alpha=0.7
)

# ---------------------------------------------------------
# Plot MEDIUM priority
# ---------------------------------------------------------

medium = india_region[
    india_region["rescue_priority"] == "MEDIUM"
]

ax.scatter(
    medium["longitude"],
    medium["latitude"],
    s=70,
    label="MEDIUM",
    alpha=0.9
)

# ---------------------------------------------------------
# Plot CRITICAL priority
# ---------------------------------------------------------

critical = india_region[
    india_region["rescue_priority"] == "CRITICAL"
]

ax.scatter(
    critical["longitude"],
    critical["latitude"],
    s=120,
    marker="*",
    label="CRITICAL",
    alpha=1.0
)

# ---------------------------------------------------------
# Labels
# ---------------------------------------------------------

ax.set_title(
    "Aviation SAR - Final Rescue Decision Map",
    fontsize=16
)

ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

ax.legend()

ax.grid(
    True,
    alpha=0.3
)

plt.tight_layout()

# ---------------------------------------------------------
# Save
# ---------------------------------------------------------

plt.savefig(
    output_file,
    dpi=200,
    bbox_inches="tight"
)

plt.close()

print("\nMap saved to:")
print(output_file)

print("\n==========================================")
print("FINAL RESCUE DECISION MAP COMPLETED")
print("==========================================")