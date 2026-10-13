import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

print("=" * 50)
print("AVIATION SAR - UAV SEARCH MAP")
print("=" * 50)

# ==================================================
# 1. Load administrative map from GeoPackage
# ==================================================

map_file = r"D:\AviationSAR\dataset\map\southern-zone.gpkg"
layer_name = "gis_osm_adminareas_a_free"

print("\nLoading administrative boundaries...")

admin = gpd.read_file(
    map_file,
    layer=layer_name
)

print("Administrative features:", len(admin))
print("CRS:", admin.crs)

# ==================================================
# 2. Load UAV search plan
# ==================================================

uav_file = r"D:\AviationSAR\dataset\flight\uav_search_plan_india.csv"

print("\nLoading UAV search plan...")

df = pd.read_csv(uav_file)

print("Total UAV records:", len(df))

# ==================================================
# 3. Keep only aircraft inside map region
# ==================================================

min_lon = 71.5
max_lon = 94.3
min_lat = 6.7
max_lat = 19.9

india_df = df[
    (df["longitude"] >= min_lon) &
    (df["longitude"] <= max_lon) &
    (df["latitude"] >= min_lat) &
    (df["latitude"] <= max_lat)
].copy()

print("Aircraft inside map region:", len(india_df))

# ==================================================
# 4. Convert UAV points to GeoDataFrame
# ==================================================

uav_points = gpd.GeoDataFrame(
    india_df,
    geometry=gpd.points_from_xy(
        india_df["longitude"],
        india_df["latitude"]
    ),
    crs="EPSG:4326"
)

# Convert map to WGS84
if admin.crs != "EPSG:4326":
    admin = admin.to_crs("EPSG:4326")

# ==================================================
# 5. Generate map
# ==================================================

print("\nGenerating UAV search map...")

fig, ax = plt.subplots(figsize=(12, 10))

# Administrative boundaries
admin.plot(
    ax=ax,
    facecolor="none",
    edgecolor="black",
    linewidth=0.5
)

# ==================================================
# 6. Plot search priorities
# ==================================================

priority_settings = {
    "HIGH": {
        "color": "red",
        "size": 60
    },
    "MEDIUM": {
        "color": "orange",
        "size": 50
    },
    "LOW": {
        "color": "blue",
        "size": 35
    }
}

for priority, settings in priority_settings.items():

    subset = uav_points[
        uav_points["search_priority"] == priority
    ]

    if len(subset) > 0:

        subset.plot(
            ax=ax,
            color=settings["color"],
            markersize=settings["size"],
            label=f"{priority} Priority",
            zorder=5
        )

# ==================================================
# 7. Add UAV numbers
# ==================================================

for _, row in india_df.iterrows():

    ax.text(
        row["longitude"] + 0.05,
        row["latitude"] + 0.05,
        f"UAV-{int(row['uav_id'])}",
        fontsize=6
    )

# ==================================================
# 8. Map information
# ==================================================

ax.set_title(
    "AVIATION SAR - UAV SEARCH PRIORITY MAP",
    fontsize=16,
    fontweight="bold"
)

ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

ax.legend()

ax.grid(
    True,
    linestyle="--",
    alpha=0.3
)

# ==================================================
# 9. Save map
# ==================================================

output_file = r"D:\AviationSAR\uav_search_map.png"

plt.savefig(
    output_file,
    dpi=150,
    bbox_inches="tight"
)

plt.close()

print("\nMap saved to:")
print(output_file)

print("\n==========================================")
print("UAV SEARCH MAP COMPLETED")
print("==========================================")