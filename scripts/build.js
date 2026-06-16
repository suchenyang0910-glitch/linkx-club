const fs = require('fs');
const path = require('path');

const BASE = __dirname + '/..';
const DIST = path.join(BASE, 'dist');

// Clean + create dist
fs.rmSync(DIST, { recursive: true, force: true });
fs.mkdirSync(DIST, { recursive: true });

// Copy source files
for (const f of fs.readdirSync(BASE)) {
  if (f.endsWith('.html') || f.endsWith('.txt') || f.endsWith('.xml') || f === '_worker.js') {
    fs.copyFileSync(path.join(BASE, f), path.join(DIST, f));
    console.log('  ' + f);
  }
}

// Copy asset dirs
for (const d of ['assets', 'public', 'images']) {
  const src = path.join(BASE, d);
  if (fs.existsSync(src)) {
    fs.cpSync(src, path.join(DIST, d), { recursive: true });
    console.log(`  ${d}/`);
  }
}

// _redirects
fs.writeFileSync(path.join(DIST, '_redirects'),
  '/radar /radar.html 301\n' +
  '/bot /bot.html 301\n' +
  '/archive /archive.html 301\n' +
  '/pro /pro.html 301\n');

// _headers
fs.writeFileSync(path.join(DIST, '_headers'),
  '/*\n  X-Robots-Tag: index, follow\n  X-Frame-Options: DENY\n');

// sitemap
let sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';
for (const p of ['', 'radar.html', 'bot.html', 'archive.html', 'pro.html']) {
  sm += `  <url><loc>https://linkx.club/${p}</loc></url>\n`;
}
sm += '</urlset>\n';
fs.writeFileSync(path.join(DIST, 'sitemap.xml'), sm);

// llms.txt
fs.writeFileSync(path.join(DIST, 'llms.txt'),
  '# SEA Compass\n> ASEAN intelligence & AI decision system\n\n## Pages\n' +
  '- [Home](https://linkx.club/)\n' +
  '- [Radar](https://linkx.club/radar.html)\n' +
  '- [YiYao Bot](https://linkx.club/bot.html)\n' +
  '- [Archive](https://linkx.club/archive.html)\n' +
  '- [Pro](https://linkx.club/pro.html)\n');

console.log(`\nDone: ${fs.readdirSync(DIST).length} files in dist/`);
