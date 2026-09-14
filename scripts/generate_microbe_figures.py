import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(str(Path.cwd()))

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

fig_dir = Path("figures")
fig_dir.mkdir(parents=True, exist_ok=True)

from scripts.process_microbe_dataset import df

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
df['is_control_field'] = df['site no.'] == 4

ion_dates = ['2026-04-15', '2026-04-29', '2026-07-27', '2026-08-13']
df_ion = df[df['date'].astype(str).str[:10].isin(ion_dates)].copy()

# -------------------------------------------------------------
# Figure 8: Forest vs Field Control (밭) Comparison across 3 Metrics
# -------------------------------------------------------------
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5.5), dpi=200)

dates_label = ['04-15 (봄1)', '04-29 (봄2)', '07-27 (여름1)', '08-13 (여름2)']
x = np.arange(len(ion_dates))
w = 0.35

# Panel 1: Bacteria (PCA-B CFU/m^3)
f_bact = [df_ion[(df_ion['date'].astype(str).str.contains(d)) & df_ion['is_forest']]['PCA-B_CFU'].mean() for d in ion_dates]
c_bact = [df_ion[(df_ion['date'].astype(str).str.contains(d)) & df_ion['is_control_field']]['PCA-B_CFU'].mean() for d in ion_dates]

ax1.bar(x - w/2, f_bact, w, label='산림(8지점)', color='#2e7d32', edgecolor='black', linewidth=0.5)
ax1.bar(x + w/2, c_bact, w, label='대조구(밭)', color='#d84315', edgecolor='black', linewidth=0.5)
ax1.set_title('공기 중 세균 농도 (PCA-B)', fontsize=13, fontweight='bold')
ax1.set_ylabel('세균 농도 (CFU/㎥)', fontsize=11, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(dates_label, fontsize=10)
ax1.grid(axis='y', linestyle='--', alpha=0.4)
ax1.legend()
for i in range(len(ion_dates)):
    ax1.text(i - w/2, f_bact[i] + 10, f"{f_bact[i]:.0f}", ha='center', fontsize=9, fontweight='bold')
    ax1.text(i + w/2, c_bact[i] + 10, f"{c_bact[i]:.0f}", ha='center', fontsize=9, fontweight='bold', color='#d84315')

# Panel 2: Fungi (PDA-F CFU/m^3)
f_fungi = [df_ion[(df_ion['date'].astype(str).str.contains(d)) & df_ion['is_forest']]['PDA-F_CFU'].mean() for d in ion_dates]
c_fungi = [df_ion[(df_ion['date'].astype(str).str.contains(d)) & df_ion['is_control_field']]['PDA-F_CFU'].mean() for d in ion_dates]

ax2.bar(x - w/2, f_fungi, w, label='산림(8지점)', color='#2e7d32', edgecolor='black', linewidth=0.5)
ax2.bar(x + w/2, c_fungi, w, label='대조구(밭)', color='#d84315', edgecolor='black', linewidth=0.5)
ax2.set_title('공기 중 진균 농도 (PDA-F)', fontsize=13, fontweight='bold')
ax2.set_ylabel('진균 농도 (CFU/㎥)', fontsize=11, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(dates_label, fontsize=10)
ax2.grid(axis='y', linestyle='--', alpha=0.4)
ax2.legend()
for i in range(len(ion_dates)):
    ax2.text(i - w/2, f_fungi[i] + 40, f"{f_fungi[i]:.0f}", ha='center', fontsize=9, fontweight='bold')
    ax2.text(i + w/2, c_fungi[i] + 40, f"{c_fungi[i]:.0f}", ha='center', fontsize=9, fontweight='bold', color='#d84315')

# Panel 3: Negative Ions (n-ion 개/cm^3)
f_ion = [df_ion[(df_ion['date'].astype(str).str.contains(d)) & df_ion['is_forest']]['n-ion'].mean() for d in ion_dates]
c_ion = [df_ion[(df_ion['date'].astype(str).str.contains(d)) & df_ion['is_control_field']]['n-ion'].mean() for d in ion_dates]

ax3.bar(x - w/2, f_ion, w, label='산림(8지점)', color='#2e7d32', edgecolor='black', linewidth=0.5)
ax3.bar(x + w/2, c_ion, w, label='대조구(밭)', color='#d84315', edgecolor='black', linewidth=0.5)
ax3.set_title('음이온 발생량 (n-ion)', fontsize=13, fontweight='bold')
ax3.set_ylabel('음이온 농도 (개/㎤)', fontsize=11, fontweight='bold')
ax3.set_xticks(x)
ax3.set_xticklabels(dates_label, fontsize=10)
ax3.grid(axis='y', linestyle='--', alpha=0.4)
ax3.legend()
for i in range(len(ion_dates)):
    ax3.text(i - w/2, f_ion[i] + 50, f"{f_ion[i]:.0f}", ha='center', fontsize=9, fontweight='bold')
    ax3.text(i + w/2, c_ion[i] + 50, f"{c_ion[i]:.0f}", ha='center', fontsize=9, fontweight='bold', color='#d84315')

fig.suptitle('산림 vs 밭(대조구) 공기미생물(세균·진균) 및 음이온 농도 비교 (대조구: 밭 기준)', fontsize=15, fontweight='bold', y=1.02)
fig.tight_layout()
fig.savefig(fig_dir / "08_산림_대조구_미생물_음이온_비교.png")
plt.close(fig)
print("Saved 08_산림_대조구_미생물_음이온_비교.png")

# -------------------------------------------------------------
# Figure 9: Species Profile (Bacteria, Fungi, Ions)
# -------------------------------------------------------------
sp_order = ["버드나무류", "소나무류", "잣나무류", "낙엽송(일본잎갈나무)", "대조구(밭)"]
sp_stats = df_ion[df_ion['species_group'].isin(sp_order)].groupby('species_group').agg(
    bact=('PCA-B_CFU', 'mean'),
    fungi=('PDA-F_CFU', 'mean'),
    ion=('n-ion', 'mean')
).reindex(sp_order)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), dpi=200)

# Left: Microbes
y_pos = np.arange(len(sp_order))
h = 0.35
ax1.barh(y_pos - h/2, sp_stats['bact'], h, label='세균 (PCA-B)', color='#1976d2', edgecolor='black', linewidth=0.5)
ax1.barh(y_pos + h/2, sp_stats['fungi'], h, label='진균 (PDA-F)', color='#e64a19', edgecolor='black', linewidth=0.5)
ax1.set_yticks(y_pos)
ax1.set_yticklabels(sp_order, fontsize=11, fontweight='bold')
ax1.set_xlabel('공기미생물 농도 (CFU/㎥)', fontsize=11, fontweight='bold')
ax1.set_title('수종별 공기미생물(세균·진균) 평균 농도', fontsize=13, fontweight='bold')
ax1.legend()
ax1.grid(axis='x', linestyle='--', alpha=0.4)

# Right: Ions
ax2.barh(y_pos, sp_stats['ion'], 0.6, color='#388e3c', edgecolor='black', linewidth=0.5)
ax2.set_yticks(y_pos)
ax2.set_yticklabels(sp_order, fontsize=11, fontweight='bold')
ax2.set_xlabel('평균 음이온 발생량 (개/㎤)', fontsize=11, fontweight='bold')
ax2.set_title('수종별 평균 음이온 발생량', fontsize=13, fontweight='bold')
ax2.grid(axis='x', linestyle='--', alpha=0.4)
for i, val in enumerate(sp_stats['ion']):
    ax2.text(val + 30, i, f"{val:.0f}개/㎤", va='center', fontsize=10, fontweight='bold')

fig.suptitle('수종별 공기미생물 부유 농도 및 음이온 방출 특성 프로파일', fontsize=15, fontweight='bold', y=1.02)
fig.tight_layout()
fig.savefig(fig_dir / "09_수종별_미생물농도_및_음이온_프로파일.png")
plt.close(fig)
print("Saved 09_수종별_미생물농도_및_음이온_프로파일.png")

# -------------------------------------------------------------
# Figure 10: Environmental & Microbe Correlation Heatmap
# -------------------------------------------------------------
env_cols = ['n-ion', 'PCA-B_CFU', 'PDA-F_CFU', 'air-temp', 'air-RH', 'windspeed', 'PM10', 'PM2.5', 'illum', 'soil-PH', 'soil-temp', 'soil-RH']
col_labels = ['음이온', '세균(PCA-B)', '진균(PDA-F)', '기온', '상대습도', '풍속', 'PM10', 'PM2.5', '조도', '토양pH', '토양온도', '토양습도']

corr = df_ion[env_cols].corr()

fig, ax = plt.subplots(figsize=(10, 8.5), dpi=200)
cax = ax.imshow(corr, cmap='RdBu_r', vmin=-1, vmax=1)

ax.set_xticks(range(len(col_labels)))
ax.set_yticks(range(len(col_labels)))
ax.set_xticklabels(col_labels, rotation=35, ha='right', fontsize=10, fontweight='bold')
ax.set_yticklabels(col_labels, fontsize=10, fontweight='bold')

# Annotate values
for i in range(len(col_labels)):
    for j in range(len(col_labels)):
        val = corr.iloc[i, j]
        color = 'white' if abs(val) > 0.4 else 'black'
        ax.text(j, i, f"{val:+.2f}", ha='center', va='center', color=color, fontsize=8.5, fontweight='bold')

cbar = fig.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label('피어슨 상관계수 (r)', fontsize=11, fontweight='bold')
ax.set_title('음이온, 공기미생물 및 환경요인 간 상호 상관관계 히트맵', fontsize=14, fontweight='bold', pad=15)
fig.tight_layout()
fig.savefig(fig_dir / "10_음이온_미생물_환경요인_상관관계_히트맵.png")
plt.close(fig)
print("Saved 10_음이온_미생물_환경요인_상관관계_히트맵.png")

# -------------------------------------------------------------
# Figure 11: Microbe vs Ion Scatter & Negative Association in Summer
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=200)

aug_data = df_ion[df_ion['date'].astype(str).str.contains('2026-08-13')]
other_data = df_ion[~df_ion['date'].astype(str).str.contains('2026-08-13')]

# Left: Bacteria vs Ion
ax1.scatter(other_data['n-ion'], other_data['PCA-B_CFU'], color='#90caf9', alpha=0.7, label='봄철/여름초기(4·7월)', s=40)
ax1.scatter(aug_data['n-ion'], aug_data['PCA-B_CFU'], color='#c2185b', alpha=0.85, label='여름성기(8월 13일)', s=60, edgecolors='black')
# Trendline for August
z = np.polyfit(aug_data['n-ion'], aug_data['PCA-B_CFU'], 1)
p = np.poly1d(z)
x_line = np.linspace(aug_data['n-ion'].min(), aug_data['n-ion'].max(), 50)
ax1.plot(x_line, p(x_line), color='#c2185b', linestyle='--', linewidth=2, label=f'8월 회귀선 (r = -0.28)')

ax1.set_xlabel('음이온 발생량 (개/㎤)', fontsize=11, fontweight='bold')
ax1.set_ylabel('세균 농도 (PCA-B, CFU/㎥)', fontsize=11, fontweight='bold')
ax1.set_title('음이온 vs 세균(PCA-B) 농도 관계', fontsize=13, fontweight='bold')
ax1.grid(True, linestyle='--', alpha=0.3)
ax1.legend(fontsize=9.5)

# Right: Fungi vs Ion
ax2.scatter(other_data['n-ion'], other_data['PDA-F_CFU'], color='#a5d6a7', alpha=0.7, label='봄철/여름초기(4·7월)', s=40)
ax2.scatter(aug_data['n-ion'], aug_data['PDA-F_CFU'], color='#2e7d32', alpha=0.85, label='여름성기(8월 13일)', s=60, edgecolors='black')
z2 = np.polyfit(aug_data['n-ion'], aug_data['PDA-F_CFU'], 1)
p2 = np.poly1d(z2)
ax2.plot(x_line, p2(x_line), color='#2e7d32', linestyle='--', linewidth=2, label=f'8월 회귀선 (r = -0.19)')

ax2.set_xlabel('음이온 발생량 (개/㎤)', fontsize=11, fontweight='bold')
ax2.set_ylabel('진균 농도 (PDA-F, CFU/㎥)', fontsize=11, fontweight='bold')
ax2.set_title('음이온 vs 진균(PDA-F) 농도 관계', fontsize=13, fontweight='bold')
ax2.grid(True, linestyle='--', alpha=0.3)
ax2.legend(fontsize=9.5)

fig.suptitle('음이온 발생량과 공기미생물 부유 농도 간의 산점도 및 여름철 역상관 추세', fontsize=14, fontweight='bold', y=1.02)
fig.tight_layout()
fig.savefig(fig_dir / "11_음이온_미생물_산점도_및_회귀선.png")
plt.close(fig)
print("Saved 11_음이온_미생물_산점도_및_회귀선.png")

print("All microbe linkage figures successfully created!")
