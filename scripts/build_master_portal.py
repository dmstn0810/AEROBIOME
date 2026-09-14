import json
import os
import sys

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), 'scripts'))
sys.stdout.reconfigure(encoding='utf-8')
print("Writing build_master_portal.py...")

# Load precomputed data
with open('site_metric_data_7dates.json', 'r', encoding='utf-8') as f:
    site_metric_data = json.load(f)

import prepare_portal_data as ppd
import generate_subcomponents as gsc


site_metric_data_json = json.dumps(site_metric_data, ensure_ascii=False)
site_encyclopedia_data_json = json.dumps(ppd.site_encyclopedia_data, ensure_ascii=False)
figures_data_json = json.dumps(ppd.figures_data, ensure_ascii=False)
site_cards_rendered = gsc.site_cards_rendered
gallery_cards_rendered = gsc.gallery_cards_rendered


html_content = f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <meta http-equiv="Pragma" content="no-cache">
  <meta http-equiv="Expires" content="0">
  <title>건국대학교 학술림(괴산) 공기미생물(Aerobiome)·음이온·기후생명건강지수(CLHEI) 전주기 통합 연구 포털</title>
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>
  <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    body {{ font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif; }}
    .chapter-tab-active {{ 
      background-color: #047857 !important; 
      color: #ffffff !important; 
      font-weight: 700 !important; 
      border-bottom: 3px solid #34d399 !important;
      box-shadow: 0 2px 4px rgba(0,0,0,0.15);
    }}
    .date-pill-active {{ background-color: #047857 !important; color: white !important; font-weight: 700; }}
    .metric-pill-active {{ background-color: #0284c7 !important; color: white !important; font-weight: 700; }}
    .stand-filter-active {{ background-color: #047857 !important; color: white !important; font-weight: 700; }}
    .gallery-filter-active {{ background-color: #059669 !important; color: white !important; font-weight: 700; }}
  </style>
</head>
<body class="bg-slate-950 text-slate-100 antialiased min-h-screen flex flex-col selection:bg-emerald-500 selection:text-white">

  <!-- Top Sticky Header -->
  <header class="bg-slate-900/95 backdrop-blur border-b border-emerald-900/60 sticky top-0 z-50 shadow-lg">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 flex flex-wrap justify-between items-center gap-3">
      <div class="flex items-center space-x-3">
        <div class="w-11 h-11 rounded-2xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center shadow-lg shadow-emerald-950">
          <i data-lucide="trees" class="text-white w-6 h-6"></i>
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-base sm:text-lg font-black tracking-tight text-white">건국대학교 학술림</h1>
            <span class="text-[11px] bg-emerald-900/90 text-emerald-200 px-2.5 py-0.5 rounded-full border border-emerald-700/60 font-semibold">충북 괴산군 불정면 신흥리 산 11-1</span>
          </div>
          <p class="text-xs text-emerald-400 font-medium">공기미생물(Aerobiome) · 산림 음이온 · 기후생명건강지수(CLHEI) 전주기 통합 연구 플랫폼</p>
        </div>
      </div>
      
      <!-- Top Action Download Buttons -->
      <div class="flex items-center space-x-2">
        <a href="괴산연습림_공기미생물_음이온_종합해석보고서.pdf" download class="text-xs px-3.5 py-2 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 font-bold transition flex items-center gap-1.5 shadow-md text-white">
          <i data-lucide="file-text" class="w-4 h-4"></i> 종합 보고서 (PDF 40p)
        </a>
        <a href="괴산연습림 전체데이터.xlsx" download class="text-xs px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 font-bold transition flex items-center gap-1.5 border border-slate-700 text-slate-200">
          <i data-lucide="table" class="w-4 h-4 text-emerald-400"></i> 마스터 엑셀 (348행)
        </a>
        <a href="괴산학술림_기후생명건강지수_평가결과.xlsx" download class="text-xs px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 font-bold transition flex items-center gap-1.5 border border-slate-700 text-slate-200">
          <i data-lucide="activity" class="w-4 h-4 text-cyan-400"></i> CLHEI 지수 엑셀
        </a>
      </div>
    </div>

    <!-- Sticky 8-Chapter Navigation Tabs Bar -->
    <nav class="bg-slate-900/90 border-t border-slate-800 overflow-x-auto">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex space-x-1 sm:space-x-1.5 text-xs font-semibold text-slate-300 py-1.5" id="chapterNavTabs">
        <button onclick="switchChapter(1)" id="nav-ch1" class="chapter-tab chapter-tab-active py-2 px-3 whitespace-nowrap rounded-xl transition flex items-center gap-1.5">
          <i data-lucide="globe" class="w-4 h-4"></i> 제1장. 개요 & 기상청 AWS
        </button>
        <button onclick="switchChapter(2)" id="nav-ch2" class="chapter-tab py-2 px-3 whitespace-nowrap rounded-xl hover:text-white transition flex items-center gap-1.5">
          <i data-lucide="line-chart" class="w-4 h-4"></i> 제2장. 7개 시기 미생물 농도
        </button>
        <button onclick="switchChapter(3)" id="nav-ch3" class="chapter-tab py-2 px-3 whitespace-nowrap rounded-xl hover:text-white transition flex items-center gap-1.5">
          <i data-lucide="wind" class="w-4 h-4 text-cyan-400"></i> 제3장. 산림 음이온 분석
        </button>
        <button onclick="switchChapter(4)" id="nav-ch4" class="chapter-tab py-2 px-3 whitespace-nowrap rounded-xl hover:text-white transition flex items-center gap-1.5">
          <i data-lucide="sparkles" class="w-4 h-4 text-amber-400"></i> 제4장. 기후생명건강지수(CLHEI)
        </button>
        <button onclick="switchChapter(5)" id="nav-ch5" class="chapter-tab py-2 px-3 whitespace-nowrap rounded-xl hover:text-white transition flex items-center gap-1.5">
          <i data-lucide="trees" class="w-4 h-4 text-emerald-400"></i> 제5장. 🌲 10대 지점 생태백과
        </button>
        <button onclick="switchChapter(6)" id="nav-ch6" class="chapter-tab py-2 px-3 whitespace-nowrap rounded-xl hover:text-white transition flex items-center gap-1.5">
          <i data-lucide="dna" class="w-4 h-4 text-purple-400"></i> 제6장. DNA 메타게놈 & 네트워크
        </button>
        <button onclick="switchChapter(7)" id="nav-ch7" class="chapter-tab py-2 px-3 whitespace-nowrap rounded-xl hover:text-white transition flex items-center gap-1.5">
          <i data-lucide="bar-chart-2" class="w-4 h-4"></i> 제7장. 환경 상관 & 아스팔트 보정
        </button>
        <button onclick="switchChapter(8)" id="nav-ch8" class="chapter-tab py-2 px-3 whitespace-nowrap rounded-xl hover:text-white transition flex items-center gap-1.5">
          <i data-lucide="image" class="w-4 h-4 text-rose-400"></i> 제8장. 🖼️ 연구 그래픽 & 다운로드
        </button>
      </div>
    </nav>
  </header>

  <!-- Hero Section -->
  <section class="bg-gradient-to-b from-slate-900 via-slate-950 to-slate-950 text-white py-8 px-4 border-b border-slate-800">
    <div class="max-w-7xl mx-auto space-y-6">
      <div class="space-y-3">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-semibold">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          2026년 3월~9월 7대 조사 전수 배양(N=348) · 초당 음이온(N=44,996) · ITS 메타게놈(2,091,638 reads) · 기후생명건강지수(CLHEI)
        </div>
        <h2 class="text-2xl sm:text-3xl lg:text-4xl font-black tracking-tight leading-snug">
          건국대학교 학술림(괴산) 공기미생물(Aerobiome) · 음이온 · CLHEI <br/>
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400">
            산림 생태계 치유 자원 전주기 빅데이터 통합 연구 포털
          </span>
        </h2>
        <p class="text-slate-400 text-xs sm:text-sm leading-relaxed max-w-4xl">
          충청북도 괴산군 불정면 건국대학교 학술림 10대 고정 조사구(소나무, 잣나무, 버들나무, 낙엽송, 리기다소나무, 밭, 주차장 대조구)에서 계측된 **348건의 공기미생물 절대 농도(CFU/㎥ = Count/0.1)**, **44,996건의 1초 단위 산림 음이온 실측치**, **기상청 불정면 AWS(685) 종관기상 연계 임내 미기후 완충 효과**, **Site 5 아스팔트 포장 토양 결측(NaN) 공식 보정**, 그리고 **차세대 기후·생명·건강 생태지수(CLHEI)**를 단일 통합 플랫폼에서 입체적으로 제공합니다.
        </p>
      </div>

      <!-- 6 Key KPI Cards -->
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        <div class="bg-slate-900/80 border border-slate-800 p-3.5 rounded-2xl hover:border-emerald-500/50 transition shadow-lg">
          <div class="text-[11px] text-slate-400 font-medium">총부유세균 (TAB)</div>
          <div class="text-xl font-black text-emerald-400 mt-1">29.8 <span class="text-xs font-normal text-slate-400">CFU/㎥</span></div>
          <div class="text-[10px] text-emerald-300 mt-0.5">실내기준(800)의 3.7% 청정</div>
        </div>
        <div class="bg-slate-900/80 border border-slate-800 p-3.5 rounded-2xl hover:border-cyan-500/50 transition shadow-lg">
          <div class="text-[11px] text-slate-400 font-medium">산림 음이온 발생량</div>
          <div class="text-xl font-black text-cyan-400 mt-1">1,673 <span class="text-xs font-normal text-slate-400">개/㎤</span></div>
          <div class="text-[10px] text-cyan-300 mt-0.5">밭(934.6) 대비 1.79배</div>
        </div>
        <div class="bg-slate-900/80 border border-slate-800 p-3.5 rounded-2xl hover:border-amber-500/50 transition shadow-lg">
          <div class="text-[11px] text-slate-400 font-medium">생태지수 (CLHEI)</div>
          <div class="text-xl font-black text-amber-400 mt-1">85.8 <span class="text-xs font-normal text-slate-400">점</span></div>
          <div class="text-[10px] text-amber-300 mt-0.5">1등급 천연 최우수 치유림</div>
        </div>
        <div class="bg-slate-900/80 border border-slate-800 p-3.5 rounded-2xl hover:border-teal-500/50 transition shadow-lg">
          <div class="text-[11px] text-slate-400 font-medium">기상 완충 쿨링 효과</div>
          <div class="text-xl font-black text-teal-400 mt-1">-2.1 <span class="text-xs font-normal text-slate-400">℃</span></div>
          <div class="text-[10px] text-teal-300 mt-0.5">폭염 저감 & 풍속 38.5% 감쇄</div>
        </div>
        <div class="bg-slate-900/80 border border-slate-800 p-3.5 rounded-2xl hover:border-blue-500/50 transition shadow-lg">
          <div class="text-[11px] text-slate-400 font-medium">7대 시계열 전수조사</div>
          <div class="text-xl font-black text-blue-400 mt-1">348 <span class="text-xs font-normal text-slate-400">건</span></div>
          <div class="text-[10px] text-blue-300 mt-0.5">가을철 7차 조사 세균 -52.0%</div>
        </div>
        <div class="bg-slate-900/80 border border-slate-800 p-3.5 rounded-2xl hover:border-purple-500/50 transition shadow-lg">
          <div class="text-[11px] text-slate-400 font-medium">ITS 차세대 메타게놈</div>
          <div class="text-xl font-black text-purple-400 mt-1">2.09M <span class="text-xs font-normal text-slate-400">reads</span></div>
          <div class="text-[10px] text-purple-300 mt-0.5">봄-여름 생태 지위 교체</div>
        </div>
      </div>

      <!-- Quick Chapter Switcher Launcher Grid -->
      <div class="pt-2">
        <span class="text-xs text-slate-400 font-bold block mb-2">원하시는 분석 챕터를 클릭하시면 해당 장으로 바로 전환됩니다:</span>
        <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-2">
          <button onclick="switchChapter(1)" class="p-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-left transition flex items-center gap-2 cursor-pointer group">
            <span class="w-6 h-6 rounded-lg bg-emerald-500/20 text-emerald-300 flex items-center justify-center text-xs font-black shrink-0 group-hover:bg-emerald-500 group-hover:text-slate-950 transition">1</span>
            <span class="text-xs font-semibold text-slate-300 group-hover:text-white">학술림 & AWS</span>
          </button>
          <button onclick="switchChapter(2)" class="p-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-left transition flex items-center gap-2 cursor-pointer group">
            <span class="w-6 h-6 rounded-lg bg-blue-500/20 text-blue-300 flex items-center justify-center text-xs font-black shrink-0 group-hover:bg-blue-500 group-hover:text-slate-950 transition">2</span>
            <span class="text-xs font-semibold text-slate-300 group-hover:text-white">7개시기 미생물</span>
          </button>
          <button onclick="switchChapter(3)" class="p-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-left transition flex items-center gap-2 cursor-pointer group">
            <span class="w-6 h-6 rounded-lg bg-cyan-500/20 text-cyan-300 flex items-center justify-center text-xs font-black shrink-0 group-hover:bg-cyan-500 group-hover:text-slate-950 transition">3</span>
            <span class="text-xs font-semibold text-slate-300 group-hover:text-white">산림 음이온</span>
          </button>
          <button onclick="switchChapter(4)" class="p-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-left transition flex items-center gap-2 cursor-pointer group">
            <span class="w-6 h-6 rounded-lg bg-amber-500/20 text-amber-300 flex items-center justify-center text-xs font-black shrink-0 group-hover:bg-amber-500 group-hover:text-slate-950 transition">4</span>
            <span class="text-xs font-semibold text-slate-300 group-hover:text-white">생태지수 CLHEI</span>
          </button>
          <button onclick="switchChapter(5)" class="p-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-left transition flex items-center gap-2 cursor-pointer group">
            <span class="w-6 h-6 rounded-lg bg-emerald-500/20 text-emerald-300 flex items-center justify-center text-xs font-black shrink-0 group-hover:bg-emerald-500 group-hover:text-slate-950 transition">5</span>
            <span class="text-xs font-semibold text-slate-300 group-hover:text-white">10대 지점 백과</span>
          </button>
          <button onclick="switchChapter(6)" class="p-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-left transition flex items-center gap-2 cursor-pointer group">
            <span class="w-6 h-6 rounded-lg bg-purple-500/20 text-purple-300 flex items-center justify-center text-xs font-black shrink-0 group-hover:bg-purple-500 group-hover:text-slate-950 transition">6</span>
            <span class="text-xs font-semibold text-slate-300 group-hover:text-white">DNA 메타게놈</span>
          </button>
          <button onclick="switchChapter(7)" class="p-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-left transition flex items-center gap-2 cursor-pointer group">
            <span class="w-6 h-6 rounded-lg bg-rose-500/20 text-rose-300 flex items-center justify-center text-xs font-black shrink-0 group-hover:bg-rose-500 group-hover:text-slate-950 transition">7</span>
            <span class="text-xs font-semibold text-slate-300 group-hover:text-white">환경상관·보정</span>
          </button>
          <button onclick="switchChapter(8)" class="p-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-left transition flex items-center gap-2 cursor-pointer group">
            <span class="w-6 h-6 rounded-lg bg-teal-500/20 text-teal-300 flex items-center justify-center text-xs font-black shrink-0 group-hover:bg-teal-500 group-hover:text-slate-950 transition">8</span>
            <span class="text-xs font-semibold text-slate-300 group-hover:text-white">그래픽 & 자료</span>
          </button>
        </div>
      </div>
    </div>
  </section>

  <!-- Main Content Container -->
  <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">

    <!-- ========================================== -->
    <!-- CHAPTER 1: 학술림 위치 & 기상청 AWS 연계 -->
    <!-- ========================================== -->
    <div id="chapter-1" class="chapter-content space-y-8">
      <!-- Title Card -->
      <div class="bg-gradient-to-r from-emerald-950/70 to-slate-900 border border-emerald-800/60 rounded-3xl p-6 shadow-xl">
        <div class="flex items-center gap-3 mb-2">
          <div class="w-10 h-10 rounded-2xl bg-emerald-500/20 flex items-center justify-center text-emerald-400 font-black">
            <i data-lucide="globe" class="w-6 h-6"></i>
          </div>
          <div>
            <span class="text-xs font-bold text-emerald-400 tracking-wider uppercase">Chapter 1. Research Site & Synoptic Weather</span>
            <h3 class="text-xl sm:text-2xl font-black text-white">제1장. 건국대학교 괴산학술림 위치 정보 및 기상청(KMA) AWS 종관기상 연계</h3>
          </div>
        </div>
        <p class="text-xs sm:text-sm text-slate-300 leading-relaxed max-w-4xl">
          충북 괴산군 불정면 신흥리 산 11-1에 위치한 건국대학교 상허생명과학대학 부속 학술림(약 310 ha)의 지리적 환경과 인근 기상청 괴산 불정면 AWS(지점 685)의 종관 기상을 실시간 매핑하여, 산림 수관에 의한 온도 쿨링 및 미기후 완충 효과를 규명합니다.
        </p>
      </div>

      <!-- Asphalt Pavement Note Banner -->
      <div class="bg-rose-950/40 border border-rose-800/80 rounded-2xl p-5 shadow-lg flex items-start gap-4">
        <div class="w-10 h-10 rounded-xl bg-rose-500/20 text-rose-400 flex items-center justify-center shrink-0 mt-0.5">
          <i data-lucide="alert-triangle" class="w-6 h-6"></i>
        </div>
        <div class="space-y-1 text-xs sm:text-sm">
          <h4 class="font-bold text-rose-200 flex items-center gap-2">
            ⚠️ Site 5 (주차장 대조구) 아스팔트 포장 토양 결측치(NaN) 처리 안내
          </h4>
          <p class="text-slate-300 leading-relaxed">
            Site 5(주차장)는 관리사무소 앞 완전 불투수 아스팔트 포장면으로, 물리적으로 토양 측정 센서(온도, 습도, pH)의 삽입이 불가능합니다. 
            이에 따라 **토양 관련 3개 파라미터(soil-PH, soil-temp, soil-RH)는 결측치(NaN / N/A)로 공식 보정**되었으며, 
            토양 환경 상관관계 분석 시에는 불투수 포장면을 제외한 **자연 산림 및 경작지 9개 지점(315건)의 유효 데이터만을 대상으로 결측치 쌍별 제거(Pairwise Deletion)**를 적용하여 학술적 엄밀성을 확보하였습니다.
          </p>
        </div>
      </div>

      <!-- Location & AWS Cards Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Site Info Card -->
        <div class="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-4">
          <div class="flex items-center gap-3 border-b border-slate-800 pb-3">
            <div class="w-9 h-9 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold">
              <i data-lucide="map-pin" class="w-5 h-5"></i>
            </div>
            <div>
              <h4 class="font-black text-white text-base">건국대학교 상허생명과학대학 부속 괴산학술림</h4>
              <p class="text-xs text-slate-400">Konkuk University Academic Forest in Goesan</p>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-3 text-xs">
            <div class="bg-slate-950 p-3 rounded-xl border border-slate-800/80">
              <span class="text-slate-400 block mb-1">소재지</span>
              <strong class="text-slate-200">충북 괴산군 불정면 신흥리 산 11-1</strong>
            </div>
            <div class="bg-slate-950 p-3 rounded-xl border border-slate-800/80">
              <span class="text-slate-400 block mb-1">좌표 및 표고</span>
              <strong class="text-slate-200">36°52'08" N, 127°52'24" E (180~450m)</strong>
            </div>
            <div class="bg-slate-950 p-3 rounded-xl border border-slate-800/80">
              <span class="text-slate-400 block mb-1">총 면적 및 관리</span>
              <strong class="text-slate-200">약 310 ha (건국대 산림조경학 전공)</strong>
            </div>
            <div class="bg-slate-950 p-3 rounded-xl border border-slate-800/80">
              <span class="text-slate-400 block mb-1">대표 임상 수종</span>
              <strong class="text-slate-200">소나무, 잣나무, 일본잎갈나무, 왕버들</strong>
            </div>
          </div>
          <p class="text-xs text-slate-400 leading-relaxed">
            건국대학교 괴산학술림은 한반도 중부 온대림의 생태적 천이 궤적과 인공 조림지의 생물다양성을 보존하고 있는 핵심 학술 교육 연구림으로, 계곡부 수변식생부터 능선부 침엽수림까지 다양한 미기후대를 형성하고 있습니다.
          </p>
        </div>

        <!-- AWS Info Card -->
        <div class="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-4">
          <div class="flex items-center gap-3 border-b border-slate-800 pb-3">
            <div class="w-9 h-9 rounded-xl bg-cyan-500/20 text-cyan-400 flex items-center justify-center font-bold">
              <i data-lucide="cloud-sun" class="w-5 h-5"></i>
            </div>
            <div>
              <h4 class="font-black text-white text-base">기상청(KMA) 괴산 불정면 AWS (지점코드 685)</h4>
              <p class="text-xs text-slate-400">Korea Meteorological Administration AWS Station</p>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-3 text-xs">
            <div class="bg-slate-950 p-3 rounded-xl border border-slate-800/80">
              <span class="text-slate-400 block mb-1">관측소 위치</span>
              <strong class="text-slate-200">충북 괴산군 불정면 목도리 293-3</strong>
            </div>
            <div class="bg-slate-950 p-3 rounded-xl border border-slate-800/80">
              <span class="text-slate-400 block mb-1">직선거리 및 고도</span>
              <strong class="text-slate-200">학술림 북서측 약 3.8 km (표고 135m)</strong>
            </div>
            <div class="bg-slate-950 p-3 rounded-xl border border-slate-800/80">
              <span class="text-slate-400 block mb-1">여름철 기온 완충</span>
              <strong class="text-emerald-400 font-black">학술림 임내 -2.1℃ 폭염 냉각</strong>
            </div>
            <div class="bg-slate-950 p-3 rounded-xl border border-slate-800/80">
              <span class="text-slate-400 block mb-1">풍속 완충율</span>
              <strong class="text-cyan-400 font-black">산림 수관에 의한 38.5% 감쇄</strong>
            </div>
          </div>
          <p class="text-xs text-slate-400 leading-relaxed">
            기상청 종관 AWS 관측값과의 1:1 대응 분석 결과, 하절기 폭염 시 외곽 농경지 및 시가지 대비 학술림 수관 하층 기온이 최대 2.1℃ 낮아 열섬 현상을 억제하고 쾌적한 치유 환경을 제공함이 입증되었습니다.
          </p>
        </div>
      </div>

      <!-- Weather Buffer Figure Showcase -->
      <div class="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl">
        <div class="flex flex-col lg:flex-row items-center gap-6">
          <div class="w-full lg:w-1/2 overflow-hidden rounded-2xl border border-slate-800 bg-slate-950 cursor-pointer" onclick="openFigureModal('images/16_괴산연습림_기상완충효과.png', 'Fig 16. 기상청 불정면 AWS 대비 괴산연습림 기상 완충 효과', '산림 수관에 의한 하절기 기온 냉각(-2.1℃) 및 풍속 감쇄(38.5%) 검증')">
            <img src="images/16_괴산연습림_기상완충효과.png" alt="괴산연습림 기상완충효과" class="w-full h-auto object-contain hover:scale-105 transition duration-300">
          </div>
          <div class="w-full lg:w-1/2 space-y-3 text-xs sm:text-sm text-slate-300">
            <span class="text-xs font-bold text-cyan-400 uppercase tracking-wider">Microclimate Buffering Mechanism</span>
            <h4 class="text-lg font-black text-white">산림의 기상 완충 메커니즘과 온열 쾌적성</h4>
            <p class="leading-relaxed">
              괴산학술림의 다층 수관 구조는 여름철 직사일사를 80% 이상 차단하고, 수목 증발산 작용을 통해 잠열을 흡수함으로써 **-2.1℃의 자연 냉각 효과(Cooling Effect)**를 발휘합니다.
            </p>
            <ul class="space-y-2 text-xs">
              <li class="flex items-center gap-2 text-slate-300">
                <i data-lucide="check-circle" class="w-4 h-4 text-emerald-400"></i>
                <span><strong>폭염 완화:</strong> 7월 27일 최고기온 시 외부 31.5℃ 대비 임내 28.7℃ 유지</span>
              </li>
              <li class="flex items-center gap-2 text-slate-300">
                <i data-lucide="check-circle" class="w-4 h-4 text-emerald-400"></i>
                <span><strong>바람 완충:</strong> 4월 15일 강풍 시 외곽 7.6m/s 대비 임내 0.5m/s로 안정화</span>
              </li>
              <li class="flex items-center gap-2 text-slate-300">
                <i data-lucide="check-circle" class="w-4 h-4 text-emerald-400"></i>
                <span><strong>치유 환경:</strong> 온열지수(THI) 72.4로 '쾌적' 구간을 유지하여 산림치유 효과 극대화</span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Benchmarking Standards Table -->
      <div class="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-4">
        <h4 class="text-base sm:text-lg font-black text-white flex items-center gap-2">
          <i data-lucide="book-open" class="w-5 h-5 text-amber-400"></i> 국내외 선행연구 문헌 고찰 및 기준치 벤치마킹
        </h4>
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs border-collapse">
            <thead>
              <tr class="border-b border-slate-800 text-slate-400 bg-slate-950/60">
                <th class="py-3 px-4">분류 / 기관</th>
                <th class="py-3 px-4">총부유세균 (TAB)</th>
                <th class="py-3 px-4">총부유진균 (TAF)</th>
                <th class="py-3 px-4">산림 음이온</th>
                <th class="py-3 px-4">특성 및 평가 해석</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-800/60 text-slate-300">
              <tr class="hover:bg-slate-800/30">
                <td class="py-3 px-4 font-bold text-emerald-400">괴산학술림 (본 연구 실측치)</td>
                <td class="py-3 px-4 font-black text-emerald-300">연중 29.8 CFU/㎥</td>
                <td class="py-3 px-4 font-black text-amber-300">봄 330 ~ 여름 1,086</td>
                <td class="py-3 px-4 font-black text-cyan-300">1,673.1 개/㎤ (최대 3,498)</td>
                <td class="py-3 px-4 text-slate-300">세균 실내기준 대비 3.7% 청정, 진균은 유기물 분해 천연 방출</td>
              </tr>
              <tr class="hover:bg-slate-800/30">
                <td class="py-3 px-4 font-semibold text-slate-400">환경부 실내공기질 권고기준</td>
                <td class="py-3 px-4 text-slate-400">800 CFU/㎥ 이하</td>
                <td class="py-3 px-4 text-slate-400">500 CFU/㎥ 이하</td>
                <td class="py-3 px-4 text-slate-400">규정 없음</td>
                <td class="py-3 px-4 text-slate-400">다중이용시설 실내 환경 기준 (밀폐 오염도 평가용)</td>
              </tr>
              <tr class="hover:bg-slate-800/30">
                <td class="py-3 px-4 font-semibold text-slate-400">WHO 가이드라인</td>
                <td class="py-3 px-4 text-slate-400">1,000 CFU/㎥ 이하</td>
                <td class="py-3 px-4 text-slate-400">1,000 CFU/㎥ 이하</td>
                <td class="py-3 px-4 text-slate-400">> 1,000 개/㎤ (청정지역)</td>
                <td class="py-3 px-4 text-slate-400">세계보건기구 생물학적 입자 노출 가이드라인</td>
              </tr>
              <tr class="hover:bg-slate-800/30">
                <td class="py-3 px-4 font-semibold text-slate-400">국립산림과학원 치유의숲 기준</td>
                <td class="py-3 px-4 text-slate-400">자연 상태 유지</td>
                <td class="py-3 px-4 text-slate-400">자연 상태 유지</td>
                <td class="py-3 px-4 text-cyan-400 font-bold">1,000 ~ 1,500 개/㎤</td>
                <td class="py-3 px-4 text-slate-400">치유의 숲 조성 시 음이온 풍부 기준 충족</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ========================================== -->
    <!-- CHAPTER 2: 7개 시기 시계열 & 공기미생물 거시 농도 -->
    <!-- ========================================== -->
    <div id="chapter-2" class="chapter-content hidden space-y-8">
      <div class="bg-gradient-to-r from-blue-950/70 to-slate-900 border border-blue-800/60 rounded-3xl p-6 shadow-xl">
        <div class="flex items-center gap-3 mb-2">
          <div class="w-10 h-10 rounded-2xl bg-blue-500/20 flex items-center justify-center text-blue-400 font-black">
            <i data-lucide="line-chart" class="w-6 h-6"></i>
          </div>
          <div>
            <span class="text-xs font-bold text-blue-400 tracking-wider uppercase">Chapter 2. Bioaerosol Longitudinal Concentrations</span>
            <h3 class="text-xl sm:text-2xl font-black text-white">제2장. 7대 조사 시계열 전수 배양 농도 및 산림 차단 메커니즘</h3>
          </div>
        </div>
        <p class="text-xs sm:text-sm text-slate-300 leading-relaxed max-w-4xl">
          2026년 3월 4일부터 9월 10일까지 총 7회에 걸쳐 10대 조사구에서 수집된 348건의 총부유세균(TAB) 및 총부유진균(TAF) 배양 농도를 정량화하고, 가을철 7차 조사(-52.0% 세균 억제)를 포함한 계절적 천이 메커니즘을 분석합니다.
        </p>
      </div>

      <!-- Interactive Chart Controls -->
      <div class="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-4">
          <div>
            <h4 class="text-sm sm:text-base font-black text-white flex items-center gap-2">
              <i data-lucide="sliders" class="w-4 h-4 text-blue-400"></i> 인터랙티브 지점별 지표 시각화 (Chart.js)
            </h4>
            <p class="text-xs text-slate-400 mt-0.5">조사 일자와 측정 항목을 선택하시면 그래프가 실시간 갱신됩니다.</p>
          </div>

          <!-- Date Filters -->
          <div class="flex flex-wrap gap-1.5" id="dateFilterGroup">
            <button onclick="changeChartDate('all')" class="date-pill date-pill-active px-2.5 py-1 rounded-lg bg-slate-800 text-xs font-semibold hover:bg-slate-700 transition">전체 평균</button>
            <button onclick="changeChartDate('260304')" class="date-pill px-2.5 py-1 rounded-lg bg-slate-800 text-xs font-semibold hover:bg-slate-700 transition">3/04 (초봄)</button>
            <button onclick="changeChartDate('260415')" class="date-pill px-2.5 py-1 rounded-lg bg-slate-800 text-xs font-semibold hover:bg-slate-700 transition">4/15 (봄)</button>
            <button onclick="changeChartDate('260429')" class="date-pill px-2.5 py-1 rounded-lg bg-slate-800 text-xs font-semibold hover:bg-slate-700 transition">4/29 (늦봄)</button>
            <button onclick="changeChartDate('260513')" class="date-pill px-2.5 py-1 rounded-lg bg-slate-800 text-xs font-semibold hover:bg-slate-700 transition">5/13 (초여름)</button>
            <button onclick="changeChartDate('260727')" class="date-pill px-2.5 py-1 rounded-lg bg-slate-800 text-xs font-semibold hover:bg-slate-700 transition">7/27 (한여름)</button>
            <button onclick="changeChartDate('260813')" class="date-pill px-2.5 py-1 rounded-lg bg-slate-800 text-xs font-semibold hover:bg-slate-700 transition">8/13 (늦여름)</button>
            <button onclick="changeChartDate('260910')" class="date-pill px-2.5 py-1 rounded-lg bg-slate-800 text-xs font-semibold hover:bg-slate-700 transition text-emerald-300 font-bold border border-emerald-500/40">9/10 (가을철 7차)</button>
          </div>
        </div>

        <!-- Metric Selectors -->
        <div class="flex flex-wrap gap-2 items-center text-xs">
          <span class="text-slate-400 font-bold">측정 지표 선택:</span>
          <button onclick="changeChartMetric('TAF_CFU_m3')" id="btn-metric-taf" class="metric-pill metric-pill-active px-3 py-1.5 rounded-lg bg-slate-800 font-semibold transition">총부유진균 (TAF, CFU/㎥)</button>
          <button onclick="changeChartMetric('TAB_CFU_m3')" id="btn-metric-tab" class="metric-pill px-3 py-1.5 rounded-lg bg-slate-800 font-semibold transition">총부유세균 (TAB, CFU/㎥)</button>
          <button onclick="changeChartMetric('n-ion')" id="btn-metric-ion" class="metric-pill px-3 py-1.5 rounded-lg bg-slate-800 font-semibold transition">산림 음이온 (개/㎤)</button>
          <button onclick="changeChartMetric('air-temp')" id="btn-metric-temp" class="metric-pill px-3 py-1.5 rounded-lg bg-slate-800 font-semibold transition">기온 (℃)</button>
          <button onclick="changeChartMetric('air-RH')" id="btn-metric-rh" class="metric-pill px-3 py-1.5 rounded-lg bg-slate-800 font-semibold transition">상대습도 (%)</button>
          <button onclick="changeChartMetric('PM10')" id="btn-metric-pm10" class="metric-pill px-3 py-1.5 rounded-lg bg-slate-800 font-semibold transition">미세먼지 PM10 (㎍/㎥)</button>
        </div>

        <!-- Canvas -->
        <div class="h-80 w-full pt-4">
          <canvas id="interactiveSiteChartCanvas"></canvas>
        </div>
      </div>

      <!-- Comparison Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl space-y-2">
          <span class="text-xs font-bold text-emerald-400">인위적 교란 차단 효과</span>
          <h4 class="text-base font-bold text-white">가을철 세균 억제율 -52.0%</h4>
          <p class="text-xs text-slate-300 leading-relaxed">
            9월 10일 가을철 7차 조사 결과, 산림 내부 8개 지점의 부유세균 농도는 평균 **36.5 CFU/㎥**로 밭 대조구(**76.0 CFU/㎥**) 대비 **52.0%의 억제율**을 나타냈습니다.
          </p>
        </div>
        <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl space-y-2">
          <span class="text-xs font-bold text-amber-400">자연 초과 메커니즘</span>
          <h4 class="text-base font-bold text-white">여름철 고습기 포자 방출</h4>
          <p class="text-xs text-slate-300 leading-relaxed">
            7월 강우(64.6mm) 직후 진균 포자가 1,086 CFU/㎥로 증가한 것은 실내 곰팡이 오염과 달리 토양 분해균(*Trichoderma*)의 건전한 양분 순환 현상입니다.
          </p>
        </div>
        <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl space-y-2">
          <span class="text-xs font-bold text-cyan-400">온대림 생태 지문</span>
          <h4 class="text-base font-bold text-white">진균/세균비 (F/B) 36.4:1</h4>
          <p class="text-xs text-slate-300 leading-relaxed">
            도시 환경의 세균 우점(F/B < 1)과 상반되게, 온대 자연림의 수관 하층은 진균이 극우점하는 천연 바이오에어로졸 지문을 입증합니다.
          </p>
        </div>
      </div>

      <!-- Longitudinal Figures Showcase -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="bg-slate-900 border border-slate-800 rounded-3xl p-5 shadow-xl space-y-2">
          <h4 class="font-bold text-white text-sm">Fig 12. 공기미생물 7개 시기 계절 변화 추세선</h4>
          <div class="aspect-[16/10] bg-slate-950 rounded-2xl overflow-hidden cursor-pointer" onclick="openFigureModal('images/12_공기미생물_6개시기_계절변화_추세.png', 'Fig 12. 공기미생물 계절 변화 추세', '초봄부터 가을까지 7개 조사 시기 미생물 농도 변화 궤적')">
            <img src="images/12_공기미생물_6개시기_계절변화_추세.png" alt="미생물 계절변화 추세" class="w-full h-full object-contain hover:scale-105 transition">
          </div>
        </div>
        <div class="bg-slate-900 border border-slate-800 rounded-3xl p-5 shadow-xl space-y-2">
          <h4 class="font-bold text-white text-sm">Fig 14. 산림 vs 밭 대조구 전 시기 미생물 비교</h4>
          <div class="aspect-[16/10] bg-slate-950 rounded-2xl overflow-hidden cursor-pointer" onclick="openFigureModal('images/14_산림_vs_밭대조구_6개시기_미생물비교.png', 'Fig 14. 산림 vs 밭 대조구 비교', '경작지 대비 자연 산림의 미생물 농도 격차 및 억제 효과')">
            <img src="images/14_산림_vs_밭대조구_6개시기_미생물비교.png" alt="산림 대조구 미생물 비교" class="w-full h-full object-contain hover:scale-105 transition">
          </div>
        </div>
      </div>
    </div>

    <!-- ========================================== -->
    <!-- CHAPTER 3: 산림 음이온 정량 분석 -->
    <!-- ========================================== -->
    <div id="chapter-3" class="chapter-content hidden space-y-8">
      <div class="bg-gradient-to-r from-cyan-950/70 to-slate-900 border border-cyan-800/60 rounded-3xl p-6 shadow-xl">
        <div class="flex items-center gap-3 mb-2">
          <div class="w-10 h-10 rounded-2xl bg-cyan-500/20 flex items-center justify-center text-cyan-400 font-black">
            <i data-lucide="wind" class="w-6 h-6"></i>
          </div>
          <div>
            <span class="text-xs font-bold text-cyan-400 tracking-wider uppercase">Chapter 3. Forest Negative Air Ions Analysis</span>
            <h3 class="text-xl sm:text-2xl font-black text-white">제3장. 산림 음이온(Negative Air Ions) 44,996건 초당 실측 빅데이터 분석</h3>
          </div>
        </div>
        <p class="text-xs sm:text-sm text-slate-300 leading-relaxed max-w-4xl">
          전자기적 흡인식 계측기를 사용하여 1초당 1회씩 수집된 총 44,996건의 실측 시계열 데이터를 분석하여, 수종별 음이온 발생 특성, 계절적 상승 궤적, 그리고 15분 연속 측정 세션 내 1분 단위 안정성을 완벽히 규명하였습니다.
        </p>
      </div>

      <!-- Ion Ranking Cards -->
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 text-center">
        <div class="bg-slate-900 border border-cyan-700/60 p-4 rounded-2xl">
          <span class="text-[10px] text-cyan-300 font-bold block mb-1">🥇 1위 (낙엽송림)</span>
          <div class="text-lg font-black text-white">2,965.5</div>
          <span class="text-[10px] text-cyan-400 mt-1 block">밭 대비 3.17배</span>
        </div>
        <div class="bg-slate-900 border border-cyan-800/60 p-4 rounded-2xl">
          <span class="text-[10px] text-cyan-300 font-bold block mb-1">🥈 2위 (소나무림)</span>
          <div class="text-lg font-black text-white">2,196.7</div>
          <span class="text-[10px] text-cyan-400 mt-1 block">밭 대비 2.35배</span>
        </div>
        <div class="bg-slate-900 border border-slate-800 p-4 rounded-2xl">
          <span class="text-[10px] text-slate-400 font-bold block mb-1">3위 (잣나무림)</span>
          <div class="text-lg font-black text-white">1,758.2</div>
          <span class="text-[10px] text-slate-400 mt-1 block">밭 대비 1.88배</span>
        </div>
        <div class="bg-slate-900 border border-slate-800 p-4 rounded-2xl">
          <span class="text-[10px] text-slate-400 font-bold block mb-1">4위 (버들나무림)</span>
          <div class="text-lg font-black text-white">1,489.0</div>
          <span class="text-[10px] text-slate-400 mt-1 block">수변 레너드 효과</span>
        </div>
        <div class="bg-slate-900 border border-slate-800 p-4 rounded-2xl">
          <span class="text-[10px] text-slate-400 font-bold block mb-1">5위 (주차장 대조)</span>
          <div class="text-lg font-black text-white">1,235.0</div>
          <span class="text-[10px] text-slate-400 mt-1 block">아스팔트 복사</span>
        </div>
        <div class="bg-slate-900 border border-rose-900/60 p-4 rounded-2xl">
          <span class="text-[10px] text-rose-300 font-bold block mb-1">6위 (밭 대조구)</span>
          <div class="text-lg font-black text-rose-300">934.6</div>
          <span class="text-[10px] text-rose-400 mt-1 block">기준 대조군 (1.0x)</span>
        </div>
      </div>

      <!-- Ion Chart Canvas -->
      <div class="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-4">
        <h4 class="text-base font-black text-white flex items-center gap-2">
          <i data-lucide="bar-chart" class="w-5 h-5 text-cyan-400"></i> 수종 그룹별 음이온 평균 발생량 및 밭 대조구 대비 배율
        </h4>
        <div class="h-80 w-full">
          <canvas id="ionSpeciesChartCanvas"></canvas>
        </div>
      </div>

      <!-- Ion Figures Showcase Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 space-y-2">
          <h5 class="text-xs font-bold text-white">Fig 01. 조사일자별·지점별 발생량</h5>
          <div class="aspect-[16/10] bg-slate-950 rounded-xl overflow-hidden cursor-pointer" onclick="openFigureModal('images/01_일자별_지점별_음이온발생량_비교.png', 'Fig 01. 음이온 발생량 비교', '조사일자별 10개 지점 음이온 발생량 프로파일')">
            <img src="images/01_일자별_지점별_음이온발생량_비교.png" alt="일자별 지점별 음이온" class="w-full h-full object-contain hover:scale-105 transition">
          </div>
        </div>
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 space-y-2">
          <h5 class="text-xs font-bold text-white">Fig 03. 산림 vs 대조구 음이온 배율</h5>
          <div class="aspect-[16/10] bg-slate-950 rounded-xl overflow-hidden cursor-pointer" onclick="openFigureModal('images/03_산림_대조구_비교_및_배율.png', 'Fig 03. 산림 대조구 음이온 배율', '밭 대조구 대비 산림의 1.79~3.17배 음이온 배율')">
            <img src="images/03_산림_대조구_비교_및_배율.png" alt="음이온 배율" class="w-full h-full object-contain hover:scale-105 transition">
          </div>
        </div>
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 space-y-2">
          <h5 class="text-xs font-bold text-white">Fig 06. 15분 세션 내 1분 단위 안정성</h5>
          <div class="aspect-[16/10] bg-slate-950 rounded-xl overflow-hidden cursor-pointer" onclick="openFigureModal('images/06_15분_세션내_1분단위_안정성추세.png', 'Fig 06. 세션 내 안정성 추세', '15분 연속 측정 시계열의 시계열 안정성 검증')">
            <img src="images/06_15분_세션내_1분단위_안정성추세.png" alt="음이온 안정성 추세" class="w-full h-full object-contain hover:scale-105 transition">
          </div>
        </div>
      </div>
    </div>

    <!-- ========================================== -->
    <!-- CHAPTER 4: 기후생명건강지수(CLHEI) 평가 -->
    <!-- ========================================== -->
    <div id="chapter-4" class="chapter-content hidden space-y-8">
      <div class="bg-gradient-to-r from-amber-950/70 to-slate-900 border border-amber-800/60 rounded-3xl p-6 shadow-xl">
        <div class="flex items-center gap-3 mb-2">
          <div class="w-10 h-10 rounded-2xl bg-amber-500/20 flex items-center justify-center text-amber-400 font-black">
            <i data-lucide="sparkles" class="w-6 h-6"></i>
          </div>
          <div>
            <span class="text-xs font-bold text-amber-400 tracking-wider uppercase">Chapter 4. Climate-Life-Health Ecosystem Index</span>
            <h3 class="text-xl sm:text-2xl font-black text-white">제4장. 기후·생명·건강 생태지수 (CLHEI) 기획 및 실증 평가</h3>
          </div>
        </div>
        <p class="text-xs sm:text-sm text-slate-300 leading-relaxed max-w-4xl">
          국내외 선행 연구를 바탕으로 생체안락도(BSI, 25%), 천연활력도(NVI, 30%), 대기청정도(API, 25%), 미생물건전도(MBI, 20%)의 4대 서브지수를 통합한 **기후·생명·건강 생태지수(CLHEI)**를 산출하여 괴산학술림의 생태적 치유 가치를 1등급으로 공인 평가하였습니다.
        </p>
      </div>

      <!-- 4 Sub-index Framework Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="bg-slate-900 border border-slate-800 p-4 rounded-2xl space-y-2">
          <span class="text-xs font-bold px-2 py-0.5 rounded bg-blue-900/60 text-blue-300 border border-blue-700">가중치 25%</span>
          <h4 class="font-bold text-white text-base">생체안락도 (BSI)</h4>
          <p class="text-xs text-slate-400 leading-relaxed">
            온습도 열쾌적성(THI), 산림 수관에 의한 풍속 완충률, 그리고 직사일사 차열 효과를 종합 반영.
          </p>
        </div>
        <div class="bg-slate-900 border border-slate-800 p-4 rounded-2xl space-y-2">
          <span class="text-xs font-bold px-2 py-0.5 rounded bg-cyan-900/60 text-cyan-300 border border-cyan-700">가중치 30%</span>
          <h4 class="font-bold text-white text-base">천연활력도 (NVI)</h4>
          <p class="text-xs text-slate-400 leading-relaxed">
            식생 광합성 및 증산작용에서 유래하는 산림 음이온 발생량과 15분 세션 안정성을 복합 정량화.
          </p>
        </div>
        <div class="bg-slate-900 border border-slate-800 p-4 rounded-2xl space-y-2">
          <span class="text-xs font-bold px-2 py-0.5 rounded bg-emerald-900/60 text-emerald-300 border border-emerald-700">가중치 25%</span>
          <h4 class="font-bold text-white text-base">대기청정도 (API)</h4>
          <p class="text-xs text-slate-400 leading-relaxed">
            총부유세균(TAB)의 절대 농도 억제율 및 미세먼지(PM10) 저감 효과를 통한 호흡기 청정 수준 평가.
          </p>
        </div>
        <div class="bg-slate-900 border border-slate-800 p-4 rounded-2xl space-y-2">
          <span class="text-xs font-bold px-2 py-0.5 rounded bg-amber-900/60 text-amber-300 border border-amber-700">가중치 20%</span>
          <h4 class="font-bold text-white text-base">미생물건전도 (MBI)</h4>
          <p class="text-xs text-slate-400 leading-relaxed">
            온대 자연림 고유의 진균/세균비(F/B) 균형과 토양 유익균 중심의 분해 생태계 건강성 반영.
          </p>
        </div>
      </div>

      <!-- Radar Chart Showcase -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
        <div class="lg:col-span-7 bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-4">
          <h4 class="text-base font-black text-white flex items-center gap-2">
            <i data-lucide="radar" class="w-5 h-5 text-amber-400"></i> 수종 그룹별 4대 서브지수 비교 레이더 차트
          </h4>
          <div class="h-80 w-full">
            <canvas id="clheiRadarCanvas"></canvas>
          </div>
        </div>

        <div class="lg:col-span-5 bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-4">
          <h4 class="text-base font-black text-white">수종 그룹별 종합 평가 결과</h4>
          <div class="space-y-3 text-xs">
            <div class="flex items-center justify-between p-3 rounded-xl bg-slate-950 border border-slate-800">
              <span class="font-bold text-slate-200">소나무류 (소나무·리기다)</span>
              <div class="text-right">
                <span class="text-emerald-400 font-black text-sm">81.9점</span>
                <span class="text-[10px] text-slate-400 block">2등급 (우수 생태 건강림)</span>
              </div>
            </div>
            <div class="flex items-center justify-between p-3 rounded-xl bg-slate-950 border border-slate-800">
              <span class="font-bold text-slate-200">잣나무류 (잣나무 a, b)</span>
              <div class="text-right">
                <span class="text-emerald-400 font-black text-sm">78.4점</span>
                <span class="text-[10px] text-slate-400 block">2등급 (우수 생태 건강림)</span>
              </div>
            </div>
            <div class="flex items-center justify-between p-3 rounded-xl bg-slate-950 border border-slate-800">
              <span class="font-bold text-slate-200">낙엽송류 (낙엽송 a, b)</span>
              <div class="text-right">
                <span class="text-emerald-400 font-black text-sm">77.7점</span>
                <span class="text-[10px] text-slate-400 block">2등급 (우수 생태 건강림)</span>
              </div>
            </div>
            <div class="flex items-center justify-between p-3 rounded-xl bg-slate-950 border border-slate-800">
              <span class="font-bold text-slate-200">버드나무류 (왕버들 a, b)</span>
              <div class="text-right">
                <span class="text-emerald-400 font-black text-sm">77.5점</span>
                <span class="text-[10px] text-slate-400 block">2등급 (우수 생태 건강림)</span>
              </div>
            </div>
            <div class="flex items-center justify-between p-3 rounded-xl bg-rose-950/40 border border-rose-900/60">
              <span class="font-bold text-rose-200">밭 (개활 경작지 대조구)</span>
              <div class="text-right">
                <span class="text-rose-400 font-black text-sm">71.3점</span>
                <span class="text-[10px] text-rose-300 block">3등급 (보통 생태 녹지)</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CLHEI Trend Figures Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="bg-slate-900 border border-slate-800 rounded-3xl p-5 shadow-xl space-y-2">
          <h4 class="font-bold text-white text-sm">Fig 18. 기후생명건강지수 전 시기 계절 추세</h4>
          <div class="aspect-[16/10] bg-slate-950 rounded-2xl overflow-hidden cursor-pointer" onclick="openFigureModal('images/18_기후생명건강지수_6개시기_계절추세.png', 'Fig 18. CLHEI 계절 추세', '봄부터 가을까지 산림의 생태지수 상승 곡선')">
            <img src="images/18_기후생명건강지수_6개시기_계절추세.png" alt="CLHEI 계절추세" class="w-full h-full object-contain hover:scale-105 transition">
          </div>
        </div>
        <div class="bg-slate-900 border border-slate-800 rounded-3xl p-5 shadow-xl space-y-2">
          <h4 class="font-bold text-white text-sm">Fig 19. 산림 vs 밭 대조구 생태지수 격차 분석</h4>
          <div class="aspect-[16/10] bg-slate-950 rounded-2xl overflow-hidden cursor-pointer" onclick="openFigureModal('images/19_산림_vs_밭대조구_생태지수_격차분석.png', 'Fig 19. 생태지수 격차 분석', '자연 산림과 경작지 대조구 간의 23.4점 격차 실증')">
            <img src="images/19_산림_vs_밭대조구_생태지수_격차분석.png" alt="CLHEI 격차분석" class="w-full h-full object-contain hover:scale-105 transition">
          </div>
        </div>
      </div>
    </div>

    <!-- ========================================== -->
    <!-- CHAPTER 5: 10대 지점별 종합 생태백과 -->
    <!-- ========================================== -->
    <div id="chapter-5" class="chapter-content hidden space-y-8">
      <div class="bg-gradient-to-r from-emerald-950/70 to-slate-900 border border-emerald-800/60 rounded-3xl p-6 shadow-xl">
        <div class="flex items-center gap-3 mb-2">
          <div class="w-10 h-10 rounded-2xl bg-emerald-500/20 flex items-center justify-center text-emerald-400 font-black">
            <i data-lucide="trees" class="w-6 h-6"></i>
          </div>
          <div>
            <span class="text-xs font-bold text-emerald-400 tracking-wider uppercase">Chapter 5. 10-Site Comprehensive Microbial Encyclopedia</span>
            <h3 class="text-xl sm:text-2xl font-black text-white">제5장. 🌲 건국대 학술림 10대 조사지점별 종합 생태백과 (Encyclopedia)</h3>
          </div>
        </div>
        <p class="text-xs sm:text-sm text-slate-300 leading-relaxed max-w-4xl">
          각 조사구의 수종, 입지 지형, 토양 환경(주차장 아스팔트 N/A 반영), 공기미생물 배양 농도, 산림 음이온 발생량, 차세대 ITS 메타게놈 우점종, 생태적 물질 순환, 그리고 맞춤형 산림 치유 가이드를 완벽하게 수록하였습니다.
        </p>
      </div>

      <!-- Controls: Stand Filter & Search -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 flex flex-wrap items-center justify-between gap-4 shadow-lg">
        <div class="flex flex-wrap gap-2" id="standFilterGroup">
          <button onclick="filterSiteCards('all')" class="stand-filter-btn stand-filter-active px-3 py-1.5 rounded-xl bg-slate-800 text-xs font-bold transition">전체 10개 지점</button>
          <button onclick="filterSiteCards('conifer')" class="stand-filter-btn px-3 py-1.5 rounded-xl bg-slate-800 text-xs font-bold transition">침엽수림 (소나무·잣나무·낙엽송)</button>
          <button onclick="filterSiteCards('riparian')" class="stand-filter-btn px-3 py-1.5 rounded-xl bg-slate-800 text-xs font-bold transition">수변 활엽수림 (왕버들)</button>
          <button onclick="filterSiteCards('control')" class="stand-filter-btn px-3 py-1.5 rounded-xl bg-slate-800 text-xs font-bold transition">대조구 (밭·주차장)</button>
        </div>
        <div class="relative w-full sm:w-72">
          <i data-lucide="search" class="w-4 h-4 text-slate-400 absolute left-3 top-3"></i>
          <input type="text" id="siteSearchInput" onkeyup="searchSiteCards()" placeholder="수종, 학명, 미생물, 치유특성 검색..." class="w-full bg-slate-950 border border-slate-700/80 rounded-xl pl-9 pr-4 py-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-emerald-500">
        </div>
      </div>

      <!-- 10 Site Cards Grid (Pre-rendered) -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6" id="siteEncyclopediaGrid">
        {site_cards_rendered}
      </div>
    </div>

    <!-- ========================================== -->
    <!-- CHAPTER 6: DNA 메타게놈 & 공기생 네트워크 -->
    <!-- ========================================== -->
    <div id="chapter-6" class="chapter-content hidden space-y-8">
      <div class="bg-gradient-to-r from-purple-950/70 to-slate-900 border border-purple-800/60 rounded-3xl p-6 shadow-xl">
        <div class="flex items-center gap-3 mb-2">
          <div class="w-10 h-10 rounded-2xl bg-purple-500/20 flex items-center justify-center text-purple-400 font-black">
            <i data-lucide="dna" class="w-6 h-6"></i>
          </div>
          <div>
            <span class="text-xs font-bold text-purple-400 tracking-wider uppercase">Chapter 6. ITS Metagenomics & Co-occurrence Network</span>
            <h3 class="text-xl sm:text-2xl font-black text-white">제6장. ITS 차세대 DNA 메타게놈(2,091,638 reads) & 공기생 상호작용 네트워크</h3>
          </div>
        </div>
        <p class="text-xs sm:text-sm text-slate-300 leading-relaxed max-w-4xl">
          봄철(4/15)과 여름철(7/27)에 수집된 2,091,638 reads의 공기진균 ITS 차세대 염기서열(NGS)을 분석하여, 봄철 엽면 피생균·알레르겐에서 여름철 토양 사상균·목재부후균으로의 생태 지위 교체(Niche Turnover) 및 공존 네트워크의 핵심 허브(Keystone Taxa)를 규명하였습니다.
        </p>
      </div>

      <!-- DNA Figures Showcase Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 space-y-2">
          <h5 class="text-xs font-bold text-white">Fig 1. 계절별 알파 다양성 (Shannon, Chao1)</h5>
          <div class="aspect-[16/10] bg-slate-950 rounded-xl overflow-hidden cursor-pointer" onclick="openFigureModal('images/fig1_seasonal_alpha_diversity.png', 'Fig 1. 알파 다양성', '여름철 종 풍부도 및 균등도 상승 검증')">
            <img src="images/fig1_seasonal_alpha_diversity.png" alt="알파 다양성" class="w-full h-full object-contain hover:scale-105 transition">
          </div>
        </div>
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 space-y-2">
          <h5 class="text-xs font-bold text-white">Fig 2. 문(Phylum) 및 강(Class) 군집비</h5>
          <div class="aspect-[16/10] bg-slate-950 rounded-xl overflow-hidden cursor-pointer" onclick="openFigureModal('images/fig2_phylum_class_composition.png', 'Fig 2. 군집 조성비', '자낭균문 vs 담자균문의 계절별 교체')">
            <img src="images/fig2_phylum_class_composition.png" alt="문 강 조성비" class="w-full h-full object-contain hover:scale-105 transition">
          </div>
        </div>
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 space-y-2">
          <h5 class="text-xs font-bold text-white">Fig 3. 상위 속(Top Genera) 히트맵</h5>
          <div class="aspect-[16/10] bg-slate-950 rounded-xl overflow-hidden cursor-pointer" onclick="openFigureModal('images/fig3_top_genera_heatmap.png', 'Fig 3. 상위 속 히트맵', '지점별 25대 주요 속 상대 풍부도')">
            <img src="images/fig3_top_genera_heatmap.png" alt="상위 속 히트맵" class="w-full h-full object-contain hover:scale-105 transition">
          </div>
        </div>
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 space-y-2">
          <h5 class="text-xs font-bold text-white">Fig 4. 베타 다양성 PCoA (Bray-Curtis)</h5>
          <div class="aspect-[16/10] bg-slate-950 rounded-xl overflow-hidden cursor-pointer" onclick="openFigureModal('images/fig4_beta_diversity_pcoa.png', 'Fig 4. 베타 다양성', '봄 vs 여름 군집의 명확한 통계적 이질성')">
            <img src="images/fig4_beta_diversity_pcoa.png" alt="베타 다양성" class="w-full h-full object-contain hover:scale-105 transition">
          </div>
        </div>
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 space-y-2">
          <h5 class="text-xs font-bold text-white">Fig 5. 기능군 및 알레르겐 분포</h5>
          <div class="aspect-[16/10] bg-slate-950 rounded-xl overflow-hidden cursor-pointer" onclick="openFigureModal('images/fig5_functional_guilds_allergens.png', 'Fig 5. 기능군 및 알레르겐', 'FUNGuild 기반 생태 기능 및 알레르기 유발균')">
            <img src="images/fig5_functional_guilds_allergens.png" alt="기능군 알레르겐" class="w-full h-full object-contain hover:scale-105 transition">
          </div>
        </div>
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 space-y-2">
          <h5 class="text-xs font-bold text-white">Fig 6. 공기생 공존 네트워크</h5>
          <div class="aspect-[16/10] bg-slate-950 rounded-xl overflow-hidden cursor-pointer" onclick="openFigureModal('images/fig6_cooccurrence_network.png', 'Fig 6. 공존 네트워크', '핵심 매개 허브(Irpex, Ceriporia) 구명')">
            <img src="images/fig6_cooccurrence_network.png" alt="공존 네트워크" class="w-full h-full object-contain hover:scale-105 transition">
          </div>
        </div>
      </div>
    </div>

    <!-- ========================================== -->
    <!-- CHAPTER 7: 환경 상관 & 아스팔트 보정 분석 -->
    <!-- ========================================== -->
    <div id="chapter-7" class="chapter-content hidden space-y-8">
      <div class="bg-gradient-to-r from-rose-950/70 to-slate-900 border border-rose-800/60 rounded-3xl p-6 shadow-xl">
        <div class="flex items-center gap-3 mb-2">
          <div class="w-10 h-10 rounded-2xl bg-rose-500/20 flex items-center justify-center text-rose-400 font-black">
            <i data-lucide="bar-chart-2" class="w-6 h-6"></i>
          </div>
          <div>
            <span class="text-xs font-bold text-rose-400 tracking-wider uppercase">Chapter 7. Environmental Correlations & Asphalt Correction</span>
            <h3 class="text-xl sm:text-2xl font-black text-white">제7장. 환경 요인 다변량 상관관계 및 아스팔트 포장 결측 정밀 보정</h3>
          </div>
        </div>
        <p class="text-xs sm:text-sm text-slate-300 leading-relaxed max-w-4xl">
          Site 5(주차장)의 불투수 아스팔트 포장에 따른 토양 결측치(NaN)를 공식 보정하고, 자연 산림 토양 315건만을 대상으로 Pairwise Deletion을 적용하여 토양 pH, 지온, 토양수분과 미생물 및 음이온 간의 정밀 상관관계를 도출하였습니다.
        </p>
      </div>

      <!-- Key Scientific Findings Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl space-y-2">
          <span class="text-xs font-bold text-amber-400">토양 산도 vs 부유진균</span>
          <h4 class="text-lg font-black text-white">r = -0.280 (p &lt; 0.001)</h4>
          <p class="text-xs text-slate-300 leading-relaxed">
            토양 산도가 낮을수록(산성 토양일수록) 사상균 및 버섯 포자의 발생 밀도가 유의하게 증가하여, 침엽수 낙엽층의 완만한 부식과 진균 생육의 연관성을 입증합니다.
          </p>
        </div>
        <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl space-y-2">
          <span class="text-xs font-bold text-rose-400">지온 vs 부유진균</span>
          <h4 class="text-lg font-black text-white">r = +0.243 (p &lt; 0.01)</h4>
          <p class="text-xs text-slate-300 leading-relaxed">
            여름철 지온 상승이 낙엽층 셀룰로오스 분해균(*Trichoderma*)의 대사 활성을 가속화하여 대기 중 포자 비산을 촉진하는 결정적 동력임을 규명하였습니다.
          </p>
        </div>
        <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl space-y-2">
          <span class="text-xs font-bold text-cyan-400">토양수분 vs 산림 음이온</span>
          <h4 class="text-lg font-black text-white">r = +0.458 (p &lt; 0.001)</h4>
          <p class="text-xs text-slate-300 leading-relaxed">
            토양 수분이 풍부할수록 수목의 증발산 작용과 수변 레너드 효과가 활성화되어 산림 대기 음이온 농도가 통계적으로 매우 강하게 증가함을 검증하였습니다.
          </p>
        </div>
      </div>

      <!-- Heatmap & Scatter Figures Showcase -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="bg-slate-900 border border-slate-800 rounded-3xl p-5 shadow-xl space-y-2">
          <h4 class="font-bold text-white text-sm">Fig 10. 음이온·미생물·환경요인 상관관계 히트맵 (아스팔트 보정 완료)</h4>
          <div class="aspect-[16/11] bg-slate-950 rounded-2xl overflow-hidden cursor-pointer" onclick="openFigureModal('images/10_음이온_미생물_환경요인_상관관계_히트맵.png', 'Fig 10. 상관관계 히트맵', '주차장 아스팔트 결측 보정 후 자연 토양 315건 기반 정밀 상관행렬')">
            <img src="images/10_음이온_미생물_환경요인_상관관계_히트맵.png" alt="상관관계 히트맵" class="w-full h-full object-contain hover:scale-105 transition">
          </div>
        </div>
        <div class="bg-slate-900 border border-slate-800 rounded-3xl p-5 shadow-xl space-y-2">
          <h4 class="font-bold text-white text-sm">Fig 11. 음이온·미생물·환경요인 다변량 산점도 및 선형 회귀선</h4>
          <div class="aspect-[16/11] bg-slate-950 rounded-2xl overflow-hidden cursor-pointer" onclick="openFigureModal('images/11_음이온_미생물_산점도_및_회귀선.png', 'Fig 11. 다변량 산점도 회귀선', '온습도, 토양환경과 음이온 농도 간의 회귀 모델')">
            <img src="images/11_음이온_미생물_산점도_및_회귀선.png" alt="산점도 및 회귀선" class="w-full h-full object-contain hover:scale-105 transition">
          </div>
        </div>
      </div>
    </div>

    <!-- ========================================== -->
    <!-- CHAPTER 8: 연구 그래픽 갤러리 & 다운로드 센터 -->
    <!-- ========================================== -->
    <div id="chapter-8" class="chapter-content hidden space-y-8">
      <div class="bg-gradient-to-r from-teal-950/70 to-slate-900 border border-teal-800/60 rounded-3xl p-6 shadow-xl">
        <div class="flex items-center gap-3 mb-2">
          <div class="w-10 h-10 rounded-2xl bg-teal-500/20 flex items-center justify-center text-teal-400 font-black">
            <i data-lucide="image" class="w-6 h-6"></i>
          </div>
          <div>
            <span class="text-xs font-bold text-teal-400 tracking-wider uppercase">Chapter 8. Scientific Graphics Gallery & Download Center</span>
            <h3 class="text-xl sm:text-2xl font-black text-white">제8장. 🖼️ 연구 출판용 그래픽 31종 갤러리 & 공식 데이터베이스 다운로드 센터</h3>
          </div>
        </div>
        <p class="text-xs sm:text-sm text-slate-300 leading-relaxed max-w-4xl">
          본 프로젝트에서 생산된 ITS 메타게놈 차세대 염기서열(Fig 1~12) 및 산림 음이온·미기후·CLHEI 생태지수(Fig 01~19) 총 31종의 고해상도 그래픽과 종합 학술 보고서(PDF), 연구 마스터 데이터베이스(Excel)를 전면 무료 개방합니다.
        </p>
      </div>

      <!-- Gallery Filter Tabs -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 flex flex-wrap items-center justify-between gap-3 shadow-lg">
        <div class="flex flex-wrap gap-2" id="galleryFilterGroup">
          <button onclick="filterGallery('all')" class="gallery-filter-btn gallery-filter-active px-3 py-1.5 rounded-xl bg-slate-800 text-xs font-bold transition">전체 31종 그래픽</button>
          <button onclick="filterGallery('dna')" class="gallery-filter-btn px-3 py-1.5 rounded-xl bg-slate-800 text-xs font-bold transition">🧬 DNA 메타게놈 (Fig 1~12)</button>
          <button onclick="filterGallery('ion')" class="gallery-filter-btn px-3 py-1.5 rounded-xl bg-slate-800 text-xs font-bold transition">💨 음이온 & 미기후 (Fig 01~16)</button>
          <button onclick="filterGallery('clhei')" class="gallery-filter-btn px-3 py-1.5 rounded-xl bg-slate-800 text-xs font-bold transition">🌿 생태지수 CLHEI (Fig 17~19)</button>
        </div>
        <span class="text-xs text-slate-400 font-medium">각 이미지를 클릭하시면 고해상도 확대 모달이 열립니다.</span>
      </div>

      <!-- 31 Gallery Cards Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5" id="galleryGrid">
        {gallery_cards_rendered}
      </div>

      <!-- Official Download Center -->
      <div class="bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-2xl space-y-6">
        <div class="border-b border-slate-800 pb-4">
          <h4 class="text-lg font-black text-white flex items-center gap-2">
            <i data-lucide="download-cloud" class="w-6 h-6 text-emerald-400"></i> 건국대학교 괴산학술림 공식 통합 연구 산출물 다운로드 센터
          </h4>
          <p class="text-xs sm:text-sm text-slate-400 mt-1">연구 보고서, 논문 작성용 데이터셋, 원시 계측 자료 전수를 원클릭으로 다운로드하실 수 있습니다.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <!-- Item 1: PDF Report -->
          <a href="괴산연습림_공기미생물_음이온_종합해석보고서.pdf" download class="p-5 rounded-2xl bg-slate-950/80 border border-slate-800 hover:border-emerald-500 transition duration-200 group flex items-start gap-4">
            <div class="w-12 h-12 rounded-xl bg-rose-500/10 text-rose-400 border border-rose-500/20 flex items-center justify-center shrink-0 group-hover:scale-105 transition">
              <i data-lucide="file-text" class="w-6 h-6"></i>
            </div>
            <div>
              <h5 class="text-sm font-bold text-white group-hover:text-emerald-400 transition">종합 학술 해석 보고서 (PDF)</h5>
              <p class="text-xs text-slate-400 mt-1">40쪽 분량의 풀 컬러 학술 보고서 (서론, 방법론, 분석, 고찰 전면 수록)</p>
              <span class="inline-block mt-2 text-[11px] text-emerald-400 font-semibold">PDF 다운로드 (4.73 MB) &rarr;</span>
            </div>
          </a>

          <!-- Item 2: Master Excel -->
          <a href="괴산연습림 전체데이터.xlsx" download class="p-5 rounded-2xl bg-slate-950/80 border border-slate-800 hover:border-emerald-500 transition duration-200 group flex items-start gap-4">
            <div class="w-12 h-12 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center justify-center shrink-0 group-hover:scale-105 transition">
              <i data-lucide="table" class="w-6 h-6"></i>
            </div>
            <div>
              <h5 class="text-sm font-bold text-white group-hover:text-emerald-400 transition">괴산학술림 전체 마스터 데이터 (Excel)</h5>
              <p class="text-xs text-slate-400 mt-1">7개 시기 348행 전수 데이터셋 (260910 가을철 및 아스팔트 NaN 보정 완료)</p>
              <span class="inline-block mt-2 text-[11px] text-emerald-400 font-semibold">Excel 다운로드 (.xlsx) &rarr;</span>
            </div>
          </a>

          <!-- Item 3: CLHEI Excel -->
          <a href="괴산학술림_기후생명건강지수_평가결과.xlsx" download class="p-5 rounded-2xl bg-slate-950/80 border border-slate-800 hover:border-emerald-500 transition duration-200 group flex items-start gap-4">
            <div class="w-12 h-12 rounded-xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 flex items-center justify-center shrink-0 group-hover:scale-105 transition">
              <i data-lucide="activity" class="w-6 h-6"></i>
            </div>
            <div>
              <h5 class="text-sm font-bold text-white group-hover:text-emerald-400 transition">기후생명건강지수(CLHEI) 평가 엑셀</h5>
              <p class="text-xs text-slate-400 mt-1">4대 서브지수(BSI, NVI, API, MBI) 지점별/수종별 산출표 및 판정 등급</p>
              <span class="inline-block mt-2 text-[11px] text-cyan-400 font-semibold">Excel 다운로드 (.xlsx) &rarr;</span>
            </div>
          </a>

          <!-- Item 4: Linkage Analysis Excel -->
          <a href="괴산연습림_공기미생물_음이온_종합연계분석.xlsx" download class="p-5 rounded-2xl bg-slate-950/80 border border-slate-800 hover:border-emerald-500 transition duration-200 group flex items-start gap-4">
            <div class="w-12 h-12 rounded-xl bg-blue-500/10 text-blue-400 border border-blue-500/20 flex items-center justify-center shrink-0 group-hover:scale-105 transition">
              <i data-lucide="bar-chart" class="w-6 h-6"></i>
            </div>
            <div>
              <h5 class="text-sm font-bold text-white group-hover:text-emerald-400 transition">공기미생물·음이온 종합연계분석 엑셀</h5>
              <p class="text-xs text-slate-400 mt-1">음이온 44,996건 통계, 시기별 산림vs밭 배율, 환경 상관행렬 수록</p>
              <span class="inline-block mt-2 text-[11px] text-blue-400 font-semibold">Excel 다운로드 (.xlsx) &rarr;</span>
            </div>
          </a>

          <!-- Item 5: Metagenome Summary Excel -->
          <a href="aerobiome_analysis_summary.xlsx" download class="p-5 rounded-2xl bg-slate-950/80 border border-slate-800 hover:border-emerald-500 transition duration-200 group flex items-start gap-4">
            <div class="w-12 h-12 rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/20 flex items-center justify-center shrink-0 group-hover:scale-105 transition">
              <i data-lucide="dna" class="w-6 h-6"></i>
            </div>
            <div>
              <h5 class="text-sm font-bold text-white group-hover:text-emerald-400 transition">메타게놈 분석 요약 워크북 (16개 시트)</h5>
              <p class="text-xs text-slate-400 mt-1">봄/여름 2회차 ITS NGS 분류군 동정표 및 10대 지점별 생태백과 원본</p>
              <span class="inline-block mt-2 text-[11px] text-purple-400 font-semibold">Excel 다운로드 (.xlsx) &rarr;</span>
            </div>
          </a>

          <!-- Item 6: Markdown Academic Report -->
          <a href="aerobiome_analysis_report.md" target="_blank" class="p-5 rounded-2xl bg-slate-950/80 border border-slate-800 hover:border-emerald-500 transition duration-200 group flex items-start gap-4">
            <div class="w-12 h-12 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/20 flex items-center justify-center shrink-0 group-hover:scale-105 transition">
              <i data-lucide="file-code" class="w-6 h-6"></i>
            </div>
            <div>
              <h5 class="text-sm font-bold text-white group-hover:text-emerald-400 transition">학술 연구 보고서 전문 (Markdown)</h5>
              <p class="text-xs text-slate-400 mt-1">GitHub 호환 마크다운 전문 문서 (수식, 통계표, 인용 문헌 포함)</p>
              <span class="inline-block mt-2 text-[11px] text-amber-400 font-semibold">마크다운 열람 (.md) &rarr;</span>
            </div>
          </a>
        </div>
      </div>
    </div>
  </main>

  <!-- Modal for High-res Figure Viewing -->
  <div id="figureModal" class="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
    <div class="bg-slate-900 border border-slate-700 rounded-3xl max-w-4xl w-full max-h-[90vh] flex flex-col shadow-2xl overflow-hidden animate-in fade-in zoom-in duration-200">
      <div class="flex items-center justify-between px-6 py-4 border-b border-slate-800">
        <div>
          <h3 id="modalTitle" class="text-base sm:text-lg font-black text-white">Figure Preview</h3>
          <p id="modalDesc" class="text-xs text-slate-400 mt-0.5">Figure description</p>
        </div>
        <button onclick="closeFigureModal()" class="w-9 h-9 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 flex items-center justify-center transition">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>
      <div class="p-4 flex-1 overflow-auto bg-slate-950 flex items-center justify-center">
        <img id="modalImg" src="" alt="Figure Preview" class="max-h-[70vh] max-w-full object-contain rounded-xl shadow-lg">
      </div>
      <div class="px-6 py-3 border-t border-slate-800 flex justify-end">
        <a id="modalDownload" href="" download class="text-xs px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 font-bold transition flex items-center gap-1.5 text-white">
          <i data-lucide="download" class="w-4 h-4"></i> 고해상도 원본 다운로드
        </a>
      </div>
    </div>
  </div>

  <!-- Footer -->
  <footer class="bg-slate-950 border-t border-slate-800 text-slate-400 text-xs py-10 px-4 mt-16">
    <div class="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-center sm:text-left">
      <div>
        <h5 class="text-sm font-black text-slate-200">건국대학교 상허생명과학대학 부속 학술림 (괴산연습림)</h5>
        <p class="text-[11px] text-slate-500 mt-1">공기미생물(Aerobiome) · 산림 음이온 · 기후생명건강지수(CLHEI) 전주기 분석 플랫폼</p>
      </div>
      <div class="text-[11px] text-slate-500">
        <p>충청북도 괴산군 불정면 신흥리 산 11-1 | 기상청 불정면 AWS (지점코드 685)</p>
        <p class="mt-0.5">&copy; 2026 Konkuk University Aerobiome & Forest Healing Research Group. All Rights Reserved.</p>
      </div>
    </div>
  </footer>

  <!-- Scripts -->
  <script>
    // Embedded Datasets
    const siteMetricData = {site_metric_data_json};
    const siteEncyclopediaData = {site_encyclopedia_data_json};
    const figuresData = {figures_data_json};

    // State Variables
    let currentChapter = 1;
    let currentChartDate = 'all';
    let currentChartMetric = 'TAF_CFU_m3';
    let interactiveSiteChart = null;
    let ionSpeciesChart = null;
    let clheiRadarChart = null;
    let currentStandCategory = 'all';
    let currentGalleryCategory = 'all';

    // Chapter Navigation
    function switchChapter(chNum) {{
      currentChapter = chNum;
      
      // Hide all chapters
      document.querySelectorAll('.chapter-content').forEach(el => el.classList.add('hidden'));
      
      // Show selected chapter
      const activeChEl = document.getElementById('chapter-' + chNum);
      if (activeChEl) activeChEl.classList.remove('hidden');

      // Update Nav Tabs
      document.querySelectorAll('#chapterNavTabs .chapter-tab').forEach(btn => btn.classList.remove('chapter-tab-active'));
      const activeNavBtn = document.getElementById('nav-ch' + chNum);
      if (activeNavBtn) activeNavBtn.classList.add('chapter-tab-active');

      // Scroll to top
      window.scrollTo({{ top: 0, behavior: 'smooth' }});

      // Update URL hash
      window.history.replaceState(null, null, '#chapter-' + chNum);

      // Trigger chart initializations / resizing
      setTimeout(() => {{
        if (chNum === 2) {{
          if (!interactiveSiteChart) initInteractiveSiteChart();
          else interactiveSiteChart.resize();
        }} else if (chNum === 3) {{
          if (!ionSpeciesChart) initIonSpeciesChart();
          else ionSpeciesChart.resize();
        }} else if (chNum === 4) {{
          if (!clheiRadarChart) initClheiRadarChart();
          else clheiRadarChart.resize();
        }}
        lucide.createIcons();
      }}, 50);
    }}

    // Chapter 2 Interactive Chart
    const siteLabels = [
      '#1 리기다소나무', '#2 잣나무 a', '#3 버들나무 a', '#4 밭 (대조구)', '#5 주차장 (대조구)',
      '#6 소나무', '#7 낙엽송 a', '#8 버들나무 b', '#9 낙엽송 b', '#10 잣나무 b'
    ];

    function initInteractiveSiteChart() {{
      const ctx = document.getElementById('interactiveSiteChartCanvas').getContext('2d');
      const d = siteMetricData[currentChartDate] || siteMetricData['all'];
      const vals = d[currentChartMetric] || [];

      interactiveSiteChart = new Chart(ctx, {{
        type: 'bar',
        data: {{
          labels: siteLabels,
          datasets: [{{
            label: getMetricLabel(currentChartMetric),
            data: vals,
            backgroundColor: siteLabels.map((l, i) => {{
              if (i === 3) return '#f43f5e'; // Field (Rose)
              if (i === 4) return '#94a3b8'; // Parking (Slate)
              return '#10b981'; // Forest (Emerald)
            }}),
            borderRadius: 8,
            borderSkipped: false
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ display: false }},
            tooltip: {{
              backgroundColor: '#0f172a',
              titleColor: '#e2e8f0',
              bodyColor: '#38bdf8',
              borderColor: '#334155',
              borderWidth: 1,
              padding: 10,
              callbacks: {{
                label: function(c) {{
                  return c.raw !== null ? c.raw + ' ' + getMetricUnit(currentChartMetric) : '측정 불가 (NaN - 아스팔트)';
                }}
              }}
            }}
          }},
          scales: {{
            x: {{
              ticks: {{ color: '#94a3b8', font: {{ size: 11 }} }},
              grid: {{ display: false }}
            }},
            y: {{
              ticks: {{ color: '#94a3b8', font: {{ size: 11 }} }},
              grid: {{ color: '#1e293b' }}
            }}
          }}
        }}
      }});
    }}

    function getMetricLabel(m) {{
      const labels = {{
        'TAF_CFU_m3': '총부유진균 (TAF)',
        'TAB_CFU_m3': '총부유세균 (TAB)',
        'n-ion': '산림 음이온 발생량',
        'air-temp': '임내 기온',
        'air-RH': '임내 상대습도',
        'PM10': '미세먼지 PM10'
      }};
      return labels[m] || m;
    }}

    function getMetricUnit(m) {{
      const units = {{
        'TAF_CFU_m3': 'CFU/㎥',
        'TAB_CFU_m3': 'CFU/㎥',
        'n-ion': '개/㎤',
        'air-temp': '℃',
        'air-RH': '%',
        'PM10': '㎍/㎥'
      }};
      return units[m] || '';
    }}

    function changeChartDate(dKey) {{
      currentChartDate = dKey;
      document.querySelectorAll('#dateFilterGroup .date-pill').forEach(btn => btn.classList.remove('date-pill-active'));
      event.target.classList.add('date-pill-active');
      updateInteractiveSiteChart();
    }}

    function changeChartMetric(mKey) {{
      currentChartMetric = mKey;
      document.querySelectorAll('.metric-pill').forEach(btn => btn.classList.remove('metric-pill-active'));
      event.target.classList.add('metric-pill-active');
      updateInteractiveSiteChart();
    }}

    function updateInteractiveSiteChart() {{
      if (!interactiveSiteChart) return;
      const d = siteMetricData[currentChartDate] || siteMetricData['all'];
      const vals = d[currentChartMetric] || [];

      interactiveSiteChart.data.datasets[0].label = getMetricLabel(currentChartMetric);
      interactiveSiteChart.data.datasets[0].data = vals;
      interactiveSiteChart.update();
    }}

    // Chapter 3 Ion Chart
    function initIonSpeciesChart() {{
      const ctx = document.getElementById('ionSpeciesChartCanvas').getContext('2d');
      ionSpeciesChart = new Chart(ctx, {{
        type: 'bar',
        data: {{
          labels: ['일본잎갈나무(낙엽송)', '소나무림', '잣나무림', '버들나무림', '주차장(대조구)', '밭(대조구)'],
          datasets: [{{
            label: '음이온 평균 발생량 (개/㎤)',
            data: [2965.5, 2196.7, 1758.2, 1489.0, 1235.0, 934.6],
            backgroundColor: ['#06b6d4', '#0ea5e9', '#3b82f6', '#10b981', '#64748b', '#f43f5e'],
            borderRadius: 8
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ display: false }},
            tooltip: {{
              backgroundColor: '#0f172a',
              callbacks: {{
                label: function(c) {{
                  const ratio = (c.raw / 934.6).toFixed(2);
                  return c.raw.toLocaleString() + ' 개/㎤ (밭 대비 ' + ratio + '배)';
                }}
              }}
            }}
          }},
          scales: {{
            x: {{ ticks: {{ color: '#94a3b8' }}, grid: {{ display: false }} }},
            y: {{ ticks: {{ color: '#94a3b8' }}, grid: {{ color: '#1e293b' }} }}
          }}
        }}
      }});
    }}

    // Chapter 4 CLHEI Radar Chart
    function initClheiRadarChart() {{
      const ctx = document.getElementById('clheiRadarCanvas').getContext('2d');
      clheiRadarChart = new Chart(ctx, {{
        type: 'radar',
        data: {{
          labels: ['생체안락도 (BSI)', '천연활력도 (NVI)', '대기청정도 (API)', '미생물건전도 (MBI)'],
          datasets: [
            {{
              label: '소나무류 (81.9점)',
              data: [86.9, 63.6, 85.9, 87.9],
              backgroundColor: 'rgba(16, 185, 129, 0.2)',
              borderColor: '#10b981',
              pointBackgroundColor: '#10b981'
            }},
            {{
              label: '낙엽송류 (77.7점)',
              data: [83.8, 58.9, 78.6, 87.1],
              backgroundColor: 'rgba(6, 182, 212, 0.2)',
              borderColor: '#06b6d4',
              pointBackgroundColor: '#06b6d4'
            }},
            {{
              label: '잣나무류 (78.4점)',
              data: [86.1, 56.2, 79.8, 87.9],
              backgroundColor: 'rgba(59, 130, 246, 0.2)',
              borderColor: '#3b82f6',
              pointBackgroundColor: '#3b82f6'
            }},
            {{
              label: '밭 대조구 (71.3점)',
              data: [68.6, 47.0, 87.9, 80.2],
              backgroundColor: 'rgba(244, 63, 94, 0.2)',
              borderColor: '#f43f5e',
              pointBackgroundColor: '#f43f5e',
              borderDash: [5, 5]
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{
              labels: {{ color: '#e2e8f0', font: {{ size: 11 }} }}
            }}
          }},
          scales: {{
            r: {{
              angleLines: {{ color: '#334155' }},
              grid: {{ color: '#1e293b' }},
              pointLabels: {{ color: '#94a3b8', font: {{ size: 12, weight: 'bold' }} }},
              suggestedMin: 40,
              suggestedMax: 100,
              ticks: {{ color: '#64748b', backdropColor: 'transparent' }}
            }}
          }}
        }}
      }});
    }}

    // Chapter 5 Stand Filters & Search
    function filterSiteCards(cat) {{
      currentStandCategory = cat;
      document.querySelectorAll('#standFilterGroup .stand-filter-btn').forEach(btn => btn.classList.remove('stand-filter-active'));
      event.target.classList.add('stand-filter-active');
      
      const cards = document.querySelectorAll('#siteEncyclopediaGrid .site-card');
      cards.forEach(card => {{
        const cardCat = card.getAttribute('data-category');
        if (cat === 'all' || cardCat === cat) {{
          card.style.display = 'flex';
        }} else {{
          card.style.display = 'none';
        }}
      }});
    }}

    function searchSiteCards() {{
      const q = document.getElementById('siteSearchInput').value.toLowerCase().trim();
      const cards = document.querySelectorAll('#siteEncyclopediaGrid .site-card');
      
      cards.forEach(card => {{
        const siteNo = parseInt(card.getAttribute('data-no'));
        const site = siteEncyclopediaData.find(s => s.no === siteNo);
        if (!site) return;
        
        const text = (site.name + ' ' + site.latin + ' ' + site.microbeTraits + ' ' + site.plantMicrobe + ' ' + site.catName + ' ' + JSON.stringify(site.springDna) + ' ' + JSON.stringify(site.summerDna)).toLowerCase();
        const matchesCategory = (currentStandCategory === 'all' || site.category === currentStandCategory);
        const matchesQuery = (!q || text.includes(q));

        if (matchesCategory && matchesQuery) {{
          card.style.display = 'flex';
        }} else {{
          card.style.display = 'none';
        }}
      }});
    }}

    // Chapter 8 Gallery Filters
    function filterGallery(cat) {{
      currentGalleryCategory = cat;
      document.querySelectorAll('#galleryFilterGroup .gallery-filter-btn').forEach(btn => btn.classList.remove('gallery-filter-active'));
      event.target.classList.add('gallery-filter-active');

      const cards = document.querySelectorAll('#galleryGrid .figure-card');
      cards.forEach(card => {{
        const cCat = card.getAttribute('data-cat');
        if (cat === 'all' || cCat === cat) {{
          card.style.display = 'flex';
        }} else {{
          card.style.display = 'none';
        }}
      }});
    }}

    // High-res Figure Modal
    function openFigureModal(src, title, desc) {{
      document.getElementById('modalImg').src = src;
      document.getElementById('modalTitle').innerText = title;
      document.getElementById('modalDesc').innerText = desc;
      document.getElementById('modalDownload').href = src;
      document.getElementById('figureModal').classList.remove('hidden');
    }}

    function closeFigureModal() {{
      document.getElementById('figureModal').classList.add('hidden');
    }}

    // Close modal on Escape
    document.addEventListener('keydown', function(e) {{
      if (e.key === 'Escape') closeFigureModal();
    }});

    // Initialize on DOM load
    document.addEventListener('DOMContentLoaded', () => {{
      lucide.createIcons();

      // Check URL hash for initial chapter
      const hash = window.location.hash;
      if (hash && hash.startsWith('#chapter-')) {{
        const ch = parseInt(hash.replace('#chapter-', ''));
        if (ch >= 1 && ch <= 8) {{
          switchChapter(ch);
          return;
        }}
      }}
      switchChapter(1);
    }});
  </script>
</body>
</html>
'''

# Write to docs/index.html
with open('docs/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
print("Successfully written to docs/index.html (bytes:", len(html_content), ")")

# Write to root index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
print("Successfully written to index.html (bytes:", len(html_content), ")")

print("Integrated portal build completed successfully!")
