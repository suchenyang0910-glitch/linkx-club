"""Quick check of index.b64 content"""
import base64, re, sys

raw = open(r'D:\projects\linkx-club-new\index.b64', 'r', encoding='utf-8').read()
print(f'Base64 file size: {len(raw)} chars')

html = base64.b64decode(raw).decode('utf-8')
print(f'HTML size: {len(html)} chars')

# find intel-grid
m = re.search(r'<div class="intel-grid">', html)
if m:
    print(f'intel-grid found at pos {m.start()}')
else:
    print('intel-grid NOT FOUND')

# count cards
cards = re.findall(r'<div class="glass-card intel-card">.*?</div>\s*</div>', html, re.DOTALL)
print(f'Card count: {len(cards)}')
for i, c in enumerate(cards[-3:]):
    nums = re.findall(r'intel\.title(\d+)', c)
    print(f'  Card -{len(cards)-i}: nums={nums}')

# check locale data
loc = re.search(r'const locales\s*=', html)
if loc:
    print(f'const locales found at pos {loc.start()}')
else:
    print('const locales NOT FOUND')
