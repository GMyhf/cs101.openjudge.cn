import random,subprocess
from pathlib import Path
I='8 1 3 5 6 8 10 12 30\n3 1 3 7\n'
def g4088(r): A=sorted(r.sample(range(100),r.randint(6,20)));B=sorted(r.sample(range(100),r.randint(1,8)));return f"{len(A)} "+" ".join(map(str,A))+f"\n{len(B)} "+" ".join(map(str,B))+"\n"

root=Path(__file__).parent; binary=root/"reference"
subprocess.run(["g++","-std=c++17","-O2",str(root/"samplecode.cpp"),"-o",str(binary)],check=True)
for i in range(21):
 c=I if i==0 else g4088(random.Random(4088+i));p=subprocess.run([str(binary)],input=c,text=True,capture_output=True,check=True);(root/"data"/f"{i}.in").write_text(c);(root/"data"/f"{i}.out").write_text(p.stdout)
binary.unlink()
