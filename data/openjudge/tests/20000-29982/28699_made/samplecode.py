# External reference: statistics page /practice/28699/
# Accepted submission: 52832114
# Source: http://cs101.openjudge.cn/practice/solution/52832114/
# License: not declared on the submission page; no license is inferred.

import sys
from collections import Counter

def solve():
    # 读取所有输入
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    m = int(input_data[1])
    
    # 提取价格并从小到大排序
    prices = [int(x) for x in input_data[2:2+n]]
    prices.sort()
    
    # 提取水果清单
    fruits = input_data[2+n : 2+n+m]
    
    # 统计每种水果的出现频次，并按频次从大到小排序
    counter = Counter(fruits)
    frequencies = list(counter.values())
    frequencies.sort(reverse=True)
    
    # 计算最小总价：高频次配低价格
    min_price = sum(freq * price for freq, price in zip(frequencies, prices))
    
    # 计算最大总价：高频次配高价格
    max_price = sum(freq * price for freq, price in zip(frequencies, prices[::-1]))
    
    print(min_price, max_price)

if __name__ == '__main__':
    solve()