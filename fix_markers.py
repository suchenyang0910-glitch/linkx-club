#!/usr/bin/env python3
import re

with open('decoded.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix stale markers
html = html.replace('__RDR_D__4', 'radar.d4')
html = html.replace('__RDR_D__', '')
html = html.replace('__RDR_', '')
html = html.replace('__ARC_I4T__', '')
html = html.replace('__ARC_I4D__', '')
html = html.replace('__ARC_I4A__', '')
html = html.replace('__ARC_', '')

# Clean up any other stale __ markers
html = re.sub(r'__[A-Z_]+__', '', html)

# Count markers  
markers = re.findall(r'__[A-Z_]+__', html)
print(f"Remaining stale markers: {len(markers)}")
if markers:
    print("First few:", markers[:5])

# Check count
print(f"Total intel-card: {html.count('glass-card intel-card')}")

with open('decoded.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Done!")
