"""4147 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001b
生成器与循环取自 scripts/build_001b.py（批次 001b），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4147
SAMPLE_IN = '3 a b c\n'
SAMPLE_OUT = '1:a->c\n2:a->b\n1:c->b\n3:a->c\n1:b->a\n2:b->c\n1:a->c\n'
REFERENCE_SOURCE = '# https://blog.csdn.net/geekwangminli/article/details/7981570\n\n# 将编号为numdisk的盘子从init杆移至desti杆 \ndef moveOne(numDisk : int, init : str, desti : str):\n    print("{}:{}->{}".format(numDisk, init, desti))\n\n#将numDisks个盘子从init杆借助temp杆移至desti杆\ndef move(numDisks : int, init : str, temp : str, desti : str):\n    if numDisks == 1:\n        moveOne(1, init, desti)\n    else: \n        # 首先将上面的（numDisk-1）个盘子从init杆借助desti杆移至temp杆\n        move(numDisks-1, init, desti, temp) \n        \n        # 然后将编号为numDisks的盘子从init杆移至desti杆\n        moveOne(numDisks, init, desti)\n        \n        # 最后将上面的（numDisks-1）个盘子从temp杆借助init杆移至desti杆 \n        move(numDisks-1, temp, init, desti)\n\nn, a, b, c = input().split()\nmove(int(n), a, b, c)\n'

def g4147(r):
    n = r.randint(1, 8)
    rods = r.sample(list("abcxyz"), 3)
    return f"{n} {' '.join(rods)}\n"

def build_cases():
    return [SAMPLE_IN] + [g4147(random.Random(NUMBER + i)) for i in range(1, 20)]

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
