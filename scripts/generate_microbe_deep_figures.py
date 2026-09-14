import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding='utf-8')

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

fig_dir = Path("figures")
fig_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_excel("괴산연습림 전체데이터.xlsx", sheet_name="원본")
df['PCA-B_CFU'] = df['PCA-B (CFU/m3)']
df['PDA-F_CFU'] = df['PDA-F (CFU/m3)']
df['is_forest'] = df['site no.'].isin([1, 2, 3, 6, 7, 8, 9, 10])
df['is_field'] = df['site no.'] == 4
df['forest_type'] = df['vege'].map({
    "리기다소나무림": "침엽수림", "소나무림": "침엽수림", "잣나무림 a": "침엽수림", "잣나무림 b": "침엽수림", "일본잎갈나무림 a": "침엽수림", "일본잎갈나무림 b": "침엽수림",
    "버드나무림 a": "활엽수림", "버드나무림 b": "활엽수림",
    "밭(대조구)": "농경지(대조구)", "주차장(대조구)": "인공포장지(참고)"
})
df['BF_ratio'] = df['PCA-B_CFU'] / (df['PDA-F_CFU'] + 1e-5)

dates_str = [str(d)[:10] for d in sorted(df['date'].unique())]
dates_labels = ['03-04 (초봄)', '04-15 (봄1)', '04-29 (봄2)', '05-13 (만춘)', '07-27 (여름1)', '08-13 (여름2)']

# -------------------------------------------------------------
# Figure 12: 6-date Seasonal Trajectory of Bacteria, Fungi, B/F
# -------------------------------------------------------------
season_df = df.groupby('date').agg(
    bact=('PCA-B_CFU', 'mean'),
    fungi=('PDA-F_CFU', 'mean'),
    bf=('BF_ratio', 'mean')
).reset_index()

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), dpi=200, sharex=True)

# Top: Concentrations
ax1.plot(dates_labels, season_df['fungi'], marker='s', color='#d84315', linewidth=2.5, label='진균 (PDA-F, CFU/㎥)')
ax1.plot(dates_labels, season_df['bact'], marker='o', color='#1565c0', linewidth=2.5, label='세균 (PCA-B, CFU/㎥)')
for i, (b, f) in enumerate(zip(season_df['bact'], season_df['fungi'])):
    ax1.annotate(f"{b:.1f}", (i, b), textcoords="offset points", xytext=(0, 8), ha='center', fontsize=9, fontweight='bold', color='#1565c0')
    ax1.annotate(f"{f:.1f}", (i, f), textcoords="offset points", xytext=(0, 8), ha='center', fontsize=9, fontweight='bold', color='#d84315')

ax1.set_ylabel('미생물 농도 (CFU/㎥)', fontsize=11, fontweight='bold')
ax1.set_title('괴산연습림 공기미생물(세균·진균) 6개 조사 시기별 계절적 농도 변화', fontsize=13, fontweight='bold')
ax1.legend(fontsize=10.5)
ax1.grid(True, linestyle='--', alpha=0.3)

# Bottom: B/F Ratio
ax2.bar(dates_labels, season_df['bf'], color='#6a1b9a', width=0.45, alpha=0.85, edgecolor='black', linewidth=0.5)
for i, v in enumerate(season_df['bf']):
    ax2.text(i, v + 0.02, f"{v:.2f}", ha='center', fontsize=9.5, fontweight='bold', color='#4a148c')
ax2.set_ylabel('세균/진균 비율 (B/F 비)', fontsize=11, fontweight='bold')
ax2.set_title('시기별 세균 대 진균 비(Bacteria-to-Fungi Ratio) 추이 (04월 피크 형성)', fontsize=12, fontweight='bold')
ax2.grid(axis='y', linestyle='--', alpha=0.3)
ax2.set_ylim(0, 1.0)

fig.tight_layout()
fig.savefig(fig_dir / "12_공기미생물_6개시기_계절변화_추세.png")
plt.close(fig)
print("Saved 12_공기미생물_6개시기_계절변화_추세.png")

# -------------------------------------------------------------
# Figure 13: Forest Type Comparison Violin / Boxplot
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=200)

types_order = ["침엽수림", "활엽수림", "농경지(대조구)", "인공포장지(참고)"]
bact_by_type = [df[df['forest_type'] == ft]['PCA-B_CFU'].dropna().values for ft in types_order]
fungi_by_type = [df[df['forest_type'] == ft]['PDA-F_CFU'].dropna().values for ft in types_order]

# Left: Bacteria
bp1 = ax1.boxplot(bact_by_type, patch_artist=True, widths=0.5,
                  boxprops=dict(facecolor='#bbdefb', color='#0d47a1', linewidth=1.2),
                  medianprops=dict(color='#b71c1c', linewidth=2),
                  flierprops=dict(marker='o', markersize=3, alpha=0.4))
ax1.set_xticks(range(1, len(types_order) + 1))
ax1.set_xticklabels(types_order, fontsize=10.5, fontweight='bold')
ax1.set_ylabel('세균 농도 (CFU/㎥, 로그스케일)', fontsize=11, fontweight='bold')
ax1.set_yscale('log')
ax1.set_title('임상/식생 유형별 세균(PCA-B) 농도 분포', fontsize=12.5, fontweight='bold')
ax1.grid(axis='y', linestyle='--', alpha=0.3)

# Right: Fungi
bp2 = ax2.boxplot(fungi_by_type, patch_artist=True, widths=0.5,
                  boxprops=dict(facecolor='#ffccbc', color='#bf360c', linewidth=1.2),
                  medianprops=dict(color='#b71c1c', linewidth=2),
                  flierprops=dict(marker='o', markersize=3, alpha=0.4))
ax2.set_xticks(range(1, len(types_order) + 1))
ax2.set_xticklabels(types_order, fontsize=10.5, fontweight='bold')
ax2.set_ylabel('진균 농도 (CFU/㎥)', fontsize=11, fontweight='bold')
ax2.set_title('임상/식생 유형별 진균(PDA-F) 농도 분포', fontsize=12.5, fontweight='bold')
ax2.grid(axis='y', linestyle='--', alpha=0.3)

# Highlight control
bp1['boxes'][2].set_facecolor('#ffe082')
bp2['boxes'][2].set_facecolor('#ffe082')

fig.suptitle('산림 임상(침엽수·활엽수)과 대조구(농경지·인공포장지) 미생물 농도 비교 (노란색: 밭 대조구)', fontsize=14, fontweight='bold', y=1.02)
fig.tight_layout()
fig.savefig(fig_dir / "13_임상별_세균_진균_분포_박스플롯.png")
plt.close(fig)
print("Saved 13_임상별_세균_진균_분포_박스플롯.png")

# -------------------------------------------------------------
# Figure 14: Forest vs Field Control across 6 Dates
# -------------------------------------------------------------
f_b = [df[(df['date'] == d) & df['is_forest']]['PCA-B_CFU'].mean() for d in sorted(df['date'].unique())]
c_b = [df[(df['date'] == d) & df['is_field']]['PCA-B_CFU'].mean() for d in sorted(df['date'].unique())]
f_f = [df[(df['date'] == d) & df['is_forest']]['PDA-F_CFU'].mean() for d in sorted(df['date'].unique())]
c_f = [df[(df['date'] == d) & df['is_field']]['PDA-F_CFU'].mean() for d in sorted(df['date'].unique())]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5.5), dpi=200)
x = np.arange(len(dates_labels))
w = 0.35

# Bacteria
ax1.bar(x - w/2, f_b, w, label='산림(8지점)', color='#2e7d32', edgecolor='black', linewidth=0.5)
ax1.bar(x + w/2, c_b, w, label='대조구(밭)', color='#e65100', edgecolor='black', linewidth=0.5)
ax1.set_title('세균 농도: 산림 vs 밭(대조구) (6개 시기)', fontsize=12.5, fontweight='bold')
ax1.set_ylabel('세균 농도 (CFU/㎥)', fontsize=11, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(dates_labels, rotation=20, fontsize=9.5)
ax1.grid(axis='y', linestyle='--', alpha=0.3)
ax1.legend()

# Fungi
ax2.bar(x - w/2, f_f, w, label='산림(8지점)', color='#2e7d32', edgecolor='black', linewidth=0.5)
ax2.bar(x + w/2, c_f, w, label='대조구(밭)', color='#e65100', edgecolor='black', linewidth=0.5)
ax2.set_title('진균 농도: 산림 vs 밭(대조구) (6개 시기)', fontsize=12.5, fontweight='bold')
ax2.set_ylabel('진균 농도 (CFU/㎥)', fontsize=11, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(dates_labels, rotation=20, fontsize=9.5)
ax2.grid(axis='y', linestyle='--', alpha=0.3)
ax2.legend()

fig.suptitle('전체 6개 조사 시기 산림과 밭(대조구)의 공기미생물 농도 전수 비교', fontsize=14, fontweight='bold', y=1.02)
fig.tight_layout()
fig.savefig(fig_dir / "14_산림_vs_밭대조구_6개시기_미생물비교.png")
plt.close(fig)
print("Saved 14_산림_vs_밭대조구_6개시기_미생물비교.png")

# -------------------------------------------------------------
# Figure 15: Benchmarking with Literature & Regulatory Standards
# -------------------------------------------------------------
bench_labels = [
    '괴산 활엽수림(버드나무)', '괴산 잣나무림', '괴산 소나무림', '괴산 밭(대조구)',
    '선행연구 산림(NIFOS)', '선행연구 농경지/전원', '환경부 실내유지기준'
]
bench_bact = [24.8, 36.9, 137.9, 200.7, 180.0, 650.0, 800.0]
bench_colors = ['#1b5e20', '#2e7d32', '#43a047', '#e65100', '#0277bd', '#f57c00', '#c2185b']

fig, ax = plt.subplots(figsize=(12, 6), dpi=200)
y_pos = np.arange(len(bench_labels))
bars = ax.barh(y_pos, bench_bact, color=bench_colors, height=0.55, edgecolor='black', linewidth=0.5)
ax.axvline(800.0, color='#c2185b', linestyle='--', linewidth=1.5, label='환경부 다중이용시설 기준 (800 CFU/㎥)')

for bar, val in zip(bars, bench_bact):
    ax.text(val + 15, bar.get_y() + bar.get_height()/2, f"{val:.1f} CFU/㎥", va='center', fontsize=9.5, fontweight='bold')

ax.set_yticks(y_pos)
ax.set_yticklabels(bench_labels, fontsize=10.5, fontweight='bold')
ax.set_xlabel('총부유세균 농도 (CFU/㎥)', fontsize=11, fontweight='bold')
ax.set_title('선행연구 및 공기질 관리기준 대비 괴산연습림 공기 중 세균 농도 벤치마크', fontsize=13, fontweight='bold', pad=12)
ax.grid(axis='x', linestyle='--', alpha=0.3)
ax.legend(loc='lower right', fontsize=10)
fig.tight_layout()
fig.savefig(fig_dir / "15_선행연구_비교_벤치마크_차트.png")
plt.close(fig)
print("Saved 15_선행연구_비교_벤치마크_차트.png")

print("All 4 deep microbe figures generated successfully!")
