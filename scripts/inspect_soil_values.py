import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

df_raw = pd.read_excel("괴산연습림 전체데이터.xlsx", sheet_name="원본")
df = df_raw.dropna(subset=['site no.']).copy()

# List of columns that have 'n'
# Weather: air-temp, air-RH, windspeed, PM10, PM2.5, illum
# Soil: soil-PH, soil-temp, soil-RH
# Microbe: PCA-B, PDA-F

# For each site on each date, let's see what happens if we replace 'n' with NaN and then:
# 1. Weather: 3 values exist in rows 1..3, rows 4..5 are NaN. If we forward-fill or fill with mean of that (date, site):
# Let's see if mean of rows 1..3 is appropriate.
# 2. Microbe: If PCA-B or PDA-F has 'n' in rows 4..5, fill with mean of the valid rows of that site on that date.
# 3. Soil: For site 5 (주차장), all rows are 'n'. If all rows are 'n', what should it be filled with?
# Let's check what values exist for other sites' soil on that date!
for col in ['soil-PH', 'soil-temp', 'soil-RH']:
    print(f"\n{col} on 2026-04-15 by site:")
    sub = df[df['date'].astype(str).str.contains('2026-04-15')]
    for s_id, grp in sub.groupby('site no.'):
        print(f"  Site {s_id}: {list(grp[col])}")
