import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import sys\n\ndef main():\n    # 读取所有输入\n    input_data = sys.stdin.read().splitlines()\n    if not input_data:\n        return\n    \n    # 第一行为提交记录数 M\n    m = int(input_data[0].strip())\n    \n    teams = {}\n    \n    for i in range(1, m + 1):\n        if i >= len(input_data):\n            break\n        line = input_data[i].strip()\n        if not line:\n            continue\n        \n        # 解析每行提交数据，去除两端空格\n        parts = line.split(\',\')\n        if len(parts) < 3:\n            continue\n        team_name = parts[0].strip()\n        problem = parts[1].strip()\n        result = parts[2].strip()\n        \n        # 初始化队伍数据\n        if team_name not in teams:\n            teams[team_name] = {\n                \'solved\': set(),\n                \'subs\': 0\n            }\n        \n        # 记录提交次数\n        teams[team_name][\'subs\'] += 1\n        \n        # 如果通过，则加入已解决题目集合\n        if result == \'yes\':\n            teams[team_name][\'solved\'].add(problem)\n            \n    # 排序规则：\n    # 1. 做对题目数降序：-len(x[1][\'solved\'])\n    # 2. 总提交次数升序：x[1][\'subs\']\n    # 3. 队伍名称字典序升序：x[0]\n    sorted_teams = sorted(\n        teams.items(),\n        key=lambda x: (-len(x[1][\'solved\']), x[1][\'subs\'], x[0])\n    )\n    \n    # 输出前 12 名（若不足 12 名，则输出全部）\n    limit = min(12, len(sorted_teams))\n    for rank in range(1, limit + 1):\n        team_name, data = sorted_teams[rank - 1]\n        solved_count = len(data[\'solved\'])\n        subs_count = data[\'subs\']\n        print(f"{rank} {team_name} {solved_count} {subs_count}")\n\nif __name__ == \'__main__\':\n    main()\n'
SAMPLE_IN = '9\nPeking University,A,no\nMassachusetts Institute of Technology,A,yes\nNational Research University Higher School of Economics,A,no\nUniversity of Oxford,A,yes\nPeking University,B,yes\nPeking University,A,yes\nUniversity of Oxford,C,no\nUniversity of Oxford,C,no\nNational Research University Higher School of Economics,C,yes\n'
SAMPLE_OUT = '1 Peking University 2 3\n2 Massachusetts Institute of Technology 1 1\n3 National Research University Higher School of Economics 1 2\n4 University of Oxford 1 3\n'
def generate_case(r):
    schools = ["Peking University", "University of Oxford", "MIT", "PKU"]
    rows = [f"{r.choice(schools)},{r.choice('ABC')},{r.choice(['yes', 'no'])}" for _ in range(r.randint(4, 20))]
    return str(len(rows)) + "\n" + "\n".join(rows) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(28127 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
