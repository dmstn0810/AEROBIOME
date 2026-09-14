import sys
from pathlib import Path
import pandas as pd
import numpy as np
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

# 1. Load original microbe dataset
df_raw = pd.read_excel("괴산연습림 전체데이터.xlsx", sheet_name="원본")
# drop rows without site no.
df = df_raw.dropna(subset=['site no.']).copy()
df['site no.'] = df['site no.'].astype(int)

# 2. Load negative ion 1-second clean data
ion_df = pd.read_csv("data/ion_dataset_all.csv")
valid_ions = ion_df[ion_df['is_valid']].copy()
# 5 equal intervals of 180 seconds (3 minutes each)
valid_ions['interval_5'] = valid_ions['second_offset'] // 180

# 5 representative values per date & site
rep_ion = valid_ions.groupby(['date', 'site_id', 'interval_5'])['ion_value'].mean().reset_index()
rep_ion_dict = {}
for _, r in rep_ion.iterrows():
    rep_ion_dict[(str(r['date']), int(r['site_id']), int(r['interval_5']))] = round(r['ion_value'], 1)

print(f"Total calculated 5-rep ion values: {len(rep_ion_dict)} (expected 4 dates * 10 sites * 5 reps = 200)")

# 3. Handle 'n' and convert values in df
# Let's see rows within each (date, site no.)
df['rep_idx'] = df.groupby(['date', 'site no.']).cumcount() # 0 to 4

# Map n-ion
def get_n_ion(row):
    d_str = str(row['date'])[:10]
    s_id = int(row['site no.'])
    idx = int(row['rep_idx'])
    key = (d_str, s_id, idx)
    return rep_ion_dict.get(key, np.nan)

df['n-ion'] = df.apply(get_n_ion, axis=1)

print("\n--- Check n-ion assigned sample (2026-04-15 Site 1) ---")
print(df[df['date'].astype(str).str.contains('2026-04-15') & (df['site no.'] == 1)][['date', 'site no.', 'vege', 'rep_idx', 'n-ion']])

print("\n--- Check n-ion assigned sample (2026-08-13 Site 8) ---")
print(df[df['date'].astype(str).str.contains('2026-08-13') & (df['site no.'] == 8)][['date', 'site no.', 'vege', 'rep_idx', 'n-ion']])

# 4. Fill 'n' values
# Numeric columns
num_cols = ['air-temp', 'air-RH', 'windspeed', 'PM10', 'PM2.5', 'illum', 'soil-PH', 'soil-temp', 'soil-RH', 'PCA-B', 'PDA-F']

# Replace 'n' with np.nan first
for col in num_cols:
    df[col] = pd.to_numeric(df[col].replace('n', np.nan), errors='coerce')

# Convert microbial colony count to CFU/m^3: colony count / 0.1 = colony count * 10
# Note: do this before or after imputing?
# If we convert before or after, it's linear so either is fine, but converting first is standard.
# Let's keep both or convert in-place:
df['PCA-B_CFU'] = df['PCA-B'] / 0.1
df['PDA-F_CFU'] = df['PDA-F'] / 0.1

print("\n--- Missing counts before imputation ---")
print(df[num_cols + ['PCA-B_CFU', 'PDA-F_CFU']].isna().sum())

# Imputation Strategy:
# 1) Within each (date, site no.), impute NaN with the mean of available replicates
for col in ['air-temp', 'air-RH', 'windspeed', 'PM10', 'PM2.5', 'illum', 'PCA-B', 'PDA-F', 'PCA-B_CFU', 'PDA-F_CFU', 'soil-PH', 'soil-temp', 'soil-RH']:
    df[col] = df.groupby(['date', 'site no.'])[col].transform(lambda s: s.fillna(s.mean()))

# 2) For soil variables in Site 5 (주차장), all 5 replicates are NaN on that date!
# Impute using Site 4: 밭(대조구) on the same date (as 밭 is the control reference!)
print("\nMissing counts after within-site imputation:")
print(df[['air-temp', 'PCA-B_CFU', 'soil-PH']].isna().sum())

# For Site 5 soil, let's fill with Site 4 (밭 대조구) soil values of the same date
soil_cols = ['soil-PH', 'soil-temp', 'soil-RH']
for col in soil_cols:
    # get mapping of date -> site 4 mean
    site4_means = df[df['site no.'] == 4].groupby('date')[col].mean()
    # fill site 5 with site 4 mean
    site5_mask = (df['site no.'] == 5) & (df[col].isna())
    df.loc[site5_mask, col] = df.loc[site5_mask, 'date'].map(site4_means)

print("\nMissing counts after Site 5 soil imputation:")
print(df[soil_cols].isna().sum())
