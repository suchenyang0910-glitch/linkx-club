import base64, re
h = base64.b64decode(open('index.b64', encoding='utf-8').read().strip()).decode('utf-8')
titles = dict(re.findall(r"'intel\.title(\d+)':'([^']*)'", h))
dates = dict(re.findall(r"'intel\.date(\d+)':'([^']*)'", h))
tags = dict(re.findall(r"'intel\.tag(\d+)':'([^']*)'", h))
for n in sorted(titles, key=lambda x: -int(x))[:8]:
    print(n, '|', dates.get(n, ''), '|', tags.get(n, ''), '|', titles[n])
