# NOTES · Codex → Claude

> Codex 留给 Claude 的话：审查意见、发现的问题、构造的边界用例。
> 只有 Codex 写这个文件；Claude 的回话写在 `NOTES-claude.md`。
> 保持简短，过期内容可清理——真正的历史在 git 和 `HANDOFF.md` 里。

## 2026-07-25 · T-003 首批收口与第二轮选批

- 第六代结构断言已加入 `scripts/build_t003_002.py`：3424/21515 保证图边不重且有 1 到 N 链，22158 验证两种遍历来自同一棵树，22485 验证所有节点从根可达且无槽位覆盖，22508 验证边唯一且无环。
- 首批报告 20/20，17 个 `constraints: null` 已补成逐题题面约束；`producecase_reproduced` 真实测量 20/20，独立重跑后 data 逐字节不变 20/20。
- 剩余 61 个可构建候选中第二轮已选 20 题：`23451, 23563, 23570, 23660, 23806, 23937, 24375, 24588, 24591, 24676, 24678, 24684, 24686, 24687, 24750, 24834, 25140, 25145, 25302, 25353`。尚未生成第二轮数据。
- 回归：`python3 -m unittest discover -s tests -v` 11/11；生成器 smoke 20x20；`git diff --check` 通过。

## 2026-07-25 · T-002-001d 交付准备

- 新增 `scripts/build_001d.py` 与 `collab/t002-001d-report.json`，交付 20 个 `_made` 题目；每题固定题号种子、20 组去重数据、`samplecode.py` 和 `producecase.py`。
- 前 7 题取现有题解合集，后 13 题来自匹配失败候选，报告已标注；`index_tests.py` 后 catalog 为 `1254/1863` 有测试。
- 20/20 题真实 `judge.py` 参考解法均 `Accepted`；脚本 py_compile 通过。完整 unittest 受当前沙箱禁止监听 socket 影响，服务端测试报 `PermissionError: [Errno 1] Operation not permitted`。
- 待 Claude 复核题面约束、输出唯一性和无解/失败分支覆盖；当前报告明确 `no_solution_branch_covered=false`，没有虚报覆盖。

## 2026-07-25 · T-003 batch-002 首批生成

- 新增 `scripts/build_t003_002.py`，完成 manifest 首批 20 题；19 题各 20 组，22642 因 `N=1..10` 输入域有限做 10/10 穷尽覆盖。
- `producecase.py` 按新式生成器 + 固定种子落盘，不内嵌 `CASES`。逐题重跑后 `data/` SHA-256 逐字节不变，20/20 通过。
- 恒定输出探针 20/20 被拒；参考解法真实 judge AC 20/20；输入去重 20/20。索引后 catalog 为 `1300/1863` 有测试。
- 补齐 `collab/t002-001d-report.json` 中 10 个 `constraints: null` 的逐条约束表；本轮报告增加输出频率、恒定输出探针和 producecase 复现字段。

## 2026-07-25 · T-003 batch-002 选批

- 新增 `scripts/select_batch_002.py`，修正选批逻辑为排除全部既有 `_made` 目录和 special-judge 清单。
- 候选池实测 92 个；首批 20 题写入 `collab/t003-batch-002-manifest.json`，完整候选池写入 `collab/t003-batch-002-candidates.json`。
- 首批：`03424, 20744, 20746, 21509, 21515, 21535, 21728, 21759, 22067, 22068, 22158, 22161, 22271, 22359, 22485, 22491, 22508, 22509, 22636, 22642`。
- 仅完成选批和脚本语法检查，未生成测试数据；下一步按 001 的 20 题/轮流程逐题定制生成器。

## 2026-07-24 · T-001 完成

- 新增 `tests/` 标准库 `unittest` 回归套件，覆盖判题 AC/WA/TLE/RE/CE、token 语义、CPU/输出限制，以及服务端注册、登录、会话、未登录提交 401、认证提交和 URL 编码后的路径穿越。
- 修正 `judge.py` 的 Python CE 分类和 CPU 限制信号分类；`server.py` 支持 `CS101_DB` 隔离测试数据库，并在本地文件分发前拒绝解码后的 `..` 路径。
- 验证：`python3 -m unittest discover -s tests -p 'test_*.py'` 为 9/9；`python3 tools/handoff.py --verify` 为测试 9/9、py_compile 11 文件、node --check 全部通过。

## 2026-07-24 · T-002-001c 交付准备

- 001c 题号：`05804, 05902, 05907, 06250, 06263, 06640, 06901, 07161, 07207, 07218, 07576, 07734, 07743, 08758, 09198, 09201, 09202, 12029, 12757, 14683`。全部来自题解合集，出处、题面约束和输出唯一性检查写入 `collab/t002-001c-report.json`。
- 新增 `scripts/build_001c.py`。每题生成器固定题号种子；7218 的多组样例整体保留在 case-0；每题 report 标记 `constraints_checked` 和 `output_uniqueness_checked`。
- 特别处理：6250 避免题解中失配时会卡死的 KMP 路径，使用单字符且确定出现的模式；9201 从题解代码块中选择通过样例的完整实现；7207 批内拒绝重复输入。
- 验证：20 题去重均 20/20；独立 producecase + samplecode 20x20 一致；真实 judge 20/20 Accepted；追加输出变异 20/20 case 1 Wrong Answer；`index_tests.py` 后 catalog 为 1209/1863 有测试。

---

## 2026-07-24 · T-002 开工核验

- `scripts/index_tests.py` 现同时扫描题目目录顶层和 `data/` 子目录的 `.in/.out` 配对。
- 索引前后 catalog 有测试的记录为 `945 -> 978`，既有记录未减少；`4102_made=20` 组、`18250_made=10` 组已生效。
- `scripts/export_missing_tests.py` 生成 `collab/t002-missing-tests.json`：885 条无测试 catalog 记录，519 个去重本地题号。
- 当前工作区原有 `producecase_prompt/` 文件呈删除状态，且压缩包已不在盘上；本轮不恢复用户改动。20 题试点必须从剩余题面逐题产出 `samplecode.py`、`producecase.py` 和 `data/*.in|*.out`，不能把已有 `_made` 数据计入。

## 2026-07-24 · T-002 20 题试点交付

- 生成脚本：`scripts/build_t002_pilot.py`；每题目录均有 `samplecode.py`、`producecase.py` 和 `data/0..19.in|out`，组 0 为网页样例。
- 试点题号：`03468, 04117, 04118, 04137, 04138, 04146, 04148, 05345, 05455, 06646, 07622, 07810, 08581, 09267, 19757, 22275, 24637, 27217, 27880, 19943`。
- `producecase.py` 内置题号固定种子和样例断言；逐题重跑生成器后，20 组输入均由 `samplecode.py` 逐字节复算一致。
- 真实 `judge.py` 验收：20/20 题 `Accepted`，每题 20 组；索引重建后 catalog 为 1051/1863 有测试、11161 个配对。
- 多解/特殊判题候选见 `collab/t002-special-judge-skips.md`，本批不生成这些题。

## 2026-07-24 · T-002-001a 交付核验

- 001a 取 manifest 前 20 个“题解代码可直接执行”题号：`03406, 03441, 03447, 03532, 03720, 04005, 04036, 04075, 04077, 04078, 04079, 04080, 04081, 04082, 04084, 04089, 04093, 04103, 04109, 04141`。
- 参考解法均原样取自题解合集，出处、题解文件、heading、seed、生成器名写入 `collab/t002-001a-report.json`；未使用自写参考解法。
- 每题包含 `samplecode.py`、`producecase.py`、20 组数据；生成器嵌入对应题解源码作为 reference solver，并先做网页样例断言。
- 验证：20/20 真实 judge Accepted；20/20 追加输出变异为 Wrong Answer 且 `case=1`；独立重跑后 20x20 输入/输出一致；索引重建后每题 `test_count=20`。

## 2026-07-24 · T-002-001a-fix · 四题去重补强

- 按复核意见只重做 `03447, 03720, 04081, 04082`，其余 16 题数据不改。
- `03447` 改为随机连通银河图（树边 + 随机补边、随机地球航线）；`03720` 改为随机一般二叉树并按缩进文本规则序列化；`04081` 改为随机一般树 DFS 合法 `u/d` 序列；`04082` 改为随机一般树、左儿子右兄弟转换、缺子节点补 `$` 后序列化。
- 四题均为 20/20 个不同输入；批内独立重跑后 20/20 题 samplecode 与输出一致，真实 judge 20/20 Accepted，追加输出变异 20/20 在 case 1 Wrong Answer。报告新增 `distinct_input_cases` 字段。

## 2026-07-24 · T-002-001b 交付准备

- 001b 取 001a 未覆盖的下一批 20 个题号：`04115, 04116, 04119, 04121, 04123, 04124, 04129, 04130, 04135, 04144, 04145, 04147, 04977, 05333, 05343, 05344, 05430, 05442, 05443, 05467`。参考解法均来自题解合集，逐题出处与约束清单写入 `collab/t002-001b-report.json`。
- 新增 `scripts/build_001b.py`，支持题解路径前缀映射、多个样例块取首个完整样例、逐题随机结构生成；每个 `producecase.py` 固定题号种子并嵌入同款参考解法。
- 题面约束已在报告的 `constraints` 逐条列出并由 `constraints_checked: true` 标记。重点结构：4130 方形迷宫/按序钥匙/终止行，5442 连通图/边数/度数上限，4124 含 `N=16` 上界组。
- 验证：20 题去重均 >=15（4123 为 16）；独立 producecase + samplecode 20x20 一致；真实 judge 20/20 Accepted；追加输出变异 20/20 case 1 Wrong Answer；`index_tests.py` 后 catalog 为 1161/1863 有测试。
