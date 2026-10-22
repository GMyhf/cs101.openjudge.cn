# AGENTS.md

This file provides guidance to the AI agent when working with code in this repository.

本仓库文档与注释均为中文；commit message 写「为什么」，一个 PR 只做一件事。
细节见 `CONTRIBUTING.md`（六条红线）与 `docs/管理员手册.md`，改代码前先读 CONTRIBUTING。

## 闸门与测试

- 提交前必跑 `python3 tools/handoff.py --verify`（全套 unittest + py_compile + 待返工检查 + full_sweep），退出码 0 才算过；CI 跑的就是这一条，job 名叫 `gate`，**不要改名为 `build`**（会与 GitHub Pages 注入的检查重名）。
- 单跑测试用 `python3 -m unittest`。
- 零第三方依赖（Python 3.10+）。缺 node/gcc/pypy3/.NET/Swift 时用例靠 `@unittest.skipUnless` 跳过，**闸门在只有 Python 的干净克隆上必须是绿的** —— 测试不得依赖被 .gitignore 的抓取数据，判题夹具在已入库的 `tests/fixtures/mirror/`。
- 新断言要做变异自检：把被测代码改坏，确认用例真的变红。
- 改了 `docs/*.md` 手册源文后要跑 `python3 tools/build_handbook.py` 重建 HTML 并一并提交，`tests/test_units.py` 检查两者同步。

## 架构红线（违反即事故，每条背后都有真实事故）

- **单文件极简**：刻意保持 `server.py`（标准库 HTTP）+ `judge.py` 两文件、零依赖。引入框架/依赖是架构决策，须先在 `collab/PLAN.md` 提出由维护者拍板。
- **判题沙箱**：`judge.py` 直接运行不可信代码且对公网开放。改 `_run`/`_limits`/`prepare_program` 时资源限制（CPU 4s、文件 2MiB、内存 768MiB）、子进程 env 白名单、`python3 -I`、临时目录隔离一条都不能放宽。
- **凭据不入库**：口令只来自 `CS101_ADMIN_USER`/`CS101_ADMIN_PASSWORD` 环境变量或未跟踪的 `data/.admin_password`；`data/*.db`、`data/.smtp.env*`、`server.log` 绝不入库（仓库曾因此整体重写）。
- **路径安全**：静态分发只走 `static/` 后缀白名单；本地页面路由走题库名白名单。不得放宽。
- **权限判断只有一份**：「列表人人可见，源码与 detail 只有本人和管理员」写在 `/api/submissions`，新接口复用它；`detail` 含失败测试数据，整份透出等于泄题。
- **上游代理**：回源 cs101.openjudge.cn 只在 GET 兜底路径，不得转发本地 cookie/凭据。

## 数据规则（gitignore 非直觉）

- `data/openjudge/tests/**` 默认不入库；例外：自产的 `*_made/` 与课题组 `*_GMyhf/` 目录**必须入库**（.gitignore 里用 `!` 翻回）。
- `1000-1999`/`2000-2999`/`3000-3682` 三个桶里的非 `*_made/` 目录是 2008 年私人工作目录，**不参与判题**（判据见 `scripts/index_tests.py · ARCHIVE_BUCKETS`）。
- 取自他人 Accepted 提交的 `samplecode.py`/`producecase.py`（文件头有 `License: not declared ...`）新增时必须保留同样的头部署名（提交号 + 来源链接 + 许可状态）。

## 部署

`main` 即发版分支：合入 main 后线上发版就是 `git pull && sudo systemctl restart cs101`。不要 `pkill`+`nohup` 手工重启（pgrep 会匹配到 shell 自己，曾静默失败）。
