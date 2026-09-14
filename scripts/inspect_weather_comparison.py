import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_excel("괴산연습림 전체데이터.xlsx", sheet_name="원본")

# Let's see survey weather averages per date and site
weather_summary = df.groupby('date').agg(
    start_time=('time', 'min'),
    end_time=('time', 'max'),
    temp_mean=('air-temp', 'mean'),
    temp_min=('air-temp', 'min'),
    temp_max=('air-temp', 'max'),
    rh_mean=('air-RH', 'mean'),
    rh_min=('air-RH', 'min'),
    rh_max=('air-RH', 'max'),
    wind_mean=('windspeed', 'mean'),
    wind_max=('windspeed', 'max'),
    pm10_mean=('PM10', 'mean'),
    pm25_mean=('PM2.5', 'mean'),
    illum_mean=('illum', 'mean'),
    soil_temp=('soil-temp', 'mean'),
    soil_rh=('soil-RH', 'mean')
).round(2)

print("=== On-site Microclimate Weather at Konkuk Univ Goesan Forest ===")
print(weather_summary.to_string())

# Also let's inspect site by site weather on each date to see Forest vs Field control weather buffering
print("\n=== Forest vs Field Control (밭) Microclimate Comparison ===")
df['is_forest'] = df['site no.'].isin([1, 2, 3, 6, 7, 8, 9, 10])
df['is_field'] = df['site no.'] == 4

f_vs_c_weather = []
for d, grp in df.groupby('date'):
    f = grp[grp['is_forest']]
    c = grp[grp['is_field']]
    f_vs_c_weather.append({
        'date': str(d)[:10],
        'forest_temp': round(f['air-temp'].mean(), 1),
        'field_temp': round(c['air-temp'].mean(), 1),
        'temp_diff(F-C)': round(f['air-temp'].mean() - c['air-temp'].mean(), 1),
        'forest_rh': round(f['air-RH'].mean(), 1),
        'field_rh': round(c['air-RH'].mean(), 1),
        'rh_diff(F-C)': round(f['air-RH'].mean() - c['air-RH'].mean(), 1),
        'forest_wind': round(f['windspeed'].mean(), 2),
        'field_wind': round(c['windspeed'].mean(), 2),
        'forest_pm25': round(f['PM2.5'].mean(), 1),
        'field_pm25': round(c['PM2.5'].mean(), 1)
    })
print(pd.DataFrame(f_vs_c_weather).to_string())
