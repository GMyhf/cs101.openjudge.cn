#!/usr/bin/env python3
"""给题目自动初标考点，写出 `data/openjudge/topics.json`（题号 -> 考点列表）。

为什么不只靠全文检索：经典的并查集题（01182 食物链、02524 宗教信仰、01611 The Suspects）
题面里根本不出现「并查集」三个字，2026-11-09 实测题面全文含「并查集」的只有 5 道。
考点得从**解法**里看，而本仓库恰好有 1049 份已入库的参考解法 `*_made/samplecode.py`。

三路证据，任一命中即打上该考点：

1. **参考代码特征**（主力）：`samplecode.py` 里的代码形状，例如
   `parent[x] != x` + 改写同一数组 → 并查集；`heapq` → 堆；`popleft` + 访问标记 → BFS。
   只收「看到就基本能确定」的特征，宁缺毋滥：排序、模拟、贪心这类从代码看不出来的不在这里判。
2. **题面明说**：题面/提示里直接写了考点名（「提示：并查集」「tags: dp」）。
3. **人工修正**：`data/openjudge/topics_overrides.json` 的 `add`/`remove`，
   在自动结果之上最后应用，重新生成不会冲掉人工判断。

用法：
    python3 scripts/tag_topics.py            # 重新生成 topics.json
    python3 scripts/tag_topics.py --explain 01182   # 看某题每个考点的证据
    python3 scripts/tag_topics.py --sample 并查集 10  # 随机抽 10 道某考点的题供人工复核
"""
import ast
import json
import textwrap
import warnings
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from server import statement_plain_text  # noqa: E402  与线上检索用同一份正文抽取

MIRROR = ROOT / "data" / "openjudge"
OUTPUT = MIRROR / "topics.json"
OVERRIDES = MIRROR / "topics_overrides.json"

# 考点词表，也是页面上筛选按钮的顺序（大致按课程讲授顺序）。
TOPICS = [
    "递归", "栈", "队列", "链表", "二叉树", "堆", "二分查找", "前缀和", "双指针",
    "贪心", "动态规划", "深度优先搜索", "回溯", "广度优先搜索", "并查集",
    "拓扑排序", "最短路", "最小生成树", "字典树", "线段树/树状数组", "KMP",
    "状态压缩", "数论",
]


def _code_body(source):
    """去掉文件头署名注释与行内注释，免得注释里的词被当成代码特征。"""
    lines = []
    for line in source.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("#"):
            continue
        lines.append(line)
    return "\n".join(lines)


def isolate_bundle(code):
    """多题合一的参考代码只留本题那一段；不是合集就原样返回。

    有 43 份 samplecode 是一个文件装二三十道题的解法，用模块级 `P=题号` 选分支
    （`if P==4140:` 或 `def r4104(...)` + 分派表）。整份拿来找特征，04104 单词翻转
    会被别的题的 BFS 标成「广度优先搜索」。认不出本题分支就返回空串：宁可不标。
    """
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            tree = ast.parse(code)
    except SyntaxError:
        return code
    number = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and \
                isinstance(node.targets[0], ast.Name) and node.targets[0].id == "P" and \
                isinstance(node.value, ast.Constant) and isinstance(node.value.value, int):
            number = node.value.value
    if number is None:
        return code

    def mentions_number(test):
        if isinstance(test, ast.BoolOp) and isinstance(test.op, ast.Or):
            return any(mentions_number(value) for value in test.values)  # if P==3726 or P==3866
        if not isinstance(test, ast.Compare) or not isinstance(test.left, ast.Name) or test.left.id != "P":
            return False
        values = []
        for comp in test.comparators:
            if isinstance(comp, ast.Constant):
                values.append(comp.value)
            elif isinstance(comp, (ast.Tuple, ast.List, ast.Set)):
                values += [e.value for e in comp.elts if isinstance(e, ast.Constant)]
        return number in values

    parts = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and \
                re.fullmatch(rf"\w*?0*{number}", node.name):
            parts.append(ast.get_source_segment(code, node) or "")
        elif isinstance(node, ast.If) and mentions_number(node.test):
            parts.append("\n".join(ast.get_source_segment(code, stmt) or "" for stmt in node.body))
    # 分支里调用的同文件辅助函数也算本题代码（例如 if P==N: return helper(a)）。
    helpers = {n.name: n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    called = set(re.findall(r"\b([A-Za-z_]\w*)\s*\(", "\n".join(parts)))
    for name in sorted(called & set(helpers)):
        segment = ast.get_source_segment(code, helpers[name]) or ""
        if segment not in parts and not any(isinstance(n, ast.If) and mentions_number(n.test)
                                            for n in ast.walk(helpers[name])):
            parts.append(segment)
    return textwrap.dedent("\n".join(textwrap.dedent(p) for p in parts))


def _recursive_functions(tree):
    """返回在自身函数体里调用了自己的函数名（直接递归）。"""
    found = set()
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for inner in ast.walk(node):
            if isinstance(inner, ast.Call):
                func = inner.func
                name = func.id if isinstance(func, ast.Name) else (
                    func.attr if isinstance(func, ast.Attribute) else None)
                if name == node.name:
                    found.add(node.name)
                    break
    return found


def _function_source(tree, source, names):
    parts = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in names:
            parts.append(ast.get_source_segment(source, node) or "")
    return "\n".join(parts)


def code_topics(source):
    """参考代码 -> {考点: 证据}。每条规则都要求「基本能确定」，宁可漏标。"""
    code = isolate_bundle(_code_body(source))
    hits = {}

    def hit(topic, why):
        hits.setdefault(topic, why)

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)  # 参考代码里的 '\d' 之类无关紧要
            tree = ast.parse(code)
    except SyntaxError:
        tree = None
    recursive = _recursive_functions(tree) if tree else set()
    rec_src = _function_source(tree, code, recursive) if tree else ""

    # 只有并查集的 find 在递归时不标「递归」：那是路径压缩的写法，不是这道题的考点。
    find_like = {name for name in recursive
                 if re.fullmatch(r"\w*(find|root|father|parent|anc)\w*", name, re.I)}
    if recursive - find_like:
        hit("递归", "函数自调用：" + ", ".join(sorted(recursive - find_like)))

    # 并查集：`p[x] != x` / `p[x] == x` 找根，且同一数组被改写成别的根。
    for m in re.finditer(r"\b(\w+)\[(\w+)\]\s*(?:!=|==)\s*\2\b", code):
        arr = m.group(1)
        if re.search(rf"\b{re.escape(arr)}\[[^\]]+\]\s*=\s*(?!\s*=)", code) and \
                re.search(r"def\s+\w*(find|root|father|parent|get|union|merge|anc)\w*\s*\(", code, re.I):
            hit("并查集", f"找根判断 {m.group(0)}，且改写 {arr}[...]")
            break
    if re.search(r"class\s+(DSU|UnionFind|DisjointSet)\b", code, re.I):
        hit("并查集", "定义了并查集类")

    if re.search(r"\bheapq\b|\bheappush\b|\bPriorityQueue\b", code):
        hit("堆", "使用 heapq / PriorityQueue")

    if re.search(r"\bbisect\b", code):
        hit("二分查找", "使用 bisect")
    elif re.search(r"\bmid\s*=\s*\(?\s*\w+\s*\+\s*\w+\s*\)?\s*(//\s*2|>>\s*1)", code) and \
            re.search(r"while\s+\(?\s*\w+\s*(<|<=)\s*\w+", code):
        hit("二分查找", "while 循环里取 mid = (lo + hi) // 2")

    visited = re.search(r"\b(vis|visit|visited|seen|used|inq|in_queue|dist|distance|step|steps)\b", code)
    if re.search(r"\.popleft\(\)", code) and visited:
        hit("广度优先搜索", f"deque.popleft() + 访问标记 {visited.group(0)}")

    if rec_src and re.search(r"\b(vis|visit|visited|seen|used|marked|path|graph|grid|adj|maze|board)\b", rec_src):
        hit("深度优先搜索", "递归函数里遍历并标记 visited/graph/grid")
    if rec_src and (re.search(r"\b(?!\w*stack)(\w+)\[[^\]]+\]\s*=\s*(True|1)\b[\s\S]*\b\1\[[^\]]+\]\s*=\s*(False|0)\b", rec_src)
                    or re.search(r"\b(?!(?:stack|stk|st|s)\.)(\w+)\.append\([^)]*\)[\s\S]*\b\1\.pop\(\)", rec_src)):
        # 不认 stack.append/pop：Tarjan 求强连通（02186 Popular Cows）也是递归里压栈弹栈，那不是回溯。
        hit("回溯", "递归里置标记后撤销（或 path.append 后 path.pop）")

    if re.search(r"@(functools\.)?(lru_cache|cache)\b", code):
        hit("动态规划", "记忆化搜索 @lru_cache")
    if re.search(r"\b(dp|f|memo)\s*(\[[^\]]*\]\s*)+=(?!=)", code) and re.search(r"\b(dp|memo)\b", code):
        hit("动态规划", "状态数组 dp[...] = ...")

    if re.search(r"\b(in_?deg(ree)?|indeg|in_degree|indegree|ind)\s*\[", code, re.I):
        hit("拓扑排序", "维护入度数组")

    if re.search(r"\b(dijkstra|spfa|bellman|floyd)\b", code, re.I):
        hit("最短路", "函数/变量名含 dijkstra/spfa/floyd")
    elif "堆" in hits and re.search(r"\b(dist|distance|dis|cost)\s*\[", code):
        hit("最短路", "heapq + dist[...]（Dijkstra 形状）")

    if re.search(r"\b(kruskal|prim|mst)\b", code, re.I):
        hit("最小生成树", "函数/变量名含 kruskal/prim/mst")

    if re.search(r"\b(trie|TrieNode)\b", code, re.I):
        hit("字典树", "定义了 Trie")

    # 只认树状数组的跳转 `x += x & -x`；单独的 `mask & -mask` 是取最低位，数独里也用。
    if re.search(r"\blowbit\b|\b(\w+)\s*[+-]=\s*\1\s*&\s*\(?-\s*\1\b", code) or \
            re.search(r"\b(seg|segment|segtree|SegmentTree|tree)\s*\[\s*2\s*\*\s*\w+\s*(\+\s*1)?\s*\]", code):
        hit("线段树/树状数组", "lowbit / x & -x / tree[2*i]")

    if re.search(r"\bkmp\b|\b(nxt|next|fail|lps|pi)\s*\[\s*\w+\s*\]\s*=\s*\w+", code, re.I) and \
            re.search(r"\bwhile\s+\w+\s*>\s*0\s+and\s+\w+\[", code):
        hit("KMP", "失配数组 + while j > 0 and ... 回退")

    if re.search(r"\b(mask|state|status)\b", code) and re.search(r"1\s*<<\s*\w+", code) and "动态规划" in hits:
        hit("状态压缩", "dp + 1 << k 掩码")

    if re.search(r"\.(left|lchild)\b", code) and re.search(r"\.(right|rchild)\b", code):
        hit("二叉树", "节点有 left/right 指针")
    if re.search(r"\.next\b", code) and re.search(r"class\s+\w*(Node|List)\w*", code):
        hit("链表", "节点类有 next 指针")

    if re.search(r"\b(stack|stk|st)\s*=\s*\[\]", code) and re.search(r"\b(stack|stk|st)\.pop\(\)", code):
        hit("栈", "stack = [] 配合 stack.pop()")

    # 不认裸的 `prefix` 变量名：02001 Shortest Prefixes 的「前缀」是字符串前缀。
    if re.search(r"\b(pre_?sum|presum|psum|prefix_?sums?)\b|\baccumulate\(", code, re.I) or \
            re.search(r"\b(\w+)\[\s*(\w+)\s*\+\s*1\s*\]\s*=\s*\1\[\s*\2\s*\]\s*\+", code) or \
            re.search(r"\b(\w+)\[\s*(\w+)\s*\]\s*=\s*\1\[\s*\2\s*-\s*1\s*\]\s*\+\s*\w+\[", code):
        hit("前缀和", "前缀和数组 / accumulate")

    if re.search(r"\b(sieve|is_prime|isprime|primes)\b", code, re.I):
        hit("数论", "素数判断 / 筛法")
    return hits


# 题面明说的考点。只认确定的名字，不认「栈」这种单字（「客栈」「堆积木」都会误中）。
STATEMENT_WORDS = {
    "并查集": r"并查集|disjoint[ -]?set|\bdsu\b|union[ -]?find",
    "动态规划": r"动态规划|\bdp\b|记忆化搜索",
    "贪心": r"贪心|\bgreedy\b",
    "二分查找": r"二分查找|二分答案|二分搜索|binary search",
    "广度优先搜索": r"广度优先|宽度优先|宽搜|\bbfs\b",
    "深度优先搜索": r"深度优先|深搜|\bdfs\b",
    "回溯": r"回溯|backtrack",
    "拓扑排序": r"拓扑排序|topological",
    "最短路": r"最短路|dijkstra|floyd|bellman|\bspfa\b|shortest path",
    "最小生成树": r"最小生成树|kruskal|\bprim\b|minimum spanning",
    "堆": r"优先队列|最小堆|最大堆|\bheap\b|priority queue",
    "单调栈": None,  # 并入「栈」，见下
    "栈": r"单调栈|\bstack\b|栈",
    "队列": r"单调队列|\bqueue\b|队列",
    "双指针": r"双指针|滑动窗口|two pointers|sliding window",
    "前缀和": r"前缀和|prefix sum",
    "字典树": r"字典树|\btrie\b",
    "线段树/树状数组": r"线段树|树状数组|segment tree|fenwick",
    "KMP": r"\bkmp\b",
    "状态压缩": r"状态压缩|状压|bitmask",
    "数论": r"number theory|数论|素数筛|欧拉筛|埃氏筛",
}
# 题面提示里的 `tags: ...` 行（Codeforces 风格，134 道题有）单独解析，比全文匹配可信。
TAG_LINE = re.compile(r"tags?\s*[:：]\s*([^。\n]{1,160})", re.I)


def statement_topics(text):
    hits = {}
    tag_line = " ".join(m.group(1) for m in TAG_LINE.finditer(text)).casefold()
    hint = ""
    at = text.rfind(" 提示 ")
    if at >= 0:
        hint = text[at:].casefold()
    for topic, pattern in STATEMENT_WORDS.items():
        if pattern is None:
            continue
        # 单字「栈」「队列」只在提示/tags 里算数：描述里出现的多是情境词。
        # 其余考点名在描述里出现也算 —— 题面说「用并查集」就是用并查集。
        scope = (tag_line + " " + hint) if topic in ("栈", "队列", "堆", "数论") else (
            tag_line + " " + text.casefold())
        m = re.search(pattern, scope, re.I)
        if m:
            where = "tags 行" if m.group(0) in tag_line else ("提示" if hint and m.group(0) in hint else "题面")
            hits[topic] = f"{where}出现「{m.group(0)}」"
    return hits


def samplecode_paths(catalog):
    """题号 -> samplecode.py 路径。路径从 catalog 的测试数据位置推出，不去猜桶名。"""
    paths = {}
    for item in catalog["problems"]:
        for case in item.get("test_cases", []):
            folder = (MIRROR / case["input"]).parent
            while folder != MIRROR and not folder.name.endswith("_made"):
                folder = folder.parent
            code = folder / "samplecode.py"
            if folder != MIRROR and code.is_file():
                paths.setdefault(item["id"], code)
                break
    return paths


def build(explain=None):
    catalog = json.loads((MIRROR / "catalog.json").read_text(encoding="utf-8"))
    codes = samplecode_paths(catalog)
    evidence = {}
    for item in catalog["problems"]:
        pid = item["id"]
        found = evidence.setdefault(pid, {})
        page = MIRROR / "pages" / f"{item['book']}__{pid}.html"
        for topic, why in statement_topics(statement_plain_text(page)).items():
            found.setdefault(topic, f"[{item['book']}] {why}")
    for pid, path in codes.items():
        for topic, why in code_topics(path.read_text(encoding="utf-8", errors="replace")).items():
            evidence[pid].setdefault(topic, f"[samplecode] {why}")

    overrides = json.loads(OVERRIDES.read_text(encoding="utf-8")) if OVERRIDES.is_file() else {}
    for pid, topics in overrides.get("add", {}).items():
        for topic in topics:
            evidence.setdefault(pid, {})[topic] = "[人工] topics_overrides.json add"
    for pid, topics in overrides.get("remove", {}).items():
        for topic in topics:
            evidence.get(pid, {}).pop(topic, None)

    unknown = {t for found in evidence.values() for t in found} - set(TOPICS)
    if unknown:
        raise SystemExit(f"考点不在词表里：{sorted(unknown)}（先加进 TOPICS）")
    if explain:
        for topic, why in sorted(evidence.get(explain, {}).items(), key=lambda kv: TOPICS.index(kv[0])):
            print(f"{topic}\t{why}")
        print(f"samplecode: {codes.get(explain, '无')}")
        return None
    order = {t: i for i, t in enumerate(TOPICS)}
    topics = {pid: sorted(found, key=order.get) for pid, found in sorted(evidence.items()) if found}
    return evidence, codes, topics


def main(argv):
    if len(argv) >= 2 and argv[0] == "--explain":
        build(explain=argv[1])
        return 0
    result = build()
    evidence, codes, topics = result
    if argv and argv[0] == "--sample":
        topic, count = argv[1], int(argv[2]) if len(argv) > 2 else 10
        pool = sorted(pid for pid, found in evidence.items() if topic in found)
        for pid in random.Random(20261109).sample(pool, min(count, len(pool))):
            print(pid, evidence[pid][topic], codes.get(pid, ""))
        return 0
    OUTPUT.write_text(json.dumps({
        "_comment": "由 scripts/tag_topics.py 生成，勿手改；人工修正写 topics_overrides.json 后重新生成。"
                    "考点按参考代码特征与题面明说自动推断，可能不全。",
        "vocabulary": TOPICS,
        "topics": topics,
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    counts = {t: sum(t in v for v in topics.values()) for t in TOPICS}
    print(f"{len(topics)}/{len(evidence)} 个题号有考点；有参考代码的 {len(codes)} 个")
    print("  ".join(f"{t} {n}" for t, n in counts.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
