# External reference: statistics page /practice/22507/
# Accepted submission: 52740160
# Source: http://cs101.openjudge.cn/practice/solution/52740160/
# License: not declared on the submission page; no license is inferred.

# External reference: statistics page /practice/22507/
# Accepted submission: 52740160
# Source: http://cs101.openjudge.cn/practice/solution/52740160/
# License: not declared on the submission page; no license is inferred.

def check_unique(s):
    # 检查是否有重复字符
    return len(set(s)) == len(s)

def count_ways(pre, post):
    # 基本不合法情况
    if len(pre) != len(post):
        return 0
    if not check_unique(pre) or not check_unique(post):
        return 0
    
    n = len(pre)
    res = 1
    
    # 递归函数：返回子树是否合法，同时统计单孩子节点数
    def dfs(pl, pr, pol, por):
        nonlocal res
        if pl > pr:
            return True
        # 前序第一个 = 后序最后一个 = 根
        if pre[pl] != post[por]:
            return False
        # 只有一个节点
        if pl == pr:
            return True
        
        # 左子树根：pre[pl+1]
        left_root = pre[pl+1]
        # 在后序中找到左子树根位置
        if left_root not in post[pol:por+1]:
            return False
        pos = post[pol:por].index(left_root) + pol
        left_size = pos - pol + 1
        
        # 递归左右
        ok1 = dfs(pl+1, pl+left_size, pol, pos)
        ok2 = dfs(pl+left_size+1, pr, pos+1, por-1)
        if not ok1 or not ok2:
            return False
        
        # 只有一个孩子 → 2种形态
        if (pl+left_size+1 > pr) or (pl+1 > pl+left_size):
            res *= 2
        return True
    
    valid = dfs(0, n-1, 0, n-1)
    return res if valid else 0

# 多组输入
import sys
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    pre, post = line.split()
    print(count_ways(pre, post))