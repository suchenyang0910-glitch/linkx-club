#!/usr/bin/env python3
"""Debug zh locale structure"""
import base64, re
from pathlib import Path

PROJECT_DIR = Path(r"D:\projects\linkx-club-new")
B64_PATH = PROJECT_DIR / "index.b64"

raw = B64_PATH.read_text("utf-8").strip()
html = base64.b64decode(raw).decode("utf-8")

idx = html.find("const locales")
print(f"const locales at index: {idx}")

brace_start = html.index('{', idx)
print(f"locales opening brace at: {brace_start}")

# Look for zh:
for search in ["'zh':", "zh:"]:
    zh_idx = html.find(search, brace_start)
    if zh_idx >= 0:
        print(f"'{search}' found at: {zh_idx}")
        break

# Show context around zh
ctx = html[zh_idx:zh_idx+500]
print(f"\nContext around zh:\n{ctx[:500]}")

# Find zh opening brace
zh_brace = html.index('{', zh_idx)
print(f"\nzh opening brace at: {zh_brace}")

# Check balance manually in small region
depth = 0
max_depth = 0
problem_pos = -1
for i in range(zh_brace, min(zh_brace + 200000, len(html))):
    c = html[i]
    if c == '{':
        depth += 1
        if depth > max_depth:
            max_depth = depth
    elif c == '}':
        depth -= 1
        if depth < 0:
            problem_pos = i
            break
        if depth == 0:
            print(f"\nFound zh closing brace at: {i} (depth back to 0)")
            print(f"zh body length: {i - zh_brace - 1}")
            break

if depth > 0:
    print(f"\nDid NOT find closing brace. Depth stuck at: {depth}")
    print(f"Max depth reached: {max_depth}")
    # Look at region around depth issues
    for i in range(zh_brace, min(zh_brace + 5000, len(html))):
        c = html[i]
        if c in '{}':
            print(f"  pos {i}: '{c}' depth before: {depth}", end="")
            if c == '{': depth += 1
            else: depth -= 1
            print(f" after: {depth}")
