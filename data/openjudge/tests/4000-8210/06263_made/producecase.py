import random, subprocess, tempfile
from pathlib import Path
SAMPLE_IN = '( V | V ) & F & ( F| V)\n!V | V & V & !F & (F | V ) & (!F | F | !V & V)\n(F&F|V|!V&!F&!(F|F&V))\n'
SAMPLE_OUT = 'F\nV\nV\n'
CASES = ['( V | V ) & F & ( F| V)\n!V | V & V & !F & (F | V ) & (!F | F | !V & V)\n(F&F|V|!V&!F&!(F|F&V))\n', '((V&F)&(F&!((V&F)|!(F|F))))\n(!(!(V|!(F|F))|(F&!((V&F)|!(F|F))))&!(V|!(F|F)))\n(F&!((V&F)|!(F|F)))\n', '(((F&F)&(V&V))&((F&F)&(V&V)))\n', '(F&F)\n((F&F)&(F&F))\n(((F&F)&(F&F))&((F&F)&(F&F)))\n', '!(((F&F)&F)|!(((F&F)&F)|(F&F)))\n', '!(((F&F)&F)|V)\n', '!((!((F&V)|F)&(F&V))|((V&F)&V))\n', '((F&F)&(!(V|(F&F))&!(F|F)))\n', '!(!((F&V)|(F&V))|((F&V)&!(V|F)))\n!(V|!((F&V)|(F&V)))\n!(((F&V)&!(V|F))|F)\n', '(!(F|(V&F))&(!(F|(V&F))&!(F|(V&F))))\n(((V&F)&F)&(!(F|(V&F))&(!(F|(V&F))&!(F|(V&F)))))\n((((V&F)&F)&(!(F|(V&F))&(!(F|(V&F))&!(F|(V&F)))))&((V&F)&F))\n', '(!(V|F)&!(F|!(V|F)))\n', '!(V|!((V&(V&F))|(V&F)))\n(!(V|!((V&(V&F))|(V&F)))&F)\n!((!(V|!((V&(V&F))|(V&F)))&F)|(!(V|!((V&(V&F))|(V&F)))&F))\n', '(F&(F&(V&F)))\n!(V|(V&V))\n(V&(V&V))\n', '!(!(!((V&V)|!((V&V)|(V&V)))|(F&F))|!(F|!((V&V)|(V&V))))\n', '((F&F)&V)\n(((F&F)&V)&((F&F)&V))\n', '!((!(!(F|V)|F)&((V&V)&V))|((V&V)&V))\n', '!(F|!((F&V)|!(!(F|(F&V))|(F&V))))\n!((F&V)|!(F|(F&V)))\n(!(!(F|(F&V))|(F&V))&!(F|!((F&V)|!(!(F|(F&V))|(F&V)))))\n', '(!(!(V|F)|!(V|F))&(!(F|V)&!(V|F)))\n', '(V&F)\n((V&F)&(V&F))\n!(((V&F)&(V&F))|((V&F)&(V&F)))\n', '(!((V&!(V|V))|F)&!(V|V))\n!(V|(V&!(V|V)))\n']
REFERENCE_SOURCE = '# 23n2300011119(武)\ndef ShuntingYard(l:list):\n    stack,output=[],[]\n    for i in l:\n        if i==" ":continue\n        if i in \'VF\':output.append(i)\n        elif i==\'(\':stack.append(i)\n        elif i in \'&|!\':\n            while True:\n                if i==\'!\':break\n                elif not stack:break\n                elif stack[-1]=="(":\n                    break\n                else:output.append(stack.pop())\n            stack.append(i)\n        elif i==\')\':\n            while stack[-1]!=\'(\':\n                output.append(stack.pop())\n            stack.pop()\n    if stack:output.extend(reversed(stack))\n    return output\n\ndef Bool_shift(a):\n    if a==\'V\':return True\n    elif a==\'F\':return False\n    elif a==True:return \'V\'\n    elif a==False:return \'F\'\n\ndef cal(a,operate,b=None):\n    if operate=="&":return Bool_shift(Bool_shift(a) and Bool_shift(b))\n    if operate=="|":return Bool_shift(Bool_shift(a) or Bool_shift(b))\n    if operate=="!":return Bool_shift(not Bool_shift(a))\n\ndef post_cal(l:list):\n    stack=[]\n    for i in l:\n        if i in \'VF\':stack.append(i)\n        elif i in "&|!":\n            if i=="!":\n                stack.append(cal(stack.pop(),\'!\'))\n            else:\n                a,b=stack.pop(),stack.pop()\n                stack.append(cal(a,i,b))\n    return stack[0]\n\nwhile True:\n    try:print(post_cal(ShuntingYard(list(input()))))\n    except EOFError:break\n'
assert CASES[0] == SAMPLE_IN
random.seed(6263)
def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=5, check=True)
    return result.stdout
assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split()
root = Path(__file__).parent / "data"
for index, content in enumerate(CASES):
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")
