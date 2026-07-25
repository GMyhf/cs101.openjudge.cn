# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
def evaluate_expression(expression):
    # Replace logical operators with Python equivalents
    expression = expression.replace("not", "not ").replace("and", " and ").replace("or", " or ")
    # Evaluate the expression
    return int(eval(expression))

# 读取输入并处理
expression = input()
print(evaluate_expression(expression))
