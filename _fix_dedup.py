#!/usr/bin/env python3
"""Fix massive duplication in index.b64 — deduplicate intel-grid cards"""
import base64, re, json, sys
from pathlib import Path

PROJECT_DIR = Path(r"D:\projects\linkx-club-new")
B64_PATH = PROJECT_DIR / "index.b64"

# 1. Decode
raw_b64 = B64_PATH.read_text("utf-8").strip()
html = base64.b64decode(raw_b64).decode("utf-8", errors="replace")
print(f"Decoded HTML: {len(html):,} chars")

# 2. Find intel-grid section
# Find the opening <div class="intel-grid"> and the closing </div>\s*</div>\s*</section>
m = re.search(r'(<div class="intel-grid">)(.*?)(</div>\s*</div>\s*</section>)', html, re.DOTALL)
if not m:
    print("ERROR: Cannot find intel-grid section")
    sys.exit(1)

grid_open = m.group(1)
grid_content = m.group(2)
grid_close = m.group(3)

print(f"Grid content: {len(grid_content):,} chars")

# 3. Find all cards
card_pattern = re.compile(
    r'<div class="glass-card intel-card">.*?</div>\s*</div>',
    re.DOTALL
)
cards = card_pattern.findall(grid_content)
print(f"Total cards found: {len(cards)}")

# 4. Deduplicate by intel number
seen_numbers = set()
unique_cards = []
for card in cards:
    num_m = re.search(r'intel\.title(\d+)', card)
    if num_m:
        num = int(num_m.group(1))
        if num not in seen_numbers:
            seen_numbers.add(num)
            unique_cards.append(card)
    else:
        unique_cards.append(card)  # keep cards without number

print(f"Unique cards: {len(unique_cards)} (removed {len(cards) - len(unique_cards)} duplicates)")

# 5. Rebuild grid content
new_grid_content = "\n" + "\n".join(unique_cards) + "\n    "

new_html = (
    html[:m.start()]
    + grid_open + new_grid_content + grid_close
    + html[m.end():]
)

print(f"New HTML: {len(new_html):,} chars (was {len(html):,}, saved {len(html)-len(new_html):,})")

# 6. Write back
b64 = base64.b64encode(new_html.encode("utf-8")).decode("ascii")
B64_PATH.write_text(b64, "utf-8")
(PROJECT_DIR / "index.html").write_text(new_html, "utf-8")
print("✅ index.b64 + index.html rewritten with deduplicated cards")

# 7. Count unique intel.title
print(f"intel.title remaining: {new_html.count('intel.title')}")
