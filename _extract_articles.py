import base64
with open('D:/projects/linkx-club-new/index.b64', 'r') as f:
    data = base64.b64decode(f.read()).decode('utf-8')

# Find all intel-card divs with actual article content
# Look for intel-grid section with articles
idx = data.find('<!-- INTEL SECTION -->')
if idx < 0:
    idx = data.find('id="intel"')
if idx < 0:
    idx = data.find('intel-grid')

if idx >= 0:
    print(f"Found intel section at position {idx}")
    # Print next 5000 chars
    print(data[idx:idx+5000])
else:
    # Search for intel-card in the HTML body closer to where articles might be
    for i in range(10):
        pos = data.find('<div class="intel-card"', i*5000)
        if pos < 0:
            break
        print(f"--- intel-card #{i} at {pos} ---")
        print(data[pos:pos+2000])
