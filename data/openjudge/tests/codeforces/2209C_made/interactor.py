"""Codeforces 2209C Find the Zero 交互器（支持自适应）。

用法：python3 -I interactor.py <隐藏数据> <参考答案（不读）>

隐藏数据格式：
    t
    每组一行，二选一：
      n F a_1 ... a_2n      固定数组（非自适应）：1..n 各一次，其余 n 个 0
      n A q s               自适应对手：q ∈ [0,100]，s 为种子
第 0 组（题面样例）两组都是 F，逐字复现 Note 的回应。

交互：先发 t，每组发 n。选手输出 `? i j`（1 ≤ i, j ≤ 2n，i ≠ j），回应 1（a_i = a_j）或 0；
`! k` 结束本组，a_k 必须为 0。每组 `?` 至多 n+1 次。按 token 读。最后一组之后立即退出。

自适应对手：「一致」= 存在满足全部回答的数组。非零值互不相同，所以回答 1 ⇔ 两处都是 0。
记 F = 被回答 1 的询问涉及的位置（必为 0），G = 回答 0 的询问边（两端不能都为 0）。
一致 ⇔ 存在大小为 n 的零位置集 Z ⊇ F 且 Z 在 G 中独立。
引理（询问总数 Q ≤ n+1 时）：一致 ⇔ F 在 G 中独立且 |F| ≤ n。
  证：必要性显然。充分性：取非零集 N = G 中与 F 相邻的点 ∪ 其余每条边各取一端，
  |N| ≤ |E(G)| ≤ Q − q1。F 非空时 q1 ≥ 1，|N| ≤ n；F 为空时 |E(G)| ≤ n+1，若恰为 n+1
  则 2n 个点上不可能是匹配，必有两边共点，|N| ≤ n。再用 F 以外的点把 N 补到 n 个
  （需要 2n − |F| ≥ n）。
于是：回答 0 可行 ⇔ i、j 不同时在 F；回答 1 可行 ⇔ F∪{i,j} 在 G 中独立且 |F∪{i,j}| ≤ n。
对手每次在两者都可行时以 q% 概率答 1，否则答 0（q = 0 即「能答 0 就答 0」，信息最少）。
报告 k 时：若存在一致数组使 a_k ≠ 0 就判 WA。判定：k ∈ F 则必为 0；否则强制非零集
C = N_G(F) ∪ {k}，剩余图 H = G 去掉 C（及 F）上的点，需 |C| + MVC(H) ≤ n。
令 d = |E(H)| − (n − |C|)，需 Σ_分量 (边数 − MVC) ≥ d；由计数 d ≤ 2 − q1 ≤ 2，
而连通分量边数 ≥ 4 时 边数 − MVC ≥ 2（最大度 ≥ 3 取该点，否则是路/环），
边数 ≤ 3 的分量暴力求 MVC，因此判定是精确的。

退出码：0 通过，42 答案错误。stderr 最后一行是给学生的一句话，不含测试数据。
"""
import random
import re
import sys

INT = re.compile(r"-?\d{1,19}\Z")


def wrong(message):
    print(message, file=sys.stderr)
    sys.exit(42)


def say(text):
    try:
        sys.stdout.write(text)
        sys.stdout.flush()
    except (BrokenPipeError, OSError):
        wrong("程序提前结束")


def tokens():
    while True:
        try:
            line = sys.stdin.readline()
        except (OSError, UnicodeDecodeError, ValueError):
            line = ""
        if not line:
            return
        yield from line.split()


class Adversary:
    """维护 F（必为 0 的位置）与 G（回答 0 的边），保证始终一致。"""

    def __init__(self, n, q, seed):
        self.n, self.q = n, q
        self.rng = random.Random(seed)
        self.forced = set()
        self.adj = {}

    def _edge(self, i, j):
        self.adj.setdefault(i, set()).add(j)
        self.adj.setdefault(j, set()).add(i)

    def can_zero(self, i, j):
        return not (i in self.forced and j in self.forced)

    def can_one(self, i, j):
        grown = self.forced | {i, j}
        if len(grown) > self.n:
            return False
        if j in self.adj.get(i, ()):
            return False
        for v in (i, j):
            if v not in self.forced and any(u in grown for u in self.adj.get(v, ())):
                return False
        return True

    def answer(self, i, j):
        zero, one = self.can_zero(i, j), self.can_one(i, j)
        if zero and one:
            reply = 1 if self.q and self.rng.randrange(100) < self.q else 0
        else:
            reply = 1 if one else 0
        if reply:
            self.forced |= {i, j}
        else:
            self._edge(i, j)
        return reply

    def can_be_nonzero(self, k):
        return can_be_nonzero(self.n, self.forced, self.adj, k)


def small_mvc(vertices, edges):
    vertices = list(vertices)
    best = len(vertices)
    for mask in range(1 << len(vertices)):
        chosen = {vertices[b] for b in range(len(vertices)) if mask >> b & 1}
        if len(chosen) < best and all(a in chosen or b in chosen for a, b in edges):
            best = len(chosen)
    return best


def can_be_nonzero(n, forced, adj, k):
    """是否存在一致数组使 a_k ≠ 0（见模块文档串的证明）。"""
    if k in forced:
        return False
    cover = {k}
    for f in forced:
        cover |= adj.get(f, set())
    if cover & forced:
        return False                     # 不会发生：F 独立且 k ∉ F
    budget = n - len(cover)
    if budget < 0:
        return False
    removed = cover | forced
    seen, slack_total, edge_total = set(), 0, 0
    for start in adj:
        if start in removed or start in seen:
            continue
        comp, stack = [], [start]
        seen.add(start)
        while stack:
            v = stack.pop()
            comp.append(v)
            for u in adj[v]:
                if u not in removed and u not in seen:
                    seen.add(u)
                    stack.append(u)
        edges = [(a, b) for a in comp for b in adj[a] if b not in removed and a < b]
        if not edges:
            continue
        edge_total += len(edges)
        if len(edges) >= 4:
            slack_total += 2
        else:
            slack_total += len(edges) - small_mvc(comp, edges)
    need = edge_total - budget
    return need <= 0 or (need <= 2 and slack_total >= need)


def main():
    data = open(sys.argv[1]).read().split()
    t = int(data[0])
    at = 1
    tests = []
    for _ in range(t):
        n, mode = int(data[at]), data[at + 1]
        if mode == "F":
            tests.append((n, [0] + [int(v) for v in data[at + 2:at + 2 + 2 * n]]))
            at += 2 + 2 * n
        else:
            tests.append((n, Adversary(n, int(data[at + 2]), int(data[at + 3]))))
            at += 4
    stream = tokens()

    def nxt():
        token = next(stream, None)
        if token is None:
            wrong("程序提前结束（没有输出 `! k` 就退出了）")
        return token

    say(f"{t}\n")
    for case_no, (n, hidden) in enumerate(tests, 1):
        say(f"{n}\n")
        used = 0
        while True:
            token = nxt()
            if token not in ("?", "!"):
                wrong(f"第 {case_no} 组：期望 `?` 或 `!`，读到了别的内容")
            if token == "!":
                ks = nxt()
                if not INT.match(ks) or not 1 <= int(ks) <= 2 * n:
                    wrong(f"第 {case_no} 组：`!` 后面应是 1..2n 的整数")
                k = int(ks)
                if isinstance(hidden, list):
                    ok = hidden[k] == 0
                else:
                    ok = not hidden.can_be_nonzero(k)
                if not ok:
                    wrong(f"第 {case_no} 组：a_k 不一定是 0（存在与全部回答一致、但 a_k ≠ 0 的数组）"
                          if not isinstance(hidden, list) else f"第 {case_no} 组：a_k 不是 0")
                break
            xs, ys = nxt(), nxt()
            if not (INT.match(xs) and INT.match(ys)):
                wrong(f"第 {case_no} 组：`?` 后面应是两个整数")
            i, j = int(xs), int(ys)
            if not (1 <= i <= 2 * n and 1 <= j <= 2 * n) or i == j:
                wrong(f"第 {case_no} 组：下标必须满足 1 ≤ i, j ≤ 2n 且 i ≠ j")
            used += 1
            if used > n + 1:
                wrong(f"第 {case_no} 组：询问超过 n+1 = {n + 1} 次")
            if isinstance(hidden, list):
                reply = 1 if hidden[i] == hidden[j] else 0
            else:
                reply = hidden.answer(i, j)
            say(f"{reply}\n")
    print("通过", file=sys.stderr)
    sys.exit(0)


if __name__ == "__main__":
    main()
