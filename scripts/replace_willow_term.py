import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

target_files = [
    'scripts/prepare_portal_data.py',
    'scripts/generate_subcomponents.py',
    'scripts/build_master_portal.py',
    'README.md',
    'aerobiome_analysis_report.md',
    'docs/aerobiome_analysis_report.md',
    '괴산연습림_공기미생물_음이온_종합해석보고서.md',
    'docs/괴산연습림_공기미생물_음이온_종합해석보고서.md'
]

total_replacements = 0

for file_path in target_files:
    if not os.path.exists(file_path):
        continue
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    count = content.count('버들나무')
    if count > 0:
        new_content = content.replace('버들나무', '버드나무')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Replaced {count} occurrences in {file_path}")
        total_replacements += count
    else:
        print(f"No occurrences in {file_path}")

print(f"\nTotal replacements made across Markdown & Python files: {total_replacements}")
