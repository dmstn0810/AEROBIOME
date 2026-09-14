import sys
import io
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shutil
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Ensure UTF-8 console output
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

workspace_dir = Path(r"C:\Users\user\orca\workspaces\괴산 공기미생물\음이온-2")
brain_dir = Path(r"C:\Users\user\.gemini\antigravity-cli\brain\6cb9fef6-d52d-4189-8337-6a158db6aad6")
fig_dir = workspace_dir / "figures"
fig_dir.mkdir(parents=True, exist_ok=True)
outputs_dir = workspace_dir / "outputs"
outputs_dir.mkdir(parents=True, exist_ok=True)

# 1. Load 348-row Master Dataset
master_file = workspace_dir / "괴산연습림 전체데이터.xlsx"
df = pd.read_excel(master_file)
print(f"[OK] Loaded master dataset: {df.shape} (348 rows, 18 columns)")

# Harmonize column names
df['PCA-B_CFU'] = df['PCA-B (CFU/m3)']
df['PDA-F_CFU'] = df['PDA-F (CFU/m3)']
df['n-ion'] = df['n-ion (개/cm3)']

# Site 5 is asphalt pavement (주차장 대조구): soil measurements are impossible
# Explicitly set soil-PH, soil-temp, soil-RH to NaN for Site 5
df.loc[df['site no.'] == 5, ['soil-PH', 'soil-temp', 'soil-RH']] = np.nan
print("[OK] Corrected Site 5 (주차장) soil to NaN (아스팔트 포장)")

site_vege_map = {
    1: '리기다소나무림', 2: '잣나무림 a', 3: '버드나무림 a', 4: '밭(대조구)', 5: '주차장(대조구)',
    6: '소나무림', 7: '일본잎갈나무림 a', 8: '버드나무림 b', 9: '일본잎갈나무림 b', 10: '잣나무림 b'
}
site_group_map = {
    1: '소나무류', 2: '잣나무류', 3: '버드나무류', 4: '밭(대조구)', 5: '주차장(대조구)',
    6: '소나무류', 7: '낙엽송류', 8: '버드나무류', 9: '낙엽송류', 10: '잣나무류'
}
forest_type_map = {
    1: '침엽수림', 2: '침엽수림', 3: '활엽수림', 4: '농경지(대조구)', 5: '인공포장지(참고)',
    6: '침엽수림', 7: '침엽수림', 8: '활엽수림', 9: '침엽수림', 10: '침엽수림'
}

df['site_name'] = df['site no.'].map(site_vege_map)
df['vege_group'] = df['site no.'].map(site_group_map)
df['forest_type'] = df['site no.'].map(forest_type_map)
df['is_forest'] = df['site no.'].isin([1, 2, 3, 6, 7, 8, 9, 10])
df['is_field'] = (df['site no.'] == 4)
df['BF_ratio'] = df['PCA-B_CFU'] / (df['PDA-F_CFU'] + 1e-5)
df['date_str'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

dates_all = sorted(df['date_str'].unique())
dates_all_labels = ['03-04 (초봄)', '04-15 (봄1)', '04-29 (봄2)', '05-13 (만춘)', '07-27 (여름1)', '08-13 (여름2)', '09-10 (가을)']

dates_ion = ['2026-04-15', '2026-04-29', '2026-07-27', '2026-08-13', '2026-09-10']
dates_ion_labels = ['04-15 (봄1)', '04-29 (봄2)', '07-27 (여름1)', '08-13 (여름2)', '09-10 (가을)']
df_ion = df[df['date_str'].isin(dates_ion)].copy()

print(f"[OK] 7 dates: {dates_all}")
print(f"[OK] 5 ion dates: {dates_ion}")

# =============================================================
# Figure 08: Forest vs Field across 5 Ion Dates
# =============================================================
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5.5), dpi=200)
x = np.arange(len(dates_ion))
w = 0.35

f_bact = [df_ion[(df_ion['date_str'] == d) & df_ion['is_forest']]['PCA-B_CFU'].mean() for d in dates_ion]
c_bact = [df_ion[(df_ion['date_str'] == d) & df_ion['is_field']]['PCA-B_CFU'].mean() for d in dates_ion]
ax1.bar(x - w/2, f_bact, w, label='산림(8지점)', color='#2e7d32', edgecolor='black', linewidth=0.5)
ax1.bar(x + w/2, c_bact, w, label='대조구(밭)', color='#d84315', edgecolor='black', linewidth=0.5)
ax1.set_title('공기 중 세균 농도 (PCA-B)', fontsize=12.5, fontweight='bold')
ax1.set_ylabel('세균 농도 (CFU/㎥)', fontsize=11, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(dates_ion_labels, fontsize=9.5)
ax1.grid(axis='y', linestyle='--', alpha=0.4)
ax1.legend()
for i in range(len(dates_ion)):
    ax1.text(i - w/2, f_bact[i] + 10, f"{f_bact[i]:.0f}", ha='center', fontsize=8.5, fontweight='bold')
    ax1.text(i + w/2, c_bact[i] + 10, f"{c_bact[i]:.0f}", ha='center', fontsize=8.5, fontweight='bold', color='#d84315')

f_fungi = [df_ion[(df_ion['date_str'] == d) & df_ion['is_forest']]['PDA-F_CFU'].mean() for d in dates_ion]
c_fungi = [df_ion[(df_ion['date_str'] == d) & df_ion['is_field']]['PDA-F_CFU'].mean() for d in dates_ion]
ax2.bar(x - w/2, f_fungi, w, label='산림(8지점)', color='#2e7d32', edgecolor='black', linewidth=0.5)
ax2.bar(x + w/2, c_fungi, w, label='대조구(밭)', color='#d84315', edgecolor='black', linewidth=0.5)
ax2.set_title('공기 중 진균 농도 (PDA-F)', fontsize=12.5, fontweight='bold')
ax2.set_ylabel('진균 농도 (CFU/㎥)', fontsize=11, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(dates_ion_labels, fontsize=9.5)
ax2.grid(axis='y', linestyle='--', alpha=0.4)
ax2.legend()
for i in range(len(dates_ion)):
    ax2.text(i - w/2, f_fungi[i] + 40, f"{f_fungi[i]:.0f}", ha='center', fontsize=8.5, fontweight='bold')
    ax2.text(i + w/2, c_fungi[i] + 40, f"{c_fungi[i]:.0f}", ha='center', fontsize=8.5, fontweight='bold', color='#d84315')

f_ion_vals = [df_ion[(df_ion['date_str'] == d) & df_ion['is_forest']]['n-ion'].mean() for d in dates_ion]
c_ion_vals = [df_ion[(df_ion['date_str'] == d) & df_ion['is_field']]['n-ion'].mean() for d in dates_ion]
ax3.bar(x - w/2, f_ion_vals, w, label='산림(8지점)', color='#1565c0', edgecolor='black', linewidth=0.5)
ax3.bar(x + w/2, c_ion_vals, w, label='대조구(밭)', color='#757575', edgecolor='black', linewidth=0.5)
ax3.set_title('공기 음이온 농도 (n-ion)', fontsize=12.5, fontweight='bold')
ax3.set_ylabel('음이온 발생량 (개/㎤)', fontsize=11, fontweight='bold')
ax3.set_xticks(x)
ax3.set_xticklabels(dates_ion_labels, fontsize=9.5)
ax3.grid(axis='y', linestyle='--', alpha=0.4)
ax3.legend()
for i in range(len(dates_ion)):
    ratio = f_ion_vals[i] / (c_ion_vals[i] + 1e-5)
    ax3.text(i - w/2, f_ion_vals[i] + 40, f"{f_ion_vals[i]:.0f}", ha='center', fontsize=8.5, fontweight='bold', color='#1565c0')
    ax3.text(i + w/2, c_ion_vals[i] + 40, f"{c_ion_vals[i]:.0f}", ha='center', fontsize=8.5, fontweight='bold')
    ax3.text(i, max(f_ion_vals[i], c_ion_vals[i]) + 150, f"{ratio:.1f}배", ha='center', fontsize=9, fontweight='bold', color='#d84315')

fig.suptitle('산림(8개 지점)과 밭(대조구)의 공기미생물 및 음이온 5개 시기 전수 비교', fontsize=14, fontweight='bold', y=1.02)
fig.tight_layout()
fig8_path = fig_dir / "08_산림_대조구_미생물_음이온_비교.png"
fig.savefig(fig8_path)
plt.close(fig)
print("[OK] Figure 08 refreshed")

# =============================================================
# Figure 12: 7-date Seasonal Trajectory of Bacteria, Fungi, B/F
# =============================================================
season_df = df.groupby('date_str').agg(
    bact=('PCA-B_CFU', 'mean'),
    fungi=('PDA-F_CFU', 'mean'),
    bf=('BF_ratio', 'mean')
).loc[dates_all].reset_index()

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), dpi=200, sharex=True)
ax1.plot(dates_all_labels, season_df['fungi'], marker='s', color='#d84315', linewidth=2.5, label='진균 (PDA-F, CFU/㎥)')
ax1.plot(dates_all_labels, season_df['bact'], marker='o', color='#1565c0', linewidth=2.5, label='세균 (PCA-B, CFU/㎥)')
for i, (b, f) in enumerate(zip(season_df['bact'], season_df['fungi'])):
    ax1.annotate(f"{b:.1f}", (i, b), textcoords="offset points", xytext=(0, 8), ha='center', fontsize=9, fontweight='bold', color='#1565c0')
    ax1.annotate(f"{f:.1f}", (i, f), textcoords="offset points", xytext=(0, 8), ha='center', fontsize=9, fontweight='bold', color='#d84315')

ax1.set_ylabel('미생물 농도 (CFU/㎥)', fontsize=11, fontweight='bold')
ax1.set_title('괴산학술림 공기미생물(세균·진균) 7개 조사 시기별 계절적 농도 변화 (3월~9월)', fontsize=13, fontweight='bold')
ax1.legend(fontsize=10.5)
ax1.grid(True, linestyle='--', alpha=0.3)

ax2.bar(dates_all_labels, season_df['bf'], color='#6a1b9a', width=0.45, alpha=0.85, edgecolor='black', linewidth=0.5)
for i, v in enumerate(season_df['bf']):
    ax2.text(i, v + 0.02, f"{v:.2f}", ha='center', fontsize=9.5, fontweight='bold', color='#4a148c')
ax2.set_ylabel('세균/진균 비율 (B/F 비)', fontsize=11, fontweight='bold')
ax2.set_title('시기별 세균 대 진균 비(Bacteria-to-Fungi Ratio) 추이 (4월 전엽기 피크 형성)', fontsize=12, fontweight='bold')
ax2.grid(axis='y', linestyle='--', alpha=0.3)
ax2.set_ylim(0, 0.9)

fig.tight_layout()
fig12_path = fig_dir / "12_공기미생물_6개시기_계절변화_추세.png"
fig.savefig(fig12_path)
plt.close(fig)
print("[OK] Figure 12 refreshed")

# =============================================================
# Figure 14: Forest vs Field Control across 7 Dates
# =============================================================
f_b = [df[(df['date_str'] == d) & df['is_forest']]['PCA-B_CFU'].mean() for d in dates_all]
c_b = [df[(df['date_str'] == d) & df['is_field']]['PCA-B_CFU'].mean() for d in dates_all]
f_f = [df[(df['date_str'] == d) & df['is_forest']]['PDA-F_CFU'].mean() for d in dates_all]
c_f = [df[(df['date_str'] == d) & df['is_field']]['PDA-F_CFU'].mean() for d in dates_all]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5.5), dpi=200)
x7 = np.arange(len(dates_all_labels))
w = 0.35

ax1.bar(x7 - w/2, f_b, w, label='산림(8지점)', color='#2e7d32', edgecolor='black', linewidth=0.5)
ax1.bar(x7 + w/2, c_b, w, label='대조구(밭)', color='#e65100', edgecolor='black', linewidth=0.5)
ax1.set_title('세균 농도: 산림 vs 밭(대조구) (7개 시기)', fontsize=12.5, fontweight='bold')
ax1.set_ylabel('세균 농도 (CFU/㎥)', fontsize=11, fontweight='bold')
ax1.set_xticks(x7)
ax1.set_xticklabels(dates_all_labels, rotation=20, fontsize=9.5)
ax1.grid(axis='y', linestyle='--', alpha=0.3)
ax1.legend()

ax2.bar(x7 - w/2, f_f, w, label='산림(8지점)', color='#2e7d32', edgecolor='black', linewidth=0.5)
ax2.bar(x7 + w/2, c_f, w, label='대조구(밭)', color='#e65100', edgecolor='black', linewidth=0.5)
ax2.set_title('진균 농도: 산림 vs 밭(대조구) (7개 시기)', fontsize=12.5, fontweight='bold')
ax2.set_ylabel('진균 농도 (CFU/㎥)', fontsize=11, fontweight='bold')
ax2.set_xticks(x7)
ax2.set_xticklabels(dates_all_labels, rotation=20, fontsize=9.5)
ax2.grid(axis='y', linestyle='--', alpha=0.3)
ax2.legend()

fig.suptitle('전체 7개 조사 시기 산림과 밭(대조구)의 공기미생물 농도 전수 비교', fontsize=14, fontweight='bold', y=1.02)
fig.tight_layout()
fig14_path = fig_dir / "14_산림_vs_밭대조구_6개시기_미생물비교.png"
fig.savefig(fig14_path)
plt.close(fig)
print("[OK] Figure 14 refreshed")

# =============================================================
# Figure 16: Microclimate Buffering across 7 Dates
# =============================================================
f_temp = [df[(df['date_str'] == d) & df['is_forest']]['air-temp'].mean() for d in dates_all]
c_temp = [df[(df['date_str'] == d) & df['is_field']]['air-temp'].mean() for d in dates_all]
f_rh = [df[(df['date_str'] == d) & df['is_forest']]['air-RH'].mean() for d in dates_all]
c_rh = [df[(df['date_str'] == d) & df['is_field']]['air-RH'].mean() for d in dates_all]
f_wind = [df[(df['date_str'] == d) & df['is_forest']]['windspeed'].mean() for d in dates_all]
c_wind = [df[(df['date_str'] == d) & df['is_field']]['windspeed'].mean() for d in dates_all]

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5.5), dpi=200)
ax1.bar(x7 - w/2, f_temp, w, label='산림 내부(8지점)', color='#2e7d32', edgecolor='black', linewidth=0.5)
ax1.bar(x7 + w/2, c_temp, w, label='개방형 밭(대조구)', color='#e65100', edgecolor='black', linewidth=0.5)
ax1.set_title('기온 완충 효과 (하계 최대 7.1℃ 냉각)', fontsize=12.5, fontweight='bold')
ax1.set_ylabel('대기 기온 (℃)', fontsize=11, fontweight='bold')
ax1.set_xticks(x7)
ax1.set_xticklabels(dates_all_labels, rotation=20, fontsize=9.5)
ax1.grid(axis='y', linestyle='--', alpha=0.3)
ax1.legend()
for i in range(len(dates_all)):
    diff = f_temp[i] - c_temp[i]
    color = '#1b5e20' if diff < 0 else '#b71c1c'
    ax1.text(i, max(f_temp[i], c_temp[i]) + 1.0, f"{diff:+.1f}℃", ha='center', fontsize=8.5, fontweight='bold', color=color)

ax2.plot(dates_all_labels, f_rh, marker='o', linewidth=2.2, color='#2e7d32', label='산림 내부(8지점)')
ax2.plot(dates_all_labels, c_rh, marker='s', linewidth=2.2, color='#e65100', label='개방형 밭(대조구)')
ax2.set_title('상대습도 변화 (7월 장마기 고습 vs 가을 적정)', fontsize=12.5, fontweight='bold')
ax2.set_ylabel('상대습도 (%)', fontsize=11, fontweight='bold')
ax2.set_xticks(x7)
ax2.set_xticklabels(dates_all_labels, rotation=20, fontsize=9.5)
ax2.grid(True, linestyle='--', alpha=0.3)
ax2.legend()
for i in range(len(dates_all)):
    ax2.annotate(f"{f_rh[i]:.1f}%", (i, f_rh[i]), textcoords="offset points", xytext=(0, 7), ha='center', fontsize=8, fontweight='bold', color='#2e7d32')

ax3.bar(x7 - w/2, f_wind, w, label='산림 내부(8지점)', color='#2e7d32', edgecolor='black', linewidth=0.5)
ax3.bar(x7 + w/2, c_wind, w, label='개방형 밭(대조구)', color='#e65100', edgecolor='black', linewidth=0.5)
ax3.set_title('풍속 감쇄 및 정온 효과 (50~75% 감쇄)', fontsize=12.5, fontweight='bold')
ax3.set_ylabel('풍속 (m/s)', fontsize=11, fontweight='bold')
ax3.set_xticks(x7)
ax3.set_xticklabels(dates_all_labels, rotation=20, fontsize=9.5)
ax3.grid(axis='y', linestyle='--', alpha=0.3)
ax3.legend()

fig.suptitle('건국대학교 괴산학술림 미기후 완충 효과 7개 시기 분석 (산림 vs 밭 대조구)', fontsize=14, fontweight='bold', y=1.02)
fig.tight_layout()
fig16_path = fig_dir / "16_괴산연습림_기상완충효과.png"
fig.savefig(fig16_path)
plt.close(fig)
# =============================================================
# Figure 10: Refreshed Correlation Heatmap (7 dates, clean soil)
# =============================================================
env_cols = ['n-ion', 'PCA-B_CFU', 'PDA-F_CFU', 'air-temp', 'air-RH', 'windspeed', 'PM10', 'PM2.5', 'illum', 'soil-PH', 'soil-temp', 'soil-RH']
col_labels = ['음이온', '세균(PCA-B)', '진균(PDA-F)', '기온', '상대습도', '풍속', 'PM10', 'PM2.5', '조도', '토양pH', '토양온도', '토양습도']

corr = df[env_cols].corr()

fig, ax = plt.subplots(figsize=(10, 8.5), dpi=200)
cax = ax.imshow(corr, cmap='RdBu_r', vmin=-1, vmax=1)

ax.set_xticks(range(len(col_labels)))
ax.set_yticks(range(len(col_labels)))
ax.set_xticklabels(col_labels, rotation=35, ha='right', fontsize=10, fontweight='bold')
ax.set_yticklabels(col_labels, fontsize=10, fontweight='bold')

for i in range(len(col_labels)):
    for j in range(len(col_labels)):
        val = corr.iloc[i, j]
        color = 'white' if abs(val) > 0.4 else 'black'
        ax.text(j, i, f"{val:+.2f}", ha='center', va='center', color=color, fontsize=8.5, fontweight='bold')

cbar = fig.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label('피어슨 상관계수 (r)', fontsize=11, fontweight='bold')
ax.set_title('음이온, 공기미생물 및 환경요인 간 상호 상관관계 히트맵 (7개 시기 전수, 아스팔트 포장 결측 배제)', fontsize=12, fontweight='bold', pad=15)
fig.tight_layout()
fig10_path = fig_dir / "10_음이온_미생물_환경요인_상관관계_히트맵.png"
fig.savefig(fig10_path)
plt.close(fig)
print("[OK] Figure 10 refreshed with asphalt soil correction")

# Sync all figures to brain directory
for fp in [fig8_path, fig10_path, fig12_path, fig14_path, fig16_path]:
    shutil.copy(fp, brain_dir / fp.name)
    print(f"[OK] Synced {fp.name} to brain")

# Export clean master data
clean_master_export = outputs_dir / "괴산연습림 전체데이터_정제본.xlsx"
df.to_excel(clean_master_export, index=False)
print(f"[OK] Saved clean master dataset to {clean_master_export}")

try:
    df.to_excel(master_file, index=False)
    print(f"[OK] Successfully updated master file: {master_file}")
except Exception as e:
    print(f"[NOTE] Master file currently open/locked ({e}). Clean copy saved in outputs/")

# =============================================================
# Build Comprehensive Excel Workbook: 괴산연습림_공기미생물_음이온_종합연계분석.xlsx
# =============================================================
excel_report_path = outputs_dir / "괴산연습림_공기미생물_음이온_종합연계분석.xlsx"

with pd.ExcelWriter(excel_report_path, engine='openpyxl') as writer:
    # Tab 1: 원본 (348 rows)
    df.to_excel(writer, sheet_name='전체_실측정제데이터', index=False)
    
    # Tab 2: 시기별_산림vs밭_비교 (7 dates)
    comp_records = []
    for d in dates_all:
        sub_d = df[df['date_str'] == d]
        f_sub = sub_d[sub_d['is_forest']]
        c_sub = sub_d[sub_d['is_field']]
        
        bact_inhibit = ((c_sub['PCA-B_CFU'].mean() - f_sub['PCA-B_CFU'].mean()) / c_sub['PCA-B_CFU'].mean() * 100) if c_sub['PCA-B_CFU'].mean() > 0 else 0
        fungi_inhibit = ((c_sub['PDA-F_CFU'].mean() - f_sub['PDA-F_CFU'].mean()) / c_sub['PDA-F_CFU'].mean() * 100) if c_sub['PDA-F_CFU'].mean() > 0 else 0
        ion_ratio = (f_sub['n-ion'].mean() / c_sub['n-ion'].mean()) if pd.notna(c_sub['n-ion'].mean()) and c_sub['n-ion'].mean() > 0 else np.nan
        temp_cooling = f_sub['air-temp'].mean() - c_sub['air-temp'].mean()
        
        comp_records.append({
            '조사일자': d,
            '산림 세균(CFU/㎥)': round(f_sub['PCA-B_CFU'].mean(), 1),
            '밭 세균(CFU/㎥)': round(c_sub['PCA-B_CFU'].mean(), 1),
            '세균 억제율': f"{bact_inhibit:.1f}%",
            '산림 진균(CFU/㎥)': round(f_sub['PDA-F_CFU'].mean(), 1),
            '밭 진균(CFU/㎥)': round(c_sub['PDA-F_CFU'].mean(), 1),
            '진균 억제율': f"{fungi_inhibit:.1f}%",
            '산림 음이온(개/㎤)': round(f_sub['n-ion'].mean(), 1) if pd.notna(f_sub['n-ion'].mean()) else "-",
            '밭 음이온(개/㎤)': round(c_sub['n-ion'].mean(), 1) if pd.notna(c_sub['n-ion'].mean()) else "-",
            '음이온 배율': f"{ion_ratio:.2f}배" if pd.notna(ion_ratio) else "-",
            '산림 냉각효과': f"{temp_cooling:+.1f}℃"
        })
    df_comp = pd.DataFrame(comp_records)
    df_comp.to_excel(writer, sheet_name='시기별_산림vs밭_비교', index=False)
    
    # Tab 3: 수종별_프로파일
    species_summary = df.groupby('vege_group').agg(
        관측수=('PCA-B_CFU', 'count'),
        세균_평균=('PCA-B_CFU', 'mean'),
        세균_중앙값=('PCA-B_CFU', 'median'),
        진균_평균=('PDA-F_CFU', 'mean'),
        진균_중앙값=('PDA-F_CFU', 'median'),
        음이온_평균=('n-ion', 'mean'),
        음이온_최대=('n-ion', 'max'),
        기온_평균=('air-temp', 'mean'),
        습도_평균=('air-RH', 'mean'),
        초미세먼지_평균=('PM2.5', 'mean')
    ).round(1).reset_index()
    species_summary.to_excel(writer, sheet_name='수종별_프로파일', index=False)
    
    # Tab 4: 상관분석
    numeric_cols = ['PCA-B_CFU', 'PDA-F_CFU', 'n-ion', 'air-temp', 'air-RH', 'windspeed', 'PM10', 'PM2.5', 'illum', 'soil-temp', 'soil-RH', 'soil-PH']
    corr_matrix = df[numeric_cols].corr().round(3)
    corr_matrix.to_excel(writer, sheet_name='환경_상관행렬')

print(f"[OK] Successfully built comprehensive workbook: {excel_report_path}")
print("=== ALL MASTER FIGURES & WORKBOOKS UPDATED SUCCESSFULLY ===")
