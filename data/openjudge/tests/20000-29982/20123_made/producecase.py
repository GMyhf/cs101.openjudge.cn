"""20123 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001d
生成器与循环取自 scripts/build_001d.py（批次 001d），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 20123
SAMPLE_IN = '123364315\n'
SAMPLE_OUT = 'YES\n'
REFERENCE_SOURCE = "#20123:7-友好数，http://cs101.openjudge.cn/practice/20123/\n#\n# 陈威宇：>=7位就一定YES了，因为所有后缀%7有两个相等的（抽屉原理），\n# 取这两个后缀里长的那个去掉短的那个即可？\n'''\n通过递归地尝试不同的子串来寻找符合条件的解.\n`dfs(n, i)` 函数是进行深度优先搜索的核心部分。它接受两个参数：`n`代表当前搜索到的子串，\n`i`代表当前处理到的位置索引。在函数内部，通过不断拼接字符来生成不同的子串，\n然后检查是否满足能够被7整除的条件。\n\n'''\ndef dfs(n, i):\n    global bo\n    if len(n) > 0 and int(n) % 7 == 0:\n        bo = True\n    if bo:\n        return\n    if i >= l:\n        return\n    dfs(n, i+1)\n    dfs(n+s[i], i+1)\n\n\ns = input()\nl = len(s)\nif l >= 7:\n    print('YES')\n    exit()\nbo = False\ndfs('', 0)\nif bo:\n    print('YES')\nelse:\n    print('NO')\n\n"

def friendly7(s):
    """存在非空保序子序列构成 7 的倍数？与参考解法的 int(sub)%7 同语义。"""
    seen=set()
    for ch in s:
        d=int(ch); seen=seen|{d%7}|{(r*10+d)%7 for r in seen}
        if 0 in seen: return True
    return False

def g20123(r):
    kind=r.random()
    if kind<0.34:                                                                               # 强制 NO：短数且无任何子序列被 7 整除
        for _ in range(400):
            s="".join(str(r.randint(1,9)) for _ in range(r.randint(1,6)))
            if not friendly7(s): return s+"\n"
        return "11\n"
    if kind<0.6:                                                                                # 短数且必 YES：走 DFS 真算法而非捷径
        for _ in range(400):
            s=str(r.randint(1,9))+"".join(str(r.randint(0,9)) for _ in range(r.randint(0,5)))
            if friendly7(s): return s+"\n"
        return "7\n"
    n=r.randint(7,60) if kind<0.88 else r.randint(99000,100000)                                 # 后者贴题面 10^5 位上界
    return str(r.randint(1,9))+"".join(str(r.randint(0,9)) for _ in range(n-1))+"\n"

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g20123(random.Random(NUMBER + i + attempt * 1000))
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
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
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
