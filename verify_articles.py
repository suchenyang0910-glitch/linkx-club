#!/usr/bin/env python3
import re

with open('decoded.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Check dates in actual HTML cards
print("=== HTML Cards (partial view) ===")
cards = re.findall(r'span class="date"[^>]*>([^<]*)</span>', html)
for c, card in enumerate(cards):
    print(f"  Card ~{c%4+1}: date={card}")

print()

# Check i18n entries
print("=== Intel i18n ===")
for m in re.finditer(r"'intel\.(tag\d|title\d|desc\d|ai\d)':'([^']*)'", html):
    print(f"  intel.{m.group(1)} = {m.group(2)[:60]}...")

print()
print("=== Radar i18n ===")
for m in re.finditer(r"'radar\.(d\d|i\d+[tda])':'([^']*)'", html):
    val = m.group(2)[:60]
    print(f"  radar.{m.group(1)} = {val}")

print()
print("=== Archive i18n ===")
for m in re.finditer(r"'archive\.(i\d+[tda])':'([^']*)'", html):
    val = m.group(2)[:60]
    print(f"  archive.{m.group(1)} = {val}")

print()
card_count = html.count('glass-card intel-card')
print(f"Total intel-card occurrences: {card_count}")
print(f"Has stale markers: {bool(re.search(r'__[A-Z_]+__', html))}")
print(f"Sections: {card_count // 4} (should be 3)")
