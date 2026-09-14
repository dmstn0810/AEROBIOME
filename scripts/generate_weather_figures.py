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
df['is_forest'] = df['site no.'].isin([1, 2, 3, 6, 7, 8, 9, 10])
df['is_field'] = df['site no.'] == 4

dates_labels = ['03-04 (초봄)', '04-15 (봄1)', '04-29 (봄2)', '05-13 (만춘)', '07-27 (여름1)', '08-13 (여름2)']
dates = sorted(df['date'].unique())

f_temp = [df[(df['date'] == d) & df['is_forest']]['air-temp'].mean() for d in dates]
c_temp = [df[(df['date'] == d) & df['is_field']]['air-temp'].mean() for d in dates]
f_rh = [df[(df['date'] == d) & df['is_forest']]['air-RH'].mean() for d in dates]
c_rh = [df[(df['date'] == d) & df['is_field']]['air-RH'].mean() for d in dates]
f_wind = [df[(df['date'] == d) & df['is_forest']]['windspeed'].mean() for d in dates]
c_wind = [df[(df['date'] == d) & df['is_field']]['windspeed'].mean() for d in dates]

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5.5), dpi=200)
x = np.arange(len(dates_labels))
w = 0.35

# 1. Temperature Buffering
ax1.bar(x - w/2, f_temp, w, label='산림 내부(8지점)', color='#2e7d32', edgecolor='black', linewidth=0.5)
ax1.bar(x + w/2, c_temp, w, label='개방형 밭(대조구)', color='#e65100', edgecolor='black', linewidth=0.5)
ax1.set_title('기온 완충 효과 (여름철 최대 7.1℃ 냉각)', fontsize=12.5, fontweight='bold')
ax1.set_ylabel('대기 기온 (℃)', fontsize=11, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(dates_labels, rotation=20, fontsize=9.5)
ax1.grid(axis='y', linestyle='--', alpha=0.3)
ax1.legend()
for i in range(len(dates)):
    diff = f_temp[i] - c_temp[i]
    color = '#1b5e20' if diff < 0 else '#b71c1c'
    ax1.text(i, max(f_temp[i], c_temp[i]) + 1.2, f"{diff:+.1f}℃", ha='center', fontsize=9, fontweight='bold', color=color)

# 2. Relative Humidity
ax2.plot(dates_labels, f_rh, marker='o', linewidth=2.2, color='#2e7d32', label='산림 내부(8지점)')
ax2.plot(dates_labels, c_rh, marker='s', linewidth=2.2, color='#e65100', label='개방형 밭(대조구)')
ax2.set_title('상대습도 변화 (7월 장마기 습도 78~91%)', fontsize=12.5, fontweight='bold')
ax2.set_ylabel('상대습도 (%)', fontsize=11, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(dates_labels, rotation=20, fontsize=9.5)
ax2.grid(True, linestyle='--', alpha=0.3)
ax2.legend()
for i in range(len(dates)):
    ax2.annotate(f"{f_rh[i]:.1f}%", (i, f_rh[i]), textcoords="offset points", xytext=(0, 7), ha='center', fontsize=8.5, fontweight='bold', color='#2e7d32')

# 3. Windspeed Attenuation
ax3.bar(x - w/2, f_wind, w, label='산림 내부(8지점)', color='#2e7d32', edgecolor='black', linewidth=0.5)
ax3.bar(x + w/2, c_wind, w, label='개방형 밭(대조구)', color='#e65100', edgecolor='black', linewidth=0.5)
ax3.set_title('풍속 감쇄 및 정온 효과 (50~70% 풍속 감쇄)', fontsize=12.5, fontweight='bold')
ax3.set_ylabel('풍속 (m/s)', fontsize=11, fontweight='bold')
ax3.set_xticks(x)
ax3.set_xticklabels(dates_labels, rotation=20, fontsize=9.5)
ax3.grid(axis='y', linestyle='--', alpha=0.3)
ax3.legend()
for i in range(len(dates)):
    ax3.text(i - w/2, f_wind[i] + 0.05, f"{f_wind[i]:.2f}", ha='center', fontsize=8.5, fontweight='bold')
    ax3.text(i + w/2, c_wind[i] + 0.05, f"{c_wind[i]:.2f}", ha='center', fontsize=8.5, fontweight='bold', color='#e65100')

fig.suptitle('건국대학교 괴산학술림 미기후 완충 효과 분석 (산림 vs 개방형 밭 대조구)', fontsize=14, fontweight='bold', y=1.02)
fig.tight_layout()
fig.savefig(fig_dir / "16_괴산연습림_기상완충효과.png")
plt.close(fig)
print("Saved 16_괴산연습림_기상완충효과.png")
