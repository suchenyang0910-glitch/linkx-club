import base64
with open('D:/projects/linkx-club-new/index.b64', 'r') as f:
    data = base64.b64decode(f.read()).decode('utf-8')
print(data)
