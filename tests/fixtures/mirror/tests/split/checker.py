"""夹具 checker：把 n 拆成两个正整数之和，任意一种拆法都对。"""
import sys

n = int(open(sys.argv[1]).read())
tokens = open(sys.argv[2], errors="replace").read().split()
if len(tokens) != 2 or not all(t.isdigit() for t in tokens):
    print("要输出两个正整数")
    sys.exit(42)
a, b = map(int, tokens)
if a > 0 and b > 0 and a + b == n:
    sys.exit(0)
print("两数之和不等于 n")
sys.exit(42)
