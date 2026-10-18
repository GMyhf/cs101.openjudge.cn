'use strict';
// 日期按服务端提供的本站日期计算，避免浏览器时区改变筛选边界。
function recentStart(today, range) {
  const date = new Date(today + 'T00:00:00Z');
  if (range === 'all') return '';
  if (range === '3m') {
    const day = date.getUTCDate();
    date.setUTCDate(1);
    date.setUTCMonth(date.getUTCMonth() - 3);
    const last = new Date(Date.UTC(date.getUTCFullYear(), date.getUTCMonth() + 1, 0)).getUTCDate();
    date.setUTCDate(Math.min(day, last));
  } else {
    date.setUTCDate(date.getUTCDate() - (Number(range) - 1));
  }
  return date.toISOString().slice(0, 10);
}

const hiddenHomeBooks = new Set(['2024fallroutine', '2025sp_routine']);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const buttons = [...document.querySelectorAll('[data-range]')];
let range = new URLSearchParams(location.search).get('range') || '30';
if (!buttons.some(button => button.dataset.range === range)) range = '30';
let problems = [], today = '', loaded = false;
const list = document.querySelector('#list'), count = document.querySelector('#count'), empty = document.querySelector('#empty');

function render() {
  buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.range === range)));
  if (!loaded) return;
  const start = recentStart(today, range);
  const rows = problems.filter(p => range === 'all' || (p.added_at && p.added_at >= start && p.added_at <= today));
  count.textContent = (start ? `${start} 至 ${today} · ` : '') + `共 ${rows.length} 道题目`;
  list.innerHTML = rows.map(p => {
    const title = (p.title || '').replace(new RegExp('^' + p.id + '\\s*[:：]\\s*', 'i'), '') || p.id;
    return `<a class="problem" href="${esc(p.path)}"><span class="pid">${esc(p.id)}</span><span class="problem-main"><span class="problem-title">${esc(title)}</span></span><time class="added"${p.added_at ? ` datetime="${esc(p.added_at)}"` : ''}>${esc(p.added_at || '日期未记录')}</time><span class="arrow" aria-hidden="true">›</span></a>`;
  }).join('');
  list.hidden = !rows.length;
  empty.hidden = !!rows.length;
}

buttons.forEach(button => button.addEventListener('click', () => {
  range = button.dataset.range;
  const url = new URL(location.href);
  url.searchParams.set('range', range);
  history.replaceState(null, '', url);
  render();
}));
render();
fetch('/api/catalog?summary=1').then(response => {
  if (!response.ok) throw new Error('Catalog unavailable');
  return response.json();
}).then(data => {
  today = data.today;
  problems = (data.problems || []).filter(p => !hiddenHomeBooks.has(p.book));
  problems.sort((a, b) => (a.added_at || '').localeCompare(b.added_at || ''));
  problems.reverse();
  loaded = true;
  render();
}).catch(() => { count.textContent = '题库暂时不可用，请稍后重试。'; });
