import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

df_raw = pd.read_excel("괴산연습림 전체데이터.xlsx", sheet_name="원본")
df = df_raw.dropna(subset=['site no.']).copy()

print("Dates and rows breakdown:")
for d, grp in df.groupby('date'):
    print(f"Date: {d} -> total rows: {len(grp)}, sites: {grp['site no.'].nunique()}")
    site_counts = grp['site no.'].value_counts().to_dict()
    print(f"  site counts: {site_counts}")

print("\nLet's check PCA-B and PDA-F on all dates:")
for d, grp in df.groupby('date'):
    pca_n = (grp['PCA-B'] == 'n').sum()
    pda_n = (grp['PDA-F'] == 'n').sum()
    print(f"Date: {d} -> PCA-B 'n' count: {pca_n}, PDA-F 'n' count: {pda_n}")
