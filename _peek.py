import base64, re
html = base64.b64decode(open('index.b64','r',encoding='utf-8').read().strip()).decode('utf-8')
pairs = {}
for m in re.finditer(r"'intel\.(title|date|tag|desc|ai)(\d+)'\s*:\s*'([^']*)'", html):
    pairs.setdefault(int(m.group(2)), {})[m.group(1)] = m.group(3)
for n in sorted(pairs):
    d = pairs[n]
    print(f"#{n} [{d.get('tag','')}] {d.get('date','')} | {d.get('title','')}")
print("total:", len(pairs))
