import random
import subprocess
import tempfile
from pathlib import Path
SAMPLE_IN = '3 a b c\n'
SAMPLE_OUT = '1:a->c\n2:a->b\n1:c->b\n3:a->c\n1:b->a\n2:b->c\n1:a->c\n'
CASES = ['3 a b c\n', '4 b y c\n', '5 a y z\n', '1 a x y\n', '6 c a x\n', '4 z c a\n', '7 b c y\n', '3 c x z\n', '7 x y b\n', '7 x a c\n', '1 a b y\n', '2 y b a\n', '8 c x y\n', '7 x z a\n', '3 x z c\n', '1 y z b\n', '3 x c y\n', '8 x b z\n', '6 x a b\n', '5 c x a\n']
REFERENCE_SOURCE = '# https://blog.csdn.net/geekwangminli/article/details/7981570\n\n# 将编号为numdisk的盘子从init杆移至desti杆 \ndef moveOne(numDisk : int, init : str, desti : str):\n    print("{}:{}->{}".format(numDisk, init, desti))\n\n#将numDisks个盘子从init杆借助temp杆移至desti杆\ndef move(numDisks : int, init : str, temp : str, desti : str):\n    if numDisks == 1:\n        moveOne(1, init, desti)\n    else: \n        # 首先将上面的（numDisk-1）个盘子从init杆借助desti杆移至temp杆\n        move(numDisks-1, init, desti, temp) \n        \n        # 然后将编号为numDisks的盘子从init杆移至desti杆\n        moveOne(numDisks, init, desti)\n        \n        # 最后将上面的（numDisks-1）个盘子从temp杆借助init杆移至desti杆 \n        move(numDisks-1, temp, init, desti)\n\nn, a, b, c = input().split()\nmove(int(n), a, b, c)\n'
assert CASES[0] == SAMPLE_IN
random.seed(4147)
def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=5, check=True)
    return result.stdout
assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split()
root = Path(__file__).parent / "data"
for index in range(20):
    content = CASES[index]
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")
