"""私有题库 1000003 论文投稿前的关键路径：数据、判别力与参考实现测试。"""
import importlib.util
import unittest
from pathlib import Path
from judge import judge

ROOT = Path(__file__).resolve().parents[1]
MADE = ROOT / "data/openjudge/tests/private/1000003_made"
DATA = MADE / "data"
REFERENCE = (MADE / "samplecode.py").read_text(encoding="utf-8")
spec = importlib.util.spec_from_file_location("producecase_1000003", MADE / "producecase.py")
producecase = importlib.util.module_from_spec(spec)
spec.loader.exec_module(producecase)


def cases():
    paths = sorted(DATA.glob("*.in"), key=lambda p: int(p.stem))
    return [(p.read_text(), p.with_suffix(".out").read_text()) for p in paths]


def total_time(n, t, edges, delay=None):
    """按定义的暴力：Bellman-Ford 式松弛求总工期；delay=(i,d) 表示任务 i 推迟 d 开始。有环返回 None。"""
    es = [0] * (n + 1)
    if delay:
        es[delay[0]] = delay[1]
    for _ in range(n + 1):
        changed = False
        for u, v in edges:
            need = es[u] + t[u] + (delay[1] if delay and v == delay[0] else 0)
            if need > es[v]:
                es[v] = need
                changed = True
        if not changed:
            return max(es[i] + t[i] for i in range(1, n + 1))
    return None


def wrong_lf_uses_es(n, t, edges):
    """典型错解：LF[u] 取后继的最早开始时间 ES[v]（应取最迟开始时间 LS[v]）。只用于无环数据。"""
    succ = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for u, v in edges:
        succ[u].append(v)
        indeg[v] += 1
    order = [i for i in range(1, n + 1) if indeg[i] == 0]
    es = [0] * (n + 1)
    for u in order:
        for v in succ[u]:
            es[v] = max(es[v], es[u] + t[u])
            indeg[v] -= 1
            if indeg[v] == 0:
                order.append(v)
    total = max(es[i] + t[i] for i in range(1, n + 1))
    crit = [i for i in range(1, n + 1) if min((es[v] for v in succ[i]), default=total) - t[i] == es[i]]
    return f"{total}\n{' '.join(map(str, crit))}\n"


class Problem1000003Tests(unittest.TestCase):
    def test_sample_answer(self):
        text, out = cases()[0]
        self.assertEqual(text, producecase.SAMPLE_IN)
        self.assertEqual(out, "16\n1 3 5 7 8\n")

    def test_every_output_matches_generator_oracle(self):
        data = cases()
        self.assertEqual(len(data), 21)
        for index, (text, out) in enumerate(data):
            self.assertTrue(producecase.valid(text), index)
            self.assertEqual(producecase.oracle(*producecase.parse(text)), out, index)

    def test_small_cases_match_the_definition(self):
        """小数据逐个推迟 1 小时：总工期变长 ⇔ 关键任务；有环 ⇔ -1。"""
        checked = 0
        for index, (text, out) in enumerate(cases()):
            n, t, edges = producecase.parse(text)
            if n > 60:
                continue
            base = total_time(n, t, edges)
            if base is None:
                self.assertEqual(out, "-1\n", index)
            else:
                crit = [i for i in range(1, n + 1) if total_time(n, t, edges, (i, 1)) > base]
                self.assertEqual(out, f"{base}\n{' '.join(map(str, crit))}\n", index)
            checked += 1
        self.assertGreaterEqual(checked, 6)

    def test_data_pins_the_common_mistakes(self):
        outs = [out for _, out in cases()]
        # 有环的组：不判环的错解在这些组上挂
        self.assertGreaterEqual(sum(o == "-1\n" for o in outs), 4)
        # 深链：递归 DFS 爆栈
        self.assertTrue(any(producecase.parse(text)[0] == 10000 and out.split()[1:] == list(map(str, range(1, 10001)))
                            for text, out in cases()))
        # 关键任务不止一条路径：某个关键任务有两个以上关键后继或前驱
        multi = 0
        for text, out in cases():
            if out == "-1\n":
                continue
            n, t, edges = producecase.parse(text)
            crit = set(map(int, out.split()[1:]))
            deg = {}
            for u, v in edges:
                if u in crit and v in crit:
                    deg[u] = deg.get(u, 0) + 1
            if any(d >= 2 for d in deg.values()) or len(crit) > 1 and not edges:
                multi += 1
        self.assertGreaterEqual(multi, 4)
        # 用后继“最早开始”而不是“最迟开始”算最迟完成时间的错解：至少 5 组答案不同（样例就是其一）
        differ = sum(out != "-1\n" and wrong_lf_uses_es(*producecase.parse(text)) != out for text, out in cases())
        self.assertGreaterEqual(differ, 5)

    def test_reference_accepted(self):
        self.assertEqual(judge("private", "1000003", "python", REFERENCE)["status"], "Accepted")


if __name__ == "__main__":
    unittest.main()
