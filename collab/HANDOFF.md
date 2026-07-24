# HANDOFF · 交接日志

> 每次「我做完这一轮，轮到你」都在**最上方追加**一条记录（倒序，最新在前）。
> 这是人（路由器）和另一方 agent 快速接手的入口。严格套用下面模板，减少人工搬运。

## 交接模板（复制这一段）

```
### <日期 YYYY-MM-DD HH:MM> · <From> → <To> · T-<任务ID>

- **做了什么**：<1-3 句，用户可见行为 / 判题与认证影响优先说>
- **改了哪些文件**：`path/a.py`, `path/b.py`
- **关联提交**：<git short sha 或「未提交，见 review-input.md」>
- **验证**：`python3 tools/handoff.py --verify` <通过/失败> ｜ 冒烟 <做了什么、结果>
- **请重点看**：<最想让对方审查/质疑的地方，边界情况、没把握的取舍>
- **红线自检**：判题沙箱未放宽 ✅/⚠️ ｜ 口令未入库 ✅/⚠️ ｜ 路径防线未动 ✅/N/A
- **下一步建议**：<给对方的一句话方向>
```

---

<!-- 新交接追加在这条分隔线下方、最上面 -->

### 2026-07-24（第五轮） · Codex → Claude · T-002 20 题试点批

- **做了什么**：交付 20 个缺测试数据题目的 `_made` 试点目录；每题包含 `samplecode.py`、固定题号种子的 `producecase.py` 和 20 组 `data/0..19.in|out`。多解/特殊判题候选另列清单，未混入本批。
- **改了哪些文件**：`scripts/build_t002_pilot.py`, `collab/t002-special-judge-skips.md`, `collab/NOTES-codex.md`, `collab/PLAN.md`, `data/openjudge/catalog.json`, `data/openjudge/test_index.json`；生成目录在 `data/openjudge/tests/*/*_made/`（按 `.gitignore` 不入 Git）
- **关联提交**：未提交，见 `review-input.md`
- **验证**：`python3 tools/handoff.py --verify` 待本轮末跑 ｜ 样例断言 20/20 通过；逐题重跑生成器后 20×20 组复算一致；`judge.py` 真实路径 20/20 `Accepted`，每题 20 组
- **请重点看**：`05455` 去重后按插入顺序建 BST；`24637` 按完全二叉树下标做树形 DP；`27880` 按 Kruskal 的“最少边、再最小最大边”输出；样例组均为网页原样输入/输出。
- **红线自检**：判题沙箱未放宽 ✅ ｜ 口令未入库 ✅ ｜ 路径防线未动 ✅
- **下一步建议**：按任务书五条标准逐题抽查；确认通过后再按约 100 题/批放量。

### 2026-07-24（第四轮） · Claude → Codex · T-002 开工核验复核通过

- **做了什么**：独立复核 `5b646ab`。新旧 catalog 逐条对比 0 丢失、33 增 88 涨；
  +2625 对出处查明（69 个含 `data/` 目录，均系人此前生成，非误扫）；全量引用文件
  0 缺失；顶层/`data/` stem 冲突 0；judge 真跑 4102：samplecode AC 20 组、
  改错版 WA 且报 `case=1`。详情见 `NOTES-claude.md` 本日复核条。
- **改了哪些文件**：`collab/PLAN.md`, `collab/NOTES-claude.md`, `collab/HANDOFF.md`（纯复核记录）
- **关联提交**：见 git log
- **验证**：见上；`python3 tools/handoff.py --verify` 通过
- **请重点看**：我记录在案的一个潜在错配点——顶层与 `data/` 出现同 stem 时 dict 覆盖
  会静默混配（当前 0 实例）。试点批生成时**保持数据只写 `data/` 一处**即可天然规避。
- **红线自检**：纯文档轮 ✅
- **下一步建议**：交 20 题试点批：逐题 `samplecode.py` + `producecase.py`（固定种子 +
  题面样例断言）+ `data/*.in|*.out`，附样例自检汇总输出；多解题跳过并列清单。

### 2026-07-24 · Codex → Claude · T-002 开工核验

- **做了什么**：索引器已支持题目目录下 `data/*.in` 与 `data/*.out`，使人的两个 `_made` 样板进入索引；按 catalog 重新导出缺数据清单。
- **改了哪些文件**：`scripts/index_tests.py`, `scripts/export_missing_tests.py`, `data/openjudge/catalog.json`, `data/openjudge/test_index.json`, `collab/t002-missing-tests.json`, `collab/PLAN.md`, `collab/NOTES-codex.md`
- **关联提交**：未提交，见 `review-input.md`
- **验证**：`python3 tools/handoff.py --verify` 通过 ｜ 冒烟：索引前后有测试 catalog 记录 `945 -> 978`，`4102_made=20`、`18250_made=10`；`git diff --check` 通过
- **请重点看**：索引结果重建了 catalog/test_index 的测试路径；已有 945 条未减少，但总配对数增加到 9701。工作区原有 prompt 删除状态未触碰。
- **红线自检**：判题沙箱未放宽 ✅ ｜ 口令未入库 ✅ ｜ 路径防线未动 ✅
- **下一步建议**：审查索引与 885 条清单后，继续交付 20 个真正新生成的 `_made` 试点目录，逐题执行样例自检和真实判题验收。

### 2026-07-24（第三轮） · Claude → Codex · T-002 前置全部清除，可以开工

- **做了什么**：人补齐了 `tests/20000-29982/` 桶。复核：七桶齐全，catalog 引用的
  14152 个 in/out 文件**零缺失**。`index_tests.py` 解禁。T-002 不再有任何前置阻塞。
- **改了哪些文件**：`collab/PLAN.md`, `collab/NOTES-claude.md`, `collab/HANDOFF.md`（纯销账）
- **关联提交**：见 git log
- **验证**：核对脚本输出 `referenced files: 14152 | missing on disk: 0`
- **请重点看**：无新增内容，规格仍以第二轮任务书为准
- **红线自检**：纯文档轮 ✅
- **下一步建议**：Codex 认领 T-002 开工：① 修索引器收 `data/*.in` → 跑
  `index_tests.py` 确认 `4102_made`/`18250_made` 生效且原 945 条不减；② 导出缺数据
  清单；③ 交 20 题试点批。

### 2026-07-24（第二轮） · Claude → Codex · T-002 任务书更新：改用人的 producecase 工作流

- **做了什么**：人恢复了 tests 树并提供了自己的生成模版
  （`data/openjudge/producecase_prompt/` 37 份单题 prompt + 实物样板
  `tests/4000-8210/4102_made/`）。任务书按人的工作流重写（NOTES-claude.md 已更新），
  我此前起草的 `tools/make_data_template.py` 删除，其中样例自检 + 固定种子两条纪律
  并入规格。二次勘查发现两个新事实：**① tests 树缺 `20000-29982` 桶，catalog 里
  2236 条引用悬空（这些题提交会崩），等人补齐，补齐前仍禁跑 `index_tests.py`**；
  ② 人已生成的 `4102_made`/`18250_made` 因数据在 `data/` 子目录而未被索引
  （`test_count=0`），修索引器（改收 `data/*.in`）纳入 T-002 范围。
- **改了哪些文件**：`collab/PLAN.md`, `collab/NOTES-claude.md`, `collab/HANDOFF.md`；
  删除 `tools/make_data_template.py`
- **关联提交**：见 git log
- **验证**：`python3 tools/handoff.py --verify` 通过；六个在盘桶的 catalog 引用
  缺失数=0（已用脚本核对），缺失的 2236 条全部属于 20000-29982 桶
- **请重点看**：规格里「产物目录布局照 `4102_made` 样板」「多解题跳过并列清单」
  「样例断言不过不许落盘」三条——试点批我会逐条验收
- **红线自检**：判题沙箱未动 ✅ ｜ 口令未入库 ✅ ｜ 路径防线未动 ✅（纯文档轮）
- **下一步建议**：Codex 可先做不依赖 20000 桶的准备工作：修索引器 + 导出缺数据清单 +
  挑 20 题试点（避开 20000-29982 段的题号即可并行）。

### 2026-07-24 · Claude → Codex · T-002（任务指派，非代码交接）

- **做了什么**：起草 T-002 任务书——为 catalog 中 918 个无测试数据的条目（去重 535 个
  全局题号）用 LLM 逐题生成参考解法 + 测试数据，目录 `tests/<bucket>/<题号>_made/`。
  模版草案 `tools/make_data_template.py` 已就位（内置样例自检闸门）。完整规格与我的
  复核标准见 `NOTES-claude.md` 2026-07-24 条。
- **改了哪些文件**：`collab/PLAN.md`, `collab/NOTES-claude.md`, `tools/make_data_template.py`
- **关联提交**：见 git log
- **验证**：`python3 tools/handoff.py --verify` 通过（模版文件在 py_compile 覆盖内）
- **请重点看**：① **两个前置阻塞**：真实 tests 树在本克隆缺失，人需先恢复；人提过要给
  自己的生成模版，若有则替换我的草案——两者就绪前不要开工生成。②「恢复 tests 树之前
  严禁跑 `index_tests.py`」这条红字（会清空 945 条已索引数据）。③ 多解题必须跳过并列清单，
  不要硬生成。
- **红线自检**：判题沙箱未动 ✅ ｜ 口令未入库 ✅ ｜ 路径防线未动 ✅（本轮纯文档 + 模版）
- **下一步建议**：Codex 认领 T-002 → 等两个前置就绪 → 先交 20 题试点批。

### 2026-07-24 · Claude → （人/Codex） · T-000

- **做了什么**：建立协作脚手架：`collab/` 五个文档 + `tools/handoff.py`（review 包生成器，
  自 Redmoon 的 `handoff.mjs` 移植为纯标准库 Python）。红线清单按本项目实际风险改写
  （判题沙箱、认证与口令、路径穿越、镜像数据不入库、上游代理、单文件极简风格）。
- **改了哪些文件**：`collab/README.md`, `collab/PLAN.md`, `collab/HANDOFF.md`,
  `collab/NOTES-claude.md`, `collab/NOTES-codex.md`, `tools/handoff.py`, `.gitignore`
- **关联提交**：见 git log
- **验证**：`python3 tools/handoff.py --verify` 通过（py_compile 全部源文件 + node --check app.js）；
  `--stdout` 试跑生成完整 review 包。
- **请重点看**：README 里的六条红线是否概括准确；`handoff.py` 的 range 推断逻辑
  （未提交改动 → diff HEAD；干净 → HEAD~1..HEAD）。
- **红线自检**：判题沙箱未动 ✅ ｜ 口令未入库 ✅ ｜ 路径防线未动 ✅
- **下一步建议**：认领 T-001 建测试套件，让交接闸门从「语法能编译」升级为「行为有仲裁」。
