import base64
with open('D:/projects/linkx-club-new/index.b64', 'r') as f:
    data = base64.b64decode(f.read()).decode('utf-8')

# Search for intel, article, or radar
for keyword in ['intel', 'article', 'radar', '每日', 'intel-card', 'intel-grid']:
    idx = data.lower().find(keyword.lower())
    if idx >= 0:
        print(f'Found "{keyword}" at position {idx}')
        start = max(0, idx - 100)
        print(data[start:idx+500])
        print('---')
