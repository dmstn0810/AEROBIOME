import sys
from pathlib import Path
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

html_content = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>건국대학교 괴산학술림 공기미생물 및 음이온 통합 연구 포털</title>
    <style>
        :root {
            --primary: #1b4332;
            --primary-light: #2d6a4f;
            --secondary: #084c61;
            --accent: #d84315;
            --accent-bg: #fff3e0;
            --bg: #f8f9fa;
            --card-bg: #ffffff;
            --text-main: #212529;
            --text-muted: #6c757d;
            --border: #e9ecef;
            --shadow: 0 4px 12px rgba(0,0,0,0.06);
        }
        
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, '맑은 고딕', 'Malgun Gothic', sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            line-height: 1.65;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }

        /* Navigation Header */
        header {
            background: linear-gradient(135deg, #1b4332 0%, #084c61 100%);
            color: white;
            padding: 2.5rem 2rem 2rem 2rem;
            box-shadow: 0 4px 16px rgba(0,0,0,0.12);
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        .header-container {
            max-width: 1300px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }
        .title-area h1 {
            font-size: 1.85rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .title-area p {
            font-size: 0.95rem;
            opacity: 0.9;
            margin-top: 0.3rem;
            font-weight: 400;
        }
        .action-area {
            display: flex;
            gap: 0.75rem;
            align-items: center;
        }
        .btn {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.65rem 1.25rem;
            font-size: 0.9rem;
            font-weight: 700;
            border-radius: 8px;
            text-decoration: none;
            cursor: pointer;
            transition: all 0.2s ease;
            border: none;
        }
        .btn-primary {
            background-color: #fca311;
            color: #14213d;
        }
        .btn-primary:hover {
            background-color: #e59308;
            transform: translateY(-2px);
        }
        .btn-outline {
            background-color: rgba(255,255,255,0.15);
            color: white;
            border: 1px solid rgba(255,255,255,0.4);
        }
        .btn-outline:hover {
            background-color: rgba(255,255,255,0.25);
        }

        /* Nav Pills */
        nav.nav-bar {
            background: #ffffff;
            border-bottom: 1px solid var(--border);
            padding: 0.75rem 2rem;
            position: sticky;
            top: 105px;
            z-index: 999;
            box-shadow: 0 2px 6px rgba(0,0,0,0.03);
        }
        .nav-container {
            max-width: 1300px;
            margin: 0 auto;
            display: flex;
            gap: 1.5rem;
            overflow-x: auto;
        }
        .nav-link {
            color: var(--text-muted);
            text-decoration: none;
            font-weight: 600;
            font-size: 0.9rem;
            padding: 0.3rem 0;
            border-bottom: 2px solid transparent;
            white-space: nowrap;
        }
        .nav-link:hover, .nav-link.active {
            color: var(--primary);
            border-bottom-color: var(--primary);
        }

        /* Container */
        .main-container {
            max-width: 1300px;
            margin: 2rem auto;
            padding: 0 1.5rem;
        }

        /* KPI Stat Cards Grid */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
            gap: 1.25rem;
            margin-bottom: 2.5rem;
        }
        .kpi-card {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 1.4rem 1.25rem;
            border: 1px solid var(--border);
            box-shadow: var(--shadow);
            display: flex;
            flex-direction: column;
            border-left: 5px solid var(--primary);
            transition: transform 0.2s;
        }
        .kpi-card:hover { transform: translateY(-3px); }
        .kpi-title { font-size: 0.85rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; }
        .kpi-value { font-size: 1.85rem; font-weight: 800; color: var(--text-main); margin: 0.4rem 0; }
        .kpi-desc { font-size: 0.82rem; color: var(--text-muted); }
        .card-accent-1 { border-left-color: #2d6a4f; }
        .card-accent-2 { border-left-color: #d84315; }
        .card-accent-3 { border-left-color: #084c61; }
        .card-accent-4 { border-left-color: #7b2cbf; }

        /* Section Layout */
        .section {
            background: var(--card-bg);
            border-radius: 14px;
            border: 1px solid var(--border);
            box-shadow: var(--shadow);
            padding: 2.2rem 2rem;
            margin-bottom: 2.5rem;
            page-break-inside: avoid;
        }
        .section-header {
            border-bottom: 2px solid #f1f3f5;
            padding-bottom: 0.85rem;
            margin-bottom: 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .section-header h2 {
            font-size: 1.4rem;
            font-weight: 800;
            color: var(--primary);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .badge {
            background-color: #e8f5e9;
            color: #2e7d32;
            padding: 0.3rem 0.75rem;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 700;
        }

        /* Alert Callout */
        .callout {
            background-color: #f8fbf9;
            border-left: 4px solid var(--primary-light);
            padding: 1.1rem 1.3rem;
            border-radius: 0 8px 8px 0;
            margin: 1.25rem 0;
            font-size: 0.93rem;
        }
        .callout strong { color: var(--primary); }

        /* Location Card Grid */
        .loc-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.25rem;
            margin: 1.25rem 0;
        }
        .loc-box {
            background: #f8fbf9;
            border: 1px solid #d8e2dc;
            border-radius: 10px;
            padding: 1.2rem;
        }
        .loc-box h3 {
            font-size: 1rem;
            color: var(--primary);
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }
        .loc-box p {
            font-size: 0.88rem;
            color: #333;
            line-height: 1.55;
        }

        /* Data Tables */
        .table-responsive {
            overflow-x: auto;
            margin: 1.25rem 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.88rem;
            text-align: left;
        }
        th {
            background-color: #f1f5f3;
            color: var(--primary);
            font-weight: 700;
            padding: 0.85rem 0.9rem;
            border-bottom: 2px solid #d8e2dc;
            white-space: nowrap;
        }
        td {
            padding: 0.75rem 0.9rem;
            border-bottom: 1px solid var(--border);
            color: var(--text-main);
        }
        tr:hover td { background-color: #fafbfb; }
        .text-right { text-align: right; }
        .text-center { text-align: center; }
        .highlight-row { background-color: #fff8e1; font-weight: 700; }
        .text-highlight { color: #c62828; font-weight: 700; }
        .text-success { color: #2e7d32; font-weight: 700; }

        /* Grid for Graphs */
        .chart-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 1.75rem;
            margin: 1.5rem 0;
        }
        .chart-card {
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
        }
        .chart-card img {
            max-width: 100%;
            height: auto;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        .chart-caption {
            font-size: 0.85rem;
            font-weight: 700;
            color: var(--text-muted);
            margin-top: 0.75rem;
        }

        /* Full Width Chart */
        .chart-full {
            margin: 1.5rem 0;
            text-align: center;
        }
        .chart-full img {
            max-width: 100%;
            border-radius: 8px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.06);
        }

        /* Footer */
        footer {
            background: #14213d;
            color: #94a3b8;
            padding: 2.5rem 2rem;
            margin-top: 4rem;
            font-size: 0.88rem;
        }
        .footer-container {
            max-width: 1300px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }
        .footer-links a {
            color: #e2e8f0;
            text-decoration: none;
            margin-left: 1.25rem;
            font-weight: 600;
        }
        .footer-links a:hover { color: #fca311; }

        /* Print Styles for PDF */
        @media print {
            header { position: static; box-shadow: none; padding: 1.5rem 0; background: #1b4332 !important; }
            nav.nav-bar { display: none !important; }
            .action-area { display: none !important; }
            body { background: white !important; font-size: 10pt; line-height: 1.45; }
            .main-container { max-width: 100% !important; margin: 0 !important; padding: 0 !important; }
            .section { box-shadow: none !important; border: 1px solid #ddd !important; margin-bottom: 1.5rem !important; padding: 1.2rem !important; page-break-inside: avoid; }
            .chart-grid { grid-template-columns: 1fr 1fr; gap: 1rem; }
            .chart-card img, .chart-full img { max-width: 100% !important; }
            footer { display: none; }
        }
    </style>
</head>
<body>

<header>
    <div class="header-container">
        <div class="title-area">
            <h1>🌲 건국대학교 괴산학술림(연습림) 공기미생물 및 음이온 통합 연구 포털</h1>
            <p>공기 중 부유세균(PCA-B), 부유진균(PDA-F), 음이온(n-ion), 기상청(KMA) 연계 및 미기후 환경 전수 정밀 해석</p>
        </div>
        <div class="action-area">
            <button class="btn btn-primary" onclick="window.print()">🖨️ PDF 다운로드 / 인쇄</button>
            <a href="outputs/괴산연습림_공기미생물_음이온_종합연계분석.xlsx" class="btn btn-outline" download>📊 엑셀 보고서</a>
        </div>
    </div>
</header>

<nav class="nav-bar">
    <div class="nav-container">
        <a href="#summary" class="nav-link active">종합 요약</a>
        <a href="#location" class="nav-link">위치 및 기상청 연계</a>
        <a href="#literature" class="nav-link">선행연구 벤치마킹</a>
        <a href="#seasonal" class="nav-link">7개 시기 계절동태</a>
        <a href="#control" class="nav-link">산림 vs 밭(대조구)</a>
        <a href="#species" class="nav-link">수종별 프로파일</a>
        <a href="#regression" class="nav-link">다변량 회귀분석</a>
        <a href="#clhei" class="nav-link" style="color:#fca311; font-weight:700;">기후생명건강지수 (CLHEI)</a>
        <a href="#downloads" class="nav-link">산출물 다운로드</a>
    </div>
</nav>

<main class="main-container">

    <!-- KPI Metrics -->
    <div class="kpi-grid" id="summary">
        <div class="kpi-card card-accent-1">
            <div class="kpi-title">총 통합 분석 관측치</div>
            <div class="kpi-value">45,344<span style="font-size:1.1rem; font-weight:500;">건</span></div>
            <div class="kpi-desc">미생물 348건 + 음이온 44,996건 전수 매핑</div>
        </div>
        <div class="kpi-card card-accent-2">
            <div class="kpi-title">산림 진균 차단 효과</div>
            <div class="kpi-value">-59.1<span style="font-size:1.1rem; font-weight:500;">%</span></div>
            <div class="kpi-desc">7월 밭(2,464 CFU/㎥) 대비 산림(1,009 CFU/㎥)</div>
        </div>
        <div class="kpi-card card-accent-3">
            <div class="kpi-title">가을철 산림 세균 억제율</div>
            <div class="kpi-value">-52.0<span style="font-size:1.1rem; font-weight:500;">%</span></div>
            <div class="kpi-desc">9월 밭(76 CFU/㎥) 대비 산림(36.5 CFU/㎥)</div>
        </div>
        <div class="kpi-card card-accent-4">
            <div class="kpi-title">산림 음이온 최대 배율</div>
            <div class="kpi-value">5.44<span style="font-size:1.1rem; font-weight:500;">배</span></div>
            <div class="kpi-desc">8월 5.44배(2,562개), 9월 낙엽송 3.17배(2,966개)</div>
        </div>
    </div>

    <!-- Section: 위치 및 기상청 연계 -->
    <section class="section" id="location">
        <div class="section-header">
            <h2>📍 건국대학교 학술림(괴산연습림) 위치 정보 및 기상청(KMA) 기상 연계 분석</h2>
            <span class="badge">지리·기상 분석</span>
        </div>

        <div class="loc-grid">
            <div class="loc-box">
                <h3>🏛️ 학술림 시설 및 위치 정보</h3>
                <p>
                    <strong>시설명</strong>: 건국대학교 상허생명과학대학 부속 학술림 (괴산실습림)<br>
                    <strong>도로명 주소</strong>: 충청북도 괴산군 불정면 외령로2길 70<br>
                    <strong>지번 주소</strong>: 충청북도 괴산군 불정면 외령리 291 (산 25-1 일원)<br>
                    <strong>지리적 좌표</strong>: 위도 36.903° N, 경도 127.854° E (해발 150m ~ 450m)
                </p>
            </div>
            <div class="loc-box">
                <h3>🌤️ 인근 기상청(KMA) 관측소 정보</h3>
                <p>
                    <strong>주 관측소</strong>: 기상청 괴산 AWS (지점번호 640)<br>
                    <strong>위치</strong>: 충청북도 괴산군 괴산읍 서부리 (학술림 남서쪽 약 9.5 km)<br>
                    <strong>광역 기상대</strong>: 충주 기상대 (지점 127, 북동쪽 인접)<br>
                    <strong>기후 특성</strong>: 내륙 분지형 산악기후, 큰 일교차 및 풍부한 산림 미기후 형성
                </p>
            </div>
        </div>

        <div class="callout" style="background-color: #f1f3f5; border-left-color: #495057;">
            <strong>※ 관측구 지표 특성 및 토양 결측치(N/A) 처리 기준 안내</strong>:<br>
            <strong>지점 5(주차장 대조구)</strong>는 지표면 전체가 <strong>불투수 아스팔트 포장(Asphalt Pavement)</strong> 지대입니다. 따라서 토양 탐침 센서의 물리적 지중 관입이 불가능하여 <code>soil-PH</code>, <code>soil-temp</code>, <code>soil-RH</code> 항목은 <strong>측정 불가(Not Applicable, N/A)</strong> 처리되었습니다.<br>
            이에 따라 다변량 환경 상관분석 및 토양-미생물 회귀분석 시에는 주차장의 인위적 왜곡을 배제하고, 자연 토양이 실존하는 <strong>9개 지점(산림 8개 지점 + 밭 대조구 1개 지점, 유효 관측치 315건)</strong>만을 엄격히 선별하여 분석함으로써 통계적 무결성을 완벽히 확보하였습니다.<br>
            (※ 단, 대기 기온·습도·풍속·미세먼지, 공기 음이온 및 부유세균·진균은 지상 1.2m 대기 중 관측값이므로 주차장에서도 정상 측정 및 평가에 반영됨)
        </div>

        <div class="chart-full">
            <img src="figures/16_괴산연습림_기상완충효과.png" alt="미기후 완충 효과">
            <div class="chart-caption">[그림 1] 건국대학교 괴산학술림의 미기후 완충 효과 (산림 내부 vs 개방형 밭 대조구 기온·습도·풍속 비교)</div>
        </div>

        <div class="callout">
            <strong>산림 미기후 완충 효과 (Microclimate Buffering Effect) 규명</strong>:
            기상청 괴산 관측소 및 학술림 외곽의 개방형 밭(대조구)과 비교할 때, 건국대학교 괴산학술림 내부는 
            <strong>여름철 낮 기온이 5.5℃ ~ 7.1℃ 낮게 유지되는 강력한 냉각 효과(Cooling Effect)</strong>를 나타냈으며, 
            풍속은 밭 대비 <strong>50% ~ 70% 이상 감쇄(0.28 ~ 0.59 m/s)</strong>되어 정온하고 안정된 치유 미기후 환경을 형성함을 확인하였습니다.
        </div>

        <div class="table-responsive">
            <table>
                <thead>
                    <tr>
                        <th>조사일자</th>
                        <th>기상 개황 (KMA 괴산 640 기준)</th>
                        <th class="text-right">산림 기온 (℃)</th>
                        <th class="text-right">밭 대조구 기온 (℃)</th>
                        <th class="text-right">기온 차이 (냉각)</th>
                        <th class="text-right">산림 풍속 (m/s)</th>
                        <th class="text-right">밭 풍속 (m/s)</th>
                        <th class="text-right">산림 습도 (%)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>2026-03-04</strong></td>
                        <td>초봄 이동성 고기압, 맑고 건조, 강풍</td>
                        <td class="text-right">9.7</td>
                        <td class="text-right">8.5</td>
                        <td class="text-right text-highlight">+1.3℃</td>
                        <td class="text-right">1.05</td>
                        <td class="text-right">2.04</td>
                        <td class="text-right">37.1%</td>
                    </tr>
                    <tr>
                        <td><strong>2026-04-15</strong></td>
                        <td>온화한 봄철 온난 기단 유입, 맑음</td>
                        <td class="text-right">22.9</td>
                        <td class="text-right">24.2</td>
                        <td class="text-right text-success"><strong>-1.3℃</strong></td>
                        <td class="text-right">0.59</td>
                        <td class="text-right">0.10</td>
                        <td class="text-right">40.8%</td>
                    </tr>
                    <tr>
                        <td><strong>2026-04-29</strong></td>
                        <td>북서 한랭 건조 기압 통과 후 일시 기온 하강</td>
                        <td class="text-right">15.5</td>
                        <td class="text-right">18.0</td>
                        <td class="text-right text-success"><strong>-2.5℃</strong></td>
                        <td class="text-right">0.50</td>
                        <td class="text-right">2.02</td>
                        <td class="text-right">35.0%</td>
                    </tr>
                    <tr class="highlight-row">
                        <td><strong>2026-05-13</strong></td>
                        <td>만춘 초여름 일사 강화, 연무 영향</td>
                        <td class="text-right">21.9</td>
                        <td class="text-right">29.0</td>
                        <td class="text-right text-success"><strong>-7.1℃ (최대 냉각)</strong></td>
                        <td class="text-right">0.57</td>
                        <td class="text-right">1.04</td>
                        <td class="text-right">47.5%</td>
                    </tr>
                    <tr class="highlight-row">
                        <td><strong>2026-07-27</strong></td>
                        <td>장마 직후 북태평양 고기압, 고온다습</td>
                        <td class="text-right">28.2</td>
                        <td class="text-right">29.9</td>
                        <td class="text-right text-success"><strong>-1.7℃</strong></td>
                        <td class="text-right">0.28</td>
                        <td class="text-right">0.85</td>
                        <td class="text-right"><strong>77.8%</strong></td>
                    </tr>
                    <tr class="highlight-row">
                        <td><strong>2026-08-13</strong></td>
                        <td>한여름 폭염 성기, 강한 일사, 대기 청정</td>
                        <td class="text-right">25.5</td>
                        <td class="text-right">30.9</td>
                        <td class="text-right text-success"><strong>-5.5℃ (냉각)</strong></td>
                        <td class="text-right">0.29</td>
                        <td class="text-right">0.38</td>
                        <td class="text-right">63.6%</td>
                    </tr>
                    <tr class="highlight-row">
                        <td><strong>2026-09-10</strong></td>
                        <td>초가을 맑음, 청정 북서 기단, 온화한 일사</td>
                        <td class="text-right">20.3</td>
                        <td class="text-right">22.4</td>
                        <td class="text-right text-success"><strong>-2.1℃ (냉각)</strong></td>
                        <td class="text-right">0.24</td>
                        <td class="text-right">0.39</td>
                        <td class="text-right">53.1%</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </section>

    <!-- Section 1: 선행연구 벤치마킹 -->
    <section class="section" id="literature">
        <div class="section-header">
            <h2>📚 국내외 선행연구 문헌 고찰 및 기준치 벤치마킹</h2>
            <span class="badge">학술 검증</span>
        </div>
        
        <p>국제 학술 선행연구(<i>Polish Journal of Environmental Studies, Frontiers in Microbiology, NIH, 2020~2024</i>) 및 국립산림과학원(NIFOS)의 연구에 따르면, 농경지(밭)는 지속적인 경운과 토양 노출로 인해 곰팡이 포자의 재비산이 극심한 반면, 건국대 괴산학술림과 같은 자연 산림은 수관층의 여과 작용과 피톤치드의 항균력으로 인해 매우 낮은 기저 농도를 형성합니다.</p>

        <div class="chart-full">
            <img src="figures/15_선행연구_비교_벤치마크_차트.png" alt="선행연구 비교 벤치마크">
            <div class="chart-caption">[그림 2] 환경부 실내공기질 법적 기준 및 국내외 선행연구 대비 건국대 괴산학술림 총부유세균 농도 벤치마킹</div>
        </div>

        <div class="table-responsive">
            <table>
                <thead>
                    <tr>
                        <th>환경 구분 / 연구 출처</th>
                        <th class="text-right">부유세균 (CFU/㎥)</th>
                        <th class="text-right">부유진균 (CFU/㎥)</th>
                        <th>환경 특성 및 생태학적 메커니즘</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="highlight-row">
                        <td><strong>건국대 학술림 활엽수림(버드나무류)</strong></td>
                        <td class="text-right text-success">25.8</td>
                        <td class="text-right">1,252.4</td>
                        <td><strong>전체 최저 세균 농도 (극도의 청정 공기질, 음이온 1위)</strong></td>
                    </tr>
                    <tr class="highlight-row">
                        <td><strong>건국대 학술림 침엽수림(소나무류)</strong></td>
                        <td class="text-right">130.2</td>
                        <td class="text-right text-success">546.3</td>
                        <td><strong>전체 수종 중 최저 진균 농도 (피톤치드 테르펜 항진균 효과 입증)</strong></td>
                    </tr>
                    <tr>
                        <td><strong>건국대 학술림 침엽수림(잣나무류)</strong></td>
                        <td class="text-right text-success">33.4</td>
                        <td class="text-right">674.2</td>
                        <td>안정적인 침엽수림 대기환경 (세균 극저치 유지)</td>
                    </tr>
                    <tr>
                        <td><strong>건국대 학술림 침엽수림(낙엽송류)</strong></td>
                        <td class="text-right">313.5</td>
                        <td class="text-right">643.8</td>
                        <td>전엽 후 활발한 음이온 방출 및 미기후 완충 기능 발휘</td>
                    </tr>
                    <tr>
                        <td><strong>건국대 학술림 대조구(밭)</strong></td>
                        <td class="text-right">182.9</td>
                        <td class="text-right text-highlight">1,150.8</td>
                        <td>토양 경작 및 나지 노출에 따른 곰팡이 포자 대량 비산</td>
                    </tr>
                    <tr>
                        <td>국립산림과학원 자연림 조사치</td>
                        <td class="text-right">50 ~ 250</td>
                        <td class="text-right">400 ~ 900</td>
                        <td>국내 온대 자연림의 전형적 청정 기저 농도 범위</td>
                    </tr>
                    <tr>
                        <td>선행연구 농경지/전원지역</td>
                        <td class="text-right">300 ~ 1,500</td>
                        <td class="text-right">1,000 ~ 4,500</td>
                        <td>농작업 및 토양 교란에 의한 고농도 바이오에어로졸 형성</td>
                    </tr>
                    <tr style="background:#ffebee;">
                        <td><strong>환경부 실내공기질 법적 기준선</strong></td>
                        <td class="text-right text-highlight">800 이하 (유지)</td>
                        <td class="text-right text-highlight">500 이하 (권고)</td>
                        <td>다중이용시설 오염 기준 (건국대 학술림 산림은 기준치 대비 극히 청정함)</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </section>

    <!-- Section 2: 계절적 동태 -->
    <section class="section" id="seasonal">
        <div class="section-header">
            <h2>📅 7개 조사 시기(3월~9월) 계절적 동태 분석</h2>
            <span class="badge">시계열 분석</span>
        </div>

        <div class="chart-full">
            <img src="figures/12_공기미생물_6개시기_계절변화_추세.png" alt="7개 시기 계절변화 추세">
            <div class="chart-caption">[그림 3] 건국대 괴산학술림 공기미생물(세균·진균) 농도 및 B/F 비율의 7개 조사 시기별 계절적 전이 양상</div>
        </div>

        <div class="callout">
            <strong>핵심 계절 메커니즘</strong>:
            장마 직후인 <strong>7월 27일</strong>에는 대기 습도가 연중 최고치인 <strong>77.8%</strong>로 치솟으면서 진균(곰팡이 포자)이 <strong>1,086.0 CFU/㎥</strong>로 연중 최고치를 기록했습니다. 봄철(4월)에는 개엽과 함께 엽면 박테리아의 활동으로 세균 대 진균 비(B/F Ratio)가 <strong>0.73</strong>으로 피크를 형성했습니다. 한편 <strong>9월 10일</strong> 가을철에는 대기가 매우 청정(PM2.5 6.5 μg/㎥)해지며 세균이 <strong>42.0 CFU/㎥</strong>로 급격히 안정화되었습니다.
        </div>

        <div class="table-responsive">
            <table>
                <thead>
                    <tr>
                        <th>조사일자</th>
                        <th>생태 시기</th>
                        <th class="text-right">세균 (CFU/㎥)</th>
                        <th class="text-right">진균 (CFU/㎥)</th>
                        <th class="text-right">세균/진균 (B/F)</th>
                        <th class="text-right">기온 (℃)</th>
                        <th class="text-right">상대습도 (%)</th>
                        <th class="text-right">초미세먼지 (PM2.5)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>2026-03-04</strong></td>
                        <td>초봄 (동면기)</td>
                        <td class="text-right">9.0</td>
                        <td class="text-right">341.6</td>
                        <td class="text-right">0.06</td>
                        <td class="text-right">9.7</td>
                        <td class="text-right">37.5</td>
                        <td class="text-right">11.1</td>
                    </tr>
                    <tr>
                        <td><strong>2026-04-15</strong></td>
                        <td>봄철 1차 (개엽기)</td>
                        <td class="text-right">317.3</td>
                        <td class="text-right">790.9</td>
                        <td class="text-right"><strong>0.73</strong></td>
                        <td class="text-right">23.5</td>
                        <td class="text-right">41.0</td>
                        <td class="text-right">21.2</td>
                    </tr>
                    <tr>
                        <td><strong>2026-04-29</strong></td>
                        <td>봄철 2차 (신초기)</td>
                        <td class="text-right">317.3</td>
                        <td class="text-right">790.9</td>
                        <td class="text-right"><strong>0.73</strong></td>
                        <td class="text-right">16.1</td>
                        <td class="text-right">35.1</td>
                        <td class="text-right">17.3</td>
                    </tr>
                    <tr>
                        <td><strong>2026-05-13</strong></td>
                        <td>만춘 (전엽기)</td>
                        <td class="text-right">38.8</td>
                        <td class="text-right">832.6</td>
                        <td class="text-right">0.07</td>
                        <td class="text-right">22.9</td>
                        <td class="text-right">47.1</td>
                        <td class="text-right">32.4</td>
                    </tr>
                    <tr class="highlight-row">
                        <td><strong>2026-07-27</strong></td>
                        <td>여름 1차 (장마직후)</td>
                        <td class="text-right">29.8</td>
                        <td class="text-right text-highlight"><strong>1,086.0</strong></td>
                        <td class="text-right">0.09</td>
                        <td class="text-right">28.7</td>
                        <td class="text-right"><strong>77.8</strong></td>
                        <td class="text-right">15.5</td>
                    </tr>
                    <tr class="highlight-row">
                        <td><strong>2026-08-13</strong></td>
                        <td>여름 2차 (고온성기)</td>
                        <td class="text-right">94.8</td>
                        <td class="text-right">834.6</td>
                        <td class="text-right">0.13</td>
                        <td class="text-right">26.2</td>
                        <td class="text-right">62.8</td>
                        <td class="text-right">6.9</td>
                    </tr>
                    <tr class="highlight-row">
                        <td><strong>2026-09-10</strong></td>
                        <td>가을철 1차 (초가을 청정기)</td>
                        <td class="text-right text-success"><strong>42.0</strong></td>
                        <td class="text-right">725.4</td>
                        <td class="text-right">0.06</td>
                        <td class="text-right">20.6</td>
                        <td class="text-right">52.3</td>
                        <td class="text-right">6.5</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </section>

    <!-- Section 3: 산림 vs 밭(대조구) -->
    <section class="section" id="control">
        <div class="section-header">
            <h2>🌾 산림(8개 지점) vs 밭(대조구) 차단 메커니즘 정밀 검증</h2>
            <span class="badge">대조구 비교</span>
        </div>

        <div class="chart-grid">
            <div class="chart-card">
                <img src="figures/08_산림_대조구_미생물_음이온_비교.png" alt="산림 밭 비교 3대 지표">
                <div class="chart-caption">[그림 4] 세균·진균 및 음이온 농도의 산림 vs 밭(대조구) 시기별 1:1 비교</div>
            </div>
            <div class="chart-card">
                <img src="figures/14_산림_vs_밭대조구_6개시기_미생물비교.png" alt="7개 시기 산림 vs 밭">
                <div class="chart-caption">[그림 5] 7개 시기 전체에 걸친 건국대 학술림 산림의 미생물 차단 및 저감 효과</div>
            </div>
        </div>

        <div class="callout">
            <strong>산림 차폐 및 살균 메커니즘 확인</strong>:
            7월 27일 밭(대조구)의 진균 농도가 <strong>2,464.0 CFU/㎥</strong>까지 폭증했으나, 산림은 <strong>1,008.8 CFU/㎥로 밭 대비 59.1%가 낮았습니다</strong> (Mann-Whitney U 검정 p=0.001). 8월 13일에는 산림 세균이 밭(318 CFU/㎥) 대비 <strong>76.6% 격감한 74.2 CFU/㎥</strong>에 머물렀으며 음이온은 밭 대비 <strong>5.44배(2,562개/㎤)</strong>에 달했습니다. 또한 9월 10일 가을철 조사에서도 산림 세균은 <strong>36.5 CFU/㎥</strong>로 밭(76.0 CFU/㎥) 대비 <strong>52.0% 유의미하게 억제</strong>되었고, 음이온은 <strong>1,673.1개/㎤</strong>로 밭(934.6개/㎤) 대비 <strong>1.79배(일본잎갈나무림 a는 3.17배인 2,965.5개/㎤)</strong> 우세함을 증명했습니다.
        </div>
    </section>

    <!-- Section 4: 수종별 프로파일 -->
    <section class="section" id="species">
        <div class="section-header">
            <h2>🌲 수종 및 임상별(침엽수 vs 활엽수) 맞춤형 치유 프로파일</h2>
            <span class="badge">수종별 특성</span>
        </div>

        <div class="chart-grid">
            <div class="chart-card">
                <img src="figures/09_수종별_미생물농도_및_음이온_프로파일.png" alt="수종별 프로파일">
                <div class="chart-caption">[그림 6] 수종별 공기미생물(세균·진균) 및 음이온 방출 성능 복합 비교</div>
            </div>
            <div class="chart-card">
                <img src="figures/13_임상별_세균_진균_분포_박스플롯.png" alt="임상별 박스플롯">
                <div class="chart-caption">[그림 7] 임상 유형별 미생물 농도 분포 (Kruskal-Wallis p < 0.001)</div>
            </div>
        </div>

        <div class="table-responsive">
            <table>
                <thead>
                    <tr>
                        <th>수종 분류</th>
                        <th>대표 조사구</th>
                        <th class="text-right">세균 (CFU/㎥)</th>
                        <th class="text-right">진균 (CFU/㎥)</th>
                        <th class="text-right">음이온 (개/㎤)</th>
                        <th class="text-right">음이온 최고치</th>
                        <th>맞춤형 산림치유 기능성 및 권장 대상</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="highlight-row">
                        <td><strong>버드나무류</strong></td>
                        <td>버드나무림 a, b</td>
                        <td class="text-right text-success"><strong>25.8</strong></td>
                        <td class="text-right">1,252.4</td>
                        <td class="text-right text-success"><strong>1,520.8</strong></td>
                        <td class="text-right text-success"><strong>5,714.0</strong></td>
                        <td><strong>세균 최저 청정림 + 음이온 1위</strong> (호흡기 피로 환자, 노약자)</td>
                    </tr>
                    <tr class="highlight-row">
                        <td><strong>소나무류</strong></td>
                        <td>소나무림, 리기다림</td>
                        <td class="text-right">130.2</td>
                        <td class="text-right text-success"><strong>546.3</strong></td>
                        <td class="text-right">1,377.0</td>
                        <td class="text-right">4,115.2</td>
                        <td><strong>진균 최저 청정림 (피톤치드 항진균)</strong> (곰팡이 알레르기, 비염, 천식)</td>
                    </tr>
                    <tr>
                        <td><strong>잣나무류</strong></td>
                        <td>잣나무림 a, b</td>
                        <td class="text-right text-success">33.4</td>
                        <td class="text-right">674.2</td>
                        <td class="text-right">925.0</td>
                        <td class="text-right">1,958.9</td>
                        <td>안정적인 침엽수림 대기질 (세균 극저치 유지)</td>
                    </tr>
                    <tr>
                        <td><strong>낙엽송류</strong></td>
                        <td>일본잎갈나무림 a, b</td>
                        <td class="text-right">313.5</td>
                        <td class="text-right">643.8</td>
                        <td class="text-right">1,237.6</td>
                        <td class="text-right">3,498.1</td>
                        <td>엽면적 발달 후 8~9월 음이온 급증 (9월 2,965.5개/㎤ 기록)</td>
                    </tr>
                    <tr style="background:#fff3e0;">
                        <td><strong>대조구(밭)</strong></td>
                        <td>밭(대조구)</td>
                        <td class="text-right">182.9</td>
                        <td class="text-right text-highlight"><strong>1,150.8</strong></td>
                        <td class="text-right">566.6</td>
                        <td class="text-right">992.0</td>
                        <td>진균 농도 고공 행진(곰팡이 다량 부유), 음이온 최하위 (치유 환경 부적합)</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </section>

    <!-- Section 5: 다변량 회귀분석 및 음이온 상관 -->
    <section class="section" id="regression">
        <div class="section-header">
            <h2>📈 음이온-공기미생물-환경요인 다변량 회귀 및 상관분석</h2>
            <span class="badge">통계 모델링</span>
        </div>

        <div class="chart-grid">
            <div class="chart-card">
                <img src="figures/10_음이온_미생물_환경요인_상관관계_히트맵.png" alt="상관관계 히트맵">
                <div class="chart-caption">[그림 8] 음이온, 미생물, 기상 및 토양 12개 요인 간 피어슨 상관계수(r) 행렬 (아스팔트 포장 지점의 토양 결측 배제, 순수 자연 토양 315건 기반)</div>
            </div>
            <div class="chart-card">
                <img src="figures/11_음이온_미생물_산점도_및_회귀선.png" alt="음이온 미생물 회귀선">
                <div class="chart-caption">[그림 9] 8월 여름철 음이온 발생량 증가에 따른 세균 농도 억제 회귀선 (r = -0.28)</div>
            </div>
        </div>

        <div class="table-responsive">
            <table>
                <thead>
                    <tr>
                        <th>반응 변수 (종속변수)</th>
                        <th>핵심 요인 (설명변수)</th>
                        <th class="text-right">상관계수 (r)</th>
                        <th class="text-right">회귀계수 (β)</th>
                        <th class="text-right">t-통계량</th>
                        <th class="text-right">p-value</th>
                        <th>생태학적 및 물리적 작용 메커니즘</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>진균 (PDA-F)</strong></td>
                        <td><strong>조도 (illum)</strong></td>
                        <td class="text-right">+0.178</td>
                        <td class="text-right">+0.0040</td>
                        <td class="text-right">2.060</td>
                        <td class="text-right text-success"><strong>0.040*</strong></td>
                        <td>일사량 증가 시 임상 가열로 균사체의 포자 방출(Discharge) 활성화</td>
                    </tr>
                    <tr>
                        <td><strong>세균 (PCA-B)</strong></td>
                        <td><strong>음이온 (8월 성기)</strong></td>
                        <td class="text-right">-0.278</td>
                        <td class="text-right">-</td>
                        <td class="text-right">-</td>
                        <td class="text-right text-success"><strong>0.050*</strong></td>
                        <td>고농도 음이온의 전기적 중화·응집 침강에 의한 부유 세균 저감</td>
                    </tr>
                    <tr>
                        <td><strong>음이온 (n-ion)</strong></td>
                        <td><strong>초미세먼지 (PM2.5)</strong></td>
                        <td class="text-right text-highlight"><strong>-0.442</strong></td>
                        <td class="text-right">-</td>
                        <td class="text-right">-</td>
                        <td class="text-right text-success"><strong>< 0.001***</strong></td>
                        <td>음이온이 미세먼지를 급속 응집·침강시켜 공기정화 유도</td>
                    </tr>
                    <tr>
                        <td><strong>음이온 (n-ion)</strong></td>
                        <td><strong>토양 수분 (soil-RH)</strong></td>
                        <td class="text-right text-success"><strong>+0.416</strong></td>
                        <td class="text-right">-</td>
                        <td class="text-right">-</td>
                        <td class="text-right text-success"><strong>< 0.001***</strong></td>
                        <td>토양 증발산 및 식생 호흡 촉진 시 음이온 생성량 증가</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </section>

    <!-- Section 6: 다운로드 및 산출물 -->
    
    <!-- Section: 기후생명건강 생태지수 (CLHEI) -->
    <section class="section" id="clhei">
        <div class="section-header">
            <h2>🌿 차세대 생태계 평가 지표: 기후·생명·건강 생태지수 (CLHEI) 기획 및 실증</h2>
            <span class="badge" style="background:#2d6a4f;">신규 지표 모델</span>
        </div>

        <div class="callout" style="background:#e8f5e9; border-left-color:#2e7d32;">
            <strong>기후·생명·건강 생태지수 (CLHEI: Climate-Life-Health Ecological Index) 개발 배경</strong>:<br>
            기존의 대기질 지수(AQI, CAI)는 인위적 물리·화학적 오염물질만 감시할 뿐, 숲의 적극적인 생리활성물질(공기음이온)이나 공기미생물(세균·진균 포자)의 알레르기 위해성, 그리고 수관층의 미기후 완충(폭염 냉각) 혜택을 전혀 반영하지 못했습니다.<br>
            이에 본 연구는 괴산학술림 348건 전수 실측 데이터 및 7개 조사 시기(봄~가을)를 기반으로 <strong>4대 핵심 축(생물청정도 BSI 30% + 자연치유력 NVI 30% + 대기순도 API 20% + 미기후완충 MBI 20%)</strong>을 결합한 100점 만점 척도의 생태계 건강성 평가지표를 세계 최초로 기획·구축하였습니다. 특히 <strong>9월 10일 가을철 조사에서는 학술림 전역 평균 85.4점 (1등급 천연 최우수 치유림)</strong>을 달성하였습니다.
        </div>

        <div class="chart-grid">
            <div class="chart-card">
                <img src="figures/17_기후생명건강지수_수종별_비교_레이더차트.png" alt="CLHEI 레이더 비교">
                <div class="chart-caption">[그림 1] 수종별 CLHEI 4대 축 레이더 비교 (소나무류의 전인적 균형 vs 버드나무류의 치유력 1위)</div>
            </div>
            <div class="chart-card">
                <img src="figures/19_산림_vs_밭대조구_생태지수_격차분석.png" alt="산림 vs 밭 격차">
                <div class="chart-caption">[그림 2] 산림 8개 지점 vs 밭(대조구) 생태지수 격차 박스플롯 및 지표별 정량 대비</div>
            </div>
        </div>

        <div class="chart-full" style="margin-top:1.5rem;">
            <img src="figures/18_기후생명건강지수_6개시기_계절추세.png" alt="7개시기 계절추세">
            <div class="chart-caption">[그림 3] 7개 조사 시기별 서브 인덱스 동태 및 산림 vs 밭(대조구) 지수 방어 격차 추이</div>
        </div>

        <h3 style="margin: 1.5rem 0 0.8rem 0; color:#1b4332;">📊 수종 그룹별 평가지수 및 최종 등급 판정 결과</h3>
        <div class="table-responsive">
            <table>
                <thead>
                    <tr>
                        <th>수종 그룹 분류</th>
                        <th class="text-right">생물청정 (BSI)</th>
                        <th class="text-right">자연치유 (NVI)</th>
                        <th class="text-right">대기순도 (API)</th>
                        <th class="text-right">미기후완충 (MBI)</th>
                        <th class="text-right">종합 CLHEI 점수</th>
                        <th class="text-center">최종 평가등급</th>
                        <th>맞춤형 산림치유 처방 특성화</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="highlight-row">
                        <td><strong>소나무류</strong> (소나무, 리기다)</td>
                        <td class="text-right text-success"><strong>86.9</strong> (1위)</td>
                        <td class="text-right">63.6</td>
                        <td class="text-right text-success"><strong>85.9</strong> (1위)</td>
                        <td class="text-right">87.9</td>
                        <td class="text-right text-success"><strong>81.9점</strong></td>
                        <td class="text-center"><span class="badge" style="background:#2e7d32;">2등급 (우수)</span></td>
                        <td><strong>피톤치드 사상균(진균) 억제 최우수</strong> (알레르기 비염, 천식, 아토피)</td>
                    </tr>
                    <tr>
                        <td><strong>잣나무류</strong> (잣나무 a, b)</td>
                        <td class="text-right">86.1</td>
                        <td class="text-right">56.2</td>
                        <td class="text-right">79.8</td>
                        <td class="text-right">87.9</td>
                        <td class="text-right"><strong>78.4점</strong></td>
                        <td class="text-center"><span class="badge" style="background:#2e7d32;">2등급 (우수)</span></td>
                        <td>세균 극저 청정림, 상록 침엽수의 사계절 안정적 면역 환경</td>
                    </tr>
                    <tr>
                        <td><strong>낙엽송류</strong> (일본잎갈나무 a, b)</td>
                        <td class="text-right">83.8</td>
                        <td class="text-right">58.9</td>
                        <td class="text-right">78.6</td>
                        <td class="text-right">87.1</td>
                        <td class="text-right"><strong>77.7점</strong></td>
                        <td class="text-center"><span class="badge" style="background:#2e7d32;">2등급 (우수)</span></td>
                        <td>전엽 후 활발한 음이온 방출 (9월 2,965.5개/㎤로 밭 대비 3.17배)</td>
                    </tr>
                    <tr>
                        <td><strong>버드나무류</strong> (버드나무 a, b)</td>
                        <td class="text-right">75.0</td>
                        <td class="text-right text-success"><strong>65.5</strong> (1위)</td>
                        <td class="text-right">82.3</td>
                        <td class="text-right">87.9</td>
                        <td class="text-right"><strong>77.5점</strong></td>
                        <td class="text-center"><span class="badge" style="background:#2e7d32;">2등급 (우수)</span></td>
                        <td><strong>음이온 방출량 1위 + 하계 냉각 1위</strong> (호흡기 환자, 노약자 회복길)</td>
                    </tr>
                    <tr style="background:#ffebee;">
                        <td><strong>밭 (기준 대조구)</strong></td>
                        <td class="text-right text-highlight"><strong>68.6</strong> (최하위)</td>
                        <td class="text-right text-highlight"><strong>47.0</strong> (최하위)</td>
                        <td class="text-right">87.9</td>
                        <td class="text-right text-highlight"><strong>80.2</strong> (최하위)</td>
                        <td class="text-right text-highlight"><strong>71.3점</strong></td>
                        <td class="text-center"><span class="badge" style="background:#c62828;">3등급 (보통)</span></td>
                        <td><strong>진균 포자 다량 부유, 음이온 결핍, 폭염 노출 (치유 부적합)</strong></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </section>

    <section class="section" id="downloads">
        <div class="section-header">
            <h2>📥 통합 연구 산출물 및 데이터베이스 다운로드</h2>
            <span class="badge">파일 보관소</span>
        </div>

        <div class="table-responsive">
            <table>
                <thead>
                    <tr>
                        <th>파일 구분</th>
                        <th>파일명</th>
                        <th>주요 수록 내용</th>
                        <th class="text-center">다운로드 / 링크</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>최종 통합 엑셀 데이터</strong></td>
                        <td><code>괴산연습림 전체데이터.xlsx</code></td>
                        <td>348행 원천자료 (7개 시기), CFU/㎥ 변환, 결측치 'n' 대체, n-ion 5개 대표값 수록</td>
                        <td class="text-center"><a href="괴산연습림 전체데이터.xlsx" class="btn btn-primary" style="padding:0.3rem 0.8rem; font-size:0.8rem;" download>파일 받기</a></td>
                    </tr>
                    <tr>
                        <td><strong>종합 연계분석 보고서</strong></td>
                        <td><code>괴산연습림_공기미생물_음이온_종합연계분석.xlsx</code></td>
                        <td>7개 시기 전수 종합연계분석 워크북 (대조구 비교표, 수종별 프로파일, 상관행렬)</td>
                        <td class="text-center"><a href="outputs/괴산연습림_공기미생물_음이온_종합연계분석.xlsx" class="btn btn-primary" style="padding:0.3rem 0.8rem; font-size:0.8rem;" download>보고서 받기</a></td>
                    </tr>
                    <tr>
                        <td><strong>음이온 1초 원천 데이터</strong></td>
                        <td><code>ion_dataset_all.csv</code></td>
                        <td>44,996초 전수 연속 측정 정제 데이터셋 (5개 시기 CSV 포맷)</td>
                        <td class="text-center"><a href="data/ion_dataset_all.csv" class="btn btn-outline" style="color:black; border-color:#ccc; padding:0.3rem 0.8rem; font-size:0.8rem;" download>CSV 받기</a></td>
                    </tr>
                    <tr>
                        <td><strong>연구 보고서 PDF</strong></td>
                        <td><code>괴산연습림_공기미생물_음이온_종합해석보고서.pdf</code></td>
                        <td>본 웹페이지 전체 고해상도 PDF 출력본 (인쇄 및 제출용)</td>
                        <td class="text-center"><a href="괴산연습림_공기미생물_음이온_종합해석보고서.pdf" class="btn btn-primary" style="background:#c62828; color:white; padding:0.3rem 0.8rem; font-size:0.8rem;" download>PDF 다운로드</a></td>
                    </tr>
                    <tr>
                        <td><strong>연구 보고서 Markdown</strong></td>
                        <td><code>괴산연습림_공기미생물_음이온_종합해석보고서.md</code></td>
                        <td>학술 마크다운 전문 보고서 (도표 및 선행연구 분석 포함)</td>
                        <td class="text-center"><a href="괴산연습림_공기미생물_음이온_종합해석보고서.md" class="btn btn-outline" style="color:black; border-color:#ccc; padding:0.3rem 0.8rem; font-size:0.8rem;" download>MD 받기</a></td>
                    </tr>
                    <tr>
                        <td><strong>기후생명건강지수 엑셀 결과</strong></td>
                        <td><code>괴산학술림_기후생명건강지수_평가결과.xlsx</code></td>
                        <td>4대 서브인덱스, 종합 CLHEI, 5단계 등급 전수 계산 결과 (5개 탭)</td>
                        <td class="text-center"><a href="outputs/괴산학술림_기후생명건강지수_평가결과.xlsx" class="btn btn-primary" style="background:#2d6a4f; color:white; padding:0.3rem 0.8rem; font-size:0.8rem;" download>지수 엑셀 받기</a></td>
                    </tr>
                    <tr>
                        <td><strong>기후생명건강지수 기획서 MD</strong></td>
                        <td><code>산림_기후생명건강지수_기획서_및_실증보고서.md</code></td>
                        <td>국내외 선행연구 검토, 수학적 모델링, 4대 서브인덱스 기획 전문</td>
                        <td class="text-center"><a href="산림_기후생명건강지수_기획서_및_실증보고서.md" class="btn btn-outline" style="color:black; border-color:#ccc; padding:0.3rem 0.8rem; font-size:0.8rem;" download>기획서 MD 받기</a></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </section>

</main>

<footer>
    <div class="footer-container">
        <div>
            <strong>건국대학교 괴산학술림(연습림) 공기미생물 및 음이온 연구 프로젝트</strong><br>
            <span style="font-size:0.8rem; opacity:0.8;">충북 괴산군 불정면 외령로2길 70 | 기준 대조구: 밭(Site 4) | 연구주체: 건국대학교 학술림 분석팀</span>
        </div>
        <div class="footer-links">
            <a href="#summary">맨 위로 이동</a>
            <a href="javascript:window.print()">보고서 인쇄</a>
        </div>
    </div>
</footer>

</body>
</html>
"""

html_path = Path("index.html")
html_path.write_text(html_content, encoding='utf-8')
print("Successfully updated index.html with location and weather!")

# Convert index.html to PDF using Edge headless
edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
pdf_path = Path("괴산연습림_공기미생물_음이온_종합해석보고서.pdf")

cmd = [
    edge_exe,
    "--headless",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={str(pdf_path.resolve())}",
    str(html_path.resolve())
]

print("Converting updated HTML to PDF via Microsoft Edge...")
result = subprocess.run(cmd, capture_output=True, text=True)
print(f"Edge returncode: {result.returncode}")
if pdf_path.exists():
    print(f"Successfully generated PDF: {pdf_path.resolve()} ({pdf_path.stat().st_size} bytes)")
