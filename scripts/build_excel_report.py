import sys
from pathlib import Path
import pandas as pd
import numpy as np
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

sys.stdout.reconfigure(encoding='utf-8')

# Read datasets
df = pd.read_csv("data/ion_dataset_all.csv")
df['timestamp_dt'] = pd.to_datetime(df['timestamp'])
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
valid_df['species_group'] = valid_df['site_name'].map(species_map)
dates = sorted(valid_df['date'].unique())

out_file = Path("outputs/음이온_전체일자_종합분석_보고서.xlsx")
wb = openpyxl.Workbook()
# remove default sheet
wb.remove(wb.active)

# Styles
header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
header_font = Font(name="맑은 고딕", size=11, bold=True, color="FFFFFF")
title_font = Font(name="맑은 고딕", size=16, bold=True, color="1F497D")
sub_font = Font(name="맑은 고딕", size=12, bold=True, color="2C5E8A")
bold_font = Font(name="맑은 고딕", size=10, bold=True)
regular_font = Font(name="맑은 고딕", size=10)
thin_side = Side(border_style="thin", color="D9D9D9")
thin_border = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)
thick_bottom = Border(bottom=Side(border_style="medium", color="1F497D"))
center_align = Alignment(horizontal="center", vertical="center")
right_align = Alignment(horizontal="right", vertical="center")
left_align = Alignment(horizontal="left", vertical="center")

# -------------------------------------------------------------
# Sheet 1: 요약보고서 (Executive Summary)
# -------------------------------------------------------------
ws1 = wb.create_sheet(title="요약보고서")
ws1.views.sheetView[0].showGridLines = True

ws1.cell(2, 2, "괴산 공기미생물 및 음이온 4개 일자 종합 분석 보고서").font = title_font
ws1.cell(3, 2, "조사 대상: 2026-04-15, 2026-04-29, 2026-07-27, 2026-08-13 (총 36,000건 관측치)").font = sub_font

# Section 1: Overview
r = 5
ws1.cell(r, 2, "1. 데이터 개요 및 측정 특성").font = sub_font
r += 1
overview_data = [
    ("조사 일자", "봄철 2회 (4월 15일, 4월 29일) / 여름철 2회 (7월 27일, 8월 13일)"),
    ("조사 지점", "총 10개 지점 (산림 8개 지점, 대조구 2개 지점[밭, 주차장])"),
    ("측정 방식", "지점당 900초 (15분간 1초 단위 연속 측정), 일자당 9,000초, 총 36,000건"),
    ("조사 순서 설계", "4월/7월: 지점 1 → 10 순차 측정 vs 8월 13일: 지점 10 → 1 역순 교차(Crossover) 측정"),
    ("유효 데이터 수", "총 36,000건 중 35,996건 유효 (2026-08-13 비수치 문자열 '****' 4건 보존 및 통계 제외)"),
    ("시계열 특성", "1초 지연 자기상관(Lag-1 Autocorrelation) 평균 0.961 (고도의 시간적 연속성 보유)")
]
for item, desc in overview_data:
    ws1.cell(r, 2, item).font = bold_font
    ws1.cell(r, 2).fill = PatternFill(start_color="F2F2F2", fill_type="solid")
    ws1.cell(r, 3, desc).font = regular_font
    ws1.cell(r, 2).border = thin_border
    ws1.cell(r, 3).border = thin_border
    r += 1

# Section 2: Core Findings Table
r += 2
ws1.cell(r, 2, "2. 일자별 산림 vs 대조구 핵심 비교").font = sub_font
r += 1

fc_headers = ["조사일자", "산림 8개 지점 평균", "산림 표준편차", "대조구 전체 평균", "밭(대조구) 평균", "주차장(대조구) 평균", "산림/대조구 배율", "산림/밭 배율"]
for c_i, h in enumerate(fc_headers, 2):
    c = ws1.cell(r, c_i, h)
    c.fill = header_fill
    c.font = header_font
    c.alignment = center_align
    c.border = thin_border

fc_summary = [
    ("2026-04-15", 551.3, 251.7, 459.7, 506.9, 412.6, 1.20, 1.09),
    ("2026-04-29", 614.1, 258.0, 1132.7, 511.1, 1754.3, 0.54, 1.20),
    ("2026-07-27", 925.3, 474.5, 700.9, 409.6, 992.3, 1.32, 2.26),
    ("2026-08-13", 2561.7, 1375.4, 898.5, 470.9, 1326.1, 2.85, 5.44)
]
r += 1
for row_vals in fc_summary:
    for c_i, val in enumerate(row_vals, 2):
        c = ws1.cell(r, c_i, val)
        c.font = regular_font
        c.border = thin_border
        if c_i == 2:
            c.alignment = center_align
        elif c_i in [8, 9]:
            c.alignment = right_align
            c.number_format = "0.00\"배\""
        else:
            c.alignment = right_align
            c.number_format = "#,##0.0"
    r += 1

# Section 3: Species Comparison
r += 2
ws1.cell(r, 2, "3. 수종(임상)별 시기별 평균 음이온 농도 (개/㎤)").font = sub_font
r += 1
sp_headers = ["수종 분류", "2026-04-15", "2026-04-29", "2026-07-27", "2026-08-13", "전체 평균", "8월/4월 배율"]
for c_i, h in enumerate(sp_headers, 2):
    c = ws1.cell(r, c_i, h)
    c.fill = header_fill
    c.font = header_font
    c.alignment = center_align
    c.border = thin_border

sp_rows = [
    ("버드나무류", 708.3, 804.4, 1050.6, 3655.7, 1554.6, 5.16),
    ("소나무류", 526.7, 608.6, 1362.5, 2617.4, 1278.8, 4.97),
    ("낙엽송(일본잎갈나무)", 505.0, 416.2, 552.3, 2452.7, 981.0, 4.86),
    ("잣나무류", 465.2, 627.0, 736.0, 1521.2, 837.2, 3.27),
    ("대조구(밭·주차장)", 459.7, 1132.7, 700.9, 898.5, 798.0, 1.95)
]
r += 1
for row_vals in sp_rows:
    for c_i, val in enumerate(row_vals, 2):
        c = ws1.cell(r, c_i, val)
        c.font = regular_font
        c.border = thin_border
        if c_i == 2:
            c.alignment = left_align
        elif c_i == 8:
            c.alignment = right_align
            c.number_format = "0.00\"배\""
        else:
            c.alignment = right_align
            c.number_format = "#,##0.0"
    r += 1

# Section 4: Key Insights Notes
r += 2
ws1.cell(r, 2, "4. 핵심 종합 분석 의견").font = sub_font
r += 1
notes = [
    ("여름철 폭발적 증가", "여름 성기인 8월 13일 산림 음이온 발생량은 평균 2,561.7개/㎤로, 봄철(4월 15일 551.3개/㎤) 대비 4.6배 증가함. 수목의 증산작용, 일조량 및 대기 활성도가 극대화된 영향임."),
    ("수종별 우수성", "버드나무류(8월 평균 3,655.7, b지점 최고 4,866.3)와 소나무류(8월 평균 2,617.4, 소나무림 3,500.2)가 전 기간에 걸쳐 가장 높은 음이온 방출 성능을 나타냄."),
    ("대조구 대비 격차", "8월 13일 기준 산림 지점은 대조구 평균 대비 2.85배, 밭 대조구(470.9) 대비로는 무려 5.44배 높은 음이온 농도를 기록하여 산림 치유 효과가 뚜렷함을 입증함."),
    ("조사 순서 교차 검증", "8월 13일 역순 측정(지점 10→1) 결과, 오전 9시대에 측정된 버드나무림 b(4,866.3)와 일본잎갈나무림 a(3,057.9)가 오후 지점보다 더 높게 나타나, 고농도 원인이 단순 오후 시간대 효과가 아닌 산림 고유 특성임을 확인."),
    ("주차장 대조구 특이치", "4월 29일 주차장 대조구에서 평균 1,754.3개/㎤(최대 3,252개/㎤)의 일시적 고농도가 발생함. 차량 이동, 먼지 마찰대전, 기상 변화 등 국소 이벤트로 추정되며, 안정적 대조구로는 밭(전 회차 400~510 유지)이 더 적합함.")
]
for n_title, n_desc in notes:
    ws1.cell(r, 2, n_title).font = bold_font
    ws1.cell(r, 2).alignment = left_align
    ws1.cell(r, 2).fill = PatternFill(start_color="E9EEF4", fill_type="solid")
    ws1.cell(r, 3, n_desc).font = regular_font
    ws1.cell(r, 3).alignment = left_align
    ws1.cell(r, 2).border = thin_border
    ws1.cell(r, 3).border = thin_border
    r += 1

ws1.column_dimensions['B'].width = 24
ws1.column_dimensions['C'].width = 26
ws1.column_dimensions['D'].width = 18
ws1.column_dimensions['E'].width = 18
ws1.column_dimensions['F'].width = 18
ws1.column_dimensions['G'].width = 18
ws1.column_dimensions['H'].width = 18
ws1.column_dimensions['I'].width = 18

# -------------------------------------------------------------
# Sheet 2: 지점별_일자별_통계 (Summary Stats per session)
# -------------------------------------------------------------
ws2 = wb.create_sheet(title="지점별_일자별_통계")
ws2.views.sheetView[0].showGridLines = True

stats_headers = [
    "조사일자", "지점번호", "지점명", "수종분류", "산림구분", "측정건수(N)", "결측건수",
    "시작시각", "종료시각", "평균", "표준편차", "중위수", "Q1(25%)", "Q3(75%)",
    "IQR", "최솟값", "최댓값", "변동계수(CV%)", "일자내순위"
]
for col_idx, h in enumerate(stats_headers, 1):
    c = ws2.cell(1, col_idx, h)
    c.fill = header_fill
    c.font = header_font
    c.alignment = center_align
    c.border = thin_border

# Group stats
grouped = df.groupby(['date', 'site_id', 'site_name', 'site_type', 'is_forest'])
row_idx = 2

for (d, s_id, s_name, s_type, is_f), grp in grouped:
    valid_vals = grp[grp['is_valid']]['ion_value']
    n_count = len(valid_vals)
    n_missing = len(grp) - n_count
    ts_min = grp['timestamp_dt'].min().strftime('%H:%M:%S')
    ts_max = grp['timestamp_dt'].max().strftime('%H:%M:%S')
    
    mean_v = valid_vals.mean()
    std_v = valid_vals.std()
    med_v = valid_vals.median()
    q1_v = valid_vals.quantile(0.25)
    q3_v = valid_vals.quantile(0.75)
    iqr_v = q3_v - q1_v
    min_v = valid_vals.min()
    max_v = valid_vals.max()
    cv_v = (std_v / mean_v * 100) if mean_v > 0 else 0
    
    row_data = [
        d, s_id, s_name, s_type, "산림" if is_f else "대조구", n_count, n_missing,
        ts_min, ts_max, mean_v, std_v, med_v, q1_v, q3_v, iqr_v, min_v, max_v, cv_v
    ]
    for c_i, val in enumerate(row_data, 1):
        cell = ws2.cell(row_idx, c_i, val)
        cell.font = regular_font
        cell.border = thin_border
        if c_i in [1, 8, 9]:
            cell.alignment = center_align
        elif c_i in [2, 5, 6, 7]:
            cell.alignment = center_align
            if c_i in [2, 6, 7]: cell.number_format = "#,##0"
        elif c_i in [3, 4]:
            cell.alignment = left_align
        elif c_i == 18:
            cell.alignment = right_align
            cell.number_format = "0.0\"%\""
        else:
            cell.alignment = right_align
            cell.number_format = "#,##0.0"
            
    # Rank formula within date (Formula: RANK(J2, ...))
    # We can calculate rank in python directly or formula
    # Let's insert formula for Excel interactivity
    date_start_row = 2 + (row_idx - 2) // 10 * 10
    date_end_row = date_start_row + 9
    rank_cell = ws2.cell(row_idx, 19, f"=RANK(J{row_idx}, $J${date_start_row}:$J${date_end_row}, 0)")
    rank_cell.font = bold_font
    rank_cell.alignment = center_align
    rank_cell.border = thin_border
    rank_cell.number_format = "0\"위\""
    
    row_idx += 1

# Auto-adjust column widths
for col in ws2.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = get_column_letter(col[0].column)
    ws2.column_dimensions[col_letter].width = max(max_len + 4, 12)

# -------------------------------------------------------------
# Sheet 3: 수종별_비교통계
# -------------------------------------------------------------
ws3 = wb.create_sheet(title="수종별_비교통계")
ws3.views.sheetView[0].showGridLines = True

sp_cols = ["수종분류", "포함지점", "2026-04-15", "2026-04-29", "2026-07-27", "2026-08-13", "전체평균", "표준편차", "8월/4월 배율", "대조구 대비 배율(전체)"]
for c_i, h in enumerate(sp_cols, 1):
    c = ws3.cell(1, c_i, h)
    c.fill = header_fill
    c.font = header_font
    c.alignment = center_align
    c.border = thin_border

species_info = [
    ("버드나무류", "버드나무림 a, 버드나무림 b"),
    ("소나무류", "소나무림, 리기다소나무림"),
    ("낙엽송(일본잎갈나무)", "일본잎갈나무림 a, 일본잎갈나무림 b"),
    ("잣나무류", "잣나무림 a, 잣나무림 b"),
    ("대조구", "밭(대조구), 주차장(대조구)")
]

control_overall_mean = valid_df[valid_df['species_group'] == '대조구']['ion_value'].mean()

for r_i, (sp, sites_str) in enumerate(species_info, 2):
    sp_data = valid_df[valid_df['species_group'] == sp]
    d_means = [sp_data[sp_data['date'] == d]['ion_value'].mean() for d in dates]
    tot_mean = sp_data['ion_value'].mean()
    tot_std = sp_data['ion_value'].std()
    ratio_aug_apr = d_means[3] / d_means[0]
    ratio_to_ctrl = tot_mean / control_overall_mean
    
    r_vals = [sp, sites_str] + d_means + [tot_mean, tot_std, ratio_aug_apr, ratio_to_ctrl]
    for c_i, val in enumerate(r_vals, 1):
        cell = ws3.cell(r_i, c_i, val)
        cell.font = regular_font
        cell.border = thin_border
        if c_i == 1:
            cell.alignment = center_align
            cell.font = bold_font
        elif c_i == 2:
            cell.alignment = left_align
        elif c_i in [9, 10]:
            cell.alignment = right_align
            cell.number_format = "0.00\"배\""
        else:
            cell.alignment = right_align
            cell.number_format = "#,##0.0"

for col in ws3.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = get_column_letter(col[0].column)
    ws3.column_dimensions[col_letter].width = max(max_len + 4, 14)

# -------------------------------------------------------------
# Sheet 4: 1분단위_구간평균 (Minute-by-minute session averages)
# -------------------------------------------------------------
ws4 = wb.create_sheet(title="1분단위_구간평균")
ws4.views.sheetView[0].showGridLines = True

min_headers = ["조사일자", "지점번호", "지점명"] + [f"{m}분" for m in range(1, 16)] + ["15분평균", "최초1분", "최종1분", "구간변화율"]
for c_i, h in enumerate(min_headers, 1):
    c = ws4.cell(1, c_i, h)
    c.fill = header_fill
    c.font = header_font
    c.alignment = center_align
    c.border = thin_border

r_i = 2
for (d, s_id, s_name), grp in df.groupby(['date', 'site_id', 'site_name']):
    m_means = [grp[grp['minute_bucket'] == m]['ion_value'].mean() for m in range(1, 16)]
    overall_m = np.nanmean(m_means)
    m1 = m_means[0]
    m15 = m_means[14]
    chg = (m15 - m1) / m1 * 100 if m1 > 0 else 0
    
    r_vals = [d, s_id, s_name] + m_means + [overall_m, m1, m15, chg]
    for c_i, val in enumerate(r_vals, 1):
        cell = ws4.cell(r_i, c_i, val)
        cell.font = regular_font
        cell.border = thin_border
        if c_i in [1, 2]:
            cell.alignment = center_align
        elif c_i == 3:
            cell.alignment = left_align
        elif c_i == 22:
            cell.alignment = right_align
            cell.number_format = "+0.0\"%\";-0.0\"%\";0.0\"%\""
        else:
            cell.alignment = right_align
            cell.number_format = "#,##0.0"
    r_i += 1

for col in ws4.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = get_column_letter(col[0].column)
    ws4.column_dimensions[col_letter].width = max(max_len + 3, 10)

# -------------------------------------------------------------
# Sheet 5: 전체원천데이터 (All 36,000 observations)
# -------------------------------------------------------------
ws5 = wb.create_sheet(title="전체원천데이터")
raw_headers = ["조사일자", "지점번호", "지점명", "수종구분", "산림여부", "경과초(0~899)", "1분구간(1~15)", "측정일시", "음이온발생량", "유효성"]
for c_i, h in enumerate(raw_headers, 1):
    c = ws5.cell(1, c_i, h)
    c.fill = header_fill
    c.font = header_font
    c.alignment = center_align

raw_rows = []
for _, row in df.iterrows():
    raw_rows.append([
        row['date'], int(row['site_id']), row['site_name'], row['site_type'],
        "산림" if row['is_forest'] else "대조구", int(row['second_offset']), int(row['minute_bucket']),
        row['timestamp'], row['ion_value'] if row['is_valid'] else row['ion_raw'], "유효" if row['is_valid'] else "결측/문자"
    ])

for r in raw_rows:
    ws5.append(r)

ws5.auto_filter.ref = f"A1:J{len(raw_rows) + 1}"

# Save workbook
wb.save(out_file)
print(f"Successfully generated Excel report with raw data: {out_file}")
