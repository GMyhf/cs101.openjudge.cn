"""4089 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

2026-10 审计：原数据全是 6 位随机号码、除样例外无一组 NO，改为按场景构造（前缀冲突、前导零、满规模等）。

出处：build_001a
生成器与循环取自 scripts/build_001a.py（批次 001a），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4089
SAMPLE_IN = '2\n3\n911\n97625999\n91125426\n5\n113\n12340\n123440\n12345\n98346\n'
SAMPLE_OUT = 'NO\nYES\n'
REFERENCE_SOURCE = 'class TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.is_end_of_number = False\n\nclass Trie:\n    def __init__(self):\n        self.root = TrieNode()\n    \n    def insert(self, number):\n        node = self.root\n        for digit in number:\n            if digit not in node.children:\n                node.children[digit] = TrieNode()\n            node = node.children[digit]\n            # 如果当前节点已经是某个电话号码的结尾，则说明存在前缀冲突\n            if node.is_end_of_number:\n                return False\n        # 插入完成后，标记为完整电话号码\n        node.is_end_of_number = True\n        # 如果当前节点还有子节点，说明有其他号码以它为前缀\n        return len(node.children) == 0\n    \n    def is_consistent(self, numbers):\n        # 按长度从短到长排序，确保短号码先被检查\n        numbers.sort(key=len)\n        for number in numbers:\n            if not self.insert(number):\n                return False\n        return True\n\ndef main():\n    import sys\n    input = sys.stdin.read\n    data = input().splitlines()\n    \n    t = int(data[0])  # 测试样例数量\n    index = 1\n    results = []\n    \n    for _ in range(t):\n        n = int(data[index])  # 当前测试样例的电话号码数量\n        index += 1\n        numbers = data[index:index + n]\n        index += n\n        \n        trie = Trie()\n        if trie.is_consistent(numbers):\n            results.append("YES")\n        else:\n            results.append("NO")\n    \n    print("\\n".join(results))\n\n# 调用主函数\nif __name__ == "__main__":\n    main()\n'

import re

_NUM_RE = re.compile(r"[0-9]{1,10}")


def valid(text):
    """题面契约：第一行 t（1≤t≤40）；每组先一行 n（1≤n≤10000），其后 n 行各一个不超过 10 位的电话号码。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    def as_int(s):
        if not re.fullmatch(r"-?[0-9]+", s):
            return None
        return int(s)
    t = as_int(lines[0])
    if t is None or not 1 <= t <= 40:
        return False
    pos = 1
    for _ in range(t):
        if pos >= len(lines):
            return False
        n = as_int(lines[pos]); pos += 1
        if n is None or not 1 <= n <= 10000 or pos + n > len(lines):
            return False
        for s in lines[pos:pos + n]:
            if not _NUM_RE.fullmatch(s):
                return False
        pos += n
    return pos == len(lines)


def _rand_len(r, lo=1, hi=10):
    # 偏向长号码，短号码数量本身有限（1 位最多 10 个）
    return min(hi, max(lo, hi - int(r.expovariate(0.45))))


def prefix_free(r, n, lo=1, hi=10):
    """生成 n 个互不为前缀（且互异）的号码，按随机顺序返回。"""
    words, prefixes, out = set(), set(), []
    tries = 0
    while len(out) < n:
        tries += 1
        assert tries < 50 * n + 1000, "前缀无关集合生成失败"
        L = _rand_len(r, lo, hi)
        s = "".join(r.choice("0123456789") for _ in range(L))
        if s in words or s in prefixes or any(s[:k] in words for k in range(1, L)):
            continue
        words.add(s); out.append(s)
        for k in range(1, L):
            prefixes.add(s[:k])
    return out


def with_conflicts(r, nums, k):
    """在前缀无关集合里埋 k 个冲突：替换掉一些号码为另一号码的真前缀或真延长，位置随机。"""
    nums = nums[:]
    for _ in range(k):
        i, j = r.sample(range(len(nums)), 2)
        base = nums[i]
        if len(base) >= 2 and (len(base) == 10 or r.random() < 0.5):
            cand = base[:r.randint(1, len(base) - 1)]
        else:
            cand = base + "".join(r.choice("0123456789") for _ in range(r.randint(1, 10 - len(base))))
        if cand in nums:
            continue
        nums[j] = cand
    return nums


def one_test(r, n, no, lo=1, hi=10, k=1):
    nums = prefix_free(r, n, lo, hi)
    if no and n >= 2:
        nums = with_conflicts(r, nums, k)
    return nums


def render(tests):
    lines = [str(len(tests))]
    for nums in tests:
        lines.append(str(len(nums)))
        lines += nums
    return "\n".join(lines) + "\n"


def build_cases():
    r = random.Random(NUMBER)
    cases = [SAMPLE_IN]
    # 1 最小规模：t=1, n=1
    cases.append(render([["5"]]))
    # 2 长号码在前、其前缀在后（只检查“前面是后面前缀”的写法会错）；外加 n=2 YES
    cases.append(render([["9123456789", "91"], ["1", "2"], ["0", "0123"], ["4444", "44"], ["12", "13"]]))
    # 3 前导零：转 int 会把 "012" 当成 "12" 的写法会误判
    cases.append(render([["012", "1234", "0013"], ["0", "1", "2"], ["00", "0", "5"],
                         ["0000000000", "000000000"], ["07", "7", "70"], ["120", "012", "0120"]]))
    # 4 t=40 每组 n=1
    cases.append(render([[ "".join(r.choice("0123456789") for _ in range(r.randint(1, 10)))] for _ in range(40)]))
    # 5 t=40 小规模混合
    cases.append(render([one_test(r, r.randint(2, 15), r.random() < 0.5) for _ in range(40)]))
    # 6 先出 NO、后面还有大量号码要读完的组夹在中间（提前 break 不读完会串组）
    tests = []
    for i in range(10):
        nums = prefix_free(r, 300)
        if i % 2 == 0:
            nums[1] = nums[0] + "1" if len(nums[0]) < 10 else nums[0][:5]
        tests.append(nums)
    cases.append(render(tests))
    # 7-8 t=20 中等规模混合
    for _ in range(2):
        cases.append(render([one_test(r, r.randint(200, 800), r.random() < 0.5) for _ in range(20)]))
    # 9 单组 n=10000 一致（长度混合）
    cases.append(render([one_test(r, 10000, False)]))
    # 10 单组 n=10000 恰一处冲突
    cases.append(render([one_test(r, 10000, True)]))
    # 11 单组 n=10000 全 10 位
    cases.append(render([one_test(r, 10000, False, 10, 10)]))
    # 12 单组 n=10000：1 位短号码与最长号码冲突
    nums = prefix_free(r, 10000, 2, 10)
    first = nums[r.randrange(len(nums))][0]
    nums.append(first)
    nums = nums[1:]
    r.shuffle(nums)
    cases.append(render([nums]))
    # 13-16 t=9、每组 n=10000（约 1MB）
    for c in range(4):
        cases.append(render([one_test(r, 10000, r.random() < 0.5, k=r.randint(1, 3)) for _ in range(9)]))
    # 17 冲突对只差一位长度、字典序相邻但输入里相距最远
    nums = prefix_free(r, 9999, 3, 9)
    w = nums[0]
    nums = nums[1:] + [w, w + "7"]
    nums = [nums[-1]] + nums[:-1]
    cases.append(render([nums]))
    # 18 t=40 中等规模，YES/NO 交替
    cases.append(render([one_test(r, 2000, i % 2 == 1) for i in range(40)]))
    # 19 t=40 中等规模，全部一致
    cases.append(render([one_test(r, 2000, False) for _ in range(40)]))
    return cases


def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=120, check=True)
    return result.stdout


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
    assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split(), "参考解法跑不出样例输出"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        assert valid(content), f"第 {index} 组不满足题面约束"
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
