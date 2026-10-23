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
        if self.lag_months_y1 == '' or self.lag_months_y2 == '' or self.wr_10_baseline == '' or self.wr_10_y1 == '' or self.wr_10_y2 == '' or self.ff_baseline_L == '' or self.ff_y1_L == '' or self.ff_y2_L == '' or self.ff_baseline_R == '' or self.ff_y1_R == '' or self.ff_y2_R == '':
            print("Data point removed for this patient because missing data value")
        else:
            Patient.all_patients.append(self)

    def __repr__(self):
        return f"Patient(subject_id={self.subject_id}, ff_baseline_R={self.ff_baseline_R}, ff_y1_R={self.ff_y1_R}, ff_y2_R={self.ff_y2_R}, ff_baseline_L={self.ff_baseline_L}, ff_y1_L={self.ff_y1_L}, ff_y2_L={self.ff_y2_L}, lag_months_y1={self.lag_months_y1}, lag_months_y2={self.lag_months_y2}, wr_10_baseline={self.wr_10_baseline}, wr_10_y1={self.wr_10_y1}, wr_10_y2={self.wr_10_y2})"


    @classmethod
    def instantiate_from_csv(cls, filename):
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

class SelectedPatient:
    #this list is the directory for every following method, once the data points are added by the constructor the other methods can refer to it for thier functions 
    selected_patients = []
    #Constructor builds objects and assign the values age of onset, gender, gene type, and years of education to them for later use
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
    def instantiate_from_csv(cls, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                SelectedPatient(
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
                    row['wr_10_y2']
                )
