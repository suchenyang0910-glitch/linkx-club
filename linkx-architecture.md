# linkx.club 二级页面架构设计文档

> 版本：v2.0 / 2026-06-16  
> 定位：SEA Compass — 东南亚华人决策操作系统  
> 路由方案：Hash-based SPA（单文件，零构建）

---

## 目录

1. [路由方案](#1-路由方案)
2. [页面总览](#2-页面总览)
3. [一级页面导航交互](#3-一级页面导航交互)
4. [Radar 情报频道](#4-radar-情报频道)
5. [YiYao Bot 产品页](#5-yiyao-bot-产品页)
6. [Compass Pro 页](#6-compass-pro-页)
7. [情报存档](#7-情报存档)

---

## 1. 路由方案

### 1.1 Hash-based SPA

采用 hash 路由（`#radar`），所有页面在单文件中通过 JS 控制显隐。无需构建，保持零依赖。

```
/               → 首页（默认）
/#radar         → 📡 Radar 情报频道
/#bot           → 🤖 YiYao Bot 产品页
/#pro           → 💎 Compass Pro
/#archive       → 📰 情报存档
```

### 1.2 路由实现逻辑

```javascript
window.addEventListener('hashchange', routePage)
window.addEventListener('DOMContentLoaded', routePage)

function routePage() {
  const hash = location.hash.slice(1) || 'home'
  // 隐藏所有页面，显示匹配页面
  document.querySelectorAll('.page').forEach(p => p.style.display = 'none')
  const target = document.getElementById('page-' + hash)
  if (target) target.style.display = 'block'
  // 滚动到顶部
  window.scrollTo(0, 0)
}
```

### 1.3 页面容器结构

```html
<body>
  <!-- Header (所有页面共享) -->
  <header class="header">...</header>
  <div class="ambient-grid"></div>

  <!-- 首页 -->
  <main id="page-home" class="page">...</main>

  <!-- Radar -->
  <main id="page-radar" class="page" style="display:none">
    <div class="back-nav">← 返回首页</div>
    ...内容...
  </main>

  <!-- Bot -->
  <main id="page-bot" class="page" style="display:none">...</main>

  <!-- Pro -->
  <main id="page-pro" class="page" style="display:none">...</main>

  <!-- Archive -->
  <main id="page-archive" class="page" style="display:none">...</main>

  <!-- Footer (所有页面共享) -->
  <footer>...</footer>
</body>
```

---

## 2. 页面总览

| 路由 | 页面名 | 核心内容 | 导航标题 (CN) | 导航标题 (EN) |
|---|---|---|---|---|
| `/` | 首页 | Hero + 痛点 + 价值流 + 能力 + 知识库 + 产品 + 工作流 + 用户 + 理念 + 情报 + CTA | — | — |
| `/#radar` | 情报频道 | 今日情报列表、分类筛选、多标签页 | 📡 情报 | 📡 Radar |
| `/#bot` | YiYao Bot | 三步决策详解、交互 mockup、使用场景 | 🤖 YiYao Bot | 🤖 YiYao Bot |
| `/#pro` | Compass Pro | 功能对比、定价卡片、FAQ | 💎 Pro | 💎 Pro |
| `/#archive` | 情报存档 | 历史情报、国家/分类/日期筛选、搜索 | 📰 存档 | 📰 Archive |

---

## 3. 一级页面导航交互

### 3.1 导航栏链接映射

```html
<nav class="nav">
  <a href="#radar" data-i18n="nav.radar">📡 情报</a>
  <a href="#bot" data-i18n="nav.bot">🤖 YiYao Bot</a>
  <a href="#archive" data-i18n="nav.archive">📰 存档</a>
  <a href="#pro" data-i18n="nav.pro">💎 Pro</a>
</nav>
```

### 3.2 按键交互矩阵

| 元素 | 交互 | 目标 | 备注 |
|---|---|---|---|
| 导航栏链接 | `href="#radar"` | 切换页面 | hash 路由 |
| Logo / 品牌名 | `href="/"` 或 `onclick="navigate('home')"` | 返回首页 | 任何页面点击回到首页 |
| "返回首页"链接 | `onclick="navigate('home')"` | 返回首页 | 每个二级页面顶部 |
| CTA 按钮（📡 查看市场观察） | `href="#radar"` | 跳转到情报页 | |
| CTA 按钮（🧭 启动决策沙盘） | `href="#bot"` | 跳转到 Bot 页 | |
| 情报卡片"阅读全文" | `href="#archive"` | 跳转到存档页 | 点击查看更多 |
| 💎 Pro CTA 按钮 | `href="#pro"` | 跳转到 Pro 页 | |
| 知识库 "查看 XXX" | `href="#bot"` | 跳转到 Bot 页 | |
| 🌐 EN / 中文 | `onclick="toggleLanguage()"` | 切换语言 | 不触发路由 |

### 3.3 页面切换行为

```
切换页面：
1. 当前页面淡出（opacity 0, transform translateY(-10px)）
2. 0.3s 后目标页面淡入（opacity 1, translateY(0)）
3. window.scrollTo(0, 0)
4. 更新导航栏高亮状态（.nav a.active）
5. 关闭移动端菜单
```

### 3.4 导航高亮

```css
.nav a.active { color: var(--text); }
.nav a.active::after { content: ''; display: block; ... }
```

---

## 4. Radar 情报频道

### 4.1 页面信息

| 字段 | 值 |
|---|---|
| 路由 | `#radar` |
| 页面 ID | `page-radar` |
| i18n 前缀 | `radar.` |
| 核心目的 | 展示每日情报流，让用户订阅前先看到内容质量 |

### 4.2 页面区块

```
BackNav (← 返回首页)

Hero 精简头
├── 标题：SEA Compass Radar
├── 副标题：每日情报推送 · AI 导航解读 · 市场观察
├── CTA：📡 订阅频道

Tab 切换条
├── 🕐 今日 (active)
├── 🗓️ 本周
├── 📂 按分类
└── 🌏 按国家

今日情报流（列表）
├── 情报卡片 × N (无限滚动或分页)
│   ├── Meta行: tag + 国家 + 时间
│   ├── 标题 + 摘要
│   ├── AI 洞察区域
│   └── 展开/收起 (点击展开全文)

分类浏览 Tab
├── 分类标签云 (政策/市场/签证/投资/教育/安全)
├── 点击标签 → 过滤列表

国家浏览 Tab
├── 国家网格 (11个东盟国家)
├── 点击国家 → 显示该国近期情报

CTA 底部
├── 📡 订阅 Radar 频道
└── 💎 升级 Pro
```

### 4.3 情报卡片组件

```
┌─────────────────────────────────────────┐
│ [政策/Policy]                    2026-06-16 · Vietnam │
│                                         │
│ 越南放宽数字游民签证条件                    │
│ 针对IT和创意产业从业者，胡志明市出台试行政策... │
│                                         │
│ ┌─ AI 洞察 ──────────────────────────┐ │
│ │ 利好出海服务商及办公地产，短期内将吸引... │ │
│ └─────────────────────────────────────┘ │
│                     [阅读全文 →]         │
└─────────────────────────────────────────┘
```

---

## 5. YiYao Bot 产品页

### 5.1 页面信息

| 字段 | 值 |
|---|---|
| 路由 | `#bot` |
| 页面 ID | `page-bot` |
| i18n 前缀 | `bot.` |
| 核心目的 | 用完整案例展示 Bot 的三步决策能力，说服用户试用 |

### 5.2 页面区块

```
BackNav (← 返回首页)

Hero 头
├── 标题：YiYao Bot — 你的 AI 决策参谋
├── 副标题：输入问题 → 三步推演 → 输出方案
├── CTA：🧭 立即体验

三步详解（展开版本）
├── Step 1: 决策推演
│   ├── 图标 + 标题
│   ├── 详细描述
│   ├── 示例：路径 A vs 路径 B vs 路径 C
│   └── 成功率可视化（柱状/标签）
│
├── Step 2: 市场判断
│   ├── 图标 + 标题
│   ├── 详细描述
│   ├── 市场阶段指示器（早期/增长/饱和/衰退）
│   └── 示例数据对比
│
├── Step 3: 风险分析
│   ├── 图标 + 标题
│   ├── 详细描述
│   ├── 风险矩阵（低/中/高）
│   └── 应对策略清单

完整对话案例（首页例题的加长版）
├── 用户提问
├── Bot 回复（完整版本，含更多路径/RAG 引用）
└── 

技术背书
├── 基于 SEA Compass 知识库（~130 文件）
├── RAG 实时检索情报网络
└── 5 种语言支持

CTA
├── 🧭 启动决策沙盘
└── 📡 订阅情报频道
```

### 5.3 市场阶段指示器

```
早期 ─────●───── 增长 ────── 饱和 ──── 衰退
         ↑ 当前
```

---

## 6. Compass Pro 页

### 6.1 页面信息

| 字段 | 值 |
|---|---|
| 路由 | `#pro` |
| 页面 ID | `page-pro` |
| i18n 前缀 | `pro.` |
| 核心目的 | 展示 Pro 版价值，推动转化 |

### 6.2 页面区块

```
BackNav (← 返回首页)

Hero 头
├── 标题：Compass Pro — 面向严肃决策者
├── 副标题：深度推演 · 策略报告 · 专属清单
├── 价格标识：Coming Soon / 预约

功能对比区
├── 对比表格 (Free vs Pro)
│   ├── 每日情报          ✅  ✅
│   ├── AI 决策推演       基础  深度
│   ├── 历史记录          ❌   ✅
│   ├── 周度策略报告       ❌   ✅
│   ├── 专属观察清单       ❌   ✅
│   ├── 市场阶段分析       ❌   ✅
│   └── 优先级支持        ❌   ✅

Pro 专属功能详解（卡片）
├── 🧠 深度推演 — 多轮对话，历史回溯
├── 📊 周度策略报告 — AI 自动生成
├── 📋 专属观察清单 — 自定义监测
└── 🔔 变化预警 — 第一时间通知

FAQ
├── Pro 什么时候上线？
├── 价格是多少？
├── 有年付折扣吗？
└── 怎么从免费版升级？

CTA
├── 💎 预约 Pro 权限（表单 / 邮件订阅）
└── 📡 先从免费频道开始
```

### 6.3 对比表格（移动端适配）

```
桌面：2 列表格（左功能名 + 右勾叉）
移动端：堆叠卡片，每行 功能名 | Free | Pro
```

---

## 7. 情报存档

### 7.1 页面信息

| 字段 | 值 |
|---|---|
| 路由 | `#archive` |
| 页面 ID | `page-archive` |
| i18n 前缀 | `archive.` |
| 核心目的 | 完整的情报库，按条件筛选浏览 |

### 7.2 页面区块

```
BackNav (← 返回首页)

页面头
├── 标题：情报存档
├── 副标题：浏览历史市场观察，AI 分析解读
├── 统计：共 N 条情报 · M 个国家 · K 个分类

筛选栏（固定/浮动）
├── 搜索框 (关键词搜索标题/内容)
├── 分类筛选 (Policy / Market / Visa / Investment / All)
├── 国家筛选 (11 国下拉或标签)
├── 时间范围 (最近 7 天 / 30 天 / 90 天 / 全部)
└── 排序 (最新 / 最热)

结果列表
├── 情报卡片 × N
│   ├── Meta: tag + 国家 + 日期
│   ├── 标题 + 摘要全文
│   ├── AI 洞察
│   └── 分享/收藏按钮 (未来功能)

分页 / 加载更多
├── 加载更多按钮
└── 已显示 X / 共 Y 条
```

### 7.3 筛选状态管理

```javascript
const filters = {
  search: '',
  category: 'all',
  country: 'all',
  timeframe: 'all',
  sort: 'newest'
}

function applyFilters() { /* 过滤渲染 */ }
```

---

> **设计决策**：所有二级页面共享 Header 和 Footer，通过 SPA hash 路由切换主内容区。每个页面独立维护自己的 i18n 文案（`radar.*`, `bot.*`, `pro.*`, `archive.*`）。移动端适配保持与首页一致，使用同一套断点。
