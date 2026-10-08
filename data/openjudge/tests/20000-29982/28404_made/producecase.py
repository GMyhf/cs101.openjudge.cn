# 28404 餐厅订单页面设计 测试数据生成器
# 用法：在本目录下 python3 producecase.py；答案由同目录 samplecode.py 生成。
# 避开歧义：
#   - 「按字母顺序」可读成区分大小写的字典序或忽略大小写，生成的餐品名在两种序下排序一致；
#   - 名字不以空格开头或结尾、不含连续空格，免得 strip/split 的写法与原样处理分歧。
import random
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SAMPLE = ('6\nDavid,3,Ceviche\nCorina,10,Beef-Burrito\nDavid,3,Fried-Chicken\nCarla,5,Water\n'
          'Carla,5,Ceviche\nRous,3,Ceviche\n')
UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LOWER = 'abcdefghijklmnopqrstuvwxyz'
NAME = r'[A-Za-z -]{1,20}'


def valid(text):
    """严格照题面核输入：第一行 N（1..5*10^4），随后 N 行「姓名,桌号,餐品」；
    姓名与餐品长 1..20，只含大小写字母、'-'、空格；桌号是 1..500 的整数。"""
    if not text.endswith('\n') or '\r' in text:
        return False
    lines = text[:-1].split('\n')
    if not re.fullmatch(r'[1-9]\d*', lines[0]):
        return False
    n = int(lines[0])
    if not 1 <= n <= 50000 or len(lines) != n + 1:
        return False
    for row in lines[1:]:
        m = re.fullmatch(rf'({NAME}),([1-9]\d*),({NAME})', row)
        if not m or not 1 <= int(m[2]) <= 500:
            return False
    return True


def word(r, lo, hi):
    return r.choice(UPPER) + ''.join(r.choice(LOWER) for _ in range(r.randint(lo, hi) - 1))


def name(r, maxlen=20, words=3):
    """首字母大写的单词用 '-' 或单个空格连接，长度 <= maxlen。"""
    s = word(r, 1, min(8, maxlen))
    for _ in range(r.randint(0, words - 1)):
        t = s + r.choice('- ') + word(r, 1, 8)
        if len(t) > maxlen:
            break
        s = t
    return s


def safe_foods(foods):
    """区分大小写字典序与忽略大小写字典序一致，且忽略大小写后互不相同。"""
    low = [f.lower() for f in foods]
    return len(set(low)) == len(low) and sorted(foods) == sorted(foods, key=str.lower)


def food_pool(r, k, maxlen=20, words=3):
    pool = set()
    while len(pool) < k:
        f = name(r, maxlen, words)
        if f.lower() not in {x.lower() for x in pool}:
            pool.add(f)
    pool = sorted(pool)
    assert safe_foods(pool)
    return pool


def build(orders):
    return f'{len(orders)}\n' + ''.join(f'{c},{t},{f}\n' for c, t, f in orders)


def random_orders(r, n, tables, foods, customers):
    return [(r.choice(customers), r.choice(tables), r.choice(foods)) for _ in range(n)]


def cases():
    r = random.Random(28404)
    out = [SAMPLE]
    # N=1 最小
    out.append(build([('A', 1, 'B')]))
    out.append(build([('Zoe', 500, 'Water')]))
    # 桌号 1..500 全出现，数值排序（卡按字符串排序：10 < 9）
    foods = food_pool(r, 5)
    out.append(build([(name(r), t, r.choice(foods)) for t in r.sample(range(1, 501), 500)]))
    # 前缀相同的餐品：Fish / Fish Taco / Fish-Taco / Fishcake
    foods = ['Fish', 'Fish Taco', 'Fish-Taco', 'Fishcake', 'Fi', 'F', 'Fish-T', 'Fish Taco-Deluxe']
    assert safe_foods(foods)
    out.append(build(random_orders(r, 200, [1, 2, 9, 10, 11, 99, 100, 101, 500], foods, ['Ann', 'Bob'])))
    # 名字长度恰为 20、含空格与连字符
    foods = []
    while len(foods) < 15:
        f = name(r, 20, 4)
        f = (f + 'x' * 20)[:20]
        if safe_foods(foods + [f]):
            foods.append(f)
    custs = [(name(r, 20, 4) + 'y' * 20)[:20] for _ in range(30)] + ['Mary-Jane Watson', 'J']
    out.append(build(random_orders(r, 300, list(range(1, 501)), foods, custs)))
    # 只有一张桌 / 只有一种餐品
    out.append(build(random_orders(r, 1000, [7], food_pool(r, 30), [name(r) for _ in range(50)])))
    out.append(build(random_orders(r, 1000, list(range(1, 501)), ['Rice'], [name(r) for _ in range(50)])))
    # 同一顾客在不同桌点餐、同一桌重复点同一道菜
    out.append(build([('Same Guy', r.choice([3, 30, 300]), r.choice(['Tea', 'Tofu', 'Toast'])) for _ in range(500)]))
    # 小规模随机
    for _ in range(4):
        n = r.randint(2, 30)
        out.append(build(random_orders(r, n, list(range(1, r.randint(2, 500) + 1)),
                                       food_pool(r, r.randint(1, 10)), [name(r) for _ in range(10)])))
    # 中等规模
    for _ in range(3):
        n = r.randint(1000, 10000)
        out.append(build(random_orders(r, n, list(range(1, 501)), food_pool(r, r.randint(10, 100)),
                                       [name(r) for _ in range(200)])))
    # 满规模 N=5*10^4：500 桌、300 种餐品（短名字以控制输入体积）
    short_c = [word(r, 1, 2) for _ in range(100)]
    out.append(build(random_orders(r, 50000, list(range(1, 501)), food_pool(r, 300, 8, 1), short_c)))
    # 满规模：餐品很多（1000 种），每桌每菜逐个 list.index 的写法压力最大
    out.append(build(random_orders(r, 50000, list(range(1, 501)), food_pool(r, 1000, 6, 1), short_c)))
    # 满规模：桌号只有几张、餐品很少
    out.append(build(random_orders(r, 50000, [1, 2, 10, 100, 500], food_pool(r, 3, 6, 1), short_c)))
    # 其余随机组
    while len(out) < 30:
        n = r.choice([r.randint(1, 50), r.randint(50, 3000)])
        tables = r.sample(range(1, 501), r.randint(1, 500))
        out.append(build(random_orders(r, n, tables, food_pool(r, r.randint(1, 60)),
                                       [name(r) for _ in range(r.randint(1, 40))])))
    return out


def run(text):
    x = subprocess.run([sys.executable, str(HERE / 'samplecode.py')], input=text,
                       text=True, capture_output=True, timeout=120)
    if x.returncode:
        raise SystemExit(x.stderr)
    return x.stdout


def main():
    d = HERE / 'data'
    d.mkdir(exist_ok=True)
    cs = cases()
    assert len(set(cs)) == len(cs), '组间重复'
    for i, c in enumerate(cs):
        assert valid(c), f'第 {i} 组不合法'
        (d / f'{i}.in').write_text(c)
        (d / f'{i}.out').write_text(run(c))


if __name__ == '__main__':
    main()
