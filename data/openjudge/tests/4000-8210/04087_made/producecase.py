import random,subprocess
from pathlib import Path
I='10 5\n1  3  8 20 2 \n9 10 12  8 9\n'
def g4087(r): n=r.randint(10,60);return f"{n} {r.randint(1,n)}\n"+" ".join(str(r.randint(1,10**6)) for _ in range(n))+"\n"

root=Path(__file__).parent; binary=root/"reference"
subprocess.run(["g++","-std=c++17","-O2",str(root/"samplecode.cpp"),"-o",str(binary)],check=True)
for i in range(21):
 c=I if i==0 else g4087(random.Random(4087+i));p=subprocess.run([str(binary)],input=c,text=True,capture_output=True,check=True);(root/"data"/f"{i}.in").write_text(c);(root/"data"/f"{i}.out").write_text(p.stdout)
binary.unlink()
