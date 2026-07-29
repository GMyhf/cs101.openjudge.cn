# External reference: http://cs101.openjudge.cn/practice/01729/statistics/
# Accepted submission: 50227328
# Source: http://cs101.openjudge.cn/practice/solution/50227328/
# License: not declared on the submission page; no license is inferred.

import heapq
Jack_x = 0
Jack_y = 0
Jill_x = 0
Jill_y = 0
result = []

def bfs():
    while True:
        length,x1,y1,p1,x2,y2,p2 = heapq.heappop(heap)
        if (x1,y1) == s_Jack and (x2,y2) == s_Jill:
            return round(pow(-length,0.5),2),p1,p2

        if (x1,y1) == s_Jack:
            l1 = [(x1,y1)]
        else:
            l1 = [(x1+1,y1),(x1-1,y1),(x1,y1+1),(x1,y1-1)]
        if (x2,y2) == s_Jill:
            l2 = [(x2,y2)]
        else:
            l2 = [(x2+1,y2),(x2-1,y2),(x2,y2+1),(x2,y2-1)]
        for a1,b1 in l1:
            if 0 <= a1 < n and 0 <= b1 < n:
                _ = matrix[a1][b1]
                if _ == '.' or _ == 'S' or _ == 'H':
                    for a2,b2 in l2:
                        if 0 <= a2 < n and 0 <= b2 < n:
                            _ = matrix[a2][b2]
                            if _ == '.' or _ == 's' or _ == 'h':
                                new_length = max(length,-(pow(a1 - a2,2) + pow(b1 - b2,2)))
                                if dp[a1][a2][b1][b2] > new_length:
                                    dp[a1][a2][b1][b2] = new_length
                                    if a1 - x1 == 0:
                                        if b1 - y1 == 1:
                                            d1 = 'E'
                                        elif b1 - y1 == -1:
                                            d1 = 'W'
                                        else:
                                            d1 = ''
                                    elif a1 - x1 == 1:
                                        d1 = 'S'
                                    else:
                                        d1 = 'N'
                                    if a2 - x2 == 0:
                                        if b2 - y2 == 1:
                                            d2 = 'E'
                                        elif b2 - y2 == -1:
                                            d2 = 'W'
                                        else:
                                            d2 = ''
                                    elif a2 - x2 == 1:
                                        d2 = 'S'
                                    else:
                                        d2 = 'N'
                                    heapq.heappush(heap,(new_length,a1,b1,p1+d1,a2,b2,p2+d2))






while True:
    matrix = []
    heap = []
    n = int(input())
    if n == 0:
        break
    for j in range(n):
        _ = input()
        if 'H' in _:
            Jack_x,Jack_y = j,_.index('H')
        if 'h' in _:
            Jill_x,Jill_y = j,_.index('h')
        if 'S' in _:
            s_Jack = (j,_.index('S'))
        if 's' in _:
            s_Jill = (j,_.index('s'))
        matrix.append(_)
    dp = [[[[1]*n for _ in range(n)] for __ in range(n)] for ___ in range(n)]
    length_home = -(pow(Jack_x - Jill_x,2) + pow(Jack_y - Jill_y,2))
    heapq.heappush(heap,(length_home,Jack_x,Jack_y,'',Jill_x,Jill_y,''))
    result.append(bfs())
for i in result:
    for j in i:
        print(j)
