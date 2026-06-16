const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8780;
const HTML_PATH = path.join(__dirname, 'index.html');

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  
  if (url.pathname === '/' || url.pathname === '/index.html') {
    fs.readFile(HTML_PATH, 'utf-8', (err, data) => {
      if (err) {
        res.writeHead(500);
        res.end('Server Error');
        return;
      }
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(data);
    });
  } else {
    res.writeHead(404);
    res.end('Not Found');
  }
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`SEA Compass server running on http://0.0.0.0:${PORT}`);
});
