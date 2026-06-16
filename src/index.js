export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // Only handle root and known paths
    if (url.pathname === '/' || url.pathname === '/index.html') {
      const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SEA Compass · 东南亚华人决策操作系统 — 东盟市场情报与AI决策推演</title>
<meta name="description" content="每天追踪东盟11国市场变化，结合AI分析与决策推演。帮你判断：去哪里发展、做什么生意、进入哪个市场、什么时候行动。">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><text y='28' font-size='28'>🧭</text></svg>">
<style>
:root {
  --bg: #060a0c;
  --card: rgba(12, 20, 23, 0.6);
  --card-hover: rgba(19, 30, 35, 0.8);
  --border: rgba(212, 175, 55, 0.1);
  --border-hover: rgba(212, 175, 55, 0.25);
  --text: #e8e8ed;
  --text-secondary: #b0a8a0;
  --dim: #7c776b;
  --emerald: #059669;
  --gold: #D4AF37;
  --gold-light: #F3E5AB;
  --rose: #F43F5E;
  --section-gap: clamp(96px, 10vw, 140px);
}
* { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { font-family: 'Inter', 'Noto Serif SC', -apple-system, sans-serif; background: var(--bg); color: var(--text); line-height: 1.7; -webkit-font-smoothing: antialiased; overflow-x: hidden; }
.container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }

/* Hero */
.hero { min-height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; position: relative; padding: 40px 24px; }
.hero-bg { position: absolute; inset: 0; background: radial-gradient(ellipse 80% 50% at 50% 40%, rgba(212,175,55,0.06) 0%, transparent 70%); pointer-events: none; }
.hero-label { font-size: 0.75rem; letter-spacing: 0.3em; text-transform: uppercase; color: var(--gold); margin-bottom: 24px; font-weight: 500; }
.hero h1 { font-family: 'Playfair Display', 'Noto Serif SC', serif; font-size: clamp(2.5rem, 7vw, 5rem); font-weight: 700; line-height: 1.15; margin-bottom: 20px; }
.hero h1 .gold { color: var(--gold); }
.hero h1 .sub { display: block; font-size: 0.4em; font-weight: 400; color: var(--text-secondary); margin-top: 8px; letter-spacing: 0.2em; }
.hero p { font-size: clamp(1rem, 2vw, 1.2rem); color: var(--text-secondary); max-width: 600px; margin-bottom: 36px; }
.hero-actions { display: flex; gap: 16px; flex-wrap: wrap; justify-content: center; }
.btn { display: inline-flex; align-items: center; gap: 8px; padding: 14px 32px; border-radius: 8px; font-weight: 500; font-size: 1rem; text-decoration: none; transition: all 0.25s; cursor: pointer; }
.btn-primary { background: var(--gold); color: #060a0c; border: none; }
.btn-primary:hover { background: #e6c048; transform: translateY(-2px); box-shadow: 0 8px 32px rgba(212,175,55,0.25); }
.btn-secondary { background: transparent; color: var(--text); border: 1px solid var(--border); }
.btn-secondary:hover { border-color: var(--gold); color: var(--gold); }
.hero-scroll { position: absolute; bottom: 40px; left: 50%; transform: translateX(-50%); color: var(--dim); font-size: 0.75rem; letter-spacing: 0.15em; animation: bounce 2s infinite; }
@keyframes bounce { 0%,100% { transform: translateX(-50%) translateY(0); } 50% { transform: translateX(-50%) translateY(8px); } }

/* Sections */
section { padding: var(--section-gap) 0; }
.section-label { font-size: 0.7rem; letter-spacing: 0.3em; text-transform: uppercase; color: var(--gold); margin-bottom: 12px; font-weight: 500; }
h2 { font-family: 'Playfair Display', 'Noto Serif SC', serif; font-size: clamp(1.8rem, 4vw, 2.8rem); font-weight: 700; margin-bottom: 16px; line-height: 1.25; }
.section-sub { color: var(--text-secondary); max-width: 600px; margin-bottom: 48px; font-size: 1rem; }

/* Pain grid */
.pain-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; }
.pain-card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 28px; transition: all 0.3s; }
.pain-card:hover { background: var(--card-hover); border-color: var(--border-hover); transform: translateY(-3px); }
.pain-icon { font-size: 2rem; margin-bottom: 12px; }
.pain-card h3 { font-size: 1rem; font-weight: 600; margin-bottom: 8px; }
.pain-card p { font-size: 0.875rem; color: var(--text-secondary); line-height: 1.6; }

/* Capabilities grid */
.cap-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
.cap-card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 32px; transition: all 0.3s; }
.cap-card:hover { background: var(--card-hover); border-color: var(--border-hover); transform: translateY(-3px); }
.cap-icon { font-size: 2.2rem; margin-bottom: 16px; }
.cap-card h3 { font-size: 1.15rem; font-weight: 600; margin-bottom: 8px; }
.cap-card p { font-size: 0.875rem; color: var(--text-secondary); margin-bottom: 16px; line-height: 1.6; }
.cap-tags { display: flex; flex-wrap: wrap; gap: 6px; }
.cap-tag { font-size: 0.7rem; padding: 4px 10px; border-radius: 999px; background: rgba(212,175,55,0.1); color: var(--gold); border: 1px solid rgba(212,175,55,0.15); }

/* Footer */
footer { border-top: 1px solid var(--border); padding: 40px 24px; text-align: center; }
footer p { color: var(--dim); font-size: 0.8rem; }
footer a { color: var(--gold); text-decoration: none; }

/* Responsive */
@media (max-width: 768px) {
  .hero h1 { font-size: clamp(2rem, 10vw, 3rem); }
  .pain-grid, .cap-grid { grid-template-columns: 1fr; }
  .hero-actions { flex-direction: column; align-items: center; }
  .btn { width: 100%; justify-content: center; }
}
</style>
</head>
<body>
<main>
  <section class="hero">
    <div class="hero-bg"></div>
    <div class="hero-label">╱ 东南亚华人决策操作系统</div>
    <h1>
      <span class="gold">SEA Compass</span>
      <span class="sub">知道你该去哪里</span>
    </h1>
    <p>每天追踪东盟11国市场变化，AI分析+决策推演。<br>从海量噪音中找到方向。</p>
    <div class="hero-actions">
      <a href="https://t.me/CompassSEA" class="btn btn-primary" target="_blank" rel="noopener">📡 订阅情报频道</a>
      <a href="https://t.me/YiYaoBot_bot" class="btn btn-secondary" target="_blank" rel="noopener">🤖 问 YiYao 决策助手</a>
    </div>
    <div class="hero-scroll">SCROLL ↓</div>
  </section>

  <section>
    <div class="container">
      <div class="section-label">╱ 你面对的</div>
      <h2>信息爆炸，决策空白</h2>
      <p class="section-sub">每天上百条新闻，几十份报告，但你真正需要的是一个判断。</p>
      <div class="pain-grid">
        <div class="pain-card">
          <div class="pain-icon">🌏</div>
          <h3>11国动态，看不过来</h3>
          <p>柬埔寨今晚出了新政策，越南明早调了关税，泰国汇率又变了——你一个人跟得上吗？</p>
        </div>
        <div class="pain-card">
          <div class="pain-icon">🧩</div>
          <h3>信息碎片，拼不出全景</h3>
          <p>每条新闻都有用，但拼在一起才能看到机会。碎片式阅读让你一直在点，看不到面。</p>
        </div>
        <div class="pain-card">
          <div class="pain-icon">⏳</div>
          <h3>看到了，但已经晚了</h3>
          <p>等你知道柬埔寨某品类火了的时候，第一批入场的人已经在数钱了。</p>
        </div>
        <div class="pain-card">
          <div class="pain-icon">🤷</div>
          <h3>该去哪？该做什么？</h3>
          <p>越南还是泰国？制造业还是电商？现在是入场时机吗？没有好的决策框架，你永远在赌。</p>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="container">
      <div class="section-label">╱ 三大能力</div>
      <h2>情报 · 推演 · 执行</h2>
      <p class="section-sub">SEA Compass 不是又一个新闻聚合器，而是你的东南亚决策副驾驶。</p>
      <div class="cap-grid">
        <div class="cap-card">
          <div class="cap-icon">📡</div>
          <h3>雷达：11国情报每天刷</h3>
          <p>28个RSS源 + AI自动分类 → 按国家/行业/紧急度推送。你只收到对你有用的信号。</p>
          <div class="cap-tags"><span class="cap-tag">11国家</span><span class="cap-tag">多语种</span><span class="cap-tag">自动路由</span></div>
        </div>
        <div class="cap-card">
          <div class="cap-icon">🧠</div>
          <h3>决策推演：问 YiYao 一秒出方案</h3>
          <p>「柬埔寨宠物食品现在入场晚不晚？」→ YiYao分析现状、推演三种路径、评估风险，给你可执行的建议。</p>
          <div class="cap-tags"><span class="cap-tag">AI决策</span><span class="cap-tag">趋势推演</span><span class="cap-tag">风险提示</span></div>
        </div>
        <div class="cap-card">
          <div class="cap-icon">🎯</div>
          <h3>时机窗口：告诉你什么时候该动</h3>
          <p>7天/30天/90天窗口分析。不是算命，是数据驱动的「最佳入场时机」判断。</p>
          <div class="cap-tags"><span class="cap-tag">入场时机</span><span class="cap-tag">趋势预判</span><span class="cap-tag">风险预警</span></div>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="container" style="text-align:center">
      <div class="section-label">╱ 产品体系</div>
      <h2>三层架构，覆盖全场景</h2>
      <div class="cap-grid" style="margin-top:40px">
        <div class="cap-card">
          <div class="cap-icon">📡</div>
          <h3>SEA Compass Radar</h3>
          <p><strong>免费 · 情报频道</strong></p>
          <p>每天推送东盟11国精选情报，覆盖政策/商业/安全/汇率，按国家分类。</p>
          <div class="cap-tags"><span class="cap-tag">免费</span><span class="cap-tag">@CompassSEA</span></div>
        </div>
        <div class="cap-card">
          <div class="cap-icon">🤖</div>
          <h3>YiYao 决策助手</h3>
          <p><strong>免费 · TG Bot</strong></p>
          <p>直接问任何东南亚商业问题，30秒内给你分析+建议。支持三国语言。</p>
          <div class="cap-tags"><span class="cap-tag">免费</span><span class="cap-tag">@YiYaoBot_bot</span></div>
        </div>
        <div class="cap-card">
          <div class="cap-icon">💎</div>
          <h3>Compass Pro</h3>
          <p><strong>即将推出 · 高级会员</strong></p>
          <p>专属决策推演、深度行业报告、个性化警报、VIP 1v1 策略咨询。</p>
          <div class="cap-tags"><span class="cap-tag">即将推出</span></div>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="container" style="text-align:center">
      <div class="section-label">╱ 适用人群</div>
      <h2>为谁而建</h2>
      <div class="pain-grid" style="margin-top:40px">
        <div class="pain-card"><div class="pain-icon">🚀</div><h3>跨境创业者</h3><p>想知道去哪里、做什么生意。不想拍脑袋决策。</p></div>
        <div class="pain-card"><div class="pain-icon">🏠</div><h3>东南亚华人家庭</h3><p>在这里安家、发展、教育、养老，需要全面的环境判断。</p></div>
        <div class="pain-card"><div class="pain-icon">💰</div><h3>投资者</h3><p>东南亚市场的早期信号，比主流媒体快3-7天。</p></div>
        <div class="pain-card"><div class="pain-icon">💻</div><h3>数字游民</h3><p>哪国人少网好机会多、签证政策变了吗、生活成本涨了多少。</p></div>
      </div>
    </div>
  </section>

  <section>
    <div class="container" style="text-align:center; max-width:700px">
      <div class="section-label">╱ 底层理念</div>
      <blockquote style="font-family:'Playfair Display','Noto Serif SC',serif;font-size:clamp(1.2rem,2.5vw,1.6rem);font-style:italic;color:var(--gold-light);line-height:1.6;margin:40px 0 24px">
        "信息不再是壁垒，<br>判断力才是。<br>我们帮你缩短从信息到决策的距离。"
      </blockquote>
      <p style="color:var(--text-secondary);font-size:0.9rem">
        — SEA Compass，来自 LinkX 集团
      </p>
    </div>
  </section>
</main>

<footer>
  <div class="container">
    <p>© 2026 <a href="https://t.me/helix_one">SEA Compass</a> · 由 LinkX 集团出品 · 在柬埔寨金边运营</p>
    <p style="margin-top:8px;font-size:0.7rem">每天发现，每天判断，每天行动。</p>
  </div>
</footer>
</body>
</html>`;

      return new Response(html, {
        headers: {
          'content-type': 'text/html; charset=utf-8',
          'cache-control': 'public, max-age=3600'
        }
      });
    }

    return new Response('Not Found', { status: 404 });
  }
};
