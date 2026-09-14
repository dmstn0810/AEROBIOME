import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import shutil
from pathlib import Path

import sys
import io

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Set font for Korean support
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

workspace_dir = Path(r"C:\Users\user\orca\workspaces\괴산 공기미생물\음이온-2")
brain_dir = Path(r"C:\Users\user\.gemini\antigravity-cli\brain\6cb9fef6-d52d-4189-8337-6a158db6aad6")
figures_dir = workspace_dir / "figures"
figures_dir.mkdir(parents=True, exist_ok=True)
outputs_dir = workspace_dir / "outputs"
outputs_dir.mkdir(parents=True, exist_ok=True)

# 1. Load Data
file_path = workspace_dir / "괴산연습림 전체데이터.xlsx"
df = pd.read_excel(file_path)

ion_col = df.columns[15] # n-ion (개/cm3)

# 2. Mathematical Formulations for Sub-Indices

def calc_bsi(row):
    """
    Bio-Sanitary Index (BSI, 생물학적 청정도 지수, 0~100)
    부유세균(PCA-B)과 부유진균(PDA-F)의 대기 위해성을 환경부/WHO 기준에 기반하여 역지수 평가.
    """
    cb = row['PCA-B (CFU/m3)']
    cf = row['PDA-F (CFU/m3)']
    
    # 부유세균 점수 (기준: 800 이하 유지기준, 자연산림 정상치 50~200)
    if cb <= 50:
        sb = 100.0
    elif cb <= 200:
        sb = 100.0 - 20.0 * (cb - 50) / 150.0
    elif cb <= 800:
        sb = 80.0 - 40.0 * (cb - 200) / 600.0
    else:
        sb = max(0.0, 40.0 - 40.0 * (cb - 800) / 1200.0)
        
    # 부유진균 점수 (기준: 500 권고기준, WHO 1000 위해기준)
    if cf <= 300:
        sf = 100.0
    elif cf <= 500:
        sf = 100.0 - 20.0 * (cf - 300) / 200.0
    elif cf <= 1000:
        sf = 80.0 - 40.0 * (cf - 500) / 500.0
    else:
        sf = max(0.0, 40.0 - 40.0 * (cf - 1000) / 1500.0)
        
    return 0.5 * sb + 0.5 * sf

def calc_nvi(row):
    """
    Nature Vitality & Therapy Index (NVI, 자연생명 치유력 지수, 0~100)
    공기 음이온 농도를 로그 포화 함수로 정규화 (5,000 개/cm3 도달 시 100점).
    """
    ion = row[ion_col]
    if pd.isna(ion):
        return np.nan
    score = 100.0 * np.log(1.0 + ion / 100.0) / np.log(1.0 + 5000.0 / 100.0)
    return min(100.0, max(0.0, score))

def calc_api(row):
    """
    Atmospheric Purity Index (API, 대기순도 지수, 0~100)
    PM10과 PM2.5 미세먼지 환경기준을 기반으로 청정도 점수 산출.
    """
    p10 = row['PM10']
    p25 = row['PM2.5']
    
    # PM10 (좋음 0~30, 보통 31~80, 나쁨 81~150)
    if p10 <= 15:
        s10 = 100.0
    elif p10 <= 30:
        s10 = 100.0 - 15.0 * (p10 - 15) / 15.0
    elif p10 <= 80:
        s10 = 85.0 - 45.0 * (p10 - 30) / 50.0
    else:
        s10 = max(0.0, 40.0 - 40.0 * (p10 - 80) / 70.0)
        
    # PM2.5 (좋음 0~15, 보통 16~35, 나쁨 36~75)
    if p25 <= 8:
        s25 = 100.0
    elif p25 <= 15:
        s25 = 100.0 - 15.0 * (p25 - 8) / 7.0
    elif p25 <= 35:
        s25 = 85.0 - 45.0 * (p25 - 15) / 20.0
    else:
        s25 = max(0.0, 40.0 - 40.0 * (p25 - 35) / 40.0)
        
    return 0.4 * s10 + 0.6 * s25

# 기준 대조구(밭, site no. 4) 일자별 평균 기온
field_temp = df[df['site no.'] == 4].groupby('date')['air-temp'].mean().to_dict()

def calc_mbi(row):
    """
    Microclimate Buffering & Comfort Index (MBI, 미기후 완충쾌적 지수, 0~100)
    하계 냉각 효과(Cooling), 온열 쾌적 온도(18~24C), 습도(45~65%), 풍속(0.2~1.0m/s) 종합.
    """
    t = row['air-temp']
    d = row['date']
    t_ref = field_temp.get(d, t)
    
    # 1) 온열 완충/쾌적 점수 (40%)
    if t_ref >= 24.0:
        # 혹서기: 밭 대조구 대비 냉각 효과 (Cooling)
        delta_t = t_ref - t
        if delta_t >= 5.0:
            st = 100.0
        elif delta_t >= 0.0:
            st = 70.0 + 6.0 * delta_t # 0도 차이면 70점, 5도 차이면 100점
        else:
            st = max(30.0, 70.0 - 10.0 * abs(delta_t))
    else:
        # 온난/춘추기: 최적 쾌적 기온(20도) 근접도
        dist = abs(t - 20.0)
        st = max(30.0, 100.0 - 5.0 * dist)
        
    # 2) 습도 쾌적도 (30%, 최적 45~65%)
    rh = row['air-RH']
    if 45.0 <= rh <= 65.0:
        sh = 100.0
    elif rh < 45.0:
        sh = max(40.0, 100.0 - 2.0 * (45.0 - rh))
    else:
        sh = max(40.0, 100.0 - 2.5 * (rh - 65.0))
        
    # 3) 풍속 정온도 (30%, 산들바람 0.2~1.0 m/s 최적)
    w = row['windspeed']
    if 0.2 <= w <= 1.0:
        sw = 100.0
    elif w < 0.2:
        sw = 90.0
    else:
        sw = max(30.0, 100.0 - 35.0 * (w - 1.0))
        
    return 0.4 * st + 0.3 * sh + 0.3 * sw

# Apply sub-indices
df['BSI'] = df.apply(calc_bsi, axis=1)
df['NVI'] = df.apply(calc_nvi, axis=1)
df['API'] = df.apply(calc_api, axis=1)
df['MBI'] = df.apply(calc_mbi, axis=1)

# 3. Composite Climate-Life-Health Eco-Index (CLHEI)
def calc_clhei(row):
    if pd.notna(row['NVI']):
        # 음이온 실측 전수 모드: BSI(30%) + NVI(30%) + API(20%) + MBI(20%)
        return 0.30 * row['BSI'] + 0.30 * row['NVI'] + 0.20 * row['API'] + 0.20 * row['MBI']
    else:
        # 음이온 미측정 상시 모드: BSI(40%) + API(30%) + MBI(30%)
        return 0.40 * row['BSI'] + 0.30 * row['API'] + 0.30 * row['MBI']

df['CLHEI'] = df.apply(calc_clhei, axis=1)

# 4. Grading System
def assign_grade(score):
    if score >= 85.0:
        return '1등급 (천연 최우수 치유림)'
    elif score >= 75.0:
        return '2등급 (우수 생태 건강림)'
    elif score >= 65.0:
        return '3등급 (보통 생태 녹지)'
    elif score >= 50.0:
        return '4등급 (환경 스트레스 주의림)'
    else:
        return '5등급 (생태 미흡 대조구)'

df['CLHEI_Grade'] = df['CLHEI'].apply(assign_grade)

# Map clean vegetative group names based on site no.
site_name_map = {
    1: '리기다소나무림',
    2: '잣나무림 a',
    3: '버드나무림 a',
    4: '밭(대조구)',
    5: '주차장(대조구)',
    6: '소나무림',
    7: '일본잎갈나무림 a',
    8: '버드나무림 b',
    9: '일본잎갈나무림 b',
    10: '잣나무림 b'
}
vege_group_map = {
    1: '소나무류',
    2: '잣나무류',
    3: '버드나무류',
    4: '밭(대조구)',
    5: '주차장(대조구)',
    6: '소나무류',
    7: '낙엽송류',
    8: '버드나무류',
    9: '낙엽송류',
    10: '잣나무류'
}
df['site_name'] = df['site no.'].map(site_name_map)
df['vege_group'] = df['site no.'].map(vege_group_map)

# Save enhanced dataset to Excel
excel_out_path = outputs_dir / "괴산학술림_기후생명건강지수_평가결과.xlsx"
with pd.ExcelWriter(excel_out_path, engine='openpyxl') as writer:
    # Tab 1: Full dataset with scores
    df.to_excel(writer, sheet_name='전체_지수산출결과', index=False)
    
    # Tab 2: Site summary
    site_sum = df.groupby(['site no.', 'site_name', 'vege_group'])[['BSI', 'NVI', 'API', 'MBI', 'CLHEI']].agg(['mean', 'std', 'min', 'max']).round(1)
    site_sum.to_excel(writer, sheet_name='지점별_평균지수')
    
    # Tab 3: Group summary
    grp_sum = df.groupby('vege_group')[['BSI', 'NVI', 'API', 'MBI', 'CLHEI']].mean().round(1).sort_values(by='CLHEI', ascending=False)
    grp_sum['평가등급'] = grp_sum['CLHEI'].apply(assign_grade)
    grp_sum.to_excel(writer, sheet_name='수종그룹별_평가지수')
    
    # Tab 4: Date summary
    date_sum = df.groupby('date')[['BSI', 'NVI', 'API', 'MBI', 'CLHEI']].mean().round(1)
    date_sum['평가등급'] = date_sum['CLHEI'].apply(assign_grade)
    date_sum.to_excel(writer, sheet_name='시기별_평균지수')
    
    # Tab 5: Forest vs Field comparison
    df['is_forest'] = df['site no.'].apply(lambda x: '산림(8개 지점)' if x not in [4, 5] else ('밭(대조구)' if x == 4 else '주차장(대조구)'))
    forest_field = df.groupby(['date', 'is_forest'])[['BSI', 'NVI', 'API', 'MBI', 'CLHEI']].mean().round(1)
    forest_field.to_excel(writer, sheet_name='산림vs대조구_비교')

print(f"[OK] Successfully exported index workbook to: {excel_out_path}")

# ==========================================
# 5. Visualizations
# ==========================================

# Chart 17: Radar Chart by Forest Type vs Control Field
categories = ['생물학적 청정도\n(BSI)', '자연 치유력\n(NVI, 음이온)', '대기 미세먼지순도\n(API)', '미기후 완충쾌적\n(MBI)']
N = len(categories)

# Compute mean of sub-indices for key types (using rows with NVI for fair radar comparison)
df_with_nvi = df[df['NVI'].notna()]
radar_groups = ['버드나무류', '소나무류', '잣나무류', '낙엽송류', '밭(대조구)']
radar_data = df_with_nvi.groupby('vege_group')[['BSI', 'NVI', 'API', 'MBI']].mean().loc[radar_groups].values

angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1] # close circle

fig, ax = plt.subplots(figsize=(9, 8), subplot_kw=dict(polar=True))
colors = ['#2d6a4f', '#1b4332', '#40916c', '#52b788', '#d00000']
line_styles = ['-', '-', '--', '-.', '-']

for i, (grp_name, vals) in enumerate(zip(radar_groups, radar_data)):
    v = vals.tolist()
    v += v[:1]
    ax.plot(angles, v, linewidth=2.2, linestyle=line_styles[i], label=f"{grp_name} (CLHEI {df_with_nvi[df_with_nvi['vege_group']==grp_name]['CLHEI'].mean():.1f}점)", color=colors[i])
    ax.fill(angles, v, color=colors[i], alpha=0.08)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=11, fontweight='bold')
ax.set_ylim(30, 100)
ax.set_yticks([40, 55, 70, 85, 100])
ax.set_yticklabels(['40점', '55점', '70점', '85점', '100점'], fontsize=9, color='gray')
ax.set_title("건국대학교 괴산학술림 수종별 기후생명건강지수(CLHEI) 4대 축 레이더 비교", fontsize=14, fontweight='bold', pad=25)
ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.1), fontsize=10)
plt.tight_layout()

fig17_path = figures_dir / "17_기후생명건강지수_수종별_비교_레이더차트.png"
fig.savefig(fig17_path, dpi=300, bbox_inches='tight')
plt.close(fig)
print(f"✓ Figure 17 saved: {fig17_path}")

# Chart 18: Seasonal Trajectory of CLHEI & Sub-indices
dates_str = [d.strftime('%m-%d') if hasattr(d, 'strftime') else str(d)[:10] for d in date_sum.index]
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 9), sharex=True)

# Subplot 1: Sub-indices trajectory
ax1.plot(dates_str, date_sum['BSI'], marker='o', linewidth=2.2, color='#2a9d8f', label='생물학적 청정도 (BSI)')
ax1.plot(dates_str, date_sum['API'], marker='s', linewidth=2.2, color='#457b9d', label='대기순도 (API, 미세먼지)')
ax1.plot(dates_str, date_sum['MBI'], marker='^', linewidth=2.2, color='#e76f51', label='미기후 완충쾌적 (MBI)')
# NVI only on 4 dates
nvi_valid_dates = [d.strftime('%m-%d') if hasattr(d, 'strftime') else str(d)[:10] for d in df[df['NVI'].notna()]['date'].unique()]
nvi_valid_means = df.groupby('date')['NVI'].mean().dropna().values
ax1.plot(nvi_valid_dates, nvi_valid_means, marker='D', linewidth=2.5, color='#e63946', linestyle='--', label='자연치유력 (NVI, 음이온)')

ax1.axhline(85, color='green', linestyle=':', alpha=0.5, label='1등급 기준선 (85점)')
ax1.axhline(75, color='blue', linestyle=':', alpha=0.5, label='2등급 기준선 (75점)')
ax1.set_ylabel("서브 인덱스 점수 (0~100점)", fontsize=11, fontweight='bold')
ax1.set_title("괴산학술림 조사 시기별 서브 인덱스 동태 (2026년 3월~8월)", fontsize=13, fontweight='bold')
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.legend(loc='lower left', fontsize=9.5, ncol=3)

# Subplot 2: Overall CLHEI by Forest vs Field
forest_traj = df[df['site no.'].isin([1,2,3,6,7,8,9,10])].groupby('date')['CLHEI'].mean()
field_traj = df[df['site no.'] == 4].groupby('date')['CLHEI'].mean()

ax2.plot(dates_str, forest_traj.values, marker='o', markersize=8, linewidth=3.0, color='#1b4332', label='산림 8개 지점 종합 평균')
ax2.plot(dates_str, field_traj.values, marker='X', markersize=8, linewidth=2.5, color='#d00000', linestyle='--', label='밭(대조구) 종합 점수')

# Highlight gap
for i, d_str in enumerate(dates_str):
    diff = forest_traj.values[i] - field_traj.values[i]
    ax2.annotate(f"산림 우세\n+{diff:.1f}p", xy=(i, forest_traj.values[i]), xytext=(i, forest_traj.values[i] + 3.0),
                 ha='center', fontsize=9, fontweight='bold', color='#1b4332')

ax2.set_xlabel("조사 일자", fontsize=11, fontweight='bold')
ax2.set_ylabel("종합 CLHEI 점수", fontsize=11, fontweight='bold')
ax2.set_title("산림 vs 밭(대조구) 기후생명건강지수(CLHEI) 격차 시계열 추이", fontsize=13, fontweight='bold')
ax2.set_ylim(55, 95)
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.legend(loc='lower right', fontsize=10)

plt.tight_layout()
fig18_path = figures_dir / "18_기후생명건강지수_6개시기_계절추세.png"
fig.savefig(fig18_path, dpi=300, bbox_inches='tight')
plt.close(fig)
print(f"[OK] Figure 18 saved: {fig18_path}")

# Chart 19: Forest vs Field Gap Boxplot & Bar Chart
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))

# Left: Overall CLHEI Boxplot by Group
order_groups = ['버드나무류', '소나무류', '잣나무류', '낙엽송류', '주차장(대조구)', '밭(대조구)']
data_box = [df[df['vege_group'] == g]['CLHEI'].values for g in order_groups if len(df[df['vege_group'] == g]) > 0]
colors_box = ['#2d6a4f', '#1b4332', '#40916c', '#52b788', '#adb5bd', '#d00000']

bplot = ax1.boxplot(data_box, patch_artist=True, tick_labels=order_groups, showmeans=True,
                    meanprops=dict(marker='D', markeredgecolor='black', markerfacecolor='yellow', markersize=6))
for patch, color in zip(bplot['boxes'], colors_box):
    patch.set_facecolor(color)
    patch.set_alpha(0.8)

ax1.axhline(85, color='green', linestyle='--', alpha=0.7, label='1등급(최우수, 85점)')
ax1.axhline(75, color='blue', linestyle='--', alpha=0.7, label='2등급(우수, 75점)')
ax1.axhline(65, color='orange', linestyle='--', alpha=0.7, label='3등급(보통, 65점)')
ax1.set_ylabel("기후생명건강지수 (CLHEI)", fontsize=11, fontweight='bold')
ax1.set_title("(A) 임상·수종 그룹별 종합 생태건강지수 분포", fontsize=12, fontweight='bold')
ax1.tick_params(axis='x', rotation=30)
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend(loc='lower left', fontsize=9)

# Right: Forest vs Field Sub-indices Comparison Bar Chart
forest_means = df[df['site no.'].isin([1,2,3,6,7,8,9,10])][['BSI', 'NVI', 'API', 'MBI', 'CLHEI']].mean()
field_means = df[df['site no.'] == 4][['BSI', 'NVI', 'API', 'MBI', 'CLHEI']].mean()

x = np.arange(5)
width = 0.35

rects1 = ax2.bar(x - width/2, forest_means.values, width, label='산림 (8개 지점 평균)', color='#1b4332', alpha=0.9)
rects2 = ax2.bar(x + width/2, field_means.values, width, label='밭 (대조구)', color='#d00000', alpha=0.85)

ax2.set_ylabel("점수 (0~100점)", fontsize=11, fontweight='bold')
ax2.set_title("(B) 산림 vs 밭(대조구) 지표별 정량 격차", fontsize=12, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(['생물청정\n(BSI)', '자연치유\n(NVI)', '대기순도\n(API)', '미기후완충\n(MBI)', '종합지수\n(CLHEI)'], fontsize=10, fontweight='bold')
ax2.set_ylim(0, 105)
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.legend(loc='lower right', fontsize=10)

# Add value labels
for rect in rects1:
    h = rect.get_height()
    ax2.annotate(f'{h:.1f}', xy=(rect.get_x() + rect.get_width() / 2, h), xytext=(0, 3),
                 textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#1b4332')
for rect in rects2:
    h = rect.get_height()
    ax2.annotate(f'{h:.1f}', xy=(rect.get_x() + rect.get_width() / 2, h), xytext=(0, 3),
                 textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#d00000')

plt.tight_layout()
fig19_path = figures_dir / "19_산림_vs_밭대조구_생태지수_격차분석.png"
fig.savefig(fig19_path, dpi=300, bbox_inches='tight')
plt.close(fig)
print(f"[OK] Figure 19 saved: {fig19_path}")

# Copy newly generated figures to brain directory for artifact embedding
for fig_p in [fig17_path, fig18_path, fig19_path]:
    dest = brain_dir / fig_p.name
    shutil.copy(fig_p, dest)
    print(f"[OK] Synced to brain: {dest}")

print("=== ALL INDEX COMPUTATIONS & FIGURES COMPLETE ===")
