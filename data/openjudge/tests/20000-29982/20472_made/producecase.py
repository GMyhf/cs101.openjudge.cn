import subprocess, tempfile
from pathlib import Path
CASES=['GGLLGG\n', 'GRRRRRGLGRLLGR\n', 'LGRGL\n', 'RGRGRLLRLGRGLLLRL\n', 'GRGGG\n', 'LLRRRGGGGLRRG\n', 'LRLRG\n', 'RGLGLLR\n', 'LGGG\n', 'LGRG\n', 'R\n', 'GR\n', 'LLGRGGRRGLLRGRRRGL\n', 'LGRRLLRGLRR\n', 'RRRRLLGL\n', 'RGRLGLLLRGGLRR\n', 'RRLLGGLRLRGRGGGGLGR\n', 'GLRRRGGLL\n', 'RLRGLLL\n', 'RGLLRRGLRL\n']
SOURCE="def is_robot_making_loop(commands):\n    # 初始位置和方向\n    x, y = 0, 0\n    direction = 'N'\n\n    # 方向变换的规则，用字典表示\n    left_turns = {'N': 'W', 'W': 'S', 'S': 'E', 'E': 'N'}\n    right_turns = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}\n\n    # 模拟机器人的移动\n    for command in commands:\n        if command == 'G':\n            if direction == 'N':\n                y += 1\n            elif direction == 'S':\n                y -= 1\n            elif direction == 'E':\n                x += 1\n            elif direction == 'W':\n                x -= 1\n        elif command == 'L':\n            direction = left_turns[direction]\n        elif command == 'R':\n            direction = right_turns[direction]\n\n    # 如果机器人回到原点，或者不是面向北方（说明它会改变方向然后可能回到原点）\n    return (x == 0 and y == 0) or direction != 'N'\n\n# 读取输入并输出结果\ncommands = input().strip()\nprint(1 if is_robot_making_loop(commands) else 0)\n\n"
with tempfile.NamedTemporaryFile('w',suffix='.py') as f:
 f.write(SOURCE); f.flush()
 root=Path(__file__).parent/'data'
 for i,c in enumerate(CASES):
  o=subprocess.run(['python3',f.name],input=c,text=True,capture_output=True,check=True).stdout
  (root/f'{i}.in').write_text(c); (root/f'{i}.out').write_text(o)
