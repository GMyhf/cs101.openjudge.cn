# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
def is_isomorphic(s, t):
    if len(s) != len(t):
        return "NO"
    
    # 创建两个映射表
    s_to_t = {}
    t_to_s = {}
    
    for i in range(len(s)):
        char_s = s[i]
        char_t = t[i]
        
        # 检查 s 到 t 的映射
        if char_s in s_to_t:
            if s_to_t[char_s] != char_t:
                return "NO"
        else:
            s_to_t[char_s] = char_t
        
        # 检查 t 到 s 的映射
        if char_t in t_to_s:
            if t_to_s[char_t] != char_s:
                return "NO"
        else:
            t_to_s[char_t] = char_s
    
    return "YES"

# 输入
s = input().strip()
t = input().strip()

# 输出结果
print(is_isomorphic(s, t))
