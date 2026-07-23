"""Direct article update script - bypasses buggy update_article_v2.py"""
import base64
import re
import subprocess
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent

def main():
    # Get clean HTML from git
    r = subprocess.run(
        ['git', 'show', 'HEAD:dist/index.html'],
        capture_output=True, text=True,
        cwd=PROJECT_DIR
    )
    html = r.stdout
    print(f'Clean HTML: {len(html):,} chars')

    # Article data
    title = '东南亚三国调整外资策略 聚焦产业链升级'
    desc = '泰国BOI力推新能源与智能制造，印尼启动6个新经济特区加码矿产深加工，马来西亚实施绩效导向投资激励框架。三大市场同步调整外资政策，争夺高端产业链布局。'
    tag_label = '投资 / Investment'
    meta = '2026-07-11 · Southeast Asia'
    insight = '东南亚从普惠税收优惠转向精准产业链激励，投资者应关注各国差异化政策窗口与配套优势。'

    # Find intel-grid section
    grid_match = re.search(
        r'(<div class="intel-grid">)(.*?)(</div>\s*</div>\s*</section>)',
        html, re.DOTALL
    )
    if not grid_match:
        print('ERROR: intel-grid not found')
        return False

    grid_open = grid_match.group(1)
    grid_content = grid_match.group(2)
    grid_close = grid_match.group(3)

    # Find existing cards
    card_pattern = re.compile(
        r'<div class="glass-card intel-card">.*?</div>\s*</div>',
        re.DOTALL,
    )
    cards = card_pattern.findall(grid_content)
    print(f'Found {len(cards)} cards')

    # Find max intel number
    max_n = 0
    for card in cards:
        for m in re.finditer(r'intel\.(?:title|desc|ai|tag|date)(\d+)', card):
            max_n = max(max_n, int(m.group(1)))
    new_n = max_n + 1
    print(f'New card number: intel.{new_n}')

    # Build new card
    new_card = f'''      <div class="glass-card intel-card"><div class="meta">
<span class="tag tag-investment" data-i18n="intel.tag{new_n}">{tag_label}</span>
<span class="date" data-i18n="intel.date{new_n}">{meta}</span>
</div>
<h4 data-i18n="intel.title{new_n}">{title}</h4>
<p data-i18n="intel.desc{new_n}">{desc}</p>
<div class="ai-insight"><p><span class="label">AI 洞察</span>
<span data-i18n="intel.ai{new_n}">{insight}</span></p></div>
</div>'''

    new_cards = [new_card] + cards
    # Keep max 4 cards, remove oldest
    if len(new_cards) > 4:
        removed = new_cards.pop(-1)
        rm_num = re.search(r'intel\.title(\d+)', removed)
        if rm_num:
            print(f'Removed oldest card intel.{rm_num.group(1)}')

    # Rebuild grid section
    new_grid = grid_open + '\n' + '\n'.join(new_cards) + '\n    ' + grid_close
    html = html[:grid_match.start()] + new_grid + html[grid_match.end():]

    # Update i18n data - find const locales
    locales_match = re.search(r'(const locales\s*=\s*\{)(.*?)(\};?\s*)', html, re.DOTALL)
    if not locales_match:
        print('ERROR: locales not found')
        return False

    body = locales_match.group(2)

    # Find zh locale
    zh_start = re.search(r"'zh'\s*:\s*\{", body)
    if not zh_start:
        zh_start = re.search(r'zh\s*:\s*\{', body)
    if not zh_start:
        print('ERROR: zh locale not found')
        return False

    # Brace balance for zh body
    depth = 0
    zh_begin = zh_start.end()
    zh_end = zh_begin
    for i in range(zh_begin, len(body)):
        if body[i] == '{':
            depth += 1
        elif body[i] == '}':
            if depth == 0:
                zh_end = i
                break
            depth -= 1

    zh_body = body[zh_begin:zh_end]

    # Add new entries
    entries = {
        f'intel.tag{new_n}': tag_label,
        f'intel.date{new_n}': meta,
        f'intel.title{new_n}': title,
        f'intel.desc{new_n}': desc,
        f'intel.ai{new_n}': insight,
    }

    for key, value in entries.items():
        quoted_key = f"'{key}'"
        pattern = re.compile(rf"({re.escape(quoted_key)}\s*:\s*)'[^']*'")
        if pattern.search(zh_body):
            zh_body = pattern.sub(lambda m: f"{m.group(1)}'{value}'", zh_body)
        else:
            if zh_body.rstrip().endswith(','):
                zh_body += f"\n    {quoted_key}:'{value}',"
            else:
                zh_body += f",\n    {quoted_key}:'{value}',"

    new_body = body[:zh_begin] + zh_body + body[zh_end:]
    html = html[:locales_match.start(2)] + new_body + html[locales_match.end(2):]

    print(f'Final HTML: {len(html):,} chars')

    # Write decoded HTML
    decoded_path = PROJECT_DIR / 'decoded.html'
    decoded_path.write_text(html, 'utf-8')
    print(f'Written {decoded_path}')

    # Encode and write index.b64
    b64 = base64.b64encode(html.encode('utf-8')).decode('ascii')
    b64_path = PROJECT_DIR / 'index.b64'
    b64_path.write_text(b64, 'utf-8')
    print(f'Written {b64_path} ({len(b64):,} chars)')

    # Also write to main index.html (may fail if locked, that's ok)
    try:
        index_path = PROJECT_DIR / 'index.html'
        index_path.write_text(html, 'utf-8')
        print(f'Written {index_path}')
    except PermissionError:
        print('Warning: index.html is locked, skipping')

    # Write to dist/index.html
    dist_dir = PROJECT_DIR / 'dist'
    if dist_dir.exists():
        dist_index = dist_dir / 'index.html'
        dist_index.write_text(html, 'utf-8')
        print(f'Written {dist_index}')

    print('Done!')
    return True

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
