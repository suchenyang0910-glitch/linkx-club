// CF Pages Worker - serve static assets from git (no VPS dependency)
// Content updated via daily cron → git push → CF Pages auto-deploy
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // Try to serve from CF Pages static assets
    try {
      const response = await env.ASSETS.fetch(request);
      if (response.status !== 404) {
        const headers = new Headers(response.headers);
        headers.set('X-Robots-Tag', 'index, follow');
        return new Response(response.body, { status: response.status, headers });
      }
    } catch {}
    
    // Fallback: serve index.html for all routes (SPA-friendly)
    try {
      const indexResponse = await env.ASSETS.fetch(new Request(new URL('/index.html', url)));
      const headers = new Headers(indexResponse.headers);
      headers.set('X-Robots-Tag', 'index, follow');
      return new Response(indexResponse.body, { status: 200, headers });
    } catch {}
    
    return new Response('Not Found', { status: 404 });
  }
}
