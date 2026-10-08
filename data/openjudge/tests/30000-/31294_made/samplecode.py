#!/usr/bin/env python3
"""31294 大肥鱼卖白饭 —— 参考实现（仓库交接件，非平台提交，不套用外部许可）。

只记手里 5 元、10 元各几张（20 元永远找不出去，不用记）。收 10 元找一张 5 元；
收 20 元要找 15 元，**优先 10+5**，不行再 5+5+5 —— 10 元只能在找 15 元时派上用场，
而 5 元哪儿都用得上，先花掉 10 元永远不亏。刚收下的那张面额都不小于要找的钱，
帮不上当前这位顾客。
"""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    five = ten = 0
    for bill in map(int, data[1:1 + n]):
        if bill == 5:
            five += 1
        elif bill == 10:
            if five == 0:
                print("NO")
                return
            five -= 1
            ten += 1
        else:
            if ten > 0 and five > 0:
                ten -= 1
                five -= 1
            elif five >= 3:
                five -= 3
            else:
                print("NO")
                return
    print("YES")


if __name__ == "__main__":
    main()
