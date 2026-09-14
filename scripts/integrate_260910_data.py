import pandas as pd
import numpy as np
import io
import sys
from pathlib import Path

# Ensure UTF-8 console output
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

workspace_dir = Path(r"C:\Users\user\orca\workspaces\괴산 공기미생물\음이온-2")

# 1. Read existing master dataset (298 rows)
master_path = workspace_dir / "괴산연습림 전체데이터.xlsx"
df_master = pd.read_excel(master_path)
print(f"Existing master dataset shape: {df_master.shape}")

# 2. Read new 260910 data from copy workbook (sheet 2)
copy_path = workspace_dir / "괴산연습림 전체데이터 copy.xlsx"
xls_copy = pd.ExcelFile(copy_path)
df_copy = pd.read_excel(copy_path, sheet_name=xls_copy.sheet_names[2])
df_0910_raw = df_copy[df_copy['date'].astype(str).str.contains('09-10|260910')].copy()
print(f"Raw 260910 rows extracted: {len(df_0910_raw)}")

# 3. Read 음이온_260910.xlsx and compute 5-interval means per site
ion_path = workspace_dir / "음이온_260910.xlsx"
xls_ion = pd.ExcelFile(ion_path)

ion_interval_means = {}
ion_1sec_records = []

site_vege_map = {
    1: '리기다소나무림',
    2: '잣나무림 a',
    3: '버드나무림 a',
    4: '밭(대조구)',
    5: '주차장(대조구)',
    6: '소나무림',
    7: '일본잎갈나무림 a',
    8: '버드나무림 b',
    9: '일본잎갈나무림 b',
    10: '잣나무림 b'
}

for s in range(1, 11):
    df_ion_s = pd.read_excel(ion_path, sheet_name=str(s))
    # Row 0 is header text, rows 1.. have values
    data_rows = df_ion_s.iloc[1:].copy()
    ion_vals = pd.to_numeric(data_rows.iloc[:, 3], errors='coerce').dropna().values
    
    # 5-interval partition
    chunks = np.array_split(ion_vals, 5)
    means = [round(float(np.mean(c)), 2) for c in chunks]
    ion_interval_means[s] = means
    
    # Also collect 1-sec records for ion_dataset_all.csv
    site_name = site_vege_map[s]
    is_forest = (s not in [4, 5])
    site_type = "대조구" if s in [4, 5] else "산림"
    
    for sec_idx, val in enumerate(ion_vals):
        time_str = str(data_rows.iloc[sec_idx, 2])
        ion_1sec_records.append({
            'date': '2026-09-10',
            'site_id': s,
            'site_name': site_name,
            'site_type': site_type,
            'is_forest': is_forest,
            'second_offset': sec_idx + 1,
            'minute_bucket': (sec_idx // 60) + 1,
            'timestamp': time_str,
            'ion_raw': float(val),
            'ion_value': float(val),
            'is_valid': True
        })

print("[OK] Computed 5-interval ion means for all 10 sites:")
for s, m in ion_interval_means.items():
    print(f"  Site {s:2d} ({site_vege_map[s]}): {m}")

# 4. Process 260910 rows for master dataset
df_0910 = df_0910_raw.copy().reset_index(drop=True)

# Preserve raw colony counts
df_0910['PCA-B (콜로니수)'] = pd.to_numeric(df_0910['PCA-B'], errors='coerce')
df_0910['PDA-F (콜로니수)'] = pd.to_numeric(df_0910['PDA-F'], errors='coerce')

# Convert colony counts to CFU/m3 (colony / 0.1 = colony * 10)
df_0910['PCA-B (CFU/m3)'] = df_0910['PCA-B (콜로니수)'] * 10.0
df_0910['PDA-F (CFU/m3)'] = df_0910['PDA-F (콜로니수)'] * 10.0

# Map n-ion values
n_ion_list = []
for s in range(1, 11):
    site_means = ion_interval_means[s]
    n_ion_list.extend(site_means)

df_0910['n-ion (개/cm3)'] = n_ion_list

# Impute Site 5 (주차장 대조구) soil values with Site 4 (밭 대조구) means of 260910
site4_soil_means = df_0910[df_0910['site no.'] == 4][['soil-PH', 'soil-temp', 'soil-RH']].astype(float).mean()

for col in ['soil-PH', 'soil-temp', 'soil-RH']:
    val_to_impute = round(float(site4_soil_means[col]), 2)
    # Replace 'n' or NaN in Site 5
    mask = (df_0910['site no.'] == 5)
    df_0910.loc[mask, col] = val_to_impute
    # Ensure numeric
    df_0910[col] = pd.to_numeric(df_0910[col], errors='coerce')

# Map clean vege names
df_0910['vege'] = df_0910['site no.'].map(site_vege_map)

# Reorder columns to exactly match df_master
master_cols = df_master.columns.tolist()
# Note: In df_master, column 15 is 'n-ion (개/cm3)'
df_0910_final = df_0910[[
    'site no.', 'date', 'time', 'vege',
    'air-temp', 'air-RH', 'windspeed', 'PM10', 'PM2.5', 'illum',
    'soil-PH', 'soil-temp', 'soil-RH',
    'PCA-B (CFU/m3)', 'PDA-F (CFU/m3)', 'n-ion (개/cm3)',
    'PCA-B (콜로니수)', 'PDA-F (콜로니수)'
]].copy()

# Ensure exact same column names
df_0910_final.columns = master_cols

# 5. Concatenate with df_master
df_combined = pd.concat([df_master, df_0910_final], ignore_index=True)
print(f"\n[OK] Combined master dataset shape: {df_combined.shape} (298 + 50 = 348 rows)")
# Standardize date column to string 'YYYY-MM-DD'
df_combined['date'] = pd.to_datetime(df_combined['date']).dt.strftime('%Y-%m-%d')
print(f"Date distribution:\n{df_combined['date'].value_counts().sort_index()}")

# Save updated master dataset
df_combined.to_excel(master_path, index=False)
print(f"[OK] Successfully saved updated master dataset to: {master_path}")

# 6. Append to data/ion_dataset_all.csv
ion_csv_path = workspace_dir / "data" / "ion_dataset_all.csv"
df_ion_all_prev = pd.read_csv(ion_csv_path)
df_ion_0910 = pd.DataFrame(ion_1sec_records)
df_ion_all_new = pd.concat([df_ion_all_prev, df_ion_0910], ignore_index=True)
df_ion_all_new.to_csv(ion_csv_path, index=False)
print(f"[OK] Appended {len(df_ion_0910)} rows to {ion_csv_path}. New total rows: {len(df_ion_all_new)}")

print("\n=== DATA INTEGRATION OF 260910 COMPLETE ===")
