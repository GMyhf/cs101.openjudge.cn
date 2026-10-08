import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\na=sys.stdin.read().split(); n=int(a[0]); versions=a[1:1+n]\ndef key(v): return tuple(map(int,v.split(".")))\nprint("\\n".join(sorted(versions,key=key)))'
SAMPLE_IN='9\n4.8\n4.8.2\n7.2\n2.96\n3.4.5\n1.0\n2\n6.4\n1.0.0\n'
def g23007(r):
    versions = []
    for _ in range(r.randint(1, 20)):
        versions.append(".".join(str(r.randint(0, 100)) for _ in range(r.randint(1, 6))))
    return str(len(versions)) + "\n" + "\n".join(versions) + "\n"


def valid(text):
    # 题面：第一行 N（1 ≤ N ≤ 100）；以下 N 行每行一个版本号，版本号为若干由 '.' 连接的非负整数，
    # 版本号总长度不超过 100，主版本号和每个子版本号的数值不超过 100
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    h = lines[0]
    if not (h.isdigit() and h.isascii() and h[0] != "0"):
        return False
    n = int(h)
    if not 1 <= n <= 100 or len(lines) != n + 1:
        return False
    for v in lines[1:]:
        if not 1 <= len(v) <= 100:
            return False
        for part in v.split("."):
            if not (part.isdigit() and part.isascii()) or (len(part) > 1 and part[0] == "0"):
                return False
            if int(part) > 100:
                return False
    return True

def special_cases():
    r = random.Random(23007)
    out = []
    def pack(vs): return str(len(vs)) + "\n" + "\n".join(vs) + "\n"
    out.append(pack(["100.100.100"]))                                          # N=1
    out.append(pack([str(r.randint(0, 100)) for _ in range(100)]))              # 只有主版本号（20% 子任务），卡字符串比较
    out.append(pack([f"{r.randint(0, 100)}.{r.choice([0, 1, 2, 9, 10, 11, 19, 20, 90, 99, 100])}" for _ in range(100)]))  # 两段，卡按浮点数比较
    chain = []
    for base in ["1", "4.8.2", "0", "100", "7.10"]:
        for z in range(8):
            chain.append(base + ".0" * z)
    chain += [f"{b}.{r.randint(0, 100)}" for b in ["1", "4.8.2", "0", "7.10"] for _ in range(15)]
    r.shuffle(chain); chain.sort(key=lambda v: -len(v.split(".")))           # 长的在前，卡补 0 后视为相等的写法
    out.append(pack(chain))
    longv = []
    for _ in range(100):
        parts = ["1"] * 49 + [str(r.randint(0, 9))]
        parts[r.randint(30, 48)] = str(r.randint(0, 1))
        longv.append(".".join(parts))                                          # 长度 99，差异在深层
    out.append(pack(longv))
    mix = []
    pref = [".".join(str(r.randint(0, 100)) for _ in range(r.randint(1, 3))) for _ in range(8)]
    for _ in range(100):
        p = r.choice(pref)
        if r.random() < .8:
            p += "".join("." + str(r.choice([0, 1, 5, 9, 10, 50, 99, 100])) for _ in range(r.randint(1, 4)))
        mix.append(p)                                                          # 共享前缀的混合
    out.append(pack(mix))
    return out

def main():
    with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
     handle.write(REFERENCE_SOURCE);handle.flush()
     root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
     specials=special_cases()
     for index in range(40):
      if index==0: content=SAMPLE_IN
      elif index>=40-len(specials): content=specials[index-(40-len(specials))]
      else:
       for attempt in range(100):
        content=g23007(random.Random(23007+index+attempt*1000))
        if content not in seen: break
       else: raise AssertionError("insufficient diversity")
      assert valid(content) and (index==0 or content not in seen), index
      seen.append(content)
      result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
      (root/f"{index}.in").write_text(content,encoding="utf-8")
      (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

if __name__ == "__main__":
    main()
