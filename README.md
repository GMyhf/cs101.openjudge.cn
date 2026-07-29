# CS101 OpenJudge

[![CI](https://github.com/GMyhf/cs101.openjudge.cn/actions/workflows/ci.yml/badge.svg)](https://github.com/GMyhf/cs101.openjudge.cn/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> 想参与开发看 [CONTRIBUTING.md](CONTRIBUTING.md)。**提 PR 前请先跑
> `python3 tools/handoff.py --verify`**，并读一遍那六条红线 ——
> 这个项目直接运行不可信代码且对公网开放，有些地方碰不得。

> 手册：[用户手册](docs/用户手册.md)（学生） · [管理员手册](docs/管理员手册.md)（部署与运维）
> · [开发教学手册](docs/DEV_HANDBOOK.md)（用这个系统教计算机课）
> · 网页版：<https://gmyhf.github.io/cs101.openjudge.cn/dev-handbook.html>
>
> 网页版由 `python3 tools/build_handbook.py` 从 Markdown 生成，**改完源文要重新构建并提交** ——
> `tests/test_units.py` 会检查两者是否同步。

CS101 题库镜像与本机判题服务。当前目录收录 1,849 道题目，其中 1,338 道已有测试数据，共 26,147 组测试数据。

> 2026-07-29 起，`data/openjudge/tests/` 下 `1000-1999` / `2000-2999` / `3000-3682` 三个桶的
> **非 `*_made/` 目录不再参与判题**：那不是抓来的平台数据，是某人 2008 年的工作目录
> （混着 1,894 个 `.c/.cpp/.java/.pas` 解法源码，数据文件名是 `mydata`/`pig`/`radar` 这种）。
> 实测 01384 的参考解法在平台上 Accepted、在本地却 TLE，卡的正是其中一份 117KB 的私人压测文件 ——
> **学生在平台过、在我们这挂**。代价是 508 条记录（246 个唯一题号）暂时没有测试数据，
> 由 T-028 逐批生成 `*_made/` 补回；判据与出处见 `scripts/index_tests.py · ARCHIVE_BUCKETS`。

## 运行服务

```bash
python3 server.py
```

服务默认监听 `0.0.0.0:8000`。本机局域网访问 `http://10.129.81.235:8000/`；同一 Tailnet 的其他机器访问 `http://100.123.12.92:8000/`。

### 常驻部署（systemd）

`deploy/cs101.service` 是常驻单元。换机器只需改 `User`/`Group`/`WorkingDirectory` 三处。

```bash
sudo cp deploy/cs101.service /etc/systemd/system/cs101.service
sudo systemctl daemon-reload
sudo systemctl enable --now cs101
```

装好之后，**发版就是这一条**：

```bash
git pull && sudo systemctl restart cs101
```

`systemctl status cs101` 看状态，日志用 `journalctl -u cs101 -f`。

> 日志不要改成 `StandardOutput=append:.../server.log`：jensen 的 SELinux 是 Enforcing，
> systemd 以 `init_t` 打开 home 目录下的文件会被拒，服务会以 `209/STDOUT` 反复重启起不来。

> 不要再用 `pkill` + `nohup` 手工重启。`pgrep -f "python3 -u server.py"` 会匹配到
> **执行这条命令的 shell 自己**（命令串里就含这段文字），把自己杀掉、链条断在启动新进程之前——
> 结果是老进程活得好好的，看起来却像重启过了。2026-07-28 就这么静默失败过一次。

管理员账号通过 `CS101_ADMIN_USER` 配置，口令通过 `CS101_ADMIN_PASSWORD` 或本机未跟踪的 `data/.admin_password` 配置。

提交页支持 Python3、PyPy3、C、C++、C#、F#、VB.NET、Swift 和 Objective-C。判题时间倍率为 Python ×10、PyPy3 ×3、C/C++/Swift/Objective-C ×1、C#/F#/VB.NET ×2；C#/F#/VB.NET 内存限额为 C/C++ 的 2 倍。题面限时按 C/C++ 口径计算。

## 题库数据

CS101 分组的题库详情、样例和分页目录保存在 `data/openjudge/`。更新目录或重新抓取：

```bash
python3 scripts/crawl_openjudge.py
```

重新扫描测试数据并更新题库索引：

```bash
python3 scripts/index_tests.py
```

测试数据按题库和题号放置，存在测试目录的题目即可进入判题队列：

```text
data/openjudge/tests/20000-29982/29647_made/data/0.in
data/openjudge/tests/20000-29982/29647_made/data/0.out
```

缺数据题目的 `_made` 目录包含 `samplecode.py`、`producecase.py` 和 `data/*.in|*.out`。数据构建批次、来源、样例锚点、约束检查、平台复验记录保存在 `collab/`；所有 `_made` 数据目录纳入 Git。

## 验证

批次构建使用固定种子生成器，并要求 `producecase.py` 重跑后 `data/` 逐字节不变。常用验证命令：

```bash
python3 tools/handoff.py --verify
python3 scripts/t004_judge_round.py 16
python3 -m unittest
```

`.github/workflows/ci.yml` 在每个 PR 上跑的就是第一条命令。CI **刻意不装工具链**：
缺 pypy3 / .NET 10 / Swift 时相应用例自动跳过，闸门在只有 Python 的干净克隆上也必须绿。
「9 种语言都还判得动」由发版时在部署机上跑的 `scripts/smoke_languages.py --require-all`
保证（见 `tools/release.sh`）——**CI 管逻辑没坏，发版冒烟管这台机器判得动。**

## 许可

本仓库自身的代码与文档以 MIT 许可发布，见 [LICENSE](LICENSE)。

**`data/openjudge/tests/` 下入库的 506 个 `*_made/` 全部是本项目自己生成的测试数据**
（抓取的真实测试数据不入库，见 `.gitignore`），属于本仓库自身的工作，同样适用 MIT。

不在 MIT 范围内的只有两处：

- **镜像内容**：`data/openjudge/pages/`（1,849 份题面）、`data/openjudge/books/`（目录页），
  以及由它们派生的 `catalog.json` / `test_index.json` / `limits.json`（题目标题与上游统计）。
  版权属 cs101.openjudge.cn 原作者。`data/openjudge/producecase_prompt/` 里每份 prompt
  也整段嵌了题面。
- **他人提交的参考实现**：220 个 `*_made/` 目录的 `samplecode.py`（218 份）与
  `producecase.py`（161 份，把参考实现内嵌成 `REFERENCE` 字符串）取自 OpenJudge 上
  别人的 Accepted 提交，文件头已注明提交号、来源链接与
  `License: not declared on the submission page; no license is inferred`。
  **这些不是本仓库能授权出去的东西。** 同目录下的 `data/*.in|*.out` 是本项目生成的。
