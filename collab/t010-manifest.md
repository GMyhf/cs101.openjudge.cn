# T-010 清单 · 提交页力扣化改造

> 本文件是 T-010 的**规格与交付门槛**，格式沿用 t004-round\*-manifest 的作用（开工前把标准写死，
> 交付时逐条对照），只是 UI 改造无需机器消费，故用 Markdown 而非 JSON。
> 人拍板的三个决策见「拍板点」一节，**未拍板前 P3 与 P1-a 不得开工**。

## 目标

把 `http://100.123.12.92:8000/practice/02942/` 改成力扣题目页那种**全屏工作台**，
并把这套设计 token 推广到全站，消灭 10 份互不一致的内联配色。

人已定的三项（2026-07-28）：
1. **全屏工作台**：整页不滚动，左右两块独立圆角卡片，提交记录移入左侧标签页
2. **加「运行样例」**：先用题面样例跑一遍再提交（需新后端端点）
3. **全站统一**：其余 10 个页面统一到同一套 token 与深色模式

## 现状勘查（已核实，含行号）

| 事实 | 位置 |
| --- | --- |
| 整页是**一个 495 行 Python 裸字符串** `SUBMIT_PAGE`（HTML+CSS+JS 三合一） | `server.py:79-573` |
| `/practice/02942/` 与 `/practice/02942/submit/` 渲染**同一页面** | `server.py:1056-1061`、`1069-1073` |
| 7 个占位符，`__STATEMENT_PARAMS__`/`__STATEMENT_CONTENT__` **未转义**注入 | `server.py:976-982` |
| 题面只取镜像页两个 `<dl>` 的内层 HTML，上游 chrome 全丢 | `problem_parts()` `server.py:943-954` |
| 编辑器是**透明 textarea 叠在高亮 `<pre>` 上**，手写高亮器，零外部库 | `server.py:196-204`、JS `288-473` |
| 判题**完全同步**，`POST /api/submit` 最长阻塞 300s，无队列无轮询 | `server.py:1320-1341` → `judge.py:169-308` |
| `style.css`、`app.js` 是**死代码**，无任何页面引用 | 仅 `tools/handoff.py:129-130` 跑 `node --check app.js` |
| `modern_problem_page()` 是**死代码**，无路由调用 | `server.py:956-968` |
| 静态兜底路由已能服务 `/static/*.css`，**服务端零改动**（`.css` MIME 正确，子目录 `ROOT in file.parents` 成立） | `server.py:1136-1145` |
| 无任何共享 chrome helper（无 `head()`/`nav()`/`layout()`），导航条在 5 处逐字复制 | — |
| **全部 1849 个镜像页**都恰有一组 `<dt>样例输入</dt><dd><pre>…</pre></dd><dt>样例输出</dt><dd><pre>…</pre></dd>`（脚本验证 ok=1849 bad=0） | `data/openjudge/pages/*.html` |

## 拍板点（**2026-07-28 人已全部批准**，见 PLAN.md Decision Log）

| # | 决定 |
| --- | --- |
| 1 | **准许新增 `static/theme.css`**（红线 6 让路一次） |
| 2 | **准许新增 `POST /api/run`，但沙箱一条不放宽**（红线 1+2） |
| 3 | **并发互斥一并做进 T-010**，不另开任务 |

分工：**Claude 实现全部四个阶段 → `tools/handoff.py --from claude --to codex` 生成 review 包
→ 人转交 Codex 红队复核 P3（沙箱 + 认证），按脚手架「生成 ↔ 审查」模式。**
与 T-008 同形——那次 Codex 抓到真 bug（`shutil.which` 查本进程 PATH、子进程拿受限 PATH，
不一致时裸名字 `FileNotFoundError` 抛成服务端 500）。若人愿意并行驱动 Codex，
P4（其余 10 页统一）机械性强、不碰红线，是最适合切走的一块。

### 拍板点 1 · 红线 6「单文件极简风格」— 是否允许新增 `static/theme.css`

现状是 10 份页面各自内联一套 `:root`，配色值互相漂移（`--accent` 有 `#2f7d55`/`#237a50`/`#3d8b68` 三个版本），
深色模式只有提交页有、且靠 19 条硬编码色覆盖堆出来。要「全站统一」，要么新增一个共享 CSS 文件，
要么在 `server.py` 里加一个 `THEME_CSS` 常量并在 10 处内联展开。

- **不是第三方依赖，也不是框架**——红线 6 的字面禁止对象（框架/依赖）都不触发；
  但它确实让本项目从「零外部资产」变成「一个外部资产」，属结构变化，故提请拍板。
- 选 A（`static/theme.css`）：浏览器可缓存、10 个页面共用一份、改配色只改一处。代价是多一个文件。
- 选 B（`server.py` 里的 `THEME_CSS` 常量）：严守两文件风格。代价是 4 个平铺 HTML
  （`index.html`/`problems.html`/`history.html`/`admin.html`）拿不到这个常量，
  要么它们继续各写一份（统一失败），要么把它们也搬进 `server.py`（`server.py` 再涨 ~600 行）。

**建议 A。** 但这是人的决定。

### 拍板点 2 · 红线 1+2「判题沙箱 + 认证边界」— 是否新增 `POST /api/run`

「运行样例」要在服务器上跑不可信用户代码，这是本项目最敏感的一条路径。设计约束：

- **复用同一套沙箱**：`prepare_program()` 与 `_run()` 原样使用，`RLIMIT_CPU`/`RLIMIT_FSIZE`/`RLIMIT_AS`
  三条限额、`env` 白名单（恰好 `{PATH, HOME}`）、`python3 -I`、临时目录隔离**一律不放宽**。
  沿用 T-008 立下的顺序：**先测能不能不放宽，再决定要不要放宽**。
- **必须登录**，与 `/api/submit` 同级（`server.py:1342` 的 401 兜底）。
- **不写 `submissions` 表**，不计入判题记录与统计。
- stdin 上限 64 KiB，输出截断 64 KiB。
- 单组预算走 `case_seconds()`，不新增更宽松的时间口径。

**已知风险（无论拍板与否都存在，建议一并处理）**：`/api/submit` 现在**对并发毫无节流**——
`ThreadingHTTPServer`（`server.py:1348`）每个并发提交都直接在 HTTP 线程上拉起编译器/解释器。
加了「运行」按钮后连点会放大这个暴露面。建议同时加「同一用户同时只允许一个判题/运行在跑」的轻量互斥。

### 拍板点 3 · 分工

- **方案甲（生成↔审查）**：Claude 实现全部 4 个阶段，Codex 专门红队 P3（沙箱 + 认证），写会失败的测试。
  与 T-008 同形——那次 Codex 抓到了真 bug（`shutil.which` PATH 不一致 → 服务端 500）。
- **方案乙（分工并行）**：Claude 做 P1+P2（token + 提交页布局），Codex 做 P4（其余 10 页统一，机械性强、
  不碰红线），P3 由 Claude 做完后 Codex 红队。两人分支隔离，冲突面只有 `server.py` 的不同区段。

**建议乙 + P3 红队**，理由：P4 是纯机械替换、量大、与红线无关，最适合并行切走；
而 P3 必须走「一方实现、另一方找茬」。

---

## 阶段规格

### P1 · 设计 token 与共享外壳

- 单一 token 表。沿用现有语义命名不新增前缀：`--ink --muted --line --bg --panel --soft --accent`，
  补 `--ok --warn --danger --radius --shadow --topbar-h`。
- **把现在硬编码的颜色收进变量**：`--tok-com/--tok-str/--tok-num/--tok-kw/--tok-pre/--tok-match`、
  `--badge-{ac,wa,other,info}-{bg,fg}`。这样深色模式从 `server.py:135-153` 的 **19 条规则塌缩成 1 个块**。
- 深色模式默认跟随系统（`prefers-color-scheme`），`data-theme` 显式覆盖胜出；
  `<head>` 里一段同步 `<script>` 在首屏绘制前写好 `dataset.theme`，避免闪白。
- 清死代码：删 `style.css`、`app.js`（**同步改 `tools/handoff.py:129-130`**）、`server.py:956-968` 的 `modern_problem_page()`。

### P2 · 提交页全屏工作台

```
<body class="app">                    height:100dvh; overflow:hidden
  <header class="topbar">             48px：CS101 · 题库 / 02942 吃糖果 · 目录 记录 说明 · ☾ · 账号
  <main class="workspace-layout">     flex:1; min-height:0; grid: 左 | 6px | 右
    <section class="pane pane-left">
      <nav class="pane-tabs">题目描述 | 我的提交 | 提交统计
      三个 .pane-body，各自独立滚动
    <div class="splitter splitter-v" id="splitter">
    <div class="pane-col">            grid-rows: 1fr | 6px | var(--result-h) | auto
      <section class="pane pane-editor">   pane-tabs: 代码 <select> ⟲重置 A字号 ⛶全屏
      <div class="splitter splitter-h" id="splitter-h">
      <section class="pane pane-result">   pane-tabs: 判题结果 | 样例
      <div class="action-bar">        .editor-state 左 | [运行样例] [提交并判题] 右
```

- `.editor{flex:1;min-height:0}` **取代写死的 `height:520px`** —— 编辑器随视口伸缩。
- 每个 `.pane` 都 `display:flex;flex-direction:column;min-height:0;overflow:hidden`，
  滚动只发生在 `.pane-body` 内，页面本身永不滚动。`min-height:0` 必须落在每一层子项上。
- **透明 textarea 与高亮 `<pre>` 的 `font`/`line-height`/`padding` 必须逐字节一致**
  （`server.py:116-117` 已警告过）——字号切换用同一个 `--code-size` 驱动两层。
- 两个滑块：现有横向逻辑（`server.py:223-235`，Pointer Events + pointer capture + localStorage）
  抽成 `makeSplitter(el,{axis,key,...})` 复用；补上现在缺失的**键盘支持**
  （元素已有 `role="separator"`/`tabindex="0"` 却无 keydown 处理）。
- 提交记录从编辑器下方整体搬进左侧 `#tab-history`；取数逻辑不动（`loadHistory()` `server.py:537-572`）。
  新「提交统计」页读 `/api/catalog`（`server.py:791-813` 已算好 `accepted_count`/`attempt_count`/`pass_rate`）。
- 判题结果从 `<dl>` 键值对改成：大号状态标题 + 一排指标 chip + 折叠的 message/snippet。**数据字段一个不改**。
- **顺带修一个既有缺陷**：历史表 `<thead>` 声明 8 列（`server.py:545`）但每行只输出 7 个 `<td>`（`559-566`），
  算好的 `size`（代码长度，`551`）从未渲染 → 该列及右侧所有列整体左移一格。
- 响应式 `@media(max-width:900px)`：恢复 `overflow:auto`、塌成单列、隐藏两个 splitter。

### P3 · 运行样例（**拍板点 2 通过后才开工**）

1. `judge.py` 把 `judge()` 里 180-267 行的编译/准备段抽成
   `prepare_program(work, language, source, warmup_input=b"")` → `(command, None)` 或 `(None, error)`。
   **纯移动，不改行为**；`tests/test_judge.py`（~28 用例，零 HTML 耦合）是安全网。
2. 新增 `judge.run_sample(book, problem_id, language, source, stdin)`：复用
   `problem_limits`/`case_seconds`/`_run`，只跑一次，返回 `{status, stdout, stderr, time_ms, memory_kb}`。
3. `server.py` 新增 `sample_io(page)`，紧挨 `problem_parts()`（`server.py:943`）：
   正则取样例输入/输出，剥 `<pre>`、`html.unescape`。**已对全部 1849 页验证通过**。
4. `submission_page()` 增加第 8 个占位符 `__SAMPLE_JSON__`（`json.dumps` 内联）——
   服务端出数据，前端不刮 DOM。
5. 新路由 `POST /api/run`，约束见拍板点 2。
6. 前端「样例」标签页三栏：输入（可编辑，预填）/ 预期输出（只读）/ 实际输出。
   判定用与 `judge.py:307` **完全相同**的规则 `actual.split() != expected.split()`。

### P4 · 全站统一

`index.html`、`problems.html`、`history.html`、`admin.html`
+ `server.py` 内的 `help_page` `984`、`account_page` `989`、`activation_page` `1004`、
`forgot_page` `1015`、`reset_page` `1020`、`account_settings_page` `1023`。
删各自的 `:root` 与基础样式，换共享 token + `.topbar`；页面专属样式保留。

---

## 交付门槛

### 必须修改的测试
- **`tests/test_server.py:227`** — `assertIn("height:520px")`。全屏布局下编辑器不再定高，
  改断言新的结构标记。**这是设计意图变更，改测试是正确的，但必须在交接里明说改了哪条、为什么。**
- 新增：`test_submit_page_embeds_sample_io`、`test_run_endpoint_requires_auth`、
  `test_run_endpoint_does_not_record_submission`。

### 必须原样保留的字符串（改了就红）
| 字符串 | 断言处 |
| --- | --- |
| `workspace-layout` | `test_server.py:219` |
| `我的提交记录`、`查看代码`、`查看判题详情` | `test_server.py:219`、`249` |
| 五个 `value="csharp">C# (.NET SDK 10)` 等 option 字面量、`G++(`、`Python3(`、`PyPy3(`、`value="pypy3"`、`value="python"` | `test_server.py:219`、`571`（**语言顺序与格式被钉死**） |
| 提交页**不得**出现 `Python ×10` | `test_server.py:240` |
| `id="account-control"`、`id="account"`、`href="/account/">账户设置</a>`、`id="logout"` | `test_server.py:128`（index.html） |
| `result-message` | `test_server.py:249`（history.html） |
| `题库目录`、`/api/catalog` | `test_server.py:194`（problems.html） |
| `提交记录`、`/api/submissions` | `test_server.py:618`（history.html） |
| `Python ×10`、`C#/F#/VB.NET 内存 ×2` | `test_server.py:242`（help_page） |
| 注册验证码 markup：`name="captcha_token" value="…"`、`class="captcha-question">N + N` | `test_server.py:39-46`——**所有登录态测试都依赖它** |

### 结构性约束（最容易踩）
`test_server.py:529` 与 `586` 会把 `SUBMIT_PAGE` 从 `<script>` 切到**最后一个** `</script>`，
再从字面量 **`const PY_KW`** 切到 **`function paintEditor`**，把这段丢进 node 执行。
所以：**高亮器 JS 必须继续内联在 `SUBMIT_PAGE` 最后一个 `<script>` 里，`PY_KW` 在前、
`paintEditor` 在后且中间连续；`SPECS`/`highlight`/`bracketMatch`/`indentFor`/`pairAction`
与 `t-kw/t-com/t-str/t-num/t-match` 类名一律不许改名。**
→ **CSS 可以外提，JS 不外提。**

### 红线自检（交接时逐条打钩，须有实测支撑）
1. **判题沙箱**：`_limits()` 三条限额值未变；`env` 仍恰好 `{PATH, HOME}`；Python 仍带 `-I`；
   新端点走的是同一个 `_run()`。→ `SandboxContractTests` 必须全绿，且**变异自检证明它真会红**。
2. **认证边界**：`/api/run` 未登录返回 401（新增测试）；口令未入 git。
3. **路径安全**：`ROOT in file.parents` 与题库名白名单正则**一字未动**；
   `static/` 只是多了一个子目录，防穿越靠的仍是 `server.py:1036` 的 `..` 拦截。
4. **不引第三方依赖**：编辑器仍是手写高亮器，零 CDN、零 npm。
5. **长请求**：提交可阻塞 300s，**不得引入客户端 fetch 超时**，也不得做「已排队」的乐观 UI
   （服务端没有队列）。

### 冒烟清单（浏览器，`http://100.123.12.92:8000/practice/02942/`）
- [ ] 整页无纵向滚动条；只有 `.pane-body` 内部滚动
- [ ] 左右、上下滑块都能拖；刷新后位置保持；键盘方向键可调
- [ ] 左侧三个标签页切换正常；提交记录**列数与表头对齐**（旧缺陷已修）
- [ ] AC / WA / Runtime Error / Compile Error 四种状态样式都对
- [ ] 「运行样例」跑通；改输入后重跑；**运行不产生提交记录**（去 `/history/` 核对）
- [ ] 深色模式切换无闪白，刷新后保持；语法高亮与徽章在深色下可读
- [ ] 窗口 <900px 塌成单列且可滚动
- [ ] 换 C++ 题提交一次，确认长耗时请求不被前端超时打断
- [ ] 管理员（GMyhf）登录，确认「判题设置」入口与他人提交详情可见性未受影响

### 闸门
```bash
python3 tools/handoff.py --verify     # 必须退出码 0，且输出含全套测试尾部计数
```
