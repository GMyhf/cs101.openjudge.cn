# External reference: /practice/30917/statistics/
# Accepted submission: 52760585
# Source: http://cs101.openjudge.cn/practice/solution/52760585/
# License: not declared on the submission page; no license is inferred.

import sys

def solve():
    # 使用 sys.stdin 读取输入，处理大数据量时比 input() 更快
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
    
    T = int(input_data[0])
    results = []
    
    for i in range(1, T + 1):
        s = input_data[i].strip()
        n = len(s)
        
        # 记录每个字符最后一次出现的下标
        last_pos = [-1] * 26
        for idx, char in enumerate(s):
            last_pos[ord(char) - ord('a')] = idx
            
        t = []               # 用列表模拟栈，方便尾部追加和弹出
        in_t = [False] * 26  # 记录字符是否已经在结果中
        
        for idx, char in enumerate(s):
            char_idx = ord(char) - ord('a')
            
            # 如果当前字符已经在结果中，直接跳过
            if in_t[char_idx]:
                continue
                
            # 贪心策略：如果栈顶元素小于当前字符，且栈顶元素在后面还会出现，则弹出
            while t and t[-1] < char and last_pos[ord(t[-1]) - ord('a')] > idx:
                removed_char_idx = ord(t.pop()) - ord('a')
                in_t[removed_char_idx] = False
                
            # 将当前字符加入结果并标记为已存在
            t.append(char)
            in_t[char_idx] = True
            
        results.append("".join(t))
        
    # 统一输出所有结果
    print("\n".join(results))

if __name__ == "__main__":
    solve()