import os
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------
# OUTPUT FOLDER
# ---------------------------------------------------------
output_dir = os.path.join("results")
os.makedirs(output_dir, exist_ok=True)

# ---------------------------------------------------------
# 1. AI MODEL PERFORMANCE - LINE / SIGNAL GRAPH
# ---------------------------------------------------------

metrics = ["Accuracy", "Precision", "Recall", "F1-Score"]
values = [96.49, 84.62, 100.00, 91.67]

plt.figure(figsize=(9, 5))

plt.plot(
    metrics,
    values,
    marker="o",
    linewidth=2,
    markersize=7
)

for i, value in enumerate(values):
    plt.annotate(
        f"{value:.2f}%",
        (metrics[i], values[i]),
        textcoords="offset points",
        xytext=(0, 10),
        ha="center",
        fontsize=10
    )

plt.title("Performance Evaluation of the Proposed AI Rescue Model")
plt.xlabel("Performance Metrics")
plt.ylabel("Score (%)")
plt.ylim(0, 105)
plt.grid(True, linestyle="--", alpha=0.4)

plt.tight_layout()

performance_path = os.path.join(
    output_dir,
    "performance_metrics.png"
)

plt.savefig(
    performance_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ---------------------------------------------------------
# 2. CONFUSION MATRIX
# ---------------------------------------------------------

confusion_matrix = np.array([
    [44, 2],
    [0, 11]
])

plt.figure(figsize=(7, 6))

plt.imshow(confusion_matrix, interpolation="nearest")

plt.title("Confusion Matrix of the Proposed AI Rescue Model")
plt.xlabel("Predicted Class")
plt.ylabel("Actual Class")

classes = [
    "Unsuccessful Rescue",
    "Successful Rescue"
]

plt.xticks(
    range(len(classes)),
    classes,
    rotation=20
)

plt.yticks(
    range(len(classes)),
    classes
)

# Display values inside matrix
for i in range(confusion_matrix.shape[0]):
    for j in range(confusion_matrix.shape[1]):
        plt.text(
            j,
            i,
            str(confusion_matrix[i, j]),
            ha="center",
            va="center",
            fontsize=14
        )

plt.colorbar(label="Number of Samples")

plt.tight_layout()

confusion_path = os.path.join(
    output_dir,
    "confusion_matrix.png"
)

plt.savefig(
    confusion_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ---------------------------------------------------------
# COMPLETION MESSAGE
# ---------------------------------------------------------

print("=" * 60)
print("AVIATION SAR - RESULT GRAPH GENERATION")
print("=" * 60)

print("\nGraphs generated successfully!\n")

print("1. Performance Graph:")
print(os.path.abspath(performance_path))

print("\n2. Confusion Matrix:")
print(os.path.abspath(confusion_path))

print("\nAll figures saved successfully.")
# ---------------------------------------------------------
# 3. FEATURE IMPORTANCE - LINE / SIGNAL GRAPH
# ---------------------------------------------------------

features = [
    "priority_score",
    "rescue_priority_score",
    "response_time_score",
    "response_level_score",
    "ground_rescue",
    "medical_team",
    "uav_assigned",
    "search_completed",
    "deployment_ready"
]

importance = [
    0.286178,
    0.270418,
    0.222820,
    0.102613,
    0.054868,
    0.053646,
    0.009456,
    0.000000,
    0.000000
]

plt.figure(figsize=(10, 6))

plt.plot(
    features,
    importance,
    marker="o",
    linewidth=2,
    markersize=7
)

for i, value in enumerate(importance):
    plt.annotate(
        f"{value:.3f}",
        (features[i], value),
        textcoords="offset points",
        xytext=(0, 8),
        ha="center",
        fontsize=9
    )

plt.title("Feature Importance of the Random Forest Rescue Model")
plt.xlabel("Input Features")
plt.ylabel("Importance Score")

plt.xticks(
    rotation=35,
    ha="right"
)

plt.grid(True, linestyle="--", alpha=0.4)

plt.tight_layout()

feature_path = os.path.join(
    output_dir,
    "feature_importance.png"
)

plt.savefig(
    feature_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\n3. Feature Importance Graph:")
print(os.path.abspath(feature_path))
# ---------------------------------------------------------
# 4. RESCUE PRIORITY DISTRIBUTION - LINE / SIGNAL GRAPH
# ---------------------------------------------------------

priority_levels = [
    "LOW",
    "MEDIUM",
    "CRITICAL"
]

priority_counts = [
    46,
    3,
    8
]

plt.figure(figsize=(8, 5))

plt.plot(
    priority_levels,
    priority_counts,
    marker="o",
    linewidth=2.5,
    markersize=8
)

for i, value in enumerate(priority_counts):
    plt.annotate(
        str(value),
        (priority_levels[i], value),
        textcoords="offset points",
        xytext=(0, 10),
        ha="center",
        fontsize=10
    )

plt.title("Rescue Priority Distribution")
plt.xlabel("Rescue Priority Level")
plt.ylabel("Number of Aircraft")

plt.grid(True, linestyle="--", alpha=0.4)

plt.tight_layout()

priority_path = os.path.join(
    output_dir,
    "rescue_priority_distribution.png"
)

plt.savefig(
    priority_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\n4. Rescue Priority Distribution Graph:")
print(os.path.abspath(priority_path))
# ---------------------------------------------------------
# 5. RESCUE OUTCOME DISTRIBUTION - LINE / SIGNAL GRAPH
# ---------------------------------------------------------

outcome_labels = [
    "High Success",
    "Moderate Success",
    "High Risk"
]

outcome_counts = [
    8,
    5,
    44
]

plt.figure(figsize=(9, 5))

plt.plot(
    outcome_labels,
    outcome_counts,
    marker="o",
    linewidth=2.5,
    markersize=8
)

for i, value in enumerate(outcome_counts):
    plt.annotate(
        str(value),
        (outcome_labels[i], value),
        textcoords="offset points",
        xytext=(0, 10),
        ha="center",
        fontsize=10
    )

plt.title("Predicted Rescue Outcome Distribution")
plt.xlabel("Predicted Rescue Outcome")
plt.ylabel("Number of Targets")

plt.grid(True, linestyle="--", alpha=0.4)

plt.tight_layout()

outcome_path = os.path.join(
    output_dir,
    "rescue_outcome_distribution.png"
)

plt.savefig(
    outcome_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\n5. Rescue Outcome Distribution Graph:")
print(os.path.abspath(outcome_path))
# ---------------------------------------------------------
# 6. RESCUE SUCCESS PROBABILITY VS RESCUE RISK
# ---------------------------------------------------------

risk_metrics = [
    "Success Probability",
    "Rescue Risk"
]

risk_values = [
    51.32,
    48.68
]

plt.figure(figsize=(8, 5))

plt.plot(
    risk_metrics,
    risk_values,
    marker="o",
    linewidth=2.5,
    markersize=8
)

for i, value in enumerate(risk_values):
    plt.annotate(
        f"{value:.2f}%",
        (risk_metrics[i], value),
        textcoords="offset points",
        xytext=(0, 10),
        ha="center",
        fontsize=10
    )

plt.title("Average Rescue Success Probability and Risk")
plt.xlabel("Outcome Measure")
plt.ylabel("Score (%)")
plt.ylim(0, 100)

plt.grid(True, linestyle="--", alpha=0.4)

plt.tight_layout()

risk_path = os.path.join(
    output_dir,
    "success_probability_vs_risk.png"
)

plt.savefig(
    risk_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\n6. Success Probability vs Rescue Risk Graph:")
print(os.path.abspath(risk_path))