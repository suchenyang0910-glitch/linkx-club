import base64, re
h = base64.b64decode(open('index.b64','r',encoding='utf-8').read().strip()).decode('utf-8')
for k, v in re.findall(r"'(intel\.(?:title|date|tag|desc|ai)\d+)'\s*:\s*'([^']*)'", h):
    print(k, '=>', v)
