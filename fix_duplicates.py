#!/usr/bin/env python3
import re

with open('decoded.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove old #4 i18n entries by their exact text values
removals = [
    # Intel ZH old #4
    "'intel.tag4':'投资 / Investment'",
    "'intel.title4':'曼谷 EEC 特区加码 AI 算力补贴'",
    "'intel.desc4':'东部经济走廊(EEC)委员会通过新案，对外资设立的数据中心及AI研发机构给予最高8年免税期及电费定额补贴。'",
    "'intel.ai4':'泰国正抢夺区域算力中心地位，相关硬件供应链及出海算力租赁企业迎来6-12个月的政策红利窗口。'",
    # Intel EN old #4
    "'intel.tag4':'Investment'",
    "'intel.title4':'Thailand EEC Boosts AI Computing Subsidies'",
    "'intel.desc4':'The Eastern Economic Corridor committee approved up to 8-year tax holidays and electricity subsidies for foreign data centers and AI research institutes.'",
    "'intel.ai4':'Thailand is vying for regional AI hub status. Hardware supply chain and\U00051fa\U0006d77 computing leasing companies face a 6-12 month policy window.'",
    # Radar ZH old #4
    "'radar.d4':'2026-06-13 \u00b7 Thailand'",
    "'radar.i4t':'曼谷 EEC 特区加码 AI 算力补贴'",
    "'radar.i4d':'东部经济走廊委员会通过新案，对外资数据中心及AI研发机构给予最高8年免税期及电费补贴。'",
    "'radar.i4a':'泰国正抢夺区域算力中心地位，相关企业迎来6-12个月的政策红利窗口。'",
    # Radar EN old #4
    "'radar.i4t':'Thailand EEC AI Computing Subsidies'",
    "'radar.i4d':'EEC committee approved up to 8-year tax holidays and electricity subsidies for foreign data centers.'",
    "'radar.i4a':'Thailand is vying for regional AI hub status. Companies face a 6-12 month policy window.'",
    # Archive ZH old #4
    "'archive.i4t':'曼谷 EEC 特区加码 AI 算力补贴'",
    "'archive.i4d':'东部经济走廊通过新案，对外资数据中心给予8年免税...'",
    "'archive.i4a':'相关企业迎来6-12个月政策红利窗口。'",
    # Archive EN old #4
    "'archive.i4t':'Thailand EEC AI Computing Subsidies'",
    "'archive.i4d':'EEC committee approved up to 8-year tax holidays and electricity subsidies...'",
    "'archive.i4a':'Companies face a 6-12 month policy window.'",
]

for r in removals:
    if r in html:
        # Remove the entry and surrounding comma/whitespace
        # Try to remove the entry with its leading comma and possibly newline
        patterns = [
            f",\\n    {r}",   # ,\n    'key':'val'
            f",{r}",          # ,'key':'val'
            f"\\n    {r},",   # \n    'key':'val',
        ]
        for pat in patterns:
            if pat in html:
                html = html.replace(pat, '')
                break
        else:
            # Just remove the entry itself
            html = html.replace(r, '')
        print(f"Removed: {r[:50]}...")
    else:
        print(f"NOT FOUND: {r[:50]}...")

# Clean up any remaining double commas or empty lines
html = re.sub(r",\s*,\s*\n", ",\n", html)
html = re.sub(r",\s*\n\s*,", ",\n", html)
html = re.sub(r",\s*,\s*", ",\n    ", html)
html = re.sub(r"\n\s*\n\s*\n", "\n\n", html)

# Verify
print("\n=== Verification ===")
for m in re.finditer(r"'intel\.(tag\d|title\d|desc\d|ai\d)':'([^']*)'", html):
    print(f"  intel.{m.group(1)} = {m.group(2)[:60]}")

print()
for m in re.finditer(r"'radar\.(d\d|i\d+[tda])':'([^']*)'", html):
    print(f"  radar.{m.group(1)} = {m.group(2)[:60]}")

print()
print(f"Old thailand refs: {html.count('2026-06-13')}, {html.count('2026-06-10')}")
print(f"Stale markers: {bool(re.search(r'__[A-Z_]+__', html))}")

with open('decoded.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("\nSaved!")
