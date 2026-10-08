import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\ndef pos(r,c):\n t,l,b,rr=0,0,r-1,c-1\n while t<=b and l<=rr:\n  for j in range(l,rr+1): yield t,j\n  t+=1\n  for i in range(t,b+1): yield i,rr\n  rr-=1\n  if t<=b:\n   for j in range(rr,l-1,-1): yield b,j\n   b-=1\n  if l<=rr:\n   for i in range(b,t-1,-1): yield i,l\n   l+=1\nr,c,msg=sys.stdin.read().rstrip("\\n").split(" ",2); r,c=int(r),int(c)\nbits="".join(format(0 if x==" " else ord(x)-64,"05b") for x in msg).ljust(r*c,"0")\ng=[["0"]*c for _ in range(r)]\nfor (i,j),x in zip(pos(r,c),bits): g[i][j]=x\nprint("".join("".join(x) for x in g))'
SAMPLE_IN='4 4 ACM\n'
import re
def valid(text):
    """题面：一行 "R C 字符串"，1<=R<=20，1<=C<=20，字符串只含大写字母和空格，长度<=R*C/5；
    R 与 C、C 与字符串之间各用单个空格隔开。"""
    m = re.fullmatch(r'([1-9]\d*) ([1-9]\d*) ([A-Z ]*)\n', text)
    if not m:
        return False
    R, C, msg = int(m.group(1)), int(m.group(2)), m.group(3)
    return 1 <= R <= 20 and 1 <= C <= 20 and 5 * len(msg) <= R * C

UP = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def g3421(r, index):
    fixed = {1: (1, 1), 2: (20, 20), 3: (20, 20), 4: (1, 20), 5: (20, 1), 6: (19, 20), 7: (20, 19),
             8: (19, 17), 9: (2, 20), 10: (20, 2), 11: (3, 7), 12: (5, 1), 13: (1, 5), 14: (17, 17), 15: (2, 2)}
    rows, cols = fixed.get(index) or (r.randint(1, 20), r.randint(1, 20))
    L = rows * cols // 5
    if index in (2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14) or index % 4 == 0: k = L      # 写满到上限
    elif index == 3: k = r.randint(L // 2, L)
    else: k = r.randint(0, L)
    if index == 2: body = "Z" * k                     # 全 11010
    elif index == 3: body = "".join(r.choice(UP) for _ in range(k))
    else: body = "".join(r.choice(UP + "   ") for _ in range(k))
    # 首尾不放空格（避免与行尾空白处理纠缠）；内部空格照常出现
    body = body.strip(" ")
    if index == 16 and L >= 3: body = "A" + " " * (L - 2) + "Z"
    return f"{rows} {cols} {body}\n"

def main():
 with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
  handle.write(REFERENCE_SOURCE);handle.flush()
  root=Path(__file__).parent/"data";root.mkdir(exist_ok=True);seen=[SAMPLE_IN]
  for index in range(40):
   if index==0:content=SAMPLE_IN
   else:
    for attempt in range(100):
     content=g3421(random.Random(3421+index+attempt*1000),index)
     if content not in seen:break
    else:raise AssertionError("insufficient diversity")
   assert valid(content),index
   seen.append(content)
   result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
   (root/f"{index}.in").write_text(content,encoding="utf-8")
   (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")
if __name__=="__main__":main()
