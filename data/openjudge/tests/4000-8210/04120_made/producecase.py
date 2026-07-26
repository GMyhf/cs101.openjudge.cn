import random,subprocess
from pathlib import Path
I='5 18\n1 2 3 5 10\n'
def g4120(r):c=sorted(r.sample(range(1,20),8));return f"8 {c[0]+c[3]}\n"+" ".join(map(str,c))+"\n"

root=Path(__file__).parent; binary=root/"reference"
subprocess.run(["g++","-std=c++17","-O2",str(root/"samplecode.cpp"),"-o",str(binary)],check=True)
for i in range(21):
 c=I if i==0 else g4120(random.Random(4120+i));p=subprocess.run([str(binary)],input=c,text=True,capture_output=True,check=True);(root/"data"/f"{i}.in").write_text(c);(root/"data"/f"{i}.out").write_text(p.stdout)
binary.unlink()
