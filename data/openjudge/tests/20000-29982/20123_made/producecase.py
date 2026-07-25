import subprocess, tempfile
from pathlib import Path
CASES=['123364315\n', '64579709\n', '11027971\n', '84255022\n', '11449373\n', '13171629\n', '30675265\n', '34557844\n', '14241670\n', '16598002\n', '35008987\n', '55983744\n', '27636040\n', '39144591\n', '945113\n', '58971043\n', '18273175\n', '99849519\n', '28264649\n', '22660765\n']
SOURCE="#20123:7-友好数，http://cs101.openjudge.cn/practice/20123/\n#\n# 陈威宇：>=7位就一定YES了，因为所有后缀%7有两个相等的（抽屉原理），\n# 取这两个后缀里长的那个去掉短的那个即可？\n'''\n通过递归地尝试不同的子串来寻找符合条件的解.\n`dfs(n, i)` 函数是进行深度优先搜索的核心部分。它接受两个参数：`n`代表当前搜索到的子串，\n`i`代表当前处理到的位置索引。在函数内部，通过不断拼接字符来生成不同的子串，\n然后检查是否满足能够被7整除的条件。\n\n'''\ndef dfs(n, i):\n    global bo\n    if len(n) > 0 and int(n) % 7 == 0:\n        bo = True\n    if bo:\n        return\n    if i >= l:\n        return\n    dfs(n, i+1)\n    dfs(n+s[i], i+1)\n\n\ns = input()\nl = len(s)\nif l >= 7:\n    print('YES')\n    exit()\nbo = False\ndfs('', 0)\nif bo:\n    print('YES')\nelse:\n    print('NO')\n\n"
with tempfile.NamedTemporaryFile('w',suffix='.py') as f:
 f.write(SOURCE); f.flush()
 root=Path(__file__).parent/'data'
 for i,c in enumerate(CASES):
  o=subprocess.run(['python3',f.name],input=c,text=True,capture_output=True,check=True).stdout
  (root/f'{i}.in').write_text(c); (root/f'{i}.out').write_text(o)
