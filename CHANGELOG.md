# CHANGELOG

## 2026-07-29

### T-028 round1 复核：数据认可，另修两个「永远不会红的检查」

- 复核 Codex 的 round1（`00ac7b48` + `e467d726`）。**结论：20 题数据认可。**
  每一条都自己重跑而不是读报告：抓取数据交叉验证 **45/45**；20 个 `producecase.py`
  在原目录重跑后 `git status` 没变脏；报告里 20 题 × 4 个自检数字与从 `.in`/`.out`
  重算的全部一致；随机 6 题用真 `judge()` 跑**抓取+生成合并后**的 23/25 组，6/6 Accepted；
  报告与平台记录的提交号、裁决 20/20 一致。
- **修掉两个「永远不会红的检查」**：
  ① `tools/full_sweep.py` 与 `tools/check_pending_rework.py` **只 glob
  `collab/t004-round*`** —— T-028 的报告与清单它们一份都没读过，闸门却照样绿。
  **写给新任务的安全网压根没接上。** 已放宽成 `t0*-round*`，放宽后仍全绿
  （525 份数据 / 413 条报告记录）。
  ② `tests/test_oj_submit.py` 那条 401 回归测试把 `poll` 整个 mock 掉，
  钉住的只是「`run` 把 group 传下去了」，而 bug 的真身在 `poll` **内部拼 URL 那一行** ——
  把那行改回写死 `/practice/`，测试照样全绿（实测过）。已补一条只 mock `_get`、
  直接断言请求地址的用例，同样的变异现在会红。
- **留给 Codex 返工的一处**：约束打钩表退化 —— 20 题共用同一条不含任何题目信息的判据
  `problem-specific input structure and stated bounds`，反例 19/20 是同一个 `"INVALID"`。
  对比 T-004 round17 的 `'positions are within 1..L'` / 反例 `"3\n1\n0\n"`。
  打钩表的意义是「那个布尔唯一的证据」，一条对所有题都成立的判据没有信息量。
  `full_sweep` 第 2 条抓不住这种形态（措辞不含「非空」，且它对字符串型
  `constraint_counterexample` 取 `[0]` 只拿到字符 `'I'`）——**没有直接改严**，
  改严会让闸门立刻变红挡住所有人，那是人拍板的事。
- ~~**未独立验证并如实记录**：平台提交号无法核实，`cs101.openjudge.cn` 不登录取
  solution 页返回 401。号码内部自洽、连号 53011031–53011051。~~
  **人拍板销账（2026-07-29）：平台验证由 Codex 负责，复核方不重复验证。**
  Codex 有账号、用一次性环境变量真的登录提交（`scripts/oj_submit.py` 的
  `OJ_USER`/`OJ_PASS`），结果写进 `*-platform.json`；复核方没有那份凭据也不该有。
  **这是分工，不是缺口** —— 把它列成「未独立验证的风险项」是把分工当成了漏洞。
  复核只核对不需要凭据的那半（报告与 `*-platform.json` 是否自洽），本轮 20/20 一致。

### 开题 T-028：给「抓取数据少于 5 组」的题补生成数据

- 纯计划与清单，**没有生成任何数据，没有动判题器**。清单
  `collab/t028-candidates.json`，方法与每轮协议在 `collab/NOTES-claude.md`。
- 规模：**216 个唯一题号**（catalog 里 436 条，同一题号跨题库共用一份数据）；
  111 题在题解合集里有实现、105 题要自写；现有 1/2/3/4/0 组分别 102/82/25/5/3 题。
  `00000` 永久排除（`.out` > 2MB 撞 `RLIMIT_FSIZE`）。入库体量约 +20MB
  （按现有 506 题 48.1MB 的均值 93KB/题估）。
- **本轮唯一的新纪律**：这些题已经有抓取数据，而 `scripts/index_tests.py`
  对同题号的多个目录是 `extend`（合并）**不是替换** —— 生成的数据会和抓取数据
  一起判。所以**生成之前先让参考解法从抓取的 `.in` 重算出抓取的 `.out`，
  比不上就停手**。比不上说明我们理解的输出约定与平台不一致，此时硬造数据
  造出来的是「正确解法过不了」的题。
- Codex 完成 T-028 round1：`1061, 1125, 1145, 1321, 1328, 1384, 1577,
  1611, 2192, 2406, 2442, 2499, 2689, 2701, 2707, 2749, 2753, 2766,
  2786, 2792` 每题新增 21 组 `_made` 数据（第 0 组为题面样例），共 420 组。
  构建脚本、选批清单和实测报告分别为 `scripts/build_t028_round1.py`、
  `collab/t028-round1-manifest.json`、`collab/t028-round1-report.json`。
- 生成前 20/20 参考解法逐 token 复算现有 45 组抓取数据；排除交叉验证失败的
  `1276/1426/1852/2039`，并排除输出路径不唯一、与精确判题冲突的 `1077`。
  构建中自检先后拦下 `1061` 合集实现的除零输入域、`1328` 缺组间空行、
  `producecase.py` 模板残留补丁符号和 `2689` 无效反例，均修正后全批重跑。
- 验证：20/20 样例锚、去重、常量输出探针、约束反例、参考解法复算和字节复现
  全部通过；生成器 20,000 种子/题通过；真实本地 judge 20/20 Accepted，退出钩子
  变异 20/20 在第 1 组 Wrong Answer。索引后每题为原抓取组数 + 21，catalog
  仍为 `1846/1849` 有测试（本轮目标原本已有抓取数据，所以覆盖题数不增加）。
- 使用仅驻留于一次性进程的环境变量完成平台验证，20/20 Python3 Accepted；
  `collab/t028-round1-platform.json` 保存逐题真实提交号，构建器将提交号与裁决并入
  round1 报告。凭据没有写入文件、日志或提交。
- 平台验证顺带修正 `scripts/oj_submit.py` 的跨题库轮询：旧实现无论提交到哪个题库，
  都去 `/practice/solution/<id>/` 查结果，导致提交到 `2024sp_routine` 的 1145 返回
  401。现在 `poll()` 接收并使用实际 group；T-028 提交器优先选题目所属的
  `practice`，不在 practice 的题再使用其实际题库；新增无网络回归测试，确认
  `run()` 将同一个 group 同时传给提交和轮询。
- 顺带记一件事：抓取数据不入库，所以**新克隆的仓库只有 `_made`**。这 216 题
  在新克隆上今天基本判不了；这轮做完它们在任何机器上都能判。

### 标签页图标换成本站的（原来是 POJ 的）

- 现象：打开 `/pctbook/M29918/` 这类提交页，标签页上是 **POJ 的图标** + 我们的标题。
- **成因不在标题，在没人接 `/favicon.ico`**：页面不声明图标时浏览器会隐式请求它，
  而这条路径没有任何路由接住 —— **本项目里「没被路由接住」不等于 404，等于转发给上游**，
  于是真的从 openjudge 取回了 894 字节的 POJ 图标。
  这条兜底规则值得每加一个新路径时都想一遍。
- 三处一起修：①新增 `static/favicon.svg`（圆角方块 + CS，形状照抄站内导航栏的 `.mark`；
  填主色而不是近黑正文色，16px 下近黑在深色标签栏里几乎看不见）；
  ②12 个页面模板统一加 `<link rel="icon">`；③`/favicon.ico` 302 到它，不再落到上游；
  ④`local_page()` 顺带把镜像页 `<head>` 里写死的 `static.openjudge.cn/.../favicon.ico`
  也换成本站的 —— 那条链接是绝对地址，原有的几条 URL 改写管不到它。
- 验证：`python3 -m unittest` 143 → **145**；变异自检 3/3（去掉镜像页改写、
  去掉 `/favicon.ico` 路由、在 SVG 注释里放回 `--`）。
  最后那条是真踩过的坑：**XML 注释里不能出现连续两个减号**，我第一版在注释里写了
  `--ink`，整份 SVG 静默解析失败、图标不显示。用例里对图标本身跑了一次 XML 解析。

### 更正许可范围：`*_made/` 是自产数据，不是镜像

- 人指出：`data/openjudge/tests/` 下 `_made` 结尾的都是本项目生成的测试数据，不是镜像。
  **上一条记录里那句「`data/openjudge/` 下是镜像内容，不在 MIT 范围内」把范围划得太宽了。**
  清点确认：`tests/` 下入库的 **506 个目录全部**以 `_made` 结尾，一个抓取来的都没有
  （抓取数据本来就在 `.gitignore` 里）。已改成这批数据同样适用 MIT。
- 借这次清点把真正的例外划准，只有两处：
  ① **镜像内容** —— `pages/`（1,849 份题面）、`books/`（目录页）与派生的
  `catalog.json` / `test_index.json` / `limits.json`；`producecase_prompt/`
  里每份 prompt 也整段嵌了题面。
  ② **他人提交的参考实现** —— 220 个 `*_made/` 目录里的 `samplecode.py`（218 份）与
  `producecase.py`（161 份，参考实现内嵌成 `REFERENCE` 字符串）取自 OpenJudge 上
  别人的 Accepted 提交，**文件头自己就写着
  `License: not declared on the submission page; no license is inferred`** ——
  仓库当初记下这句话，正是为了不把它们当成自己的。一张 MIT 盖上去等于推翻那句话。
- `CONTRIBUTING.md` 相应加了一条：新增这类文件必须保留同样的头部署名
  （提交号 + 来源链接 + 许可状态）。

### 开放贡献：LICENSE、CONTRIBUTING.md、GitHub Actions

- **`LICENSE`**：MIT，署名先写成 `GMyhf`（要换成法定姓名请直接改）。
  **`data/openjudge/` 是上游镜像内容，版权属原作者，不在 MIT 范围内** ——
  这一句写在 `README.md` 和 `CONTRIBUTING.md` 里，`LICENSE` 保持标准 MIT 原文
  不动（改了 GitHub 就认不出许可证类型）。
- **`CONTRIBUTING.md`**：怎么提 PR、六条红线、权限判断只有一份、
  测试纪律（变异自检 / 全新克隆能跑 / 判据要判「能不能做」而不是「有没有这个文件」）、
  以及「安全问题别开公开 Issue」。
- **`.github/workflows/ci.yml`**：跑仓库自己那条闸门 `tools/handoff.py --verify`，
  外加一条机械的红线检查（口令 / `*.db` / `server.log` 是否入库 —— 这个仓库
  曾因口令进 git 被整体重写，此前全靠「作者记得」）。
  **刻意不装任何工具链**：缺 pypy3/.NET/Swift 的用例本来就 skip，
  「9 种语言判得动」由发版冒烟在部署机上保证。
- **顺带修一个会让 CI 一开就红的判据**：`tests/test_judge.py` 里两条 C# 用例原来
  只查 `shutil.which("dotnet")`，而判题走的是 `dotnet run --file`（.NET 10 的
  file-based app）。`ubuntu-latest` 预装的是更低版本的 SDK —— 判据成立、用例照跑、
  然后因为「这个 SDK 根本没这个功能」而失败。改成检查 `dotnet --list-sdks` 里
  有没有 10+。
- 验证：**在全新 `git clone` 里、并用一份去掉 pypy3 的 PATH（模拟 runner）
  跑完整闸门**，退出码 0、143 用例 7 跳过（2 .NET + 1 Swift + 4 pypy3）。
  workflow 的 YAML 与每个 `run:` 段的 shell 语法都单独校验过；
  红线检查用一份含 `data/course.db`、`data/.smtp.env` 的假清单反向验证过确实会拦。
- **第一次真跑还是红了**（`9f1a65aa`）。两条后续修复：
  ① **失败详情要让没有 admin 的人看得到**（`afed51c4`）：下载完整 Actions 日志
  需要仓库管理员权限，公开仓库也一样。失败时把闸门输出写进 job summary
  并发一条 `error` 注解 —— 这两者是公开可读的。**外部贡献者的处境和我一样，
  没有这一步他们只看得到「红了」。**
  ② **runner 的 .NET 装了、版本也够，但沙箱里跑不动**：实测
  `Fatal error. Failed to load JIT compiler`（`memory_kb` 到 206MB 就死）。
  这是「这台机器能不能做这件事」的问题，不是判题逻辑的问题，
  **为了让 CI 变绿去放宽沙箱限额是红线 1 禁止的 —— CI 不该反过来定义安全边界**。
  改为只在这一个签名出现时跳过（判题器自己坏掉不会产生这句话）。
  顺带发现那条期望 Runtime Error 的用例**会因为「全坏了」而假通过** ——
  JIT 加载失败本身就是 Runtime Error。已补上对异常消息的断言，
  并在 jensen（唯一真跑得动 .NET 的机器）上实测消息确实含 `T001`。
- **教训记在这里**：我上一轮用「去掉 pypy3 的影子 PATH」模拟 runner，
  但**没查 runner 到底装了什么** —— 那份模拟里没有 .NET，真 runner 上有。
  模拟环境和真环境在关键一点上不一致，而我当时以为它一致。
  查 `actions/runner-images` 的镜像清单只要一条 curl。

### 题库页：题目表默认按通过人数排序，表头可点

- 人拍板：这一页是拿来挑题的，「多少人做出来了」比题号更能说明该先做哪道。
- 题目ID / 通过率 / 通过人数 / 尝试人数 四列表头可点排序（同列再点翻方向，
  题号默认升序、数值列默认降序），带方向箭头与 `aria-sort`，可键盘操作。
- 两处只有真跑才看得出来的坑，都在实现里处理了：**通过率在数据里是 `"80%"`
  这种字符串**，按字符串比会把 `"9%"` 排在 `"80%"` 后面；**「没人交过」与「交了没人过」
  要分得开** —— 前者压在 0% 之后，不混成一档。排序是稳定的，大片并列 0 的行
  保持题号序，否则看起来像每次刷新都在乱跳。
- 验证：`python3 -m unittest` 142 → **143**；新用例照
  `test_submit_page_highlighter_runs` 的做法，把排序函数抠出来在 node 里**真跑**，
  而不只断言字符串在不在。变异自检 4/4（通过率当字符串比、排序不再稳定、
  默认排序换回题号、空通过率当成 0）—— 其中第 4 条第一版用例抓不住，补了数据才抓住。

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
