# 参与开发

欢迎修 bug、补测试数据、改页面。这份文档只讲三件事：**怎么提**、**哪些地方碰不得**、
**怎么证明你没弄坏东西**。

## 先跑通闸门

```bash
git clone https://github.com/GMyhf/cs101.openjudge.cn.git
cd cs101.openjudge.cn
python3 tools/handoff.py --verify      # 全套测试 + 语法检查，退出码 0 才算过
python3 server.py                      # 起服务，默认 0.0.0.0:8000
```

**零第三方依赖**：只需要 Python 3（3.10+）。装了 `node` 会多跑几条页面内 JS 的用例，
装了 gcc/g++/pypy3/.NET 10/Swift 会多跑对应语言的判题用例，没装就跳过 —— 闸门在
只有 Python 的干净克隆上也必须是绿的。

## 怎么提

- **外部贡献者**：Fork → 开分支 → 提 Pull Request。不需要任何授权。
- **有写权限的人**：也请走 PR。`main` 是发版分支，`tools/release.sh` 直接从它拉代码
  重启线上服务 —— **合进 `main` 的东西下一次发版就上线**。

一个 PR 只做一件事。commit message 写「为什么」，不是「改了哪个文件」。

## 六条红线（审查时必查）

这个项目跑的是**别人写的代码**，而且对公网开放。下面六条不是风格偏好，
每一条背后都有一次真实事故（细节见 `docs/DEV_HANDBOOK.md` 和 `collab/HANDOFF.md`）。
碰到其中任何一条的 PR，一定会被人工逐行看，CI 绿不代表能合。

1. **判题沙箱**。`judge.py` 直接运行不可信代码。改 `_run` / `_limits` / `prepare_program`
   要能回答：资源限制（CPU 4s、文件 2MiB、内存 768MiB）还在吗？子进程 `env` 还是白名单吗？
   Python 还带 `-I` 吗？临时目录之外有没有多出可写路径？
   **放宽任何一条，等于把公网算力和一条提权路径一起送出去。**
2. **认证边界**。`/api/submit`、`/api/run` 必须登录。管理员口令只来自环境变量或
   未跟踪的 `data/.admin_password`，**任何形式的口令都不得进 git** —— 这个仓库
   曾因此被整体重写过一次。同理 `data/.smtp.env`、`data/*.db` 都不入库。
3. **路径安全**。静态分发只走 `static/` 下的后缀白名单（`ROOT in file.parents` 只防
   「逃出 ROOT」，防不住「ROOT 里的东西不该全公开」—— `data/course.db` 一度可以直接下载）。
   本地页面路由用题库名白名单。改路由不得放宽这两道防线。
4. **数据不入库**。抓取的真实测试数据 `data/openjudge/tests/**` 在 `.gitignore` 里；
   只有 `*_made/` 生成数据入库。加抓取脚本前先看 `.gitignore`。
5. **上游代理**。未命中本地镜像时会回源 `cs101.openjudge.cn`。
   **不要把本地会话 cookie 或任何凭据转发给上游**，回源只发生在 GET 读页面这条路径上。
6. **单文件极简风格**。刻意保持 `server.py`（标准库 HTTP）+ `judge.py` 两个文件、
   零第三方依赖。**引入框架或依赖是架构决策，先在 `collab/PLAN.md` 里提出来，
   由维护者拍板，不要直接在 PR 里带进来。**

## 权限判断只有一份

「谁能看到别人的代码和判题详情」这条规则写在 `/api/submissions` 里：
**列表人人可见，源码与 `detail` 只有本人和管理员**。新增任何展示提交的接口，
请复用这条判断，不要另写一份 —— 有两份，迟早只改一份。

`detail` 里含 `failing_input` / `expected_output`，那是出错那组的测试数据，
**公开等于泄题**。任何新接口都不要整份透出去。

## 测试怎么写才算数

- **新断言要做一次变异自检**：把被测的那行代码改坏，确认对应用例真的变红。
  「删掉代码测试照样绿」的覆盖率是负资产。
- **闸门必须在全新 `git clone` 上成立**。测试不能依赖 `.gitignore` 掉的抓取数据；
  判题夹具自带在 `tests/fixtures/mirror/` 并已入库。
- **判据要判「这台机器能不能做这件事」，不是「有没有这个可执行文件」**。
  用 `@unittest.skipUnless(...)` 让缺工具链的机器跳过，而不是报错。
- 页面里的 JS 逻辑，能抠出来丢进 `node` 真跑就真跑（见
  `test_submit_page_highlighter_runs`、`test_problem_table_sorts_by_accepted_count_by_default`）。
  只断言「字符串在不在」抓不住排序、正则这类错。

## 报问题

开 Issue 时请写清楚：**做了什么操作 → 期望什么 → 实际什么**。
判题相关的问题请附题库、题号、语言，以及提交详情页的链接（`/book/<题库>/solution/<号>/`）。

**不要在公开 Issue 里贴** 口令、会话 cookie、`.smtp.env` 的内容或任何测试数据。
安全问题请直接私下联系维护者，不要开公开 Issue。

## 关于许可与镜像内容

本仓库自身的代码与文档以 MIT 许可发布（见 `LICENSE`）。

**`data/openjudge/` 下是 cs101.openjudge.cn 的镜像内容**（题面、样例、目录页）——
版权属原作者，不在 MIT 许可范围内，提 PR 时也请不要把新抓取的题面数据加进来。
