#!/usr/bin/env python3
"""Debug script for cron — check intel-grid content in committed HTML"""
import base64, re, sys, subprocess

# Read committed version
result = subprocess.run(
    ["git", "show", "HEAD:index.b64"],
    cwd=r"D:\projects\linkx-club-new",
    capture_output=True, timeout=30
)
raw_b64 = result.stdout.decode('utf-8', errors='replace')
decoded = base64.b64decode(raw_b64).decode('utf-8', errors='replace')

print(f"Committed HTML: {len(decoded)} chars")
print(f"intel.title count: {decoded.count('intel.title')}")
print(f"intel-grid count: {decoded.count('intel-grid')}")

# Find all intel-grid divs
for idx, m in enumerate(re.finditer(r'<div class="intel-grid">', decoded)):
    start = m.start()
    snippet = decoded[start:start+300]
    print(f"\n--- intel-grid #{idx} at pos {start} ---")
    print(f"Context: ...{snippet}...")

# Find first intel-grid content
m = re.search(r'(<div class="intel-grid">)(.*?)(</div>\s*</div>\s*</section>)', decoded, re.DOTALL)
if m:
    content = m.group(2)
    cards = list(re.finditer(r'<div class="glass-card intel-card">', content))
    print(f"\n=== Cards in first intel-grid: {len(cards)} ===")
    for i, c in enumerate(cards[:10]):
        ctx = content[c.start():c.start()+200]
        title_m = re.search(r'data-i18n="intel\.title(\d+)">([^<]+)', ctx)
        if title_m:
            print(f"  Card {i}: intel.{title_m.group(1)} -> {title_m.group(2)[:50]}")
    if len(cards) > 10:
        # Also show last few
        for i, c in enumerate(cards[-4:]):
            ctx = content[c.start():c.start()+200]
            title_m = re.search(r'data-i18n="intel\.title(\d+)">([^<]+)', ctx)
            if title_m:
                print(f"  Card {len(cards)-4+i}: intel.{title_m.group(1)} -> {title_m.group(2)[:50]}")
else:
    print("\nFirst intel-grid regex did NOT match!")
    # Try simpler match
    m2 = re.search(r'(<div class="intel-grid">)', decoded)
    if m2:
        print(f"Found intel-grid at {m2.start()}")
