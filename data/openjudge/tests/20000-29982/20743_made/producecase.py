import subprocess, tempfile
from pathlib import Path
CASES=['(eg(en(duj))po)\n', '(cddaaccddbccd)dd\n', '(aad)dccc\n', '(dabacdadccccadacc)\n', '(b)a\n', '(adcbaaadcabbbbcdcda)acca\n', '(cbcacdcd)ac\n', '(ccddaddccdcbb)aaa\n', '(bcdacaadddaaad)a\n', '(dccbadbddcbbabacabbc)abbbc\n', '(accdbdabaadcabcbd)aac\n', '(cabbbbaabdbadbbacbba)ccbb\n', '(ac)aabcd\n', '(cdbaadbbaabdc)\n', '(dddcdc)cddbb\n', '(aadacbd)cbcad\n', '(cbdbcccdcaabcbbbcd)bcb\n', '(ddabaaccbddcbddcd)bdb\n', '(bdccbbc)dbad\n', '(bdbb)d\n']
SOURCE="def reverse_parentheses(s):\n    stack = []\n    for char in s:\n        if char == ')':\n            temp = []\n            while stack and stack[-1] != '(':\n                temp.append(stack.pop())\n            # remove the opening parenthesis\n            if stack:\n                stack.pop()\n            # add the reversed characters back to the stack\n            stack.extend(temp)\n        else:\n            stack.append(char)\n    return ''.join(stack)\n\n# 读取输入并处理\ns = input().strip()\nprint(reverse_parentheses(s))\n"
with tempfile.NamedTemporaryFile('w',suffix='.py') as f:
 f.write(SOURCE); f.flush()
 root=Path(__file__).parent/'data'
 for i,c in enumerate(CASES):
  o=subprocess.run(['python3',f.name],input=c,text=True,capture_output=True,check=True).stdout
  (root/f'{i}.in').write_text(c); (root/f'{i}.out').write_text(o)
