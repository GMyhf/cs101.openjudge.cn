"""绑定 93 对修正数据的合法性、独立答案和重抓后修正行为；不依赖私有下载目录。"""
from collections import Counter, defaultdict, deque
from decimal import Decimal
from functools import cmp_to_key
from math import isqrt
from contextlib import redirect_stdout
import io
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "scripts"), str(ROOT / "tools")]
import gmyhf_input_repairs as repairs
import materialize_gmyhf_downloads as materializer
from full_sweep import VALID_DRIVER


def oracle(number, text):
    lines = text.splitlines()
    if number == 18109:
        s = lines[0].lower()
        counts = Counter(s)
        best = max(dict.fromkeys(s), key=lambda ch: counts[ch])
        return f"{best} {counts[best]}"
    if number == 18223:
        result = []
        for line in lines[1:]:
            values = list(map(int, line.split()))
            possible = any(sum(v*s for v, s in zip(values, signs)) == 24
                           for signs in itertools.product((-1, 1), repeat=4))
            result.append("YES" if possible else "NO")
        return "\n".join(result)
    if number == 20074:
        result = {"M": 0, "F": 0}
        for line in lines[1:]:
            h, w, sex = line.split()
            h, w, steps = int(h), int(w), 0
            while not 185*h*h <= w*100000 <= 249*h*h:
                w += 8 if w*100000 < 185*h*h else -5
                steps += 1
                if steps > 1000:
                    raise ValueError("BMI 调整不收敛")
            result[sex] = max(result[sex], steps)
        return f"{result['M']} {result['F']}"
    if number == 20089:
        target = int(lines[0])
        counts = list(map(int, lines[1].split()))
        costs = (50, 100, 250, 500, 1000, 2500, 5000)
        best = min((sum(choice) for choice in itertools.product(*(range(v+1) for v in counts))
                    if sum(v*c for v, c in zip(choice, costs)) == target), default=None)
        return str(best) if best is not None else "Fail"
    if number == 20136:
        police, n = map(int, lines[0].split())
        adj = [list(map(int, line.split()[1:])) for line in lines[1:]]
        depths = {0: 0}
        maximum = 0
        def visit(u, parent):
            nonlocal maximum
            for v in adj[u]:
                if v == parent:
                    continue
                if v in depths:
                    maximum = max(maximum, depths[u]-depths[v]+1)
                else:
                    depths[v] = depths[u]+1
                    visit(v, u)
        visit(0, -1)
        return "YES!" if police == 1 or maximum > police else "NO!"
    if number == 20162:
        answers = []
        for line in lines[1:]:
            a, b, c, radius = map(int, line.split())
            lo, hi = sorted((a, b))
            answers.append(str(hi-lo-max(0, min(hi, c+radius)-max(lo, c-radius))))
        return "\n".join(answers)
    if number == 21458:
        target, _ = map(int, lines[0].split())
        states = {0: 0}
        for line in lines[1:]:
            duration, gain = map(int, line.split())
            following = {used+duration: value+gain for used, value in states.items()
                         if used+duration <= target}
            for used, value in following.items():
                states[used] = max(states.get(used, -1), value)
        return str(states.get(target, -1))
    if number == 21532:
        n = int(text)
        divisor = min(v for d in range(1, isqrt(n)+1) if n % d == 0 for v in (d, n//d) if v >= 6)
        return str(n//divisor)
    if number == 25301:
        days = defaultdict(list)
        for line in lines[1:]:
            student, month, day = line.split()
            days[int(month), int(day)].append(student)
        return "\n".join(f"{month} {day} " + " ".join(days[month, day])
                         for month, day in sorted(days) if len(days[month, day]) > 1)
    if number == 26971:
        values = list(map(int, lines[1].split()))
        candies = [1]*len(values)
        for i in sorted(range(len(values)), key=lambda i: values[i]):
            for j in (i-1, i+1):
                if 0 <= j < len(values) and values[j] < values[i]:
                    candies[i] = max(candies[i], candies[j]+1)
        return str(sum(candies))
    if number == 26976:
        values = list(map(int, lines[1].split()))
        signs = [(b > a)-(b < a) for a, b in zip(values, values[1:]) if a != b]
        return str(1 + sum(i == 0 or value != signs[i-1] for i, value in enumerate(signs)))
    if number == 27373:
        capacity = int(lines[0])
        values = lines[2].split()
        best = ""
        for mask in range(1, 1 << len(values)):
            selected = [v for i, v in enumerate(values) if mask & (1 << i)]
            if sum(map(len, selected)) > capacity:
                continue
            selected.sort(key=cmp_to_key(lambda a, b: (b+a > a+b)-(b+a < a+b)))
            candidate = "".join(selected)
            if (len(candidate), candidate) > (len(best), best):
                best = candidate
        return best
    if number == 27862:
        n = int(lines[0])
        children = defaultdict(list)
        for line in lines[1:n]:
            a, b = map(int, line.split())
            children[a].append(b)
        payoffs = {i: (a, b) for i, a, b in (map(int, line.split()) for line in lines[n+1:])}
        def choose(node, player):
            if not children[node]:
                return payoffs[node]
            left, right = (choose(v, 1-player) for v in children[node])
            if left[player] == right[player]:
                raise ValueError("博弈树选择收益相同")
            return max((left, right), key=lambda p: p[player])
        return " ".join(map(str, choose(1, 0)))
    if number in (28012, 28193):
        if number == 28012:
            n = int(lines[0])
            costs = [1]*n
            edges = lines[1:n]
            blocked = set(map(int, lines[n].split()))
            start = 0
        else:
            n, _ = map(int, lines[0].split())
            costs = [0, *map(int, lines[1].split())]
            edges, blocked, start = lines[2:], set(), 1
        graph = defaultdict(list)
        for line in edges:
            a, b = map(int, line.split())
            graph[a].append(b)
            graph[b].append(a)
        seen = set(blocked)
        total = 0
        for root in range(start, n+start) if number == 28193 else [0]:
            if root in seen:
                continue
            component = []
            queue = deque([root])
            seen.add(root)
            while queue:
                u = queue.popleft()
                component.append(u)
                for v in graph[u]:
                    if v not in seen:
                        seen.add(v)
                        queue.append(v)
            total += min(costs[v] for v in component) if number == 28193 else len(component)
        return str(total)
    if number == 28664:
        weights = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
        return "\n".join("YES" if value[-1] == "10X98765432"[
            sum(int(v)*w for v, w in zip(value[:17], weights)) % 11] else "NO" for value in lines[1:])
    if number == 29256:
        _, groups = map(int, lines[0].split())
        values = list(map(int, lines[1].split()))
        lo, hi = max(values), sum(values)
        while lo < hi:
            mid = (lo+hi)//2
            needed, running = 1, 0
            for value in values:
                if running+value > mid:
                    needed += 1
                    running = 0
                running += value
            if needed <= groups:
                hi = mid
            else:
                lo = mid+1
        return str(lo)
    if number == 29740:
        n, _ = map(int, lines[0].split())
        states = [None, *(tuple(map(int, line.split())) for line in lines[1:n+1])]
        parents, outgoing = defaultdict(list), set()
        for line in lines[n+1:]:
            a, b, w = map(int, line.split())
            parents[b].append((a, w))
            outgoing.add(a)
        result = {}
        def evaluate(node):
            if node not in result:
                result[node] = (sum(max(0, evaluate(p))*w for p, w in parents[node])-states[node][1]
                                if parents[node] else states[node][0])
            return result[node]
        outputs = [(i, evaluate(i)) for i in range(1, n+1) if i not in outgoing]
        return "\n".join(f"{i} {value}" for i, value in outputs if value > 0) or "NULL"
    if number == 30281:
        a, b, c = map(Decimal, lines[0].split())
        # 本次六组均 c>=max(a,b)，不存在便宜对角线来回移动的奇偶问题。
        if c < max(a, b):
            raise ValueError("需使用一般格点距离算法")
        c = min(c, a+b)
        items = [(s, int(x), int(y)) for s, x, y in (line.split() for line in lines[1:])]
        values = []
        for order in itertools.permutations(items):
            path = [(None, 0, 0), *order, (None, 100, 100)]
            cost = Decimal(0)
            for (_, x, y), (_, xx, yy) in zip(path, path[1:]):
                dx, dy = abs(x-xx), abs(y-yy)
                cost += min(dx, dy)*c + max(0, dx-dy)*a + max(0, dy-dx)*b
            values.append((cost, tuple(p[0] for p in order)))
        values.sort()
        if values[0][0] == values[1][0]:
            raise ValueError("拾取顺序不唯一")
        cost, names = values[0]
        return " ".join(names) + f"\n{cost:.2f}"
    if number == 30942:
        if int(lines[1]) != len(lines[0]):
            raise ValueError("本次修正应覆盖 k=字符串长度的边界")
        return str(len(lines[0]))
    raise ValueError(number)


class GMyhfInputRepairTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries = json.loads(repairs.LEDGER.read_text())["entries"]

    def test_every_repaired_pair_matches_independent_answer_and_provenance(self):
        self.assertEqual(93, len(self.entries))
        audit = json.loads((ROOT / "collab/gmyhf-download-acceptance.json").read_text())
        original = {f["input"] for finding in audit["findings"]
                    if finding["classification"] == "确认违反题面" for f in finding["files"]}
        self.assertEqual(original, {e["input"] for e in self.entries})
        self.assertEqual(set(repairs.REASONS), {e["global_number"] for e in self.entries})
        for entry in self.entries:
            with self.subTest(problem=entry["global_number"], file=entry["input"]):
                input_path, output_path = ROOT / entry["input"], ROOT / entry["output"]
                input_data, output_data = input_path.read_bytes(), output_path.read_bytes()
                self.assertEqual(entry["input_sha256"], repairs.sha(input_data))
                self.assertEqual(entry["output_sha256"], repairs.sha(output_data))
                self.assertEqual(oracle(entry["global_number"], input_data.decode()).split(),
                                 output_data.decode().split())
                self.assertEqual(entry["corrected_output"].encode(), output_data)
                source = json.loads((input_path.parent.parent / "SOURCE.json").read_text())
                self.assertEqual("collab/gmyhf-input-repairs.json", source["correction_ledger"])
                record = next(r for r in source["files"] if r["case"] == int(input_path.stem))
                self.assertEqual(entry["before_input_sha256"], record["correction"]["before_input_sha256"])

    def test_repaired_inputs_satisfy_existing_statement_contracts(self):
        for number in repairs.REASONS:
            entries = [e for e in self.entries if e["global_number"] == number]
            directory = (ROOT / entries[0]["input"]).parent.parent
            module = directory.parent / directory.name.replace("_GMyhf", "_made") / "producecase.py"
            with self.subTest(problem=number), tempfile.TemporaryDirectory() as tmp:
                data = Path(tmp) / "data"
                data.mkdir()
                for entry in entries:
                    path = ROOT / entry["input"]
                    (data / path.name).write_bytes(path.read_bytes())
                result = subprocess.run([sys.executable, "-c", VALID_DRIVER, str(module), str(data),
                                         str(number)], cwd=tmp, text=True, capture_output=True, timeout=30)
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual([], json.loads(result.stdout))

    def test_materialization_repairs_old_pair_and_refuses_unknown_changes(self):
        before = b"a"*3000 + b"\n"
        after = b"a"*1000 + b"\n"
        row = {"before_input_sha256": repairs.sha(before), "before_output_sha256": repairs.sha(b"a 3000\n"),
               "input_sha256": repairs.sha(after), "output_sha256": repairs.sha(b"a 1000\n"),
               "corrected_output": "a 1000\n"}
        table = {(18109, "4.in"): row}
        self.assertEqual((after, b"a 1000\n", row), repairs.repair_pair(
            18109, "4.in", before, b"a 3000\n", table))
        self.assertEqual((after, b"a 1000\n", row), repairs.repair_pair(
            18109, "4.in", after, b"a 1000\n", table))
        with self.assertRaises(ValueError):
            repairs.repair_pair(18109, "4.in", before+b"x", b"a 3000\n", table)
        with self.assertRaises(ValueError):
            repairs.repair_pair(18109, "4.in", before, b"a 2999\n", table)

    def test_materializer_applies_repairs_before_replacing_existing_directory(self):
        before, after = b"a"*3000+b"\n", b"a"*1000+b"\n"
        old_output, new_output = b"a 3000\n", b"a 1000\n"
        row = {"reason": "合法长度边界", "before_input_sha256": repairs.sha(before),
               "before_output_sha256": repairs.sha(old_output), "input_sha256": repairs.sha(after),
               "output_sha256": repairs.sha(new_output), "corrected_output": new_output.decode()}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tests = root / "data/openjudge/tests"
            download = tests / "admin_download"
            raw = download / "18109"
            raw.mkdir(parents=True)
            (raw / "4.in").write_bytes(before)
            (raw / "4.out").write_bytes(old_output)
            (download / "manifest.json").write_text(json.dumps({"fetched_at": "test", "problems": {
                "18109": {"title": "长度边界", "files": [
                    {"filename": "4.in", "bytes": len(before)},
                    {"filename": "4.out", "bytes": len(old_output)}]}}}))
            (root / "collab").mkdir()
            (root / "collab/valid-contracts.json").write_text('{"dirs": []}')
            attrs = {"ROOT": root, "TESTS": tests, "DL": download,
                     "OPENJUDGE": root / "data/openjudge", "REPORT": root / "collab/report.json"}
            with patch.multiple(materializer, **attrs), \
                    patch.object(materializer, "local_id_map", return_value={18109: "18109"}), \
                    patch.object(materializer, "multi_answer_hit", return_value=None), \
                    patch.object(materializer, "load_repairs", return_value={(18109, "4.in"): row}), \
                    redirect_stdout(io.StringIO()):
                materializer.main()
                destination = tests / "10000-19963/18109_GMyhf/data/0.in"
                self.assertEqual(after, destination.read_bytes())
                self.assertEqual(new_output, destination.with_suffix(".out").read_bytes())
                provenance = json.loads((destination.parent.parent / "SOURCE.json").read_text())
                self.assertEqual("collab/gmyhf-input-repairs.json", provenance["correction_ledger"])
                report = json.loads((root / "collab/report.json").read_text())
                self.assertEqual(1, report["materialized"][0]["corrected_pairs"])
                # 未经审核的新抓取内容不能删除已修正的活目录。
                (raw / "4.in").write_bytes(before+b"x")
                with self.assertRaises(ValueError):
                    materializer.main()
                self.assertEqual(after, destination.read_bytes())


if __name__ == "__main__":
    unittest.main()
