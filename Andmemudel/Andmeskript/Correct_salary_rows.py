import pandas as pd
import numpy as np

# Lae failid
contracts = pd.read_csv("Andmemudel/Andmeskript/Contract_Table.csv", parse_dates=["Start Date", "End Date"])
salary = pd.read_csv("Andmemudel/Salary_Table.csv", parse_dates=["Period"])
working_time = pd.read_excel("Andmemudel/Working Time Calendar Table.xlsx", parse_dates=["Month"])

# Kui Period on ainult kuu-tekst, teisenda kuupäevaks
if salary["Period"].dtype == "object":
    salary["Period"] = pd.to_datetime(salary["Period"], format="%Y-%m")

# Ühenda palgafail lepingutega
merged = salary.merge(contracts[["Employee ID","Contract ID","Start Date","End Date"]], on=["Employee ID","Contract ID"], how="left")

# Ühenda tööpäevade tabeliga
merged = merged.merge(working_time[["Month","Working Days"]], left_on="Period", right_on="Month", how="left", suffixes=("","_Month"))
merged = merged.drop(columns=["Month_Month"])  # eemaldame dubleeritud veeru

# Funktsioon arvutab osalise kuu proportsiooni
def adjust_partial_month(row):
    start_date = row["Start Date"]
    end_date = row["End Date"]
    period_start = row["Period"].replace(day=1)
    period_end = (row["Period"] + pd.offsets.MonthEnd(0))
    total_working_days = row["Working Days"]
    
    # Algus kuupäeva piiramine lepingu algusega
    effective_start = max(start_date, period_start)
    # Lõpu kuupäeva piiramine lepingu lõpuga (või kuu lõpp)
    effective_end = min(end_date if not pd.isna(end_date) else period_end, period_end)
    
    # Kui leping ei kata kuud üldse, tagastame NaN
    if effective_end < effective_start:
        return pd.Series([np.nan]*4)
    
    # Arvuta proportsioon
    days_covered = (effective_end - effective_start).days + 1
    proportion = days_covered / (period_end - period_start).days + 1e-6  # väike offset jagamise vältimiseks
    
    # Arvuta proportsionaalsed väärtused
    adjusted_salary = row["Salary Amount"] * proportion
    adjusted_benefits = row["Benefits"] * proportion if "Benefits" in row else np.nan
    adjusted_actual_working_days = row["actual_working_days"] * proportion if "actual_working_days" in row else total_working_days * proportion
    adjusted_missed_days = row["missed_days"] * proportion if "missed_days" in row else 0
    
    return pd.Series([adjusted_salary, adjusted_benefits, adjusted_actual_working_days, adjusted_missed_days])

# Rakenda funktsioon ainult kehtivatele ridadele
valid_rows = merged[
    (merged["Start Date"] <= merged["Period"] + pd.offsets.MonthEnd(0)) &
    ((merged["End Date"].isna()) | (merged["Period"] <= merged["End Date"]))
]

adjusted_values = valid_rows.apply(adjust_partial_month, axis=1)
adjusted_values.columns = ["Salary_Adjusted","Benefits_Adjusted","Actual_Working_Days_Adjusted","Missed_Days_Adjusted"]

# Lisa veerud tagasi
valid_rows = pd.concat([valid_rows.reset_index(drop=True), adjusted_values], axis=1)

# Salvesta uus palgafail
valid_rows.to_csv("Salary_Table_Corrected_Partial.csv", index=False)
print("Uus palgafail loodud: Salary_Table_Corrected_Partial.csv")
