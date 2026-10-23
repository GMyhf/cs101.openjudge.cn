"""按审核清单修正 GMyhf 输入；哈希不符即停止，避免重抓后静默套用旧修正。"""
from __future__ import annotations

import calendar
from decimal import Decimal
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "collab/gmyhf-input-repairs.json"
REASONS = {
    18109: "保留前 1000 个字符，覆盖题面最大合法长度",
    18223: "越界正整数按 10^100 取模映射到 1..10^100，0 改为 1",
    20074: "身高、体重调整到各自题面闭区间的最近边界",
    20089: "恢复被重复拼接 10500 次的原始预算与七类计数",
    20136: "补齐无向图缺失的反向邻接，保留边与环结构",
    20162: "系数调整到严格范围内，半径调整到 1..99999999",
    21458: "把越界增肌量 20 调整为合法上界 19",
    21532: "用 2^29 替代越界的 2^30，保留大整数二次幂案例",
    25301: "保留前 99 个学生并同步人数，覆盖最大合法规模",
    26971: "按去重后的评分排名压缩，严格保留相邻评分大小与相等关系",
    26976: "恢复被重复黏连的 1..9 序列，去掉额外输入",
    27373: "把超长整数拆成至多 20 位的正整数，更新个数并保留容量边界",
    27862: "增加一个分支节点，把三叉节点改为二叉结构，保留全部叶子收益",
    28012: "移除最后一行受限节点之后的重复行",
    28193: "按无向端点去重，更新边数，保留连通分量",
    28664: "重建合法地区、出生日期和顺序码，交替覆盖正确及错误校验位",
    29256: "把越界评分 1 调整为合法下界 2",
    29740: "合并重复有向边并累加权重，更新边数，保留网络计算语义",
    30281: "三种移动成本同时除以 2；原输入存在并列最优时微调一处坐标，确保输出唯一",
    30942: "把修改次数设为字符串长度，覆盖最大合法修改次数",
}


def sha(payload):
    return hashlib.sha256(payload).hexdigest()


def unique_route(costs, points):
    a, b, c = costs
    a, b, c = min(a, b+c), min(b, a+c), min(c, a+b)

    def distance(p, q):
        dx, dy = abs(p[0]-q[0]), abs(p[1]-q[1])
        return min(dx, dy)*c + max(0, dx-dy)*a + max(0, dy-dx)*b

    values = []
    for order in itertools.permutations(points):
        route = [(0, 0), *order, (100, 100)]
        values.append(sum(distance(p, q) for p, q in zip(route, route[1:])))
    return values.count(min(values)) == 1


def repair_input(number, payload):
    lines = payload.decode("utf-8").splitlines()
    if number == 18109:
        lines = [lines[0][:1000]]
    elif number == 18223:
        limit = 10**100
        lines = [lines[0]] + [" ".join(str(1 if v == 0 else (v-1) % limit + 1)
                                      for v in map(int, line.split())) for line in lines[1:]]
    elif number == 20074:
        rows = [line.split() for line in lines[1:]]
        lines = [lines[0]] + [f"{min(190, max(150, int(h)))} {min(100, max(45, int(w)))} {s}"
                              for h, w, s in rows]
    elif number == 20089:
        seed = b"10500\n10 0 0 0 3 1 2"
        if payload != seed*10500 + b"\n":
            raise ValueError("20089 不符合已审核的重复拼接形状")
        return seed + b"\n"
    elif number == 20136:
        adj = [set(map(int, line.split()[1:])) for line in lines[1:]]
        for i, neighbors in enumerate(adj):
            for j in list(neighbors):
                adj[j].add(i)
        lines = [lines[0]] + [" ".join(map(str, [i, *sorted(neighbors)]))
                              for i, neighbors in enumerate(adj)]
    elif number == 20162:
        cap = 99999999
        rows = [list(map(int, line.split())) for line in lines[1:]]
        lines = [lines[0]] + [" ".join(map(str, [*(max(-cap, min(cap, v)) for v in row[:3]),
                                                  max(1, min(cap, row[3]))])) for row in rows]
    elif number == 21458:
        lines = [lines[0]] + [f"{t} {min(int(w), 19)}" for t, w in
                              (line.split() for line in lines[1:])]
    elif number == 21532:
        lines = [str(2**29)]
    elif number == 25301:
        lines = ["99", *lines[1:100]]
    elif number == 26971:
        values = list(map(int, lines[1].split()))
        ranks = {v: i for i, v in enumerate(sorted(set(values)))}
        lines = [lines[0], " ".join(str(ranks[v]) for v in values)]
    elif number == 26976:
        if lines[-1].split() != list(map(str, range(1, 10))):
            raise ValueError("26976 不符合已审核的重复拼接形状")
        lines = ["9", " ".join(map(str, range(1, 10)))]
    elif number == 27373:
        values = [str(int(v[i:i+20])) for v in lines[2].split() for i in range(0, len(v), 20)]
        lines = [lines[0], str(len(values)), " ".join(values)]
    elif number == 27862:
        if lines[0] != "8":
            raise ValueError("27862 不符合已审核的三叉树形状")
        lines = ["9", "1 2", "1 3", "2 4", "2 5", "3 6", "3 9", "9 7", "9 8",
                 *lines[8:]]
    elif number == 28012:
        lines = lines[:int(lines[0])+1]
    elif number == 28193:
        n, _ = map(int, lines[0].split())
        edges = list(dict.fromkeys(tuple(sorted(map(int, line.split()))) for line in lines[2:]))
        lines = [f"{n} {len(edges)}", lines[1], *(f"{a} {b}" for a, b in edges)]
    elif number == 28664:
        fixed = []
        weights = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
        for i, value in enumerate(lines[1:], 1):
            year = 1900 + int(value[6:10]) % 125
            month = (int(value[10:12])-1) % 12 + 1
            day = (int(value[12:14])-1) % calendar.monthrange(year, month)[1] + 1
            prefix = f"110101{year:04}{month:02}{day:02}{i:03}"
            check = "10X98765432"[sum(int(v)*w for v, w in zip(prefix, weights)) % 11]
            if i % 2 == 0:
                check = "0123456789X"[("0123456789X".index(check)+1) % 11]
            fixed.append(prefix + check)
        lines = [lines[0], *fixed]
    elif number == 29256:
        lines = [lines[0], " ".join(str(max(2, int(v))) for v in lines[1].split())]
    elif number == 29740:
        n, _ = map(int, lines[0].split())
        weights = {}
        for line in lines[n+1:]:
            a, b, w = map(int, line.split())
            weights[a, b] = weights.get((a, b), 0) + w
        lines = [f"{n} {len(weights)}", *lines[1:n+1],
                 *(f"{a} {b} {w}" for (a, b), w in weights.items())]
    elif number == 30281:
        lines[0] = " ".join(str(Decimal(v)/2) for v in lines[0].split())
        costs = tuple(map(Decimal, lines[0].split()))
        rows = [line.split() for line in lines[1:]]
        points = [(int(row[1]), int(row[2])) for row in rows]
        if not unique_route(costs, points):
            found = None
            for radius in range(1, 199):
                for index, axis, sign in itertools.product(range(3), range(2), (-1, 1)):
                    candidate = [list(p) for p in points]
                    candidate[index][axis] += sign*radius
                    if not -99 <= candidate[index][axis] <= 99:
                        continue
                    if unique_route(costs, candidate):
                        found = candidate
                        break
                if found is not None:
                    break
            if found is None:
                raise ValueError("30281 无法构造唯一最优路线")
            lines[1:] = [f"{row[0]} {x} {y}" for row, (x, y) in zip(rows, found)]
    elif number == 30942:
        lines[1] = str(len(lines[0]))
    else:
        raise ValueError(f"未审核的输入修正规则：{number}")
    return ("\n".join(lines) + "\n").encode("utf-8")


def load_repairs():
    data = json.loads(LEDGER.read_text(encoding="utf-8"))
    return {(row["global_number"], row["original_input"]): row for row in data["entries"]}


def repair_pair(number, filename, input_data, output_data, repairs):
    entry = repairs.get((number, filename))
    if entry is None:
        return input_data, output_data, None
    current = sha(input_data), sha(output_data)
    after = entry["input_sha256"], entry["output_sha256"]
    if current == after:
        return input_data, output_data, entry
    before = entry["before_input_sha256"], entry["before_output_sha256"]
    if current != before:
        raise ValueError(f"{number}/{filename} 已变化，须重新审核后更新修正清单")
    fixed_input = repair_input(number, input_data)
    fixed_output = entry["corrected_output"].encode("utf-8")
    if (sha(fixed_input), sha(fixed_output)) != after:
        raise ValueError(f"{number}/{filename} 修正规则或答案与审核哈希不符")
    return fixed_input, fixed_output, entry
