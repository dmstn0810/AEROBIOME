import pandas as pd
import json

excel_path = 'outputs/괴산학술림_기후생명건강지수_평가결과.xlsx'
xls = pd.ExcelFile(excel_path)
print("Sheet names:", xls.sheet_names)

import sys
sys.stdout.reconfigure(encoding='utf-8')
df_site = pd.read_excel(excel_path, sheet_name=1)
print("--- Site Evaluation ---")
print(df_site.to_string())

df_vege = pd.read_excel(excel_path, sheet_name=2)
print("\n--- Vegetation Group Evaluation ---")
print(df_vege.to_string())

