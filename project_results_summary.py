import os
import pandas as pd

print("=" * 70)
print("          AVIATION SAR - FINAL SYSTEM RESULTS")
print("=" * 70)

# ============================================================
# 1. SATELLITE RESULTS
# ============================================================

print("\nSATELLITE TERRAIN CLASSIFICATION")
print("-" * 45)

total_test = 2700
correct = 2431
wrong = 269

accuracy = (correct / total_test) * 100

print(f"Test Images       : {total_test}")
print(f"Correct           : {correct}")
print(f"Wrong             : {wrong}")
print(f"Accuracy          : {accuracy:.2f} %")

# ============================================================
# 2. AIRCRAFT DETECTION RESULTS
# ============================================================

print("\nAIRCRAFT DETECTION - YOLOv8")
print("-" * 45)

print("Precision         : 77.7 %")
print("Recall            : 52.3 %")
print("mAP50             : 55.4 %")
print("mAP50-95          : 30.7 %")

# ============================================================
# 3. FLIGHT DATA
# ============================================================

print("\nFLIGHT DATA ANALYSIS")
print("-" * 45)

flight_file = (
    r"D:\AviationSAR\dataset\flight"
    r"\aircraft_last_known_positions.csv"
)

flight_df = pd.read_csv(flight_file)

print(f"Aircraft Records  : {len(flight_df)}")

airborne = flight_df[
    (flight_df["velocity"] > 0) |
    (flight_df["baro_altitude"] > 0)
]

print(f"Airborne Aircraft  : {len(airborne)}")

# ============================================================
# 4. UAV SEARCH PLANNING
# ============================================================

print("\nUAV SEARCH PLANNING")
print("-" * 45)

uav_file = (
    r"D:\AviationSAR\dataset\flight"
    r"\uav_search_plan_india.csv"
)

uav_df = pd.read_csv(uav_file)

print(f"India Region       : {len(uav_df)}")

print("\nSearch Priority:")
print(uav_df["search_priority"].value_counts())

# ============================================================
# 5. RESCUE DECISION
# ============================================================

print("\nRESCUE DECISION OPTIMIZATION")
print("-" * 45)

rescue_file = (
    r"D:\AviationSAR\dataset\flight"
    r"\rescue_decision_results.csv"
)

rescue_df = pd.read_csv(rescue_file)

print(f"Total Decisions    : {len(rescue_df)}")

print("\nRescue Priority:")
print(rescue_df["rescue_priority"].value_counts())

# ============================================================
# 6. OUTPUT FILES
# ============================================================

print("\nFINAL OUTPUT FILES")
print("-" * 45)

files = [
    r"D:\AviationSAR\map_overview.png",
    r"D:\AviationSAR\uav_search_map.png",
    r"D:\AviationSAR\final_rescue_decision_map.png",
    r"D:\AviationSAR\dataset\flight\opensky_cleaned.csv",
    r"D:\AviationSAR\dataset\flight\aircraft_last_known_positions.csv",
    r"D:\AviationSAR\dataset\flight\uav_search_plan_india.csv",
    r"D:\AviationSAR\dataset\flight\rescue_decision_results.csv"
]

for file in files:

    if os.path.exists(file):

        size = os.path.getsize(file)

        print(f"[OK] {os.path.basename(file)} - {size:,} bytes")

    else:

        print(f"[MISSING] {file}")

# ============================================================
# FINAL
# ============================================================

print("\n" + "=" * 70)
print("              AVIATION SAR PIPELINE COMPLETED")
print("=" * 70)

print("\nPipeline:")
print("Satellite CNN")
print("      ↓")
print("Aircraft YOLOv8 Detection")
print("      ↓")
print("OpenSky Flight Analysis")
print("      ↓")
print("UAV Search Planning")
print("      ↓")
print("Rescue Decision Optimization")
print("      ↓")
print("Final Rescue Decision Map")

print("\n" + "=" * 70)