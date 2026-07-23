#!/usr/bin/env python3
"""
Cron fix: clean up massive duplication in locales (393k entries for 19 cards),
then add new article and rebuild.
"""
import base64, re, subprocess, sys
from pathlib import Path
from datetime import datetime

PROJECT_DIR = Path(r"D:\projects\linkx-club-new")
B64_PATH = PROJECT_DIR / "index.b64"

TAG_CONFIG = {
    "Policy":     {"css": "tag-policy",     "label": "政策 / Policy",     "emoji": "📜"},
    "Market":     {"css": "tag-market",     "label": "市场 / Market",     "emoji": "📊"},
    "Visa":       {"css": "tag-visa",       "label": "签证 / Visa",       "emoji": "🛂"},
    "Investment": {"css": "tag-investment", "label": "投资 / Investment", "emoji": "💰"},
}

# --- New article data ---
NEW_TITLE = "越南7月实施29项新规重构营商环境"
NEW_DESC = "越南2026年7月1日起正式实施29部法律2部法令及34项法令改革，涉及电商、数字转型、税务、网络安全等多个领域，外资企业需重新进行合规审查以适应新监管框架。"
NEW_TAG = "Policy"
NEW_META = "2026-07-10 · Vietnam"
NEW_INSIGHT = "越南密集出台新规信号明确：通过法治化手段系统性优化营商环境，外资合规成本上升但市场规范化提速。"


def main():
    # 1. Decode
    print("Decoding index.b64...")
    raw_b64 = B64_PATH.read_text("utf-8").strip()
    html = base64.b64decode(raw_b64).decode("utf-8", errors="replace")
    print(f"  HTML: {len(html):,} chars")

    # 2. Find intel-grid and extract current cards
    print("Finding intel-grid...")
    m = re.search(r'(<div class="intel-grid">)(.*?)(</div>\s*</div>\s*</section>)', html, re.DOTALL)
    if not m:
        print("ERROR: intel-grid not found!")
        sys.exit(1)

    grid_open, grid_content, grid_close = m.group(1), m.group(2), m.group(3)
    card_pattern = re.compile(r'<div class="glass-card intel-card">.*?</div>\s*</div>', re.DOTALL)
    cards = card_pattern.findall(grid_content)
    print(f"  Found {len(cards)} cards in grid")

    # Get current card numbers
    current_nums = set()
    for card in cards:
        num_m = re.search(r'intel\.title(\d+)', card)
        if num_m:
            current_nums.add(int(num_m.group(1)))
    print(f"  Current card numbers: {sorted(current_nums)}")

    # 3. Find const locales
    print("Finding const locales...")
    lm = re.search(r'(const locales\s*=\s*\{)(.*?)(\};?\s*)', html, re.DOTALL)
    if not lm:
        print("ERROR: const locales not found")
        sys.exit(1)

    locales_prefix = lm.group(1)
    locales_body = lm.group(2)
    locales_suffix = lm.group(3)
    print(f"  Locales body: {len(locales_body):,} chars")

    # 4. In the locales body, for each language, keep only current card entries + non-intel entries
    # Track positions of each language: zh: { ... }, en: { ... }
    lang_pattern = re.compile(r"""
        ('?\w+'?\s*:\s*\{)   # e.g. 'zh': { or zh: {
        ((?:[^{}]|\{[^{}]*\})*)
        (\})
    """, re.VERBOSE | re.DOTALL)

    new_locales_parts = []
    pos = 0
    
    for lang_m in lang_pattern.finditer(locales_body):
        lang_header = lang_m.group(1)
        lang_content = lang_m.group(2)
        lang_close = lang_m.group(3)
        
        # Parse existing intel entries in this language
        intel_entries = re.findall(
            r"(intel\.\w+\s*:\s*)'([^']*)'",
            lang_content
        )
        
        # Group by key
        seen_keys = {}  # key -> most recent value (last occurrence wins)
        for entry_key, entry_val in intel_entries:
            seen_keys[entry_key.strip().rstrip(":")] = entry_val
        
        # Filter: keep only non-intel entries and intel entries whose number is in current_nums
        new_lang_lines = []
        for line in lang_content.strip().split("\n"):
            line_stripped = line.strip().rstrip(",")
            # Check if it's an intel entry
            im = re.match(r"(intel\.\w+)\s*:\s*", line_stripped)
            if im:
                key = im.group(1)
                # Extract number from key
                num_m = re.search(r'(\d+)$', key)
                if num_m and int(num_m.group(1)) in current_nums:
                    # Keep it - use the last value for this key
                    clean_key = im.group(1).strip()
                    if clean_key in seen_keys:
                        new_lang_lines.append(f"    {clean_key}:'{seen_keys[clean_key]}',")
                # else: skip (stale intel entry)
            elif line_stripped:
                # Non-intel entry - keep as is
                new_lang_lines.append(line)
            else:
                new_lang_lines.append(line)
        
        new_lang_content = "\n".join(new_lang_lines)
        new_locales_parts.append(f"{lang_header}\n{new_lang_content}\n{lang_close}")
        pos = lang_m.end()
    
    # Add any remaining content after last language
    remaining = locales_body[pos:].strip()
    if remaining:
        new_locales_parts.append(remaining)
    
    new_locales_body = "\n".join(new_locales_parts)
    print(f"  New locales body: {len(new_locales_body):,} chars")
    
    new_html = html[:lm.start()] + locales_prefix + new_locales_body + locales_suffix + html[lm.end():]
    print(f"  Cleaned HTML: {len(new_html):,} chars")
    print(f"  intel.title count after cleanup: {new_html.count('intel.title')}")

    # 5. Add new card
    tc = TAG_CONFIG.get(NEW_TAG, TAG_CONFIG["Market"])
    new_n = max(current_nums) + 1 if current_nums else 1
    print(f"\nAdding new card: intel.{new_n}")

    new_card = (
        f'      <div class="glass-card intel-card">'
        f'<div class="meta">'
        f'<span class="tag {tc["css"]}" data-i18n="intel.tag{new_n}">{tc["label"]}</span>'
        f'<span class="date" data-i18n="intel.date{new_n}">{NEW_META}</span>'
        f'</div>'
        f'<h4 data-i18n="intel.title{new_n}">{NEW_TITLE}</h4>'
        f'<p data-i18n="intel.desc{new_n}">{NEW_DESC}</p>'
        f'<div class="ai-insight"><p><span class="label">AI 洞察</span>'
        f'<span data-i18n="intel.ai{new_n}">{NEW_INSIGHT}</span></p></div>'
        f'</div>'
    )

    new_cards = [new_card] + cards
    if len(new_cards) > 4:
        removed = new_cards.pop(-1)
        rm_num_search = re.search(r'intel\.title(\d+)', removed)
        if rm_num_search:
            print(f"  Removed oldest card: intel.{rm_num_search.group(1)}")

    new_grid_content_val = "\n" + "\n".join(new_cards) + "\n    "
    new_html = (
        new_html[:m.start()]
        + grid_open + new_grid_content_val + grid_close
        + new_html[m.end():]
    )

    # 6. Add i18n entries for the new card in each language
    new_entries = {
        f'intel.tag{new_n}': tc["label"],
        f'intel.date{new_n}': NEW_META,
        f'intel.title{new_n}': NEW_TITLE,
        f'intel.desc{new_n}': NEW_DESC,
        f'intel.ai{new_n}': NEW_INSIGHT,
    }

    # Find each language block and add entries
    def add_entries_to_lang(new_html):
        # Find locales again (after HTML was modified above)
        lm2 = re.search(r'(const locales\s*=\s*\{)(.*?)(\};?\s*)', new_html, re.DOTALL)
        if not lm2:
            return new_html

        body = lm2.group(2)
        
        # Find each language section
        lang_matches = list(re.finditer(r"""('?\w+'?\s*:\s*\{)((?:[^{}]|\{[^{}]*\})*)(\})""", body, re.DOTALL))
        
        for lang_match in lang_matches:
            lh = lang_match.group(1)
            lc = lang_match.group(2)
            lc_end = lang_match.group(3)
            
            # Check which entries already exist
            existing_entries = set()
            for entry_key in new_entries:
                if f"intel.tag{new_n}" in lc and f"intel.date{new_n}" in lc:
                    pass  # already has this number
            
            # Add any missing entries
            additions = []
            for entry_key, entry_val in new_entries.items():
                if entry_key not in " ".join(re.findall(r"(intel\.\w+)", lc)):
                    additions.append(f"    {entry_key}:'{entry_val}',")
            
            if additions:
                new_lc = lc.rstrip() + "\n" + "\n".join(additions) + "\n"
                body = body[:lang_match.start()] + lh + new_lc + lc_end + body[lang_match.end():]
        
        new_html = new_html[:lm2.start()] + lm2.group(1) + body + lm2.group(3) + new_html[lm2.end():]
        return new_html

    new_html = add_entries_to_lang(new_html)
    
    print(f"\nFinal HTML: {len(new_html):,} chars")
    print(f"intel.title count: {new_html.count('intel.title')}")

    # 7. Write back
    print("\nWriting files...")
    b64 = base64.b64encode(new_html.encode("utf-8")).decode("ascii")
    B64_PATH.write_text(b64, "utf-8")
    (PROJECT_DIR / "index.html").write_text(new_html, "utf-8")
    print("✅ index.b64 + index.html written")

    # 8. Build
    print("\n🚀 Building...")
    r = subprocess.run(
        ["npm", "run", "build"], cwd=PROJECT_DIR,
        capture_output=True, text=True, timeout=120,
    )
    for line in r.stdout.split("\n")[-5:]:
        if line.strip():
            print(f"  {line.strip()}")
    if r.returncode != 0:
        print(f"⚠️ Build error: {r.stderr[-300:]}")
        return

    # 9. Commit & push
    print("\n📤 Pushing...")
    subprocess.run(["git", "add", "-A"], cwd=PROJECT_DIR, capture_output=True, timeout=10)
    subprocess.run(
        ["git", "commit", "-m", f"daily article {datetime.now():%Y-%m-%d}"],
        cwd=PROJECT_DIR, capture_output=True, text=True, timeout=10,
    )
    pr = subprocess.run(
        ["git", "push"], cwd=PROJECT_DIR,
        capture_output=True, text=True, timeout=30,
    )
    if pr.returncode == 0:
        print("✅ git push ok")
    else:
        print(f"⚠️ push failed: {pr.stderr[-300:]}")

    print("\n✅ All done!")


if __name__ == "__main__":
    main()
