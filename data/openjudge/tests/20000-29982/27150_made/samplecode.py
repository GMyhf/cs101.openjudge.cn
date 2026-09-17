# 27150 Divisibility by Eight 加强版 —— 参考实现。
# 为本仓库编写的交接件（2026-09-17，特判数据重建），不取自平台提交，不套用外部许可。
#
# 任何一个合法结果的末三位去掉前导零后仍是合法结果（1000 是 8 的倍数），所以只要
# 按不带前导零的写法枚举 0..992 里 8 的倍数，逐个查是不是输入的子序列即可。
import sys

digits = sys.stdin.readline().strip()
for value in range(0, 1000, 8):
    text = str(value)
    position = 0
    for ch in text:
        position = digits.find(ch, position)
        if position < 0:
            break
        position += 1
    else:
        print("YES")
        print(text)
        break
else:
    print("NO")
