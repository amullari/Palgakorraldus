import pandas as pd
import numpy as np
import random
from datetime import timedelta

# --- Faili lugemine ---
file_path = "Andmemudel/Andmeskript/Contract_Table.csv"   # <- siia pane oma algse faili nimi
df = pd.read_csv(file_path)

# Kuupäevad datetime kujule
df["Start Date"] = pd.to_datetime(df["Start Date"], errors="coerce")
df["End Date"] = pd.to_datetime(df["End Date"], errors="coerce")

# --- Abifunktsioon juhusliku kuupäeva genereerimiseks 2024 ---
def random_date_2024(min_start=None):
    if random.random() < 0.75:
        season = random.choice(["spring", "autumn"])
        if season == "spring":
            start, end = pd.to_datetime("2024-03-01"), pd.to_datetime("2024-05-31")
        else:
            start, end = pd.to_datetime("2024-09-01"), pd.to_datetime("2024-11-30")
    else:
        month = random.choice([1,2,6,7,8,12])
        start = pd.to_datetime(f"2024-{month:02d}-01")
        if month == 2:
            end = pd.to_datetime("2024-02-29")  # liigaasta
        elif month in [1,3,5,7,8,10,12]:
            end = pd.to_datetime(f"2024-{month:02d}-31")
        else:
            end = pd.to_datetime(f"2024-{month:02d}-30")
    
    # Kui ette on antud lepingu alguskuupäev, korrigeerime vahemikku
    if min_start is not None:
        if start < min_start:
            start = min_start
        if end <= start:
            end = pd.to_datetime("2024-12-31")
    
    delta = (end - start).days
    return start + pd.to_timedelta(np.random.randint(0, delta+1), unit="D")

# --- Lepingute parandamine ---
df_fixed = df.copy()
changes = []

for idx, row in df_fixed[df_fixed["Contract ID"].str.endswith("U")].iterrows():
    emp_id = row["Employee ID"]
    base_contract_id = row["Contract ID"][:-1]

    mask = (df_fixed["Employee ID"] == emp_id) & (df_fixed["Contract ID"] == base_contract_id)
    if mask.any():
        new_start = random_date_2024(min_start=df_fixed.loc[mask, "Start Date"].values[0])

        # Jätkulepingu uued kuupäevad
        old_start = df_fixed.loc[idx, "Start Date"]
        df_fixed.loc[idx, "Start Date"] = new_start
        df_fixed.loc[idx, "End Date"] = pd.NaT

        # Algse lepingu lõpp = uus algus –1 päev
        old_end = df_fixed.loc[mask, "End Date"].values[0]
        new_end = new_start - timedelta(days=1)
        if df_fixed.loc[mask, "Start Date"].values[0] > np.datetime64(new_end):
            new_end = df_fixed.loc[mask, "Start Date"].values[0]
        df_fixed.loc[mask, "End Date"] = new_end

        # Raporti jaoks
        changes.append({
            "Employee ID": emp_id,
            "Base Contract": base_contract_id,
            "Base End (old)": old_end,
            "Base End (new)": new_end,
            "Update Contract": row["Contract ID"],
            "Update Start (old)": old_start,
            "Update Start (new)": new_start
        })

# --- Kontroll: ükski leping ei lõppe enne algust ---
for idx, row in df_fixed.iterrows():
    start, end = row["Start Date"], row["End Date"]
    if pd.notna(start) and pd.notna(end) and end < start:
        df_fixed.loc[idx, "End Date"] = start

# --- Failide salvestamine ---
df_fixed.to_csv("Contract_Table_Updated.csv", index=False)
pd.DataFrame(changes).to_csv("Contract_Fix_Report.csv", index=False)

print("Valmis! Uuendatud fail: Contract_Table_Updated.csv")
print("Raport muudatustest: Contract_Fix_Report.csv")
