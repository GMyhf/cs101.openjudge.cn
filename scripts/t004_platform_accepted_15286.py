import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    w = int(input_data[1])
    
    items = []
    for i in range(n):
        items.append(int(input_data[2 + i]))
        
    # 核心剪枝 1：从大到小排序，优先放大的道具
    items.sort(reverse=True)
    
    # ans 记录全局最优解，最坏情况下需要 n 个包（每个道具一个包）
    ans = n
    # bags 数组就是你要的“记录装了一半的包”的数据结构
    bags = []

    def dfs(idx):
        nonlocal ans
        
        # 核心剪枝 2：如果当前用的包数已经大于等于已知的最优解，直接放弃这条搜索分支
        if len(bags) >= ans:
            return
            
        # 如果所有道具都放完了，更新最优解
        if idx == n:
            ans = min(ans, len(bags))
            return
            
        current_item = items[idx]
        
        # 尝试 1：把当前道具放进已经开过的包里
        for i in range(len(bags)):
            if bags[i] + current_item <= w:
                bags[i] += current_item  # 放进去
                dfs(idx + 1)             # 继续放下一个道具
                bags[i] -= current_item  # 回溯：拿出来，尝试下一种可能
                
        # 尝试 2：新开一个包来装当前道具
        bags.append(current_item)
        dfs(idx + 1)
        bags.pop() # 回溯：把新开的包撤销

    dfs(0)
    print(ans)

if __name__ == '__main__':
    solve()
