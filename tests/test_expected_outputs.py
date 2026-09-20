"""期望输出的**独立 oracle**：先用官方样例证明 oracle 自己是对的，再拿它核 `.out`。

为什么要有它。`scripts/build_codeforces_basic_data.py` 里的每道题是一个函数，
**同一段代码既造输入又算答案** —— 它算错了，21 组会自洽地全错，组数、去重、输入契约
这些判据一条都不会红。这类题（`data_status = generated_tests`）在仓库里有一百多道，
它们的期望输出此前没有任何外部锚点。

这份文件对已复核的题各写一份**算法不同的实现**，并且：

  1. 先拿 `data/openjudge/statements/<题号>.json` 里的**官方样例**跑这份实现 ——
     这是仓外事实，用来证明 oracle 本身没跑偏（2026-09-20 写 2184F 时就靠它抓到
     自己把无向边当成了父子边）；
  2. 再拿它逐组核 `.out`。

两道特判题（550C、1352A）的答案不唯一，这里改成按题意验证答案合法且最优。

**已知未覆盖**：`generated_tests` 里其余约 98 道题仍然只有生成器一家之言。
要么逐题补 oracle 到这里，要么把它们迁到单题流水线（`producecase.py` + `samplecode.py`
+ 官方样例断言）。
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIRROR = ROOT / "data" / "openjudge"
STATEMENTS = MIRROR / "statements"
CASES = MIRROR / "tests" / "codeforces"


def _ints(text):
    return [int(token) for token in text.split()]


# ------------------------------------------------------------ 精确比对的 oracle

def oracle_25a(text):
    values = _ints(text)[1:]
    odd = [index for index, value in enumerate(values) if value % 2]
    even = [index for index, value in enumerate(values) if value % 2 == 0]
    return f"{(odd if len(odd) == 1 else even)[0] + 1}\n"


def oracle_34b(text):
    lines = text.splitlines()
    _, m = _ints(lines[0])
    prices = sorted(_ints(lines[1]))
    return f"{-sum(price for price in prices[:m] if price < 0)}\n"


def oracle_363b(text):
    lines = text.splitlines()
    n, k = _ints(lines[0])
    heights = _ints(lines[1])
    best = current = sum(heights[:k])
    answer = 0
    for index in range(1, n - k + 1):
        current += heights[index + k - 1] - heights[index - 1]
        if current < best:
            best, answer = current, index
    return f"{answer + 1}\n"


def oracle_368b(text):
    lines = text.splitlines()
    n, m = _ints(lines[0])
    values = _ints(lines[1])
    suffix = [0] * (n + 1)
    seen = set()
    for index in range(n - 1, -1, -1):
        seen.add(values[index])
        suffix[index] = len(seen)
    return "".join(f"{suffix[int(line) - 1]}\n" for line in lines[2:2 + m])


def oracle_427a(text):
    officers = missing = 0
    for event in _ints(text.splitlines()[1]):
        if event == -1:
            if officers:
                officers -= 1
            else:
                missing += 1
        else:
            officers += event
    return f"{missing}\n"


def oracle_580c(text):
    lines = text.splitlines()
    n, m = _ints(lines[0])
    cats = _ints(lines[1])
    graph = [[] for _ in range(n + 1)]
    for line in lines[2:2 + n - 1]:
        x, y = _ints(line)
        graph[x].append(y)
        graph[y].append(x)
    answer = 0
    stack = [(1, 0, cats[0])]
    while stack:
        node, parent, run = stack.pop()
        if run > m:
            continue
        children = [child for child in graph[node] if child != parent]
        if not children:
            answer += 1
            continue
        for child in children:
            stack.append((child, node, run + 1 if cats[child - 1] else 0))
    return f"{answer}\n"


def oracle_615a(text):
    lines = text.splitlines()
    n, m = _ints(lines[0])
    lit = set()
    for line in lines[1:1 + n]:
        lit |= set(_ints(line)[1:])
    return ("YES" if len(lit) == m else "NO") + "\n"


def oracle_986b(text):
    lines = text.splitlines()
    n = int(lines[0])
    tree = [0] * (n + 2)

    def update(index):
        while index <= n:
            tree[index] += 1
            index += index & -index

    def query(index):
        total = 0
        while index > 0:
            total += tree[index]
            index -= index & -index
        return total

    inversions = 0
    for position, value in enumerate(_ints(lines[1])):
        inversions += position - query(value)
        update(value)
    # Petr 洗 3n 次、Alex 洗 7n+1 次，奇偶性分别是 n 与 n+1。
    return ("Petr" if inversions % 2 == n % 2 else "Um_nik") + "\n"


def oracle_1520d(text):
    import collections
    values = _ints(text)
    position, out = 1, []
    for _ in range(values[0]):
        n = values[position]
        row = values[position + 1:position + 1 + n]
        position += 1 + n
        counts = collections.Counter(value - index for index, value in enumerate(row))
        out.append(f"{sum(count * (count - 1) // 2 for count in counts.values())}\n")
    return "".join(out)


def oracle_1749c(text):
    """Alice 能赢的最大 k。用堆来模拟，和生成器的 `bisect` 版不是同一份代码。

    **这道题是官方样例锚点的价值所在**：2026-09-20 之前生成器算的是一个不相干的贪心
    （排序后 `value > answer` 就加一），21 组里 20 组答案是错的，而所有既有判据全绿 ——
    官方样例第二组 `4 4 4 4` 应为 0、旧写法给 4，一跑就露。
    """
    import heapq
    values = _ints(text)
    position, out = 1, []
    for _ in range(values[0]):
        n = values[position]
        row = values[position + 1:position + 1 + n]
        position += 1 + n

        def wins(k):
            # 小根堆存「还能用的数」，大于当前上限的数一旦被 Bob 顶上去就再也回不来。
            usable = sorted(row)
            for limit in range(k, 0, -1):
                pick = None
                for index in range(len(usable) - 1, -1, -1):
                    if usable[index] <= limit:
                        pick = index
                        break
                if pick is None:
                    return False
                usable.pop(pick)
                if usable:
                    heap = list(usable)
                    heapq.heapify(heap)
                    smallest = heapq.heappop(heap)
                    heapq.heappush(heap, smallest + limit)
                    usable = sorted(heap)
            return True

        out.append(f"{next((k for k in range(n, -1, -1) if wins(k)), 0)}\n")
    return "".join(out)


def oracle_1850h(text):
    values = _ints(text)
    position, out = 1, []
    for _ in range(values[0]):
        n, m = values[position], values[position + 1]
        position += 2
        parent = list(range(n + 1))
        potential = [0] * (n + 1)

        def find(node):
            root, shift = node, 0
            while parent[root] != root:
                shift += potential[root]
                root = parent[root]
            while parent[node] != root:
                parent[node], potential[node], node, shift = (
                    root, shift, parent[node], shift - potential[node])
            return root, shift

        ok = True
        for _ in range(m):
            a, b, d = values[position:position + 3]
            position += 3
            root_a, shift_a = find(a)
            root_b, shift_b = find(b)
            if root_a == root_b:
                if shift_a - shift_b != d:
                    ok = False
            else:
                parent[root_a] = root_b
                potential[root_a] = shift_b + d - shift_a
        out.append(("YES" if ok else "NO") + "\n")
    return "".join(out)


def oracle_2184f(text):
    """可达的「抖动次数」集合：叶子 {1}，内部点 {1} ∪ {各子树可达次数之和}。

    生成器走的是另一条路（枚举 2^n 个点集）。**输入里的边是无向的**，根是 1 号点 ——
    2026-09-20 第一版 oracle 把 `u v` 当成父子边写，官方样例第三组立刻对不上。
    """
    values = _ints(text)
    position, out = 1, []
    for _ in range(values[0]):
        n = values[position]
        position += 1
        graph = [[] for _ in range(n + 1)]
        for _ in range(n - 1):
            u, v = values[position:position + 2]
            position += 2
            graph[u].append(v)
            graph[v].append(u)

        def reach(node, parent):
            children = [child for child in graph[node] if child != parent]
            if not children:
                return {1}
            sums = {0}
            for child in children:
                child_reach = reach(child, node)
                sums = {a + b for a in sums for b in child_reach}
            return {1} | sums

        out.append(("YES" if any(k % 3 == 0 for k in reach(1, 0)) else "NO") + "\n")
    return "".join(out)


ORACLES = {
    "25A": oracle_25a, "34B": oracle_34b, "363B": oracle_363b, "368B": oracle_368b,
    "427A": oracle_427a, "580C": oracle_580c, "615A": oracle_615a, "986B": oracle_986b,
    "1520D": oracle_1520d, "1749C": oracle_1749c, "1850H": oracle_1850h,
    "2184F": oracle_2184f,
}


# ------------------------------------------------- 答案不唯一的题：按题意验证

def verify_550c(text, answer):
    """删掉若干位得到能被 8 整除的数，答案不唯一，只能验证合法性与存在性。"""
    digits = text.strip()
    exists = any(int("".join(digits[i] for i in range(len(digits)) if mask >> i & 1)) % 8 == 0
                 for mask in range(1, 1 << len(digits)))
    tokens = answer.split()
    if tokens[0].upper() == "YES":
        if not exists:
            return "答案说 YES，但不存在能被 8 整除的子序列"
        witness = tokens[1]
        stream = iter(digits)
        if not all(char in stream for char in witness):
            return f"{witness} 不是 {digits} 的子序列"
        if int(witness) % 8:
            return f"{witness} 不能被 8 整除"
        if len(witness) > 1 and witness[0] == "0":
            return f"{witness} 有前导零"
    elif exists:
        return "答案说 NO，但存在能被 8 整除的子序列"
    return None


def verify_1352a(text, answer):
    """拆成最少个「圆数」之和；拆法不唯一，个数必须最少（= 非零数位个数）。"""
    values = text.split()
    tokens = answer.split()
    position, cursor = 1, 0
    for _ in range(int(values[0])):
        n = values[position]
        position += 1
        count = int(tokens[cursor])
        cursor += 1
        parts = [int(token) for token in tokens[cursor:cursor + count]]
        cursor += count
        if count != sum(1 for char in n if char != "0"):
            return f"{n}: 用了 {count} 个圆数，最少是 {sum(1 for c in n if c != '0')} 个"
        if sum(parts) != int(n):
            return f"{n}: 各项之和是 {sum(parts)}"
        bad = [part for part in parts if not (part and set(str(part)[1:]) <= {"0"})]
        if bad:
            return f"{n}: {bad[0]} 不是圆数"
    return None


VERIFIERS = {"550C": verify_550c, "1352A": verify_1352a}

# 2026-09-20 起，逐题补的 oracle 放在 `tests/cf_oracles.py`（这个文件会长到上百道题，
# 判据本身留在这里，题解搬过去）。两边的注册表在这里合并，检查方式完全一样。
try:
    from cf_oracles import ORACLES as _MORE_ORACLES, VERIFIERS as _MORE_VERIFIERS
except ImportError:                                            # 直接 `python3 tests/...`
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from cf_oracles import ORACLES as _MORE_ORACLES, VERIFIERS as _MORE_VERIFIERS
ORACLES.update(_MORE_ORACLES)
VERIFIERS.update(_MORE_VERIFIERS)


def case_insensitive_problems():
    """catalog 里标了 `case_insensitive_tokens` 的题：判题就是大小写不敏感的，
    这里的比对要用同一口径，否则 `Yes`/`YES` 会被当成不一致。"""
    catalog = json.loads((MIRROR / "catalog.json").read_text(encoding="utf-8"))
    return {item["id"] for item in catalog["problems"]
            if item.get("book") == "codeforces"
            and item.get("comparison") == "case_insensitive_tokens"}


def normalize(text, problem_id, loose):
    tokens = text.split()
    return [token.lower() for token in tokens] if problem_id in loose else tokens


def samples(problem_id):
    data = json.loads((STATEMENTS / f"{problem_id}.json").read_text(encoding="utf-8"))
    return data.get("samples") or []


def data_cases(problem_id):
    directory = CASES / f"{problem_id}_made" / "data"
    for path in sorted(directory.glob("*.in"), key=lambda item: int(item.stem)):
        yield path.name, path.read_text(encoding="utf-8"), \
            path.with_suffix(".out").read_text(encoding="utf-8")


class OracleTests(unittest.TestCase):
    def test_oracles_reproduce_the_official_samples(self):
        """先证明 oracle 自己是对的 —— 官方样例是这里唯一的仓外事实。"""
        loose = case_insensitive_problems()
        for problem_id, oracle in ORACLES.items():
            rows = samples(problem_id)
            self.assertTrue(rows, f"{problem_id} 镜像题面里没有官方样例")
            for index, row in enumerate(rows):
                got = oracle(row["input"])
                self.assertEqual(normalize(got, problem_id, loose),
                                 normalize(row["output"], problem_id, loose),
                                 f"{problem_id} 官方样例 {index} 对不上")

    def test_verifiers_accept_the_official_samples(self):
        for problem_id, verify in VERIFIERS.items():
            rows = samples(problem_id)
            self.assertTrue(rows, f"{problem_id} 镜像题面里没有官方样例")
            for index, row in enumerate(rows):
                self.assertIsNone(verify(row["input"], row["output"]),
                                  f"{problem_id} 官方样例 {index} 被判据拒了")

    def test_every_generated_problem_has_an_oracle_or_a_written_reason(self):
        """覆盖率本身是判据：`generated_tests` 的题答案只有生成器一家之言。

        2026-09-20 给这 113 道题逐题补了独立 oracle，当场抓到 11 道答案或输入是错的。
        新加的题如果走中央生成器，就必须在 `tests/cf_oracles.py` 里配一份 oracle，
        或者把「为什么不用核」写进 `UNCOVERED` —— 一个缺陷被接受和被忽略，
        从代码上看一模一样，区别只在有没有写下来。
        """
        from cf_oracles import UNCOVERED
        covered = set(ORACLES) | set(VERIFIERS)
        missing = []
        for item in self.rows_by_book("codeforces"):
            if item.get("data_status") != "generated_tests":
                continue
            problem_id = item["id"]
            if problem_id in covered or problem_id in UNCOVERED:
                continue
            missing.append(problem_id)
        self.assertEqual(missing, [], f"这些题没有独立 oracle，也没写明理由：{missing}")
        for problem_id, reason in UNCOVERED.items():
            self.assertTrue(reason.strip(), f"{problem_id} 的豁免理由不能是空的")

    def rows_by_book(self, book):
        catalog = json.loads((MIRROR / "catalog.json").read_text(encoding="utf-8"))
        return [item for item in catalog["problems"] if item.get("book") == book]

    def test_expected_outputs_match_an_independent_oracle(self):
        failures = []
        loose = case_insensitive_problems()
        for problem_id, oracle in ORACLES.items():
            for name, text, expected in data_cases(problem_id):
                if (normalize(oracle(text), problem_id, loose)
                        != normalize(expected, problem_id, loose)):
                    failures.append(f"{problem_id}/{name}: oracle 与 .out 不一致")
        for problem_id, verify in VERIFIERS.items():
            for name, text, expected in data_cases(problem_id):
                message = verify(text, expected)
                if message:
                    failures.append(f"{problem_id}/{name}: {message}")
        self.assertEqual(failures, [], "\n".join(failures))


if __name__ == "__main__":
    unittest.main()
