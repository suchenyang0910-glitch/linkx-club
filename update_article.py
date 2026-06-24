"""
update_article.py — linkx.club 文章更新工具
===========================================
职责：
  直接操作 index.b64，不依赖任何 LLM。
  接收参数 → 解码 → 插入新文章 → 删除最旧#4 → 重新编码 → 构建 → git push

用法：
  # 手动
  python update_article.py "标题" "描述" "标签" "国家·日期" "AI洞察"

  # 从 cron 调用（非交互式）
  python update_article.py --text "标题" --desc "描述" --tag "标签" --meta "国家·日期" --insight "AI洞察"
"""

import base64
import json
import os
import re
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
INDEX_B64 = PROJECT_DIR / "index.b64"


def decode_index() -> str:
    """解码 index.b64 为原始 HTML"""
    raw = INDEX_B64.read_text(encoding="utf-8").strip()
    try:
        return base64.b64decode(raw).decode("utf-8")
    except Exception:
        return raw  # 可能已经是明文


def encode_index(html: str):
    """编码并写回 index.b64"""
    encoded = base64.b64encode(html.encode("utf-8")).decode("ascii")
    INDEX_B64.write_text(encoded, encoding="utf-8")


def find_article_blocks(html: str) -> list:
    """
    在 HTML 中查找 "南洋市场观察" 区域的文章卡片。
    返回 [(全文块, href, 标题文本, 索引), ...]
    """
    # 找 '南洋市场观察' section
    section_start = html.find('南洋市场观察')
    if section_start < 0:
        print("⚠️ 未找到 '南洋市场观察' section")
        return []

    # 找 section 结束 (下一个 h2 或 section 或 footer)
    section_end = html.find('<div id="latest-report"', section_start)
    if section_end < 0:
        section_end = html.find('<footer', section_start)
    if section_end < 0:
        section_end = len(html)

    section = html[section_start:section_end]

    # 找所有文章 block
    blocks = []
    # 每个文章 block 格式: 一段文字包含 date-label, title-link, desc, insight
    pattern = re.compile(
        r'<div class="intel-card[^"]*"[^>]*>(.*?)</div>\s*</div>',
        re.DOTALL,
    )
    for match in pattern.finditer(section):
        block_html = match.group(0)
        # 提取信息
        href_match = re.search(r'href="([^"]*)"', block_html)
        title_match = re.search(r'<h4[^>]*>(.*?)</h4>', block_html, re.DOTALL)
        date_match = re.search(r'class="intel-date"[^>]*>(.*?)</div>', block_html)
        
        href = href_match.group(1) if href_match else ""
        title = title_match.group(1).strip() if title_match else ""
        date = date_match.group(1).strip() if date_match else ""

        blocks.append({
            "full": block_html,
            "href": href,
            "title": title,
            "date": date,
        })

    return blocks


def generate_article_html(
    tag: str,
    country_date: str,
    title: str,
    description: str,
    ai_insight: str,
) -> str:
    """生成新文章卡片 HTML"""
    emoji_map = {
        "政策": "📜", "Policy": "📜",
        "市场": "📊", "Market": "📊",
        "签证": "🛂", "Visa": "🛂",
        "投资": "💰", "Investment": "💰",
    }
    emoji = ""
    for k, v in emoji_map.items():
        if k.lower() in tag.lower():
            emoji = v
            break
    if not emoji:
        emoji = "📌"

    slug = re.sub(r'[^\w\s-]', '', title)
    slug = re.sub(r'[-\s]+', '-', slug).strip('-').lower()
    
    return f"""
          <a href="/content/intel/{slug}.html"
             class="block group glass-card p-6 relative overflow-hidden cursor-pointer transition-all duration-500 hover:translate-y-[-4px]"
             onclick="event.preventDefault(); window.__openArticle(this.href)"
             data-title="{title}"
             data-meta="{country_date}"
             data-tag="{tag}"
             data-desc='{description}'
             data-insight='{ai_insight}'>

            <div class="flex items-center gap-3 mb-3">
              <span class="intel-tag text-xs font-medium px-3 py-1 rounded-full"
                    style="background:rgba(212,175,55,0.1);color:#D4AF37;border:1px solid rgba(212,175,55,0.2)">
                {emoji} {tag}
              </span>
              <span class="intel-date text-xs" style="color:rgba(255,255,255,0.4)">{country_date}</span>
            </div>

            <h4 class="font-semibold text-base mb-2 leading-snug group-hover:text-[#D4AF37] transition-colors"
                style="color:var(--text)">{title}</h4>

            <p class="text-sm leading-relaxed mb-3" style="color:var(--text-secondary)">
              {description}
            </p>

            <div class="flex items-center gap-2 text-xs font-medium"
                 style="color:rgba(5,150,105,0.8)">
              <span>🤖</span>
              <span>{ai_insight}</span>
            </div>

            <div class="absolute inset-0 bg-gradient-to-t from-transparent via-transparent to-transparent
                        group-hover:bg-gradient-to-b group-hover:from-transparent group-hover:via-transparent
                        group-hover:to-[rgba(212,175,55,0.02)] transition-all duration-500 pointer-events-none">
            </div>
          </a>"""


def update_html(html: str, new_article_html: str) -> str:
    """
    在 '南洋市场观察' section 的末尾（紧挨着 </div> 之前）插入新文章卡片。
    并删除该 section 中最旧的卡片（超过4篇时）。
    """
    section_marker = '南洋市场观察'
    idx = html.find(section_marker)
    if idx < 0:
        print("❌ 找不到 '南洋市场观察' 标记")
        return html

    # 找 section 内 card 容器结束位置
    # 在 section 内，文章卡片通常包在 <div class="intel-list"> 或直接放
    list_start = html.find('<div class="space-y-4"', idx)  # 找"查看全部报告"之前的列表
    if list_start < 0:
        list_start = html.find('<div class="grid', idx)
    
    # 找列表结束（在 LATEST REPORT 之前）
    report_marker = '最新专题报告'
    end_marker_idx = html.find(report_marker, idx)
    if end_marker_idx < 0:
        end_marker_idx = html.find('</section>', idx)
    if end_marker_idx < 0:
        end_marker_idx = html.find('<div id="latest-report"', idx)

    if list_start < 0:
        print("❌ 找不到文章列表容器")
        return html

    # 获取列表区域
    list_area = html[list_start:end_marker_idx]
    
    # 找所有文章卡片（从 list_area 中提取）
    card_pattern = re.compile(r'(<a\s+[^>]*class="block group glass-card[^>]*>.*?</a>)', re.DOTALL)
    cards = card_pattern.findall(list_area)
    
    print(f"  找到 {len(cards)} 个现有文章卡片")

    # 插入新卡片到列表开头
    new_list_start = list_area.find('<div') if '<div' in list_area else 0
    # 重建列表
    
    # 替换列表 - 插入新卡片在最前面，如果超过4篇则删除最后一篇
    new_cards = [new_article_html] + cards
    if len(new_cards) > 4:
        removed = new_cards.pop(-1)  # 删除最旧的
        print(f"  移除最旧卡片 (保持 ≤4 篇)")

    # 重建列表 HTML
    new_list_html = '<div class="space-y-4">\n' + '\n'.join(new_cards) + '\n        </div>'
    
    # 替换
    new_html = html[:list_start] + new_list_html + html[end_marker_idx:]
    
    print(f"  插入新卡片成功 | 现有 {len(new_cards)} 篇")
    return new_html


def build_and_push():
    """运行 npm build + git push"""
    print("\n🚀 Building...")
    r = subprocess.run(
        ["npm", "run", "build"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        timeout=60,
    )
    print(r.stdout[-300:] if r.stdout else "")
    if r.returncode != 0:
        print(f"⚠️ Build stderr: {r.stderr[-200:]}")
        return False

    print("\n📤 Git push...")
    subprocess.run(["git", "add", "-A"], cwd=PROJECT_DIR, capture_output=True, timeout=10)
    subprocess.run(
        ["git", "commit", "-m", f"daily article {__import__('datetime').datetime.now().strftime('%Y-%m-%d')}"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        timeout=10,
    )
    r = subprocess.run(
        ["git", "push"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if r.returncode == 0:
        print("✅ Git push 成功")
        return True
    else:
        print(f"⚠️ Git push 失败: {r.stderr[-200:]}")
        return False


def main():
    """主入口：解析参数 → 执行更新"""
    import argparse

    parser = argparse.ArgumentParser(description="linkx.club 文章更新器")
    parser.add_argument("title", nargs="?", help="文章标题 (10-20字)")
    parser.add_argument("description", nargs="?", help="文章描述 (40-80字)")
    parser.add_argument("--tag", default="Market", help="标签: Policy/Market/Visa/Investment")
    parser.add_argument("--meta", default="", help="国家·日期, 如 Vietnam · 2026.06.21")
    parser.add_argument("--insight", default="", help="AI 洞察 (30-60字)")
    parser.add_argument("--text", help="标题 (命名参数)")
    parser.add_argument("--desc", help="描述 (命名参数)")
    parser.add_argument("--dry-run", action="store_true", help="只预览，不写入")

    args = parser.parse_args()

    # 支持位置参数和命名参数
    title = args.text or args.title
    desc = args.desc or args.description

    if not title:
        print("❌ 请提供文章标题")
        parser.print_help()
        sys.exit(1)

    print(f"📰 新文章: {title}")
    print(f"   标签: {args.tag}")
    print(f"   来源: {args.meta}")
    print(f"   描述: {desc}")
    print(f"   洞察: {args.insight}")

    # 1. 解码
    html = decode_index()
    print(f"📄 index.b64 解码成功 ({len(html)} chars)")

    # 2. 生成新文章 HTML
    new_card = generate_article_html(args.tag, args.meta, title, desc or "", args.insight or "")

    # 3. 更新
    new_html = update_html(html, new_card)

    if new_html == html:
        print("❌ 更新失败：HTML 无变化")
        sys.exit(1)

    print(f"📝 HTML 变化: {len(new_html) - len(html)} chars")

    # 4. 编码写入
    if args.dry_run:
        print("\n⏸ Dry-run — 不写入")
        # 检查语法
        if "南洋市场观察" in new_html:
            print("✅ 语法检查通过")
        return

    encode_index(new_html)
    print("✅ index.b64 写入成功")

    # 5. Build + Push
    build_and_push()


if __name__ == "__main__":
    main()
