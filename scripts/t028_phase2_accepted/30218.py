# External reference: http://cs101.openjudge.cn/practice/30218/statistics/
# Accepted submission: 52789483
# Source: http://cs101.openjudge.cn/practice/solution/52789483/
# License: not declared on the submission page; no license is inferred.

n = int(input())
units = list(map(int, input().split()))
stack = []

for unit in units:
    if unit > 0:
        # 勇士，直接入栈
        stack.append(unit)
    else:
        # 怪物，需要和栈顶勇士战斗
        monster_hp = -unit  # 怪物原始生命值（正数）
        alive = True  # 标记怪物是否存活
        while stack and stack[-1] > 0 and alive:
            warrior_hp = stack.pop()  # 取出栈顶勇士
            # 战斗：互减生命值
            warrior_remain = warrior_hp - monster_hp
            monster_remain = monster_hp - warrior_hp

            if warrior_remain > 0:
                # 勇士存活，怪物死亡
                stack.append(warrior_remain)
                alive = False
            elif monster_remain > 0:
                # 怪物存活，继续和下一个勇士战斗
                monster_hp = monster_remain
            else:
                # 双方都死亡
                alive = False
        # 若怪物存活且栈中无勇士，怪物入栈
        if alive:
            stack.append(-monster_hp)

# 输出结果
print(len(stack))
if stack:
    print(' '.join(map(str, stack)))
else:
    print()  # 无幸存者时输出空行
