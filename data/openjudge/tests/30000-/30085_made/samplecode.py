# External reference: /practice/30085/statistics/
# Accepted submission: 52831605
# Source: http://cs101.openjudge.cn/practice/solution/52831605/
# License: not declared on the submission page; no license is inferred.

import sys

def main():
    # 读取所有输入数据
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    w = int(input_data[0])
    n = int(input_data[1])
    prices = [int(x) for x in input_data[2:2+n]]
    
    # 升序排序
    prices.sort()
    
    left = 0
    right = n - 1
    group_count = 0
    
    # 双指针扫描
    while left <= right:
        if left == right:
            # 只剩下一个纪念品，单独一组
            group_count += 1
            break
        
        if prices[left] + prices[right] <= w:
            # 两个可以分在同一组
            left += 1
            right -= 1
        else:
            # 最贵的纪念品只能单独一组
            right -= 1
        
        group_count += 1
        
    print(group_count)

if __name__ == '__main__':
    main()