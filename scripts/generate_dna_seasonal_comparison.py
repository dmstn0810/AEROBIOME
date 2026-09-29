import h5py
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Matplotlib configuration for Korean font and aesthetics
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 11

# 1. Spring 260415 Raw Data Extraction
tax415_raw = pd.read_excel('TAXONOMY_Assignment_260415.xlsx')
tax415 = tax415_raw.iloc[1:].copy()
tax415.columns = ['Query', 'Taxonomy', 'Kindom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species'] + list(tax415.columns[9:])
tax415_map = dict(zip(tax415['Query'], tax415['Genus']))

f_h5 = h5py.File('ASV_table_260415.biom', 'r')
sample_ids_415 = [s.decode() if isinstance(s, bytes) else str(s) for s in f_h5['sample/ids'][:]]
obs_ids_415 = [o.decode() if isinstance(o, bytes) else str(o) for o in f_h5['observation/ids'][:]]
data_415 = f_h5['observation/matrix/data'][:]
indices_415 = f_h5['observation/matrix/indices'][:]
indptr_415 = f_h5['observation/matrix/indptr'][:]

mat415 = np.zeros((len(obs_ids_415), len(sample_ids_415)))
for i in range(len(obs_ids_415)):
    start, end = indptr_415[i], indptr_415[i+1]
    mat415[i, indices_415[start:end]] = data_415[start:end]
f_h5.close()

df_mat415 = pd.DataFrame(mat415, index=obs_ids_415, columns=sample_ids_415)
df_mat415['Genus_clean'] = df_mat415.index.map(tax415_map).fillna('g__Unassigned')
df_mat415['Genus_clean'] = df_mat415['Genus_clean'].str.replace('g__', '')

spring_p = df_mat415.groupby('Genus_clean')[['9_P_densiflora', '10_P_densiflora']].sum().sum(axis=1)
spring_p_pct = (spring_p / spring_p.sum() * 100)

spring_s = df_mat415.groupby('Genus_clean')[['5_S_koreensis', '6_S_koreensis']].sum().sum(axis=1)
spring_s_pct = (spring_s / spring_s.sum() * 100)

# 2. Summer 260727 Raw Data Extraction
tax727_raw = pd.read_excel('TAXONOMY_Assignment_260727.xlsx')
tax727 = tax727_raw.iloc[1:].copy()
tax727.columns = ['Query', 'Taxonomy', 'Kindom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species'] + list(tax727.columns[9:])
tax727_map = dict(zip(tax727['Query'], tax727['Genus']))

with open('ASV_table_260727.biom', 'r') as f:
    biom727 = json.load(f)

cols727 = [c['id'] for c in biom727['columns']]
rows727 = [r['id'] for r in biom727['rows']]
mat727 = np.zeros((len(rows727), len(cols727)))
for r, c, val in biom727['data']:
    mat727[r, c] = val

df_mat727 = pd.DataFrame(mat727, index=rows727, columns=cols727)
df_mat727['Genus_clean'] = df_mat727.index.map(tax727_map).fillna('g__Unassigned')
df_mat727['Genus_clean'] = df_mat727['Genus_clean'].str.replace('g__', '')

summer_p = df_mat727.groupby('Genus_clean')[['7_P_densiflora', '8_P_densiflora']].sum().sum(axis=1)
summer_p_pct = (summer_p / summer_p.sum() * 100)

summer_s = df_mat727.groupby('Genus_clean')[['3_S_koreensis', '4_S_koreensis']].sum().sum(axis=1)
summer_s_pct = (summer_s / summer_s.sum() * 100)

summer_a = df_mat727.groupby('Genus_clean')['5_Field'].sum()
summer_a_pct = (summer_a / summer_a.sum() * 100)

# Combine into master dataframe
master_df = pd.DataFrame({
    'Type P (Spring)': spring_p_pct,
    'Type P (Summer)': summer_p_pct,
    'Type S (Spring)': spring_s_pct,
    'Type S (Summer)': summer_s_pct,
    'Type A (Summer)': summer_a_pct
}).fillna(0)

# Clean Genus names for clarity
rename_map = {
    'Capnodiales_gen_Incertae_sedis': 'Capnodiales (sp.)',
    'Eukaryota_gen_Incertae_sedis': 'Unassigned / Other Fungi',
    'Nectriaceae_gen_Incertae_sedis': 'Nectriaceae (sp.)',
    'Sordariaceae_gen_Incertae_sedis': 'Sordariaceae (sp.)'
}
master_df.index = [rename_map.get(g, g) for g in master_df.index]

# Top 9 distinct genera
top_genera = [
    'Coprinellus',      # Wood decay (Pine summer)
    'Trichoderma',      # Organic matter decomposer (Willow summer)
    'Fusarium',         # Soil-borne pathogen (Field summer)
    'Capnodiales (sp.)',# Foliar epiphyte (Spring dominant)
    'Cladosporium',     # Airborne spore / allergen (Spring)
    'Penicillium',      # Ubiquitous mold
    'Umbelopsis',       # Pine spring soil/litter
    'Irpex',            # White-rot fungus (Pine summer)
    'Aspergillus'       # Storage/agricultural mold
]

plot_df = master_df.reindex(top_genera).fillna(0)
others = 100 - plot_df.sum(axis=0)
plot_df.loc['Others (기타 분류군)'] = others.clip(lower=0)
plot_df = plot_df / plot_df.sum(axis=0) * 100

# Distinct color palette tailored for microbial functional guilds
color_dict = {
    'Coprinellus': '#AD1457',       # Deep Wine / Mulberry (Wood decay)
    'Trichoderma': '#2E7D32',       # Vibrant Forest Green (Litter decomposer)
    'Fusarium': '#1565C0',          # Strong Royal Blue (Field pathogen)
    'Capnodiales (sp.)': '#00838F', # Dark Cyan / Teal (Foliar epiphyte)
    'Cladosporium': '#FBC02D',      # Warm Golden Yellow (Spring spore)
    'Penicillium': '#FF8F00',       # Amber Orange
    'Umbelopsis': '#6A1B9A',        # Deep Purple
    'Irpex': '#E64A19',             # Deep Coral / Vermilion (Wood rot)
    'Aspergillus': '#795548',       # Earthy Brown
    'Others (기타 분류군)': '#CFD8DC'# Neutral Light Gray
}
colors = [color_dict[g] for g in plot_df.index]

# Figure Setup (2 Panels)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7.5), gridspec_kw={'width_ratios': [2.2, 1.6]})

# --- Panel A: Seasonal Succession in Forest Stands (Type P & Type S) ---
forest_cols = ['Type P (Spring)', 'Type P (Summer)', 'Type S (Spring)', 'Type S (Summer)']
forest_data = plot_df[forest_cols].T
bottoms = np.zeros(len(forest_cols))
x_pos = np.arange(len(forest_cols))

for i, genus in enumerate(plot_df.index):
    vals = forest_data[genus].values
    ax1.bar(x_pos, vals, bottom=bottoms, width=0.52, label=genus, color=colors[i], edgecolor='white', linewidth=0.7)
    bottoms += vals

ax1.set_xticks(x_pos)
ax1.set_xticklabels([
    'Type P\n(봄철 04/15)', 'Type P\n(여름철 07/27)', 
    'Type S\n(봄철 04/15)', 'Type S\n(여름철 07/27)'
], fontsize=11, fontweight='bold')
ax1.set_ylabel('상대 풍부도 (Relative Abundance, %)', fontsize=12, fontweight='bold')
ax1.set_title('(A) 산림 식생별 봄·여름철 공기진균 군집 천이\n[Seasonal Succession in Forest Stands: Type P vs Type S]', 
              fontsize=13, fontweight='bold', pad=35)
ax1.set_ylim(0, 100)
ax1.grid(axis='y', linestyle='--', alpha=0.35)

# Clear boundary lines and headers for stand groups
ax1.axvline(1.5, color='#90A4AE', linestyle='--', linewidth=1.5)
ax1.text(0.5, 102.5, '소나무림 (Type P)', ha='center', va='bottom', fontsize=12, fontweight='bold', color='#1B5E20',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8F5E9', edgecolor='#81C784', linewidth=1.2))
ax1.text(2.5, 102.5, '버드나무림 (Type S)', ha='center', va='bottom', fontsize=12, fontweight='bold', color='#004D40',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#E0F2F1', edgecolor='#4DB6AC', linewidth=1.2))

# --- Panel B: Summer Spatial Differentiation (Type P vs Type S vs Type A) ---
summer_cols = ['Type P (Summer)', 'Type S (Summer)', 'Type A (Summer)']
summer_data = plot_df[summer_cols].T
bottoms_s = np.zeros(len(summer_cols))
x_pos_s = np.arange(len(summer_cols))

for i, genus in enumerate(plot_df.index):
    vals_s = summer_data[genus].values
    ax2.bar(x_pos_s, vals_s, bottom=bottoms_s, width=0.52, color=colors[i], edgecolor='white', linewidth=0.7)
    bottoms_s += vals_s

ax2.set_xticks(x_pos_s)
ax2.set_xticklabels([
    'Type P\n(소나무림)', 'Type S\n(버드나무림)', 'Type A\n(농경지 밭)'
], fontsize=11, fontweight='bold')
ax2.set_title('(B) 여름철 입지별 공기진균 생태 기능 분화\n[Summer Spatial Differentiation: Type P vs S vs A]', 
              fontsize=13, fontweight='bold', pad=35)
ax2.set_ylim(0, 100)
ax2.grid(axis='y', linestyle='--', alpha=0.35)

# Header for Summer 3-Site Comparison
ax2.text(1.0, 102.5, '여름철(07/27) 3대 입지 동시 비교', ha='center', va='bottom', fontsize=12, fontweight='bold', color='#37474F',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#ECEFF1', edgecolor='#B0BEC5', linewidth=1.2))

# Legend setup with italicized genus names
handles, labels = ax1.get_legend_handles_labels()
formatted_labels = []
for l in labels:
    if 'Others' in l or 'Unassigned' in l:
        formatted_labels.append(l)
    elif '(sp.)' in l:
        base = l.replace(' (sp.)', '')
        formatted_labels.append(f'${base}$ sp.')
    else:
        formatted_labels.append(f'${l}$')

fig.legend(handles, formatted_labels, loc='center left', bbox_to_anchor=(0.91, 0.5), 
           fontsize=11, frameon=True, framealpha=0.98, edgecolor='#90A4AE', 
           title='주요 공기진균 우점 속 (Genera)\n[ITS 차세대 염기서열 실측치]', title_fontsize=11.5)

plt.tight_layout(rect=[0, 0, 0.90, 0.95])

out_dir = Path('figures')
out_dir.mkdir(exist_ok=True)
fig_path = out_dir / 'fig_dna_community_seasonal_comparison.png'
plt.savefig(fig_path, dpi=300, bbox_inches='tight')

docs_img_path = Path('docs/images') / 'fig_dna_community_seasonal_comparison.png'
plt.savefig(docs_img_path, dpi=300, bbox_inches='tight')

print(f'Successfully updated figure at {fig_path} and {docs_img_path}')
