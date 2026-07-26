def calculate(x):
    s_x = str(x)
    count = 0
    for char in s_x:
        count += d[int(char)]
    return count
d = {0:6, 1:2, 2:5, 3:5, 4:4, 5:5, 6:6, 7:3, 8:7, 9:6}
n = int(input())
res = 0
for i in range(1112):
    if calculate(i)*2+calculate(2*i) == n-4:
        res += 1
for i in range(1112):
    for j in range(i):
        if calculate(i)+calculate(j)+calculate(i+j) == n-4:
            res += 2
print(res)