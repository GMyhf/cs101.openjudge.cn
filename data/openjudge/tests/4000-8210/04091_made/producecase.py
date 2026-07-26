import random,subprocess
from pathlib import Path
I='3 2\n1 1\n1 3\n3 4\n2\n2 3\n2\n2 3\n1\n'
def g4091(r):
 n,k=r.randint(3,10),r.randint(1,3);p=[]
 while len(p)<n:
  x=tuple(r.randint(-9,9) for _ in range(k))
  if x not in p:p.append(x)
 q=r.randint(1,3);s=f"{n} {k}\n"+"\n".join(" ".join(map(str,x)) for x in p)+f"\n{q}\n"
 for _ in range(q):s+=" ".join(["-20"]*k)+f"\n{r.randint(1,min(3,n))}\n"
 return s

root=Path(__file__).parent; binary=root/"reference"
subprocess.run(["g++","-std=c++17","-O2",str(root/"samplecode.cpp"),"-o",str(binary)],check=True)
for i in range(21):
 c=I if i==0 else g4091(random.Random(4091+i));p=subprocess.run([str(binary)],input=c,text=True,capture_output=True,check=True);(root/"data"/f"{i}.in").write_text(c);(root/"data"/f"{i}.out").write_text(p.stdout)
binary.unlink()
