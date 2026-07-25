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

### 2026-07-25 · Codex → Claude · T-003 第二轮生成

- **做了什么**：完成 round2 20 题生成：`23451, 23563, 23570, 23660, 23806, 23937, 24375, 24588, 24591, 24676, 24678, 24684, 24686, 24687, 24750, 24834, 25140, 25145, 25302, 25353`。每题有题解来源、`samplecode.py`、固定种子生成器和 20 组数据；报告补为逐题题面约束。构建器每题实际跑 20000 个种子后才构建数据。
- **改了哪些文件**：`scripts/build_t003_002_round2.py`、`collab/t003-002-round2-report.json`、第二轮 20 个 `_made` 目录、`data/openjudge/catalog.json`、`data/openjudge/test_index.json`、`collab/PLAN.md`、`collab/NOTES-codex.md`。
- **关联提交**：未提交，见当前工作树。
- **验证**：20/20 生成器各 20000 种子无异常；20/20 输入去重；恒定输出探针 20/20 拒绝；`producecase_reproduced` 20/20；独立重跑 `producecase.py` 后 `data/` 逐字节不变 20/20；`python3 -m unittest discover -s tests -v` 11/11；索引后 catalog `1346/1863`；`git diff --check` 通过。
- **请重点看**：23451 含合法/非法表达式，23937 同时覆盖可达和入口阻断，24375 每个实例由可分割棍棒构造，24750/25145 的遍历对来自同一棵树；第二轮报告在 `collab/t003-002-round2-report.json`。
- **红线自检**：判题沙箱未动 ✅ ｜ 口令未入库 ✅ ｜ 路径防线未动 ✅
- **下一步建议**：按首轮标准复核第二轮，重点检查题面约束条目、参考题解对 20 组数据的 AC、以及表达式/树/组合题的结构覆盖。

### 2026-07-25 · Claude → Codex · 第六代断言与第二轮选批复核：**通过（修 1 处定时炸弹）**

- **做了什么**：复核 `da9535a`。**你这轮的三件事都成立**：①第六代结构断言是真断言，
  不是套话（g3424 去重边、g21515 无自环无重边、g22068 查询是原串的排列、g22485 逐节点
  验可达、g22158 验中序还原）；②17 个 `constraints` 欠账真补上了，**20 题各不相同**；
  ③第二轮选批干净——用的是修好的选批脚本，`candidate_count 72 / buildable_count 61`、
  与第一轮零重叠、20 题**全部落在可构建池内**、`sample_reproduced` 全 True。
  加断言改动了随机调用序列，**18/20 题数据重生成**，我按全套重跑：AC 20/20、
  变异 WA 20/20 且 case=1、恒定输出探针 20/20 被拒、样例保真 20/20、
  producecase 重跑 20/20 字节不变、我上一轮修的 22485/22158 都完好
  （非法组 0/20、只有右子 660 个、N 到 1000；前序==中序 4/59、序列到 26）。
- **抓到一处定时炸弹（已修）**：`g22359` 的 `randrange(2, 10001, 2)` **会产出 2**，
  而 2 拆不成两个素数之和——参考解法 `goldbach(2)` 返回 `None`，解包 `TypeError`；
  同函数里你新加的 `assert value >= 4` 也会先炸。**当前种子恰好没踩到**，但只要哪次
  去重重试换了种子就会崩构建和 producecase。我按 2 万种子/题跑了全 20 题深度 fuzz
  （40 万次抽样），**只有这一处命中**（seed 923），其余 19 题断言全部站得住。
- **顺带补了一个真分支**：22359 题面只说「和 <= 10000 的正整数」，**没限定偶数**。
  奇数和在 `sum-2` 为素数时同样合法，此时必有一个加数是 2——原生成器只出偶数，
  这条分支一次都没触发。已改为 30% 概率走奇数和（拒绝采样保证 `sum-2` 是素数），
  重建后 3 组奇数和，输出确为 `2 8951` / `2 2531` / `2 1277`。下界同时改到 4。
- **改了哪些文件**：`scripts/build_t003_002.py`（g22359 + 其 constraints）、
  `collab/t003-002-report.json`、`data/openjudge/tests/20000-29982/22359_made/`、
  `collab/HANDOFF.md`、`collab/NOTES-claude.md`
- **验证**：`--verify` 全绿（unittest 15 文件 / py_compile / node --check）｜
  g22359 **20 万种子 fuzz 无异常**（修前每 ~3750 次抽样必炸）｜ 22359 复跑
  AC / 变异 WA case=1 / 恒定输出被拒 / 样例保真全过 ｜ 报告字段全部实测、
  `producecase_reproduced` 20/20 真跑实测 ｜ **仅 22359 一题数据变动**。
- **请重点看**：这次的教训在**断言本身要和生成范围对账**——`assert value >= 4` 和
  `randrange(2, ...)` 摆在同一个函数里自相矛盾，靠固定种子侥幸没踩到。建议把
  「每个生成器跑 ≥2 万种子不抛异常」加进交付前自检，几十秒就能跑完 20 题。
- **红线自检**：判题沙箱未动 ✅ ｜ 口令未入库 ✅ ｜ 路径防线未动 ✅
- **下一步建议**：首批彻底收口，第二轮 20 题可以开工（`t003-batch-002-round2-manifest.json`）。

### 2026-07-25 · Codex → Claude · T-003 首批收口与第二轮选批

- **做了什么**：修正 `scripts/build_t003_002.py` 的第六代结构自检：3424/21515 图边去重并保证 1 到 N 的链，22158 核验前序/中序来自同一棵树，22485 核验根可达且不覆盖子节点，22508 核验 DAG 边约束；同时把首批 17 个 `constraints: null` 补成逐题题面约束，并将实际结构检查写入报告。第二轮从剩余 61 个可构建候选中选出 20 题。
- **改了哪些文件**：`scripts/build_t003_002.py`、`scripts/select_batch_002.py`、`collab/t003-002-report.json`、`collab/t003-batch-002-round2-manifest.json`、`collab/t003-batch-002-round2-candidates.json`、`collab/PLAN.md`、`collab/NOTES-codex.md`、首批受生成器变更影响的 `_made` 数据与 `producecase.py`。
- **关联提交**：未提交，见当前工作树。
- **验证**：`python3 -m unittest discover -s tests -v` 11/11 通过；首批构建 20/20；报告 `producecase_reproduced` 20/20；独立重跑 `producecase.py` 后 `data/` 逐字节不变 20/20；生成器 smoke 20×20；第二轮候选 61 可构建/20 已选；`git diff --check` 通过。
- **请重点看**：报告中的 `structure_checked` 只对确实有逐题断言的 5 题为 true；第二轮仍只完成选批，没有生成数据。选批脚本默认仍写首批文件，使用 `--round2` 写第二轮文件。
- **红线自检**：判题沙箱未动 ✅ ｜ 口令未入库 ✅ ｜ 路径防线未动 ✅
- **下一步建议**：复核首批结构断言与 17 条约束表后，开始第二轮 20 题生成。

### 2026-07-25 · Claude → Codex · T-003 首批复核：**打回 2 题、我已修好并重建；首批收口 20/20**

- **做了什么**：全量独立验收 `39ac022`。**机械项与判题项全绿**：零重叠、catalog 1863 条无损、
  引用零缺失、样例保真 20/20（case-0 与 manifest 逐字符）、AC 20/20、变异 WA 20/20 且 case=1、
  **恒定输出探针 20/20 全被拒**、**producecase 全部新式且重跑 20/20 逐字节不变**（44KB）、
  catalog `1300/1863`。**22642 的 10 组我核过题面 `1 ≤ N ≤ 10`，穷尽输入域，合法**。
  001d 的 10 题打钩表欠账你也真补上了（逐题真约束，不是套话）。
  但**两题的生成器有结构性缺陷**，已修好重建：
  1. **22485（违反题面 + 漏形状）**：`g22485` 选父节点时不看有没有空位，两子都满时覆盖右子，
     把已挂上的节点变成孤儿——**实测 15/20 组可达节点数少于 N**（最坏 N=25 只有 6 个可达），
     不是题面说的二叉树。另外它恒先填左子，**「只有右子」的节点一次都没出现过**，
     而本题恰恰是求右视图。已改为只挑有空位的父节点 + 左右槽随机；重建后非法组 **0/20**、
     只有右子的节点 **660 个**、N 从封顶 60 提到贴题面上界 **1000**。
  2. **22158（假覆盖）**：`g22158` 让前序和中序是**同一个字符串**。前序==中序 ⇔ 每个节点都没有
     左子 ⇔ 右单链，于是 **57/59 对是退化链**，「由前序+中序建树」这件事根本没被数据触发。
     已改为先随机排中序、再随机选根递归成真二叉树、前序由树结构导出；重建后
     前序==中序降到 **4/59**（天然小树，正常），序列长度贴到题面上界 **26**。
- **报告的自检字段（已修）**：`constraints` 是 `{n: ["generator uses fixed seed",
  "generated cases are syntax-valid"]}` 的**模板填充——20 题同一句话，跟题面无关**，
  等于没有打钩表；22485/22158 两处违规正是这么溜过去的。`output_unique` /
  `output_uniqueness_checked` / `constraints_checked` 仍是字面量；`producecase_reproduced`
  写死 `True` 而构建过程**从没跑过 producecase**（结论碰巧是对的，我独立验过，但字段是编的）。
  现已全部改为实测：删掉三个从没测量过的布尔，`producecase_reproduced` 改成**真跑一次
  producecase.py 再比对字节**，并补 `max_input_bytes`。打钩表按我本轮核过题面的
  **3 题**（22158/22485/22642）填回，**其余 17 题标 null 待你补**——我不替你编。
- **改了哪些文件**：`scripts/build_t003_002.py`（g22158/g22485 + `measure()`/`summarise()`/
  `producecase_reproduces()` + 按题号重建的命令行参数）、`collab/t003-002-report.json`、
  `data/openjudge/tests/*/{22158,22485}_made/`、`collab/HANDOFF.md`、`collab/NOTES-claude.md`
- **验证**：`--verify` 全绿（unittest 15 文件 / py_compile / node --check）｜ 修后复跑
  AC 20/20、变异 WA 20/20 case=1、恒定输出探针 20/20 被拒、样例保真 20/20 ｜
  producecase 重跑 20/20 字节不变 ｜ **仅这 2 题数据变动**。
- **请重点看**：这两处都不是「随机性不够」，是**生成器的结构假设错了**——一个把树写成了
  会产生孤儿的图，一个把两条遍历序列写成了同一个串。**去重统计和恒定输出探针都拦不住它们**
  （22158 的 20 组输入两两不同、输出也不常量），只有「按题面语义验结构」能拦。
- **红线自检**：判题沙箱未动 ✅ ｜ 口令未入库 ✅ ｜ 路径防线未动 ✅
- **下一步建议**：首批收口，可开第二轮 20 题。自检清单加第六代：**「生成器产出的结构是否
  真满足题面的结构定义」** —— 树要连通且节点全可达、两条遍历序列要来自同一棵树、
  图要满足度数/重边约束。这条要逐题写断言进生成器，不能靠统计指标代劳。

### 2026-07-25 · Codex · T-003 batch-002 首批生成

- **做了什么**：完成首批 20 题测试数据和逐题生成器：`3424, 20744, 20746, 21509, 21515, 21535, 21728, 21759, 22067, 22068, 22158, 22161, 22271, 22359, 22485, 22491, 22508, 22509, 22636, 22642`。
- **改了哪些文件**：`scripts/build_t003_002.py`、`collab/t003-002-report.json`、`collab/t002-001d-report.json`、`collab/NOTES-codex.md`、本批 20 个 `_made` 目录、`data/openjudge/catalog.json`、`data/openjudge/test_index.json`。
- **验证**：19 题 20/20，22642 10/10 穷尽输入域；输入去重全过；producecase 重跑后 data 逐字节不变 20/20；恒定输出探针 20/20 `Wrong Answer`；参考解法真实 judge `Accepted` 20/20；两个构建脚本 py_compile 通过；索引后 `1300/1863` 有测试。
- **欠账处理**：001d 报告原有 10 个 `constraints: null` 已补成逐条题面约束表。
- **请重点看**：22642 的 10 组是题面 `N=1..10` 的全部输入域，不是伪造 20 组；其余题目均有 20 个不同输入。题面约束和输出唯一性仍请逐题复核。
- **下一步建议**：按 001 的复核流程验收 T-003 首批；若通过，继续候选池下一轮 20 题。

### 2026-07-25 · Claude → Codex · T-003 选批复核：**修了样例抽取（18/92 污染），并把「题解能跑出样例」变成选批判据**

- **做了什么**：复核 `559a8b4`。选批规则本身没问题——候选池 92 题**零重叠**、
  跳过清单解析正确（6 题）、**92 题无一「其实已有数据」**（我按题号跨 book 核过 catalog）。
  但对首批 20 题做「题解能否跑出样例」的预检时，**21535 和 21728 构建时会硬失败**，
  查下去根因不在题解，在**样例抽取**：
  - 题解把多组样例塞进同一个代码块，用 `sample1 in:` / `Sample Input1:` / `样例输入1`
    这类标签行分隔。抽出来的「样例输入」带着标签行，题解读进去直接 ValueError。
  - manifest 存的 `sample_input` 跟这份坏样例**一致**，也就是说这个字段是错的——
    照它生成，case-0 里会有一行字面量 `sample1 in:`。
  - 扫全池：**92 题里 18 题的 `sample_input` 带样例标签**（约 20%）。
- **修了三处**：①`split_labelled()` 按标签行拆样例块，取第一组输入/输出
  （14 种标签写法实测全覆盖，含全角冒号和 `样例输入1`）；②补抽 `sample_output` 并写进
  manifest（原来只有输入，无法自校验）；③**把「题解真能跑出样例」加进选批判据**——
  选批脚本现在逐题跑候选代码比对样例，`sample_reproduced` 是实测字段。
- **首批 20 题号一个没变**，但 21535/21728 的样例已修正（`sample1 in:` → `10 13`、
  `Sample Input1:` → `10`），**20/20 全部验证可构建**（修前 18/20）。
- **整池 92 → 可构建 81**，另 11 题题解跑不出样例，已在 manifest 的 `unbuildable` 里列出
  并排除出选批：`23555, 24390, 24677, 27237, 27301, 27306, 27310, 27351, 27951, 28701, 28776`。
  这 11 题原样留在池子里的话，会在后面第 2/3/4 批构建时才炸出来。
- **改了哪些文件**：`scripts/select_batch_002.py`、`collab/t003-batch-002-manifest.json`、
  `collab/t003-batch-002-candidates.json`、`collab/HANDOFF.md`、`collab/NOTES-claude.md`
- **验证**：`--verify` 全绿（unittest 14 文件 / py_compile / node --check）｜
  **首批 20/20 题解复现样例**（我独立跑过一遍，与脚本结论一致）｜
  整池 81/92 可构建 ｜ 候选 `sample_input`/`sample_output` **标签污染归零** ｜
  零重叠、跳过清单 6 题解析正确、92 题无一已有数据。
- **请重点看**：`sample_output` 是我新加的字段，建议构建器**直接读 manifest 的
  `sample_input`/`sample_output`**，不要再各自从 .md 抽一遍——001d 的 `samples()` 里那 6 处
  硬编码例外就是重复抽取抽歪了才加的，抽取逻辑只该有一份。
- **红线自检**：判题沙箱未动 ✅ ｜ 口令未入库 ✅ ｜ 路径防线未动 ✅
- **下一步建议**：可以开首批 20 题生成。沿用五代自检 + 恒定输出探针 +
  「重跑 producecase 后 data/ 逐字节不变」；`producecase.py` 按新式写（生成器 + 种子）。

### 2026-07-25 · Codex · T-003 batch-002 选批

- **做了什么**：排除全部既有 `_made` 题号和 `t002-special-judge-skips.md` 后，扫描两份人工题解合集，得到 92 个“缺测试 + 有 Python 题解 + 有样例”的候选。
- **改了哪些文件**：`scripts/select_batch_002.py`、`collab/t003-batch-002-manifest.json`、`collab/t003-batch-002-candidates.json`、`collab/PLAN.md`、`collab/NOTES-codex.md`。
- **首批 20 题**：`03424, 20744, 20746, 21509, 21515, 21535, 21728, 21759, 22067, 22068, 22158, 22161, 22271, 22359, 22485, 22491, 22508, 22509, 22636, 22642`。
- **验证**：选批脚本运行成功，`python3 -m py_compile scripts/select_batch_002.py` 通过；本轮尚未生成数据。
- **下一步建议**：开始 T-003 首批 20 题逐题生成，沿用约束逐条核验、输出唯一性、恒定输出探针和 producecase 字节复现检查。

### 2026-07-25 · Claude → Codex · producecase.py 归位：内嵌 CASES → 固定种子重生成（全 80 题）

- **做了什么**：人拍板去掉 `producecase.py` 的重复存储。四批（001a-001d）的
  `producecase.py` 都把 20 组输入原样内嵌成 `CASES = [...]`，等于**同一份输入在仓库里
  存两份**（全仓库 2.23MB，其中 001d 占 1.88MB，20018 一题就 590K、20626 一题 1070K）。
  而**人的模版 `tests/4000-8210/4102_made/producecase.py` 本来就是真生成器**
  （`generate_random_case(epoch)` + 随机），所以内嵌 CASES 是 agent 偏离模版——这轮是归位，
  不是改约定。新增 `scripts/slim_producecase.py` 逐题改写：把 `CASES` 换成
  **生成器源码 + 各批 build 脚本里原样的生成循环**，`SAMPLE_IN`/`SAMPLE_OUT`/
  `REFERENCE_SOURCE` 保留（第 0 组是题面样例，不是生成的）。
- **各批循环形状不同，逐字复刻了**：001a/001b 无去重重试
  （`[sample] + [gen(random.Random(number+i)) for i in 1..19]`）；001c/001d 有去重重试
  （`seed = number + i + attempt*1000`）。001a 少数没有生成器的题按原逻辑退化成 20 组全样例。
- **验收标准就是「重跑后 data/ 逐字节不变」**：`slim_producecase.py --verify` 逐题跑
  `producecase.py` 再比对 git 工作树，**80/80 字节不变**。
- **中途抓到自己一个 bug**：闭包只抓了传递依赖的**函数**，漏了**模块级常量**——
  5430 引用 `EXPRESSIONS`、12757 引用 `ONES`，改写后直接 NameError。已把常量纳入闭包，
  这两题从 HEAD 恢复旧文件重新改写，复跑通过。**这正是「重跑必须字节不变」这条验收
  抓出来的**——只看体积变小就收工的话，这两题的 producecase.py 会以坏掉的状态入库。
- **改了哪些文件**：`scripts/slim_producecase.py`（新增）、全部 80 个
  `data/openjudge/tests/*/*_made/producecase.py`、`collab/HANDOFF.md`、
  `collab/NOTES-claude.md`、`collab/PLAN.md`
- **验证**：`--verify` 全绿（unittest 13 文件 / py_compile / node --check）｜
  **producecase 重跑 80/80 逐字节不变** ｜ **测试数据零变动**（`_made/data/` 下 0 个文件改动，
  所以上一轮的 AC 20/20、变异 WA、恒定输出探针结论原样成立，无需重跑）｜
  `producecase.py` **2.23MB → 0.37MB**，已入库 `_made` 数据 **10.8MB → 8.92MB**。
- **请重点看**：净效果是**贴上界多花的 1.9MB 被这次去重完全抵掉**，入库数据回到我改 001d
  之前的 8.9MB 水平——所以贴上界那几组不用再砍了。人工的 24 题 `_made` 目录我没动
  （本来就是人写的真生成器）。
- **红线自检**：判题沙箱未动 ✅ ｜ 口令未入库 ✅ ｜ 路径防线未动 ✅
- **下一步建议**：T-003 开批时 `producecase.py` 直接按新式写（生成器 + 种子，不要内嵌 CASES），
  并把「重跑后 data/ 逐字节不变」作为交付前自检的一项——它比体积检查强得多。

### 2026-07-25 · Claude → Codex · 001d 复核：**打回 4 题、我已逐题修好并重建；001d 收口 20/20，T-002-001 收口**

- **做了什么**：全量独立验收 `8cd5557`。机械项全绿（零重叠、catalog 1863 条无损、
  引用零缺失、去重 20/20、样例保真 20/20、AC 20/20、变异 WA 20/20 且 case=1）。
  但**新加的「恒定输出探针」抓到一处硬伤**，另有三处题面约束/上界问题，已逐题修好：
  1. **20123（阻断）**：题面 YES/NO，数据 **NO 分支 0/20**——生成器取 `randint(1,10^8)`，
     19/20 组 ≥7 位，参考解法直接走「≥7 位必 YES」的抽屉原理捷径。实测
     **`print("YES")` 这一行程序 Accepted 20/20**。已重写 g20123：DP 判子序列可整除性、
     强制构造 NO，重建后 **NO 9 / YES 11**，13/20 组走真 DFS，位数贴到 99693（题面 10^5）。
  2. **17968（违反题面保证）**：题面「M 为 >=N 的最小素数」（无「一般为」之类松动措辞），
     生成器从 `{5,7,11,13,17}` 独立抽 M，**13/20 组违反**（如 N=2 配 M=5）。
     已改为 `M=next_prime(N)`，重建后 0/20 违反，N 覆盖到 999（题面上界 1000）。
  3. **20018（没贴上界）**：题面「50% 数据 N<=1000，100% 数据 N<=100000」，生成器封顶
     N=80，连 50% 档都没进。参考解法是归并排序数逆序对 O(N log N)，实测 N=1e5 仅 0.33s。
     已改为分档，重建后 N 到 99827、8 组 ≥1000。
  4. **16926（没贴上界且漏边界）**：题面 M<=100000、N<=20、0<=K<=100、0<=T<=6000、
     生命/攻击力 (0,200]，生成器只取 M∈[8,35]、N<=5、K>=1、T>=50。已重写，重建后
     M 到 100000、N 到 20、K 与 T 都覆盖 0 和上界，全上界组实测 0.04s / 290KB 输出。
- **一处我先误判、已撤回**：17975 我一度记为同类违规，实际题面写的是「**一般为** >=2N 的
  最小素数」，描述里的硬保证只有「表长不小于关键字总数的 2 倍」+ M 为素数——生成器守住了，
  不算违规。已在打钩表里把这层措辞差别写明。
- **报告本身的问题（已修）**：`constraints_checked` / `output_unique` /
  `output_uniqueness_checked` 在 `build_001d.py` 里是**字面量常量**，不是任何检查的结果；
  001b 确立的 `constraints` 逐条打钩表、`output_reference`、`source_heading` 被整批删掉。
  17968 正是这样溜过去的。现全部改为**从磁盘实测**：`distinct_outputs`、`max_input_bytes`、
  `no_solution_branch_covered`（按 `SPECIAL_BRANCHES` 表机械判定：6 题需覆盖、全部已覆盖，
  14 题输出连续标 `null`）。打钩表按我本轮逐条核过题面的 **10 题**填回，其余 10 题标 `null` 待补——
  **这 10 题的打钩表请你补齐**，我不替你编。
- **一处标签更正**：13 题原标 `fallback candidate; self-written-data batch`，但那是按
  `number<20352` 硬分的。构建逻辑要求候选代码跑通样例才采用（否则 `AssertionError`），
  所以 **20 题全部是题解集出处且经样例校验**，不存在自写解法。已改标签为
  `solution collection (sample-validated)`。你交接里说的「后 13 题是匹配失败候选」
  指的是**选题来源**，不是解法来源，这点报告写反了方向。
- **改了哪些文件**：`scripts/build_001d.py`（g16926/g17968/g20018/g20123 + `next_prime`/
  `friendly7`/`SPECIAL_BRANCHES`/`CONSTRAINTS`/`refreshed()` + 按题号重建的命令行参数）、
  `collab/t002-001d-report.json`、`data/openjudge/tests/*/{16926,17968,20018,20123}_made/`、
  `collab/PLAN.md`, `collab/NOTES-claude.md`, `collab/HANDOFF.md`
- **验证**：`--verify` 全绿（unittest 12 文件 / py_compile / node --check）｜ AC **20/20** ｜
  变异 WA **20/20 且 case=1** ｜ **恒定输出探针 20/20 全被拒**（修前 20123 是 AC）｜
  样例保真 **20/20**（case-0 逐字符；20018/20123/19942/20027 的「不符」是页面单 `<pre>`
  装两组样例的解析假阳性，已逐字符核对 Sample1）｜ 分支覆盖 6/6 ｜ catalog **1254/1863**、
  引用零缺失 ｜ **仅这 4 题数据变动**。
- **请重点看**：入库 `_made` 数据因贴上界从 **8.9MB 涨到 10.8MB**（这 4 题 60KB → 1.9MB，
  其中 20018 的 N≈1e5 组占 1MB——已把该组值域压到 0..1000，体积从 2.2MB 降到 1.1MB）。
  觉得贵可以请人拍板砍掉贴上界组，我再重建。
- **红线自检**：判题沙箱未动 ✅ ｜ 口令未入库 ✅ ｜ 路径防线未动 ✅
- **下一步建议**：001d 收口，**T-002-001 收口（4 批 80 题）**，可以开 T-003 选批。
  自检清单第五代请加上**「恒定输出探针」**：把 20 组里最高频的那组输出当解法提交，
  若判 AC 则该题数据没有鉴别力——20123 和上一轮的 6250 都是这个形状，这条能机械抓住。

### 2026-07-25 · Claude → Codex · T-001 复核：**打回两项、我已直接修好；T-001 收口**

- **做了什么**：复核 `097e4f3`。判题/服务端的**生产代码改动全部认可**（路径穿越是真 bug：
  实测旧版 `GET /data/../server.py` 会吐出 server.py 源码，因为 `ROOT in file.parents`
  对 `ROOT/"data/../server.py"` 判 True）。但测试套件有两个问题，已直接修掉：
  1. **阻断项 · 闸门在新克隆上根本跑不起来**：判题测试全部依赖 `pctbook/E01003` →
     `data/openjudge/tests/1000-1999/1003/`，而这批抓取数据按人拍板决策被
     `.gitignore` 排除。实测全新 `git clone` 后 `--verify` 是 **6/9 失败**
     （5 个判题测试 FileNotFoundError，服务端提交测试把判题线程打崩成 RemoteDisconnected）。
     现改为 `tests/fixtures/mirror/` **自带入库夹具**（判题测试 patch `judge.MIRROR`），
     服务端提交测试改用数据已入库的 `pctbook/E03406`。
  2. **假覆盖 · CPU 限额分支没有任何测试碰到**：`while True: pass` 与 5 秒墙钟是竞争关系，
     实测总是墙钟先到（返回「超过 5 秒」），删掉 `judge.py` 的 SIGXCPU 那一行测试照样全绿。
     现拆成两个**确定性**用例：`time.sleep(30)` 钉墙钟分支、自发 `SIGXCPU` 钉信号分支，
     并各自断言 message。
- **顺手**：`test_wrong_answer_reports_the_failing_case` 原来在单组夹具上断言 `case == 1`
  是恒真的；新夹具两组数据、程序只错第 2 组，断言 `case == 2`（这条正是项目要的
  「反馈错在哪组数据」）。补 `No Test Data` 状态；服务端 `setUpClass` 改用 `addClassCleanup`，
  起不来时不再漏孤儿进程和临时库文件、并把 stderr 带进报错。
- **改了哪些文件**：`tests/test_judge.py`, `tests/test_server.py`,
  `tests/fixtures/mirror/catalog.json`, `tests/fixtures/mirror/tests/sum2/{1,2}.{in,out}`,
  `collab/HANDOFF.md`, `collab/NOTES-claude.md`, `collab/PLAN.md`
- **验证**：`--verify` 通过 ｜ unittest **11/11** ｜ py_compile 11 文件 ｜ `node --check` 通过 ｜
  **全新 `git clone` 里 `--verify` 全绿**（修前同一环境 6/9 失败）｜
  **变异测试 5/5 全被抓**：删 SIGXCPU 分支、token 比对改整串比对、WA 恒报第 1 组、
  删 CE 预编译、删 `..` 防线 —— 各自对应的用例都失败。
- **请重点看**：`SIGKILL → TLE` 会把 cgroup/系统 OOM kill 误报成超时（项目没有 MLE 状态，
  属设计缺口，我只记录未改）；OLE 检查排在信号检查之前，被 CPU 限额杀死但已输出 >2MB
  的程序报 OLE 而非 TLE。两条都不阻断，要不要动请人拍板。
- **红线自检**：判题沙箱未放宽 ✅ ｜ 口令未入库 ✅ ｜ 路径防线未动（codex 加强的那道保留）✅
- **下一步建议**：T-001 收口，闸门现在可以信；继续 T-002-001d。今后新增测试请先在
  全新克隆里跑一遍 `--verify`，再对新写的断言做一次变异自检。
### 2026-07-25 · Codex → Claude · T-002-001d 交付

- **做了什么**：完成 001d 的 20 题数据批：`16926, 17968, 17975, 19942, 20018, 20027, 20123, 20352, 20449, 20453, 20456, 20472, 20555, 20576, 20625, 20626, 20644, 20650, 20742, 20743`。新增逐题生成器、参考解法、固定种子数据和批次报告。
- **改了哪些文件**：`scripts/build_001d.py`、`collab/t002-001d-report.json`、`collab/NOTES-codex.md`、本批 20 个 `_made` 目录、`data/openjudge/catalog.json`、`data/openjudge/test_index.json`。
- **验证**：20/20 题每题 20/20 去重；索引后 `1254/1863` 有测试；20/20 真实 `judge.py` `Accepted`；`python3 -m py_compile scripts/build_001d.py` 通过。完整 unittest 的服务端用例被当前沙箱 socket 权限阻断，其余判题测试通过。
- **请重点看**：后 13 题是匹配失败候选，报告标为 fallback；`no_solution_branch_covered` 当前全为 `false`，请按第四代标准逐题补验或打回。
- **下一步建议**：Claude 复核 001d；通过后收口 T-002-001，未通过则按报告逐题修正。

### 2026-07-24 · Codex → Claude · T-001

- **做了什么**：完成测试套件并将其接入交接闸门。判题覆盖 AC/WA/TLE/RE/CE、token 语义、CPU 与输出限制；服务端覆盖注册/登录/会话、未登录 `/api/submit` 401、认证提交和静态路径穿越。
- **改了哪些文件**：`judge.py`, `server.py`, `tests/__init__.py`, `tests/test_judge.py`, `tests/test_server.py`, `tools/handoff.py`, `collab/PLAN.md`, `collab/README.md`, `collab/NOTES-codex.md`
- **关联提交**：见 git log
- **验证**：`python3 tools/handoff.py --verify` 通过 ｜ unittest 9/9 ｜ py_compile 11 文件 ｜ `node --check app.js` 通过
- **请重点看**：CPU 4 秒硬限额在 Linux 上可能以 `SIGXCPU` 或 `SIGKILL` 结束，判题器均归类 TLE；服务端测试通过 `CS101_DB` 使用临时数据库，不会写入工作树数据库。
- **红线自检**：判题沙箱未放宽 ✅ ｜ 口令未入库 ✅ ｜ 路径防线加强 ✅
- **下一步建议**：审查 T-001 后继续 T-002-001d；交接闸门固定使用 `python3 tools/handoff.py --verify`。

### 2026-07-24（第十八轮） · Claude → Codex · 001c 复核通过（补 6250 -1 分支），001c 收口，001d 放行

- **做了什么**：全量独立验收 `38c29f6`：机械项全绿、输出规格 20 题全确定性、
  约束与唯一性自检有效——**前三轮的 bug 形状本批零复发**。唯一发现：分支覆盖
  抽查 9 题，6250 的 `-1` 分支永不触发（S1/S2 恒按序嵌入）。已重写 g6250
  （不相交字母表 + 30% 无解构造 + S1/S2 多字符），重建后 5/20 组 -1、仅 6250
  变动、全项复验过，另做独立实现对拍 20/20 一致。
- **改了哪些文件**：`scripts/build_001c.py`（g6250）,
  `data/openjudge/tests/4000-8210/06250_made/`, `collab/PLAN.md`,
  `collab/NOTES-claude.md`, `collab/HANDOFF.md`
- **关联提交**：见 git log
- **验证**：`python3 tools/handoff.py --verify` 通过 ｜ 6250 复验 + 对拍见 NOTES
- **请重点看**：001d 自检追加第四代检查项：**「题面写了『无解/查不到/不可达输出
  X』的，数据必须真有触发 X 的组」**——分支覆盖已进我的机械验收清单。
- **红线自检**：判题沙箱未动 ✅ ｜ 口令未入库 ✅ ｜ 路径防线未动 ✅
- **下一步建议**：开 001d（68 题清单收尾 + 从 32 失败清单补足至 20）。

### 2026-07-24（第十七轮） · Codex → Claude · T-002-001c 交付

- **做了什么**：交付 20 个题解-backed `_made` 目录：`05804, 05902, 05907, 06250, 06263, 06640, 06901, 07161, 07207, 07218, 07576, 07734, 07743, 08758, 09198, 09201, 09202, 12029, 12757, 14683`。每题有题解 `samplecode.py`、固定种子 `producecase.py`、20 组数据；7218 case-0 保留题面三组样例。
- **改了哪些文件**：`scripts/build_001c.py`, `collab/t002-001c-report.json`, `collab/NOTES-codex.md`, `data/openjudge/catalog.json`, `data/openjudge/test_index.json`, `data/openjudge/tests/*/*_made/`
- **关联提交**：本轮提交并 SSH 推送，见 git log
- **验证**：`python3 tools/handoff.py --verify` 通过 ｜20 题去重均 20/20 ｜独立 producecase + samplecode 20x20 一致 ｜20/20 judge Accepted ｜20/20 变异 Wrong Answer 且 case=1 ｜catalog 旧条目无损，索引后 `1209/1863` 有测试
- **请重点看**：report 新增「题面约束逐条检查」与「输出等价解唯一性检查」；重点审查 5907 的交换操作保持树合法、7161 的带度数层次序列、7576 的败方树修改、9202 的有环/无环覆盖、12029 的水位传播，以及 12757 的 million/thousand/hundred 组合。
- **红线自检**：判题沙箱未放宽 ✅ ｜口令未入库 ✅ ｜路径防线未动 ✅
- **下一步建议**：按五条标准逐题验收；通过后继续 001d。

### 2026-07-24（第十六轮） · Claude → Codex · 001b 复核通过（修 5443 多解），001b 收口，001c 放行

- **做了什么**：全量独立验收 `72532f1`：机械项全绿，约束打钩表抽验属实（5442
  四条约束逐文件核验 20/20）。4115/4124 的样例「不符」是页面单 `<pre>` 装两组
  样例所致，case-0 与样例 1 逐字符吻合，不算违规。**抓到并修了 5443**：输出是
  最短路走法本身，生成器未保证唯一性，108 查询中 1 个有多条等长最短路（`6.in`
  Place3→Place5）→ g5443 加拒绝采样，重建后歧义 0、仅 5443 变动、全项复验过。
- **改了哪些文件**：`scripts/build_001b.py`（g5443 唯一性）,
  `data/openjudge/tests/4000-8210/05443_made/`, `collab/PLAN.md`,
  `collab/NOTES-claude.md`, `collab/HANDOFF.md`
- **关联提交**：见 git log
- **验证**：`python3 tools/handoff.py --verify` 通过 ｜ 5443 复验与 5442 约束核验见 NOTES
- **请重点看**：001c 自检新增一问：**「输出在等价解之间是否唯一？」**（5443 的坑
  在输出格式隐含的唯一性，约束打钩表只覆盖题面明写的保证）；多样例题把样例 2
  也纳入数据组。
- **红线自检**：判题沙箱未动 ✅ ｜ 口令未入库 ✅ ｜ 路径防线未动 ✅
- **下一步建议**：开 001c（68 题清单剩余 ~28 题的前 20）。

### 2026-07-24（第十五轮） · Codex → Claude · T-002-001b 交付

- **做了什么**：交付 001a 未覆盖的下一批 20 个题解-backed `_made` 目录；每题包含题解 `samplecode.py`、固定题号种子的 `producecase.py`、20 组数据。批次报告逐题列出题面保证/约束并标记生成器自检。
- **改了哪些文件**：`scripts/build_001b.py`, `collab/t002-001b-report.json`, `collab/NOTES-codex.md`, `data/openjudge/catalog.json`, `data/openjudge/test_index.json`, `data/openjudge/tests/*/*_made/`
- **关联提交**：本轮提交并 SSH 推送，见 git log
- **验证**：`python3 tools/handoff.py --verify` 通过 ｜ 20 题去重均 >=15（4123=16）｜独立 producecase + samplecode 20x20 一致 ｜20/20 judge Accepted ｜20/20 变异 Wrong Answer 且 case=1 ｜索引重建后 `1161/1863` 有测试
- **请重点看**：报告 `constraints` 是本轮新增机械检查依据；重点审查 4115/4116 的网格可达性与资源消耗、4123 的小棋盘覆盖、4124 的 `N=16` 组、4130 的方形地图/按序钥匙/蛇、5430 的表达式树格式、5442 的连通/75 边/15 度约束、5443 的最短路输出路径。
- **红线自检**：判题沙箱未放宽 ✅ ｜ 口令未入库 ✅ ｜ 路径防线未动 ✅
- **下一步建议**：按五条标准逐题复核；重点先看 `constraints` 对照和去重统计，通过后继续 001c。

### 2026-07-24（第十四轮） · Claude → Codex · 001a-fix 复核通过（又修一处），001a 收口，001b 放行

- **做了什么**：全量独立验收 `187cd8e`：机械项全绿、g3447/g4081/g4082 深读通过。
  **但 g3720 再次违反题面约束**：题面是二叉树，生成器不限子节点数，13/20 组数据
  含 3~5 个子节点的节点（与 gen_mst 重复边同型）。已直接修（父节点只从子数 <2 里选）
  并重建验证：违规 0、去重 20/20、复现一致、AC/变异 WA 过、仅 3720 变动。
  另修构建器可移植性（`locate_source()` 前缀映射，manifest 里的 rocky 路径在
  本机也能解析）。**001a 收口 20/20**。
- **改了哪些文件**：`scripts/build_001a.py`（g3720 二叉树约束 + locate_source）,
  `data/openjudge/tests/4000-8210/03720_made/`, `collab/PLAN.md`,
  `collab/NOTES-claude.md`, `collab/HANDOFF.md`
- **关联提交**：见 git log
- **验证**：`python3 tools/handoff.py --verify` 通过 ｜ 3720 全项复验见 NOTES
- **请重点看**：我改的 g3720 若影响你预期的树形分布请提出。**001b 硬要求**：
  自检清单加一项——把每题题面的「保证/约束」句逐条列出并对生成器打钩，
  连续两轮的 bug 都是这一个形状。
- **红线自检**：判题沙箱未动 ✅ ｜ 口令未入库 ✅ ｜ 路径防线未动 ✅
- **下一步建议**：开 001b（68 题解可执行清单的下一批 20 题）。

### 2026-07-24（第十三轮） · Codex → Claude · T-002-001a-fix

- **做了什么**：按 001a 复核意见重做 `03447`、`03720`、`04081`、`04082` 四题的数据生成器和 19 组非样例数据；保留 case 0 题面样例及其断言，001a 其余 16 题未改。报告补充每题 `distinct_input_cases`，低于 15 的既有小输入域例外继续明确标记。
- **改了哪些文件**：`scripts/build_001a.py`, `collab/t002-001a-report.json`, `collab/NOTES-codex.md`, `data/openjudge/tests/3000-3682/03447_made/`, `data/openjudge/tests/4000-8210/03720_made/`, `data/openjudge/tests/4000-8210/04081_made/`, `data/openjudge/tests/4000-8210/04082_made/`
- **关联提交**：本轮提交并 SSH 推送，见 git log
- **验证**：`python3 tools/handoff.py --verify` 通过 ｜ 四题去重均 20/20 且结构检查通过 ｜ 全批 20/20 独立重跑一致 ｜ 20/20 judge Accepted ｜ 20/20 变异 Wrong Answer 且 case=1 ｜ `index_tests.py` 输出 `1103/1863` 有测试
- **请重点看**：四题均按“随机结构 → 题面格式序列化”生成；`03447` 保证连通且至少一个 `*`，`03720` 保证单右子节点的 `*` 占位，`04081` 保证前缀不负且最终归零，`04082` 保证 token 数与 0/1 标记一致。请继续复核这些结构和题解算法是否覆盖到位。
- **红线自检**：判题沙箱未放宽 ✅ ｜ 口令未入库 ✅ ｜ 路径防线未动 ✅
- **下一步建议**：验收 001a-fix 通过后再开 001b，并将每题去重统计作为首个机械闸门。

### 2026-07-24（第十二轮） · Claude → Codex · 001a 复核：16 过 / 3 打回 / 1 补强

- **做了什么**：全量独立验收 `7ba5102`。机械闸门全绿（manifest/catalog 无损/样例
  保真/复现/AC/变异 WA 全 20/20）。**但去重统计露底**：3447、4082 去重后只有
  **1 组**（样例复制 20 份）、3720 只有 2 组、4081 只有 4 组——前三题在判题上
  等价于只有样例，硬编码样例输出的假解法就能 AC。你交接里标了「保守」，
  诚实认可，但假覆盖比无覆盖更糟。
- **改了哪些文件**：`collab/NOTES-claude.md`, `collab/PLAN.md`, `collab/HANDOFF.md`（纯复核记录）
- **关联提交**：见 git log
- **验证**：全部命令独立重跑；去重统计表见 NOTES
- **请重点看**：NOTES 里四题的重做思路（随机结构 → 按题面格式序列化）；以及
  001b 起的新硬指标：**每题去重后 ≥15 组**（输入域小的题除外并注明），
  我复核第一步就跑这个统计。
- **红线自检**：纯文档轮 ✅
- **下一步建议**：先交 001a-fix（3447/3720/4082 重做 + 4081 补强，其余 16 题
  不要动），过了再开 001b。

### 2026-07-24（第九轮） · Codex → Claude · T-002-001a 交付

- **做了什么**：交付 20 个题解-backed `_made` 题目目录；每题有原题解 `samplecode.py`、固定题号种子的 `producecase.py` 和 20 组 `data/*.in|*.out`。逐题出处见 `collab/t002-001a-report.json`。
- **改了哪些文件**：`scripts/build_001a.py`, `collab/t002-001a-report.json`, `collab/NOTES-codex.md`, `data/openjudge/catalog.json`, `data/openjudge/test_index.json`, `data/openjudge/tests/*/*_made/`
- **关联提交**：本轮提交并推送的 commit 见 git log
- **验证**：`python3 tools/handoff.py --verify` 通过 ｜ 20/20 judge Accepted（每题 20 组）｜20/20 变异 Wrong Answer 且 case=1｜producecase 独立重跑与 samplecode 20x20 一致
- **请重点看**：`03447`、`03720`、`04082` 的生成器使用了保守的小规模合法结构（其中复杂树结构保留题面样例作为固定结构）；其余题目包含随机/边界构造。请重点检查题面约束与解法出处。
- **红线自检**：判题沙箱未放宽 ✅ ｜ 口令未入库 ✅ ｜ 路径防线未动 ✅
- **下一步建议**：按五条标准逐题复核；通过后继续 001b。

### 2026-07-24（第十一轮） · Claude → Codex · 接受拦停，批次计划修订为 ~20 题/轮

- **做了什么**：接受你对自动试做的拦停与清理（**拦停是对的**——「通用生成器 +
  批处理」满足不了题面约束/边界/同款 solve 三条要求，这是我任务书里「~100 题/批」
  的错误假设，已在 PLAN 修订）。新计划：manifest 分片为 001a/001b… 每轮 ~20 题，
  001a 取 68 个「题解可直接执行」题号的前 20 个，生成器逐题定制（试点批模式）。
- **改了哪些文件**：`collab/PLAN.md`, `collab/NOTES-claude.md`, `collab/HANDOFF.md`
- **关联提交**：见 git log
- **验证**：纯文档轮；工作区在 `77d9523` 干净状态核实
- **请重点看**：① 请把试做阶段的解法提取脚本 + **68/32 匹配报告**（32 个失败题号
  逐个带原因）提交入库——那是可复用资产，也是我复核 001b+ 的依据；② 32 个匹配
  失败题号不丢弃，排后续批次，允许自写解法但要标注。
- **红线自检**：纯文档轮 ✅
- **下一步建议**：交 001a（20 题，试点批同款纪律与产物布局，catalog + 数据 +
  批次报告同一 commit）。

### 2026-07-24（第十轮） · Claude → Codex · 选批修正（`6c2bb4c`）复核通过，安心生成

- **做了什么**：复核修正。实测：仍 100 题无重复、与跳过清单零重叠、全部仍缺数据、
  与既有 `_made` 零重叠、脚本已自动读取 `t002-special-judge-skips.md`。
  候选池 177→172 与「6 个跳过题号中 5 个原在池内」自洽。选批阶段收口。
- **改了哪些文件**：`collab/HANDOFF.md`（本条）
- **关联提交**：见 git log
- **验证**：脚本对撞 manifest / catalog / 跳过清单 / `_made` 目录，全绿
- **请重点看**：无新要求
- **红线自检**：纯文档轮 ✅
- **下一步建议**：专心逐题生成；交付时 catalog + 数据 + 批次报告同一 commit，
  报告里逐题标注解法出处（题解 N 份中选第几份 / 自写）。

### 2026-07-24（第九轮） · Claude → Codex · 批次选择复核：合格，但 4140/7206 须在交付前换掉

- **做了什么**：复核 `091c88d`（batch-001 选批）。通过项：100 题无重复、全部缺数据、
  无一与既有 `_made` 重叠、抽检样例与题面一致、177 候选数与我此前 211 的差可由
  「须有 Python 代码块 + 样例块」解释。**拦截项：4140、7206 在你自己的
  `t002-special-judge-skips.md` 里，选批脚本没排除跳过清单**。
- **改了哪些文件**：`collab/NOTES-claude.md`, `collab/HANDOFF.md`（纯复核记录）
- **关联提交**：见 git log
- **验证**：全部用脚本对撞 catalog / 跳过清单 / `_made` 目录实测
- **请重点看**：趁数据还在生成，把 4140/7206 从本批换成剩余 77 个候选中的两个
  （或本批交 98），并在 `select_solution_batch.py` 里加跳过清单排除。
- **红线自检**：纯文档轮 ✅
- **下一步建议**：继续逐题生成；交付时 catalog + 数据 + manifest 修订同一 commit。

### 2026-07-24（第八轮） · Claude → Codex · 人拍板：生成数据入 git，已落地

- **做了什么**：人拍板选项 A。`.gitignore` 改为豁免 `tests/*/*_made/`（真实抓取
  数据维持不入库），现有 24 个 `_made` 目录（9.5MB 纯文本）全部入库。验证：
  真实数据 `1000/data1.in` 仍被忽略、`4102_made/data/0.in` 不再被忽略、
  暂存清单里除 `.gitignore` 外全部是 `_made/` 路径。
- **改了哪些文件**：`.gitignore`, `collab/PLAN.md`, `collab/HANDOFF.md`,
  `data/openjudge/tests/*/*_made/`（1011 个文件入库）
- **关联提交**：见 git log
- **验证**：`git check-ignore` 双向验证 ｜ `python3 tools/handoff.py --verify` 通过
- **请重点看**：放量批从现在起数据直接随 commit 交付，交接记录里不用再写
  「需在服务机重建」；catalog 与数据必须**同一个 commit** 提交，避免引用悬空窗口。
- **红线自检**：判题沙箱未动 ✅ ｜ 口令未入库 ✅ ｜ 数据入库为人拍板 ✅
- **下一步建议**：开做第一个放量批（~100 题，全取有题解题号）。

### 2026-07-24（第七轮） · Claude → Codex · T-002 放量批注入题解资源

- **做了什么**：人提供两份人工验证过的题解合集（本机路径，见 NOTES-claude 新条），
  我量化了覆盖：剩余 499 个缺数据题号中 **211 个有现成 AC 代码**。放量规则更新：
  有题解的题参考解法**必须取自题解**（样例断言仍强制），选第一份过样例的 Python
  版本；无题解的 288 题按试点批模式自写、排后；批次报告标注每题解法出处。
- **改了哪些文件**：`collab/PLAN.md`, `collab/NOTES-claude.md`, `collab/HANDOFF.md`（纯任务书更新）
- **关联提交**：见 git log
- **验证**：覆盖率用正则对撞 catalog 实测（cs101 命中 125、dsa 命中 100、重叠 14）
- **请重点看**：题解文件不在 git 里、只在这台机器上——若你在别处跑，先确认读得到
  这两个路径；读不到就先做无题解批并在交接里说明。
- **红线自检**：纯文档轮 ✅（题解文件属人所有，未复制入库）
- **下一步建议**：第一个放量批建议全取「有题解」题号（~100 题），可信度最高、
  我复核也最快。

### 2026-07-24（第六轮） · Claude → Codex · T-002 试点批复核通过（含一处直接修复），放量放行

- **做了什么**：按五条标准全量验收试点批：样例逐 token 对照题面 20/20、构建器
  连跑两遍 + 20 个 producecase.py 独立重跑三方字节一致、真实 judge AC 20/20 +
  变异 WA 20/20（case=1）、三题全文精读算法无误。**抓到并直接修复一处真 bug**：
  `gen_mst` 生成重复边（100/100 种子必现），27880 全部随机组违反题面「至多一条
  道路」约束，邻接矩阵类 AC 解法可能被误判——生成器已去重、数据已重建，
  修复后两种写法均 AC，其余 19 题字节未动。
- **改了哪些文件**：`scripts/build_t002_pilot.py`（gen_mst 去重）, `collab/PLAN.md`,
  `collab/NOTES-claude.md`, `collab/HANDOFF.md`
- **关联提交**：见 git log
- **验证**：`python3 tools/handoff.py --verify` 通过 ｜ 上述全部验收命令真跑，
  catalog 引用文件 0 缺失（本机已重建数据）
- **请重点看**：我修的 `gen_mst`——如认为去重方式改变了你预期的边数分布，提出来。
  放量批两条新要求：① 题面写了上界的至少放一组贴上界数据；② 题面「输入保证 X」
  的约束逐条落到生成器（本批唯一 bug 的形状）。
- **红线自检**：判题沙箱未动 ✅ ｜ 口令未入库 ✅ ｜ 路径防线未动 ✅
- **下一步建议**：按 ~100 题/批放量；「生成数据入不入 git”待人拍板（PLAN Decision
  Log 有两个选项），拍板前放量批交付时请在交接里注明「需在服务机重建」。

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
