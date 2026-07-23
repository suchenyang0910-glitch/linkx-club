#!/usr/bin/env python3
"""
Step 1: Clean up duplicate intel entries in locales.
Uses line-level filtering (fast even on 142MB body).
"""
import base64, re
from pathlib import Path

PROJECT_DIR = Path(r"D:\projects\linkx-club-new")
B64_PATH = PROJECT_DIR / "index.b64"

def find_balanced_brace(text, start):
    """Find matching closing brace from start position (at or after the opening brace)"""
    depth = 0
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
    
    # Find the zh: {  section within locales body  
    zh_idx = html.find("'zh':", brace_start)
    if zh_idx < 0:
        zh_idx = html.find("zh:", brace_start)
    if zh_idx < 0:
        print("ERROR: zh locale not found")
        return
    
    # Find zh opening brace
    zh_brace = html.index('{', zh_idx)
    zh_end = find_balanced_brace(html, zh_brace)
    if zh_end < 0:
        print("ERROR: Cannot find zh closing brace")
        return
    
    zh_body = html[zh_brace+1:zh_end]
    print(f"zh body: {len(zh_body):,} chars")
    
    # Count intel.* entries before cleanup
    before_count = len(re.findall(r"intel\.\w+", zh_body))
    print(f"intel.* entries in zh before: {before_count}")
    
    # Filter lines - keep only intel entries with current numbers + all non-intel lines
    # Build set of keys to keep: intel.tag/date/title/desc/ai + current numbers
    keep_keys = set()
    for n in current_nums:
        for prefix in ["intel.tag", "intel.date", "intel.title", "intel.desc", "intel.ai"]:
            keep_keys.add(f"{prefix}{n}")
    
    new_lines = []
    removed = 0
    kept = 0
    
    for line in zh_body.split("\n"):
        stripped = line.strip().rstrip(",")
        # Check if this is an intel entry
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
    
    print(f"Removed: {removed}, Kept: {kept}")
    
    new_zh_body = "\n".join(new_lines)
    new_html = html[:zh_brace+1] + new_zh_body + html[zh_end:]
    
    after_count = len(re.findall(r"intel\.\w+", new_html))
    print(f"intel.* entries in HTML after: {after_count}")
    print(f"HTML size: {len(new_html):,} chars (was {len(html):,})")
    
    # Write back
    b64 = base64.b64encode(new_html.encode("utf-8")).decode("ascii")
    B64_PATH.write_text(b64, "utf-8")
    (PROJECT_DIR / "index.html").write_text(new_html, "utf-8")
    print("✅ Written")
    
    # Try to also fix en locale if it exists
    en_idx = html.find("'en':", brace_start)
    if en_idx < 0:
        en_idx = html.find("en:", brace_start)
    
    if en_idx > 0 and en_idx < zh_idx:
        # en comes before zh - skip, already handled in zh-only approach
        pass
    
    print(f"\nSaved {(len(html) - len(new_html)) / 1024 / 1024:.1f} MB")

if __name__ == "__main__":
    main()
