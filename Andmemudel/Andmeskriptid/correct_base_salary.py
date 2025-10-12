"""
Adjust base salary to ensure base salary unchanged during the year 
Dependencies: pandas, numpy
"""
import pandas as pd
import numpy as np

# --- CONFIG: failinimed ---
WORKDAYS_XLSX = "Andmemudel/Working Time Calendar Table.xlsx"
SALARY_CSV = "Andmemudel/Salary_Table_Corrected.csv"
OUTPUT_CSV = "Andmemudel/Salary_Table_Corrected_Salary.csv"

# --- CONFIG: veerud ---
COL_EMP = "Employee ID"
COL_CON = "Contract ID"
COL_PERIOD = "Period"
COL_PERIOD_END = "Period_End_Date"
COL_SALARY = "Salary"
COL_BENEFITS = "Benefits"
COL_ACTUAL = "Actual_Working_Days"
COL_MISSED = "Missed_Days"

# --- Lae failid ---

salary = pd.read_csv(SALARY_CSV, parse_dates=["Period", "Period_End_Date"])
workdays = pd.read_excel(WORKDAYS_XLSX, parse_dates=["Month"])
cols_keep = [COL_CON, COL_PERIOD,COL_PERIOD_END,COL_SALARY, COL_BENEFITS,COL_ACTUAL,COL_MISSED]
# Numbriliste veergude ohutu konverteerimine

for c in [COL_SALARY, COL_BENEFITS, COL_ACTUAL, COL_MISSED]:
    salary[c] = pd.to_numeric(salary[c], errors="coerce")
# lisa normtööpäevade arv
merged = salary.merge(
    workdays[["Month", "Working Days"]],
    left_on=COL_PERIOD_END,
    right_on="Month",
    how="left"
)
out_rows = []
grouped = merged.groupby([COL_CON], sort=False)
for (contr), group in grouped:
    group = group.copy()
    # leia esimeselt realt päevapalga suurus ja arvuta kuupalk töötatud päevade arvu alusel

    daily_salary = group[COL_SALARY].iloc[0]/(group["Working Days"] - group[COL_MISSED].iloc[0])
    group[COL_SALARY] = np.round(daily_salary * group[COL_ACTUAL],2)
    out_rows.extend(group[cols_keep].to_dict("records"))
# --- Lõpptulemus ---
out_df = pd.DataFrame(out_rows)

# Salvesta
out_df.to_csv(OUTPUT_CSV, index=False, date_format="%Y-%m-%d")

print(f"Töödeldud read: {len(out_df)}. Salvestatud: {OUTPUT_CSV}")