import subprocess, tempfile
from pathlib import Path
CASES=['( not ( True or False ) ) and ( False or True and True )\n', '( False and False ) and ( not False or True )\n', '( False and False ) and ( not True or False )\n', '( False or False ) or ( not False or True )\n', '( True and True ) or ( not True or True )\n', '( False and False ) and ( not False or False )\n', '( False and True ) and ( not True or False )\n', '( False or True ) and ( not True or False )\n', '( False or False ) and ( not True or True )\n', '( True or False ) and ( not False or True )\n', '( True or True ) and ( not True or True )\n', '( False and True ) or ( not True or False )\n', '( True or False ) or ( not False or False )\n', '( True and False ) or ( not False or False )\n', '( False or True ) and ( not False or False )\n', '( False or True ) and ( not True or True )\n', '( True and False ) or ( not True or False )\n', '( True and False ) and ( not False or False )\n', '( True or False ) or ( not True or False )\n', '( False or True ) or ( not False or False )\n']
SOURCE='def evaluate_expression(expression):\n    # Replace logical operators with Python equivalents\n    expression = expression.replace("not", "not ").replace("and", " and ").replace("or", " or ")\n    # Evaluate the expression\n    return int(eval(expression))\n\n# 读取输入并处理\nexpression = input()\nprint(evaluate_expression(expression))\n'
with tempfile.NamedTemporaryFile('w',suffix='.py') as f:
 f.write(SOURCE); f.flush()
 root=Path(__file__).parent/'data'
 for i,c in enumerate(CASES):
  o=subprocess.run(['python3',f.name],input=c,text=True,capture_output=True,check=True).stdout
  (root/f'{i}.in').write_text(c); (root/f'{i}.out').write_text(o)
