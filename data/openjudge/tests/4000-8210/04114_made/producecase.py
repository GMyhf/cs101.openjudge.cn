import random,subprocess
from pathlib import Path
I='3\n2\n1.0 2.0 3.0 4.0\n4.0 5.0 6.0 7.0\n3\n0.0 0.0 0.0 1.0\n0.0 1.0 0.0 2.0\n1.0 1.0 2.0 1.0\n3\n0.0 0.0 0.0 1.0\n0.0 2.0 0.0 3.0\n1.0 1.0 2.0 1.0\n'
def g4114(r):
 if r.random()<.5:
  return "1\n3\n"+"\n".join(f"{x} 0 {x+r.randint(1,8)} 0" for x in r.sample(range(-100,101),3))+"\n"
 b=r.randint(-100,100);return f"1\n3\n{b} {b} {b} {b+1}\n{b} {b+2} {b} {b+3}\n{b+1} {b+1} {b+2} {b+1}\n"

root=Path(__file__).parent; binary=root/"reference"
subprocess.run(["g++","-std=c++17","-O2",str(root/"samplecode.cpp"),"-o",str(binary)],check=True)
for i in range(21):
 c=I if i==0 else g4114(random.Random(4114+i));p=subprocess.run([str(binary)],input=c,text=True,capture_output=True,check=True);(root/"data"/f"{i}.in").write_text(c);(root/"data"/f"{i}.out").write_text(p.stdout)
binary.unlink()
