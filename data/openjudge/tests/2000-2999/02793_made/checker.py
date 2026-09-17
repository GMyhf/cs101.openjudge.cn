"""02793 孙子问题 —— special judge。

`python3 -I checker.py <输入> <学生输出> <参考答案>`；退出 0 通过、42 答案错误、3 数据自身出错。

判据（与参考答案里的具体数值无关，任何合法的 b 都通过）：记 L = lcm(a)，
f(N) = Σ b_i·(N mod a_i)。要 f(N) ≡ N (mod L) 对所有 N 成立。f(0)=0，且

    f(k) − f(k−1) = Σ b_i − Σ_{i: a_i | k} a_i·b_i

所以等价于：对每个 k，Σ_{i∈S(k)} a_i·b_i ≡ Σ b_i − 1 (mod L)，S(k) = {i : a_i | k}。
S(k) 只取决于 gcd(k, L)，能出现的集合恰好是「闭集」{i : a_i | lcm(a_T)}（T 取遍下标
子集，空集对应 k=1），n<=10 最多 1024 个，直接枚举。

解总是存在（见 samplecode.py 的构造），所以输出 NO 一律判错；参考答案若出现 NO 或
自身不满足判据，说明数据坏了，退 3 报 Judge Error。

格式：输出按空白切 token 顺序对应各组。每组要么是 `NO`（判错），要么是 n 个正整数：
只含 ASCII 数字、无前导零、不超过 50 位、>= 1。多出的 token 判错。
"""
import sys

MAX_DIGITS = 50


def verdict(ok, message):
    print(message)
    sys.exit(0 if ok else 42)


def gcd(x, y):
    while y:
        x, y = y, x % y
    return x


def closed_sets(a):
    n = len(a)
    lcm_of = [1] * (1 << n)
    for mask in range(1, 1 << n):
        low = (mask & -mask).bit_length() - 1
        prev = lcm_of[mask & (mask - 1)]
        lcm_of[mask] = prev * a[low] // gcd(prev, a[low])
    sets = set()
    for mask in range(1 << n):
        sets.add(sum(1 << i for i in range(n) if lcm_of[mask] % a[i] == 0))
    return lcm_of[-1], sets


def good(a, b):
    L, sets = closed_sets(a)
    total = sum(b)
    return all((sum(a[i] * b[i] for i in range(len(a)) if s >> i & 1) - total + 1) % L == 0
               for s in sets)


def groups_of(path):
    tokens = open(path, encoding="utf-8").read().split()
    p, groups = 0, []
    while p < len(tokens):
        n = int(tokens[p]); p += 1
        if n == 0:
            break
        groups.append([int(x) for x in tokens[p:p + n]]); p += n
    return groups


def read_answers(tokens, groups):
    """逐组取出 b；返回 (列表, 出错信息)。列表元素为 None 表示该组输出了 NO。"""
    p, out = 0, []
    for index, a in enumerate(groups, 1):
        if p < len(tokens) and tokens[p] == b"NO":
            out.append(None); p += 1
            continue
        chunk = tokens[p:p + len(a)]; p += len(a)
        if len(chunk) < len(a):
            return None, f"第 {index} 组输出的数不够"
        for token in chunk:
            if not (token.isdigit() and token.isascii()) or token[:1] == b"0":
                return None, f"第 {index} 组有不是正整数（或带前导零）的输出"
            if len(token) > MAX_DIGITS:
                return None, f"第 {index} 组有超过 50 位的数"
        out.append([int(t) for t in chunk])
    if p < len(tokens):
        return None, "输出比数据组数多"
    return out, ""


def main():
    groups = groups_of(sys.argv[1])
    reference, problem = read_answers(open(sys.argv[3], "rb").read().split(), groups)
    if reference is None or any(b is None or not good(a, b) for a, b in zip(groups, reference)):
        print("参考答案有误"); sys.exit(3)
    student, problem = read_answers(open(sys.argv[2], "rb").read().split(), groups)
    if student is None:
        verdict(False, problem)
    for index, (a, b) in enumerate(zip(groups, student), 1):
        if b is None:
            verdict(False, f"第 {index} 组存在满足题意的 b，不应输出 NO")
        if not good(a, b):
            verdict(False, f"第 {index} 组的 b 不满足题意")
    verdict(True, "ok")


main()
