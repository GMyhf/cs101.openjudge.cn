# CS101 OpenJudge

> 手册：[用户手册](docs/用户手册.md)（学生） · [管理员手册](docs/管理员手册.md)（部署与运维）
> · [开发教学手册](docs/DEV_HANDBOOK.md)（用这个系统教计算机课）
> · 网页版：<https://gmyhf.github.io/cs101.openjudge.cn/dev-handbook.html>
>
> 网页版由 `python3 tools/build_handbook.py` 从 Markdown 生成，**改完源文要重新构建并提交** ——
> `tests/test_units.py` 会检查两者是否同步。

CS101 题库镜像与本机判题服务。当前目录收录 1,849 道题目，其中 1,846 道已有测试数据，共 27,465 组测试数据。

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
