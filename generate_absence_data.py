import pandas as pd
import numpy as np
from datetime import datetime

from load_lists import generate_absence_reasons, df_absence_reason

current_date = datetime.today().date()  

def generate_absence_data(df: pd.DataFrame) -> pd.DataFrame:
    """Generate absence data for employees based on their absence rates and employment periods."""
    absence_records = []

    # Process each employee
    for _, row in df.iterrows():
        join_date = row["Join Date"]
        leave_date = row["Leave Date"] if pd.notnull(row["Leave Date"]) else current_date
        absence_rate = row["Absence Rate"]
        employee_id = row["EmployeeId"]

        # Generate working days between join and leave date
        working_days = pd.date_range(start=join_date, end=leave_date, freq='B')  # 'B' is business day freq

        # Generate random values and filter by absence rate
        random_vals = np.random.rand(len(working_days))
        absent_days = working_days[random_vals < absence_rate]

        # Append records to the list
        absence_records.extend([(employee_id, date) for date in absent_days])

    # Create the absence DataFrame
    df_absence = pd.DataFrame(absence_records, columns=["EmployeeId", "Date"])
    return df_absence

# Generate absence data

df_employee = pd.read_csv("./outputs/employee.csv")
print(df_employee.head())

df_absence = generate_absence_data(df_employee)

def generate_absence_reasons(n: int) -> pd.Series:
    return df_absence_reason['Name'].sample(
        n=n, 
        weights=df_absence_reason['Probability'], 
        replace=True
    ).reset_index(drop=True)

reason_series = generate_absence_reasons(10)
# Add absence reasons to the absence DataFrame
df_absence['Reason'] = generate_absence_reasons(len(df_absence))    

# Save the result
df_absence.to_csv("./outputs/absence.csv", index=False)

# Preview the result
print("Absence data generated:")
print(df_absence.head())

