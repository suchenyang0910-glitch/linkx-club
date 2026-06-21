#!/usr/bin/env python3
import re

with open('decoded.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Article data
NEW_DATE = '2026-06-17 \u00b7 Cambodia'
NEW_ZH_TAG = '\u6295\u8d44 / Investment'
NEW_ZH_TITLE = '\u67ec\u57d4\u5be8\u526f\u9996\u76f8\u8d74\u97e9\u62db\u5546\u5f15\u8d44\uff0c\u7784\u51c6EV\u53ca\u9ad8\u79d1\u5236\u9020\u4e1a'
NEW_ZH_DESC = '\u526f\u9996\u76f8\u5b59\u5360\u6258\u7387\u56e2\u8d74\u97e9\u8def\u6f14\uff0c\u5148\u540e\u62dc\u4f1a\u4e09\u661f\u7535\u5b50\u3001\u5927\u67f1KC\u96c6\u56e2\u7b49\u5de8\u5934\uff0c\u63a8\u52a8\u97e9\u56fd\u6295\u8d44\u8fdb\u5165\u6c7d\u8f66\u96f6\u90e8\u4ef6\u3001\u7535\u52a8\u8f66\u7cfb\u7edf\u53ca\u6570\u5b57\u533b\u7597\u9886\u57df\uff0c\u6807\u5fd7\u67ec\u57d4\u5be8\u5de5\u4e1a\u6218\u7565\u4ece\u4f20\u7edf\u5236\u8863\u5411\u9ad8\u9644\u52a0\u503c\u5236\u9020\u4e1a\u8f6c\u578b\u3002'
NEW_ZH_AI = '\u67ec\u57d4\u5be8\u4ea7\u4e1a\u5347\u7ea7\u4fe1\u53f7\u660e\u786e\uff0cEV\u4f9b\u5e94\u94fe\u53ca\u914d\u5957\u57fa\u5efa\u5c06\u8fce\u5916\u8d44\u96c6\u4e2d\u6d41\u5165\u7a97\u53e3\uff0c\u5173\u6ce8\u540e\u7eed\u6295\u8d44\u843d\u5730\u8282\u594f\u4e0e\u653f\u7b56\u914d\u5957\u3002'

NEW_EN_TAG = 'Investment'
NEW_EN_TITLE = "Cambodia Deputy PM Courts Korean Investment in EV & High-Tech Manufacturing"
NEW_EN_DESC = "Deputy PM Sun Chanthol led a roadshow in Korea, meeting Samsung and Daejoo KC Group to attract investment in auto parts, EV systems, and digital healthcare \u2014 signaling a strategic shift from garments to higher-value manufacturing."
NEW_EN_AI = "Clear signal of Cambodia's industrial upgrade. EV supply chain and infrastructure will see concentrated foreign capital inflows. Watch policy support and deal execution."

# ============ 1. Remove old #4 from all sections ============
# Intel section (date 2026-06-10 + Thailand)
old4_pat = r'<div class="glass-card intel-card"><div class="meta"><span class="tag tag-invest" data-i18n="intel\.tag4">\u6295\u8d44 / Investment</span><span class="date">2026-06-10 \u00b7 Thailand</span></div><h4 data-i18n="intel\.title4">[^<]*</h4><p data-i18n="intel\.desc4">[^<]*</p><div class="ai-insight"><p><span class="label">AI \u6d1e\u5bdf</span><span data-i18n="intel\.ai4">[^<]*</span></p></div></div>'
html = re.sub(old4_pat, '', html)

# Radar section (date 2026-06-13 + Thailand, uses radar.d4, radar.i4t etc)
old4_radar = r'<div class="glass-card intel-card"><div class="meta"><span class="tag tag-invest">\u6295\u8d44 / Investment</span><span class="date" data-i18n="radar\.d4">2026-06-13 \u00b7 Thailand</span></div><h4 data-i18n="radar\.i4t">[^<]*</h4><p data-i18n="radar\.i4d">[^<]*</p><div class="ai-insight"><p><span class="label">AI \u6d1e\u5bdf</span><span data-i18n="radar\.i4a">[^<]*</span></p></div></div>'
html = re.sub(old4_radar, '', html)

# Archive section (date 2026-06-13 + Thailand, uses archive.i4t etc)
old4_arch = r'<div class="glass-card intel-card"><div class="meta"><span class="tag tag-invest">\u6295\u8d44</span><span class="date">2026-06-13 \u00b7 Thailand</span></div><h4 data-i18n="archive\.i4t">[^<]*</h4><p data-i18n="archive\.i4d">[^<]*</p><div class="ai-insight"><p><span class="label">AI \u6d1e\u5bdf</span><span data-i18n="archive\.i4a">[^<]*</span></p></div></div>'
html = re.sub(old4_arch, '', html)

# ============ 2. Shift i18n keys ============
# Intel section: 1->2, 2->3, 3->4
for suffix in ['tag', 'title', 'desc', 'ai']:
    for old_num, new_num in [('1', 'Z2'), ('2', 'Z3'), ('3', 'Z4')]:
        html = html.replace(f'intel.{suffix}{old_num}', f'__INTEL_{suffix.upper()}{new_num}__')
for suffix in ['tag', 'title', 'desc', 'ai']:
    html = html.replace(f'__INTEL_{suffix.upper()}Z2__', f'intel.{suffix}2')
    html = html.replace(f'__INTEL_{suffix.upper()}Z3__', f'intel.{suffix}3')
    html = html.replace(f'__INTEL_{suffix.upper()}Z4__', f'intel.{suffix}4')

# Radar section
radar_keys = {'d': 'd', 'i1t': 'i1t', 'i1d': 'i1d', 'i1a': 'i1a',
              'i2t': 'i2t', 'i2d': 'i2d', 'i2a': 'i2a',
              'i3t': 'i3t', 'i3d': 'i3d', 'i3a': 'i3a',
              'i4t': 'i4t', 'i4d': 'i4d', 'i4a': 'i4a'}
for old_key in radar_keys:
    html = html.replace(f'radar.{old_key}', f'__RDR_{old_key.upper()}__')

# old1->2, old2->3, old3->4
html = html.replace('__RDR_D1__', 'radar.d2')
html = html.replace('__RDR_D2__', 'radar.d3')
html = html.replace('__RDR_D3__', 'radar.d4')

html = html.replace('__RDR_I1T__', 'radar.i2t')
html = html.replace('__RDR_I2T__', 'radar.i3t')
html = html.replace('__RDR_I3T__', 'radar.i4t')

html = html.replace('__RDR_I1D__', 'radar.i2d')
html = html.replace('__RDR_I2D__', 'radar.i3d')
html = html.replace('__RDR_I3D__', 'radar.i4d')

html = html.replace('__RDR_I1A__', 'radar.i2a')
html = html.replace('__RDR_I2A__', 'radar.i3a')
html = html.replace('__RDR_I3A__', 'radar.i4a')

# Archive section
for old_key in ['i1t', 'i1d', 'i1a', 'i2t', 'i2d', 'i2a', 'i3t', 'i3d', 'i3a', 'i4t', 'i4d', 'i4a']:
    html = html.replace(f'archive.{old_key}', f'__ARC_{old_key.upper()}__')

html = html.replace('__ARC_I1T__', 'archive.i2t')
html = html.replace('__ARC_I2T__', 'archive.i3t')
html = html.replace('__ARC_I3T__', 'archive.i4t')

html = html.replace('__ARC_I1D__', 'archive.i2d')
html = html.replace('__ARC_I2D__', 'archive.i3d')
html = html.replace('__ARC_I3D__', 'archive.i4d')

html = html.replace('__ARC_I1A__', 'archive.i2a')
html = html.replace('__ARC_I2A__', 'archive.i3a')
html = html.replace('__ARC_I3A__', 'archive.i4a')

# ============ 3. Insert new #1 HTML cards ============
# Main intel section
main_pos = html.find('<div class="intel-grid">')
if main_pos >= 0:
    first_card = html.find('<div class="glass-card intel-card"', main_pos)
    line_start = html.rfind('\n', 0, first_card - 5) + 1
    new_card_zh = f'''      <div class="glass-card intel-card"><div class="meta"><span class="tag tag-invest" data-i18n="intel.tag1">{NEW_ZH_TAG}</span><span class="date">{NEW_DATE}</span></div><h4 data-i18n="intel.title1">{NEW_ZH_TITLE}</h4><p data-i18n="intel.desc1">{NEW_ZH_DESC}</p><div class="ai-insight"><p><span class="label">AI \u6d1e\u5bdf</span><span data-i18n="intel.ai1">{NEW_ZH_AI}</span></p></div></div>
'''
    html = html[:line_start] + new_card_zh + html[line_start:]

# Radar section
radar_pos = html.find('id="page-radar"')
if radar_pos < 0:
    radar_pos = html.find('data-page="radar"')
if radar_pos >= 0:
    first_radar = html.find('<div class="glass-card intel-card"', radar_pos)
    if first_radar >= 0:
        line_start = html.rfind('\n', 0, first_radar - 5) + 1
        new_radar = f'''      <div class="glass-card intel-card"><div class="meta"><span class="tag tag-invest">{NEW_ZH_TAG}</span><span class="date" data-i18n="radar.d1">{NEW_DATE}</span></div><h4 data-i18n="radar.i1t">{NEW_ZH_TITLE}</h4><p data-i18n="radar.i1d">{NEW_ZH_DESC}</p><div class="ai-insight"><p><span class="label">AI \u6d1e\u5bdf</span><span data-i18n="radar.i1a">{NEW_ZH_AI}</span></p></div></div>
'''
        html = html[:line_start] + new_radar + html[line_start:]

# Archive section
arch_pos = html.find('intel-grid" style="margin-bottom:32px"')
if arch_pos >= 0:
    first_arch = html.find('<div class="glass-card intel-card"', arch_pos)
    if first_arch >= 0:
        line_start = html.rfind('\n', 0, first_arch - 5) + 1
        new_arch = f'''      <div class="glass-card intel-card"><div class="meta"><span class="tag tag-invest">{NEW_ZH_TAG}</span><span class="date">{NEW_DATE}</span></div><h4 data-i18n="archive.i1t">{NEW_ZH_TITLE}</h4><p data-i18n="archive.i1d">{NEW_ZH_DESC}</p><div class="ai-insight"><p><span class="label">AI \u6d1e\u5bdf</span><span data-i18n="archive.i1a">{NEW_ZH_AI}</span></p></div></div>
'''
        html = html[:line_start] + new_arch + html[line_start:]

# ============ 4. Insert new i18n entries ============
def insert_i18n(html, section, zh_entries, en_entries):
    """Insert i18n entries before the first existing key for this section."""
    # Find first existing key
    for key in zh_entries:
        search = f"'{section}.{key}'"
        idx = html.find(search)
        if idx >= 0:
            insert_text = ''
            for k, v in zh_entries.items():
                val_escaped = v.replace("'", "\\'")
                insert_text += f"    '{section}.{k}':'{val_escaped}',\n"
            for k, v in en_entries.items():
                val_escaped = v.replace("'", "\\'")
                insert_text += f"    '{section}.{k}':'{val_escaped}',\n"
            html = html[:idx] + insert_text + html[idx:]
            break
    return html

html = insert_i18n(html, 'intel', 
    {'tag1': NEW_ZH_TAG, 'title1': NEW_ZH_TITLE, 'desc1': NEW_ZH_DESC, 'ai1': NEW_ZH_AI},
    {'tag1': NEW_EN_TAG, 'title1': NEW_EN_TITLE, 'desc1': NEW_EN_DESC, 'ai1': NEW_EN_AI})

html = insert_i18n(html, 'radar',
    {'d1': NEW_DATE, 'i1t': NEW_ZH_TITLE, 'i1d': NEW_ZH_DESC, 'i1a': NEW_ZH_AI},
    {'d1': NEW_DATE, 'i1t': NEW_EN_TITLE, 'i1d': NEW_EN_DESC, 'i1a': NEW_EN_AI})

html = insert_i18n(html, 'archive',
    {'i1t': NEW_ZH_TITLE, 'i1d': NEW_ZH_DESC, 'i1a': NEW_ZH_AI},
    {'i1t': NEW_EN_TITLE, 'i1d': NEW_EN_DESC, 'i1a': NEW_EN_AI})

# ============ 5. Clean up stale markers ============
html = html.replace('__RDR_D4__', '')
html = html.replace('__RDR_I4T__', '')
html = html.replace('__RDR_I4D__', '')
html = html.replace('__RDR_I4A__', '')
html = html.replace('__ARC_I4T__', '')
html = html.replace('__ARC_I4D__', '')
html = html.replace('__ARC_I4A__', '')

# ============ 6. Verify ============
print("Verification:")
print(f"  Old Thailand intel: {'2026-06-10' in html}")
print(f"  Old Thailand radar: {'2026-06-13' in html}")
print(f"  New intel tag1: {'intel.tag1' in html}")
print(f"  New intel title1: {'intel.title1' in html}")
print(f"  New radar d1: {'radar.d1' in html}")
print(f"  New radar i1t: {'radar.i1t' in html}")
print(f"  New archive i1t: {'archive.i1t' in html}")
print(f"  Intel-card count: {html.count('glass-card intel-card')}")
print(f"  Stale markers: {html.count('__INTEL_') + html.count('__RDR_') + html.count('__ARC_')}")

with open('decoded.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Saved!")
