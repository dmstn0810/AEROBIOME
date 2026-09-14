import sys
from pathlib import Path
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

df_raw = pd.read_excel("괴산연습림 전체데이터.xlsx", sheet_name="원본")
df = df_raw.dropna(subset=['site no.']).copy()

print("--- Inspecting rows with 'n' in PCA-B or PDA-F ---")
n_microbe = df[(df['PCA-B'] == 'n') | (df['PDA-F'] == 'n')]
print(n_microbe[['date', 'site no.', 'vege', 'air-temp', 'soil-PH', 'PCA-B', 'PDA-F']])

print("\n--- Inspecting pattern of 'n' in weather/environmental columns ---")
# For each date and site, which rows (1st, 2nd, 3rd, 4th, 5th) have 'n'?
df['row_in_site'] = df.groupby(['date', 'site no.']).cumcount() + 1
for col in ['air-temp', 'soil-PH', 'PCA-B', 'PDA-F']:
    print(f"\nValue of 'row_in_site' where {col} == 'n':")
    print(df[df[col] == 'n']['row_in_site'].value_counts())
