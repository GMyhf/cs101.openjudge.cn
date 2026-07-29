# CHANGELOG

## 2026-07-29

### 题库页：排名点用户名、状态点结果，各进一页

- 新增 `/book/<题库>/user/<用户名>/`（这个人在本题库做过的题）和
  `/book/<题库>/solution/<提交号>/`（一次提交的详情），对应
  `/api/books/<题库>/user/<用户名>/` 与 `/api/books/<题库>/solution/<提交号>/`。
  两页都复用 `book.html` 这一份模板，标签条分别高亮「排名」「状态」。
- **权限照抄 `/api/submissions` 那条判断，不另写一份**：
  用户页只出记分板字段（结果 / 次数 / 时间），**完全不出代码和判题详情**；
  提交详情页记分板那半人人可见（谁、哪道题、什么结果、用时内存代码长度），
  **代码与判题详情只有本人和管理员**，别人看到的是一句明写的「看不到」而不是空白。
  两页整页都要登录，未登录 401。
- 提交号跨题库取不出来（`where id = ? and book = ?`），不存在的用户/提交都是 404。
- 验证：`python3 -m unittest` 138 → **142**、`tools/handoff.py --verify` 通过；
  变异自检 3/3（`owner` 恒真、用户页带上 `source`、去掉跨库校验）；
  本人 / 他人 / 管理员三种视角各截图核对。

### 线上数据：清掉 20 条 `NOT-IN-CATALOG` 占位提交

- 不是代码改动，是**对 jensen 上 `data/course.db` 的一次不可逆删除**，记在这里备查。
- 删的是：`book='practice'`、`problem='NOT-IN-CATALOG'`、`user='GMyhf'`、
  `result='Problem Not Found'`、`created like '2026-07-28 08:22:%'` —— id 36–55 共 20 条，
  来自 T-025 开放公网当天的手工冒烟。`changes()` 返回 20，与删前清点一致。
- **删前先备份**：`tools/backup_db.py` → `course-20260729T032301Z.db.gz`
  （`users=9 submissions=55 settings=2`，存于 jensen `~/backups/cs101`）。
  删后 `submissions=35`、`pragma integrity_check` 为 `ok`。
- 未动其余 35 条。服务无需重启（每次请求现读库），practice 状态页已确认干净。

### 线上数据：再清掉 11 条无题库的早期提交

- 同样是**对 jensen 上 `data/course.db` 的不可逆删除**。删的是 id 1–11：
  `book is null`、`user='GMyhf'`、`created like '2026-07-23%'` —— 早于 `book` 列存在，
  无 `language`、无 `source`。`changes()` 返回 11，与删前清点一致。
  （更正上一条里的说法：这些行的 `book` 是 `NULL`，不是空串。）
- **删前先备份**：`course-20260729T035517Z.db.gz`（`submissions=35`）。
  删后 `submissions=24`、`book` 为空的行 0 条、`pragma integrity_check` 为 `ok`。
- 线上复核：`/api/stats` 为 `submissions=24 accepted=10 solved_problems=4`；
  `/history/` 24 行、无缺 `book` 的行。剩下的全部是真实用户提交
  （ZHANGSan / FuYn / Camellia / lyss_121259 / GMyhf 各自的真题记录）。

### 题库页：通过人数 / 尝试人数可点进统计页

- `book.html` 把这两个数字做成链接，指向 `/history/?book=…&problem=…`，
  与 `/problems/` 目录页原有做法一致。数字为 0 时不做链接。
- 统计页仍是 `/api/submissions` 那套老规则：**列表人人可见，代码与判题详情只有
  本人和管理员拿得到**。未登录访问该 URL 是 401，页面提示先登录。
- 顺带两处：①按题目进入时把条数上限默认拉到 500，并在真被截断时明说
  「已达上限，下面的统计只算这 N 条」—— 四张统计卡是按返回的行算的，
  默认 50 条会让它们看起来像全量结论。②补上 `history.html` 缺失的 `.wrap` 规则，
  这一页此前一直贴着浏览器左边框。
- 验证：`python3 -m unittest` 138 通过（新增 2 条）、`tools/handoff.py --verify` 通过；
  变异自检 1/1（把 `source` 的本人/管理员判断去掉即变红）；普通用户与管理员两种
  身份各截图核对。

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
