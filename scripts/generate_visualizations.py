import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.dates as mdates

sys.stdout.reconfigure(encoding='utf-8')

# Configure fonts
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

fig_dir = Path("figures")
fig_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv("data/ion_dataset_all.csv")
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['hour_float'] = df['timestamp'].dt.hour + df['timestamp'].dt.minute / 60.0 + df['timestamp'].dt.second / 3600.0

valid_df = df[df['is_valid']].copy()

species_map = {
    "리기다소나무림": "소나무류",
    "소나무림": "소나무류",
    "잣나무림 a": "잣나무류",
    "잣나무림 b": "잣나무류",
    "버드나무림 a": "버드나무류",
    "버드나무림 b": "버드나무류",
    "일본잎갈나무림 a": "낙엽송(일본잎갈나무)",
    "일본잎갈나무림 b": "낙엽송(일본잎갈나무)",
    "밭(대조구)": "대조구",
    "주차장(대조구)": "대조구"
}
is_forest = {
    "리기다소나무림": True,
    "잣나무림 a": True,
    "잣나무림 b": True,
    "버드나무림 a": True,
    "버드나무림 b": True,
    "소나무림": True,
    "일본잎갈나무림 a": True,
    "일본잎갈나무림 b": True,
    "밭(대조구)": False,
    "주차장(대조구)": False
}
valid_df['species_group'] = valid_df['site_name'].map(species_map)

dates = sorted(valid_df['date'].unique())
sites = [
    "리기다소나무림", "잣나무림 a", "버드나무림 a", "밭(대조구)", "주차장(대조구)",
    "소나무림", "일본잎갈나무림 a", "버드나무림 b", "일본잎갈나무림 b", "잣나무림 b"
]

# -------------------------------------------------------------
# Figure 1: Grouped Bar Chart of Site Means by Date
# -------------------------------------------------------------
site_date_stats = valid_df.groupby(['site_name', 'date']).agg(
    mean=('ion_value', 'mean'),
    std=('ion_value', 'std')
).unstack('date')

means = site_date_stats['mean'].reindex(sites)
stds = site_date_stats['std'].reindex(sites)

x = np.arange(len(sites))
width = 0.2
colors = ['#4e79a7', '#59a14f', '#f28e2b', '#e15759']

fig, ax = plt.subplots(figsize=(15, 8), dpi=200)

for i, (date, color) in enumerate(zip(dates, colors)):
    offset = (i - 1.5) * width
    bars = ax.bar(x + offset, means[date], width, yerr=stds[date], capsize=3,
                  label=f"{date}", color=color, alpha=0.9, edgecolor='black', linewidth=0.5)

ax.set_ylabel('음이온 발생량 (개/㎤)', fontsize=12, fontweight='bold')
ax.set_title('조사일자 및 조사지점별 평균 음이온 발생량 비교 (오차막대: 표준편차)', fontsize=15, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(sites, rotation=25, ha='right', fontsize=11, fontweight='bold')
ax.legend(title='조사일자', fontsize=11, title_fontsize=12)
ax.grid(axis='y', linestyle='--', alpha=0.4)
fig.tight_layout()
fig.savefig(fig_dir / "01_일자별_지점별_음이온발생량_비교.png")
plt.close(fig)
print("Saved 01_일자별_지점별_음이온발생량_비교.png")

# -------------------------------------------------------------
# Figure 2: Species Seasonal Trajectory
# -------------------------------------------------------------
species_order = ["버드나무류", "소나무류", "낙엽송(일본잎갈나무)", "잣나무류", "대조구"]
species_date_stats = valid_df.groupby(['species_group', 'date'])['ion_value'].agg(['mean', 'std']).reset_index()

fig, ax = plt.subplots(figsize=(11, 7), dpi=200)
palette = {
    "버드나무류": "#2ca02c",
    "소나무류": "#1f77b4",
    "낙엽송(일본잎갈나무)": "#ff7f0e",
    "잣나무류": "#9467bd",
    "대조구": "#7f7f7f"
}
markers = {"버드나무류": "o", "소나무류": "s", "낙엽송(일본잎갈나무)": "^", "잣나무류": "D", "대조구": "X"}

for sp in species_order:
    sp_data = species_date_stats[species_date_stats['species_group'] == sp]
    ax.plot(sp_data['date'], sp_data['mean'], marker=markers[sp], markersize=9,
            linewidth=2.5, label=sp, color=palette[sp])
    for _, row in sp_data.iterrows():
        ax.annotate(f"{row['mean']:.0f}", (row['date'], row['mean']),
                    textcoords="offset points", xytext=(0, 9), ha='center',
                    fontsize=9, fontweight='bold', color=palette[sp])

ax.set_xlabel('조사일자', fontsize=12, fontweight='bold')
ax.set_ylabel('평균 음이온 발생량 (개/㎤)', fontsize=12, fontweight='bold')
ax.set_title('수종(임상)별 시기별 음이온 발생량 변화 추세', fontsize=15, fontweight='bold', pad=15)
ax.legend(title='수종 분류', fontsize=11, title_fontsize=12)
ax.grid(True, linestyle='--', alpha=0.4)
fig.tight_layout()
fig.savefig(fig_dir / "02_수종별_계절추세_변화.png")
plt.close(fig)
print("Saved 02_수종별_계절추세_변화.png")

# -------------------------------------------------------------
# Figure 3: Forest vs Control Comparison & Ratio
# -------------------------------------------------------------
fc_df = valid_df.groupby(['date', 'is_forest'])['ion_value'].mean().unstack()
fc_df.columns = ['대조구(밭·주차장)', '산림(8개 지점)']
fc_df['산림/대조구 배율'] = fc_df['산림(8개 지점)'] / fc_df['대조구(밭·주차장)']

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=200)

# Left: Bar chart
x_idx = np.arange(len(dates))
w = 0.35
ax1.bar(x_idx - w/2, fc_df['산림(8개 지점)'], w, label='산림(8개 지점)', color='#2e7d32', edgecolor='black', linewidth=0.5)
ax1.bar(x_idx + w/2, fc_df['대조구(밭·주차장)'], w, label='대조구(밭·주차장)', color='#8d6e63', edgecolor='black', linewidth=0.5)
ax1.set_xticks(x_idx)
ax1.set_xticklabels(dates, rotation=15, fontsize=10, fontweight='bold')
ax1.set_ylabel('평균 음이온 발생량 (개/㎤)', fontsize=11, fontweight='bold')
ax1.set_title('산림 vs 대조구 평균 농도 비교', fontsize=13, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(axis='y', linestyle='--', alpha=0.4)

# Value annotations
for i in range(len(dates)):
    f_val = fc_df['산림(8개 지점)'].iloc[i]
    c_val = fc_df['대조구(밭·주차장)'].iloc[i]
    ax1.text(i - w/2, f_val + 30, f"{f_val:.0f}", ha='center', fontsize=9, fontweight='bold', color='#1b5e20')
    ax1.text(i + w/2, c_val + 30, f"{c_val:.0f}", ha='center', fontsize=9, fontweight='bold', color='#4e342e')

# Right: Ratio Line plot
ax2.plot(dates, fc_df['산림/대조구 배율'], marker='o', markersize=10, linewidth=3, color='#c2185b')
ax2.axhline(1.0, color='gray', linestyle=':', linewidth=1.5, label='동일 기준선(1.0배)')
for i, d in enumerate(dates):
    ratio = fc_df['산림/대조구 배율'].iloc[i]
    ax2.annotate(f"{ratio:.2f}배", (d, ratio), textcoords="offset points",
                 xytext=(0, 10), ha='center', fontsize=11, fontweight='bold', color='#c2185b')

ax2.set_xticks(range(len(dates)))
ax2.set_xticklabels(dates, rotation=15, fontsize=10, fontweight='bold')
ax2.set_ylabel('대조구 대비 산림 배율 (배)', fontsize=11, fontweight='bold')
ax2.set_title('시기별 대조구 대비 산림 음이온 발생 배율', fontsize=13, fontweight='bold')
ax2.set_ylim(0, 3.5)
ax2.legend(fontsize=10)
ax2.grid(True, linestyle='--', alpha=0.4)

fig.suptitle('산림 지역과 대조구 간 음이온 방출 효과 비교', fontsize=15, fontweight='bold', y=1.02)
fig.tight_layout()
fig.savefig(fig_dir / "03_산림_대조구_비교_및_배율.png")
plt.close(fig)
print("Saved 03_산림_대조구_비교_및_배율.png")

# -------------------------------------------------------------
# Figure 4: Box Plot of Distributions across Sites & Dates
# -------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(16, 12), dpi=200, sharey=False)
axes = axes.flatten()

for idx, date in enumerate(dates):
    ax = axes[idx]
    sub = valid_df[valid_df['date'] == date]
    data_to_plot = [sub[sub['site_name'] == s]['ion_value'].dropna().values for s in sites]
    
    # Custom boxplot
    bp = ax.boxplot(data_to_plot, patch_artist=True,
                    boxprops=dict(facecolor='#d0e1f9', color='#1e3f66', linewidth=1.2),
                    whiskerprops=dict(color='#1e3f66', linewidth=1.2),
                    capprops=dict(color='#1e3f66', linewidth=1.2),
                    medianprops=dict(color='#d63031', linewidth=2),
                    flierprops=dict(marker='.', markersize=2, alpha=0.2, color='gray'),
                    widths=0.6)
    
    # Color control sites differently
    for s_i, s_name in enumerate(sites):
        if not is_forest[s_name]:
            bp['boxes'][s_i].set_facecolor('#fde2e4')
            bp['boxes'][s_i].set_edgecolor('#c92a2a')
            
    ax.set_title(f"[{date}] 지점별 음이온 분포 (900초)", fontsize=12, fontweight='bold')
    ax.set_xticks(range(1, len(sites) + 1))
    ax.set_xticklabels(sites, rotation=35, ha='right', fontsize=9)
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.set_ylabel('음이온 발생량 (개/㎤)', fontsize=10)

fig.suptitle('조사일자별 각 지점 음이온 발생량 분포 (붉은색: 대조구, 파란색: 산림지점)', fontsize=15, fontweight='bold', y=0.99)
fig.tight_layout(rect=[0, 0.03, 1, 0.96])
fig.savefig(fig_dir / "04_지점별_음이온분포_박스플롯.png")
plt.close(fig)
print("Saved 04_지점별_음이온분포_박스플롯.png")

# -------------------------------------------------------------
# Figure 5: Crossover / Diurnal Timing Plot
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 7), dpi=200)

session_timing = valid_df.groupby(['date', 'site_id', 'site_name', 'is_forest']).agg(
    mean=('ion_value', 'mean'),
    start_hour=('hour_float', 'min')
).reset_index()

for date, col, mkr in zip(dates, colors, ['o', 's', '^', 'D']):
    d_data = session_timing[session_timing['date'] == date].sort_values('start_hour')
    ax.plot(d_data['start_hour'], d_data['mean'], marker=mkr, markersize=8,
            linewidth=2, label=date, color=col, alpha=0.85)
    for _, row in d_data.iterrows():
        # Label only high or interesting sites
        if row['mean'] > 1500 or row['date'] == '2026-08-13':
            ax.annotate(row['site_name'], (row['start_hour'], row['mean']),
                        textcoords="offset points", xytext=(0, 8), ha='center',
                        fontsize=8, color=col)

ax.set_xlabel('측정 시작 시각 (24시간제)', fontsize=12, fontweight='bold')
ax.set_ylabel('지점 평균 음이온 발생량 (개/㎤)', fontsize=12, fontweight='bold')
ax.set_title('일중 측정 시각에 따른 음이온 발생량 및 조사 순서 교차(Crossover) 효과\n(4월/7월: 지점1→10 순차측정 vs 8월13일: 지점10→1 역순측정)', fontsize=14, fontweight='bold', pad=12)
ax.set_xticks(np.arange(8, 16.5, 1))
ax.set_xticklabels([f"{int(h):02d}:00" for h in np.arange(8, 16.5, 1)])
ax.grid(True, linestyle='--', alpha=0.4)
ax.legend(title='조사일자', fontsize=10, title_fontsize=11)
fig.tight_layout()
fig.savefig(fig_dir / "05_측정시각_및_역순교차_비교.png")
plt.close(fig)
print("Saved 05_측정시각_및_역순교차_비교.png")

# -------------------------------------------------------------
# Figure 6: Within-session 1-minute Trend Profiles
# -------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(16, 10), dpi=200, sharex=True, sharey=True)
axes = axes.flatten()

for idx, date in enumerate(dates):
    ax = axes[idx]
    sub = valid_df[valid_df['date'] == date]
    min_stats = sub.groupby(['minute_bucket', 'site_name'])['ion_value'].mean().unstack()
    
    for s_name in sites:
        ls = '-' if is_forest[s_name] else '--'
        lw = 1.5 if is_forest[s_name] else 2.5
        alpha = 0.8 if is_forest[s_name] else 1.0
        ax.plot(min_stats.index, min_stats[s_name], label=s_name, linestyle=ls, linewidth=lw, alpha=alpha)
        
    ax.set_title(f"[{date}] 15분 측정 구간 내 1분 단위 평균 추이", fontsize=12, fontweight='bold')
    ax.set_xlabel('측정 경과 분 (1~15분)', fontsize=10)
    ax.set_ylabel('음이온 발생량 (개/㎤)', fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.set_xticks(range(1, 16))

axes[0].legend(fontsize=8, loc='upper right', ncol=2)
fig.suptitle('각 조사일자별 15분 관측 세션 내 1분 단위 시간적 안정성 추이\n(실선: 산림 지점, 점선: 대조구 지점)', fontsize=15, fontweight='bold', y=0.98)
fig.tight_layout(rect=[0, 0.03, 1, 0.95])
fig.savefig(fig_dir / "06_15분_세션내_1분단위_안정성추세.png")
plt.close(fig)
print("Saved 06_15분_세션내_1분단위_안정성추세.png")

# -------------------------------------------------------------
# Figure 7: Coefficient of Variation (CV) Stability
# -------------------------------------------------------------
cv_stats = valid_df.groupby(['site_name', 'date']).agg(
    mean=('ion_value', 'mean'),
    std=('ion_value', 'std')
).reset_index()
cv_stats['cv'] = cv_stats['std'] / cv_stats['mean'] * 100
cv_pivot = cv_stats.pivot(index='site_name', columns='date', values='cv').reindex(sites)

fig, ax = plt.subplots(figsize=(14, 7), dpi=200)
x = np.arange(len(sites))
width = 0.2

for i, (date, color) in enumerate(zip(dates, colors)):
    offset = (i - 1.5) * width
    ax.bar(x + offset, cv_pivot[date], width, label=date, color=color, alpha=0.9, edgecolor='black', linewidth=0.5)

ax.set_ylabel('변동계수 (CV, %)', fontsize=12, fontweight='bold')
ax.set_title('지점별·일자별 음이온 발생량 변동계수(CV) 비교 (측정 안정성 지표)', fontsize=14, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(sites, rotation=25, ha='right', fontsize=11, fontweight='bold')
ax.legend(title='조사일자', fontsize=11, title_fontsize=12)
ax.grid(axis='y', linestyle='--', alpha=0.4)
fig.tight_layout()
fig.savefig(fig_dir / "07_지점별_변동계수_안정성비교.png")
plt.close(fig)
print("Saved 07_지점별_변동계수_안정성비교.png")

print("All 7 figures successfully generated and saved!")
