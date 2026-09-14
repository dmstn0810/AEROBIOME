import pandas as pd
import json
import numpy as np

df = pd.read_excel('괴산연습림 전체데이터.xlsx')

# Map date formats
# '2026-03-04' -> '260304'
def date_key(d):
    s = str(d)[:10].replace('-', '')
    return s[2:] # '260304'

df['dkey'] = df['date'].apply(date_key)
dates = sorted(df['dkey'].unique().tolist())
print("Dates keys:", dates)

metrics = {
    'TAF_CFU_m3': 'PDA-F_CFU',
    'TAB_CFU_m3': 'PCA-B_CFU',
    'n-ion': 'n-ion',
    'air-temp': 'air-temp',
    'air-RH': 'air-RH',
    'PM10': 'PM10',
    'soil-temp': 'soil-temp',
    'windspeed': 'windspeed'
}

site_metric_data = {}

for d in dates:
    sub_df = df[df['dkey'] == d]
    site_metric_data[d] = {}
    for m_out, m_in in metrics.items():
        vals = []
        for s in range(1, 11):
            s_rows = sub_df[sub_df['site no.'] == s]
            if len(s_rows) > 0:
                v = s_rows[m_in].mean()
                if pd.isna(v):
                    vals.append(None)
                else:
                    vals.append(round(float(v), 1))
            else:
                vals.append(None)
        site_metric_data[d][m_out] = vals

# All dates combined
site_metric_data['all'] = {}
for m_out, m_in in metrics.items():
    vals = []
    for s in range(1, 11):
        s_rows = df[df['site no.'] == s]
        v = s_rows[m_in].mean()
        if pd.isna(v):
            vals.append(None)
        else:
            vals.append(round(float(v), 1))
    site_metric_data['all'][m_out] = vals

with open('site_metric_data_7dates.json', 'w', encoding='utf-8') as f:
    json.dump(site_metric_data, f, ensure_ascii=False, indent=2)

print("Generated site_metric_data_7dates.json successfully!")
