import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

for file_path in ['index.html', 'docs/index.html']:
    print(f"\n--- Validating {file_path} ---")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Check Chapters
    for i in range(1, 9):
        assert f'id="chapter-{i}"' in content, f"Missing chapter-{i} in {file_path}"
        assert f'id="nav-ch{i}"' in content, f"Missing nav-ch{i} in {file_path}"
    print("All 8 chapters and nav buttons present!")

    # 2. Check image sources
    img_srcs = re.findall(r'<img[^>]*src=[\"\']([^\"\']+)[\"\']', content)
    base_dir = 'docs' if 'docs' in file_path else '.'
    missing_imgs = []
    for src in img_srcs:
        # Resolve path
        target_path = os.path.join(base_dir, src.replace('/', os.sep))
        if not os.path.exists(target_path):
            missing_imgs.append((src, target_path))
    
    if missing_imgs:
        print(f"Warning: {len(missing_imgs)} missing images in {file_path}:", missing_imgs[:3])
    else:
        print(f"All {len(img_srcs)} referenced images exist on disk!")

    # 3. Check download links
    hrefs = re.findall(r'<a[^>]*href=[\"\']([^\"\']+)[\"\'][^>]*download', content)
    missing_downloads = []
    for h in hrefs:
        target_path = os.path.join(base_dir, h.replace('/', os.sep))
        if not os.path.exists(target_path):
            missing_downloads.append((h, target_path))
    
    if missing_downloads:
        print(f"Warning: {len(missing_downloads)} missing download files in {file_path}:", missing_downloads)
    else:
        print(f"All {len(hrefs)} download links exist on disk!")

print("\nValidation complete!")
