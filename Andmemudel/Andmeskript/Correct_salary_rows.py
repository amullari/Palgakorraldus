# -*- coding: utf-8 -*-
"""
Adjust salary rows for partial-month contracts.
Outputs: Salary_Table_Corrected.csv (same headers, modified values)
Dependencies: pandas, numpy, openpyxl
"""

import pandas as pd
import numpy as np
from pandas.tseries.offsets import MonthEnd

# --- CONFIG: failinimed ---
CONTRACTS_CSV = "Andmemudel/Contract_Table.csv"
SALARY_CSV = "Andmemudel/Salary_Table.csv"
WORKDAYS_XLSX = "Andmemudel/Working Time Calendar Table.xlsx"
OUTPUT_CSV = "Andmemudel/Salary_Table_Corrected.csv"

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
contracts = pd.read_csv(CONTRACTS_CSV, parse_dates=["Start Date", "End Date"])
salary = pd.read_csv(SALARY_CSV, dtype=str)
workdays = pd.read_excel(WORKDAYS_XLSX, parse_dates=["Month"])

# Kuupäevade konverteerimine
salary[COL_PERIOD] = pd.to_datetime(salary[COL_PERIOD], errors="coerce")
if COL_PERIOD_END not in salary.columns:
    salary[COL_PERIOD_END] = pd.NaT
salary[COL_PERIOD_END] = pd.to_datetime(salary[COL_PERIOD_END], errors="coerce")

# Numbriliste veergude ohutu konverteerimine
def to_numeric_safe(s):
    return pd.to_numeric(s, errors="coerce")

for c in [COL_SALARY, COL_BENEFITS, COL_ACTUAL, COL_MISSED]:
    if c not in salary.columns:
        salary[c] = np.nan
    else:
        salary[c] = to_numeric_safe(salary[c])

# Paranda perioodid kuu alguse/lõpu järgi
salary[COL_PERIOD] = salary[COL_PERIOD].dt.to_period("M").dt.start_time
salary[COL_PERIOD_END] = salary[COL_PERIOD] + MonthEnd(0)

# --- Ühenda lepingud ja tööpäevade kalender ---
merged = salary.merge(
    contracts[[COL_EMP, COL_CON, "Start Date", "End Date"]],
    on=[COL_CON],
    how="left"
)
merged = merged[
    (merged["Start Date"] <= merged[COL_PERIOD_END]) &
    (merged["End Date"].isna() | (merged["End Date"] >= merged[COL_PERIOD]))
]
merged = merged.merge(
    workdays[["Month", "Working Days"]],
    left_on=COL_PERIOD_END,
    right_on="Month",
    how="left"
)

# --- Arvuta kuu päevade ja kattuvuse info ---
merged["month_total_days"] = (merged[COL_PERIOD_END] - merged[COL_PERIOD]).dt.days + 1
merged["eff_start"] = merged[[COL_PERIOD, "Start Date"]].max(axis=1)
merged["eff_end"] = merged[[COL_PERIOD_END, "End Date"]].min(axis=1)
merged["days_covered"] = (merged["eff_end"] - merged["eff_start"]).dt.days + 1
merged.loc[merged["days_covered"] < 0, "days_covered"] = 0

# --- Grupipõhine töötlemine ---
out_rows = []
grouped = merged.groupby([COL_EMP, COL_PERIOD], sort=False)

for (emp, period), group in grouped:
    group = group.copy()
    month_wd = group["Working Days"].iloc[0]
    # Eeldame, et kuu tööpäevad = actual + missed
    # kasutame esimeselt realt väärtusi (sama kuu sees peaks olema sama)
    total_actual = group[COL_ACTUAL].iloc[0]
    total_missed = group[COL_MISSED].iloc[0]

    # Kui mõlemal real sama väärtus (nt mõlemal 15 ja 8) → võtame ühe korra
    """     if len(group) > 1 and total_actual == group[COL_ACTUAL].iloc[1]:
        total_actual = total_actual / len(group)
        total_missed = total_missed / len(group)
    """
    total_days = group["month_total_days"].iloc[0]

    if pd.isna(month_wd) or total_days <= 0:
        group["Adjustment_Comment"] = "No working-days info; row left unchanged"
        out_rows.extend(group.to_dict("records"))
        continue

    # --- Jagame kuu tööpäevad proportsionaalselt päevade kattuvusega ---
    group["coverage_exact"] = group["days_covered"] / total_days
    group["Assigned_Working_Days"] = np.floor(group["coverage_exact"] * month_wd).astype(int)

    # Korrektsioon ümarduse jäägi jaoks
    remainder = int(month_wd) - group["Assigned_Working_Days"].sum()
    if remainder != 0:
        remainders = (group["coverage_exact"] * month_wd) - group["Assigned_Working_Days"]
        idx_sort = np.argsort(-remainders if remainder > 0 else remainders)
        for j in idx_sort[:abs(remainder)]:
            group.loc[group.index[j], "Assigned_Working_Days"] += np.sign(remainder)

    # --- Jaota actual ja missed päevad proportsionaalselt ---
    total_assigned = group["Assigned_Working_Days"].sum()
    if total_assigned > 0:
        group[COL_ACTUAL] = np.round((group["Assigned_Working_Days"] / total_assigned) * total_actual).astype(int)
        group[COL_MISSED] = np.round((group["Assigned_Working_Days"] / total_assigned) * total_missed).astype(int)

    group["Adjustment_Comment"] = "Adjusted proportionally for overlapping contracts"
    out_rows.extend(group.to_dict("records"))

# --- Lõpptulemus ---
out_df = pd.DataFrame(out_rows)

# Lisa puuduolevad veerud ja korrigeeri järjekord
for col in salary.columns:
    if col not in out_df.columns:
        out_df[col] = np.nan
cols_final = list(salary.columns)
if "Adjustment_Comment" in out_df.columns:
    cols_final += ["Assigned_Working_Days", "Adjustment_Comment"]
out_df = out_df[cols_final]

# Salvesta
out_df.to_csv(OUTPUT_CSV, index=False, date_format="%Y-%m-%d")

print(f"Töödeldud read: {len(out_df)}. Salvestatud: {OUTPUT_CSV}")
print("Kuu tööpäevad jagatud proportsionaalselt lepingute vahel.")
