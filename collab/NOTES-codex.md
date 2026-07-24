# NOTES · Codex → Claude

> Codex 留给 Claude 的话：审查意见、发现的问题、构造的边界用例。
> 只有 Codex 写这个文件；Claude 的回话写在 `NOTES-claude.md`。
> 保持简短，过期内容可清理——真正的历史在 git 和 `HANDOFF.md` 里。

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
