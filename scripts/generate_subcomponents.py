import json
import os

print("Starting build_integrated_portal.py...")

# Load precomputed data
with open('site_metric_data_7dates.json', 'r', encoding='utf-8') as f:
    site_metric_data = json.load(f)

# Import prepare_portal_data
import scripts.prepare_portal_data as ppd
site_encyclopedia_data = ppd.site_encyclopedia_data
figures_data = ppd.figures_data

site_metric_data_json = json.dumps(site_metric_data, ensure_ascii=False)
site_encyclopedia_data_json = json.dumps(site_encyclopedia_data, ensure_ascii=False)
figures_data_json = json.dumps(figures_data, ensure_ascii=False)

# Generate HTML Cards for Chapter 2/5 (10 sites)
def render_site_cards():
    html_cards = []
    for s in site_encyclopedia_data:
        spring_dna_html = "".join([f'<span class="inline-block px-2 py-0.5 rounded text-[11px] bg-purple-900/40 text-purple-200 border border-purple-700/50 mr-1 mb-1 font-mono">{d["g"]} ({d["pct"]}%)</span>' for d in s["springDna"]])
        summer_dna_html = "".join([f'<span class="inline-block px-2 py-0.5 rounded text-[11px] bg-emerald-900/40 text-emerald-200 border border-emerald-700/50 mr-1 mb-1 font-mono">{d["g"]} ({d["pct"]}%)</span>' for d in s["summerDna"]])
        
        soil_display = f'<span class="text-amber-300 font-bold">{s["soilPh"]}</span> · <span class="text-sky-300 font-bold">{s["soilMoist"]}</span>'
        if s["no"] == 5:
            soil_display = '<span class="px-2 py-0.5 rounded bg-rose-900/80 text-rose-200 text-xs font-bold border border-rose-600">⚠️ 아스팔트 포장 (물리적 측정 불가, NaN 공식 보정)</span>'

        card = f'''
        <div class="site-card bg-slate-900/90 border border-slate-700/80 rounded-2xl p-5 shadow-xl flex flex-col justify-between hover:border-emerald-500/60 transition duration-200" data-no="{s["no"]}" data-category="{s["category"]}">
          <div>
            <!-- Header -->
            <div class="flex items-start justify-between gap-2 border-b border-slate-800 pb-3 mb-3">
              <div>
                <div class="flex items-center gap-2">
                  <span class="w-6 h-6 rounded-full bg-emerald-500/20 text-emerald-400 font-black text-xs flex items-center justify-center border border-emerald-500/30">#{s["no"]}</span>
                  <h3 class="text-base sm:text-lg font-black text-white">{s["name"]}</h3>
                </div>
                <p class="text-[11px] font-serif italic text-emerald-400/90 mt-0.5">{s["latin"]}</p>
                <span class="inline-block mt-1 text-[10px] font-semibold px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">{s["catName"]}</span>
              </div>
              <div class="text-right shrink-0">
                <span class="text-xs px-2.5 py-1 rounded-full bg-emerald-950 text-emerald-300 font-bold border border-emerald-700/60">{s["grade"]}</span>
                <div class="text-[11px] text-slate-400 mt-1">CLHEI <strong class="text-emerald-400 text-sm">{s["clhei"]}점</strong></div>
              </div>
            </div>

            <!-- Key Metrics Badges -->
            <div class="grid grid-cols-3 gap-2 mb-3 text-center">
              <div class="bg-slate-800/80 rounded-xl p-2 border border-slate-700/50">
                <div class="text-[10px] text-slate-400">부유진균 (연중)</div>
                <div class="text-xs sm:text-sm font-black text-amber-400 mt-0.5">{s["tafMean"]} <span class="text-[9px] font-normal text-slate-400">CFU/㎥</span></div>
              </div>
              <div class="bg-slate-800/80 rounded-xl p-2 border border-slate-700/50">
                <div class="text-[10px] text-slate-400">부유세균 (연중)</div>
                <div class="text-xs sm:text-sm font-black text-emerald-400 mt-0.5">{s["tabMean"]} <span class="text-[9px] font-normal text-slate-400">CFU/㎥</span></div>
              </div>
              <div class="bg-slate-800/80 rounded-xl p-2 border border-slate-700/50">
                <div class="text-[10px] text-slate-400">산림 음이온</div>
                <div class="text-xs sm:text-sm font-black text-cyan-400 mt-0.5">{s["nIonMean"]} <span class="text-[9px] font-normal text-slate-400">개/㎤</span></div>
              </div>
            </div>

            <!-- Environmental Condition -->
            <div class="bg-slate-950/60 rounded-xl p-2.5 border border-slate-800 text-xs text-slate-300 mb-3 space-y-1">
              <div class="flex items-center gap-1 text-[11px] text-slate-400">
                <i data-lucide="map-pin" class="w-3.5 h-3.5 text-emerald-400 shrink-0"></i>
                <span>위치: <strong>{s["location"]}</strong></span>
              </div>
              <div class="flex items-center gap-1 text-[11px] text-slate-400">
                <i data-lucide="layers" class="w-3.5 h-3.5 text-amber-400 shrink-0"></i>
                <span>토양 환경: {soil_display}</span>
              </div>
              <div class="flex items-center gap-1 text-[11px] text-slate-400">
                <i data-lucide="activity" class="w-3.5 h-3.5 text-rose-400 shrink-0"></i>
                <span>피크 농도: <strong>{s["peak"]}</strong></span>
              </div>
            </div>

            <!-- DNA Profiles -->
            <div class="space-y-2 mb-3">
              <div>
                <div class="text-[11px] font-bold text-purple-300 flex items-center gap-1 mb-1">
                  <i data-lucide="dna" class="w-3.5 h-3.5"></i> 봄철 메타게놈 우점 (04/15):
                </div>
                <div>{spring_dna_html}</div>
              </div>
              <div>
                <div class="text-[11px] font-bold text-emerald-300 flex items-center gap-1 mb-1">
                  <i data-lucide="dna" class="w-3.5 h-3.5"></i> 여름철 메타게놈 우점 (07/27):
                </div>
                <div>{summer_dna_html}</div>
              </div>
            </div>

            <!-- Ecological Traits -->
            <div class="text-xs text-slate-300 leading-relaxed bg-slate-800/40 rounded-xl p-3 border border-slate-700/60 mb-3 space-y-2">
              <p><strong class="text-emerald-300">생태 동태:</strong> {s["microbeTraits"]}</p>
              <p><strong class="text-teal-300">임목-미생물 상호작용:</strong> {s["plantMicrobe"]}</p>
              <p><strong class="text-amber-300">물질 순환:</strong> {s["nutrientCycling"]}</p>
            </div>
          </div>

          <!-- Forest Healing Recommendation -->
          <div class="pt-3 border-t border-slate-800/90 text-xs">
            <div class="flex items-start gap-1.5 bg-emerald-950/40 border border-emerald-800/40 rounded-xl p-2.5 text-emerald-200">
              <i data-lucide="sparkles" class="w-4 h-4 text-emerald-400 shrink-0 mt-0.5"></i>
              <div>
                <strong class="text-emerald-300 block mb-0.5">산림 치유 가이드:</strong>
                <span class="text-[11px] text-slate-300">{s["healthGuide"]}</span>
              </div>
            </div>
          </div>
        </div>
        '''
        html_cards.append(card)
    return "\n".join(html_cards)

site_cards_rendered = render_site_cards()

# Generate HTML Gallery Cards for Chapter 8 (31 figures)
def render_gallery_cards():
    gallery_html = []
    for f in figures_data:
        badge_color = "bg-purple-900/60 text-purple-300 border-purple-700" if f["cat"] == "dna" else ("bg-cyan-900/60 text-cyan-300 border-cyan-700" if f["cat"] == "ion" else "bg-emerald-900/60 text-emerald-300 border-emerald-700")
        cat_label = "🧬 DNA 메타게놈" if f["cat"] == "dna" else ("💨 음이온·미기후" if f["cat"] == "ion" else "🌿 기후생명건강지수")
        
        card = f'''
        <div class="figure-card bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-lg hover:border-emerald-500/70 transition flex flex-col group" data-cat="{f["cat"]}">
          <div class="relative bg-slate-950/80 p-2 overflow-hidden aspect-[4/3] flex items-center justify-center cursor-pointer" onclick="openFigureModal('{f["src"]}', '{f["title"]}', '{f["desc"]}')">
            <img src="{f["src"]}" alt="{f["title"]}" class="max-h-full max-w-full object-contain group-hover:scale-105 transition duration-300" loading="lazy">
            <div class="absolute inset-0 bg-slate-950/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center gap-2 text-white font-bold text-xs">
              <i data-lucide="zoom-in" class="w-5 h-5 text-emerald-400"></i> 클릭하여 고해상도 확대
            </div>
          </div>
          <div class="p-4 flex flex-col justify-between flex-1">
            <div>
              <div class="flex items-center justify-between gap-1 mb-1.5">
                <span class="text-[10px] font-bold px-2 py-0.5 rounded border {badge_color}">{cat_label}</span>
                <span class="text-[10px] text-slate-500 font-mono">{f["id"]}</span>
              </div>
              <h4 class="text-sm font-bold text-white group-hover:text-emerald-300 transition line-clamp-1">{f["title"]}</h4>
              <p class="text-xs text-slate-400 mt-1.5 line-clamp-2 leading-relaxed">{f["desc"]}</p>
            </div>
            <div class="pt-3 mt-3 border-t border-slate-800 flex justify-end">
              <a href="{f["src"]}" download class="text-[11px] font-semibold text-emerald-400 hover:text-emerald-300 flex items-center gap-1">
                <i data-lucide="download" class="w-3.5 h-3.5"></i> 원본 PNG 다운로드
              </a>
            </div>
          </div>
        </div>
        '''
        gallery_html.append(card)
    return "\n".join(gallery_html)

gallery_cards_rendered = render_gallery_cards()

print("Subcomponents generated. Building master HTML...")
