# CHANGELOG

## 2026-07-29

### 重做：题库页（题目 / 排名 / 状态），走 `/book/` 前缀

- 新增 `book.html`、`server.py · book_page_payload()` / `Handler.book_page()`、
  路由 `/book/<题库>/[ranking|status]/` 与 `/api/books/<题库>/`；
  首页题库标题由 `/problems/?book=…` 改指 `/book/<题库>/`。
- **与被撤销的 `93dedfff` 的差别**：那一版接管了 `/{题库}/`，把上游镜像原页顶掉了；
  这一版走 `/book/` 前缀，`/pctbook/` 等镜像页原样保留，题面里的老链接不受影响。
- 排名与状态需登录才返回数据（站点自 T-025 起对公网开放）；状态行只含
  `time_ms` / `memory_kb`，不含 `failing_input` / `expected_output` / 源码。
- 验证：`python3 -m unittest` 136 通过（新增 4 条）、`tools/handoff.py --verify` 通过；
  8 个题库 × 3 个标签页共 24 个页面逐个实测 200；变异自检 2/2。

### 已撤销：题库页题目、排名、状态 Tab

- `93dedfff`：新增统一题库页、排名和状态接口，后由 `7242818b` 撤销。
- `f1a89e10`：首页题库标题改为直达题库页，后由 `da43880a` 撤销。
- `1dabfb46`：题库页样式改为参考 pctbook 结构，后由 `00a04c7e` 撤销。
- 当前生效状态：上述功能、路由、模板、首页入口及相关测试均已移除；线上服务已按撤销后的 `main` 重启，`/pctbook/` 恢复原页面。

### 记录规范

- 此后每笔功能改动、修复、部署相关代码改动及其撤销，都必须在本文件留下可追溯的提交号和结果说明。
