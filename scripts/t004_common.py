"""数据生成批次的共享自检模块。

**为什么要有这个文件**：001a→round5 一路立起来的自检规矩，是写在交接文档里的散条目，
每轮 build 脚本各自重写一遍。结果是**同一个缺陷反复回来**：

| 缺陷 | 立规矩 | 又出现 |
| --- | --- | --- |
| 报告自检字段写死字面量 | 001d | round5 的 `constant_output_probe.status` |
| 手维护的「哪些题没有 oracle」清单 | round4 拆掉 | round5 又写了一份 |
| 变异落在死代码上、等于空操作 | round4 | —— |
| 去重不足 15 组却不记豁免 | 001a | T-007 抓到 5 题、round5 的 4012 |
| 「独立 oracle」其实是参考解法本身 | round4 打回 | round5 的 4011 |

根因不是粗心，是**修复留在了旧脚本里，新脚本从零重写就带不过来**。
所以这里把判据实现一次，后续批次 import 它，而不是各写各的。

**设计上的一条硬规矩**：凡是「实测值」字段，一律由本模块自己算出来，
函数不接受调用方传入的现成结果。想把 `status` 写成 `"rejected"` 这种事，
在这个接口下做不到——这正是 001d 那条规矩失效的原因（当时只写进了文档）。
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

# 每题去重后的最低组数（001a 立）。低于它必须在报告里显式记豁免理由，
# 而不是让数字悄悄躺在那儿——T-007 回扫时 5 题就是这么漏过去的。
MIN_DISTINCT_CASES = 15

# 「独立 oracle」与参考解法的重合报警线。round4 的 17/20、round5 的 4011
# 都是「改个变量名的同一份实现」，逐字重合一算就现形。
#
# 两条判据取或，因为单看比率会在短实现上失真：round5 的 3377 参考解法只有 5 行，
# 两行模板（`while i<=j:` 和 `else:out.append(v[j]);j-=1`）就把比率顶到 40%，
# 而两边算法其实不同（整段反转比较 vs 逐字符增量裁决）——那是误报。
#   · 比率 >= 0.80：短实现里几乎整份一样才报（4140 的 1 行对 1 行 = 1.00）
#   · 逐字相同 >= 5 行：长实现里抄了实质内容就报（4011 是 15 行）
ORACLE_OVERLAP_ALARM = 0.80
ORACLE_SHARED_LINES_ALARM = 5


def constant_output_probe(outputs, exemption=None):
    """恒定输出探针（001d 立）：把最高频的输出原样当解法提交，会不会 AC。

    status **由测量推出**，不接受调用方传入——round5 把它写成了字面量 "rejected"，
    于是 4140 的 21/21（常量解法必 AC、数据零鉴别力）也显示 rejected。
    """
    tokens = [tuple(str(o).split()) for o in outputs]
    total = len(tokens)
    freq = Counter(tokens).most_common(1)[0][1] if tokens else 0
    return {
        "frequency": freq,
        "total": total,
        # 频次等于总数 = 常量解法能过全部数据 = 这份数据没有鉴别力
        # 探针 AC = 常量解法能过全部数据 = 没有鉴别力。但「题面无输入、答案唯一」这类题
        # 天生如此（4140），必须给出豁免理由才算合格，不能默默放过。
        "status": ("exempted" if exemption else "accepted")
                  if total and freq == total else "rejected",
        "exemption": exemption,
        "share": round(freq / total, 3) if total else None,
    }


def distinct_cases(cases, exemption=None):
    """去重组数（001a 立）。不足 MIN_DISTINCT_CASES 时**必须**给出豁免理由。"""
    distinct = len({str(c) for c in cases})
    row = {"total": len(cases), "distinct": distinct, "threshold": MIN_DISTINCT_CASES}
    if distinct >= MIN_DISTINCT_CASES:
        row["status"] = "passed"
        return row
    if not exemption:
        row["status"] = "FAILED"
        row["reason"] = (f"去重后只有 {distinct} 组，低于 {MIN_DISTINCT_CASES}，"
                         f"且没有给出豁免理由（输入域本身小于 15 才算豁免）")
        return row
    row["status"] = "exempted"
    row["exemption"] = exemption
    return row


def constraint_checklist(items):
    """题面约束逐条打钩（001b 立）。**每条的取值必须是生成器实测出来的布尔，不能是字面量。**

    2026-07-26 人拍板「有既有 Accepted 就直接拿来当题目实现、不再另写实现做对拍」之后，
    这条从「多条检查之一」变成了**唯一承重的那根**：

    平台 Accepted 只保证「在**满足题面约束**的输入上正确」。对越界输入，AC 代码照样会
    输出某个东西，而我们会把它当成标准答案写进 .out。以前有两份独立实现时，越界输入
    常会让两者分歧从而暴露；现在只剩一份，**没有任何东西会报警**。

    真实例子：T-007 回扫抓到 9202 的生成器给每张图都造了自环，而题面写明「每行两个
    **不相等**的整数」。换成新规范，AC 代码会对这些非法图给出输出、数据照样「自洽」，
    然后学生正确的解法会在本不该存在的数据上挂掉。

    传入形如 [("1<=n<=1000", True), ("边的两端不相等", True), ...] 的列表；
    值必须是 bool（生成器里 assert 出来的那个），字符串/None 一律判 FAILED。
    """
    if not items:
        return {"status": "FAILED", "reason": "没有给出题面约束打钩表 —— "
                                              "在「AC 源码直接当实现」的流程下这是唯一承重的检查",
                "checked": 0}
    rows, bad = [], []
    for entry in items:
        try:
            text, value = entry
        except (TypeError, ValueError):
            bad.append(f"条目格式不对: {entry!r}")
            continue
        if not isinstance(value, bool):
            # 001d 的教训：字段写成字面量常量，看着通过、其实没测
            bad.append(f"{text!r} 的取值是 {value!r}，不是生成器实测的布尔")
        elif not value:
            bad.append(f"{text!r} 未满足")
        rows.append({"constraint": str(text), "holds": value})
    return {"status": "passed" if not bad else "FAILED", "checked": len(rows),
            "items": rows, "problems": bad[:8]}


def has_oracle(oracle, number, sample_input):
    """这题到底有没有独立 oracle —— **从实现推导，不查手维护的清单**。

    round4 的 `NO_INDEPENDENT_ORACLE` 常量停在返工前的旧集合，导致重跑任何一题
    都会把报告里的 passed 悄悄改回 no_independent_oracle（4034 就是这么掉的）；
    round5 又写了一份同样的常量。清单会和事实脱节，而脱节时它是静默的。
    """
    try:
        oracle(number, sample_input)
    except LookupError:
        return False
    return True


def _normalise(source):
    """按行去掉空白与注释，用于比较两份实现的骨架。"""
    out = []
    for line in str(source).split("\n"):
        line = re.sub(r"#.*$", "", line)
        line = re.sub(r"\s+", "", line)
        if line:
            out.append(line)
    return out


def oracle_independence(reference_source, oracle_source):
    """oracle 与参考解法的逐字重合率。高了就不是「独立」，只是改了变量名。

    round5 的 4011：27 行里 15 行逐字相同，差异只有 agents→Pn、distribute→walk
    和 INF 常量，核心算法一模一样。这种对拍证明不了任何事。
    """
    a, b = _normalise(reference_source), _normalise(oracle_source)
    shared = len(set(a) & set(b))
    base = min(len(a), len(b)) or 1
    ratio = shared / base
    alarm = ratio >= ORACLE_OVERLAP_ALARM or shared >= ORACLE_SHARED_LINES_ALARM
    return {
        "reference_lines": len(a),
        "oracle_lines": len(b),
        "identical_lines": shared,
        "identical_sample": sorted(set(a) & set(b))[:5],
        "overlap": round(ratio, 3),
        "status": "ALARM" if alarm else "passed",
        # 这是**分诊信号，不是判决**：重合高只说明值得人去看一眼两边是不是同一个算法，
        # 指标本身判定不了独立性。写成判决会让人要么盲信、要么因为误报而整体忽略它。
        "note": ("与参考解法逐字重合较多，**请人工确认两边是不是同一个算法**"
                 if alarm else None),
    }


def mutation_is_effective(run, reference_source, mutated_source, cases):
    """变异必须**真的改变行为**（round4 立）。

    只断言源码文本变了是不够的：round4 有 3 条变异的替换串落在别题分支或死代码上，
    21 组输出一模一样，探针等于在测一个不存在的变化。
    """
    if mutated_source == reference_source:
        return {"status": "FAILED", "reason": "变异串没匹配上，源码没有变化",
                "changed_cases": 0, "total": len(cases)}
    changed = sum(1 for c in cases if run(reference_source, c) != run(mutated_source, c))
    return {
        "status": "passed" if changed else "FAILED",
        "changed_cases": changed,
        "total": len(cases),
        "reason": None if changed else "变异后 21 组输出完全一致，是空操作变异",
    }


def byte_reproduction(made_dir, timeout=900):
    """把 `_made` 目录拷出去重跑 producecase.py，`data/` 必须逐字节不变。

    2026-07-25 人拍板去掉内嵌 CASES 时立的验收标准。
    """
    made_dir = Path(made_dir)
    snapshot = lambda root: {p.name: p.read_bytes() for p in sorted(root.glob("*"))}
    try:
        with tempfile.TemporaryDirectory() as folder:
            work = Path(folder) / "w"
            shutil.copytree(made_dir, work)
            before = snapshot(work / "data")
            result = subprocess.run([sys.executable, "producecase.py"], cwd=work,
                                    capture_output=True, text=True, timeout=timeout)
            if result.returncode:
                return {"status": "FAILED", "reason": "producecase.py 跑挂了",
                        "detail": (result.stderr or result.stdout).strip()[-300:]}
            after = snapshot(work / "data")
            if after == before:
                return {"status": "passed"}
            differing = sorted(set(before) ^ set(after)) + \
                sorted(k for k in set(before) & set(after) if before[k] != after[k])
            return {"status": "FAILED", "reason": "重跑后 data/ 与入库内容不一致",
                    "differing_files": differing[:8]}
    except subprocess.TimeoutExpired:
        return {"status": "FAILED", "reason": f"producecase.py 超过 {timeout}s 未结束"}


def samplecode_recompute(made_dir, timeout=60):
    """参考解法对每组 .in 复算，输出须与 .out token 相等。

    round5 的 3433 就是靠这条露出来的：它根本没有 samplecode.py。
    """
    made_dir = Path(made_dir)
    # 参考实现可能是 Python 也可能是 C++。命名约定（2026-07-26 理清）：
    #   samplecode.py      —— Python 是参考实现（绝大多数题）
    #   samplecode.cpp     —— C++ 就是参考实现（3433 本来只有 C++；4011 的 Python 两档都 TLE）
    #   samplecode_ac.cpp  —— Python 仍是产出数据的参考，C++ 只是额外的平台背书
    #                         （3728 / 4009 / 3718 属于这种）
    # 三种都要认：只认其中一种就会把另一类误报成「没有参考实现」。
    script = made_dir / "samplecode.py"
    cpp = next((made_dir / name for name in ("samplecode.cpp", "samplecode_ac.cpp")
                if (made_dir / name).exists()), made_dir / "samplecode.cpp")
    if not script.exists() and not cpp.exists():
        return {"status": "FAILED",
                "reason": "目录里没有 samplecode.py / samplecode.cpp / samplecode_ac.cpp",
                "files": sorted(p.name for p in made_dir.iterdir())}
    executable = None
    if cpp.exists():
        with tempfile.TemporaryDirectory() as folder:
            executable = Path(folder) / "samplecode"
            build = subprocess.run(["g++", "-std=c++17", "-O2", str(cpp), "-o", str(executable)],
                                   capture_output=True, text=True, timeout=timeout)
            if build.returncode:
                return {"status": "FAILED", "reason": f"{cpp.name} 编译失败",
                        "detail": (build.stderr or build.stdout).strip()[-300:]}
            return _recompute_cases(made_dir, [str(executable)], timeout)
    return _recompute_cases(made_dir, [sys.executable, str(script)], timeout)


def _recompute_cases(made_dir, command, timeout):
    bad = []
    inputs = sorted((made_dir / "data").glob("*.in"), key=lambda p: int(p.stem))
    for path in inputs:
        expected = path.with_suffix(".out")
        try:
            got = subprocess.run(command,
                                 input=path.read_text(errors="replace"),
                                 text=True, capture_output=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            bad.append(f"{path.name}:TLE")
            continue
        if got.returncode or got.stdout.split() != expected.read_text(errors="replace").split():
            bad.append(path.name)
    return {"status": "passed" if not bad else "FAILED", "cases": len(inputs),
            "mismatched": bad[:8]}


def sample_is_case_zero(made_dir, sample_input):
    """第 0 组必须是题面样例——数据与题面之间唯一的锚。"""
    first = sorted((Path(made_dir) / "data").glob("*.in"), key=lambda p: int(p.stem))
    if not first:
        return {"status": "FAILED", "reason": "没有任何 .in"}
    same = first[0].read_text(errors="replace").split() == str(sample_input).split()
    return {"status": "passed" if same else "FAILED",
            "reason": None if same else "第 0 组不是题面样例"}


def audit(made_dir, *, cases, outputs, sample_input, exemption=None,
          reference_source=None, oracle_source=None, constraints=None,
          run_byte_reproduction=True):
    """把上面全部判据跑一遍，返回可直接写进报告的条目。

    调用方**不能**传入任何「实测结果」——只能给原料（数据、源码、豁免理由），
    结论一律由本函数算。这是 001d「报告自检字段必须是实测值」那条规矩的落地形式：
    写进文档管不住，写进接口才管得住。
    """
    row = {
        "distinct_cases": distinct_cases(cases, exemption),
        "constant_output_probe": constant_output_probe(outputs, exemption),
        "sample_is_case_zero": sample_is_case_zero(made_dir, sample_input),
        "samplecode_recompute": samplecode_recompute(made_dir),
    }
    if constraints is not None:
        row["constraint_checklist"] = constraint_checklist(constraints)
    if run_byte_reproduction:
        row["byte_reproduction"] = byte_reproduction(made_dir)
    if reference_source is not None and oracle_source is not None:
        row["oracle_independence"] = oracle_independence(reference_source, oracle_source)
    row["failed"] = sorted(k for k, v in row.items()
                           if isinstance(v, dict) and v.get("status") in ("FAILED", "ALARM", "accepted"))
    return row
