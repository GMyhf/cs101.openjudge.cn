# Source: /home/ubuntu/hongfei/2024spring-cs201/2024spring_dsa_problems.md
"""
GitHub Copilot Chat:
This solution works by recursively splitting the string into four parts and 
checking if each part is a valid coordinate. 
The safe_locations function takes the remaining string, the current parts, 
and the current depth as arguments. 
If the depth is 4, it checks if the string is empty and if all parts are 
valid coordinates. If so, it returns 1, otherwise it returns 0. 
If the depth is less than 4, it tries to split the string at every possible 
position and recursively calls itself with the new parts and increased depth. 
"""


def safe_locations(s, parts, depth=0):
    if depth == 4:
        if not s and all(0 <= int(part) <= 500 and 
                (part == '0' or not part.startswith('0')) for part in parts):
            return 1
        return 0
    return sum(safe_locations(s[i:], parts + [s[:i]], depth + 1) 
               for i in range(1, len(s) + 1))


s = input().strip()
print(safe_locations(s, []))

