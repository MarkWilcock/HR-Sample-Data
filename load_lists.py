import pandas as pd

# Load the AbsenceReason worksheet from the Excel file
df_absence_reason = pd.read_excel('inputs/HR Lists.xlsx', sheet_name='AbsenceReason')
#print(df_absence_reason.head())

def generate_absence_reasons(n):
    return df_absence_reason['Name'].sample(
        n=n, 
        weights=df_absence_reason['Probability'], 
        replace=True
    ).reset_index(drop=True)

#reason_series = generate_absence_reasons(10)
#print(reason_series)
