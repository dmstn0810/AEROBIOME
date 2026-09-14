import sys
from pathlib import Path
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

df_raw = pd.read_excel("괴산연습림 전체데이터.xlsx", sheet_name="원본")
df = df_raw.dropna(subset=['site no.']).copy()

# Load negative ion summary stats
ion_stats = pd.read_csv("outputs/site_summary_stats.csv")

print("=== Comparing Microbe Survey Time vs Negative Ion Survey Time ===")
for d in ['2026-04-15', '2026-04-29', '2026-07-27', '2026-08-13']:
    print(f"\n--- Date: {d} ---")
    sub_m = df[df['date'].astype(str).str.contains(d)]
    sub_i = ion_stats[ion_stats['date'] == d]
    
    for s_id in range(1, 11):
        m_rows = sub_m[sub_m['site no.'] == s_id]
        m_time = m_rows['time'].iloc[0] if not m_rows.empty else None
        
        i_row = sub_i[sub_i['site_id'] == s_id]
        if not i_row.empty:
            i_start = i_row['start_time'].iloc[0]
            i_end = i_row['end_time'].iloc[0]
            s_name = i_row['site_name'].iloc[0]
            print(f"Site {s_id:2d} ({s_name:10s}): Microbe Time = {str(m_time):8s} | Ion Time = {str(i_start)[11:]} ~ {str(i_end)[11:]}")
