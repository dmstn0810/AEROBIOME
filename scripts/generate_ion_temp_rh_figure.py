import sys
import io
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

master_path = Path(r"C:\Users\USER\orca\projects\AEROBIOME\outputs\괴산연습림 전체데이터_정제본.xlsx")
df = pd.read_excel(master_path).dropna(subset=['n-ion (개/cm3)']).copy()

# Site ordering by mean ion
sites_order = [
    (8, '버드나무림 b'), (6, '소나무림'), (7, '일본잎갈나무림 a'), (3, '버드나무림 a'),
    (5, '주차장(대조구)'), (1, '리기다소나무림'), (10, '잣나무림 b'), (9, '일본잎갈나무림 b'),
    (2, '잣나무림 a'), (4, '밭(대조구)')
]
site_names = [s[1] for s in sites_order]
site_ids = [s[0] for s in sites_order]

# Aggregate stats
site_stats = df.groupby('site no.').agg(
    ion_mean=('n-ion (개/cm3)', 'mean'),
    ion_std=('n-ion (개/cm3)', 'std'),
    temp_mean=('air-temp', 'mean'),
    temp_std=('air-temp', 'std'),
    rh_mean=('air-RH', 'mean'),
    rh_std=('air-RH', 'std')
).reindex(site_ids)

fig, axes = plt.subplots(2, 2, figsize=(16, 12), dpi=200)

# Colors: Forest (Green/Blue), Controls (Red/Brown)
bar_colors = ['#2e7d32', '#1565c0', '#00838f', '#2e7d32', '#d84315', '#1565c0', '#5e35b1', '#00838f', '#5e35b1', '#c62828']

# 1. Ion bar chart
ax1 = axes[0, 0]
x = np.arange(len(site_names))
bars1 = ax1.bar(x, site_stats['ion_mean'], yerr=site_stats['ion_std'], capsize=4, color=bar_colors, edgecolor='black', alpha=0.85, linewidth=0.7)
ax1.set_xticks(x)
ax1.set_xticklabels(site_names, rotation=35, ha='right', fontsize=10, fontweight='bold')
ax1.set_ylabel('음이온 발생량 (개/㎤)', fontsize=11, fontweight='bold')
ax1.set_title('(A) 10개 지점별 평균 음이온 발생량 (평균 내림차순)', fontsize=13, fontweight='bold')
ax1.grid(axis='y', linestyle='--', alpha=0.4)
for i, v in enumerate(site_stats['ion_mean']):
    ax1.text(i, v + site_stats['ion_std'].iloc[i] + 40, f"{v:.0f}", ha='center', fontsize=9, fontweight='bold')

# 2. Temperature and Humidity by Site
ax2 = axes[0, 1]
w = 0.38
b_temp = ax2.bar(x - w/2, site_stats['temp_mean'], w, label='대기온도 (℃)', color='#e65100', alpha=0.85, edgecolor='black', linewidth=0.7)
ax2_rh = ax2.twinx()
b_rh = ax2_rh.bar(x + w/2, site_stats['rh_mean'], w, label='대기습도 (%)', color='#0277bd', alpha=0.85, edgecolor='black', linewidth=0.7)

ax2.set_xticks(x)
ax2.set_xticklabels(site_names, rotation=35, ha='right', fontsize=10, fontweight='bold')
ax2.set_ylabel('대기온도 (℃)', fontsize=11, fontweight='bold', color='#e65100')
ax2_rh.set_ylabel('대기상대습도 (%)', fontsize=11, fontweight='bold', color='#0277bd')
ax2.set_title('(B) 10개 지점별 평균 대기온도 및 상대습도 (산림 냉각·가습)', fontsize=13, fontweight='bold')
ax2.set_ylim(15, 30)
ax2_rh.set_ylim(35, 70)
ax2.grid(axis='y', linestyle='--', alpha=0.3)

for i, t in enumerate(site_stats['temp_mean']):
    ax2.text(i - w/2, t + 0.3, f"{t:.1f}℃", ha='center', fontsize=8, fontweight='bold', color='#bf360c')
for i, h in enumerate(site_stats['rh_mean']):
    ax2_rh.text(i + w/2, h + 0.7, f"{h:.1f}%", ha='center', fontsize=8, fontweight='bold', color='#01579b')

# 3. Scatter: Ion vs Temperature
ax3 = axes[1, 0]
for s_id, s_name in sites_order:
    sub = df[df['site no.'] == s_id]
    c = '#c62828' if s_id in [4, 5] else '#2e7d32'
    m = 's' if s_id in [4, 5] else 'o'
    ax3.scatter(sub['air-temp'], sub['n-ion (개/cm3)'], label=s_name if s_id in [4, 6, 8, 2] else None,
                alpha=0.75, s=45, edgecolor='black', linewidth=0.5)

ax3.set_xlabel('대기온도 (℃)', fontsize=11, fontweight='bold')
ax3.set_ylabel('음이온 발생량 (개/㎤)', fontsize=11, fontweight='bold')
ax3.set_title('(C) 대기온도에 따른 음이온 발생량 분포 (24~26℃ 최적 방출)', fontsize=13, fontweight='bold')
ax3.grid(True, linestyle='--', alpha=0.4)
ax3.legend(fontsize=9, loc='upper left')

# 4. Scatter: Ion vs Humidity
ax4 = axes[1, 1]
for s_id, s_name in sites_order:
    sub = df[df['site no.'] == s_id]
    ax4.scatter(sub['air-RH'], sub['n-ion (개/cm3)'], label=s_name if s_id in [4, 6, 8, 2] else None,
                alpha=0.75, s=45, edgecolor='black', linewidth=0.5)

ax4.set_xlabel('대기상대습도 (%)', fontsize=11, fontweight='bold')
ax4.set_ylabel('음이온 발생량 (개/㎤)', fontsize=11, fontweight='bold')
ax4.set_title('(D) 대기습도에 따른 음이온 발생량 분포 (55~70% 고습 환경 우세)', fontsize=13, fontweight='bold')
ax4.grid(True, linestyle='--', alpha=0.4)
ax4.legend(fontsize=9, loc='upper left')

fig.suptitle('괴산학술림 10개 지점별 공기 음이온, 대기온도, 상대습도 통합 비교 프로파일', fontsize=16, fontweight='bold', y=0.99)
fig.tight_layout(rect=[0, 0.03, 1, 0.96])

fig_path1 = Path("figures/지점별_음이온_온도_습도_종합프로파일.png")
fig_path2 = Path("docs/images/지점별_음이온_온도_습도_종합프로파일.png")
fig_path3 = Path(r"C:\Users\USER\.gemini\antigravity-cli\brain\e9af4cf4-b0e4-44fe-9176-0e5cb78066c4\지점별_음이온_온도_습도_종합프로파일.png")

fig.savefig(fig_path1)
fig.savefig(fig_path2)
fig.savefig(fig_path3)
plt.close(fig)
print("[OK] Generated and saved 지점별_음이온_온도_습도_종합프로파일.png")
