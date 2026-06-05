(function() {
  const articleId = window.location.pathname;
  const container = document.getElementById('comment-widget');
  if (!container) return;

  const apiBase = 'https://linkx.club/api/comment';

  function escape(s) {
    const d = document.createElement('div');
    d.textContent = s;
    return d.innerHTML;
  }

  function formatTime(ts) {
    const d = new Date(ts);
    return d.toLocaleDateString('zh-CN') + ' ' + d.toLocaleTimeString('zh-CN', {hour:'2-digit',minute:'2-digit'});
  }

  function loadComments() {
    fetch(apiBase + '?article_id=' + encodeURIComponent(articleId))
      .then(r => r.json())
      .then(data => {
        const list = container.querySelector('.comment-list');
        if (!data.comments || data.comments.length === 0) {
          list.innerHTML = '<p style="color:#64748b;font-size:.85rem">暂无评论，来写第一条吧</p>';
        } else {
          list.innerHTML = data.comments.map(c =>
            `<div class="comment-item">
              <div class="comment-meta">${escape(c.display_name || c.author || '匿名用户')} · ${formatTime(c.timestamp)}</div>
              <div class="comment-body">${escape(c.content)}</div>
            </div>`
          ).join('');
        }
      }).catch(() => {});
  }

  container.innerHTML = `
    <div class="comment-section">
      <h2>💬 评论</h2>
      <div class="comment-form">
        <input type="text" id="comment-input" placeholder="写下你的想法…" maxlength="500">
        <button id="comment-submit">发送</button>
      </div>
      <div class="comment-list"></div>
    </div>
  `;

  document.getElementById('comment-submit').addEventListener('click', () => {
    const input = document.getElementById('comment-input');
    const content = input.value.trim();
    if (!content || content.length < 2) return;

    const btn = document.getElementById('comment-submit');
    btn.disabled = true;
    btn.textContent = '发送中…';

    fetch(apiBase, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        article_id: articleId,
        content: content
      })
    }).then(r => {
      if (r.ok) {
        input.value = '';
        loadComments();
      } else {
        alert('发送失败，请重试');
      }
    }).catch(() => {
      alert('网络错误');
    }).finally(() => {
      btn.disabled = false;
      btn.textContent = '发送';
    });
  });

  loadComments();
})();
