"""输入契约：**照题面逐条写**的校验器，跑遍这些题当前在判的每一组数据。

为什么要有它。2026-09-20 全库按题面核对输入约束，查出 23 道题的数据越出题面
（Codeforces 14 道 + 镜像题库 9 道）。这类缺陷的共同点是**所有既有闸门都是绿的**：
生成器自洽、参考实现能复现 `.out`、组数够、第 0 组与样例相符 —— 题面从没进过这个环。

更要命的是它的上一版修法：`7f6a07bd` 直接手改了 14 道题的 `.in/.out`，没回头改生成器，
于是 1850H 的 21 组输入全被写成 `1 NaN`（判题时等价于「输出 YES 就能过」），
456A/2184F 出现重复组，另外 11 道的数据与生成器彻底对不上 —— 重跑一次生成器就会
把手改的内容整片冲掉。**所以这份文件校验的是数据本身**，与生成器无关：
生成器改错了、有人手改了数据、下一轮重建跑偏了，这里都会红。

写法约定：每个校验器读一整份输入文本，返回 `None` 表示合规，返回一句话表示哪条越界。
引用题面时写明数值，方便对着镜像题面逐字复核。
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIRROR = ROOT / "data" / "openjudge"


def numbers(text):
    return [int(token) for token in text.split()]


def is_tree(count, edges):
    parent = list(range(count + 1))

    def find(node):
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    if len(edges) != count - 1:
        return False
    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        parent[ra] = rb
    return len({find(node) for node in range(1, count + 1)}) == 1


# ---------------------------------------------------------------- Codeforces

def check_25a(text):
    lines = text.splitlines()
    if len(lines) != 2:
        return f"应为 2 行，实际 {len(lines)} 行"
    n = int(lines[0])
    values = numbers(lines[1])
    if not 3 <= n <= 100:
        return f"n={n} 越出题面 3<=n<=100"
    if len(values) != n:
        return f"第二行 {len(values)} 个数，n={n}"
    if any(not 1 <= value <= 100 for value in values):
        return f"数值 {max(values)} 越出题面「不超过 100 的自然数」"
    odd = sum(value % 2 for value in values)
    if odd not in (1, n - 1):
        return f"题面保证恰有一个数奇偶性不同，实际奇数 {odd} 个"
    return None


def check_34b(text):
    lines = text.splitlines()
    n, m = numbers(lines[0])
    if not 1 <= m <= n <= 100:
        return f"n={n} m={m} 越出题面 1<=m<=n<=100"
    prices = numbers(lines[1])
    if len(prices) != n:
        return f"第二行 {len(prices)} 个价格，n={n}"
    if any(not -1000 <= price <= 1000 for price in prices):
        return "价格越出题面 -1000<=a_i<=1000"
    return None


def check_363b(text):
    lines = text.splitlines()
    n, k = numbers(lines[0])
    if not 1 <= n <= 150_000:
        return f"n={n} 越出题面 1<=n<=1.5*10^5"
    if not 1 <= k <= n:
        return f"k={k} 越出题面 1<=k<=n（n={n}）"
    heights = numbers(lines[1])
    if len(heights) != n:
        return f"第二行 {len(heights)} 个高度，n={n}"
    if any(not 1 <= height <= 100 for height in heights):
        return f"高度 {max(heights)} 越出题面 1<=h_i<=100"
    return None


def check_368b(text):
    lines = text.splitlines()
    head = numbers(lines[0])
    if len(head) != 2:
        return f"第一行应为 n 和 m 两个整数，实际 {len(head)} 个"
    n, m = head
    if not 1 <= n <= 10 ** 5 or not 1 <= m <= 10 ** 5:
        return f"n={n} m={m} 越出题面 1<=n,m<=10^5"
    values = numbers(lines[1])
    if len(values) != n:
        return f"第二行 {len(values)} 个元素，n={n}"
    if any(not 1 <= value <= 10 ** 5 for value in values):
        return "元素越出题面 1<=a_i<=10^5"
    queries = [numbers(line) for line in lines[2:] if line.strip()]
    if len(queries) != m:
        return f"查询行 {len(queries)} 行，m={m}"
    if any(len(row) != 1 or not 1 <= row[0] <= n for row in queries):
        return f"查询越出题面 1<=l_i<=n（n={n}）"
    return None


def check_427a(text):
    lines = text.splitlines()
    n = int(lines[0])
    if not 1 <= n <= 10 ** 5:
        return f"n={n} 越出题面 1<=n<=10^5"
    events = numbers(lines[1])
    if len(events) != n:
        return f"第二行 {len(events)} 个事件，n={n}"
    bad = [event for event in events if event != -1 and not 1 <= event <= 10]
    if bad:
        return f"事件 {bad[0]} 越出题面「-1 或正数，且一次至多招募 10 人」"
    return None


def check_550c(text):
    lines = text.splitlines()
    if len(lines) != 1:
        return f"应为 1 行，实际 {len(lines)} 行"
    digits = lines[0]
    if not digits.isdigit():
        return "题面：单行一个非负整数"
    if len(digits) > 100:
        return f"长度 {len(digits)} 越出题面 100 位"
    if len(digits) > 1 and digits[0] == "0":
        return "题面明写不含前导零"
    return None


def check_580c(text):
    lines = text.splitlines()
    n, m = numbers(lines[0])
    if not 2 <= n <= 10 ** 5:
        return f"n={n} 越出题面 2<=n<=10^5"
    if not 1 <= m <= n:
        return f"m={m} 越出题面 1<=m<=n（n={n}）"
    cats = numbers(lines[1])
    if len(cats) != n or any(cat not in (0, 1) for cat in cats):
        return "第二行应为 n 个 0/1"
    edges = [tuple(numbers(line)) for line in lines[2:] if line.strip()]
    if any(len(edge) != 2 or not 1 <= edge[0] <= n or not 1 <= edge[1] <= n
           or edge[0] == edge[1] for edge in edges):
        return "边越出题面 1<=x_i,y_i<=n 且 x_i!=y_i"
    if not is_tree(n, edges):
        return "题面保证给定的边构成一棵树"
    return None


def check_615a(text):
    lines = [line for line in text.splitlines() if line.strip() != "" or True]
    n, m = numbers(lines[0])
    if not 1 <= n <= 100 or not 1 <= m <= 100:
        return f"n={n} m={m} 越出题面 1<=n,m<=100"
    rows = lines[1:]
    if len(rows) != n:
        return f"按钮行 {len(rows)} 行，n={n}"
    for row in rows:
        values = numbers(row)
        count = values[0]
        if not 0 <= count <= m:
            return f"x_i={count} 越出题面 0<=x_i<=m（m={m}）"
        if len(values) - 1 != count:
            return f"x_i={count} 与实际 {len(values) - 1} 个灯泡编号不符"
        if any(not 1 <= bulb <= m for bulb in values[1:]):
            return f"灯泡编号越出题面 1<=y_ij<=m（m={m}）"
    return None


def check_986b(text):
    lines = text.splitlines()
    n = int(lines[0])
    if not 10 ** 3 <= n <= 10 ** 6:
        return f"n={n} 越出题面 10^3<=n<=10^6"
    perm = numbers(lines[1])
    if sorted(perm) != list(range(1, n + 1)):
        return "第二行应为 1..n 的排列"
    return None


def _multi_case(text, per_case, limit):
    values = numbers(text)
    position = 0
    t = values[position]
    position += 1
    if not 1 <= t <= limit:
        return f"t={t} 越出题面 1<=t<={limit}"
    for _ in range(t):
        message, position = per_case(values, position)
        if message:
            return message
    if position != len(values):
        return f"读完 {t} 组后还剩 {len(values) - position} 个数"
    return None


def check_1352a(text):
    def case(values, position):
        n = values[position]
        if not 1 <= n <= 10 ** 4:
            return f"n={n} 越出题面 1<=n<=10^4", position
        return None, position + 1
    return _multi_case(text, case, 10 ** 4)


def check_1520d(text):
    def case(values, position):
        n = values[position]
        if not 1 <= n <= 2 * 10 ** 5:
            return f"n={n} 越出题面 1<=n<=2*10^5", position
        row = values[position + 1:position + 1 + n]
        if any(not 1 <= value <= n for value in row):
            return f"a_i 越出题面 1<=a_i<=n（n={n}）", position
        return None, position + 1 + n
    return _multi_case(text, case, 10 ** 4)


def check_1749c(text):
    def case(values, position):
        n = values[position]
        if not 1 <= n <= 100:
            return f"n={n} 越出题面 1<=n<=100", position
        row = values[position + 1:position + 1 + n]
        if any(not 1 <= value <= n for value in row):
            return f"a_i 越出题面 1<=a_i<=n（n={n}）", position
        return None, position + 1 + n
    return _multi_case(text, case, 100)


def check_1850h(text):
    def case(values, position):
        n, m = values[position], values[position + 1]
        if not 2 <= n <= 2 * 10 ** 5:
            return f"n={n} 越出题面 2<=n<=2*10^5", position
        if not 1 <= m <= n:
            return f"m={m} 越出题面 1<=m<=n（n={n}）", position
        position += 2
        for _ in range(m):
            a, b, d = values[position:position + 3]
            if a == b or not 1 <= a <= n or not 1 <= b <= n:
                return f"条件 ({a},{b}) 越出题面 a_i!=b_i 且 1<=a_i,b_i<=n", position
            if not -10 ** 9 <= d <= 10 ** 9:
                return f"d_i={d} 越出题面 |d_i|<=10^9", position
            position += 3
        return None, position
    return _multi_case(text, case, 100)


def check_2184f(text):
    def case(values, position):
        n = values[position]
        if not 2 <= n <= 2 * 10 ** 5:
            return f"n={n} 越出题面 2<=n<=2*10^5", position
        position += 1
        edges = []
        for _ in range(n - 1):
            u, v = values[position:position + 2]
            if u == v or not 1 <= u <= n or not 1 <= v <= n:
                return f"边 ({u},{v}) 越出题面 1<=u,v<=n 且 u!=v", position
            edges.append((u, v))
            position += 2
        if not is_tree(n, edges):
            return "题面保证每组数据是一棵树", position
        return None, position
    return _multi_case(text, case, 10 ** 4)


def check_456a(text):
    lines = text.splitlines()
    n = int(lines[0])
    if not 1 <= n <= 10 ** 5:
        return f"n={n} 越出题面 1<=n<=10^5"
    rows = [numbers(line) for line in lines[1:] if line.strip()]
    if len(rows) != n or any(len(row) != 2 for row in rows):
        return f"应为 n 行、每行两个整数，实际 {len(rows)} 行"
    if any(not 1 <= value <= n for row in rows for value in row):
        return f"价格/质量越出题面 1<=a_i,b_i<=n（n={n}）"
    if len({row[0] for row in rows}) != n or len({row[1] for row in rows}) != n:
        return "题面保证 a_i 两两不同、b_i 两两不同"
    return None


def check_1742a(text):
    def case(values, position):
        row = values[position:position + 3]
        if any(not 0 <= value <= 20 for value in row):
            return f"{row} 越出题面 0<=a,b,c<=20", position
        return None, position + 3
    return _multi_case(text, case, 9261)


# ------------------------------------------------------------------ 镜像题库

def check_02943(text):
    lines = [line for line in text.splitlines() if line.strip()]
    n = int(lines[0])
    if not 1 < n < 100:
        return f"N={n} 越出题面 1 < N < 100"
    rows = lines[1:]
    if len(rows) != n:
        return f"白鼠行 {len(rows)} 行，N={n}"
    weights = []
    for row in rows:
        weight, color = row.split()
        weights.append(int(weight))
        if not 1 <= int(weight) <= 1000:
            return f"重量 {weight} 越出题面「不大于 1000 的正整数」"
        if len(color) > 10:
            return f"颜色字符串 {color} 超过题面的 10 个字符"
    if len(set(weights)) != n:
        return "题面：白鼠的重量各不相同"
    return None


def check_02092(text):
    lines = [line for line in text.splitlines() if line.strip()]
    position = 0
    while True:
        n, m = numbers(lines[position])
        position += 1
        if n == 0 and m == 0:
            break
        if not 2 <= n <= 500 or not 2 <= m <= 500:
            return f"N={n} M={m} 越出题面 2<=N<=500、2<=M<=500"
        counts = {}
        for _ in range(n):
            row = numbers(lines[position])
            position += 1
            if len(row) != m:
                return f"一张周榜 {len(row)} 个编号，M={m}"
            if len(set(row)) != m:
                return "题面：每张周榜的选手编号互不相同"
            if any(not 1 <= player <= 10000 for player in row):
                return "选手编号越出题面 1..10000"
            for player in row:
                counts[player] = counts.get(player, 0) + 1
        best = max(counts.values())
        if sum(value == best for value in counts.values()) != 1:
            return "题面保证：每组数据恰好一个最佳选手"
        if all(value == best for value in counts.values()):
            return "题面保证：每组数据至少一个次佳选手"
    if position != len(lines):
        return "0 0 之后还有内容"
    return None


def check_04080(text):
    lines = [line for line in text.splitlines() if line.strip()]
    n = int(lines[0])
    if not 2 <= n <= 100:
        return f"n={n} 越出题面 2<=N<=100"
    weights = numbers(lines[1])
    if len(weights) != n:
        return f"第二行 {len(weights)} 个权值，n={n}"
    return None


def check_04137(text):
    lines = [line for line in text.splitlines() if line.strip()]
    t = int(lines[0])
    if not 1 <= t <= 10:
        return f"t={t} 越出题面 t <= 10"
    if len(lines) - 1 != t:
        return f"数据行 {len(lines) - 1} 行，t={t}"
    for line in lines[1:]:
        digits, k = line.split()
        value = int(digits)
        if not 0 < value < 10 ** 9:
            return f"n={digits} 越出题面 0 < n < 10^9"
        if "0" in digits:
            return f"n={digits} 违反题面「每个数位上数字均不为 0」"
        if not 0 < int(k) < len(digits):
            return f"k={k} 越出题面 0 < k < m（m={len(digits)}）"
    return None


def check_07604(text):
    lines = text.splitlines()
    n = int(lines[0])
    if not 1 < n < 5:
        return f"n={n} 越出题面 1 < n < 5"
    text_line = lines[1]
    if not text_line.isalpha():
        return "题面：字符串只包含大小写字母"
    if len(text_line) > 500:
        return f"字符串长度 {len(text_line)} 超过题面的 500"
    if len(text_line) < n:
        return f"字符串长度 {len(text_line)} 不足以构成一个 {n}-gram"
    return None


def check_19962(text):
    lines = text.splitlines()
    n = int(lines[0])
    if not 1 <= n <= 100_000:
        return f"N={n} 越出题面 1 <= N <= 100000"
    values = numbers(lines[1])
    if len(values) != n:
        return f"第二行 {len(values)} 个坐标，N={n}"
    if any(not 1 <= value <= 100_000 for value in values):
        return f"坐标 {min(values)} 越出题面 1 <= Ai <= 100000"
    return None


def check_29853(text):
    lines = text.splitlines()
    n = int(lines[0])
    if not 1 <= n <= 1000:
        return f"N={n} 越出题面 1<=N<=1000"
    for index, line in enumerate(lines[1:3]):
        values = numbers(line)
        if len(values) != n:
            return f"第 {index + 2} 行 {len(values)} 个难度，N={n}"
        if any(not 1 <= value <= 1000 for value in values):
            return f"难度 {min(values)} 越出题面 1<=Ai,Bi<=10^3"
    return None


def check_30085(text):
    lines = [line for line in text.splitlines() if line.strip()]
    w = int(lines[0])
    if not 80 <= w <= 200:
        return f"w={w} 越出题面 80 <= w <= 200"
    n = int(lines[1])
    if not 1 <= n <= 3 * 10 ** 4:
        return f"n={n} 越出题面 1 <= n <= 3*10^4"
    prices = [int(line) for line in lines[2:]]
    if len(prices) != n:
        return f"价格 {len(prices)} 行，n={n}"
    if any(not 5 <= price <= w for price in prices):
        return f"价格越出题面 5 <= Pi <= w（w={w}）"
    return None


def check_30192(text):
    lines = [line for line in text.splitlines() if line.strip()]
    w, n = numbers(lines[0])
    if not 100 <= w <= 400:
        return f"W={w} 越出题面 100 <= W <= 400"
    if not 1 <= n <= 16:
        return f"n={n} 越出题面 1 <= n <= 16"
    rows = lines[1:]
    if len(rows) != n:
        return f"队员行 {len(rows)} 行，n={n}"
    for row in rows:
        time, weight = numbers(row)
        if not 1 <= time <= 50:
            return f"t={time} 越出题面 1 <= t <= 50"
        if not 10 <= weight <= 100:
            return f"w={weight} 越出题面 10 <= w <= 100"
    return None


def check_04101(text):
    lines = [line for line in text.splitlines() if line != ""]
    k = int(lines[0])
    if k < 1:
        return f"k={k}，题面：第一行 k 表示有 k 组测试输入"
    position = 1
    for _ in range(k):
        n = int(lines[position])
        position += 1
        if not 3 <= n <= 30:
            return f"n={n} 越出题面 3 <= n <= 30"
        rows = lines[position:position + n]
        position += n
        if len(rows) != n or any(len(row) != n for row in rows):
            return f"地图不是 {n}x{n}"
        extra = {ch for row in rows for ch in row} - set("rb#")
        if extra:
            return f"地图里出现题面没有定义的字符 {sorted(extra)}（题面只有 '#'、'r'、'b'）"
    if position != len(lines):
        return f"读完 {k} 组后还剩 {len(lines) - position} 行"
    return None


def check_01958(text):
    """题面：「There is no input.」——输入必须是空的。

    2026-09-20 之前的一版把「21 份输入都是空文件」当成缺陷「修」掉了，给每组塞了一个
    n 并把输出改成一个数；而正解是不读输入、直接打印 n=1..12 的 12 行答案，于是
    **任何正确程序都会 21 组全错**。这条用例把题面这一句钉住。
    """
    if text.strip() != "":
        return f"题面写的是「There is no input.」，实际输入是 {text[:20]!r}"
    return None


VALIDATORS = {
    ("practice", "01958"): check_01958,
    ("codeforces", "25A"): check_25a,
    ("codeforces", "34B"): check_34b,
    ("codeforces", "363B"): check_363b,
    ("codeforces", "368B"): check_368b,
    ("codeforces", "427A"): check_427a,
    ("codeforces", "550C"): check_550c,
    ("codeforces", "580C"): check_580c,
    ("codeforces", "615A"): check_615a,
    ("codeforces", "986B"): check_986b,
    ("codeforces", "1352A"): check_1352a,
    ("codeforces", "1520D"): check_1520d,
    ("codeforces", "1749C"): check_1749c,
    ("codeforces", "1850H"): check_1850h,
    ("codeforces", "2184F"): check_2184f,
    ("codeforces", "456A"): check_456a,
    ("codeforces", "1742A"): check_1742a,
    ("practice", "02943"): check_02943,
    ("dsapre", "02092"): check_02092,
    ("2024sp_routine", "04080"): check_04080,
    ("2024sp_routine", "04137"): check_04137,
    ("practice", "07604"): check_07604,
    ("practice", "19962"): check_19962,
    ("pctbook", "M29853"): check_29853,
    ("practice", "30085"): check_30085,
    ("practice", "30192"): check_30192,
    ("pctbook", "M05585"): check_04101,
}


# 唯一一条豁免：题面写死「没有输入」的题，21 组输入必然全同 —— 这是题面的结论，
# 不是数据塌陷。豁免写在这里而不是把判据放宽，理由与 full_sweep 的例外表一致：
# 一个缺陷被接受和被忽略，从代码上看一模一样，区别只在有没有写下来。
DISTINCTNESS_EXEMPT = {("practice", "01958"): "题面：There is no input."}


class InputContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        catalog = json.loads((MIRROR / "catalog.json").read_text(encoding="utf-8"))
        cls.rows = {(item["book"], item["id"]): item for item in catalog["problems"]}

    def test_every_case_satisfies_the_statement(self):
        failures = []
        for key, check in VALIDATORS.items():
            row = self.rows.get(key)
            self.assertIsNotNone(row, f"{key} 不在 catalog 里")
            cases = row.get("test_cases") or []
            self.assertTrue(cases, f"{key} 没有在判数据")
            for case in cases:
                text = (MIRROR / case["input"]).read_text(encoding="utf-8")
                try:
                    message = check(text)
                except (ValueError, IndexError) as error:
                    # 读不成题面说的形状本身就是一种越界（1850H 被手改成 `1 NaN`
                    # 那次，整数解析直接抛异常），所以按失败记，不让它把用例打断。
                    message = f"按题面的输入格式读不下来：{error!r}"
                if message:
                    failures.append(f"{key[0]}/{key[1]} {case['input']}: {message}")
        self.assertEqual(failures, [], "\n".join(failures))

    def test_cases_are_distinct(self):
        """手改数据的另一种塌陷：21 组里出现重复（456A/2184F 上真的发生过）。"""
        for key in VALIDATORS:
            if key in DISTINCTNESS_EXEMPT:
                continue
            cases = self.rows[key].get("test_cases") or []
            texts = {(MIRROR / case["input"]).read_bytes() for case in cases}
            self.assertEqual(len(texts), len(cases), f"{key} 有重复输入")


if __name__ == "__main__":
    unittest.main()
