import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

# Load clean ion dataset
ion_df = pd.read_csv("data/ion_dataset_all.csv")
valid_ions = ion_df[ion_df['is_valid']].copy()

# Add 5-interval block (0..4)
# 900 seconds // 180 = 0, 1, 2, 3, 4
valid_ions['interval_5'] = valid_ions['second_offset'] // 180

# Compute 5 representative values per date and site
rep_5 = valid_ions.groupby(['date', 'site_id', 'site_name', 'interval_5'])['ion_value'].agg(['mean', 'median', 'std', 'count']).reset_index()

print("Sample 5 representative values for Date 2026-04-15 Site 1:")
print(rep_5[(rep_5['date'] == '2026-04-15') & (rep_5['site_id'] == 1)])

print("\nSample 5 representative values for Date 2026-08-13 Site 8 (버드나무림 b):")
print(rep_5[(rep_5['date'] == '2026-08-13') & (rep_5['site_id'] == 8)])
