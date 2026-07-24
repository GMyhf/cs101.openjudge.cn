# 协作脚手架 · Claude ⇄ Codex

两个 AI（Claude Code 与 Codex）不能靠"记忆"协作，只能靠**共享事实源**交接。
这个目录就是那层事实源：谁都能读、谁都能写、每一轮都留下书面痕迹。

## 文件职责

| 文件 | 作用 | 谁写 |
| --- | --- | --- |
| `PLAN.md` | 唯一任务清单 + 决策记录（Decision Log） | 人拍板；两个 agent 更新状态 |
| `HANDOFF.md` | 交接日志：每一次「我做完了，轮到你」都追加一条 | 交接方 |
| `NOTES-claude.md` | Claude 留给 Codex 的话（改了什么、哪里没把握） | 只有 Claude |
| `NOTES-codex.md` | Codex 留给 Claude 的话（审查意见、发现的问题） | 只有 Codex |
| `review-input.md` | 脚本自动生成的 review 包（**不入库**） | `tools/handoff.py` |

> `git` 是最硬的桥梁，测试是最硬的仲裁。文档负责「为什么」和「接下来」，
> 代码与测试负责「是什么」。冲突时，能跑通验证的方案胜出。
> **本项目暂无自动化测试套件**——在它建成之前（见 PLAN T-001），仲裁标准是
> `python3 tools/handoff.py --verify`（语法编译检查）+ 手动冒烟（起 `server.py`、
> 提交一道有测试数据的题、确认判题结果）。这是个已知的弱闸门，补测试优先级高。

## 一轮标准循环

```
1. 人：把目标写进 collab/PLAN.md（Backlog 里加一条任务）
2. 实现方（如 Claude）：
     - 认领任务 → 改 PLAN.md 状态为 In progress，署名
     - 实现 → python3 tools/handoff.py --verify → 手动冒烟 → git commit（小步、清晰 message）
     - 写 NOTES-claude.md：做了什么 / 哪里没把握 / 想让对方重点看哪里
     - 追加一条 HANDOFF.md 交接记录
     - 运行 python3 tools/handoff.py --from claude --to codex
3. 人：把生成的 collab/review-input.md 交给 Codex（或让 Codex 直接读仓库）
4. 审查方（Codex）：
     - 读 review-input.md → 审查 / 挑 bug / 写会失败的测试
     - 把意见写进 NOTES-codex.md；能直接修的就修 + commit
     - 追加一条 HANDOFF.md 交接记录，轮回给 Claude
5. 实现方：git pull → 看对方 commit 与 NOTES → 继续迭代
6. 验证全绿 + 双方无异议 → 在 PLAN.md 标 Done，写进 Decision Log（如有决策）
```

## 协作模式（按需选）

- **生成 ↔ 审查**：一方写实现，另一方交叉审查。不同模型盲点不同，能抓到单模型漏掉的问题。
- **规划 ↔ 执行**：一方拆任务写 PLAN，另一方逐条实现，偏差写回 NOTES。
- **红队 / 对抗**：关键逻辑（判题沙箱、认证、路径处理）由另一方专门找茬、写会失败的测试。
- **分工并行**：按模块切分，各用 git 分支或 `git worktree` 隔离，避免踩同一段代码。

## 硬约束（避免互相覆盖）

- 开工前先在 `PLAN.md` 认领任务并署名；**不要两个 agent 同时改同一文件的同一段**。
- 小步提交、清晰 commit message，审查方才看得懂 diff。
- 交接格式统一走 `HANDOFF.md` 模板，减少人工搬运。
- **交回时必须附一次真正跑完的验证结果**（当前是 `--verify` 输出 + 冒烟结论；
  测试套件建成后是全套测试尾部计数）。不接受「我觉得没问题」。
- **交付后回来销账：任务落地时，把它回答掉的「未决 / 待拍板 / TODO」逐条改成带出处的已决记录。**
  保留原问题、注明最终取值与代码出处，不要删除，让来回可查。
  两个 agent 每轮都读这些文档，一份多数已决的待办清单会让人重开已经关掉的方向。

## 本项目红线（审查时必查）

1. **判题沙箱**：`judge.py` 直接运行不可信用户代码。任何对 `_run`/`_limits` 的改动都要问：
   资源限制（CPU 4s / 文件 2MiB / 内存 768MiB）还在吗？`env` 还是白名单吗？
   Python 还带 `-I`（隔离模式）吗？临时目录之外有没有可写路径？
2. **认证边界**：`/api/submit` 必须登录；管理员口令只来自环境变量或未跟踪的
   `data/.admin_password`，**任何形式的口令都不得进 git**（历史上已因此重写过一次仓库）。
3. **路径安全**：静态文件分发依赖 `ROOT in file.parents` 防目录穿越；本地页面路由用
   白名单正则匹配题库名。改路由时不得放宽这两道防线。
4. **数据不入库**：`data/openjudge/tests/`、`data/*.db`、`__MACOSX` 均在 `.gitignore`；
   抓取脚本的产物入不入库要先看 `.gitignore` 再决定。
5. **上游代理**：未命中本地镜像时会回源真 `cs101.openjudge.cn`。不要把本地会话
   cookie / 凭据转发给上游；回源只该发生在 GET 读页面这条路径上。
6. **单文件极简风格**：本项目刻意保持 `server.py`（标准库 HTTP）+ `judge.py` 两个文件、
   零第三方依赖。引入框架或依赖属于架构决策，必须先在 PLAN 里由人拍板。

## 生成 review 包

```bash
python3 tools/handoff.py --from claude --to codex          # 默认：未提交改动 or 最近一次提交
python3 tools/handoff.py --from claude --to codex --base main   # main..HEAD 的全部改动
python3 tools/handoff.py --from codex --to claude --range HEAD~3..HEAD --verify
```

生成 `collab/review-input.md`：包含改动摘要、changed files、完整 diff、交接方 NOTES、
PLAN 里的未决项，以及一份针对本项目的 review 检查清单。把这个文件喂给另一方即可。
