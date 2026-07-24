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
