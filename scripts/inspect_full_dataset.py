import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

# Read excel sheet '원본'
df_raw = pd.read_excel("괴산연습림 전체데이터.xlsx", sheet_name="원본")
# drop rows where site no is null
df = df_raw.dropna(subset=['site no.']).copy()
print(f"Total non-empty rows: {len(df)}")
print("Columns:", list(df.columns))

print("\nDates in 괴산연습림 전체데이터:")
print(df['date'].value_counts().sort_index())

print("\nSites in 괴산연습림 전체데이터:")
print(df[['site no.', 'vege']].drop_duplicates())

print("\nRows per (date, site no.):")
print(df.groupby(['date', 'site no.']).size().value_counts())

print("\nLet's check 'n' occurrences across columns:")
for col in df.columns:
    n_count = (df[col] == 'n').sum()
    null_count = df[col].isna().sum()
    print(f"  {col}: 'n'={n_count}, isna={null_count}")

# Check sample rows for one site on one date
sample_sub = df[(df['date'] == df['date'].iloc[0]) & (df['site no.'] == 1)]
print("\nSample (date 1, site 1):")
print(sample_sub.to_string())

# Check 2026-04-15 sample if exists
apr15 = df[df['date'].astype(str).str.contains('2026-04-15')]
if not apr15.empty:
    print("\nSample for 2026-04-15 site 1:")
    print(apr15[apr15['site no.'] == 1].to_string())
