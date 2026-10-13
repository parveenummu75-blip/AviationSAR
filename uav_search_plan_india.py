import pandas as pd
import os

# ============================================================
# AVIATION SAR - INDIA REGION UAV SEARCH PLAN
# ============================================================

input_file = r"D:\AviationSAR\dataset\flight\uav_search_plan.csv"

output_file = r"D:\AviationSAR\dataset\flight\uav_search_plan_india.csv"

# India-region bounds from your map dataset
MIN_LON = 71.518
MAX_LON = 94.277
MIN_LAT = 6.756
MAX_LAT = 19.917

print("=" * 55)
print("AVIATION SAR - INDIA UAV SEARCH PLANNING")
print("=" * 55)

print("\nLoading UAV search plan...")

df = pd.read_csv(input_file)

print("Total UAV plan records:", len(df))

# ------------------------------------------------------------
# Filter aircraft inside map region
# ------------------------------------------------------------

india_df = df[
    (df["longitude"] >= MIN_LON) &
    (df["longitude"] <= MAX_LON) &
    (df["latitude"] >= MIN_LAT) &
    (df["latitude"] <= MAX_LAT)
].copy()

print("Aircraft inside map region:", len(india_df))

# ------------------------------------------------------------
# Sort by priority
# ------------------------------------------------------------

priority_order = {
    "HIGH": 0,
    "MEDIUM": 1,
    "LOW": 2
}

india_df["priority_order"] = india_df["search_priority"].map(priority_order)

india_df = india_df.sort_values(
    ["priority_order", "priority_score"],
    ascending=[True, False]
)

# Remove helper column
india_df.drop(columns=["priority_order"], inplace=True)

# ------------------------------------------------------------
# Save
# ------------------------------------------------------------

india_df.to_csv(output_file, index=False)

print("\n==========================================")
print("INDIA UAV SEARCH PLAN")
print("==========================================")

print("\nPriority distribution:")
print(india_df["search_priority"].value_counts())

print("\nFirst 10 India-region aircraft:")
print(
    india_df.head(10).to_string(index=False)
)

print("\n==========================================")
print("UAV SEARCH PLAN COMPLETED")
print("==========================================")

print("\nOutput saved to:")
print(output_file)

print("==========================================")