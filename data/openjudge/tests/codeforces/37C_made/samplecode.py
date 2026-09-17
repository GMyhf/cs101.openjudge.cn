#!/usr/bin/env python3
# Codeforces 37C Old Berland Language —— 参考实现。
# 为本仓库编写的交接件（2026-09-17，特判数据重建），不取自任何提交，不套用外部许可。
#
# 按长度从短到长分配「规范前缀码」：当前码字 code（整数），换到更长的长度 l 时左移补 0，
# 分配后加一；若 code 已经需要 l+1 位（code >= 2**l）说明 Kraft 和超过 1，无解。
import sys

data = sys.stdin.buffer.read().split()
n = int(data[0])
lengths = list(map(int, data[1:1 + n]))
order = sorted(range(n), key=lambda i: lengths[i])
words = [""] * n
code = 0
previous = 0
for i in order:
    code <<= lengths[i] - previous
    previous = lengths[i]
    if code >> lengths[i]:
        print("NO")
        sys.exit(0)
    words[i] = format(code, "b").zfill(lengths[i])
    code += 1
sys.stdout.write("YES\n" + "\n".join(words) + "\n")
