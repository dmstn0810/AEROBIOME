import sys
from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats

sys.stdout.reconfigure(encoding='utf-8')

# Read the finalized, cleaned dataset
df = pd.read_excel("괴산연습림 전체데이터.xlsx", sheet_name="원본")

# Standardize column names
df['PCA-B_CFU'] = df['PCA-B (CFU/m3)']
df['PDA-F_CFU'] = df['PDA-F (CFU/m3)']
# Find the n-ion column name (might have unicode char)
ion_col = [c for c in df.columns if 'n-ion' in c][0]
df['n-ion'] = df[ion_col]

species_map = {
    "리기다소나무림": "소나무류", "소나무림": "소나무류",
    "잣나무림 a": "잣나무류", "잣나무림 b": "잣나무류",
    "버드나무림 a": "버드나무류", "버드나무림 b": "버드나무류",
    "일본잎갈나무림 a": "낙엽송(일본잎갈나무)", "일본잎갈나무림 b": "낙엽송(일본잎갈나무)",
    "밭(대조구)": "대조구(밭)", "주차장(대조구)": "주차장(참고)"
}
df['species_group'] = df['vege'].map(species_map)
df['forest_type'] = df['vege'].map({
    "리기다소나무림": "침엽수림", "소나무림": "침엽수림", "잣나무림 a": "침엽수림", "잣나무림 b": "침엽수림", "일본잎갈나무림 a": "침엽수림", "일본잎갈나무림 b": "침엽수림",
    "버드나무림 a": "활엽수림", "버드나무림 b": "활엽수림",
    "밭(대조구)": "농경지(대조구)", "주차장(대조구)": "인공포장지(참고)"
})
df['is_forest'] = df['site no.'].isin([1, 2, 3, 6, 7, 8, 9, 10])
df['is_field'] = df['site no.'] == 4

# Bacteria-to-Fungi ratio (B/F ratio)
df['BF_ratio'] = df['PCA-B_CFU'] / (df['PDA-F_CFU'] + 1e-5)

dates = sorted(df['date'].unique())
print(f"Total records: {len(df)} across {len(dates)} dates")

# 1. Seasonal summary across all 6 dates
print("\n=== 1. Seasonal Trajectory of Microbes across 6 Dates ===")
season_stats = df.groupby('date').agg(
    bact_mean=('PCA-B_CFU', 'mean'),
    bact_median=('PCA-B_CFU', 'median'),
    bact_sd=('PCA-B_CFU', 'std'),
    fungi_mean=('PDA-F_CFU', 'mean'),
    fungi_median=('PDA-F_CFU', 'median'),
    fungi_sd=('PDA-F_CFU', 'std'),
    bf_mean=('BF_ratio', 'mean'),
    temp=('air-temp', 'mean'),
    rh=('air-RH', 'mean'),
    pm10=('PM10', 'mean'),
    pm25=('PM2.5', 'mean')
).round(2)
print(season_stats.to_string())

# 2. Forest vs Field control across all 6 dates
print("\n=== 2. Forest vs Field Control (밭) across All 6 Dates ===")
f_vs_c = []
for d in dates:
    sub = df[df['date'] == d]
    f = sub[sub['is_forest']]
    c = sub[sub['is_field']]
    row = {
        'date': str(d)[:10],
        'f_bact': f['PCA-B_CFU'].mean(),
        'c_bact': c['PCA-B_CFU'].mean(),
        'bact_p': stats.mannwhitneyu(f['PCA-B_CFU'], c['PCA-B_CFU']).pvalue,
        'f_fungi': f['PDA-F_CFU'].mean(),
        'c_fungi': c['PDA-F_CFU'].mean(),
        'fungi_p': stats.mannwhitneyu(f['PDA-F_CFU'], c['PDA-F_CFU']).pvalue,
        'f_bf': f['BF_ratio'].mean(),
        'c_bf': c['BF_ratio'].mean(),
    }
    f_vs_c.append(row)
f_vs_c_df = pd.DataFrame(f_vs_c).round(2)
print(f_vs_c_df.to_string())

# 3. Forest Type Comparison across All 6 Dates
print("\n=== 3. Forest Type Comparison across All 6 Dates ===")
ft_stats = df.groupby('forest_type').agg(
    n=('site no.', 'count'),
    bact_mean=('PCA-B_CFU', 'mean'),
    bact_median=('PCA-B_CFU', 'median'),
    fungi_mean=('PDA-F_CFU', 'mean'),
    fungi_median=('PDA-F_CFU', 'median'),
    bf_mean=('BF_ratio', 'mean'),
    pm25_mean=('PM2.5', 'mean')
).round(2)
print(ft_stats.to_string())

# Kruskal-Wallis across forest types
kw_bact = stats.kruskal(*[df[df['forest_type'] == ft]['PCA-B_CFU'] for ft in df['forest_type'].unique()])
kw_fungi = stats.kruskal(*[df[df['forest_type'] == ft]['PDA-F_CFU'] for ft in df['forest_type'].unique()])
print(f"Kruskal-Wallis across forest types: Bacteria H={kw_bact.statistic:.2f} (p={kw_bact.pvalue:.4e}), Fungi H={kw_fungi.statistic:.2f} (p={kw_fungi.pvalue:.4e})")

# 4. Multiple Linear Regression for Microbe Concentrations
print("\n=== 4. Multiple Regression Model for Bacteria and Fungi ===")
reg_cols = ['air-temp', 'air-RH', 'windspeed', 'PM10', 'PM2.5', 'illum', 'soil-temp', 'soil-RH']

def run_ols(X_mat, y_vec, col_names):
    X_design = np.column_stack([np.ones(len(X_mat)), X_mat])
    beta, residuals, rank, s = np.linalg.lstsq(X_design, y_vec, rcond=None)
    n = len(y_vec)
    p = X_design.shape[1]
    y_pred = X_design @ beta
    ss_tot = np.sum((y_vec - np.mean(y_vec))**2)
    ss_res = np.sum((y_vec - y_pred)**2)
    r2 = 1 - ss_res / ss_tot
    adj_r2 = 1 - (1 - r2) * (n - 1) / (n - p)
    sigma2 = ss_res / (n - p)
    cov_beta = sigma2 * np.linalg.inv(X_design.T @ X_design)
    se_beta = np.sqrt(np.diagonal(cov_beta))
    t_stats = beta / se_beta
    p_vals = [2 * (1 - stats.t.cdf(np.abs(t), df=n-p)) for t in t_stats]
    
    res_df = pd.DataFrame({
        'coef': beta,
        'std err': se_beta,
        't': t_stats,
        'P>|t|': p_vals
    }, index=['const'] + col_names).round(4)
    return r2, adj_r2, res_df

X_data = df[reg_cols].values
r2_b, adj_r2_b, res_b = run_ols(X_data, df['PCA-B_CFU'].values, reg_cols)
print(f"--- Bacteria (PCA-B CFU/m3) OLS: R2 = {r2_b:.3f}, Adj R2 = {adj_r2_b:.3f} ---")
print(res_b.to_string())

r2_f, adj_r2_f, res_f = run_ols(X_data, df['PDA-F_CFU'].values, reg_cols)
print(f"\n--- Fungi (PDA-F CFU/m3) OLS: R2 = {r2_f:.3f}, Adj R2 = {adj_r2_f:.3f} ---")
print(res_f.to_string())

# 5. Species level breakdown across all 6 dates
print("\n=== 5. Species Level Breakdown across All 6 Dates ===")
sp_all = df.groupby('species_group').agg(
    n=('site no.', 'count'),
    bact_mean=('PCA-B_CFU', 'mean'),
    bact_median=('PCA-B_CFU', 'median'),
    fungi_mean=('PDA-F_CFU', 'mean'),
    fungi_median=('PDA-F_CFU', 'median'),
    bf_mean=('BF_ratio', 'mean')
).round(2)
print(sp_all.to_string())

# Save detailed outputs
f_vs_c_df.to_csv("outputs/microbe_forest_vs_control_6dates.csv", index=False, encoding='utf-8-sig')
ft_stats.to_csv("outputs/microbe_forest_type_stats.csv", encoding='utf-8-sig')
sp_all.to_csv("outputs/microbe_species_all_dates_stats.csv", encoding='utf-8-sig')
print("\nSaved deep microbe stats to outputs/")
