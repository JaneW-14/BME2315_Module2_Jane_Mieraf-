
# main file for calling constructor from Mod2_data.py


#Importing all the neccessary packages 
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import statistics
import pandas as pd
from pathlib import Path
from scipy.interpolate import interp1d

#importing the classes created in the Mod2_data.py file
from Mod2_data import Patient
from Mod2_data import SelectedPatient

# This configuration allows any user to run the script without modifying the file paths.
filename = Path(__file__).with_name("Module2_FSHD_Dataset.csv")
cleanfilename = Path(__file__).with_name("Patient_data.csv")
interpolated_filename = Path(__file__).with_name("Patient_data_interpolated.csv")
graph_filename = Path(__file__).with_name("Patient_data_interpolation.png")
regression_filename = Path(__file__).with_name(
    "FF_change_vs_WR_change_regression.png"
)

#call the methods to create the patient objects from the original FSHD dataset and then run it through the checks in the data file that remove any missing data sets. 
# All the data points that pass the requirements will be exported to a new file called "patient_data.csv"
Patient.instantiate_from_csv(filename)
Patient.export_to_csv(cleanfilename)

# Read the cleaned patient data from the CSV file into a DataFrame
patients = pd.read_csv(cleanfilename)

# INTERPOLATION CODE 

# Define the target time points for interpolation by using the minimum lag time at each time point 
T1 = patients["lag_months_y1"].min()
T2 = patients["lag_months_y2"].min()

# Define the measurements to be interpolated and their corresponding baseline, T1, and T2 fields.
measurements = {
    "ff_R": ("ff_baseline_R", "ff_y1_R", "ff_y2_R"),
    "ff_L": ("ff_baseline_L", "ff_y1_L", "ff_y2_L"),
    "wr_10": ("wr_10_baseline", "wr_10_y1", "wr_10_y2"),
}

#create a function called interpolate_measurement that requires the rows, fields, target date to interpolate to and version of interpolation (linear or quadratic)
#this code was created by the built in Copilot 

def interpolate_measurement(row, fields, target, kind):
    baseline_field, y1_field, y2_field = fields

    times = np.array([
        0.0,
        row["lag_months_y1"],
        row["lag_months_y2"],
    ])

    values = np.array([
        row[baseline_field],
        row[y1_field],
        row[y2_field],
    ])

    point_count = 2 if kind == "linear" else 3

    return float(
        interp1d(
            times[:point_count],
            values[:point_count],
            kind=kind,
        )(target)
    )

#this creates a table to display the results of the interpolation 
interpolated_patients = pd.DataFrame({
    "subject_id": patients["subject_id"],
    "T1_months": T1,
    "T2_months": T2,
})

for measure, fields in measurements.items():
    #for interpolating data to the t1 marker the code uses a linear interpolation because there are only two data points 
    interpolated_patients[f"{measure}_T1"] = patients.apply(
        interpolate_measurement,
        axis=1,
        fields=fields,
        target=T1,
        kind="linear",
    )
    #for interpolating data to the t2 marker the code uses a quadratic interpolation because there are three data points
    interpolated_patients[f"{measure}_T2"] = patients.apply(
        interpolate_measurement,
        axis=1,
        fields=fields,
        target=T2,
        kind="quadratic",
    )


# Add original baseline measurements to the data frame to allow them to be plotted alongside the interpolated values
interpolated_patients["ff_R_baseline"] = patients["ff_baseline_R"]
interpolated_patients["ff_L_baseline"] = patients["ff_baseline_L"]
interpolated_patients["wr_10_baseline"] = patients["wr_10_baseline"]

#this exports the interpolated data to a CSV file
interpolated_patients.to_csv(interpolated_filename, index=False)


# Plot measured visits and interpolated values
fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

plot_measurements = [
    ("ff_R", "Right fat fraction (%)"),
    ("ff_L", "Left fat fraction (%)"),
    ("wr_10", "WR-10"),
]

for ax, (measure, ylabel) in zip(axes, plot_measurements):
    baseline_field, y1_field, y2_field = measurements[measure]

    for patient_index, (_, patient) in enumerate(patients.iterrows()):
        visit_times = [
            0,
            patient["lag_months_y1"],
            patient["lag_months_y2"],
        ]

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

# Close the figure after saving so the script does not wait for a plot window.
plt.close(fig)

print(f"\n Interpolation: T1 = {T1:.2f} months; T2 = {T2:.2f} months")
print(f"Interpolated {len(patients)} patients: {interpolated_filename}")
print(f"Graph saved: {graph_filename}")

# T-TEST CODE ------------------
# Perform paired t-tests to compare left and right fat fraction at each visit.

# Compare left and right fat fraction at each visit
fat_fraction_visits = {
    "Baseline": ("ff_L_baseline", "ff_R_baseline"),
    "T1": ("ff_L_T1", "ff_R_T1"),
    "T2": ("ff_L_T2", "ff_R_T2"),
}

test_results = []

for visit, (left_col, right_col) in fat_fraction_visits.items():
    paired_data = interpolated_patients[
        [left_col, right_col]
    ].dropna()

    left = paired_data[left_col]
    right = paired_data[right_col]

    # Safeguard: a paired t-test needs at least two complete pairs.
    if len(paired_data) < 2:
        t_stat, p_value = np.nan, np.nan
    else:
        t_stat, p_value = stats.ttest_rel(left, right)

    test_results.append({
        "Visit": visit,
        "N paired": len(paired_data),
        "Mean left": left.mean(),
        "Mean right": right.mean(),
        "Mean difference (L-R)": (left - right).mean(),
        "t-statistic": t_stat,
        "p-value": p_value,
    })

    # Average both sides for each patient
    average_col = f"ff_TA_average_{visit}"

    interpolated_patients[average_col] = (
        interpolated_patients[[left_col, right_col]]
        .mean(axis=1, skipna=False)
    )


results_df = pd.DataFrame(test_results)

print("\nPaired t-tests: Left vs. Right TA Fat Fraction")
print(results_df.round(4).to_string(index=False))

# FIND SRM VALUES

#The SelectedPatient class is meant to be only used with the Interpolated_patient.csv. this class has all the methods I need to create to find the SRM 
#The reason I choose to create a new class is because the 3 different data files have the same column names and it would get very confusing trying to specific about 
#which data file and which corresponding column I needed to use 

#assigns the objects created by the SelectedPatient constructor to selectedpatient list
SelectedPatient.instantiate_from_csv(interpolated_filename) #interpolated filename is the variable name established earlier in the code. It allows anyone with the entire repisitory to run the code, because it is not calling on local files

#calls the method in the Mod2_data.pys that find the difference between the noted time points and assigns them to the appropriate variables

difference_baseline_T1 = SelectedPatient.difference_baseline_T1()
difference_baseline_T2 = SelectedPatient.difference_baseline_T2()
difference_T1_T2 = SelectedPatient.difference_T1_T2()

#used to check correct caculations for the difference found for each patient data point 
#print(f"Change (for left and right) in ff in TA from baseline to T1: {difference_baseline_T1}")
#print(f"Change (for left and right) in ff in TA from baseline to T2: {difference_baseline_T2}")
#print(f"Change (for left and right) in ff in TA from T1 to T2: {difference_T1_T2}")

#calls the method in the Mod2_data.pys that find the mean difference between the noted time points and assigns them to the appropriate variables
mean_difference_baseline_T1 = SelectedPatient.mean_difference_baseline_T1()
mean_difference_baseline_T2 = SelectedPatient.mean_difference_baseline_T2()
mean_difference_T1_T2 = SelectedPatient.mean_difference_T1_T2()
#prints the mean values 
print(f"\nMean change from baseline to T1: {mean_difference_baseline_T1}")
print(f"\nMean change from baseline to T2: {mean_difference_baseline_T2}")
print(f"\nMean change from T1 to T2: {mean_difference_T1_T2}")

#calls the method in the Mod2_data.pys that find the standard deviation of the difference between the noted time points and assigns them to the appropriate variables
SD_difference_baseline_T1 = SelectedPatient.SD_difference_baseline_T1()
SD_difference_baseline_T2 = SelectedPatient.SD_difference_baseline_T2()
SD_difference_T1_T2 = SelectedPatient.SD_difference_T1_T2()

#prints the standard deviation values
print(f"\nSD from baseline to T1: {SD_difference_baseline_T1}")
print(f"\n SD from baseline to T2: {SD_difference_baseline_T2}")
print(f"\n SD from T1 to T2: {SD_difference_T1_T2}")

#calls the method in the Mod2_data.pys that find the SRM of the difference between the noted time points and assigns them to the appropriate variables
SRM_baseline_T1 = SelectedPatient.SRM_baseline_T1()
SRM_baseline_T2 = SelectedPatient.SRM_baseline_T2()
SRM_T1_T2 = SelectedPatient.SRM_T1_T2()
#prints the SRM values
print(f"\n SRM from baseline to T1: {SRM_baseline_T1}")
print(f"\n SRM from baseline to T2: {SRM_baseline_T2}")
print(f"\n SRM from T1 to T2: {SRM_T1_T2}")

#calls the method in the Mod2_data.pys that find the change in WR between the noted time points and assigns them to the appropriate variables
change_baseline_T1_WR = SelectedPatient.change_WR_baseline_T1()
change_baseline_T2_WR = SelectedPatient.change_WR_baseline_T2()
change_T1_T2_WR = SelectedPatient.change_WR_T1_T2()

#prints the change in WR values for verification
#print(f"\nChange (for left and right) in WR from baseline to T1: {change_baseline_T1_WR}")
#print(f"\n Change (for left and right) in WR from baseline to T2: {change_baseline_T2_WR}")
#print(f"\nChange (for left and right) in WR from T1 to T2: {change_T1_T2_WR}")

#calls the method in the Mod2_data.pys that find the mean change in WR between the noted time points and assigns them to the appropriate variables
mean_WR_baseline_T1 = SelectedPatient.mean_WR_baseline_T1()
mean_WR_baseline_T2 = SelectedPatient.mean_WR_baseline_T2()
mean_WR_T1_T2 = SelectedPatient.mean_WR_T1_T2()

#prints the mean in WR change
print(f"\nMean change in WR from baseline to T1: {mean_WR_baseline_T1}")
print(f"\n Mean change in WR from baseline to T2: {mean_WR_baseline_T2}")
print(f"\nMean change in WR from T1 to T2: {mean_WR_T1_T2}")

#calls the method in the Mod2_data.pys that find the standard deviation of the change in WR between the noted time points and assigns them to the appropriate variables
SD_WR_baseline_T1 = SelectedPatient.SD_WR_baseline_T1()
SD_WR_baseline_T2 = SelectedPatient.SD_WR_baseline_T2()
SD_WR_T1_T2 = SelectedPatient.SD_WR_T1_T2()

#prints the standard deviation of the change in WR values
print(f"\n SD change in WR from baseline to T1: {SD_WR_baseline_T1}")
print(f"\n SD change in WR from baseline to T2: {SD_WR_baseline_T2}")
print(f"\nSD change in WR from T1 to T2: {SD_WR_T1_T2}")

#calls the method in the Mod2_data.pys that find the SRM of the change in WR between the noted time points and assigns them to the appropriate variables
SRM_WR_baseline_T1 = SelectedPatient.SRM_WR_baseline_T1()
SRM_WR_baseline_T2 = SelectedPatient.SRM_WR_baseline_T2()
SRM_WR_T1_T2 = SelectedPatient.SRM_WR_T1_T2()

#prints the SRM of the change in WR values
print(f"\n SRM change in WR from baseline to T1: {SRM_WR_baseline_T1}")
print(f"\n SRM change in WR from baseline to T2: {SRM_WR_baseline_T2}")
print(f"\nSRM change in WR from T1 to T2: {SRM_WR_T1_T2}")


#TESTING IF THE CHANGE IN FF IN 0-12 MONTHS CAN PREDICT THE CHANGE IN WR-10 FROM 0-24 MONTHS 

#assigning values to the x and y arrays for the regression analysis
x_values = np.array([difference[0] for difference in difference_baseline_T1])
y_values = np.array(change_baseline_T2_WR)
valid_values = np.isfinite(x_values) & np.isfinite(y_values)
x_values = x_values[valid_values]
y_values = y_values[valid_values]

#creating the scatter plot and regression line for the relationship between fat fraction change and WR-10 change
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(x_values, y_values, alpha=0.75)
ax.set_xlabel("Fat fraction change: baseline to T1")
ax.set_ylabel("WR-10 change: baseline to T2")
ax.set_title("Fat Fraction Change vs. WR-10 Change")
ax.grid(True, alpha=0.25)

#making sure there are enoguh valid data points to perform the regression analysis
if len(x_values) >= 2 and np.ptp(x_values) > 0:
    regression = stats.linregress(x_values, y_values)
    line_x = np.linspace(x_values.min(), x_values.max(), 100)
    ax.plot(
        line_x,
        regression.intercept + regression.slope * line_x,
        color="tab:red",
        label=f"Linear regression (R² = {regression.rvalue ** 2:.3f})",
    )
    ax.legend()
    print(
        "\nLinear regression for fat fraction change (baseline to T1) "
        "vs. WR-10 change (baseline to T2): "
        f"slope={regression.slope:.4f}, "
        f"intercept={regression.intercept:.4f}, "
        f"R²={regression.rvalue ** 2:.4f}, "
        f"p-value={regression.pvalue:.4g}"
    )
else:
    print(
        "\nCould not calculate linear regression: it requires at least "
        "two paired values and variation in the x-values."
    )

fig.tight_layout()
fig.savefig(regression_filename, dpi=200, bbox_inches="tight")
plt.close(fig)
# this saves the linear regression plot to a file within the repository 
print(f"Regression plot saved: {regression_filename}")