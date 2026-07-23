const state = { problems: [] };
const $ = (s) => document.querySelector(s);
async function get(url) { const r = await fetch(url); return r.json(); }
function renderProblems() { $('#problem-list').innerHTML = state.problems.slice(0, 4).map(p => `<div class="problem"><span class="problem-id">${p.id}</span><div class="problem-title">${p.title}<small>${p.chapter} · 通过率 ${p.rate}%</small></div><span class="difficulty">${p.difficulty}</span></div>`).join(''); }
async function load() { const data = await get('/api/course'); state.problems = data.problems; $('#notice').textContent = data.course.notice; renderProblems(); const me = await get('/api/me'); updateUser(me); }
function updateUser(me) { $('#side-user').textContent = me.authenticated ? me.user : '访客'; $('#side-role').textContent = me.authenticated ? '课程管理员' : '未登录'; $('#login-open').textContent = me.authenticated ? '管理工作台 ↗' : '管理员登录 ↗'; }
function showModal(open) { $('#modal').classList.toggle('hidden', !open); if (open) $('#login-form input').focus(); }
$('#login-open').onclick = () => showModal(true); $('#modal-close').onclick = () => showModal(false);
$('#modal').onclick = e => { if (e.target.id === 'modal') showModal(false); };
$('#logout').onclick = async () => { await fetch('/api/logout', { method: 'POST' }); updateUser({ authenticated: false }); };
$('#login-form').onsubmit = async e => { e.preventDefault(); const form = new FormData(e.target); const r = await fetch('/api/login', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(Object.fromEntries(form)) }); if (r.ok) { showModal(false); updateUser({authenticated:true,user:form.get('username')}); } else $('#login-error').textContent = (await r.json()).error; };
document.querySelectorAll('[data-view]').forEach(el => el.onclick = () => { const label = el.textContent.trim().replace(/\s*\d+$/, ''); $('#crumb').textContent = label; document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active')); const nav = document.querySelector(`[data-view="${el.dataset.view}"]`); if (nav && nav.classList.contains('nav-item')) nav.classList.add('active'); if (el.dataset.view === 'problems') document.querySelector('.recent').scrollIntoView({behavior:'smooth'}); });
$('#menu').onclick = () => $('.sidebar').classList.toggle('open'); $('.close-notice').onclick = e => e.currentTarget.parentElement.remove(); load();
