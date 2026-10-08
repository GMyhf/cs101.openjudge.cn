# 26267 面对危机的蒂姆(KMP模板)：判断 T 是否为 S 的子串。
# 题面只说"字符串长度不超过 1000000"，样例为大写字母；为免歧义，只生成 A-Z、非空、无空白的两行。
import random
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAXLEN = 1000000
SAMPLE = 'SOFUNNYANDTIRINGWASHERGAME\nINGWA\n'
UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def valid(text):
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    if len(lines) != 2:
        return False
    for s in lines:
        if not (1 <= len(s) <= MAXLEN):
            return False
        if any(c not in UPPER for c in s):
            return False
    return True


def rs(r, n, alpha):
    return ''.join(r.choice(alpha) for _ in range(n))


def mk(s, t):
    return f'{s}\n{t}\n'


def random_case(r, n_hi, m_hi, alpha, mode):
    n = r.randint(1, n_hi)
    m = r.randint(1, min(m_hi, n))
    s = rs(r, n, alpha)
    t = rs(r, m, alpha)
    if mode == 'plant':
        at = r.randint(0, n - m)
        s = s[:at] + t + s[at + m:]
    elif mode == 'near':
        # 处处放"差最后一个字符"的近似匹配，确保答案为 NO（若意外匹配上也无妨，答案由参考解给出）
        bad = t[:-1] + (alpha[(alpha.index(t[-1]) + 1) % len(alpha)])
        reps = max(1, n // (2 * m))
        lst = list(s)
        for _ in range(reps):
            at = r.randint(0, n - m)
            lst[at:at + m] = bad
        s = ''.join(lst)
    return mk(s, t)


def build_cases():
    r = random.Random(26267)
    cases = [SAMPLE]
    # 满规模：卡朴素 O(nm) 的写法
    cases.append(mk('A' * MAXLEN, 'A' * 4999 + 'B'))                      # NO
    cases.append(mk('A' * (MAXLEN - 1) + 'B', 'A' * 4999 + 'B'))          # YES，只在末尾
    big = rs(r, MAXLEN, 'AB')
    cases.append(mk(big, big[MAXLEN - 40000:]))                           # YES，T 是 S 的后缀
    # 边界
    cases.append(mk('A', 'A'))
    cases.append(mk('A', 'B'))
    cases.append(mk('AB', 'ABC'))                                         # T 比 S 长
    cases.append(mk('ABCDEFG', 'ABCDEFG'))                                # T == S
    cases.append(mk('ABABABABAC', 'ABABAC'))                              # 需要回退的匹配
    cases.append(mk('ABABABABAB', 'ABABAC'))
    cases.append(mk('AAAAAAAAAB', 'AAAB'))
    cases.append(mk('BAAAAAAAAA', 'BA'))                                  # 开头
    cases.append(mk('ZZZZZZZZZZ', 'Z' * 11))                              # 同字符、更长
    s = rs(r, 5000, UPPER)
    cases.append(mk(s, s[:2000]))                                         # 前缀
    t = s[:-1] + ('A' if s[-1] != 'A' else 'B')
    cases.append(mk(s, t))                                                # 只差最后一个字符
    cases.append(mk('Q' * 1000 + 'R', 'Q' * 1000 + 'R' + 'Q'))
    # 随机组：不同字母表、植入 / 近似 / 纯随机
    alphas = ['AB', 'ABCD', UPPER]
    modes = ['plant', 'near', 'rand']
    for i in range(27):
        alpha = alphas[i % 3]
        mode = modes[(i // 3) % 3]
        n_hi = [50, 2000, 30000][i % 3]
        m_hi = [8, 300, 3000][(i // 9) % 3]
        c = random_case(r, n_hi, m_hi, alpha, mode)
        while c in cases:
            c = random_case(r, n_hi, m_hi, alpha, mode)
        cases.append(c)
    return cases


def run_ref(text):
    x = subprocess.run([sys.executable, str(HERE / 'samplecode.py')], input=text,
                       text=True, capture_output=True, timeout=120)
    if x.returncode:
        raise SystemExit(x.stderr)
    return x.stdout


def main():
    cases = build_cases()
    assert len(set(cases)) == len(cases), '存在重复组'
    d = HERE / 'data'
    d.mkdir(exist_ok=True)
    for i, c in enumerate(cases):
        assert valid(c), f'第 {i} 组不合法'
        (d / f'{i}.in').write_text(c)
        (d / f'{i}.out').write_text(run_ref(c))


if __name__ == '__main__':
    main()
