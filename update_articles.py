#!/usr/bin/env python3
"""
Update linkx.club daily articles: remove oldest (#4), shift others, insert new #1
"""
import re, base64

with open('decoded.html', 'r', encoding='utf-8') as f:
    html = f.read()

# New article content
NEW_DATE = "2026-06-17 · Cambodia"
NEW_TITLE = "柬埔寨副首相赴韩招商，瞄准EV及高科制造业"
NEW_DESC = "副首相孙占托率团赴韩路演，先后拜会三星电子、大柱KC集团等巨头，推动韩国投资进入汽车零部件、电动车系统及数字医疗领域，标志柬埔寨工业战略从传统制衣向高附加值制造业转型。"
NEW_AI = "柬埔寨产业升级信号明确，EV供应链及配套基建将迎外资集中流入窗口，关注后续投资落地节奏与政策配套。"

NEW_DATE_EN = "2026-06-17 · Cambodia"
NEW_TITLE_EN = "Cambodia Deputy PM Courts Korean Investment in EV & High-Tech Manufacturing"
NEW_DESC_EN = "Deputy PM Sun Chanthol led a roadshow in Korea, meeting Samsung and Daejoo KC Group to attract investment in auto parts, EV systems, and digital healthcare — signaling a strategic shift from garments to higher-value manufacturing."
NEW_AI_EN = "Clear signal of Cambodia's industrial upgrade. EV supply chain and infrastructure will see concentrated foreign capital inflows. Watch policy support and deal execution."

# ====================================================================
# Helper: remove block and shift i18n keys
# ====================================================================
def delete_hardcoded_article(html, section_prefix, old_tag, old_date, old_title, old_desc, old_ai):
    """Remove a hardcoded intel card div block from the HTML section."""
    # Build the pattern for the exact card
    # Try matching the tag class and date - these should be unique enough
    pattern = re.escape(f'<div class="glass-card intel-card"><div class="meta"><span class="tag tag-{old_tag}"') + r'.*?' + re.escape(f'</span></p></div></div>')
    # Be more specific: find the card containing the date string
    start_marker = f'<div class="glass-card intel-card">'
    date_marker = old_date
    
    idx = html.find(start_marker)
    while idx >= 0:
        end_idx = html.find('</div>\n      </div>', idx)
        if end_idx < 0:
            end_idx = html.find('</div></div>', idx)
        if end_idx < 0:
            break
        # Check if this card contains our date
        card_section = html[idx:end_idx+len('</div></div>')]
        if old_date in card_section:
            # Remove this card
            before = html[:idx]
            after = html[end_idx+len('</div></div>'):]
            # Clean up extra whitespace/newlines
            return before.rstrip() + '\n' + after.lstrip()
        idx = html.find(start_marker, idx + 1)
    return html


def shift_i18n_keys(html, section_prefix):
    """Shift i18n keys for 4 articles: delete old #4, shift 1->2, 2->3, 3->4"""
    # Step 1: Remove old #4 keys (section_prefix.tag4, .title4, .desc4, .ai4)
    for suffix in ['tag4', 'title4', 'desc4', 'ai4', 'd4', 'i4t', 'i4d', 'i4a']:
        key = f'{section_prefix}.{suffix}'
        pattern = re.escape(key) + r"'[^']*',?\s*"
        html = re.sub(pattern, '', html)
    
    # Step 2: Replace keys to shift: 
    # Use temp markers to avoid cascade
    html = html.replace(f'{section_prefix}.tag1', f'__TAG1__')
    html = html.replace(f'{section_prefix}.title1', f'__TIT1__')
    html = html.replace(f'{section_prefix}.desc1', f'__DES1__')
    html = html.replace(f'{section_prefix}.ai1', f'__AI1__')
    
    html = html.replace(f'{section_prefix}.tag2', f'__TAG2__')
    html = html.replace(f'{section_prefix}.title2', f'__TIT2__')
    html = html.replace(f'{section_prefix}.desc2', f'__DES2__')
    html = html.replace(f'{section_prefix}.ai2', f'__AI2__')
    
    html = html.replace(f'{section_prefix}.tag3', f'__TAG3__')
    html = html.replace(f'{section_prefix}.title3', f'__TIT3__')
    html = html.replace(f'{section_prefix}.desc3', f'__DES3__')
    html = html.replace(f'{section_prefix}.ai3', f'__AI3__')
    
    # For radar section, also handle d and i1t, i1d, i1a etc
    if section_prefix.startswith('radar') or section_prefix.startswith('archive'):
        for s in ['d1', 'd2', 'd3', 'd4']:
            html = html.replace(f'{section_prefix}.{s}', f'__{s.upper()}__')
    
    # Now reassign: 1->2, 2->3, 3->4
    html = html.replace('__TAG1__', f'{section_prefix}.tag2')
    html = html.replace('__TIT1__', f'{section_prefix}.title2')
    html = html.replace('__DES1__', f'{section_prefix}.desc2')
    html = html.replace('__AI1__', f'{section_prefix}.ai2')
    
    html = html.replace('__TAG2__', f'{section_prefix}.tag3')
    html = html.replace('__TIT2__', f'{section_prefix}.title3')
    html = html.replace('__DES2__', f'{section_prefix}.desc3')
    html = html.replace('__AI2__', f'{section_prefix}.ai3')
    
    html = html.replace('__TAG3__', f'{section_prefix}.tag4')
    html = html.replace('__TIT3__', f'{section_prefix}.title4')
    html = html.replace('__DES3__', f'{section_prefix}.desc4')
    html = html.replace('__AI3__', f'{section_prefix}.ai4')
    
    if section_prefix.startswith('radar') or section_prefix.startswith('archive'):
        html = html.replace('__D1__', f'{section_prefix}.d2')
        html = html.replace('__D2__', f'{section_prefix}.d3')
        html = html.replace('__D3__', f'{section_prefix}.d4')
        
        # Handle i1t,i1d,i1a -> i2t,i2d,i2a
        # and i2t,i2d,i2a -> i3t,i3d,i3a
        # and i3t,i3d,i3a -> i4t,i4d,i4a
        for old_suf, new_suf in [('1t', '2t'), ('1d', '2d'), ('1a', '2a')]:
            html = html.replace(f'{section_prefix}.i{old_suf}', f'__I{old_suf.upper()}__')
        for old_suf, new_suf in [('2t', '3t'), ('2d', '3d'), ('2a', '3a')]:
            html = html.replace(f'{section_prefix}.i{old_suf}', f'__I{old_suf.upper()}__')
        for old_suf, new_suf in [('3t', '4t'), ('3d', '4d'), ('3a', '4a')]:
            html = html.replace(f'{section_prefix}.i{old_suf}', f'__I{old_suf.upper()}__')
        
        # Now map back
        for old_suf, new_suf in [('1T', 'i2t'), ('1D', 'i2d'), ('1A', 'i2a')]:
            html = html.replace(f'__I{old_suf}__', f'{section_prefix}.{new_suf}')
        for old_suf, new_suf in [('2T', 'i3t'), ('2D', 'i3d'), ('2A', 'i3a')]:
            html = html.replace(f'__I{old_suf}__', f'{section_prefix}.{new_suf}')
        for old_suf, new_suf in [('3T', 'i4t'), ('3D', 'i4d'), ('3A', 'i4a')]:
            html = html.replace(f'__I{old_suf}__', f'{section_prefix}.{new_suf}')
    
    return html


def insert_i18n_entry(html, section_prefix, zh_vals, en_vals):
    """Insert new #1 i18n entries after the section label."""
    # Find where to insert - look for the first existing i18n entry for this section
    # and insert before it
    first_key = f'{section_prefix}.tag1'
    idx = html.find(first_key)
    if idx < 0:
        first_key = f'{section_prefix}.d1'  # for radar/archive
        idx = html.find(first_key)
    
    if idx < 0:
        print(f"WARNING: Could not find insertion point for {section_prefix}")
        return html
    
    # Build insertion text
    insert_text = f'\n    '
    for key, val in zh_vals.items():
        insert_text += f"'{section_prefix}.{key}':'{val}',"
    insert_text += f'\n    '
    for key, val in en_vals.items():
        insert_text += f"'{section_prefix}.{key}':'{val}',"
    insert_text += f'\n    '
    
    html = html[:idx] + insert_text + html[idx:]
    return html


# ====================================================================
# REMOVE OLD #4 CARDS (HTML sections)
# ====================================================================

# Main intel section - remove old #4 card (Thailand EEC)
# Find the old #4 card and remove it
html = delete_hardcoded_article(html, 'intel', 'invest', '2026-06-10 · Thailand', '', '', '')

# Radar section - remove old #4
html = delete_hardcoded_article(html, 'radar', 'invest', '2026-06-13 · Thailand', '', '', '')

# Archive section - remove old #4
html = delete_hardcoded_article(html, 'archive', 'invest', '2026-06-13 · Thailand', '', '', '')


# ====================================================================
# SHIFT I18N KEYS: delete old #4, shift 1->2, 2->3, 3->4
# ====================================================================

# Main intel section
html = shift_i18n_keys(html, 'intel')

# Radar section  
html = shift_i18n_keys(html, 'radar')

# Archive section
html = shift_i18n_keys(html, 'archive')


# ====================================================================
# INSERT NEW #1 CARDS AND I18N ENTRIES
# ====================================================================

# The old #4 cards have been removed. Now we need to:
# A) Insert new #1 HTML intel card in main section
# B) Insert new #1 HTML radar card in radar section
# C) Insert i18n entries

# Find the intel-grid div and insert the new card as #1
intel_grid_end = html.find('</div><!-- end intel-grid -->')
if intel_grid_end < 0:
    # Find the grid closing by looking for the row of 4 intel cards
    # The section has <!-- INTEL GRID --> marker or similar
    intel_grid_end = html.find('<div class="intel-grid"')
    if intel_grid_end >= 0:
        # Find the closing div
        grid_close = html.find('</div>', intel_grid_end)
        grid_close = html.find('</div>', grid_close + 1)
        grid_close = html.find('</div>', grid_close + 1) 
    else:
        grid_close = -1

# Simpler approach: just find the first intel-card and insert before it
first_card_pos = html.find('class="glass-card intel-card"')
if first_card_pos > 0:
    # Find the line start (last newline before this card)
    line_start = html.rfind('\n', 0, first_card_pos)
    line_start = html.rfind('\n', 0, line_start - 1) + 1
    
    new_intel_card = '''      <div class="glass-card intel-card"><div class="meta"><span class="tag tag-invest" data-i18n="intel.tag1">投资 / Investment</span><span class="date">2026-06-17 · Cambodia</span></div><h4 data-i18n="intel.title1">柬埔寨副首相赴韩招商，瞄准EV及高科制造业</h4><p data-i18n="intel.desc1">副首相孙占托率团赴韩路演，先后拜会三星电子、大柱KC集团等巨头，推动韩国投资进入汽车零部件、电动车系统及数字医疗领域，标志柬埔寨工业战略从传统制衣向高附加值制造业转型。</p><div class="ai-insight"><p><span class="label">AI 洞察</span><span data-i18n="intel.ai1">柬埔寨产业升级信号明确，EV供应链及配套基建将迎外资集中流入窗口，关注后续投资落地节奏与政策配套。</span></p></div></div>
'''
    html = html[:line_start] + new_intel_card + html[line_start:]

# Find radar cards section and insert new #1
# Find the first radar card
for section_name in ['radar', 'archive']:
    # Find cards in this section
    # Look for the second occurrence pattern - after the section title
    markers = [m.start() for m in re.finditer(r'class="glass-card intel-card"', html)]
    if not markers:
        continue
    
    # Find the intel-card in the i18n section vs HTML card section
    # The i18n JSON also has these strings but they're not HTML cards
    # Let's just find the specific section by context
    
    # For radar section - find the radar section content
    # Look for the section div containing radar data
    radar_section_idx = html.find('id="page-radar"')
    if radar_section_idx < 0:
        radar_section_idx = html.find('data-page="radar"')
    
    # For archive - find archive section
    archive_section_idx = html.find('id="page-archive"')
    if archive_section_idx < 0:
        archive_section_idx = html.find('data-page="archive"')
    
    target_idx = radar_section_idx if section_name == 'radar' else archive_section_idx
    if target_idx < 0:
        continue
    
    # Find first intel-card after this section
    search_from = target_idx
    card_pos = html.find('class="glass-card intel-card"', search_from)
    if card_pos < 0:
        continue
    
    # Find line start
    line_start = html.rfind('\n', 0, card_pos)
    line_start = html.rfind('\n', 0, line_start - 1) + 1
    
    if section_name == 'radar':
        new_card = '''      <div class="glass-card intel-card"><div class="meta"><span class="tag tag-invest">投资 / Investment</span><span class="date" data-i18n="radar.d1">2026-06-17 · Cambodia</span></div><h4 data-i18n="radar.i1t">柬埔寨副首相赴韩招商，瞄准EV及高科制造业</h4><p data-i18n="radar.i1d">副首相孙占托率团赴韩路演，先后拜会三星电子、大柱KC集团等巨头，推动韩国投资进入汽车零部件、电动车系统及数字医疗领域，标志柬埔寨工业战略从传统制衣向高附加值制造业转型。</p><div class="ai-insight"><p><span class="label">AI 洞察</span><span data-i18n="radar.i1a">柬埔寨产业升级信号明确，EV供应链及配套基建将迎外资集中流入窗口，关注后续投资落地节奏与政策配套。</span></p></div></div>
'''
    else:
        new_card = '''      <div class="glass-card intel-card"><div class="meta"><span class="tag tag-invest">投资</span><span class="date">2026-06-17 · Cambodia</span></div><h4 data-i18n="archive.i1t">柬埔寨副首相赴韩招商，瞄准EV及高科制造业</h4><p data-i18n="archive.i1d">副首相孙占托率团赴韩路演，先后拜会三星电子、大柱KC集团等巨头...</p><div class="ai-insight"><p><span class="label">AI 洞察</span><span data-i18n="archive.i1a">柬埔寨产业升级信号明确，EV供应链将迎外资集中流入窗口。</span></p></div></div>
'''
    
    html = html[:line_start] + new_card + html[line_start:]


# ====================================================================
# INSERT I18N ENTRIES
# ====================================================================

# Insert new intel entries
intel_zh = {
    'tag1': '投资 / Investment',
    'title1': NEW_TITLE,
    'desc1': NEW_DESC,
    'ai1': NEW_AI,
}
intel_en = {
    'tag1': 'Investment',
    'title1': NEW_TITLE_EN,
    'desc1': NEW_DESC_EN,
    'ai1': NEW_AI_EN,
}
html = insert_i18n_entry(html, 'intel', intel_zh, intel_en)

# Insert new radar entries
radar_zh = {
    'd1': NEW_DATE,
    'i1t': NEW_TITLE,
    'i1d': NEW_DESC,
    'i1a': NEW_AI,
}
radar_en = {
    'd1': NEW_DATE_EN,
    'i1t': NEW_TITLE_EN,
    'i1d': NEW_DESC_EN,
    'i1a': NEW_AI_EN,
}
html = insert_i18n_entry(html, 'radar', radar_zh, radar_en)

# Insert new archive entries
archive_zh = {
    'i1t': NEW_TITLE,
    'i1d': NEW_DESC,
    'i1a': NEW_AI,
}
archive_en = {
    'i1t': NEW_TITLE_EN,
    'i1d': NEW_DESC_EN,
    'i1a': NEW_AI_EN,
}
html = insert_i18n_entry(html, 'archive', archive_zh, archive_en)


# ====================================================================
# ENSURE NO DUPLICATE CARDS: Remove any remaining old #4 cards
# ====================================================================
# Check for any remaining old content
html = html.replace('2026-06-10 · Thailand', '')
html = html.replace('2026-06-13 · Thailand', '')


# ====================================================================
# WRITE OUTPUT
# ====================================================================
with open('decoded.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Updated decoded.html successfully")

# Verify: count intel cards
card_count = html.count('class="glass-card intel-card"')
print(f"Intel cards found: {card_count}")

# Check i18n entries
for section in ['intel', 'radar', 'archive']:
    for key in [f'{section}.tag1', f'{section}.title1', f'{section}.desc1', f'{section}.ai1']:
        if key in html:
            print(f"  ✅ {key} present")
        else:
            print(f"  ❌ {key} MISSING!")
