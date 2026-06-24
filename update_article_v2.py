"""
update_article_v2.py — linkx.club 文章更新工具 (i18n 版)
=======================================================
linkx.club 的文章使用 JS locales 对象管理多语言内容。
本脚本正确处理卡片编号和 i18n 数据更新。

用法:
  python update_article_v2.py --title "标题" --desc "描述" --tag "Policy" --meta "2026-06-21 · Thailand" --insight "AI洞察"
  python update_article_v2.py ... --dry-run    只预览不写入
  python update_article_v2.py ... --skip-push  写入但不 git push
"""

import argparse
import base64
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
INDEX_B64 = PROJECT_DIR / "index.b64"

TAG_CONFIG = {
    "Policy":    {"css": "tag-policy",    "label": "政策 / Policy",    "emoji": "📜"},
    "Market":    {"css": "tag-market",    "label": "市场 / Market",    "emoji": "📊"},
    "Visa":      {"css": "tag-visa",      "label": "签证 / Visa",      "emoji": "🛂"},
    "Investment":{"css": "tag-investment","label": "投资 / Investment","emoji": "💰"},
}


def decode() -> str:
    raw = INDEX_B64.read_text("utf-8").strip()
    try:
        return base64.b64decode(raw).decode("utf-8")
    except:
        return raw


def encode(html: str):
    b64 = base64.b64encode(html.encode("utf-8")).decode("ascii")
    INDEX_B64.write_text(b64, "utf-8")
    # Also write decoded HTML to index.html and dist/index.html for live serving
    (PROJECT_DIR / "index.html").write_text(html, "utf-8")
    dist_dir = PROJECT_DIR / "dist"
    if dist_dir.exists():
        (dist_dir / "index.html").write_text(html, "utf-8")
    print("鉁?index.html + dist/index.html written")


def update(html: str, tag: str, meta: str, title: str, desc: str, insight: str) -> str:
    tc = TAG_CONFIG.get(tag, TAG_CONFIG["Market"])

    grid_match = re.search(
        r'(<div class="intel-grid">)(.*?)(</div>\s*</div>\s*</section>)',
        html, re.DOTALL,
    )
    if not grid_match:
        print("❌ 找不到 intel-grid 容器")
        return html

    grid_open = grid_match.group(1)
    grid_content = grid_match.group(2)
    grid_close = grid_match.group(3)

    card_pattern = re.compile(
        r'<div class="glass-card intel-card">.*?</div>\s*</div>',
        re.DOTALL,
    )
    cards = card_pattern.findall(grid_content)
    print(f"  找到 {len(cards)} 张现有卡片")

    if not cards:
        print("❌ 卡片解析失败")
        return html

    # 最大编号
    max_n = 0
    for card in cards:
        for m in re.finditer(r'intel\.(?:title|desc|ai|tag|date)(\d+)', card):
            max_n = max(max_n, int(m.group(1)))
    new_n = max_n + 1
    print(f"  新文章编号: intel.{new_n}")

    # 构建新卡片
    new_card = (
        f'      <div class="glass-card intel-card">'
        f'<div class="meta">'
        f'<span class="tag {tc["css"]}" data-i18n="intel.tag{new_n}">{tc["label"]}</span>'
        f'<span class="date" data-i18n="intel.date{new_n}">{meta}</span>'
        f'</div>'
        f'<h4 data-i18n="intel.title{new_n}">{title}</h4>'
        f'<p data-i18n="intel.desc{new_n}">{desc}</p>'
        f'<div class="ai-insight"><p><span class="label">AI 洞察</span>'
        f'<span data-i18n="intel.ai{new_n}">{insight}</span></p></div>'
        f'</div>'
    )

    new_cards = [new_card] + cards
    if len(new_cards) > 4:
        removed = new_cards.pop(-1)
        rm_num = re.search(r'intel\.title(\d+)', removed)
        if rm_num:
            print(f"  移除最旧卡片 #intel.{rm_num.group(1)}")

    result = (
        html[:grid_match.start()]
        + grid_open + "\n" + "\n".join(new_cards) + "\n    " + grid_close
        + html[grid_match.end():]
    )

    # 更新 i18n JS 数据
    result = update_i18n_data(result, new_n, tc["label"], meta, title, desc, insight)
    return result


def update_i18n_data(html: str, n: int, tag_label: str, meta: str, title: str, desc: str, insight: str) -> str:
    """更新 const locales = { zh: { ... } } 中的 intel 字段"""
    # 找到 const locales = { ... }  (可能以 }; 或仅 } 结尾)
    m = re.search(r'(const locales\s*=\s*\{)(.*?)(\};?\s*)', html, re.DOTALL)
    if not m:
        # fallback: 找第一个 const locales 然后平衡括号
        idx = html.find('const locales')
        if idx < 0:
            print("  ⚠️ 未找到 const locales")
            return html
        brace_start = html.index('{', idx + 14)
        depth = 1
        pos = brace_start + 1
        while depth > 0 and pos < len(html):
            if html[pos] == '{': depth += 1
            elif html[pos] == '}': depth -= 1
            pos += 1
        prefix = html[idx:brace_start+1]
        body = html[brace_start+1:pos-1]
        suffix = html[pos-1:pos+1]
        # 模拟 match 对象
        class FakeMatch:
            def group(self, n):
                return [prefix, body, suffix][n-1]
            def start(self, n):
                return [idx, brace_start+1, pos-1][n-1]
            def end(self, n):
                return [brace_start+1, pos-1, pos+1][n-1]
        m = FakeMatch()
        print(f"  📐 locales 区间: {idx}-{pos} ({pos-idx} chars)")

    body = m.group(2)

    # 找到 zh: { ... } 内层
    # 注意: JS 对象嵌套用 {}，需要用平衡匹配
    # 简化：找 'zh':{ 到匹配的 }
    zh_start = re.search(r"'zh'\s*:\s*\{", body)
    if not zh_start:
        zh_start = re.search(r"zh\s*:\s*\{", body)
    if not zh_start:
        print("  ⚠️ 未找到 zh locale")
        return html

    # 从 zh_start 开始逐字符找匹配的大括号
    depth = 0
    zh_begin = zh_start.end()
    zh_end = zh_begin
    for i in range(zh_begin, len(body)):
        if body[i] == '{':
            depth += 1
        elif body[i] == '}':
            if depth == 0:
                zh_end = i
                break
            depth -= 1

    zh_body = body[zh_begin:zh_end]

    # 构建新条目
    entries = {
        f'intel.tag{n}': tag_label,
        f'intel.date{n}': meta,
        f'intel.title{n}': title,
        f'intel.desc{n}': desc,
        f'intel.ai{n}': insight,
    }

    # 检查哪些已存在，哪些需要新增
    existing_keys = set(re.findall(r"'intel\.\w+'\s*:", zh_body))

    updates_made = False
    for key, value in entries.items():
        quoted_key = f"'{key}'"
        pattern = re.compile(rf"({re.escape(quoted_key)}\s*:\s*)'[^']*'")
        if pattern.search(zh_body):
            # 已存在，替换值
            zh_body = pattern.sub(lambda m: f"{m.group(1)}'{value}'", zh_body)
        else:
            # 新增
            if zh_body.rstrip().endswith(','):
                zh_body += f"\n    {quoted_key}:'{value}',"
            else:
                zh_body += f",\n    {quoted_key}:'{value}',"
        updates_made = True

    if not updates_made:
        print("  ⚠️ i18n 无更新")
    else:
        print(f"  ✅ i18n 数据更新: {list(entries.keys())}")

    # 重建
    new_body = body[:zh_begin] + zh_body + body[zh_end:]
    return html[:m.end(2)] + new_body + html[m.end(2):]


def build_and_push(skip_push: bool = False):
    print("\n🚀 Building...")
    r = subprocess.run(
        ["npm", "run", "build"], cwd=PROJECT_DIR,
        capture_output=True, text=True, timeout=60,
    )
    for line in r.stdout.split("\n")[-5:]:
        if line.strip():
            print(f"  {line.strip()}")
    if r.returncode != 0:
        print(f"⚠️ Build error: {r.stderr[-200:]}")
        return False
    if skip_push:
        print("⏸ --skip-push")

    print("\n📤 Pushing...")
    subprocess.run(["git", "add", "-A"], cwd=PROJECT_DIR, capture_output=True, timeout=10)
    subprocess.run(["git", "commit", "-m", f"daily article {datetime.now():%Y-%m-%d}"],
                   cwd=PROJECT_DIR, capture_output=True, text=True, timeout=10)
    r = subprocess.run(["git", "push"], cwd=PROJECT_DIR, capture_output=True, text=True, timeout=30)
    if r.returncode == 0:
        print("✅ git push ok")
        return True
    print(f"⚠️ push failed: {r.stderr[-300:]}")
    return False


def main():
    parser = argparse.ArgumentParser(description="linkx.club 文章更新 i18n版")
    parser.add_argument("--title", required=True)
    parser.add_argument("--desc", required=True)
    parser.add_argument("--tag", default="Market", choices=["Policy","Market","Visa","Investment"])
    parser.add_argument("--meta", default="")
    parser.add_argument("--insight", default="")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-push", action="store_true")
    args = parser.parse_args()

    print(f"📰 linkx.club 文章更新")
    print(f"  {args.tag} | {args.meta} | {args.title}")
    print(f"  {args.desc}")
    print(f"  🤖 {args.insight}")

    html = decode()
    print(f"📄 index.b64: {len(html)} chars")

    new_html = update(html, args.tag, args.meta, args.title, args.desc, args.insight)
    if new_html == html:
        print("❌ HTML 无变化")
        sys.exit(1)
    print(f"📝 Diff: {len(new_html) - len(html):+d} chars")

    if args.dry_run:
        print("⏸ Dry-run - no write")
        return

    encode(new_html)
    print("✅ index.b64 written")
    build_and_push(skip_push=args.skip_push)
    print("✅ Done")


if __name__ == "__main__":
    main()
