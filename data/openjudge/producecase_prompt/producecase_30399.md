请根据生成数据的模版 producecase_template.py，以及能够AC的代码ac.py，给出下面这个题目的生产数据的 producecase.py。题面的heights[r][c]缺少范围，也请给出。



## 两样滑雪场

A有一个矩形滑雪场坐落在两洋之间，太平洋处于滑雪场的西边界和北边界，而大西洋处于滑雪场的东边界和南边界。

这个滑雪场被分割成 m x n个方形单元格。给定一个 m x n 的整数矩阵 heights ， heights[r][c] 表示坐标 (r, c) 处的单元格的海拔。

滑雪的时候只能滑平路或下坡，不能上坡。所以站在一个单元格，可以滑到它相邻的东西南北4个单元格中海拔没有增加的单元格。滑雪不能走回头路，即一旦向东滑后就不可向西滑；一旦向西滑后就不可向东滑；一旦向北滑后就不可向南滑；一旦向南滑后就不可向北滑。

问有哪些单元格x，以x作为起点，既可以滑到太平洋边上，也可以滑到大西洋边上。



输入

第一行输入两个整数m,n表示滑雪场的大小，1≤m,n≤10, 接下来m行，每行包含n个整数，表示矩阵heights

输出

逐行输出滑雪场矩阵中既可滑到太平洋又可滑到大西洋的坐标点(按照从上(北）到下（南), 同一行从左(西)向右(东)，的顺序输出)，若没有这样的点，输出None

样例输入

```
2 2
2 1
1 2
```

样例输出

```
0 0
0 1
1 0
1 1
```



producecase_template.py

```python
import random
import time
import os

# 确保 data 目录存在
os.makedirs("data", exist_ok=True)

def solve(m, n, k):
    """等价类划分问题逻辑 (ac.py 同款)"""
    groups = {}
    for num in range(m + 1, n):
        s = sum(map(int, str(num)))
        if s % k == 0:
            groups.setdefault(s, []).append(num)

    result_lines = []
    for s in sorted(groups):
        result_lines.append(','.join(map(str, sorted(groups[s]))))
    return result_lines


for epoch in range(20):
    # 随机生成 m, n, k
    m = random.randint(1, 9000)
    n = random.randint(m + 2, min(m + 2000, 10000))  # 保证范围合理
    k = random.randint(1, 9)

    # 写入输入文件
    with open(f"data/{epoch}.in", "w") as f:
        f.write(f"{m},{n},{k}\n")

    start = time.time()

    # 调用逻辑
    result = solve(m, n, k)

    end = time.time() - start
    print(f"[{epoch}] {end:.3f}s | m={m}, n={n}, k={k}")

    # 写入输出文件
    with open(f"data/{epoch}.out", "w") as f:
        if result:
            f.write("\n".join(result) + "\n")
        else:
            f.write("\n")  # 没有满足条件的情况


```



ac.py

```python
import sys
sys.setrecursionlimit(10000)

def main():
    import sys
    data = sys.stdin.read().split()
    if not data:
        return
    
    m = int(data[0])
    n = int(data[1])
    heights = []
    index = 2
    for i in range(m):
        row = list(map(int, data[index:index+n]))
        heights.append(row)
        index += n

    # Directions for Pacific: up (-1,0), left (0,-1)
    # Directions for Atlantic: down (1,0), right (0,1)
    
    def can_reach_pacific(r, c, visited):
        if r == 0 or c == 0:
            return True
        visited.add((r, c))
        for dr, dc in [(-1, 0), (0, -1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n:
                if (nr, nc) not in visited and heights[nr][nc] <= heights[r][c]:
                    if can_reach_pacific(nr, nc, visited):
                        return True
        return False

    def can_reach_atlantic(r, c, visited):
        if r == m - 1 or c == n - 1:
            return True
        visited.add((r, c))
        for dr, dc in [(1, 0), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n:
                if (nr, nc) not in visited and heights[nr][nc] <= heights[r][c]:
                    if can_reach_atlantic(nr, nc, visited):
                        return True
        return False

    results = []
    for r in range(m):
        for c in range(n):
            if can_reach_pacific(r, c, set()) and can_reach_atlantic(r, c, set()):
                results.append((r, c))
    
    if results:
        for r, c in results:
            print(r, c)
    else:
        print("None")

if __name__ == "__main__":
    main()
```

