import sys
from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv("data/ion_dataset_all.csv")
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['hour_float'] = df['timestamp'].dt.hour + df['timestamp'].dt.minute / 60.0 + df['timestamp'].dt.second / 3600.0

# Filter valid
valid_df = df[df['is_valid']].copy()

print("=== 1. Summary by Date and Site ===")
site_stats = valid_df.groupby(['date', 'site_id', 'site_name', 'site_type', 'is_forest']).agg(
    n=('ion_value', 'count'),
    mean=('ion_value', 'mean'),
    std=('ion_value', 'std'),
    median=('ion_value', 'median'),
    q25=('ion_value', lambda x: np.percentile(x, 25)),
    q75=('ion_value', lambda x: np.percentile(x, 75)),
    min=('ion_value', 'min'),
    max=('ion_value', 'max'),
    start_time=('timestamp', 'min'),
    end_time=('timestamp', 'max'),
    start_hour=('hour_float', 'min')
).reset_index()

site_stats['cv'] = site_stats['std'] / site_stats['mean'] * 100 # %
site_stats['iqr'] = site_stats['q75'] - site_stats['q25']
site_stats['rank_within_date'] = site_stats.groupby('date')['mean'].rank(ascending=False, method='min')

# Let's save site_stats
Path("outputs").mkdir(parents=True, exist_ok=True)
site_stats.to_csv("outputs/site_summary_stats.csv", index=False, encoding='utf-8-sig')

print("\nTop 3 sites by date:")
for d, grp in site_stats.groupby('date'):
    top = grp.sort_values('mean', ascending=False).head(3)
    print(f"[{d}]")
    for _, r in top.iterrows():
        print(f"  {int(r['rank_within_date'])}위: {r['site_name']} (평균 {r['mean']:.1f}, SD {r['std']:.1f})")

print("\n=== 2. Forest vs Control Comparison ===")
fc_stats = valid_df.groupby(['date', 'is_forest']).agg(
    n=('ion_value', 'count'),
    mean=('ion_value', 'mean'),
    std=('ion_value', 'std'),
    median=('ion_value', 'median')
).reset_index()
fc_stats['category'] = fc_stats['is_forest'].map({True: '산림(8지점)', False: '대조구(밭·주차장)'})
print(fc_stats[['date', 'category', 'n', 'mean', 'std', 'median']])

# Forest vs Control ratio
fc_pivot = fc_stats.pivot(index='date', columns='category', values='mean')
fc_pivot['산림/대조구 배율'] = fc_pivot['산림(8지점)'] / fc_pivot['대조구(밭·주차장)']
print("\n산림 vs 대조구 배율:")
print(fc_pivot)

print("\n=== 3. Tree Species Grouping ===")
species_group = {
    "소나무류(소나무·리기다)": ["소나무림", "리기다소나무림"],
    "잣나무류": ["잣나무림 a", "잣나무림 b"],
    "버드나무류": ["버드나무림 a", "버드나무림 b"],
    "낙엽송(일본잎갈나무)": ["일본잎갈나무림 a", "일본잎갈나무림 b"],
    "대조구": ["밭(대조구)", "주차장(대조구)"]
}
inv_species = {}
for k, v in species_group.items():
    for s in v:
        inv_species[s] = k
valid_df['species_group'] = valid_df['site_name'].map(inv_species)

spec_stats = valid_df.groupby(['date', 'species_group']).agg(
    n=('ion_value', 'count'),
    mean=('ion_value', 'mean'),
    std=('ion_value', 'std'),
    median=('ion_value', 'median')
).reset_index()

spec_pivot = spec_stats.pivot(index='species_group', columns='date', values='mean')
spec_pivot['전체평균'] = valid_df.groupby('species_group')['ion_value'].mean()
spec_pivot['8월/4월(15일)배율'] = spec_pivot['2026-08-13'] / spec_pivot['2026-04-15']
print("\n수종별 일자별 평균 및 배율:")
print(spec_pivot.round(1))

print("\n=== 4. Autocorrelation (Lag-1) and Session Trends ===")
# Compute lag-1 autocorrelation for each site session
autocorr_results = []
for (d, s_id, s_name), grp in valid_df.groupby(['date', 'site_id', 'site_name']):
    vals = grp['ion_value'].values
    if len(vals) > 1:
        corr = np.corrcoef(vals[:-1], vals[1:])[0, 1]
    else:
        corr = np.nan
    # slope per minute
    time_min = grp['second_offset'].values / 60.0
    slope, intercept, r_val, p_val, std_err = stats.linregress(time_min, vals)
    first_min = vals[:60].mean()
    last_min = vals[-60:].mean()
    autocorr_results.append({
        'date': d,
        'site_id': s_id,
        'site_name': s_name,
        'lag1_corr': corr,
        'slope_per_min': slope,
        'first_min_mean': first_min,
        'last_min_mean': last_min,
        'delta_last_first': last_min - first_min
    })
ac_df = pd.DataFrame(autocorr_results)
print("Average lag-1 autocorrelation across all 40 sessions:", ac_df['lag1_corr'].mean())
print("Min lag-1:", ac_df['lag1_corr'].min(), "Max lag-1:", ac_df['lag1_corr'].max())
