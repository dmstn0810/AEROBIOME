# 건국대학교 학술림(괴산) 공기미생물(Aerobiome) 전주기 분석 플랫폼

> **공식 인터랙티브 웹 대시보드**: [https://dmstn0810.github.io/AEROBIOME/](https://dmstn0810.github.io/AEROBIOME/)  
> **조사 대상지**: 충청북도 괴산군 불정면/장연면 건국대학교 학술림 10대 고정 조사구  
> **연구 데이터**: 2026년 3월~8월 6대 조사 전수 배양 농도(N=298), 기상청 괴산 불정면 AWS 종관 기상, 현장 미기후·토양 환경, 2회차(봄·여름) 공기진균 ITS 메타게놈 차세대 염기서열(2,091,638 reads)

---

## 📌 연구 개요 (Overview)
본 프로젝트는 건국대학교 괴산 학술림의 산림 대기 미생물상(Airborne Fungal & Bacterial Aerobiome)을 규명하기 위해, **에어 샘플러 포집 유량(0.1 ㎥) 기준 절대 농도(CFU/㎥ = Count/0.1) 정량화**, **기상청 AWS 및 현장 미기후 결측치 대치**, **ITS 메타게놈 차세대 염기서열분석(NGS)**, **공기생 공존 네트워크(Co-occurrence Network)**, 그리고 **환경부 실내공기질 다중이용시설 권고기준(세균 800 CFU/㎥, 진균 500 CFU/㎥)**과의 비교를 통합 수행한 종합 연구 분석 플랫폼입니다.

---

## 📊 주요 분석 결과 (Key Findings)

1. **거시적 바이오에어로졸 농도 궤적 (6대 조사 시계열, N=298)**:
   - **총부유세균 (TAB)**: 연중 $8.8 \sim 94.8\,\text{CFU/m}^3$ (여름 평균 $29.8\,\text{CFU/m}^3$)로 **환경부 실내 권고기준(800 CFU/㎥) 대비 1~12% 수준의 완벽한 청정성**을 입증.
   - **총부유진균 (TAF)**: 3월 초봄($330.7\,\text{CFU/m}^3$, 14.6% 초과) $\rightarrow$ 7월 한여름(**$1,086.0\,\text{CFU/m}^3$, 68% 초과**).
   - **자연 초과 메커니즘**: 실내 곰팡이 오염과 달리, 고온다습 다우기(기온 28.7℃, 습도 77.8%, 장마 3일 누적강수 64.6mm)에 의한 **토양 유기물 분해균(*Trichoderma*) 및 버섯 담자포자의 자연스러운 방출 현상**.
   - **진균/세균 비(F/B Ratio)**: 여름철 **36.4:1**로 자연 온대림 고유의 바이오에어로졸 지문 확인.

2. **미시적 DNA 메타게놈 종 구조 연계 (2,091,638 reads)**:
   - **봄철 (04/15, 진균 789 CFU/㎥)**: 엽면 피생균 및 호흡기 알레르겐 우점 $\rightarrow$ *Capnodiales_sp.* (42.4%), *Cladosporium* (14.1%), *Penicillium* (13.5%), *Alternaria* (6.4%). 건조 강풍(7.6m/s, 최대 16.3m/s) 비산.
   - **여름철 (07/27, 진균 1,086 CFU/㎥)**: 토양 사상균 및 목재부후균 폭발 $\rightarrow$ *Trichoderma hamatum/harzianum* (37.9%), *Fusarium oxysporum* (15.0%), *Coprinellus radians* (10.4%).

3. **10대 조사지점별 시공간 핫스팟**:
   - **밭 (대조구, Site 4)**: 여름철 **$2,464.0\,\text{CFU/m}^3$ (전 지점 최고치)**, *Fusarium*(45.1%) 등 지표면 교란 사상균 우점.
   - **버들나무림 (수변 저습지, Site 3, 8)**: 연중 $700 \sim 1,672\,\text{CFU/m}^3$ 고농도 유지, 활엽수 탄저병균(*Colletotrichum* 12.4%) 우점.
   - **잣나무림 a (Stand A, Site 2)**: 여름철 **$2,104.0\,\text{CFU/m}^3$**, 산림 낙엽층 최고 수준의 분해 활성 발현.
   - **주차장 (대조구, Site 5)**: **연중 평균 $363.9\,\text{CFU/m}^3$ (전 지점 최저치)**, 유일하게 실내 권고기준(500)을 상시 충족하는 음성 대조군.
   - **소나무림 (Site 6)**: 목재 백색부후균 *Coprinellus radians*(59.4%) 우점.
   - **낙엽송림 a (Site 7)**: 연중 평균 $444.3\,\text{CFU/m}^3$로 쾌적하여 가장 추천되는 산림치유 힐링 코스.

4. **공기생 상호작용 네트워크**:
   - 봄철 모듈(피생균-알레르겐) vs 여름철 모듈(토양분해균-병원균) 간의 뚜렷한 상호배제(음의 상관)와 계절적 생태 지위 교체(Niche turnover) 증명.
   - 매개 핵심 허브(Keystone Taxa): *Irpex*, *Ceriporia*.

---

## 📁 저장소 디렉토리 구조 (Repository Structure)

```
AEROBIOME/
├── docs/                               # GitHub Pages 배포 디렉토리
│   ├── index.html                      # 전주기 인터랙티브 웹 대시보드
│   ├── aerobiome_analysis_summary.xlsx # 15개 시트 마스터 데이터 워크북
│   └── images/                         # 연구 출판용 고해상도 그래픽 (Fig 1 ~ Fig 12)
│       ├── fig1_seasonal_alpha_diversity.png
│       ├── fig2_phylum_class_composition.png
│       ├── fig3_top_genera_heatmap.png
│       ├── fig4_beta_diversity_pcoa.png
│       ├── fig5_functional_guilds_allergens.png
│       ├── fig6_cooccurrence_network.png
│       ├── fig7_microbe_environment_correlation.png
│       ├── fig8_bioaerosol_concentration.png
│       ├── fig9_all6dates_longitudinal_trends.png
│       ├── fig10_all6dates_spatiotemporal_heatmap.png
│       ├── fig11_all6dates_environmental_correlations.png
│       └── fig12_dna_macro_integration.png
├── ASV_table_260415.biom               # 1차(봄) NGS ASV 테이블 (HDF5)
├── ASV_table_260727.biom               # 2차(여름) NGS ASV 테이블 (JSON)
├── TAXONOMY_Assignment_260415.xlsx     # 1차 분류군 동정표 (UNITE)
├── TAXONOMY_Assignment_260727.xlsx     # 2차 분류군 동정표 (UNITE)
├── 괴산연습림 전체데이터.xlsx          # 6대 조사 전수 원본 데이터
├── aerobiome_analysis_summary.xlsx     # 통합 분석 엑셀
├── .gitignore
└── README.md
```

---

## 💻 로컬 실행 방법 (Local Execution)
```bash
# 저장소 복제
git clone https://github.com/dmstn0810/AEROBIOME.git
cd AEROBIOME

# docs 폴더에서 로컬 HTTP 서버 실행
python -m http.server 8080 --directory docs

# 브라우저에서 접속
http://localhost:8080
```
