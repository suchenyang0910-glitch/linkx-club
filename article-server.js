const http = require('http');
const fs = require('fs');
const path = require('path');

const DATA_PATH = '/root/SettleCore/linkx-site/data/articles.json';
const SITE_DIR = '/root/SettleCore/linkx-site';
const API_KEY = process.env.ARTICLE_API_KEY || '';
const PORT = 3034;
const HOST = '0.0.0.0';

// ── DB helpers ──
function load() {
  if (!fs.existsSync(DATA_PATH)) return { articles: [], nextId: 1 };
  try { return JSON.parse(fs.readFileSync(DATA_PATH, 'utf8')); }
  catch(e) { return { articles: [], nextId: 1 }; }
}
function save(db) {
  fs.writeFileSync(DATA_PATH, JSON.stringify(db, null, 2));
}

// ── HTML template ──
function renderArticleHTML(article, host) {
  const tagColors = { vn: 'dc2626', th: '2563eb', my: 'ca8a04', sg: '7c3aed', kh: '059669' };
  const tagTextColors = { vn: 'fca5a5', th: '93c5fd', my: 'fde68a', sg: 'c4b5fd', kh: '6ee7b7' };
  const c = article.country;
  const tagBg = tagColors[c] || '334155';
  const tagTxt = tagTextColors[c] || '94a3b8';
  const countryFlag = { vn: '🇻🇳', th: '🇹🇭', my: '🇲🇾', sg: '🇸🇬', kh: '🇰🇭' }[c] || '🌏';
  const countryName = article.country_name || c.toUpperCase();
  const articleUrl = `https://${host}/article/${article.id}`;

  // Build figures into content
  let figuresHTML = '';
  if (article.figures && article.figures.length > 0) {
    article.figures.forEach(fig => {
      if (!fig.placeholder) {
        figuresHTML += `<figure class="post-figure"><img src="${fig.src}" alt="${fig.caption}" loading="lazy"><figcaption>${fig.caption}</figcaption></figure>\n`;
      }
    });
  }

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>${article.title} — linkx.club</title>
<meta name="description" content="${(article.description||'').replace(/"/g,'&quot;')}">
<meta name="keywords" content="${countryName},${article.tag||''}"/>
<link rel="stylesheet" href="/styles/global.v4.css"><link rel="icon" type="image/svg+xml" href="/favicon.svg">
<meta property="og:title" content="${article.title}"/><meta property="og:description" content="${(article.description||'').replace(/"/g,'&quot;')}"/>
<meta property="og:type" content="Article"/><meta property="og:url" content="${articleUrl}"/>
<meta property="og:image" content="https://${host}${article.cover}"/>
<meta name="twitter:card" content="summary_large_image"/>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-KHW9QC8PK3"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','G-KHW9QC8PK3');</script>
<script>function toggleSidebar(){document.getElementById('sidebar').classList.toggle('open');document.getElementById('sidebarOverlay').classList.toggle('open');}</script>
</head>
<body>
<header class="site-header"><div class="container"><a href="/" class="logo"><img src="/logo.jpg" alt="LinkX" class="logo-img"> linkx.club</a><nav class="desktop-nav"><a href="/">首页</a><a href="/">全部专题</a></nav><button class="hamburger" onclick="toggleSidebar()">☰</button></div></header>
<div class="sidebar-overlay" id="sidebarOverlay" onclick="toggleSidebar()"></div>
<div class="sidebar" id="sidebar"><a href="/">首页</a><a href="/article/59">🇰🇭 柬埔寨·运河</a><a href="/article/58">🇸🇬 新加坡·家办</a><a href="/article/57">🇲🇾 马来西亚·数据中心</a><a href="/article/56">🇹🇭 泰国·EV</a><a href="/article/55">🇻🇳 越南·供应链</a></div>
<main class="container">
<nav class="breadcrumb"><a href="/">Home</a><span>${countryName} ${article.tag||''}</span></nav>
<article>
<h1>${article.title}</h1>
<p class="meta">${article.date} · ${article.author} · <span class="tag" style="display:inline-block;font-size:.75rem;padding:2px 10px;border-radius:99px;background:#${tagBg};color:#${tagTxt};margin-bottom:0">${countryFlag} ${countryName} · ${article.tag||''}</span></p>
${article.cover ? `<figure class="post-figure"><img src="${article.cover}" alt="${article.title}" loading="lazy"><figcaption>${(article.caption||article.title)}</figcaption></figure>` : ''}
${article.content_html}
<hr/>
<p style="color:#64748b;font-size:.88rem">🌐 <strong>linkx.club</strong> — 东南亚地缘分析 · 中资出海 · 投资决策<br/>🇻🇳 越南 · 🇹🇭 泰国 · 🇲🇾 马来西亚 · 🇸🇬 新加坡 · 🇰🇭 柬埔寨<br/>每周 2-3 篇深度，帮你读懂东南亚。</p>
<div class="share-section">
<p class="share-label">📤 分享这篇文章</p>
<div class="share-buttons">
<a href="https://twitter.com/intent/tweet?text=${encodeURIComponent(article.title)}&url=${encodeURIComponent(articleUrl)}" target="_blank" class="share-btn share-twitter">𝕏</a>
<a href="https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(articleUrl)}" target="_blank" class="share-btn share-facebook">f</a>
<a href="https://t.me/share/url?url=${encodeURIComponent(articleUrl)}&text=${encodeURIComponent(article.title)}" target="_blank" class="share-btn share-telegram">✈</a>
<button onclick="navigator.clipboard.writeText('${articleUrl}').then(()=>{this.textContent='✅'})" class="share-btn share-copy">🔗</button>
</div>
</div>
<div id="comment-widget"></div>
<script src="/js/comment-widget.js"></script>
</article>
</main>
<footer class="site-footer"><div class="container"><p>&copy; 2026 linkx.club — 东南亚地缘分析 · ${article.author}</p></div></footer>
</body>
</html>`;
}

// ── Homepage template ──
function renderHomepage(articles, host) {
  const tagColors = { vn: ['#dc262622','#fca5a5'], th: ['#2563eb22','#93c5fd'], my: ['#ca8a0422','#fde68a'], sg: ['#7c3aed22','#c4b5fd'], kh: ['#05966922','#6ee7b7'] };
  const countryFlag = { vn: '🇻🇳', th: '🇹🇭', my: '🇲🇾', sg: '🇸🇬', kh: '🇰🇭' };
  const borderColors = { vn: '#dc2626', th: '#2563eb', my: '#ca8a04', sg: '#7c3aed', kh: '#059669' };

  // Sort by id DESC (newest first)
  const sorted = [...articles].filter(a => a.published !== false).sort((a,b) => b.id - a.id);
  const featured = sorted.slice(0, 2);
  const rest = sorted.slice(2);

  let countryNav = '';
  sorted.forEach(a => {
    const c = a.country;
    const bc = borderColors[c] || '#334155';
    const tc = (tagColors[c]||[,'#94a3b8'])[1];
    countryNav += `<a href="/article/${a.id}" class="country-btn" style="border-color:${bc};color:${tc}">${countryFlag[c]||'🌏'} ${a.country_name||c.toUpperCase()} — ${a.tag||''}</a>\n`;
  });

  let featuredHTML = '';
  if (featured[0]) {
    const a = featured[0];
    const c = a.country;
    const tc = (tagColors[c]||[,'#94a3b8'])[0];
    featuredHTML += `<a href="/article/${a.id}" class="card-lg" style="border-color:${borderColors[c]||'#3b82f6'};position:relative"><span class="tag" style="background:${tc};color:${(tagColors[c]||[,'#94a3b8'])[1]}">${countryFlag[c]||'🌏'} ${a.country_name||c.toUpperCase()} · ${a.tag||''}</span><h3>${a.title}</h3><p>${a.description||''}</p></a>\n`;
  }
  if (featured[1]) {
    const a = featured[1];
    const c = a.country;
    featuredHTML += `<a href="/article/${a.id}" class="card"><span class="tag" style="background:${(tagColors[c]||[,'#334155'])[0]};color:${(tagColors[c]||[,'#94a3b8'])[1]}">${countryFlag[c]||'🌏'} ${a.country_name||c.toUpperCase()} · ${a.tag||''}</span><h3>${a.title}</h3><p>${(a.description||'').slice(0,60)}...</p></a>\n`;
  }

  let restHTML = '';
  rest.forEach(a => {
    const c = a.country;
    const tc = (tagColors[c]||[,'#334155'])[0];
    restHTML += `<a href="/article/${a.id}" class="card"><span class="tag" style="background:${tc};color:${(tagColors[c]||[,'#94a3b8'])[1]}">${countryFlag[c]||'🌏'} ${a.country_name||c.toUpperCase()} · ${a.tag||''}</span><h3>${a.title}</h3><p>${(a.description||'').slice(0,70)}...</p></a>\n`;
  });

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>linkx.club — 东南亚地缘分析</title>
<meta name="description" content="东南亚地缘政治·中资出海·商业分析。越南、泰国、马来西亚、新加坡、柬埔寨。">
<link rel="stylesheet" href="/styles/global.v4.css"><link rel="icon" type="image/svg+xml" href="/favicon.svg">
<meta property="og:image" content="/images/linkx-og.png"><meta property="og:title" content="linkx.club — 东南亚地缘分析"/>
<meta property="og:description" content="东南亚地缘政治·中资出海·商业分析"/><meta property="og:type" content="website"/>
<meta name="keywords" content="东南亚,地缘政治,中资出海,越南,泰国,马来西亚,新加坡,柬埔寨"/>
<meta name="monetag" content="4ee62fb24e5ddc9d9258670c605c2d9e"/>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-KHW9QC8PK3"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','G-KHW9QC8PK3');</script>
<script>function toggleSidebar(){document.getElementById('sidebar').classList.toggle('open');document.getElementById('sidebarOverlay').classList.toggle('open');}</script>
</head>
<body>
<header class="site-header"><div class="container"><a href="/" class="logo"><img src="/logo.jpg" alt="LinkX" class="logo-img"> linkx.club</a><nav class="desktop-nav"><a href="/">首页</a><a href="/">全部专题</a></nav><button class="hamburger" onclick="toggleSidebar()">☰</button></div></header>
<div class="sidebar-overlay" id="sidebarOverlay" onclick="toggleSidebar()"></div>
<div class="sidebar" id="sidebar"><a href="/">首页</a>${sorted.slice(0,5).map(a => `<a href="/article/${a.id}">${countryFlag[a.country]||'🌏'} ${a.country_name||a.country.toUpperCase()}·${a.tag||''}</a>`).join('\n')}</div>
<section class="hero"><div class="container"><h1>linkx.club</h1><p class="tagline">东南亚地缘分析 · 中资出海 · 投资决策</p><p style="font-size:.9rem;color:#64748b">${sorted.map(a => `${countryFlag[a.country]||'🌏'} ${a.country_name||a.country.toUpperCase()}`).join(' · ')}</p></div></section>
<div class="container">
<div class="country-nav">${countryNav}</div>
<p class="section-title">🌟 最新专题</p>
<div class="featured-grid">${featuredHTML}</div>
<p class="section-title">📡 系列专题</p>
<div class="article-grid">${restHTML}</div>
</div>
<footer class="site-footer"><div class="container"><p>&copy; 2026 linkx.club — 东南亚地缘分析</p></div></footer>
</body>
</html>`;
}

// ── Migrate static HTML into DB ──
function parseArticle(filePath) {
  const html = fs.readFileSync(filePath, 'utf8');
  const title = (html.match(/<h1>([^<]+)<\/h1>/)||[])[1] || '';
  const description = (html.match(/<meta name="description" content="([^"]+)"/)||[])[1] || '';
  const date = (html.match(/(\d{4}-\d{2}-\d{2})/)||[])[1] || '';
  const tagMatch = html.match(/<span[^>]*>([\u{1F1E6}-\u{1F1FF}🇻🇳🇹🇭🇲🇾🇸🇬🇰🇭]+)\s*([^<·]+) · ([^<]+)<\/span>/u) ||
                  html.match(/🇻🇳|🇹🇭|🇲🇾|🇸🇬|🇰🇭/);
  const figMatches = [...html.matchAll(/<figure class="post-figure"><img src="([^"]+)"[^>]*><figcaption>([^<]+)<\/figcaption><\/figure>/g)];
  
  // Determine country
  let country = '', countryName = '';
  if (html.includes('🇻🇳')) { country = 'vn'; countryName = '越南'; }
  else if (html.includes('🇹🇭')) { country = 'th'; countryName = '泰国'; }
  else if (html.includes('🇲🇾')) { country = 'my'; countryName = '马来西亚'; }
  else if (html.includes('🇸🇬')) { country = 'sg'; countryName = '新加坡'; }
  else if (html.includes('🇰🇭')) { country = 'kh'; countryName = '柬埔寨'; }
  
  // Get tag from sidebar
  const tagMatch2 = html.match(/·\s*([^<]+)<\/span>/) || ['',''];
  const tag = (tagMatch2[1]||'').trim() || '';

  // Cover image
  const coverMatch = html.match(/<figure class="post-figure"><img src="([^"]+)"[^>]*><figcaption>([^<]+)<\/figcaption><\/figure>/);
  const cover = coverMatch ? coverMatch[1] : '';
  const caption = coverMatch ? coverMatch[2] : '';

  // Content HTML (everything between first <p> after h1 and before <hr/>)
  const bodyStart = html.indexOf('<p>', html.indexOf('<h1>'));
  const bodyEnd = html.indexOf('<hr/>', bodyStart);
  let content_html = bodyStart > 0 && bodyEnd > 0 ? html.slice(bodyStart, bodyEnd).trim() : '';

  // Figures list
  const figures = figMatches.map(m => ({ src: m[1], caption: m[2] }));
  
  return { title, description, date, country, countryName, tag: tag.replace(/·\s*/,''), cover, caption, content_html, figures };
}

// ── Server ──
const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const pathname = url.pathname;
  const method = req.method;

  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (method === 'OPTIONS') { res.writeHead(204); res.end(); return; }

  // ── API: list articles ──
  if (pathname === '/api/articles' && method === 'GET') {
    const db = load();
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(db.articles.filter(a => a.published !== false).map(a => ({
      id: a.id, title: a.title, description: a.description, country: a.country,
      country_name: a.countryName, tag: a.tag, date: a.date, cover: a.cover
    }))));
    return;
  }

  // ── API: get single article ──
  const articleMatch = pathname.match(/^\/api\/article\/(\d+)$/);
  if (articleMatch && method === 'GET') {
    const db = load();
    const article = db.articles.find(a => a.id === parseInt(articleMatch[1]));
    if (!article) { res.writeHead(404); res.end('{"error":"not found"}'); return; }
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(article));
    return;
  }

  // ── API: create article ──
  if (pathname === '/api/article' && method === 'POST') {
    const auth = req.headers['authorization'] || '';
    if (auth !== `Bearer ${API_KEY}`) { res.writeHead(401); res.end('{"error":"unauthorized"}'); return; }
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const data = JSON.parse(body);
        const db = load();
        const id = db.nextId++;
        const article = { id, ...data, published: true, date: data.date || new Date().toISOString().slice(0,10), created_at: new Date().toISOString() };
        db.articles.push(article);
        save(db);
        res.writeHead(201, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ id }));
      } catch(e) { res.writeHead(400); res.end(JSON.stringify({ error: e.message })); }
    });
    return;
  }

  // ── API: migrate from static files ──
  if (pathname === '/api/migrate' && method === 'POST') {
    const auth = req.headers['authorization'] || '';
    if (auth !== `Bearer ${API_KEY}`) { res.writeHead(401); res.end('{"error":"unauthorized"}'); return; }
    
    const postsDir = path.join(SITE_DIR, 'l1', 'posts');
    const db = load();
    let migrated = 0;

    if (fs.existsSync(postsDir)) {
      const dirs = fs.readdirSync(postsDir).filter(d => /^\d+$/.test(d)).sort((a,b) => parseInt(a)-parseInt(b));
      dirs.forEach(dir => {
        const filePath = path.join(postsDir, dir, 'index.html');
        if (fs.existsSync(filePath) && !filePath.endsWith('.bak')) {
          const article = parseArticle(filePath);
          if (article.title && !db.articles.find(a => a.id === parseInt(dir))) {
            db.articles.push({
              id: parseInt(dir),
              ...article,
              published: true,
              created_at: new Date().toISOString()
            });
            migrated++;
          }
        }
      });
    }
    db.nextId = Math.max(...db.articles.map(a => a.id), 0) + 1;
    save(db);
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ migrated, total: db.articles.length }));
    return;
  }

  // ── Render: homepage ──
  if (pathname === '/' || pathname === '/home') {
    const db = load();
    const host = req.headers.host || 'linkx.club';
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(renderHomepage(db.articles, host));
    return;
  }

  // ── Render: article page ──
  const renderMatch = pathname.match(/^\/article\/(\d+)$/);
  if (renderMatch) {
    const db = load();
    const article = db.articles.find(a => a.id === parseInt(renderMatch[1]));
    if (!article) { res.writeHead(404); res.end('Not Found'); return; }
    const host = req.headers.host || 'linkx.club';
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(renderArticleHTML(article, host));
    return;
  }

  // ── Health ──
  if (pathname === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'ok', articles: load().articles.length }));
    return;
  }

  res.writeHead(404); res.end('Not Found');
});

server.listen(PORT, HOST, () => {
  console.log(`Article API running on ${HOST}:${PORT}`);
  const db = load();
  console.log(`  Articles in DB: ${db.articles.length}`);
});
