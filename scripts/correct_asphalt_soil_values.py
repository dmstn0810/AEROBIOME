import sys
import io
from pathlib import Path
import pandas as pd
import numpy as np

# Ensure UTF-8 output
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

workspace_dir = Path(r"C:\Users\user\orca\workspaces\괴산 공기미생물\음이온-2")
master_file = workspace_dir / "괴산연습림 전체데이터.xlsx"

df = pd.read_excel(master_file)
print(f"[INFO] Loaded master dataset: {df.shape}")

# Site 5 is asphalt pavement (주차장 대조구): soil measurements are impossible
# Set soil-PH, soil-temp, soil-RH to NaN for Site 5
site5_mask = df['site no.'] == 5
print(f"[INFO] Found {site5_mask.sum()} rows for Site 5 (주차장)")

df.loc[site5_mask, ['soil-PH', 'soil-temp', 'soil-RH']] = np.nan
print("[OK] Set soil-PH, soil-temp, soil-RH to NaN for Site 5 (아스팔트 포장)")

# Save back to master Excel file
df.to_excel(master_file, index=False)
print(f"[OK] Successfully saved updated {master_file}")

# Verify
df_verify = pd.read_excel(master_file)
s5_soil = df_verify.loc[df_verify['site no.'] == 5, ['soil-PH', 'soil-temp', 'soil-RH']]
print(f"[VERIFY] Site 5 null count:\n{s5_soil.isnull().sum()}")
print(f"[VERIFY] Non-Site 5 null count:\n{df_verify.loc[df_verify['site no.'] != 5, ['soil-PH', 'soil-temp', 'soil-RH']].isnull().sum()}")
