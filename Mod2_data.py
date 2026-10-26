#constructor file 
#File to create the class constructor and methods that will be used in the main python file 
 
#importing data set file 
import csv

#making the class that will organize the patient data 
class Patient:
    #this list is the directory for every following method, once the data points are added by the constructor the other methods can refer to it for thier functions 
    all_patients = []
    #Constructor builds objects and assign the values age of onset, gender, gene type, and years of education to them for later use
    def __init__(self, ff_baseline_R, ff_y1_R, ff_y2_R, ff_baseline_L,ff_y1_L,ff_y2_L, lag_months_y1, lag_months_y2,wr_10_baseline,wr_10_y1,wr_10_y2, subject_id=None):
        #only creating attributes required for the analysis of our specific research question
        self.subject_id = subject_id
        self.ff_baseline_R = ff_baseline_R
        self.ff_y1_R = ff_y1_R
        self.ff_y2_R = ff_y2_R
        self.ff_baseline_L = ff_baseline_L
        self.ff_y1_L = ff_y1_L
        self.ff_y2_L = ff_y2_L
        self.lag_months_y1 = lag_months_y1
        self.lag_months_y2 = lag_months_y2
        self.wr_10_baseline = wr_10_baseline
        self.wr_10_y1 = wr_10_y1
        self.wr_10_y2 = wr_10_y2
        #within the constructor there is a conditional that will not construct an object (and therefore add it to the new csv) if it is missing data points 
        if self.lag_months_y1 == '' or self.lag_months_y2 == '' or self.wr_10_baseline == '' or self.wr_10_y1 == '' or self.wr_10_y2 == '' or self.ff_baseline_L == '' or self.ff_y1_L == '' or self.ff_y2_L == '' or self.ff_baseline_R == '' or self.ff_y1_R == '' or self.ff_y2_R == '':
            print("Data point removed for this patient because missing data value")
        else:
            Patient.all_patients.append(self)
#retriever, returns a string representation of the patient object for debugging and printing purposes
    def __repr__(self):
        return f"Patient(subject_id={self.subject_id}, ff_baseline_R={self.ff_baseline_R}, ff_y1_R={self.ff_y1_R}, ff_y2_R={self.ff_y2_R}, ff_baseline_L={self.ff_baseline_L}, ff_y1_L={self.ff_y1_L}, ff_y2_L={self.ff_y2_L}, lag_months_y1={self.lag_months_y1}, lag_months_y2={self.lag_months_y2}, wr_10_baseline={self.wr_10_baseline}, wr_10_y1={self.wr_10_y1}, wr_10_y2={self.wr_10_y2})"

#instantiate_from_csv reads a CSV file and creates Patient objects for each row according to the Patient class constructor

    @classmethod
    def instantiate_from_csv(cls, filename):
        cls.all_patients.clear()
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cls(
                    row['ff_baseline_R'],
                    row['ff_y1_R'],
                    row['ff_y2_R'],
                    row['ff_baseline_L'],
                    row['ff_y1_L'],
                    row['ff_y2_L'],
                    row['lag_months_y1'],
                    row['lag_months_y2'],
                    row['wr_10_baseline'],
                    row['wr_10_y1'],
                    row['wr_10_y2'],
                    row.get('subject_id')
                )
# to keep our code organized we decided to make a new data file with the "cleaned" version of the data file that removes all missing data point 
# and data unrelated to our question 
#export_to_csv writes the cleaned data to a new CSV file
    @classmethod
    def export_to_csv(cls, filename):
        fieldnames = [
            'subject_id',
            'ff_baseline_R',
            'ff_y1_R',
            'ff_y2_R',
            'ff_baseline_L',
            'ff_y1_L',
            'ff_y2_L',
            'lag_months_y1',
            'lag_months_y2',
            'wr_10_baseline',
            'wr_10_y1',
            'wr_10_y2',
        ]
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(
                {
                    field: getattr(patient, field)
                    for field in fieldnames
                }
                for patient in cls.all_patients
            )
# this class creates a list of "selected patients" data points that passed the conditional in the Patient class and are now part of the Pantient_data.csv
class SelectedPatient:
    #this list is the directory for every following method, once the data points are added by the constructor the other methods can refer to it for thier functions 
    selected_patients = []
    def __init__(self, ff_baseline_R, ff_y1_R, ff_y2_R, ff_baseline_L,ff_y1_L,ff_y2_L, lag_months_y1, lag_months_y2,wr_10_baseline,wr_10_y1,wr_10_y2):
        self.ff_baseline_R = ff_baseline_R
        self.ff_y1_R = ff_y1_R
        self.ff_y2_R = ff_y2_R
        self.ff_baseline_L = ff_baseline_L
        self.ff_y1_L = ff_y1_L
        self.ff_y2_L = ff_y2_L
        self.lag_months_y1 = lag_months_y1
        self.lag_months_y2 = lag_months_y2
        self.wr_10_baseline = wr_10_baseline
        self.wr_10_y1 = wr_10_y1
        self.wr_10_y2 = wr_10_y2
        # Add the current instance to the list of selected patients
        SelectedPatient.selected_patients.append(self)

    def __repr__(self):
        return f"SelectedPatient(ff_baseline_R={self.ff_baseline_R}, ff_y1_R={self.ff_y1_R}, ff_y2_R={self.ff_y2_R}, ff_baseline_L={self.ff_baseline_L}, ff_y1_L={self.ff_y1_L}, ff_y2_L={self.ff_y2_L}, lag_months_y1={self.lag_months_y1}, lag_months_y2={self.lag_months_y2}, wr_10_baseline={self.wr_10_baseline}, wr_10_y1={self.wr_10_y1}, wr_10_y2={self.wr_10_y2})"
    @classmethod
    #reads the data file created by the Patient Class called Patient_data.csv and instantiates SelectedPatient objects from it
    def instantiate_from_csv(cls, filename):
        cls.selected_patients.clear()
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                SelectedPatient(
                    row['ff_R_baseline'],
                    row['ff_R_T1'],
                    row['ff_R_T2'],
                    row['ff_L_baseline'],
                    row['ff_L_T1'],
                    row['ff_L_T2'],
                    row['T1_months'],
                    row['T2_months'],
                    row['wr_10_baseline'],
                    row['wr_10_T1'],
                    row['wr_10_T2']
                )
    @classmethod 
    # Now we can perform our test on our selected data points 

    # first we found the difference in Fat Fraction values between baseline and T1 
    # we can average our the left and right fat fraction values into one data point because we know they aren't statistically different due to the results of our t-test
    def difference_baseline_T1(cls):
        B_T1_differences = []
        for patient in cls.selected_patients:
            average_baseline_LR = (float(patient.ff_baseline_R) + float(patient.ff_baseline_L)) / 2
            average_T1_LR = (float(patient.ff_y1_R) + float(patient.ff_y1_L)) / 2
            diff_average = average_T1_LR - average_baseline_LR
            B_T1_differences.append((diff_average,))
        return B_T1_differences
# finds the difference in Fat fraction baseline to t2 
    @classmethod
    def difference_baseline_T2(cls):
        B_T2_differences = []
        for patient in cls.selected_patients:
            average_baseline_LR = (float(patient.ff_baseline_R) + float(patient.ff_baseline_L)) / 2
            average_T2_LR = (float(patient.ff_y2_R) + float(patient.ff_y2_L)) / 2
            diff_average = average_T2_LR - average_baseline_LR
            B_T2_differences.append((diff_average,))
        return B_T2_differences
    
#finds the difference in Fat fraction T1 to T2
    @classmethod 
    def difference_T1_T2(cls):
        T1_T2_differences = []
        for patient in cls.selected_patients:
            average_T1_LR = (float(patient.ff_y1_R) + float(patient.ff_y1_L)) / 2
            average_T2_LR = (float(patient.ff_y2_R) + float(patient.ff_y2_L)) / 2
            diff_average = average_T2_LR - average_T1_LR
            T1_T2_differences.append((diff_average,))
        return T1_T2_differences

    #Now that we have a new data set made up of the differences between the time points we can find the mean and SD  
    # finds mean in the difference between the baseline and t1 
    @classmethod
    def mean_difference_baseline_T1(cls):
        B_T1_differences = cls.difference_baseline_T1()
        return sum(diff[0] for diff in B_T1_differences) / len(B_T1_differences) if B_T1_differences else None
    
    # finds mean in the difference between the baseline and t2
    @classmethod
    def mean_difference_baseline_T2(cls):
        B_T2_differences = cls.difference_baseline_T2()
        return sum(diff[0] for diff in B_T2_differences) / len(B_T2_differences) if B_T2_differences else None

    # finds mean in the difference between t1 and t2
    @classmethod
    def mean_difference_T1_T2(cls):
        T1_T2_differences = cls.difference_T1_T2()
        return sum(diff[0] for diff in T1_T2_differences) / len(T1_T2_differences) if T1_T2_differences else None

    # finds SD in the difference between the baseline and t1
    @classmethod
    def SD_difference_baseline_T1(cls):
        B_T1_differences = cls.difference_baseline_T1()
        if not B_T1_differences:
            return None
        mean = cls.mean_difference_baseline_T1()
        squared_diffs = [(diff[0] - mean) ** 2 for diff in B_T1_differences]
        return (sum(squared_diffs) / len(squared_diffs)) ** 0.5

    # finds SD in the difference between the baseline and t2
    @classmethod
    def SD_difference_baseline_T2(cls):
        B_T2_differences = cls.difference_baseline_T2()
        if not B_T2_differences:
            return None
        mean = cls.mean_difference_baseline_T2()
        squared_diffs = [(diff[0] - mean) ** 2 for diff in B_T2_differences]
        return (sum(squared_diffs) / len(squared_diffs)) ** 0.5

    # finds SD in the difference between t1 and t2
    @classmethod
    def SD_difference_T1_T2(cls):
        T1_T2_differences = cls.difference_T1_T2()
        if not T1_T2_differences:
            return None
        mean = cls.mean_difference_T1_T2()
        squared_diffs = [(diff[0] - mean) ** 2 for diff in T1_T2_differences]
        return (sum(squared_diffs) / len(squared_diffs)) ** 0.5
    
    # Calculates SRM by dividing the mean found by the other method by the SD found by the other method
    # SRM value for baseline to t1 Fat fraction 
    @classmethod 
    def SRM_baseline_T1(cls):
        B_T1_differences = cls.difference_baseline_T1()
        if not B_T1_differences:
            return None
        mean = cls.mean_difference_baseline_T1()
        SD = cls.SD_difference_baseline_T1()
        return mean / SD if SD else None
    # SRM value for baseline to t2 Fat fraction
    @classmethod
    def SRM_baseline_T2(cls):
        B_T2_differences = cls.difference_baseline_T2()
        if not B_T2_differences:
            return None
        mean = cls.mean_difference_baseline_T2()
        SD = cls.SD_difference_baseline_T2()
        return mean / SD if SD else None

    # SRM value for t1 to t2 Fat fraction
    @classmethod
    def SRM_T1_T2(cls):
        T1_T2_differences = cls.difference_T1_T2()
        if not T1_T2_differences:
            return None
        mean = cls.mean_difference_T1_T2()
        SD = cls.SD_difference_T1_T2()
        return mean / SD if SD else None 
    
    #RUN WALK ANALYSIS -------------------------------------------------

    #First calculate the change between each time point (baseline, T1 (year 1), T2 (year 2))
    @classmethod
    def change_WR_baseline_T1(cls):
        change_WR_baseline_T1 =[]
        for patient in cls.selected_patients:
            change_WR_baseline_T1.append(float(patient.wr_10_y1) - float(patient.wr_10_baseline))
        return change_WR_baseline_T1

    @classmethod
    def change_WR_baseline_T2(cls):
        change_WR_baseline_T2 =[]
        for patient in cls.selected_patients:
            change_WR_baseline_T2.append(float(patient.wr_10_y2) - float(patient.wr_10_baseline))
        return change_WR_baseline_T2

    @classmethod
    def change_WR_T1_T2(cls):
        change_WR_T1_T2 =[]
        for patient in cls.selected_patients:
            change_WR_T1_T2.append(float(patient.wr_10_y2) - float(patient.wr_10_y1))
        return change_WR_T1_T2
    
#now find the mean change values from these newly created data set list 

    @classmethod
    def mean_WR_baseline_T1(cls):
        change_WR_baseline_T1 = cls.change_WR_baseline_T1()
        if not change_WR_baseline_T1:
            return None
        return sum(change_WR_baseline_T1) / len(change_WR_baseline_T1)

    @classmethod
    def mean_WR_baseline_T2(cls):
        change_WR_baseline_T2 = cls.change_WR_baseline_T2()
        if not change_WR_baseline_T2:
            return None
        return sum(change_WR_baseline_T2) / len(change_WR_baseline_T2)

    @classmethod
    def mean_WR_T1_T2(cls):
        change_WR_T1_T2 = cls.change_WR_T1_T2()
        if not change_WR_T1_T2:
            return None
        return sum(change_WR_T1_T2) / len(change_WR_T1_T2)
    
#now find the standard deviation of these values 
    @classmethod
    def SD_WR_baseline_T1(cls):
        change_WR_baseline_T1 = cls.change_WR_baseline_T1()
        if not change_WR_baseline_T1:
            return None
        mean = cls.mean_WR_baseline_T1()
        return (sum((x - mean) ** 2 for x in change_WR_baseline_T1) / len(change_WR_baseline_T1)) ** 0.5

    @classmethod
    def SD_WR_baseline_T2(cls):
        change_WR_baseline_T2 = cls.change_WR_baseline_T2()
        if not change_WR_baseline_T2:
            return None
        mean = cls.mean_WR_baseline_T2()
        return (sum((x - mean) ** 2 for x in change_WR_baseline_T2) / len(change_WR_baseline_T2)) ** 0.5

    @classmethod
    def SD_WR_T1_T2(cls):
        change_WR_T1_T2 = cls.change_WR_T1_T2()
        if not change_WR_T1_T2:
            return None
        mean = cls.mean_WR_T1_T2()
        return (sum((x - mean) ** 2 for x in change_WR_T1_T2) / len(change_WR_T1_T2)) ** 0.5
    
    #now caculate the standard response mean for each difference in time point 

    @classmethod
    def SRM_WR_baseline_T1(cls):
        mean = cls.mean_WR_baseline_T1()
        SD = cls.SD_WR_baseline_T1()
        return mean / SD if SD else None

    @classmethod
    def SRM_WR_baseline_T2(cls):
        mean = cls.mean_WR_baseline_T2()
        SD = cls.SD_WR_baseline_T2()
        return mean / SD if SD else None

    @classmethod
    def SRM_WR_T1_T2(cls):
        mean = cls.mean_WR_T1_T2()
        SD = cls.SD_WR_T1_T2()
        return mean / SD if SD else None

    