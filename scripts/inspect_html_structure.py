import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('docs/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

chapters = re.findall(r'id=["\'](chapter-\d+)["\']', text)
print("Chapters in docs/index.html:", chapters)

nav_tabs = re.findall(r'id=["\'](nav-ch\d+)["\'][^>]*>(.*?)<\/button>', text, re.DOTALL)
for tid, content in nav_tabs:
    clean_text = re.sub(r'<[^>]+>', '', content).strip()
    print(f"Tab {tid}: {clean_text}")

with open('index.html', 'r', encoding='utf-8') as f:
    text_root = f.read()

card_titles = re.findall(r'<h[23][^>]*>(.*?)</h[23]>', text_root)
print(f"Root index.html headings: {len(card_titles)}")
for h in card_titles:
    clean_h = re.sub(r'<[^>]+>', '', h).strip()
    if clean_h:
        print(f"  - {clean_h}")


