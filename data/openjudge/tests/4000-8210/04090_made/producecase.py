import random,subprocess
from pathlib import Path
I='5\n1 \n2 \n3 \n4 \n5\n2\nADD 2 4 1\nMIN 4 5\n'
def g4090(r):
 v=[r.randint(-9,9) for _ in range(r.randint(3,10))];o=[]
 initial=v[:]
 for _ in range(12):
  z=r.choice(["ADD","REVERSE","REVOLVE","MIN","INSERT","DELETE"])
  if z=="DELETE" and len(v)>1:x=r.randint(1,len(v));v.pop(x-1);o.append(f"DELETE {x}")
  elif z=="INSERT":x=r.randint(1,len(v));d=r.randint(-9,9);v.insert(x,d);o.append(f"INSERT {x} {d}")
  else:
   x=r.randint(1,len(v));y=r.randint(x,len(v))
   if z=="ADD":d=r.randint(-3,3);v[x-1:y]=[q+d for q in v[x-1:y]];o.append(f"ADD {x} {y} {d}")
   elif z=="REVERSE":v[x-1:y]=v[x-1:y][::-1];o.append(f"REVERSE {x} {y}")
   elif z=="REVOLVE":d=r.randint(0,8);w=v[x-1:y];d%=len(w);v[x-1:y]=w[-d:]+w[:-d] if d else w;o.append(f"REVOLVE {x} {y} {d}")
   else:o.append(f"MIN {x} {y}")
 return f"{len(initial)}\n"+"\n".join(map(str,initial))+f"\n{len(o)}\n"+"\n".join(o)+"\n"

root=Path(__file__).parent; binary=root/"reference"
subprocess.run(["g++","-std=c++17","-O2",str(root/"samplecode.cpp"),"-o",str(binary)],check=True)
for i in range(21):
 c=I if i==0 else g4090(random.Random(4090+i));p=subprocess.run([str(binary)],input=c,text=True,capture_output=True,check=True);(root/"data"/f"{i}.in").write_text(c);(root/"data"/f"{i}.out").write_text(p.stdout)
binary.unlink()
