mode = int(input())
if mode == 1:
    x = int(input())
    print(abs(x))
elif mode == 2:
    a, b, c = map(int, input().split())
    print(a + b, b + c, c + a)
elif mode == 3:
    a, b, c = map(int, input().split())
    print(a + b)
    print(c + b)
    print(a + c)
elif mode == 4:
    a, b, c = input().split()
    print(a, b, c, sep="->")
elif mode == 5:
    n = int(input())
    num = []
    for i in range(n):
        a = int(input())
        num.append(a)
    for x in num:
        print(x, end="#")
elif mode == 6:
    n = int(input())
    nums = list(map(int, input().split()))
    nums.sort(reverse=True)
    print(" ".join(map(str, nums)))
elif mode == 7:
    a, b = map(int, input().split())
    print(f"{a}*{b}={a*b}")
elif mode == 8:
    a, b = map(int, input().split())
    print(f"{a/b:.3f}")
elif mode == 9:
    n = int(input())
    nums = list(map(int, input().split()))
    print(",".join(map(str, nums)))
