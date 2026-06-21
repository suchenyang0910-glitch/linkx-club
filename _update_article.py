import base64
import re

# Current articles and their i18n keys
# These are in order: #1 (newest) to #4 (oldest)
# After update: delete #4, shift #1->#2, #2->#3, #3->#4, insert new #1

NEW_ARTICLE = {
    "tag_class": "tag-policy",
    "tag_text": "政策 / Policy",
    "tag_key": "intel.tag1",
    "date": "2026-06-21",
    "country": "Thailand",
    "title": "泰国议会连批五大自贸协定",
    "title_key": "intel.title1",
    "desc": "泰国议会6月18日批准5项贸易协定，包含泰国-EFTA首个欧洲FTA及东盟-中国自贸区升级版，大幅拓展泰国出口市场准入。",
    "desc_key": "intel.desc1",
    "ai": "泰国首次与欧洲经济集团签署FTA，覆盖瑞士挪威等富裕市场，东南亚区域贸易一体化再提速。",
    "ai_key": "intel.ai1"
}

# Updated articles (shifted from old #1, #2, #3)
SHIFTED = [
    {  # was #1 -> becomes #2
        "tag_class": "tag-policy",
        "tag_text": "政策 / Policy",
        "tag_key": "intel.tag2",
        "date": "2026-06-15",
        "country": "Vietnam",
        "title": "越南放宽数字游民签证条件",
        "title_key": "intel.title2",
        "desc": "针对IT和创意产业从业者，胡志明市出台试行政策，允许凭海外收入证明直接申请1年期居留卡，免除繁琐劳工证办理。",
        "desc_key": "intel.desc2",
        "ai": "利好出海服务商及办公地产，短期内将吸引大量周边国家华人 nomad 流入。",
        "ai_key": "intel.ai2"
    },
    {  # was #2 -> becomes #3
        "tag_class": "tag-market",
        "tag_text": "市场 / Market",
        "tag_key": "intel.tag3",
        "date": "2026-06-14",
        "country": "Indonesia",
        "title": "印尼电商新规实施两月后复盘",
        "title_key": "intel.title3",
        "desc": "社交电商与传统电商分离政策落地后，本土中小商家流量下滑30%，但客单价提升15%。本土仓配服务商迎来爆发式增长。",
        "desc_key": "intel.desc3",
        "ai": "纯流量打法失效，转向重资产的供应链合规运营。投资仓储物流服务是当前最佳切入点。",
        "ai_key": "intel.ai3"
    },
    {  # was #3 -> becomes #4
        "tag_class": "tag-visa",
        "tag_text": "签证 / Visa",
        "tag_key": "intel.tag4",
        "date": "2026-06-12",
        "country": "Malaysia",
        "title": "大马第二家园 (MM2H) 门槛微调",
        "title_key": "intel.title4",
        "desc": "内政部宣布对来自东盟成员国的申请人实行资金门槛八折优惠，旨在促进区域内高净值人群流动。",
        "desc_key": "intel.desc4",
        "ai": "对持新加坡、泰国等长居的华人形成极强吸引力，新山房产询盘量预计本月内上涨。",
        "ai_key": "intel.ai4"
    }
]

def make_article_card(a):
    return (
        f'      <div class="glass-card intel-card">'
        f'<div class="meta">'
        f'<span class="tag {a["tag_class"]}" data-i18n="{a["tag_key"]}">{a["tag_text"]}</span>'
        f'<span class="date">{a["date"]} · {a["country"]}</span>'
        f'</div>'
        f'<h4 data-i18n="{a["title_key"]}">{a["title"]}</h4>'
        f'<p data-i18n="{a["desc_key"]}">{a["desc"]}</p>'
        f'<div class="ai-insight"><p>'
        f'<span class="label">AI 洞察</span>'
        f'<span data-i18n="{a["ai_key"]}">{a["ai"]}</span>'
        f'</p></div></div>'
    )

# Build the new intel-grid block
all_articles = [NEW_ARTICLE] + SHIFTED
new_intel_block = '<div class="intel-grid">\n' + '\n'.join(make_article_card(a) for a in all_articles) + '\n    </div>'

# Read and decode
with open('D:/projects/linkx-club-new/index.b64', 'r') as f:
    raw = f.read()
data = base64.b64decode(raw).decode('utf-8')

# Find the intel-grid section
pattern = r'<div class="intel-grid">(?:\s*<div class="glass-card intel-card">.*?</div></div>\s*)+?\s*</div>'
match = re.search(pattern, data, re.DOTALL)

if not match:
    print("ERROR: Could not find intel-grid section")
    # Try a different approach - find by explicit string
    idx_start = data.find('<div class="intel-grid">')
    if idx_start >= 0:
        # Find end of this grid
        # Count depth
        depth = 0
        found = False
        for i in range(idx_start, len(data)):
            if data[i:i+6] == '<div c' and 'intel-grid' in data[i:i+50]:
                depth += 1
            if data[i:i+4] == '<div':
                # Count opening divs
                pass
        
        print(f"Found intel-grid at {idx_start}")
        # Find closing </div> of intel-grid
        idx_end = data.find('</div>', idx_start)
        for _ in range(3):
            idx_end = data.find('</div>', idx_end + 6)
        
        print(f"Cut from {idx_start} to {idx_end+6}")
        print(f"Content: {data[idx_start:idx_end+10]}")
else:
    print(f"Found intel-grid match from {match.start()} to {match.end()}")
    old_section = match.group(0)
    
    # Replace
    new_data = data.replace(old_section, new_intel_block, 1)
    
    # Verify
    if new_data == data:
        print("ERROR: No replacement happened")
    else:
        # Encode and save
        encoded = base64.b64encode(new_data.encode('utf-8')).decode('ascii')
        with open('D:/projects/linkx-club-new/index.b64', 'w') as f:
            f.write(encoded)
        print(f"SUCCESS: Updated index.b64 ({len(encoded)} bytes)")
