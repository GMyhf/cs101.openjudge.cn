'use strict';
// 首页与题库目录共用显示范围和顺序；私有题库的权限仍由服务端过滤。
const catalogBooks = {
  hidden: new Set(['2024fallroutine', '2025sp_routine']),
  order: ['pctbook', 'practice', 'routine', '2024sp_routine', 'codeforces'],
  isVisible(book) { return !this.hidden.has(book); },
  compare(a, b) {
    const rank = book => this.order.includes(book) ? this.order.indexOf(book) : this.order.length;
    return rank(a) - rank(b) || a.localeCompare(b);
  }
};
