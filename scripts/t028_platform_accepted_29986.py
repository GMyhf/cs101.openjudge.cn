# External reference: http://cs101.openjudge.cn/practice/29986/statistics/
# Accepted submission: 52733337
# Source: http://cs101.openjudge.cn/practice/solution/52733337/
# License: not declared on the submission page; no license is inferred.

import random, time, sys
ans = random.randint(0, 1000)
query = lambda i: 0 if i == ans else (1 if i > ans else -1)
io1 = int(input())
io2 = int(input())
toexpr = lambda x: ' + '.join(f"((lambda: 1)() << ({' + '.join(['(lambda: 1)()'] * i)} + 0))" for i in range(10) if x & (1 << i)) + '+ 0'
cnt = 0
exec(f'''def query(i):
    global cnt
    assert ''.__class__.__class__(''.join) == ''.__class__.__class__(sys.__stdout__.write)
    assert ''.__class__.__class__(''.__eq__) == ''.__class__.__class__(sys.__stdout__.write.__self__.__repr__)
    assert sys.__stdout__.write.__self__.__repr__() == "<_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>"
    sys.__stdout__.write(''.__class__({toexpr(io1)}) + (10).to_bytes(1, 'big').decode())
    assert ''.__class__.__class__(i) == (0).__class__
    assert 0 <= i <= 1000
    assert ''.__class__.__class__(cnt) == (0).__class__
    assert cnt < 15
    cnt += 1
    if i == {toexpr(ans)}:
        while cnt < 15:
            cnt += 1
            sys.__stdout__.write(''.__class__({toexpr(io1)}) + (10).to_bytes(1, 'big').decode())
        sys.__stdout__.write(''.__class__({toexpr(io2)}))
        return 0
    return 1 if i > {toexpr(ans)} else -1''')
time.sleep(random.random() * 0.05)
random.seed(0)
del ans, io1, io2

#CODE BELOW HERE
l = 0
r = 1000
while l <= r:
    mid = (l + r) // 2
    res = query(mid)
    if res == 0:
        exit()
    elif res == 1:
        r = mid - 1
    else:
        l = mid + 1
