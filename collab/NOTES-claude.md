# NOTES · Claude → Codex

> Claude 留给 Codex 的话：我改了什么、哪里没把握、想让你重点看哪里。
> 只有 Claude 写这个文件；Codex 的回话写在 `NOTES-codex.md`。
> 保持简短，过期内容可清理——真正的历史在 git 和 `HANDOFF.md` 里。

---

## 2026-07-24 · T-002 任务书：LLM 生成缺失测试数据（Codex 实现，Claude 复核）

### 背景与目标

项目本意：把 cs101.openjudge.cn 现代化，提供「编写 → 提交 → 反馈错在哪组数据」的
完整闭环。判题闭环已通（`judge.py` 会报 `case: N`），瓶颈是数据覆盖：catalog 1863 个
条目中 918 个 `test_cases` 为空（按去重全局题号 535 个）。目标：给这些题目生成
可信的测试数据，目录命名 `<题号>_made` 标记出处。

### 现场事实（开工前必读，2026-07-24 二次勘查后更新）

1. tests 树已恢复到 `data/openjudge/tests/`，**但缺 `20000-29982` 这个桶**：catalog 里
   有 **2236 条**测试引用指向它，当前全部指向不存在的文件——这些题目现在提交判题
   会在读 `.in` 时崩掉。→ 等人补齐这个桶；**补齐前仍然禁跑 `index_tests.py`**
   （会把这 2236 条从 catalog 里清掉）。其余六个桶引用文件全部在盘上（缺失数=0，已核）。
2. **人的模版与工作流已到位，以它为准**（我此前的 `tools/make_data_template.py` 已删）。
   人的流程：`data/openjudge/producecase_prompt/producecase_<题号>[_made].md` 是单题
   prompt（含题面 + `producecase_template.py` 模版 + 一份能 AC 的 `ac.py`）→ LLM 产出
   `producecase.py` → 在 `tests/<bucket>/<题号>_made/` 目录里运行生成数据。
   已有实物样板：`tests/4000-8210/4102_made/`（`producecase.py` + `samplecode.py` +
   `data/*.in|*.out`）。**产物目录布局照这个样板来**，保持全库一致。
3. **已生成的 `4102_made`、`18250_made` 目前并没有生效**（catalog 里 `test_count=0`）：
   producecase.py 往 `data/` 子目录写，而 `index_tests.py` 只 glob 目录顶层。
   → T-002 范围内修索引器：`directory.glob("*.in")` 改为同时收子目录
   （如 `glob("*.in") + glob("data/*.in")`），让人已有的两个目录原样生效，不搬文件。
4. 缺数据题目清单以 **catalog.json 中 `test_cases == []`** 为准，开工时重新导出
   （catalog 当前 945 有/918 无，按去重全局题号 466/535；人早前说 818/1045，
   以机器导出为准，差异在首批报告里说明）。
5. 题面在 `data/openjudge/pages/<book>__<id>.html`，结构干净：
   `<dt>描述/输入/输出/样例输入/样例输出</dt><dd><pre>…</pre></dd>`。
   **注意本地 id 后缀数字 ≠ 页面里的「全局题号」**（例：`pctbook/E03406` 页面标
   全局题号 2407）；`index_tests.py` 按**本地 id 尾部数字**匹配目录名，建目录用这个数字。
6. `index_tests.py` 的目录正则是 `(\d+)`，`4102_made` 天然被索引成 4102。bucket 是
   固定集合，若题号落在缝隙里（3683-3999、8211-9999、19964-19999），需扩 `BUCKETS`
   ——扩了要在交接里说明。

### 工作方式

- 每题产出三样，全部入 `tests/<bucket>/<题号>_made/`：`samplecode.py`（能 AC 的参考
  解法）、`producecase.py`（数据生成器，内嵌同款 solve 逻辑）、`data/NN.in|NN.out`。
  同时把组装好的 prompt 存进 `producecase_prompt/producecase_<题号>_made.md`
  （沿用人的命名），保持人已建立的出处链完整。已有 37 份 prompt 的题目优先用人写的。
- **两条纪律并进 producecase.py（人的模版里没有，是我加的复核门槛）**：
  ① 固定随机种子（建议 `random.seed(<题号>)`），数据必须可复现；
  ② 生成前先断言 solve() 复现**题面样例**（原样复制，一字不改），断言失败不许落盘。
- **只给没有真实数据的题目生成**；一题多库（同一题号出现在多个 book）只生成一份。
- **多解题不生成**：本地判题是 token 精确比对，构造题/任意解/浮点题会误判 WA。
  识别出来就跳过，题号进「需 special judge」清单，留给后续任务。
- 数据规模守住判题限制：单组 CPU 4s、输出 ≤ 2MiB；组数参考人的模版（~20 组）即可，
  注意题面自带的时限（很多是 1000ms，别生成只有 4s 才跑得完的规模）。
- **分批**：先 20 题试点 → 交我复核 → 通过后按 ~100 题/批放量，每批交接一次。
  每批报告：生成数（题号列表）、跳过数及原因分类、样例自检全过的汇总输出。
- 20000 桶补齐后、每批合入后：跑 `scripts/index_tests.py`，报告前后计数。

### 我的复核标准（先说清，免得返工）

1. 抽样读题面 vs `solve()`：算法是否真的解这道题（这是唯一无法机器化的部分，
   我会重点花时间在这里）；
2. 复跑 `make_data.py`：可复现（固定种子）、样例断言真的在跑；
3. 数据形状：有最小/最大边界组、规模不超判题限制（CPU 4s / 输出 2MiB）；
4. 用 `judge.py` 真判：拿参考解法当提交，走一遍真实判题路径拿到 Accepted；
   再故意改错一行，确认能拿到 WA 且 `case` 指对组号（反馈闭环是本项目的本意）；
5. 「需 special judge」清单抽查：是否真的多解，还是偷懒漏做。

---

## 2026-07-24 · T-000 脚手架落地

- 脚手架整体形状照搬 Redmoon/collab（那边跑了 50+ 任务、两轮角色对调，流程被验证过）。
  按本项目做的适配：`handoff.mjs` → `handoff.py`（这里没有 npm）；`npm test` 闸门 →
  `--verify` + 冒烟（这里还没有测试，见 PLAN T-001）；红线从「服务端权威/协议版本」
  换成「判题沙箱/认证口令/路径穿越」。
- **哪里没把握**：README 红线第 5 条（上游代理）是我从 `server.py:151-168` 读出来的
  ——目前回源确实只在 do_GET 的兜底路径上，且没有转发本地 Cookie。如果你审查时
  发现回源会带任何请求头之外的东西，这条红线要改写。
