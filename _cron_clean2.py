#!/usr/bin/env python3
"""
Step 1v2: Clean up duplicate intel entries in locales.
Uses line-level filtering on zh body found by balanced brace starting from locales open.
"""
import base64, re
from pathlib import Path

PROJECT_DIR = Path(r"D:\projects\linkx-club-new")
B64_PATH = PROJECT_DIR / "index.b64"

def find_matching_brace(text, start, initial_depth=0):
    """Find matching closing brace starting from start (at the opening brace position)"""
    depth = initial_depth
    i = start
    while i < len(text):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1

def main():
    raw = B64_PATH.read_text("utf-8").strip()
    html = base64.b64decode(raw).decode("utf-8")
    print(f"HTML: {len(html):,} chars")

    # Find current card numbers from intel-grid
    grid_m = re.search(r'<div class="intel-grid">(.*?)</div>\s*</div>\s*</section>', html, re.DOTALL)
    cards = re.findall(r'intel\.title(\d+)', grid_m.group(1))
    current_nums = set(int(n) for n in cards)
    print(f"Current intel-grid card numbers: {sorted(current_nums)}")

    # Find const locales
    idx = html.find("const locales")
    if idx < 0:
        print("ERROR: const locales not found")
        return
    
    # Find the opening brace of const locales
    brace_start = html.index('{', idx)
    
    # Count depth up to brace_start
    initial_depth = 0
    for c in html[:brace_start]:
        if c == '{': initial_depth += 1
        elif c == '}': initial_depth -= 1
    print(f"Initial depth at locales open: {initial_depth}")
    
    # Find zh: within locales
    zh_idx = html.find("zh:", brace_start)
    if zh_idx < 0:
        print("ERROR: zh not found")
        return
    
    zh_brace = html.index('{', zh_idx)
    
    # Find zh closing brace using depth from const locales open
    zh_end = find_matching_brace(html, zh_brace, initial_depth=initial_depth)
    if zh_end < 0:
        print("ERROR: zh closing brace not found")
        return
    
    zh_body = html[zh_brace:zh_end+1]
    # Remove the outer braces to get the inner content
    zh_inner = html[zh_brace+1:zh_end]
    print(f"zh body: {len(zh_inner):,} chars")
    
    before_count = len(re.findall(r"intel\.\w+", zh_inner))
    print(f"intel.* entries in zh before: {before_count}")
    
    # Build set of keys to keep
    keep_keys = set()
    for n in current_nums:
        for prefix in ["intel.tag", "intel.date", "intel.title", "intel.desc", "intel.ai"]:
            keep_keys.add(f"{prefix}{n}")
    
    new_lines = []
    removed = 0
    kept = 0
    
    for line in zh_inner.split("\n"):
        stripped = line.strip().rstrip(",")
        im = re.match(r"(intel\.\w+)\s*:", stripped)
        if im:
            key = im.group(1)
            if key in keep_keys:
                new_lines.append(line)
                kept += 1
            else:
                removed += 1
        else:
            new_lines.append(line)
            kept += 1
    
    print(f"Removed duplicate intel lines: {removed}, Kept: {kept}")
    
    new_zh_inner = "\n".join(new_lines)
    new_html = html[:zh_brace+1] + new_zh_inner + html[zh_end:]
    
    after_count = len(re.findall(r"intel\.\w+", new_html))
    print(f"intel.* entries in HTML after: {after_count}")
    print(f"HTML size: {len(new_html):,} chars (was {len(html):,})")
    print(f"Saved: {(len(html) - len(new_html)) / 1024 / 1024:.1f} MB")
    
    # Write back
    b64 = base64.b64encode(new_html.encode("utf-8")).decode("ascii")
    B64_PATH.write_text(b64, "utf-8")
    (PROJECT_DIR / "index.html").write_text(new_html, "utf-8")
    print("✅ Written")

if __name__ == "__main__":
    main()
