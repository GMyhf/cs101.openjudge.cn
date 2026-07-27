# CS101 OpenJudge

CS101 题库镜像与本机判题服务。当前目录收录 1,849 道题目，其中 1,846 道已有测试数据，共 27,465 组测试数据。

## 运行服务

```bash
python3 server.py
```

服务默认监听 `0.0.0.0:8000`。本机局域网访问 `http://10.129.81.235:8000/`；同一 Tailnet 的其他机器访问 `http://100.123.12.92:8000/`。

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
