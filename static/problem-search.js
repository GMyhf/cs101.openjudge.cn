'use strict';
// 首页与题库目录共用的检索逻辑：题号/标题/考点在本地匹配，题面正文走 /api/search。
// 考点来自 data/openjudge/topics.json（scripts/tag_topics.py 按参考代码与题面自动初标）。
const problemSearch = {
  key(p) { return p.book + '/' + p.id; },

  // 空格分隔的每个词都要命中（题号、标题、考点名或题面正文之一），与服务端同一口径。
  matches(p, query, contentHits) {
    const terms = query.trim().toLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length) return true;
    if (contentHits && contentHits.has(this.key(p))) return true;
    const hay = [p.id, p.title || '', ...(p.topics || [])].join(' ').toLowerCase();
    return terms.every(t => hay.includes(t));
  },

  hasTopic(p, topic) { return !topic || (p.topics || []).includes(topic); },

  // 考点按出现次数从多到少；只列当前可见题目里真有的考点。
  topicCounts(problems) {
    const counts = new Map();
    for (const p of problems) for (const t of p.topics || []) counts.set(t, (counts.get(t) || 0) + 1);
    return [...counts].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], 'zh'));
  },

  // 题面全文检索：输入停顿 250ms 再请求，只用最后一次请求的结果（防止慢请求覆盖新结果）。
  _timer: null, _seq: 0,
  fetchContent(query, done) {
    clearTimeout(this._timer);
    const q = query.trim();
    const seq = ++this._seq;
    if (!q) { done(new Map()); return; }
    this._timer = setTimeout(() => {
      fetch('/api/search?q=' + encodeURIComponent(q), { credentials: 'same-origin' })
        .then(r => r.json())
        .then(data => {
          if (seq !== this._seq) return;
          done(new Map((data.matches || []).map(m => [m.book + '/' + m.id, m.snippet || ''])));
        })
        .catch(() => { if (seq === this._seq) done(new Map()); });
    }, 250);
  },
};
