import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

df_raw = pd.read_excel("괴산연습림 전체데이터.xlsx", sheet_name="원본")
df = df_raw.dropna(subset=['site no.']).copy()

numeric_cols = ['air-temp', 'air-RH', 'windspeed', 'PM10', 'PM2.5', 'illum', 'soil-PH', 'soil-temp', 'soil-RH', 'PCA-B', 'PDA-F']

print("=== Checking 'n' occurrences per column and date ===")
for d, grp in df.groupby('date'):
    print(f"\nDate: {d}")
    for col in numeric_cols:
        n_cnt = (grp[col] == 'n').sum()
        if n_cnt > 0:
            print(f"  {col}: {n_cnt} 'n's")
