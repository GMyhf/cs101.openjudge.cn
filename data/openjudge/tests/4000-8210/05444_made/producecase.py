"""5444 堆栈基本操作 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的数据。

第 0 组是题面样例；第 1~36 组沿用原生成方式（小规模：随机打乱/逆序/末元素越界/含重复）；
第 37 组起是加强组：随机合法出栈序列（含 n 到 10000）、恒等序列、前面都合法只在末尾出错（卡掉边模拟边输出、
出错前已打印部分操作的写法）、含 0/负数/大于 n 的数。原第 37~39 组与第 1~3 组重复，已换成加强组。
"""
import random, subprocess
from pathlib import Path
ROOT = Path(__file__).parent
SAMPLE = '7\n4 5 3 6 2 7 1\n'


def valid(text):
    """题面：两行，第一行为 n（序列元素个数），第二行为 n 个整数（可能不在 1…n 之间）。"""
    lines = text.split("\n")
    if len(lines) != 3 or lines[2] != "" or not lines[0].isdigit() or int(lines[0]) < 1:
        return False
    items = lines[1].split(" ")
    return len(items) == int(lines[0]) and all(x.lstrip("-").isdigit() and x[:2] != "-0" for x in items)


def stack_perm(rng, n, push_bias=0.5):
    """随机合法出栈序列。"""
    out, stack, nxt = [], [], 1
    while len(out) < n:
        if nxt <= n and (not stack or rng.random() < push_bias):
            stack.append(nxt); nxt += 1
        else:
            out.append(stack.pop())
    return out


def late_break(rng, seq):
    """把合法序列的末尾弄坏：交换末段两个元素成非法序列，或末元素换成越界值/重复值。"""
    n = len(seq); seq = seq[:]
    kind = rng.randrange(3)
    if kind == 0:
        seq[-1] = rng.choice([0, -1, n + 1, 10 ** 9])
    elif kind == 1:
        seq[-1] = seq[-2]
    else:
        # 找末段一对使序列非法的交换
        for _ in range(1000):
            i = rng.randrange(max(0, n - 6), n - 1); j = rng.randrange(i + 1, n)
            t = seq[:]; t[i], t[j] = t[j], t[i]
            if not ok(t):
                return t
        seq[-1] = n + 1
    return seq


def ok(seq):
    stack, nxt = [], 1
    for w in seq:
        while nxt <= len(seq) and (not stack or stack[-1] != w):
            stack.append(nxt); nxt += 1
        if not stack or stack[-1] != w: return False
        stack.pop()
    return True


def extra(i, salt=0):
    rng = random.Random(544400 + i + 1000 * salt)
    j = i - 37
    sizes = [5, 8, 12, 20, 50, 100, 1000, 3000, 10000, 10000]
    n = sizes[j % len(sizes)] 
    t = j // len(sizes)
    if t == 0:
        seq = stack_perm(rng, n, rng.choice([0.3, 0.5, 0.7]))          # 合法：随机出栈序列
    elif t == 1:
        seq = late_break(rng, stack_perm(rng, n))                       # 非法：末尾才出错
    else:
        seq = list(range(1, n + 1)) if j % 2 else stack_perm(rng, n, 0.9)  # 恒等序列 / 接近逆序
        if j % 3 == 0:
            seq[rng.randrange(n)] = -rng.randint(1, 100)               # 混入负数
    return str(n) + '\n' + ' '.join(map(str, seq)) + '\n'


def case(i):
    if i == 0: return SAMPLE
    if i >= 37: return extra(i)
    rng=random.Random(544400+i); n=1+i%18
    if i%4==0:
        seq=list(range(1,n+1)); rng.shuffle(seq)
    elif i%4==1:
        seq=list(range(n,0,-1))
    elif i%4==2:
        seq=list(range(1,n+1)); seq[-1]=n+1
    else:
        seq=list(range(1,n+1)); seq[n//2]=seq[max(0,n//2-1)]
    return str(n)+'\n'+' '.join(map(str,seq))+'\n'


def main():
    cases = []
    for i in range(67):
        c, salt = case(i), 0
        while c in cases:  # 与已有组撞车就换种子重抽
            salt += 1; c = extra(i, salt)
        cases.append(c)
    assert all(valid(c) for c in cases), "有数据越出题面约束"
    assert len(set(cases)) == len(cases), "有重复组"
    for i, inp in enumerate(cases):
        out=subprocess.run(['python3',str(ROOT/'samplecode.py')],input=inp,text=True,capture_output=True,check=True).stdout
        (ROOT/'data'/f'{i}.in').write_text(inp); (ROOT/'data'/f'{i}.out').write_text(out)


if __name__ == "__main__":
    main()
