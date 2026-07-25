import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'class stack():\n    def __init__(self):\n        self.val=[]\n    def isempty(self):\n        return len(self.val)==0\n    def push(self,item):\n        self.val.append(item)\n    def top(self):\n        return self.val[-1]\n    def pop(self):\n        del self.val[-1]\n\ndef operatorcheck():\n    for i in range(len(exp)):\n        if exp[i] not in ch:\n            return 0\n    return 1\n\ndef bracketcheck():\n    bracket=stack()\n    for i in range(len(exp)):\n        if exp[i]==\'(\':\n            bracket.push(\'(\')\n        if exp[i]==\')\':\n            if bracket.isempty():\n                return 0\n            else:\n                bracket.pop()\n    if bracket.isempty():\n        return 1\n    else:\n        return 0\n\ndef onlybracket():\n    for i in range(len(exp)):\n        if exp[i]!=\'(\' and exp[i]!=\')\':\n            return 0\n    return 1\n            \ndef cut():\n    i=0\n    while i<=len(exp)-1:\n        if exp[i]==\'*\' or exp[i]==\'/\' or exp[i]==\'(\' or exp[i]==\')\':\n            expression.append(exp[i])\n            i+=1\n            continue\n        if exp[i]==\'+\' or exp[i]==\'-\':\n            if i==0 or exp[i-1] not in ch[5:]:\n                temp=\'\'+exp[i]\n                i+=1\n                while i<=len(exp)-1 and exp[i] in ch[6:]:\n                    temp=temp+exp[i]\n                    i+=1\n                expression.append(float(temp))\n                continue\n            else:\n                expression.append(exp[i])\n                i+=1\n                continue\n        if exp[i] in ch[6:]:\n            temp=\'\'\n            while i<=len(exp)-1 and exp[i] in ch[6:]:\n                temp=temp+exp[i]\n                i+=1\n            expression.append(float(temp))\n            continue\ndef value(s,x,y):\n    if s==\'+\':\n        return x+y\n    if s==\'*\':\n        return x*y\n    if s==\'-\':\n        return x-y\n    if s==\'/\':\n        return x/y\n\ndef calc():\n    operator=stack()\n    operand=stack()\n    for i in range(len(expression)):\n        if expression[i] not in ch[0:6]:\n            operand.push(expression[i])\n        elif expression[i]==\'(\':\n            operator.push(\'(\')\n        elif expression[i]==\')\':\n            while operator.top()!=\'(\':\n                b=operand.top()\n                operand.pop()\n                a=operand.top()\n                operand.pop()\n                operand.push(value(operator.top(),a,b))\n                operator.pop()\n            operator.pop()\n        elif expression[i] in ch[0:4]:\n            while not operator.isempty() and prior[operator.top()]>=prior[expression[i]]:\n                b=operand.top()\n                operand.pop()\n                a=operand.top()\n                operand.pop()\n                operand.push(value(operator.top(),a,b))\n                operator.pop()\n            operator.push(expression[i])\n    while not operator.isempty():\n        b=operand.top()\n        operand.pop()\n        a=operand.top()\n        operand.pop()\n        operand.push(value(operator.top(),a,b))\n        operator.pop()\n    print(\'{:.3f}\'.format(operand.top()))\n                \n        \nch=[\'+\',\'-\',\'*\',\'/\',\'(\',\')\',\'.\',\'0\',\'1\',\'2\',\'3\',\'4\',\'5\',\'6\',\'7\',\'8\',\'9\']\nprior={\'*\':3,\'/\':3,\'+\':2,\'-\':2,\'(\':1}\nwhile True:\n    s=list(map(str,input().split()))\n    if s==["quit"]:\n        break\n    if len(s)==0:\n        print("No expression.")\n        continue\n    exp=""\n    for i in range(len(s)):\n        exp=exp+s[i]\n    if operatorcheck()==False:\n        print("Unknown operator.")\n        continue\n    if bracketcheck()==False:\n        print("Unmatched bracket.")\n        continue\n    if onlybracket()==True:\n        print("No expression.")\n        continue\n    expression=[]\n    try:\n        cut()\n        calc()\n    except:\n        print("Not implemented.")\n        continue\n'
SAMPLE_IN = '(((-10.1 + 4.3) * 8.5) - 6) / 4   \n((1+     2)*3\n      (1+1+1.   1) /    3\n\n1 ++ 1\n1 +++ 1\n1^2\nquit\n'
SAMPLE_OUT = '-13.825\nUnmatched bracket.\n1.033\nNo expression.\n2.000\nNot implemented.\nUnknown operator.\n'
def generate_case(r):
    atoms = [str(r.randint(0, 99)), f"{r.randint(1, 99)}.{r.randint(0, 9)}"]
    denominator = atoms[0] if atoms[0] != "0" else "1"
    lines = [f"{atoms[0]} + {atoms[1]}", f"({atoms[0]} * {atoms[1]})", f"{atoms[1]} / {denominator}"]
    if r.random() < .5:
        lines.append("1 ++ 1")
    if r.random() < .5:
        lines.append("1^2")
    assert lines and all(line != "quit" for line in lines)
    return "\n".join(lines + ["quit"]) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(23451 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
