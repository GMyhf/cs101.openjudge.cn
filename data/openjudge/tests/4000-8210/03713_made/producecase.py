import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\nsmall={"zero":0,"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10,"eleven":11,"twelve":12,"thirteen":13,"fourteen":14,"fifteen":15,"sixteen":16,"seventeen":17,"eighteen":18,"nineteen":19}\ntens={"twenty":20,"thirty":30,"forty":40,"fifty":50,"sixty":60,"seventy":70,"eighty":80,"ninety":90}\nfor line in sys.stdin:\n    cur=total=0; neg=False\n    for w in line.split():\n        if w=="negative": neg=True\n        elif w in small: cur+=small[w]\n        elif w in tens: cur+=tens[w]\n        elif w=="hundred": cur*=100\n        elif w=="thousand": total+=cur*1000; cur=0\n        elif w=="million": total+=cur*1000000; cur=0\n    value=total+cur\n    print(-value if neg else value)'
SAMPLE_IN='six\nnegative seven hundred twenty nine\none million one hundred one\neight hundred fourteen thousand twenty two\n'
def g3713(r):
    phrases=[
        "zero","one","twelve","nineteen","twenty one","forty two",
        "one hundred","three hundred five","nine hundred ninety nine",
        "one thousand two","twelve thousand three hundred forty five",
        "one million one hundred one","negative seven hundred twenty nine",
        "negative one million two hundred thirty four",
        "eight hundred fourteen thousand twenty two",
        "six hundred thousand","seventy thousand nineteen",
        "four million five hundred",
        "negative ninety nine million nine hundred ninety nine thousand nine hundred ninety nine",
        "two hundred thirty four million five hundred sixty seven thousand eight hundred ninety",
        "negative one thousand one",
        "fifteen million sixteen thousand seventeen"
    ]
    return "\n".join(r.sample(phrases, r.randint(1, 5)))+"\n"

with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0: content=SAMPLE_IN
  else:
   for attempt_no in range(100):
    content=g3713(random.Random(3713+index+attempt_no*1000))
    if content not in seen: break
   else: raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{index}.in").write_text(content,encoding="utf-8")
  (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")
