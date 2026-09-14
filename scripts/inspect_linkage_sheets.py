import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

excel_path = 'outputs/괴산연습림_공기미생물_음이온_종합연계분석.xlsx'
xls = pd.ExcelFile(excel_path)
print("Sheet names in linkage analysis:", xls.sheet_names)

for s in xls.sheet_names:
    print(f"--- Sheet: {s} ---")
    df_s = pd.read_excel(excel_path, sheet_name=s)
    print(df_s.head(5).to_string())
