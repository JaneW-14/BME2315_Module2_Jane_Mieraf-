# main file for calling constructor from Mod2_data.py

import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import statistics
import pandas as pd
from pathlib import Path
from scipy.interpolate import interp1d
from Mod2_data import Patient

# Load the complete patients and export their measured values.
filename = "/Users/janewyatt/Desktop/BME 2315 /Module 2/Module2_FSHD_Dataset.csv"
cleanfilename = Path(__file__).with_name("Patient_data.csv")
interpolated_filename = Path(__file__).with_name("Patient_data_interpolated.csv")
graph_filename = Path(__file__).with_name("Patient_data_interpolation.png")
Patient.instantiate_from_csv(filename)
Patient.export_to_csv(cleanfilename)

patients = pd.read_csv(cleanfilename)
T1 = patients["lag_months_y1"].min()
T2 = patients["lag_months_y2"].min()

measurements = {
    "ff_R": ("ff_baseline_R", "ff_y1_R", "ff_y2_R"),
    "ff_L": ("ff_baseline_L", "ff_y1_L", "ff_y2_L"),
    "wr_10": ("wr_10_baseline", "wr_10_y1", "wr_10_y2"),
}


def interpolate_measurement(row, fields, target, kind):
    baseline_field, y1_field, y2_field = fields
    times = np.array([0.0, row["lag_months_y1"], row["lag_months_y2"]])
    values = np.array([
        row[baseline_field],
        row[y1_field],
        row[y2_field],
    ])
    point_count = 2 if kind == "linear" else 3
    return float(interp1d(times[:point_count], values[:point_count], kind=kind)(target))


interpolated_patients = pd.DataFrame({
    "subject_id": patients["subject_id"],
    "T1_months": T1,
    "T2_months": T2,
})

for measure, fields in measurements.items():
    interpolated_patients[f"{measure}_T1"] = patients.apply(
        interpolate_measurement,
        axis=1,
        fields=fields,
        target=T1,
        kind="linear",
    )
    interpolated_patients[f"{measure}_T2"] = patients.apply(
        interpolate_measurement,
        axis=1,
        fields=fields,
        target=T2,
        kind="quadratic",
    )

interpolated_patients.to_csv(interpolated_filename, index=False)

fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
plot_measurements = [
    ("ff_R", "Right fat fraction (%)"),
    ("ff_L", "Left fat fraction (%)"),
    ("wr_10", "WR-10"),
]

for ax, (measure, ylabel) in zip(axes, plot_measurements):
    baseline_field, y1_field, y2_field = measurements[measure]
    for patient_index, (_, patient) in enumerate(patients.iterrows()):
        visit_times = [0, patient["lag_months_y1"], patient["lag_months_y2"]]
        visit_values = [
            patient[baseline_field],
            patient[y1_field],
            patient[y2_field],
        ]
        ax.plot(
            visit_times,
            visit_values,
            color="gray",
            alpha=0.2,
            linewidth=0.8,
            label="Measured visits" if patient_index == 0 else None,
        )
        ax.scatter(
            visit_times,
            visit_values,
            color="black",
            alpha=0.45,
            s=18,
            zorder=3,
        )

    ax.scatter(
        np.full(len(patients), T1),
        interpolated_patients[f"{measure}_T1"],
        color="tab:blue",
        marker="D",
        alpha=0.75,
        s=32,
        label=f"Linear estimate at T1 ({T1:.2f} months)",
        zorder=4,
    )
    ax.scatter(
        np.full(len(patients), T2),
        interpolated_patients[f"{measure}_T2"],
        color="tab:orange",
        marker="D",
        alpha=0.75,
        s=32,
        label=f"Quadratic estimate at T2 ({T2:.2f} months)",
        zorder=4,
    )
    ax.axvline(T1, color="tab:blue", linestyle=":", alpha=0.6)
    ax.axvline(T2, color="tab:orange", linestyle=":", alpha=0.6)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.25)
    ax.legend()

axes[-1].set_xlabel("Months since baseline")
fig.suptitle("Measured Visits and Interpolated Values for All Patients")
fig.tight_layout()
fig.savefig(graph_filename, dpi=200, bbox_inches="tight")
plt.close(fig)

print(f"T1 = {T1:.2f} months; T2 = {T2:.2f} months")
print(f"Interpolated {len(patients)} patients: {interpolated_filename}")
print(f"Graph saved: {graph_filename}")