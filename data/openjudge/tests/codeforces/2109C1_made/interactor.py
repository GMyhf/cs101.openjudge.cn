"""Interactor for Codeforces 2109C1 "Hacking Numbers (Easy Version)": at most 7 commands per test.

Written for this repository as a hand-off artifact; no external source, no external license.

Hidden data (the .in file), following the statement's "Hacks" section:
    t                      1 <= t <= 5000
    n x                    one line per test: n = target given to the program, x = the unknown
                           integer, 1 <= n, x <= 1e9
(The Hacks text says "n and x -- denoting the unknown integer and the target value ...,
respectively", which contradicts the names used everywhere else; we keep the statement's names:
n is the target, x the unknown.)  The .out file lists the per-test command limit, one per line;
it is informational only and not read here.

Protocol (Codeforces-faithful):
  * jury prints t, then for each test prints n;
  * contestant commands (whitespace-separated tokens, case sensitive):
      add y   (-1e18 <= y <= 1e18)  -> "1" and x += y if 1 <= x + y <= 1e18, else "0"
      mul y   (1 <= y <= 1e18)      -> "1" and x *= y if 1 <= x * y <= 1e18, else "0"
      div y   (1 <= y <= 1e18)      -> "1" and x //= y if y divides x, else "0"
      digit                         -> "1" and x = S(x)
      !                             -> "1" if x == n (next test starts), else "-1" and WA
    y must be a canonical decimal integer (no '+', no leading zeros, no "-0").
  * an invalid command or a command beyond the per-test limit gets "-1" and WA;
    "!" does not count toward the limit.
  * after the last test the jury closes its output (the program sees EOF) and reads the
    rest of the program's output: anything but whitespace is WA ("extra output").
Exit 0 = accepted, 42 = wrong answer.  stderr's last line is the verdict message.
"""
import os
import re
import sys

WRONG = 42
BIG = 10 ** 18
INT_RE = re.compile(rb"-?(?:0|[1-9][0-9]*)\Z")


def limit_for(n):
    return 7


def fail(message):
    sys.stderr.write(message + "\n")
    sys.stderr.flush()
    os._exit(WRONG)


def say(value):
    data = f"{value}\n".encode()
    try:
        while data:
            data = data[os.write(1, data):]
    except OSError:
        fail("程序已提前退出，交互未完成")


class Tokens:
    def __init__(self):
        self.stream = sys.stdin.buffer
        self.pending = []

    def next(self):
        while not self.pending:
            try:
                line = self.stream.readline()
            except OSError:
                line = b""
            if not line:
                return None
            self.pending = line.split()
            self.pending.reverse()
        return self.pending.pop()

    def rest_is_blank(self):
        if self.pending:
            return False
        while True:
            try:
                chunk = self.stream.read1(65536)
            except OSError:
                return True
            if not chunk:
                return True
            if chunk.strip():
                return False


def parse_int(token, low, high):
    if token is None or len(token) > 20 or not INT_RE.match(token) or token == b"-0":
        return None
    value = int(token)
    return value if low <= value <= high else None


def digit_sum(v):
    return sum(map(int, str(v)))


def main():
    with open(sys.argv[1], "rb") as handle:
        numbers = list(map(int, handle.read().split()))
    t = numbers[0]
    tests = [(numbers[1 + 2 * i], numbers[2 + 2 * i]) for i in range(t)]
    tokens = Tokens()
    say(t)
    for index, (n, x) in enumerate(tests, 1):
        say(n)
        limit = limit_for(n)
        used = 0
        while True:
            word = tokens.next()
            if word is None:
                fail(f"第 {index} 个测试还没回答「!」程序就结束了")
            if word == b"!":
                if x == n:
                    say(1)
                    break
                say(-1)
                fail(f"第 {index} 个测试回答「!」时 x 不等于 n")
            if word == b"digit":
                used += 1
                if used > limit:
                    say(-1)
                    fail(f"第 {index} 个测试的命令数超过上限 {limit}")
                x = digit_sum(x)
                say(1)
                continue
            if word not in (b"add", b"mul", b"div"):
                say(-1)
                fail(f"第 {index} 个测试收到无法识别的命令（命令区分大小写）")
            argument = tokens.next()
            if argument is None:
                fail(f"第 {index} 个测试的命令缺少参数，程序就结束了")
            used += 1
            if used > limit:
                say(-1)
                fail(f"第 {index} 个测试的命令数超过上限 {limit}")
            if word == b"add":
                y = parse_int(argument, -BIG, BIG)
            else:
                y = parse_int(argument, 1, BIG)
            if y is None:
                say(-1)
                fail(f"第 {index} 个测试的命令参数不合法或越界")
            if word == b"add":
                res = x + y
                ok = 1 <= res <= BIG
            elif word == b"mul":
                res = x * y
                ok = 1 <= res <= BIG
            else:
                ok = x % y == 0
                res = x // y
            if ok:
                x = res
            say(1 if ok else 0)
    try:
        os.close(1)
    except OSError:
        pass
    if not tokens.rest_is_blank():
        fail("所有测试回答完后程序还有多余输出")
    os._exit(0)


main()
