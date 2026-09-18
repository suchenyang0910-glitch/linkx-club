import base64, re
h = base64.b64decode(open('index.b64', 'r', encoding='utf-8').read().strip()).decode('utf-8')
print("len", len(h))
# find zh locale intel entries
for key in ['date', 'tag', 'ai']:
    print("==", key)
    for m in re.findall(r"'intel\." + key + r"\d+'\s*:\s*'[^']*'", h):
        print(" ", m)
