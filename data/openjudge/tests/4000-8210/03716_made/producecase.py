import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\nout=[]\nfor line in sys.stdin.read().splitlines():\n    parts=line.split()\n    if parts and not parts[0].startswith("#") and parts[0]!="":\n        out.append(" ".join(parts[1:]))\nprint(len(out)); print("\\n".join(out))'
SAMPLE_IN='# Start of my config file\n\n# time config\ntimevar TIMESLOT  120\ntimevar TIMEOUT 600\n\n# port config\nportvar HTTP_PORTS [80,8000,8080,8888]\n\n# End of the config file\n'
def g3716(r):
    lines=["# generated config"]
    for i in range(r.randint(1, 8)):
        lines.append(r.choice(["timevar","portvar","pathvar"])+" KEY"+str(i)+" "+r.choice(["0","120","[1,2,3]","/tmp/x"]))
        if r.random()<.35: lines.append("")
        if r.random()<.25: lines.append("# note")
    lines.append("# End of the config file")
    return "\n".join(lines)+"\n"

with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0: content=SAMPLE_IN
  else:
   for attempt_no in range(100):
    content=g3716(random.Random(3716+index+attempt_no*1000))
    if content not in seen: break
   else: raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{index}.in").write_text(content,encoding="utf-8")
  (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")
