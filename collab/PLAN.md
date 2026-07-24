# PLAN · 唯一任务清单与决策记录

> 这是 Claude 与 Codex 共享的**唯一任务事实源**。人拍板任务与优先级；
> 两个 agent 认领任务、更新状态、署名。状态流转：`Backlog → In progress → Review → Done`。
> 每条任务用一个 `T-<编号>` 标识，交接与提交信息里引用它。
>
> **格式硬约束**（Redmoon 的教训，见其 2026-07-19 交接）：每行恰好 5 列；
> 追加复核结论写进备注列、用 ` — ` 分隔，**不要**用 `| ` 另起一格——超出表头的
> 单元格在 GitHub 渲染时被直接丢弃，人看到的会是另一份 PLAN。描述里含 `|` 的
> 代码片段要转义（`\|`），否则会把行切碎。

## 状态看板

| ID | 任务 | 状态 | 负责 | 关联提交 / 备注 |
| --- | --- | --- | --- | --- |
| T-000 | 搭建 Claude⇄Codex 协作脚手架（本目录 + `tools/handoff.py`） | Done | Claude | 移植自 Redmoon/collab，红线清单按本项目改写 |
| T-001 | **建立测试套件**：判题核心（AC/WA/TLE/RE/CE、输出比对的 token 语义、资源限制真的生效）+ 服务端（注册/登录/会话、`/api/submit` 未登录 401、静态文件不可穿越）。建成后它取代 `--verify` 成为交接闸门 | Backlog | — | 无测试是当前最大的协作风险：审查方没有仲裁工具，只能人肉读 diff |
| T-002 | **为缺测试数据的题目 LLM 生成测试数据**（实现方 = Codex，复核方 = Claude）：按 `tools/make_data_template.py` 模版，为 catalog 中 `test_cases` 为空的题目逐题写参考解法 + 数据生成器，产出 `data/openjudge/tests/<bucket>/<题号>_made/`。**先做 20 题试点批交 Claude 复核，复核通过再分批放量**。详细规格见 `NOTES-claude.md` 2026-07-24 条（二次勘查后已更新：以人的 producecase 工作流为准） | Backlog | Codex | **前置已全部清除**（2026-07-24：七桶齐全，catalog 引用的 14152 个文件零缺失，`index_tests.py` 解禁）。范围内含：索引器改收 `data/` 子目录，让人已有的 `4102_made`/`18250_made` 生效 |

## Decision Log

> 人拍板的决策记在这里：日期 · 决策 · 理由 / 出处。agent 不得自行改写已有条目。

- 2026-07-24 · 协作脚手架落地，流程与文件职责沿用 Redmoon/collab 的形状；
  仲裁闸门暂为 `--verify` + 手动冒烟，T-001 建成测试套件后升级。
- 2026-07-24 · 人拍板 T-002：项目本意是把 cs101.openjudge.cn 现代化，提供完整的
  编写、提交、反馈错在哪组数据的闭环；缺数据的题目用 LLM 生成测试数据，
  目录命名 `<题号>_made`（如 `4102_made`）以标记出处。分工：Codex 生成、Claude 复核。
- 2026-07-24 ·（已决）人的模版落地：`data/openjudge/producecase_prompt/` 37 份单题
  prompt（题面 + producecase_template.py + ac.py → LLM 产出 producecase.py），实物
  样板 `tests/4000-8210/4102_made/`。**以人的工作流为准**，Claude 起草的
  `tools/make_data_template.py` 已删；其样例自检 + 固定种子两条纪律并入 T-002 规格。
- 2026-07-24 · Claude 勘查发现并记录：① 恢复的 tests 树缺 `20000-29982` 桶
  （2236 条 catalog 引用悬空，判题会崩），等人补齐；② 人已生成的 `4102_made`/
  `18250_made` 因数据在 `data/` 子目录而未被索引器收录（`test_count=0`），
  修索引器纳入 T-002 范围。
