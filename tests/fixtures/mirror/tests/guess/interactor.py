"""夹具交互器：猜 [0, n] 里的整数，最多 15 次询问。输入文件两行：n 与秘密数。"""
import sys

n, secret = map(int, open(sys.argv[1]).read().split())


def say(text):
    sys.stdout.write(f"{text}\n")
    sys.stdout.flush()


say(n)
for _ in range(15):
    line = sys.stdin.readline().split()
    if not line:
        print("程序提前结束", file=sys.stderr)
        sys.exit(42)
    if line[0] == "!":
        if len(line) == 2 and line[1] == str(secret):
            sys.exit(0)
        print("猜错了", file=sys.stderr)
        sys.exit(42)
    if line[0] != "?" or len(line) != 2 or not line[1].lstrip("-").isdigit():
        print("询问格式不对", file=sys.stderr)
        sys.exit(42)
    guess = int(line[1])
    say(0 if guess == secret else 1 if guess > secret else -1)
print("询问超过 15 次", file=sys.stderr)
sys.exit(42)
