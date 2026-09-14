from pathlib import Path

script_path = Path("scripts/generate_web_and_pdf.py")
with open(script_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update navigation
old_nav = '<a href="#regression" class="nav-link">다변량 회귀분석</a>\n        <a href="#downloads" class="nav-link">산출물 다운로드</a>'
new_nav = '<a href="#regression" class="nav-link">다변량 회귀분석</a>\n        <a href="#clhei" class="nav-link" style="color:#fca311; font-weight:700;">기후생명건강지수 (CLHEI)</a>\n        <a href="#downloads" class="nav-link">산출물 다운로드</a>'

if old_nav in content:
    content = content.replace(old_nav, new_nav)
    print('[OK] Nav updated')
else:
    print('[Warning] old_nav not found')

# 2. Section for CLHEI
clhei_section = '''
    <!-- Section: 기후생명건강 생태지수 (CLHEI) -->
    <section class="section" id="clhei">
        <div class="section-header">
            <h2>🌿 차세대 생태계 평가 지표: 기후·생명·건강 생태지수 (CLHEI) 기획 및 실증</h2>
            <span class="badge" style="background:#2d6a4f;">신규 지표 모델</span>
        </div>

        <div class="callout" style="background:#e8f5e9; border-left-color:#2e7d32;">
            <strong>기후·생명·건강 생태지수 (CLHEI: Climate-Life-Health Ecological Index) 개발 배경</strong>:<br>
            기존의 대기질 지수(AQI, CAI)는 인위적 물리·화학적 오염물질만 감시할 뿐, 숲의 적극적인 생리활성물질(공기음이온)이나 공기미생물(세균·진균 포자)의 알레르기 위해성, 그리고 수관층의 미기후 완충(폭염 냉각) 혜택을 전혀 반영하지 못했습니다.<br>
            이에 본 연구는 괴산학술림 298건 전수 실측 데이터를 기반으로 <strong>4대 핵심 축(생물청정도 BSI 30% + 자연치유력 NVI 30% + 대기순도 API 20% + 미기후완충 MBI 20%)</strong>을 결합한 100점 만점 척도의 생태계 건강성 평가지표를 세계 최초로 기획·구축하였습니다.
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
            <img src="figures/18_기후생명건강지수_6개시기_계절추세.png" alt="6개시기 계절추세">
            <div class="chart-caption">[그림 3] 6개 조사 시기별 서브 인덱스 동태 및 산림 vs 밭(대조구) 지수 방어 격차 추이</div>
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
                        <td class="text-right">61.1</td>
                        <td class="text-right text-success"><strong>84.2</strong> (1위)</td>
                        <td class="text-right">86.6</td>
                        <td class="text-right text-success"><strong>81.1점</strong></td>
                        <td class="text-center"><span class="badge" style="background:#2e7d32;">2등급 (우수)</span></td>
                        <td><strong>피톤치드 사상균(진균) 억제 최우수</strong> (알레르기 비염, 천식, 아토피)</td>
                    </tr>
                    <tr>
                        <td><strong>버드나무류</strong> (버드나무 a, b)</td>
                        <td class="text-right">75.1</td>
                        <td class="text-right text-success"><strong>65.0</strong> (1위, 8월 85+)</td>
                        <td class="text-right">79.9</td>
                        <td class="text-right text-success"><strong>86.7</strong> (1위)</td>
                        <td class="text-right"><strong>76.9점</strong></td>
                        <td class="text-center"><span class="badge" style="background:#2e7d32;">2등급 (우수)</span></td>
                        <td><strong>음이온 방출량 1위 + 하계 냉각 1위</strong> (호흡기 환자, 노약자 회복길)</td>
                    </tr>
                    <tr>
                        <td><strong>잣나무류</strong> (잣나무 a, b)</td>
                        <td class="text-right">85.2</td>
                        <td class="text-right">54.1</td>
                        <td class="text-right">77.3</td>
                        <td class="text-right">86.3</td>
                        <td class="text-right"><strong>77.3점</strong></td>
                        <td class="text-center"><span class="badge" style="background:#2e7d32;">2등급 (우수)</span></td>
                        <td>세균 극저 청정림, 상록 침엽수의 사계절 안정적 면역 환경</td>
                    </tr>
                    <tr>
                        <td><strong>낙엽송류</strong> (일본잎갈나무 a, b)</td>
                        <td class="text-right">81.8</td>
                        <td class="text-right">53.8</td>
                        <td class="text-right">75.7</td>
                        <td class="text-right">85.6</td>
                        <td class="text-right"><strong>75.5점</strong></td>
                        <td class="text-center"><span class="badge" style="background:#2e7d32;">2등급 (우수)</span></td>
                        <td>잎 전엽 후 하계 수관 차폐율 및 일사 차단 우수</td>
                    </tr>
                    <tr style="background:#ffebee;">
                        <td><strong>밭 (기준 대조구)</strong></td>
                        <td class="text-right text-highlight"><strong>66.7</strong> (최하위)</td>
                        <td class="text-right text-highlight"><strong>43.9</strong> (최하위)</td>
                        <td class="text-right">86.4</td>
                        <td class="text-right text-highlight"><strong>77.9</strong> (최하위)</td>
                        <td class="text-right text-highlight"><strong>69.9점</strong></td>
                        <td class="text-center"><span class="badge" style="background:#c62828;">3등급 (최하위)</span></td>
                        <td><strong>진균 포자 다량 부유, 음이온 결핍, 폭염 노출 (치유 부적합)</strong></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </section>
'''

if '<section class="section" id="downloads">' in content:
    content = content.replace('<section class="section" id="downloads">', clhei_section + '\n    <section class="section" id="downloads">')
    print('[OK] CLHEI section inserted')
else:
    print('[Warning] downloads section not found')

# 3. Add to downloads table
old_dl = '''                    <tr>
                        <td><strong>연구 보고서 Markdown</strong></td>
                        <td><code>괴산연습림_공기미생물_음이온_종합해석보고서.md</code></td>
                        <td>학술 마크다운 전문 보고서 (도표 및 선행연구 분석 포함)</td>
                        <td class="text-center"><a href="괴산연습림_공기미생물_음이온_종합해석보고서.md" class="btn btn-outline" style="color:black; border-color:#ccc; padding:0.3rem 0.8rem; font-size:0.8rem;" download>MD 받기</a></td>
                    </tr>'''

new_dl = old_dl + '''
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
                    </tr>'''

if old_dl in content:
    content = content.replace(old_dl, new_dl)
    print('[OK] Downloads table updated')
else:
    print('[Warning] old_dl not found')

with open(script_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('[OK] Updated scripts/generate_web_and_pdf.py successfully!')
