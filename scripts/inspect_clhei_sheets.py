import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

excel_path = 'outputs/괴산학술림_기후생명건강지수_평가결과.xlsx'
df_comp = pd.read_excel(excel_path, sheet_name=4)
print("--- Forest vs Control Comparison ---")
print(df_comp.to_string())

df_date = pd.read_excel(excel_path, sheet_name=3)
print("\n--- Date-wise Evaluation ---")
print(df_date.to_string())
