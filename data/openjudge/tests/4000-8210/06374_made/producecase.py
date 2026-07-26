import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = 'n = int(input())\np = input()\n\nline_char_num = 0\nword_list = p.split(" ")\noutput = [[]]\nfor word in word_list:\n    if len(word) + line_char_num > 80:\n        output.append([])\n        output[-1].append(word)\n        line_char_num = len(word)+1\n    else:\n        output[-1].append(word)\n        line_char_num += len(word)+1\n\nfor line in output:\n    print(" ".join(line))\n\n'
SAMPLE = '84\nOne sweltering day, I was scooping ice cream into cones and told my four children they could "buy" a cone from me for a hug. Almost immediately, the kids lined up to make their purchases. The three youngest each gave me a quick hug, grabbed their cones and raced back outside. But when my teenage son at the end of the line finally got his turn to "buy" his ice cream, he gave me two hugs. "Keep the changes," he said with a smile.\n'
GENERATOR_NAME = 'g6374'
def g6374(r):
    z=["".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(r.randint(1,15))) for _ in range(r.randint(6,40))]
    return f"{len(z)}\n{' '.join(z)}\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"
        p.write_text(REFERENCE, encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text, encoding="utf-8")
        (data/f"{i}.out").write_text(run(text), encoding="utf-8")
if __name__=="__main__": main()
