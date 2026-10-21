#!/usr/bin/env python3
"""1000002: deterministic cases; answers use direct substring comparison."""
import random
from pathlib import Path


def valid(text):
    fields = text.split()
    if not fields:
        return False
    try:
        count = int(fields[0])
    except ValueError:
        return False
    return (1 <= count <= 10 and len(fields) == count + 1
            and all(1 <= len(s) <= 2000 and all('a' <= c <= 'z' for c in s)
                    for s in fields[1:]))


def oracle(s):
    # Enumerate starts first, independently of the reference's run algorithm.
    for start in range(len(s)):
        for length in range(1, (len(s) - start) // 2 + 1):
            if s[start:start + length] == s[start + length:start + 2 * length]:
                return start
    return -1


def squarefree(n):
    s = '0'
    while len(s) < n:
        s = ''.join({'0': '012', '1': '02', '2': '1'}[c] for c in s)
    return s[:n].translate(str.maketrans('012', 'abc'))


def cases():
    rng = random.Random(1000002)
    yield ['abcabcaa', 'dabcabc', 'abc', 'aa', 'a', 'abcc']
    yield ['z', 'ab', 'zz', 'aba', 'abab', 'abba', 'abcd', 'abcab', 'abcabc', 'abcdabcd']
    yield ['abcabcaa', 'dabcabcaa', 'zabcdabcdaa', 'xyzxyzbb', 'abcdabcdee']
    yield ['abcdefgg', 'abcdefghijklmnopqrstuvwxyzz', 'abcabca', 'abacaba']
    yield ['a' * n for n in [2, 3, 4, 5, 10, 99, 200, 999, 1999, 2000]]
    yield [squarefree(n) for n in [10, 20, 50, 100, 200, 500, 999, 1500, 1999, 2000]]
    yield [squarefree(n) + 'zz' for n in [1, 7, 31, 100, 511, 998, 1998]]
    yield [squarefree(n) * 2 for n in [5, 13, 51, 200, 500, 1000]]
    yield ['z' + squarefree(999) * 2, squarefree(998) + 'zz']
    yield [('ab' * 1000), ('abc' * 666) + 'ab', 'abcdefghijklmnopqrstuvwxyz' * 76]
    for k in range(11):
        alphabet = ['ab', 'abc', 'abcd', 'abcdefghijklmnopqrstuvwxyz'][k % 4]
        strings = []
        for j in range(10):
            n = rng.randint(1, 2000 if k >= 7 else 150)
            s = ''.join(rng.choice(alphabet) for _ in range(n))
            if j % 3 == 0 and len(s) <= 1000:
                s += s
            strings.append(s)
        yield strings


def build():
    data = Path(__file__).parent / 'data'
    data.mkdir(exist_ok=True)
    inputs = set()
    for index, strings in enumerate(cases()):
        assert 1 <= len(strings) <= 10
        assert all(1 <= len(s) <= 2000 and all('a' <= c <= 'z' for c in s) for s in strings)
        text = str(len(strings)) + '\n' + '\n'.join(strings) + '\n'
        assert valid(text)
        assert text not in inputs
        inputs.add(text)
        answers = '\n'.join(str(oracle(s)) for s in strings) + '\n'
        (data / f'{index}.in').write_text(text, encoding='utf-8')
        (data / f'{index}.out').write_text(answers, encoding='utf-8')
    print(f'generated {len(inputs)} cases')


if __name__ == '__main__':
    build()
