import random
REFERENCE='# External reference: /practice/31002/statistics/\n# Accepted submission: 52760512\n# Source: http://cs101.openjudge.cn/practice/solution/52760512/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\n\ndef find_treasure():\n    # 读取输入\n    try:\n        map_str = sys.stdin.readline().strip()\n        treasure = sys.stdin.readline().strip()\n    except Exception:\n        return\n\n    # 获取字符串长度\n    map_len = len(map_str)\n    treasure_len = len(treasure)\n\n    # 存储所有找到的起始索引\n    indices = []\n\n    # 只有当地图长度不小于宝藏长度时才进行匹配\n    if map_len >= treasure_len and treasure_len > 0:\n        for i in range(map_len - treasure_len + 1):\n            # 截取等长子串并对比\n            if map_str[i : i + treasure_len] == treasure:\n                indices.append(i)\n\n    # 输出结果\n    print(treasure)\n    if indices:\n        print(" ".join(map(str, indices)))\n    else:\n        print("NoTreasure")\n\n\nif __name__ == "__main__":\n    find_treasure()'
SAMPLE='abababa\naba\n'
GENERATOR_NAME='g31002'
CPP=False
def g31002(r):
    s_len=r.randint(8,100); s="".join(r.choice("abcde") for _ in range(s_len)); t="".join(r.choice("abcde") for _ in range(r.randint(1,min(8,s_len))))
    return f"{s}\n{t}\n"

def valid(text):
    """题面契约：两行；地图串长度 ≤200，标记串长度 ≤10；格子为非空白字符。"""
    if not text.endswith('\n'): return False
    lines=text[:-1].split('\n')
    if len(lines)!=2: return False
    m,t=lines
    if not (1<=len(m)<=200 and 1<=len(t)<=10): return False
    return all(c.isprintable() and not c.isspace() for c in m+t)

def extra_cases():
    """补充：满长度 200 / 标记长度 10、大量重叠命中、最短串、整串即宝藏、末尾命中、满规模无宝藏。"""
    r=random.Random(310020)
    out=[]
    out.append('a'*200+'\n'+'a'*10+'\n')                       # 191 处重叠命中
    out.append('ab'*100+'\n'+'ababababab'+'\n')                # 周期串重叠
    out.append('a\n'+'a\n')                                     # 最小规模
    out.append('b\n'+'a\n')                                     # 最小规模无宝藏
    out.append('abcdefghij\n'+'abcdefghij\n')                   # 整串即宝藏
    out.append('x'*190+'abcdefghij\n'+'abcdefghij\n')           # 只在末尾命中
    out.append('a'*199+'b\n'+'a'*9+'c\n')                       # 满规模几乎匹配但无宝藏
    s=''.join(r.choice('ab') for _ in range(200)); out.append(s+'\n'+'aba\n')
    s=''.join(r.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(200)); out.append(s+'\n'+s[57:67]+'\n')
    out.append('aaaaaaaaab'*20+'\n'+'aab\n')
    return out

from pathlib import Path
import subprocess, sys, tempfile
def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/('main.cpp' if CPP else 'main.py'); p.write_text(REFERENCE)
        if CPP:
            exe=Path(d)/'main'; c=subprocess.run(['g++','-O2','-std=c++17',str(p),'-o',str(exe)],capture_output=True,text=True,timeout=30)
            if c.returncode: raise SystemExit(c.stderr)
            cmd=[str(exe)]
        else: cmd=[sys.executable,str(p)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=120)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    if GENERATOR_NAME == 'g30216':
        cases=[SAMPLE]+[f'{n}\n' for n in range(1,11)]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,11)]
    else:
        cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1, 30)]+extra_cases()
    for i,c in enumerate(cases): (data/f'{i}.in').write_text(c); (data/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
