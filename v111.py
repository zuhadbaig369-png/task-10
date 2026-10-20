import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

exercise_df = sns.load_dataset("exercise")

print("Original Exercise Dataset:")
print(exercise_df.head())

running_data = exercise_df.loc[exercise_df["kind"] == "running"]
one_minute_data = running_data.loc[
    running_data["time"] == "1 min", ["id", "pulse"]
]
thirty_minute_data = running_data.loc[
    running_data["time"] == "30 min", ["id", "pulse"]
]

fitness_merge = one_minute_data.merge(
    thirty_minute_data,
    on="id",
    suffixes=("_1_minute", "_30_minutes"),
)
print("\nMerged Fitness Data:")
print(fitness_merge)

fitness_merge["pulse_progress"] = (
    fitness_merge["pulse_30_minutes"] - fitness_merge["pulse_1_minute"]
)
fitness_merge = fitness_merge.sort_values("pulse_progress", ascending=False)
print("\nSorted Fitness Progress:")
print(fitness_merge)

participant_names = [
    "Participant " + str(participant_id)
    for participant_id in fitness_merge["id"]
]
fitness_data = {
    "participant": participant_names,
    "pulse_1_minute": fitness_merge["pulse_1_minute"].tolist(),
    "pulse_30_minutes": fitness_merge["pulse_30_minutes"].tolist(),
}
chart_df = pd.DataFrame(fitness_data)
print("\nChart Data:")
print(chart_df)

positions = np.arange(len(chart_df["participant"]))
bar_width = 0.35

plt.figure(figsize=(12, 7))
one_minute_bars = plt.bar(
    positions - bar_width / 2,
    chart_df["pulse_1_minute"],
    width=bar_width,
    label="After 1 minute",
)
thirty_minute_bars = plt.bar(
    positions + bar_width / 2,
    chart_df["pulse_30_minutes"],
    width=bar_width,
    label="After 30 minutes",
)

plt.title("Running Exercise Pulse Comparison")
plt.xlabel("Participant")
plt.ylabel("Pulse Rate")
plt.xticks(positions, chart_df["participant"], rotation=45)
plt.legend()

for bars in (one_minute_bars, thirty_minute_bars):
    for bar in bars:
        value = bar.get_height()
        plt.annotate(
            str(value),
            (bar.get_x() + bar.get_width() / 2, value),
            textcoords="offset points",
            xytext=(0, 5),
            ha="center",
        )

plt.tight_layout()
plt.savefig("fitness-progress-comparison.png", dpi=180, bbox_inches="tight")
plt.show()