import sys
from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv("data/ion_dataset_all.csv")
valid_df = df[df['is_valid']].copy()

dates = sorted(valid_df['date'].unique())

print("=== 1. Non-parametric Kruskal-Wallis Test across 4 Dates ===")
date_groups = [valid_df[valid_df['date'] == d]['ion_value'].values for d in dates]
kw_date = stats.kruskal(*date_groups)
print(f"Kruskal-Wallis across dates: H = {kw_date.statistic:.2f}, p-value = {kw_date.pvalue:.4e}")

print("\n=== 2. Forest vs Control Mann-Whitney U Test by Date ===")
for d in dates:
    f_vals = valid_df[(valid_df['date'] == d) & (valid_df['is_forest'])]['ion_value'].values
    c_vals = valid_df[(valid_df['date'] == d) & (~valid_df['is_forest'])]['ion_value'].values
    u_res = stats.mannwhitneyu(f_vals, c_vals, alternative='two-sided')
    print(f"[{d}] Mann-Whitney U: statistic = {u_res.statistic:.0f}, p-value = {u_res.pvalue:.4e}")
    # Effective sample size consideration:
    # If using session averages (N=8 forest vs N=2 control):
    f_means = valid_df[(valid_df['date'] == d) & (valid_df['is_forest'])].groupby('site_id')['ion_value'].mean().values
    c_means = valid_df[(valid_df['date'] == d) & (~valid_df['is_forest'])].groupby('site_id')['ion_value'].mean().values
    u_means = stats.mannwhitneyu(f_means, c_means, alternative='two-sided')
    print(f"     Session-means Mann-Whitney U (N=8 vs 2): statistic = {u_means.statistic:.0f}, p-value = {u_means.pvalue:.4f}")

print("\n=== 3. Species Group Kruskal-Wallis by Date ===")
species_map = {
    "리기다소나무림": "소나무류", "소나무림": "소나무류",
    "잣나무림 a": "잣나무류", "잣나무림 b": "잣나무류",
    "버드나무림 a": "버드나무류", "버드나무림 b": "버드나무류",
    "일본잎갈나무림 a": "낙엽송(일본잎갈나무)", "일본잎갈나무림 b": "낙엽송(일본잎갈나무)",
    "밭(대조구)": "대조구", "주차장(대조구)": "대조구"
}
valid_df['species_group'] = valid_df['site_name'].map(species_map)

for d in dates:
    sub = valid_df[valid_df['date'] == d]
    sp_grps = [sub[sub['species_group'] == sp]['ion_value'].values for sp in sub['species_group'].unique()]
    kw_sp = stats.kruskal(*sp_grps)
    print(f"[{d}] Kruskal-Wallis across species: H = {kw_sp.statistic:.2f}, p-value = {kw_sp.pvalue:.4e}")

print("\n=== 4. Within-site pairs comparison (a vs b) ===")
for d in dates:
    print(f"\n--- Date: {d} ---")
    for sp_name, s_a, s_b in [("잣나무림", "잣나무림 a", "잣나무림 b"),
                               ("버드나무림", "버드나무림 a", "버드나무림 b"),
                               ("일본잎갈나무림", "일본잎갈나무림 a", "일본잎갈나무림 b")]:
        val_a = valid_df[(valid_df['date'] == d) & (valid_df['site_name'] == s_a)]['ion_value'].mean()
        val_b = valid_df[(valid_df['date'] == d) & (valid_df['site_name'] == s_b)]['ion_value'].mean()
        print(f"  {sp_name}: a={val_a:.1f} vs b={val_b:.1f} (차이={val_b - val_a:+.1f})")
