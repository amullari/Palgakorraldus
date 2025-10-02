# -*- coding: utf-8 -*-
"""
Adjust salary rows for partial-month contracts.
Outputs: Salary_Table_Corrected.csv (same headers, modified values)
Dependencies: pandas, numpy, openpyxl
"""

import pandas as pd
import numpy as np
from pandas.tseries.offsets import MonthEnd

# --- CONFIG: failinimed (muuda ainult siin, kui sinu failinimed erinevad) ---
CONTRACTS_CSV = "Andmemudel/Contract_Table.csv"
SALARY_CSV = "Andmemudel/Salary_Table.csv"
WORKDAYS_XLSX = "Andmemudel/Working Time Calendar Table.xlsx"
OUTPUT_CSV = "Andmemudel/Salary_Table_Corrected.csv"

# --- CONFIG: veergude nimed (kui sinu veerud erinevad, muuda siin) ---
COL_EMP = "Employee ID"
COL_CON = "Contract ID"
COL_PERIOD = "Period"                    # Kuu esimene päev
COL_PERIOD_END = "Period_End_Date"       # Kuu viimane päev
COL_SALARY = "Salary"
COL_BENEFITS = "Benefits"
COL_ACTUAL = "Actual_Working_Days"
COL_MISSED = "Missed_Days"

# --- Lae failid ---
contracts = pd.read_csv(CONTRACTS_CSV, parse_dates=["Start Date", "End Date"])
salary = pd.read_csv(SALARY_CSV, dtype=str)  # laeme esmalt stringina, konverteerime allpool
workdays = pd.read_excel(WORKDAYS_XLSX, parse_dates=["Month"])

# Konverteeri vajalikud veerud kuupäevadeks (ohutult)
salary[COL_PERIOD] = pd.to_datetime(salary[COL_PERIOD], errors="coerce")
if COL_PERIOD_END in salary.columns:
    salary[COL_PERIOD_END] = pd.to_datetime(salary[COL_PERIOD_END], errors="coerce")
else:
    # kui pole, lisame (ei muuda pealkirja — lihtsalt lisame veeru)
    salary[COL_PERIOD_END] = pd.NaT

# konverteeri numeric veerud (sõltuvalt sisendist võivad olla tühjad)
def to_numeric_safe(s):
    return pd.to_numeric(s, errors="coerce")

for c in [COL_SALARY, COL_BENEFITS, COL_ACTUAL, COL_MISSED]:
    if c in salary.columns:
        salary[c] = to_numeric_safe(salary[c])
    else:
        # kui mõni veerg puudu, lisa NaN (aga script eeldab olemasolu)
        salary[c] = np.nan

# Tagame, et contracts kuupäevad on kuupäevad
contracts["Start Date"] = pd.to_datetime(contracts["Start Date"], errors="coerce")
contracts["End Date"] = pd.to_datetime(contracts["End Date"], errors="coerce")


# --- Fix: Period peab olema kuu esimene päev ---
salary[COL_PERIOD] = salary[COL_PERIOD].dt.to_period('M').dt.start_time

# Paranda Period end date (kuulõpp)
salary[COL_PERIOD_END] = salary[COL_PERIOD] + MonthEnd(0)

# Ühenda lepingute algus/lõpp Salary tabeliga, vasak-ühendus säilitab originaalread
merged = salary.merge(
    contracts[[COL_EMP, COL_CON, "Start Date", "End Date"]],
    on=[COL_CON],
    how="left"
)
# Alles jätame ainult read, kus leping kattub perioodiga
merged = merged[
    (merged["Start Date"] <= merged[COL_PERIOD_END]) &
    (merged["End Date"].isna()   | (merged["End Date"]   >= merged[COL_PERIOD]))
]
merged = merged.merge(
    workdays[["Month", "Working Days"]],
    left_on="Period_End_Date",
    right_on="Month",
    how="left"
)

# --- Grupipõhine töötlemine: Employee ID + Period ---
out_rows = []
grouped = merged.groupby([COL_EMP, COL_PERIOD], sort=False)

for (emp, period), group in grouped:
    # põhiväärtused
    # Veendu, et month_total_days olemas
    if "month_total_days" not in merged.columns:
        merged["month_total_days"] = (merged[COL_PERIOD_END] - merged[COL_PERIOD]).dt.days + 1

    # --- põhiväärtused grupi töötlemiseks ---
    month_wd = int(group["Working Days"].iloc[0]) if pd.notna(group["Working Days"].iloc[0]) else np.nan
    total_month_days = int(group["month_total_days"].iloc[0])

    # Kui tööpäevade kalender puudu või kuu päevade arv <= 0, jätame read muutmata
    if np.isnan(month_wd) or total_month_days <= 0:
        for _, row in group.iterrows():
            row = row.copy()
            row["Adjustment_Comment"] = "No working-days info; row left unchanged"
            out_rows.append(row)
        continue

    # coverage exact (float): fraction of calendar days covered
    group = group.copy()
    group["coverage_exact"] = group["days_covered"] / total_month_days

    # assigned working days (float)
    group["assigned_wd_exact"] = group["coverage_exact"] * month_wd

    # Largest remainder method -> integer allocation that sums to month_wd
    floors = np.floor(group["assigned_wd_exact"].values).astype(int)
    remainders = group["assigned_wd_exact"].values - floors
    need = month_wd - floors.sum()
    # protect
    if need < 0:
        # kui ümardus ületas — vähendame suurima floor väärtuse
        # (väga harv; siin lihtne korrigeerimine)
        # vähenda mitu korda kuni sum = month_wd
        idx_order = np.argsort(remainders)  # väikesim fraction esimesena
        i = 0
        while need < 0 and i < len(idx_order):
            j = idx_order[i]
            if floors[j] > 0:
                floors[j] -= 1
                need += 1
            i += 1
    else:
        # lisa +1 suurima fractional väärtusega ridadele
        idx_desc = np.argsort(-remainders)
        for j in idx_desc[:need]:
            floors[j] += 1

    group["Assigned_Working_Days"] = floors

    # --- Reeglid Actual working days (ja missaed days) ---
    # Kui originaalne sum(Actual working Days) > 0, püüame säilitada sama kokku (kui mõistlik)
    orig_total_actual = group[COL_ACTUAL].sum()
    if pd.notna(orig_total_actual) and orig_total_actual > 0:
        # jagame selle orig_total_actual proportsionaalselt Assigned_Working_Days
        target_total_actual = min(int(round(orig_total_actual)), month_wd)
        # proportionally by assigned days
        exacts = group["Assigned_Working_Days"].astype(float) / group["Assigned_Working_Days"].sum()
        exacts = exacts.fillna(1.0 / len(exacts))  # kui jagaja 0
        actual_exact = exacts * target_total_actual
        floors_a = np.floor(actual_exact).astype(int)
        rem_a = actual_exact - floors_a
        need_a = target_total_actual - floors_a.sum()
        idx_desc_a = np.argsort(-rem_a)
        for j in idx_desc_a[:need_a]:
            floors_a[j] += 1
        group[COL_ACTUAL] = floors_a
    else:
        # kui algselt pole andmeid, eeldame et tegelikult töötas vastavalt assigned WD
        group[COL_ACTUAL] = group["Assigned_Working_Days"]

    # Nüüd koostame missed_days nii, et sum(Actual) + sum(missed) = month_wd
    sum_actual = int(group[COL_ACTUAL].sum())
    needed_missed = month_wd - sum_actual
    if needed_missed < 0:
        # kui actual > month (erand), vähendame esimesel real
        # korrigeerime esimese rea actual
        idx0 = group.index[0]
        group.loc[idx0, COL_ACTUAL] = group.loc[idx0, COL_ACTUAL] + needed_missed  # needed_missed negative
        needed_missed = 0

    # Assign all missed to first contract (sorteeritud by eff_start then Start Date)
    group = group.sort_values(["eff_start", "Start Date"], na_position="last").reset_index(drop=True)
    group[COL_MISSED] = 0
    if needed_missed > 0:
        group.loc[0, COL_MISSED] = needed_missed

    # --- Salary & Benefits adjustment: püüame säilitada töötatud-päeva hinda ---
    # esmalt arvuta grupi sum orig salary & orig actual (orig as in input)
    sum_orig_salary = group[COL_SALARY].sum()
    sum_orig_actual = group[COL_ACTUAL].sum()  # note: we may have just changed this; but we prefer per-row original if present
    # For per-row: if original actual (before modification) existed, we should prefer to preserve original per-row daily rate.
    # Me salvestame enne muutmist orig_row_actual ja orig_row_salary:
    # (me ei salvestanud - seega teeme heuristiliselt: kui orig actual >0 use per-row rate; else fallback to group average)
    # To keep it simple & robust:
    # - If row had original non-zero Actual working Days (we stored earlier), use its daily = orig_salary / orig_actual.
    # - Else fallback to group-level daily = (sum of original salaries) / max(1, sum of original actuals) or monthly avg.

    # BUT: we lost original per-row actual when overwrote group[COL_ACTUAL]. 
    # To avoid that, re-fetch from merged (orig) using indices
    orig_rows = merged.loc[group.index]
    for idx, row in group.iterrows():
        orig_idx = row.name  # position in merged
        # get original values from merged
        orig_salary_val = merged.loc[orig_idx, COL_SALARY] if COL_SALARY in merged.columns else np.nan
        orig_actual_val = merged.loc[orig_idx, COL_ACTUAL] if COL_ACTUAL in merged.columns else np.nan
        orig_benef_val = merged.loc[orig_idx, COL_BENEFITS] if COL_BENEFITS in merged.columns else np.nan

        # decide daily salary rate:
        if pd.notna(orig_actual_val) and orig_actual_val > 0 and pd.notna(orig_salary_val):
            daily_salary = orig_salary_val / orig_actual_val
        else:
            # fallback: use group-average daily if possible
            if pd.notna(sum_orig_salary) and sum(orig_rows[COL_ACTUAL].fillna(0)) > 0:
                daily_salary = sum_orig_salary / max(sum(orig_rows[COL_ACTUAL].fillna(0)), 1)
            elif pd.notna(orig_salary_val):
                daily_salary = orig_salary_val / max(month_wd, 1)
            else:
                daily_salary = np.nan

        # Benefits: similar approach
        if pd.notna(orig_benef_val) and pd.notna(orig_actual_val) and orig_actual_val > 0:
            daily_benef = orig_benef_val / orig_actual_val
        else:
            # group-level fallback
            sum_orig_benef = group[COL_BENEFITS].sum()
            if pd.notna(sum_orig_benef) and sum(orig_rows[COL_ACTUAL].fillna(0)) > 0:
                daily_benef = sum_orig_benef / max(sum(orig_rows[COL_ACTUAL].fillna(0)), 1)
            elif pd.notna(orig_benef_val):
                daily_benef = orig_benef_val / max(month_wd, 1)
            else:
                daily_benef = np.nan

        # compute adjusted amounts based on new actual days
        adj_actual = int(row[COL_ACTUAL])
        adj_salary = (daily_salary * adj_actual) if pd.notna(daily_salary) else np.nan
        adj_benef = (daily_benef * adj_actual) if pd.notna(daily_benef) else np.nan

        # kirjutame ümber grupi reale
        group.at[idx, COL_SALARY] = round(adj_salary, 2) if pd.notna(adj_salary) else np.nan
        group.at[idx, COL_BENEFITS] = round(adj_benef, 2) if pd.notna(adj_benef) else np.nan

        # lisame väikese kommentaari
        group.at[idx, "Adjustment_Comment"] = "Split by contract days; salary/benefits adjusted to keep day-rate (fallbacks used where needed)"

    # append rows to out_rows
    for _, r in group.iterrows():
        out_rows.append(r)

# Koondame väljundi DataFrame ja säilitame originaalse kolonnijärjekorra + uued muudetud väärtused
out_df = pd.DataFrame(out_rows)

# Tagame, et kõik algsed veerud on kohal (kui mõni puudu, lisame NaN)
for col in salary.columns:
    if col not in out_df.columns:
        out_df[col] = np.nan

# Asetame veergude järjekorra sarnaseks algsele salary DataFrame'ile, kuid lisame Adjustment_Comment lõppu
cols_final = list(salary.columns)
if "Adjustment_Comment" in out_df.columns:
    cols_final = cols_final + ["Adjustment_Comment"]

out_df = out_df[cols_final]

# Salvesta tulemus (koos samade pealkirjadega)
out_df.to_csv(OUTPUT_CSV, index=False, date_format="%Y-%m-%d")

print(f"Töödeldud read: {len(out_df)}. Salvestatud: {OUTPUT_CSV}")
print("Märkused: 'Period' on seatud kuu esimesele päevale; 'Period end date' kuu lõpp. Vaata veergu 'Adjustment_Comment' täpsema selgituse jaoks.")
