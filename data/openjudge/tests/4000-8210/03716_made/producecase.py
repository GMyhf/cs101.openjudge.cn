"""3716 配置文件解析 测试数据生成器：固定种子，重跑可逐字节复现 data/。

题面约束（valid() 逐条核）：
  - 行数小于 20，每行字符数小于 50（描述里另有「不超过 100」，取更紧的 <50）；
  - 每行第 1 个字符不为空格；三种行：配置行（三段，之间用若干空格隔开）、
    以 '#' 开头的注释行、空行；
  - 第 1 行和最后一行不为空行，最后一行固定为 "# End of the config file"。

2026-10 审计修正：原生成器最多可产出 26 行（越出「行数小于 20」），且除样例外
配置项之间都只有单个空格、从没出现过 0 个配置行，按单空格 split 取 [1][2] 的错误写法
抓不住。现在：行数封顶 19，随机插入多空格分隔、各种注释形态，覆盖 0 个配置行 /
19 行满规模 / 49 字符长行。
"""
import random
import re
import subprocess
import tempfile
from pathlib import Path

REFERENCE_SOURCE = 'import sys\nout=[]\nfor line in sys.stdin.read().splitlines():\n    parts=line.split()\n    if parts and not parts[0].startswith("#"):\n        out.append(" ".join(parts[1:]))\nprint(len(out))\nfor x in out: print(x)\n'
SAMPLE_IN = '# Start of my config file\n\n# time config\ntimevar TIMESLOT  120\ntimevar TIMEOUT 600\n\n# port config\nportvar HTTP_PORTS [80,8000,8080,8888]\n\n# End of the config file\n'
SAMPLE_OUT = '3\nTIMESLOT 120\nTIMEOUT 600\nHTTP_PORTS [80,8000,8080,8888]\n'
END = "# End of the config file"
CONFIG_RE = re.compile(r"[^ #][^ ]* +[^ ]+ +[^ ]+")


def valid(text):
    if not text.endswith("\n") or "\r" in text or "\t" in text:
        return False
    lines = text[:-1].split("\n")
    if not 1 <= len(lines) < 20:
        return False
    if lines[0] == "" or lines[-1] != END:
        return False
    for line in lines:
        if len(line) >= 50:
            return False
        if any(not (32 <= ord(ch) < 127) for ch in line):
            return False
        if line == "" or line.startswith("#"):
            continue
        if not CONFIG_RE.fullmatch(line):
            return False
    return True


TYPES = ["timevar", "portvar", "pathvar", "strvar", "intvar", "v", "listvar"]
KEYS = ["TIMESLOT", "TIMEOUT", "HTTP_PORTS", "PATH", "NAME", "K", "MAX_CONN", "retry", "x1", "LOG_LEVEL"]
VALUES = ["0", "120", "600", "[80,8000,8080,8888]", "/tmp/x", "/usr/local/bin", "abc", "-1",
          "a#b", "[1,2,3]", "3.14", "yes", "ON", "x"]
COMMENTS = ["# note", "#", "#no space", "## double", "# port config", "#   spaced   comment",
            "# timevar FAKE 1", "#x y z"]


def sep(r, spaces):
    return " " * (r.randint(1, 4) if spaces else 1)


def config_line(r, i, spaces):
    while True:
        line = (r.choice(TYPES) + sep(r, spaces) + r.choice(KEYS) + str(i) + sep(r, spaces)
                + r.choice(VALUES))
        if len(line) < 50:
            return line


def gen(r, total, n_config, spaces, long_line=False):
    """total 行（含首行注释与末行 END），其中 n_config 个配置行。"""
    middle = total - 2
    assert 0 <= n_config <= middle
    kinds = ["c"] * n_config + ["o"] * (middle - n_config)
    r.shuffle(kinds)
    lines = [r.choice(["# generated config", "# Start of my config file", "#begin"])]
    if total == 1:
        return END + "\n"
    ci = 0
    for k in kinds:
        if k == "c":
            lines.append(config_line(r, ci, spaces))
            ci += 1
        else:
            lines.append("" if r.random() < .5 else r.choice(COMMENTS))
    if long_line:
        # 把一个配置行拉到 49 个字符
        for idx, line in enumerate(lines):
            if line and not line.startswith("#"):
                head = "longvar" + " " * 3 + "LONG_KEY" + " " * 2
                lines[idx] = head + "v" * (49 - len(head))
                break
    lines.append(END)
    return "\n".join(lines) + "\n"


def build_cases():
    cases = [SAMPLE_IN]
    specials = [
        lambda r: END + "\n",                       # 只有一行，0 个配置行
        lambda r: "# only comments\n\n#x\n\n" + END + "\n",
        lambda r: gen(r, 2, 0, False),
        lambda r: gen(r, 3, 1, False),
        lambda r: gen(r, 3, 1, True),
        lambda r: gen(r, 19, 17, True),             # 19 行满规模，几乎全是配置行
        lambda r: gen(r, 19, 17, False),
        lambda r: gen(r, 19, 0, False),
        lambda r: gen(r, 19, 9, True, long_line=True),
        lambda r: gen(r, 19, 12, True),
    ]
    seed = 3716
    for f in specials:
        seed += 1
        c = f(random.Random(seed))
        if c not in cases:
            cases.append(c)
    k = 0
    while len(cases) < 40:
        k += 1
        r = random.Random(3716 * 1000 + k)
        total = r.randint(2, 19)
        c = gen(r, total, r.randint(0, total - 2), r.random() < .7, r.random() < .2)
        if c not in cases:
            cases.append(c)
    return cases


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN
    assert all(valid(c) for c in cases), [i for i, c in enumerate(cases) if not valid(c)]
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        for index, content in enumerate(cases):
            result = subprocess.run(["python3", handle.name], input=content, text=True,
                                    capture_output=True, timeout=10, check=True)
            if index == 0:
                assert result.stdout == SAMPLE_OUT
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
