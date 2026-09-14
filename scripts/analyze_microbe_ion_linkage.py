import sys
from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(str(Path.cwd()))

# Run dataset processing script to get clean df
from scripts.process_microbe_dataset import df

# Define species groups
species_map = {
    "리기다소나무림": "소나무류",
    "소나무림": "소나무류",
    "잣나무림 a": "잣나무류",
    "잣나무림 b": "잣나무류",
    "버드나무림 a": "버드나무류",
    "버드나무림 b": "버드나무류",
    "일본잎갈나무림 a": "낙엽송(일본잎갈나무)",
    "일본잎갈나무림 b": "낙엽송(일본잎갈나무)",
    "밭(대조구)": "대조구(밭)",
    "주차장(대조구)": "주차장(참고)"
}
df['species_group'] = df['vege'].map(species_map)
df['is_forest'] = df['site no.'].isin([1, 2, 3, 6, 7, 8, 9, 10])
df['is_control_field'] = df['site no.'] == 4 # 밭(대조구)

# -------------------------------------------------------------
# Analysis 1: Forest vs Field Control (밭) across dates
# -------------------------------------------------------------
print("=== 1. Forest vs Field Control (밭) Comparison ===")
# Filter dates where n-ion is available (4 dates)
ion_dates = ['2026-04-15', '2026-04-29', '2026-07-27', '2026-08-13']
df_ion = df[df['date'].astype(str).str[:10].isin(ion_dates)].copy()

fc_comp = []
for d in ion_dates:
    sub = df_ion[df_ion['date'].astype(str).str.contains(d)]
    forest = sub[sub['is_forest']]
    field = sub[sub['is_control_field']]
    
    # metrics: PCA-B_CFU, PDA-F_CFU, n-ion
    row = {
        'date': d,
        'forest_bact_mean': forest['PCA-B_CFU'].mean(),
        'field_bact_mean': field['PCA-B_CFU'].mean(),
        'bact_ratio(F/C)': forest['PCA-B_CFU'].mean() / field['PCA-B_CFU'].mean(),
        'forest_fungi_mean': forest['PDA-F_CFU'].mean(),
        'field_fungi_mean': field['PDA-F_CFU'].mean(),
        'fungi_ratio(F/C)': forest['PDA-F_CFU'].mean() / field['PDA-F_CFU'].mean(),
        'forest_ion_mean': forest['n-ion'].mean(),
        'field_ion_mean': field['n-ion'].mean(),
        'ion_ratio(F/C)': forest['n-ion'].mean() / field['n-ion'].mean(),
    }
    fc_comp.append(row)

fc_df = pd.DataFrame(fc_comp)
print(fc_df.to_string())

# -------------------------------------------------------------
# Analysis 2: Species Comparison
# -------------------------------------------------------------
print("\n=== 2. Species Group Means across Ion Dates ===")
sp_summary = df_ion.groupby('species_group').agg(
    n=('site no.', 'count'),
    bact_mean=('PCA-B_CFU', 'mean'),
    bact_sd=('PCA-B_CFU', 'std'),
    fungi_mean=('PDA-F_CFU', 'mean'),
    fungi_sd=('PDA-F_CFU', 'std'),
    ion_mean=('n-ion', 'mean'),
    ion_sd=('n-ion', 'std'),
    temp_mean=('air-temp', 'mean'),
    rh_mean=('air-RH', 'mean')
).round(1)
print(sp_summary.to_string())

# -------------------------------------------------------------
# Analysis 3: Correlation between n-ion and microbes
# -------------------------------------------------------------
print("\n=== 3. Correlation between n-ion and Airborne Microbes ===")
# Overall in 4 dates
valid_pairs = df_ion.dropna(subset=['n-ion', 'PCA-B_CFU', 'PDA-F_CFU'])
r_bact_p, p_bact_p = stats.pearsonr(valid_pairs['n-ion'], valid_pairs['PCA-B_CFU'])
r_bact_s, p_bact_s = stats.spearmanr(valid_pairs['n-ion'], valid_pairs['PCA-B_CFU'])

r_fungi_p, p_fungi_p = stats.pearsonr(valid_pairs['n-ion'], valid_pairs['PDA-F_CFU'])
r_fungi_s, p_fungi_s = stats.spearmanr(valid_pairs['n-ion'], valid_pairs['PDA-F_CFU'])

print(f"Overall (N={len(valid_pairs)}):")
print(f"  n-ion vs PCA-B (Bacteria): Pearson r = {r_bact_p:.3f} (p={p_bact_p:.4e}), Spearman rho = {r_bact_s:.3f} (p={p_bact_s:.4e})")
print(f"  n-ion vs PDA-F (Fungi):    Pearson r = {r_fungi_p:.3f} (p={p_fungi_p:.4e}), Spearman rho = {r_fungi_s:.3f} (p={p_fungi_s:.4e})")

# Within Forest sites only
forest_pairs = valid_pairs[valid_pairs['is_forest']]
r_fbact_p, p_fbact_p = stats.pearsonr(forest_pairs['n-ion'], forest_pairs['PCA-B_CFU'])
r_ffungi_p, p_ffungi_p = stats.pearsonr(forest_pairs['n-ion'], forest_pairs['PDA-F_CFU'])
print(f"\nWithin Forest Sites Only (N={len(forest_pairs)}):")
print(f"  n-ion vs PCA-B (Bacteria): Pearson r = {r_fbact_p:.3f} (p={p_fbact_p:.4e})")
print(f"  n-ion vs PDA-F (Fungi):    Pearson r = {r_ffungi_p:.3f} (p={p_ffungi_p:.4e})")

# By date correlations
print("\nCorrelation by Survey Date:")
for d in ion_dates:
    d_pairs = valid_pairs[valid_pairs['date'].astype(str).str.contains(d)]
    rb, pb = stats.pearsonr(d_pairs['n-ion'], d_pairs['PCA-B_CFU'])
    rf, pf = stats.pearsonr(d_pairs['n-ion'], d_pairs['PDA-F_CFU'])
    print(f"[{d}] vs Bacteria: r={rb:+.3f} (p={pb:.3f}) | vs Fungi: r={rf:+.3f} (p={pf:.3f})")

# Full environmental correlation matrix
env_cols = ['PCA-B_CFU', 'PDA-F_CFU', 'n-ion', 'air-temp', 'air-RH', 'windspeed', 'PM10', 'PM2.5', 'illum', 'soil-PH', 'soil-temp', 'soil-RH']
corr_matrix = df_ion[env_cols].corr()
print("\n--- Environmental Correlation with Microbes and Ion ---")
print(corr_matrix[['PCA-B_CFU', 'PDA-F_CFU', 'n-ion']].round(3))
