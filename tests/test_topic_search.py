"""T-063 按考点与题面内容检索：正文抽取、检索接口、考点初标规则、前端共用匹配逻辑。"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import server  # noqa: E402
import tag_topics  # noqa: E402


def page_html(content, menu=True):
    """镜像页的最小骨架：正文 dl、正文下方的菜单、统计区。"""
    bottom = ('<ul class="bottomMenu"><li><a href="#">查看</a></li><li>提交</li></ul>'
              if menu else "")
    return (f'<html><div id="pageTitle"><h2>T: 测试题</h2></div>'
            f'<dl class="problem-content">{content}</dl>{bottom}'
            f'<div class="problem-statistics col-3"><dl><dt>全局题号</dt><dd>1</dd></dl></div></html>')


class StatementTextTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)

    def text(self, html):
        path = self.tmp / "p.html"
        path.write_text(html, encoding="utf-8")
        return server.statement_plain_text(path)

    def test_keeps_bare_less_than_in_constraints(self):
        # 01182：题面裸写 `1 <= N`，宽松的去标签正则会把数据范围整段吃掉
        text = self.text(page_html("<dt>描述</dt><dd>N（1<=N<=50000）和 K<b>句</b></dd>"))
        self.assertIn("1<=N<=50000", text)
        self.assertIn("句", text)

    def test_nested_problem_content_keeps_hint(self):
        # 30363：problem-content 里再套一层，提示里的「并查集」在内层 </dl> 之后
        inner = '<dd><dl class="problem-content"><dt>描述</dt><dd>求连通块</dd></dl></dd><dt>提示</dt><dd>tags: 并查集dsu</dd>'
        self.assertIn("并查集dsu", self.text(page_html(inner)))

    def test_stops_before_menu_and_statistics(self):
        text = self.text(page_html("<dt>描述</dt><dd>正文</dd>"))
        self.assertNotIn("提交", text)
        self.assertNotIn("全局题号", text)
        # 没有菜单的页也不能把统计区吞进来
        self.assertNotIn("全局题号", self.text(page_html("<dd>正文</dd>", menu=False)))

    def test_missing_page_is_empty(self):
        self.assertEqual(server.statement_plain_text(self.tmp / "nope.html"), "")


class SearchPayloadTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        (self.tmp / "pages").mkdir()
        problems = [("practice", "01182", "动物王国 食物链 并查集"),
                    ("practice", "02524", "宗教信仰 学生"),
                    ("private", "1000003", "论文 关键路径 并查集"),
                    ("dsapre", "09999", "下线题库 并查集")]
        for book, pid, body in problems:
            (self.tmp / "pages" / f"{book}__{pid}.html").write_text(
                page_html(f"<dd>{body}</dd>"), encoding="utf-8")
        (self.tmp / "catalog.json").write_text(json.dumps({"problems": [
            {"book": b, "id": i, "path": f"/{b}/{i}/"} for b, i, _ in problems]}), encoding="utf-8")
        for name, value in (("MIRROR", self.tmp), ("CATALOG_RAW_CACHE", None),
                            ("SEARCH_INDEX_CACHE", None), ("CATALOG_TITLE_CACHE", {})):
            patcher = mock.patch.object(server, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def ids(self, query, user=None):
        return [m["id"] for m in server.search_payload(query, user)["matches"]]

    def test_private_and_offline_books_are_filtered(self):
        self.assertEqual(self.ids("并查集"), ["01182"])
        self.assertEqual(self.ids("并查集", "someone"), ["01182"])
        self.assertEqual(sorted(self.ids("并查集", "GMyhf")), ["01182", "1000003"])

    def test_every_term_must_match_case_insensitively(self):
        self.assertEqual(self.ids("动物王国 并查集"), ["01182"])
        self.assertEqual(self.ids("宗教信仰 并查集"), [])
        self.assertEqual(self.ids("测试题"), ["01182", "02524"])  # 标题也在索引里
        self.assertEqual(self.ids("   "), [])

    def test_snippet_is_short_excerpt_around_hit(self):
        match = server.search_payload("宗教", None)["matches"][0]
        self.assertIn("宗教", match["snippet"])
        self.assertLessEqual(len(match["snippet"]), 92)


class CodeTopicRuleTests(unittest.TestCase):
    """每条规则都钉一个「该中」和一个踩过的「不该中」。"""

    def topics(self, code):
        return set(tag_topics.code_topics(code))

    def test_union_find_by_root_check(self):
        code = ("def find(x):\n    if p[x] != x:\n        p[x] = find(p[x])\n    return p[x]\n"
                "def union(a, b):\n    p[find(a)] = find(b)\n")
        found = self.topics(code)
        self.assertIn("并查集", found)
        # find 的递归是路径压缩，不是这道题的「递归」考点
        self.assertNotIn("递归", found)
        self.assertNotIn("并查集", self.topics("for i in range(n):\n    if a[i] == i:\n        print(i)\n"))

    def test_tarjan_is_not_backtracking(self):
        # 02186 Popular Cows：Tarjan 在递归里压栈弹栈、置 in_stack 再撤销，曾被标成「回溯」
        code = ("def tarjan(u):\n    stack.append(u)\n    in_stack[u] = True\n"
                "    for v in g[u]:\n        tarjan(v)\n    w = stack.pop()\n    in_stack[w] = False\n")
        self.assertNotIn("回溯", self.topics(code))
        code = ("def dfs(k):\n    for i in range(n):\n        if not used[i]:\n            used[i] = True\n"
                "            path.append(i)\n            dfs(k + 1)\n            path.pop()\n            used[i] = False\n")
        self.assertIn("回溯", self.topics(code))

    def test_lowest_bit_alone_is_not_fenwick(self):
        # 02982 数独用 `mask & -mask` 取最低位，曾被标成树状数组
        self.assertNotIn("线段树/树状数组", self.topics("bit = mask & -mask\n"))
        self.assertIn("线段树/树状数组", self.topics("while x <= n:\n    t[x] += 1\n    x += x & -x\n"))

    def test_string_prefix_is_not_prefix_sum(self):
        # 02001 Shortest Prefixes 的 prefix 是字符串前缀
        self.assertNotIn("前缀和", self.topics("prefix = []\nprefix.append(c)\n"))
        self.assertIn("前缀和", self.topics("for i in range(n):\n    s[i + 1] = s[i] + a[i]\n"))

    def test_bundle_keeps_only_own_branch(self):
        # 43 份 samplecode 一个文件装多道题，按 `P=题号` 分派；别的题的 BFS 不能算到本题头上
        code = ("from collections import deque\nP=4104\n"
                "def r4087(a):\n    q = deque([0]); seen = {0}\n    while q:\n        q.popleft()\n"
                "def r4104(a):\n    print(a[::-1])\n"
                "if P==3866 or P==4104:\n    pass\n")
        self.assertNotIn("广度优先搜索", self.topics(code))
        self.assertIn("r4104", tag_topics.isolate_bundle(code))
        self.assertNotIn("r4087", tag_topics.isolate_bundle(code))
        # 一个分支都认不出来就什么都不标
        self.assertEqual(tag_topics.isolate_bundle("P=4999\nif P==1:\n    x=1\n"), "")

    def test_statement_tag_line_and_scoped_single_words(self):
        found = tag_topics.statement_topics("描述 求最短距离 提示 tags: dsu, greedy")
        self.assertEqual(set(found), {"并查集", "贪心"})
        # 「堆积木」「客栈」出现在描述里不算堆/栈
        self.assertEqual(tag_topics.statement_topics("描述 猫猫堆积木，住在客栈"), {})


class TopicsFileTests(unittest.TestCase):
    def test_topics_file_is_well_formed(self):
        data = json.loads((ROOT / "data/openjudge/topics.json").read_text(encoding="utf-8"))
        self.assertEqual(data["vocabulary"], tag_topics.TOPICS)
        catalog_ids = {p["id"] for p in json.loads(
            (ROOT / "data/openjudge/catalog.json").read_text(encoding="utf-8"))["problems"]}
        for pid, topics in data["topics"].items():
            self.assertIn(pid, catalog_ids)
            self.assertTrue(topics)
            self.assertTrue(set(topics) <= set(tag_topics.TOPICS), (pid, topics))
            self.assertEqual(topics, sorted(topics, key=tag_topics.TOPICS.index), pid)
        # 用户提问时点名的三道经典并查集题，题面里都没有「并查集」三个字
        for pid in ("01182", "02524", "01611"):
            self.assertIn("并查集", data["topics"].get(pid, []), pid)

    def test_catalog_payloads_carry_topics(self):
        summary = server.catalog_summary_payload()
        item = next(p for p in summary["problems"] if p["id"] == "01182")
        self.assertIn("并查集", item["topics"])


@unittest.skipUnless(shutil.which("node"), "需要 node 才能真跑页面里的检索逻辑")
class ProblemSearchJsTests(unittest.TestCase):
    def test_matching_rules(self):
        script = (ROOT / "static/problem-search.js").read_text(encoding="utf-8")
        harness = script + """
const p = {book: "practice", id: "01182", title: "01182:食物链", topics: ["并查集"]};
const q = {book: "practice", id: "02524", title: "02524:宗教信仰", topics: []};
const checks = [
  problemSearch.matches(p, "并查集", null),              // 考点名可直接搜
  problemSearch.matches(p, "食物链 并查集", null),        // 多个词都要命中
  !problemSearch.matches(p, "食物链 最短路", null),
  problemSearch.matches(p, "011", null),                  // 题号前缀
  problemSearch.matches(q, "学生", new Map([["practice/02524", "…学生…"]])),  // 正文命中由服务端给
  !problemSearch.matches(q, "学生", new Map()),
  problemSearch.matches(q, "", null),
  problemSearch.hasTopic(p, "并查集") && !problemSearch.hasTopic(q, "并查集") && problemSearch.hasTopic(q, ""),
  JSON.stringify(problemSearch.topicCounts([p, q, {topics: ["并查集", "堆"]}])) === '[["并查集",2],["堆",1]]',
];
const bad = checks.map((ok, i) => ok ? null : i).filter(i => i !== null);
if (bad.length) { console.error("failed checks", bad); process.exit(1); }
"""
        with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as handle:
            handle.write(harness)
        self.addCleanup(os.unlink, handle.name)
        result = subprocess.run(["node", handle.name], capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
