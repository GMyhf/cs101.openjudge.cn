# 累计偏移 + 按余数前缀和，O(65536*2 + M)；替换原 O(NM) 逐个模拟写法以承受满规模数据
MOD = 65536


def solve(text):
    """累计偏移 D；第 i 位为 1 ⇔ (v mod 2^(i+1) + D mod 2^(i+1)) mod 2^(i+1) ≥ 2^i，按余数前缀和 O(1) 回答。"""
    data = text.split(); n, m = int(data[0]), int(data[1])
    cnt = [0] * MOD
    for token in data[2:2 + n]:
        cnt[int(token)] += 1
    prefix = [None] * 16
    level = cnt
    for i in range(15, -1, -1):
        size = 1 << (i + 1)
        if len(level) != size:
            level = [level[r] + level[r + size] for r in range(size)]
        acc = [0] * (size + 1)
        for r in range(size):
            acc[r + 1] = acc[r] + level[r]
        prefix[i] = acc
    offset = 0; out = []; pos = 2 + n
    for _ in range(m):
        op, x = data[pos], int(data[pos + 1]); pos += 2
        if op == "C":
            offset = (offset + x) % MOD
        else:
            size = 1 << (x + 1); half = 1 << x; d = offset % size; acc = prefix[x]
            lo, hi = (half - d) % size, (size - d) % size  # 余数落在循环区间 [lo, hi)
            out.append(str(acc[hi] - acc[lo] if lo < hi else acc[size] - acc[lo] + acc[hi]))
    return "\n".join(out) + ("\n" if out else "")


if __name__ == '__main__':
    import sys
    sys.stdout.write(solve(sys.stdin.read()))
