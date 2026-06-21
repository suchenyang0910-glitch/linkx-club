#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

with open('decoded.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Use a different approach: find all i18n entries and reconstruct without duplicates
# The issue is that the old #4 Thailand EEC entries are still present alongside the 
# shifted new #4 Malaysia MM2H entries.

# Let's find duplicate title4 entries (the wrong ones have '曼谷 EEC')
wrong_titles_zh = ['曼谷 EEC 特区加码 AI 算力补贴']
wrong_titles_en = ['Thailand EEC Boosts AI Computing Subsidies', 'Thailand EEC AI Computing Subsidies']

# Remove entries containing these titles
lines = html.split('\n')
new_lines = []
skip_next = False
for i, line in enumerate(lines):
    stripped = line.strip()
    should_skip = False
    
    for wt in wrong_titles_zh + wrong_titles_en:
        if wt in stripped:
            should_skip = True
            break
    
    # Also skip old radar.d4 = 2026-06-13
    if "radar.d4':" in stripped and '2026-06-13' in stripped:
        should_skip = True
    
    # Skip old archive entries with '东部经济走廊通过新案'
    if "archive.i4t':" in stripped and '曼谷 EEC' in stripped:
        should_skip = True
    if "archive.i4d':" in stripped and '东部经济走廊' in stripped:
        should_skip = True
    if "archive.i4a':" in stripped and '政策红利窗口' in stripped:
        should_skip = True
    if "archive.i4a':" in stripped and 'policy window' in stripped:
        should_skip = True
    
    if should_skip:
        print(f"SKIP line {i}: {line[:80]}")
        continue
    
    new_lines.append(line)

html = '\n'.join(new_lines)

# Clean up: remove double commas and excess whitespace
html = re.sub(r",\s*,\s*", ",", html)
html = re.sub(r",\s*\n\s*,", ",", html)

# Verify
print("\n=== Final Verification ===")
for m in re.finditer(r"'intel\.(tag\d|title\d|desc\d|ai\d)':'([^']*)'", html):
    print(f"  intel.{m.group(1)} = {m.group(2)[:60]}")

print()
for m in re.finditer(r"'radar\.(d\d|i\d+[tda])':'([^']*)'", html):
    print(f"  radar.{m.group(1)} = {m.group(2)[:60]}")

print()
for m in re.finditer(r"'archive\.(i\d+[tda])':'([^']*)'", html):
    print(f"  archive.{m.group(1)} = {m.group(2)[:60]}")

print()
print(f"Old Thailand refs (2026-06-13): {html.count('2026-06-13')}")
print(f"Old Thailand refs (2026-06-10): {html.count('2026-06-10')}")
print(f"Intel-card count: {html.count('glass-card intel-card')}")

with open('decoded.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("\nSaved!")
