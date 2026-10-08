import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import sys\n\ndef main():\n    # 读取所有输入\n    input_data = sys.stdin.read().splitlines()\n    if not input_data:\n        return\n    \n    # 第一行为提交记录数 M\n    m = int(input_data[0].strip())\n    \n    teams = {}\n    \n    for i in range(1, m + 1):\n        if i >= len(input_data):\n            break\n        line = input_data[i].strip()\n        if not line:\n            continue\n        \n        # 解析每行提交数据，去除两端空格\n        parts = line.split(\',\')\n        if len(parts) < 3:\n            continue\n        team_name = parts[0].strip()\n        problem = parts[1].strip()\n        result = parts[2].strip()\n        \n        # 初始化队伍数据\n        if team_name not in teams:\n            teams[team_name] = {\n                \'solved\': set(),\n                \'subs\': 0\n            }\n        \n        # 记录提交次数\n        teams[team_name][\'subs\'] += 1\n        \n        # 如果通过，则加入已解决题目集合\n        if result == \'yes\':\n            teams[team_name][\'solved\'].add(problem)\n            \n    # 排序规则：\n    # 1. 做对题目数降序：-len(x[1][\'solved\'])\n    # 2. 总提交次数升序：x[1][\'subs\']\n    # 3. 队伍名称字典序升序：x[0]\n    sorted_teams = sorted(\n        teams.items(),\n        key=lambda x: (-len(x[1][\'solved\']), x[1][\'subs\'], x[0])\n    )\n    \n    # 输出前 12 名（若不足 12 名，则输出全部）\n    limit = min(12, len(sorted_teams))\n    for rank in range(1, limit + 1):\n        team_name, data = sorted_teams[rank - 1]\n        solved_count = len(data[\'solved\'])\n        subs_count = data[\'subs\']\n        print(f"{rank} {team_name} {solved_count} {subs_count}")\n\nif __name__ == \'__main__\':\n    main()\n'
SAMPLE_IN = '9\nPeking University,A,no\nMassachusetts Institute of Technology,A,yes\nNational Research University Higher School of Economics,A,no\nUniversity of Oxford,A,yes\nPeking University,B,yes\nPeking University,A,yes\nUniversity of Oxford,C,no\nUniversity of Oxford,C,no\nNational Research University Higher School of Economics,C,yes\n'
SAMPLE_OUT = '1 Peking University 2 3\n2 Massachusetts Institute of Technology 1 1\n3 National Research University Higher School of Economics 1 2\n4 University of Oxford 1 3\n'
SAMPLE2_IN = '31\nUniversity of Waterloo,C,yes\nUniversity of Waterloo,C,yes\nUniversity of Waterloo,C,yes\nUniversity of Waterloo,C,yes\nUniversity of Waterloo,C,yes\nUniversity of Waterloo,D,yes\nUniversity of Waterloo,D,no\nUniversity of Waterloo,D,yes\nUniversity of Waterloo,X,no\nUniversity of Waterloo,G,no\nUniversity of Waterloo,P,no\nPeking University,A,no\nPeking University,B,no\nPeking University,Y,yes\nPeking University,Z,no\nPeking University,Y,no\nPeking University,Y,yes\nPeking University,Y,yes\nPeking University,Z,yes\nPeking University,A,yes\nUniversity of Warsaw,T,no\nUniversity of Warsaw,T,yes\nUniversity of Warsaw,F,no\nUniversity of Warsaw,F,no\nUniversity of Warsaw,F,no\nUniversity of Warsaw,F,no\nUniversity of Warsaw,F,no\nUniversity of Warsaw,F,yes\nUniversity of Warsaw,Q,no\nUniversity of Warsaw,F,no\nUniversity of Warsaw,B,no\n'
SAMPLE3_IN = '14\nTeamA,A,no\nTeamB,B,yes\nTeamC,C,no\nTeamD,D,yes\nTeamE,E,no\nTeamF,F,yes\nTeamG,G,no\nTeamH,H,yes\nTeamI,I,no\nTeamJ,J,yes\nTeamK,K,no\nTeamL,L,yes\nTeamM,M,no\nTeamN,N,yes\n'
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def valid(text):
    """题面：第一行 M (1<=M<=1000)；接下去 M 行“队名,题号,结果”，
    队名仅由大小写字母和空格组成，题号为 A-Z 之一，结果为 yes/no。"""
    import re
    if not text.endswith('\n') or '\r' in text:
        return False
    lines = text[:-1].split('\n')
    if not re.fullmatch(r'[1-9][0-9]*', lines[0]):
        return False
    m = int(lines[0])
    if not 1 <= m <= 1000 or len(lines) != m + 1:
        return False
    for line in lines[1:]:
        # 生成数据额外要求队名非空、首尾无空格、无连续空格，避免输出歧义
        if not re.fullmatch(r'[A-Za-z]+( [A-Za-z]+)*,[A-Z],(yes|no)', line):
            return False
    return True

def _name(r, style):
    if style == 0:
        return 'Team' + ''.join(r.choice(LETTERS) for _ in range(r.randint(1, 3)))
    words = ['Peking', 'University', 'of', 'Oxford', 'Tsinghua', 'Moscow', 'State', 'Institute',
             'Technology', 'Waterloo', 'Warsaw', 'Seoul', 'National', 'Tokyo', 'Harvard', 'Zhejiang']
    return ' '.join(r.choice(words) for _ in range(r.randint(1, 4)))

def generate_case(r, m, nteams, nprob, pyes, style):
    teams = set()
    while len(teams) < nteams:
        teams.add(_name(r, style))
    teams = sorted(teams)
    probs = LETTERS[:nprob]
    # 每支队伍至少出现一次，保证“恰好 nteams 支队伍”名副其实
    assert nteams <= m
    picks = teams + [r.choice(teams) for _ in range(m - nteams)]
    r.shuffle(picks)
    rows = [f"{t},{r.choice(probs)},{'yes' if r.random() < pyes else 'no'}" for t in picks]
    return str(m) + "\n" + "\n".join(rows) + "\n"

def tie_case(r):
    # 大量队伍做对数、提交数完全相同，只能靠队名字典序区分（含前缀关系与空格）
    names = ['Team', 'Team A', 'Team AB', 'TeamA', 'TeamB', 'Team B', 'Alpha', 'Alpha Beta',
             'Beta', 'Gamma', 'Zeta', 'Theta', 'Kappa', 'Lambda']
    rows = []
    for nm in names:
        rows += [f"{nm},A,no", f"{nm},A,yes", f"{nm},B,yes"]
    r.shuffle(rows)
    return str(len(rows)) + "\n" + "\n".join(rows) + "\n"

def repeat_ac_case(r):
    # 重复 AC 同一题：只计一次做对，但提交数照计
    rows = ['Alpha,A,yes'] * 30 + ['Beta,A,yes', 'Beta,B,yes'] + ['Gamma,C,no'] * 5 + ['Gamma,C,yes'] * 3
    rows += [f"Team{c},{c},yes" for c in 'ABCDEFGHIJKL']
    r.shuffle(rows)
    return str(len(rows)) + "\n" + "\n".join(rows) + "\n"

def cases():
    r = random.Random(28127)
    out = [SAMPLE_IN, SAMPLE2_IN, SAMPLE3_IN,
           '1\nPeking University,A,no\n',
           '1\nZ,Z,yes\n']
    out.append(tie_case(r))
    out.append(repeat_ac_case(r))
    out.append(generate_case(r, 12, 12, 3, 0.5, 0))        # 恰好 12 支队伍
    out.append(generate_case(r, 13, 13, 3, 0.5, 0))        # 恰好 13 支，截断最后一名
    out.append(generate_case(r, 40, 11, 5, 0.0, 1))        # 全部 no
    out.append(generate_case(r, 40, 8, 4, 1.0, 1))         # 全部 yes
    out.append(generate_case(r, 20, 4, 3, 0.5, 1))
    out.append(generate_case(r, 200, 30, 26, 0.4, 0))
    out.append(generate_case(r, 500, 60, 26, 0.3, 1))
    out.append(generate_case(r, 1000, 300, 26, 0.5, 0))    # 满规模，队伍很多
    out.append(generate_case(r, 1000, 15, 26, 0.5, 1))     # 满规模，队伍少，做题多
    out.append(generate_case(r, 1000, 5, 26, 0.9, 1))      # 少于 12 队，满规模
    out.append(generate_case(r, 1000, 900, 2, 0.5, 0))     # 大量队伍并列，靠提交数和名字
    out.append(generate_case(r, 1000, 40, 3, 0.2, 1))
    out.append(generate_case(r, 999, 1, 26, 0.5, 1))       # 只有一支队伍
    assert len(out) == 20 and len(set(out)) == 20
    for c in out:
        assert valid(c), c[:80]
    return out

def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        for index, content in enumerate(cases()):
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            if index == 0: assert result.stdout == SAMPLE_OUT
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()
