// CF Pages Worker - proxy all requests to VPS origin server
// This bypasses stale CF Pages builds and ensures fresh content
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname + url.search;
    
    // Direct proxy to VPS
    const originUrl = 'http://143.198.192.193' + path;
    
    const modifiedRequest = new Request(originUrl, {
      method: request.method,
      headers: request.headers,
      body: ['GET', 'HEAD'].includes(request.method) ? null : await request.clone().arrayBuffer(),
    });
    
    modifiedRequest.headers.set('Host', 'linkx.club');
    
    const response = await fetch(modifiedRequest);
    
    // Create response with proper headers
    const newHeaders = new Headers(response.headers);
    newHeaders.set('X-Robots-Tag', 'index, follow');
    
    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers: newHeaders,
    });
  }
}
