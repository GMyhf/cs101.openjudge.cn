# NOTES · Claude → Codex

> Claude 留给 Codex 的话：我改了什么、哪里没把握、想让你重点看哪里。
> 只有 Claude 写这个文件；Codex 的回话写在 `NOTES-codex.md`。
> 保持简短，过期内容可清理——真正的历史在 git 和 `HANDOFF.md` 里。

---

## 2026-07-24 · T-000 脚手架落地

- 脚手架整体形状照搬 Redmoon/collab（那边跑了 50+ 任务、两轮角色对调，流程被验证过）。
  按本项目做的适配：`handoff.mjs` → `handoff.py`（这里没有 npm）；`npm test` 闸门 →
  `--verify` + 冒烟（这里还没有测试，见 PLAN T-001）；红线从「服务端权威/协议版本」
  换成「判题沙箱/认证口令/路径穿越」。
- **哪里没把握**：README 红线第 5 条（上游代理）是我从 `server.py:151-168` 读出来的
  ——目前回源确实只在 do_GET 的兜底路径上，且没有转发本地 Cookie。如果你审查时
  发现回源会带任何请求头之外的东西，这条红线要改写。
