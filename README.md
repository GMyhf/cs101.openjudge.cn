# CS101 OpenJudge

本地运行：

```bash
python3 server.py
```

本机局域网访问 `http://10.129.81.235:8000/`；同一 Tailnet 的其他机器访问 `http://100.123.12.92:8000/`。默认管理员账号为 `GMyhf`，口令为 `legend200909`；生产环境可通过 `CS101_ADMIN_USER` 和 `CS101_ADMIN_PASSWORD` 覆盖。

## 本地题库

原 CS101 分组的 8 个题库、1,863 道题目详情和分页目录已保存到 `data/openjudge/`。更新目录或重新抓取：

```bash
python3 scripts/crawl_openjudge.py
```

测试数据按题库和题号放置，存在测试目录的题目即可进入本地判题队列：

```text
data/openjudge/tests/pctbook/M20134/01.in
data/openjudge/tests/pctbook/M20134/01.out
```
