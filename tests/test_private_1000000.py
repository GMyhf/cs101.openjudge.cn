"""私有题库 1000000「KMP 字符比较次数（nextval）」的数据判别力。

参考实现与生成器是一伙的，数据自洽不说明对。这里用两样外部事实压它：
① 题面背景给出的样例答案（nextval 31 次、普通 next 32 次、位置 19）；
② 一份算法不同的 oracle —— next 用定义暴力求最长相等真前后缀，nextval 按定义递推，
   匹配循环逐字照抄题面 —— 逐组核 `.out`。
再拿几种典型错法喂进判题器，确认它们真的挂。
"""
import unittest
from pathlib import Path

from judge import judge

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/openjudge/tests/private/1000000_made/data"
# 2026-10-09 发到平台成为 practice/31378，平台上传的就是上面那份数据；本站 practice 镜像收录时
# 用同一个随机种子重建，两份必须逐字节相同，否则本站和平台就是两套数据。
PUBLIC = ROOT / "data/openjudge/tests/30000-/31378_made/data"


def brute_next(p):
    nxt = [-1]
    for j in range(1, len(p)):
        prefix = p[:j]
        nxt.append(max(k for k in range(j) if prefix[:k] == prefix[j - k:]))
    return nxt


def oracle(text, use_nextval=True):
    p, t = text.split()
    nxt = brute_next(p) if len(p) <= 400 else None
    if nxt is None:                              # 长模式串用 Z 函数求 border，仍与参考实现不同
        z = [0] * len(p)
        left = right = 0
        for i in range(1, len(p)):
            if i < right:
                z[i] = min(right - i, z[i - left])
            while i + z[i] < len(p) and p[z[i]] == p[i + z[i]]:
                z[i] += 1
            if i + z[i] > right:
                left, right = i, i + z[i]
        border = [0] * (len(p) + 1)              # border[j] = p[:j] 的最长真 border
        for i in range(len(p) - 1, 0, -1):
            border[i + z[i]] = max(border[i + z[i]], z[i])
        for j in range(len(p) - 1, 0, -1):
            border[j] = max(border[j], border[j + 1] - 1)
        nxt = [-1] + [border[j] for j in range(1, len(p))]
    table = nxt
    if use_nextval:
        table = [-1] * len(p)
        for j in range(1, len(p)):
            table[j] = table[nxt[j]] if p[j] == p[nxt[j]] else nxt[j]
    i = j = cnt = 0
    while i < len(t) and j < len(p):
        if j == -1:
            i += 1; j = 0; continue
        cnt += 1
        if t[i] == p[j]:
            i += 1; j += 1
        else:
            j = table[j]
    return f"{cnt} {i - j if j == len(p) else -1}\n"


REFERENCE = (DATA.parent / "samplecode.py").read_text(encoding="utf-8")


class Problem1000000Tests(unittest.TestCase):
    def test_oracle_reproduces_the_background_numbers(self):
        sample = (DATA / "0.in").read_text(encoding="utf-8")
        self.assertEqual(oracle(sample), "31 19\n")
        self.assertEqual(oracle(sample, use_nextval=False), "32 19\n")

    def test_every_expected_output_matches_the_oracle(self):
        cases = sorted(DATA.glob("*.in"), key=lambda path: int(path.stem))
        self.assertEqual(len(cases), 21)
        for path in cases:
            text = path.read_text(encoding="utf-8")
            self.assertEqual(path.with_suffix(".out").read_text(encoding="utf-8"), oracle(text), path.name)

    def test_data_tells_nextval_from_next(self):
        differs = sum(oracle(path.read_text(encoding="utf-8")) !=
                      oracle(path.read_text(encoding="utf-8"), use_nextval=False)
                      for path in DATA.glob("*.in"))
        self.assertGreaterEqual(differs, 10)

    def test_platform_copy_31378_has_the_same_bytes(self):
        private = {path.name: path.read_bytes() for path in DATA.iterdir()}
        public = {path.name: path.read_bytes() for path in PUBLIC.iterdir()}
        self.assertEqual(len(private), 42)
        self.assertEqual(public, private)
        self.assertEqual((PUBLIC.parent / "samplecode.py").read_text(encoding="utf-8").split('"""', 2)[2],
                         REFERENCE.split('"""', 2)[2])

    def test_reference_accepted_and_typical_mistakes_rejected(self):
        self.assertEqual(judge("private", "1000000", "python", REFERENCE)["status"], "Accepted")
        self.assertEqual(judge("practice", "31378", "python", REFERENCE)["status"], "Accepted")
        # 实测（2026-10-09）：next 挂 14/21、多计 -1 挂 16/21、从 1 数挂 11/21
        mistakes = {
            # 用普通 next，不做 nextval 优化
            "next": REFERENCE.replace("val[j] = val[nxt[j]] if p[j] == p[nxt[j]] else nxt[j]",
                                      "val[j] = nxt[j]"),
            # 把 j == -1 时的后移也算成一次比较
            "count -1": REFERENCE.replace("            i += 1\n            j = 0\n            continue",
                                          "            i += 1\n            j = 0\n            count += 1\n            continue"),
            # 位置从 1 开始数
            "1-based": REFERENCE.replace("print(count, i - m if j == m else -1)",
                                         "print(count, i - m + 1 if j == m else -1)"),
        }
        for name, source in mistakes.items():
            self.assertNotEqual(source, REFERENCE, name)
            for book, problem in (("private", "1000000"), ("practice", "31378")):
                self.assertNotEqual(judge(book, problem, "python", source)["status"], "Accepted",
                                    (name, book))


if __name__ == "__main__":
    unittest.main()
