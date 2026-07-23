#!/usr/bin/env python3
"""Check locales structure in index.b64"""
import base64, re
from pathlib import Path

b64 = Path(r"D:\projects\linkx-club-new\index.b64").read_text("utf-8").strip()
html = base64.b64decode(b64).decode("utf-8", errors="replace")

print(f"HTML size: {len(html):,} chars")

# Find const locales section
m = re.search(r"(const locales\s*=\s*\{)(.*?)(\};?\s*)", html, re.DOTALL)
if m:
    body = m.group(2)
    print(f"Locales body: {len(body):,} chars")
    
    # Count intel entries
    pattern = re.compile(r"intel\.\w+")
    intel_keys = pattern.findall(body)
    print(f"intel.* keys in locales: {len(intel_keys)}")
    
    # Check unique intel numbers
    num_pattern = re.compile(r"intel\.(?:title|desc|ai|tag|date)(\d+)")
    nums = set()
    for k in intel_keys:
        n = num_pattern.search(k)
        if n:
            nums.add(int(n.group(1)))
    print(f"Unique intel numbers: {len(nums)}")
    if nums:
        print(f"Range: {min(nums)} - {max(nums)}")
    
    # Show sample of body
    print(f"\nFirst 400 chars of locales body:")
    print(body[:400])
    
    # Check zh locale specifically
    zh_m = re.search(r"'zh'\s*:\s*\{(.*?)\}", body, re.DOTALL)
    if zh_m:
        zh = zh_m.group(1)
        print(f"\nzh locale body: {len(zh):,} chars")
        zh_intel = pattern.findall(zh)
        print(f"intel.* keys in zh: {len(zh_intel)}")
        # Unique numbers in zh
        zh_nums = set()
        for k in zh_intel:
            n = num_pattern.search(k)
            if n:
                zh_nums.add(int(n.group(1)))
        print(f"Unique intel numbers in zh: {len(zh_nums)}")
        if zh_nums:
            print(f"zh range: {min(zh_nums)} - {max(zh_nums)}")
    else:
        print("\nzh locale not found")
else:
    print("const locales not found")
    idx = html.find("const locales")
    if idx >= 0:
        print(f"Found at index: {idx}")
        print(f"Context: {html[idx:idx+1000]}")
