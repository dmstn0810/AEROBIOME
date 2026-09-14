import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv("data/ion_dataset_all.csv")

print("=== Artifacts Check: Zeros & 998/999 ===")
for date in df['date'].unique():
    sub = df[df['date'] == date]
    print(f"\n--- Date: {date} ---")
    zeros = sub[sub['ion_value'] == 0]
    nines = sub[sub['ion_value'].isin([998, 999])]
    print(f"Zero count: {len(zeros)} (sites: {zeros['site_name'].value_counts().to_dict()})")
    print(f"998/999 count: {len(nines)} (sites: {nines['site_name'].value_counts().to_dict()})")

print("\n--- Distribution of values near 998/999 for 밭(대조구) on 2026-04-15 ---")
sub = df[(df['date'] == '2026-04-15') & (df['site_name'] == '밭(대조구)')]
print(sub['ion_value'].describe())
print("Value counts near 0 and 999:")
print("0s:", (sub['ion_value'] == 0).sum())
print("999s:", (sub['ion_value'] == 999).sum())
print("values between 1 and 998 count:", ((sub['ion_value'] > 0) & (sub['ion_value'] < 999)).sum())
print("Histogram bins of ion_value:")
print(pd.cut(sub['ion_value'], bins=[0, 1, 100, 300, 500, 700, 900, 998, 1000], include_lowest=True).value_counts().sort_index())

print("\n--- Let's see some sequential values in 밭(대조구) on 2026-04-15 ---")
print(sub[['second_offset', 'ion_value']].iloc[350:380].to_string())
