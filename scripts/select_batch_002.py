#!/usr/bin/env python3
"""Select the next solution-backed T-003 batch after T-002-001."""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from build_001a import locate_source

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data/openjudge/catalog.json"
SKIPS = ROOT / "collab/t002-special-judge-skips.md"
OUT = ROOT / "collab/t003-batch-002-manifest.json"
POOL_OUT = ROOT / "collab/t003-batch-002-candidates.json"
SOURCES = [
    Path("/home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md"),
    Path("/home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md"),
]


# 题解常把多组样例塞进同一个代码块，用 `sample1 in:` / `Sample Input1:` / `样例输入1`
# 这类标签行分隔。整块当样例会把标签行写进 case-0，题解喂进去直接 ValueError。
SAMPLE_LABEL = re.compile(
    r"^\s*(?:sample|样例)\s*\d*\s*[-_ ]?\s*(in(?:put)?|out(?:put)?|输入|输出)?\s*\d*\s*[:：]?\s*$",
    re.I,
)


def split_labelled(block):
    """把带标签的样例块拆开，返回 (第一组输入, 第一组输出)。无标签则原样返回。"""
    lines = block.splitlines()
    if not any(SAMPLE_LABEL.match(line) for line in lines):
        return block, None
    parts, current = [], None
    for line in lines:
        match = SAMPLE_LABEL.match(line)
        if match:
            tag = (match.group(1) or "").lower()
            current = ["out" if tag.startswith(("out", "输出")) else "in", []]
            parts.append(current)
            continue
        if current is not None:
            current[1].append(line)

    def first(kind):
        for name, body in parts:
            if name == kind and "\n".join(body).strip():
                return "\n".join(body).strip() + "\n"
        return None

    return first("in") or block, first("out")


def sections(path):
    path = locate_source(str(path))
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    starts = [i for i, line in enumerate(lines) if re.match(r"^##\s+", line)]
    for i, start in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else len(lines)
        match = re.match(r"^##\s+[^\d]*(\d+)[:：]\s*(.*)$", lines[start])
        if not match:
            continue
        text = "\n".join(lines[start:end])
        codes = re.findall(r"```(?:python|py)?\s*\n(.*?)```", text, re.S | re.I)
        samples = re.findall(r"(?:样例输入|Sample Input|sample input)\s*\n+```\n(.*?)```", text, re.S | re.I)
        outputs = re.findall(r"(?:样例输出|Sample Output|sample output)\s*\n+```\n(.*?)```", text, re.S | re.I)
        yield int(match.group(1)), match.group(2).strip(), codes, samples, outputs


EXPLAIN = re.compile(r"^\s*(#|解释|说明|===+|-{5,})")


def trim_explanation(block):
    """砍掉样例输出尾巴上的题面讲解。

    题解里的样例输出块常把答案和讲解写在一起，例如
    `0 0 7\n1 0 -7\n1 2 3\n\n解释：\nA = [...`、`5\nHHHOO\n# 1->H->3->...`。
    整块当期望输出，题解算得再对也「跑不出样例」——11 个被判不可构建的候选里有 10 个是这么来的。
    只在未截断版本对不上、截断版本对得上时才采用（见 reproduces），并在候选里标记，
    这样最坏情况只是少救回一题，不会把错解法放进来。
    """
    kept = []
    for line in block.splitlines():
        if EXPLAIN.match(line):
            break
        kept.append(line)
    while kept and not kept[-1].strip():
        kept.pop()
    return ("\n".join(kept) + "\n") if kept else block


def reproduces(codes, sample_in, sample_out):
    """题解里是否真有一段能跑出样例。

    选批只检查「有 import/def 的代码块」是不够的：构建器要求候选代码跑通样例，
    跑不通就 AssertionError 硬失败。把这条前移到选批，后面几批不会再被埋雷。
    """
    trimmed = trim_explanation(sample_out)
    for code in codes:
        try:
            with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
                handle.write(code)
                handle.flush()
                result = subprocess.run(["python3", handle.name], input=sample_in, text=True,
                                        capture_output=True, timeout=10)
            if result.returncode:
                continue
            if result.stdout.split() == sample_out.split():
                return True, sample_out, False
            if trimmed != sample_out and result.stdout.split() == trimmed.split():
                return True, trimmed, True
        except (OSError, subprocess.SubprocessError):
            continue
    return False, sample_out, False


def number(value):
    match = re.search(r"(\d+)$", value)
    return int(match.group(1)) if match else None


def skipped():
    return {int(x) for x in re.findall(r"\|\s*0*(\d+)\s*\|", SKIPS.read_text(encoding="utf-8"))}


def made_numbers():
    result = set()
    for path in (ROOT / "data/openjudge/tests").glob("*/*_made"):
        value = number(path.name[:-5])
        if value is not None:
            result.add(value)
    return result


def main():
    round_name = sys.argv[1] if len(sys.argv) > 1 else ""
    suffix = {f"--round{k}": f"round{k}" for k in range(2, 10)}.get(round_name)
    batch_name = f"T-003-002-r{suffix[-1]}" if suffix else "T-003-002"
    out = ROOT / (f"collab/t003-batch-002-{suffix}-manifest.json" if suffix else "collab/t003-batch-002-manifest.json")
    pool_out = ROOT / (f"collab/t003-batch-002-{suffix}-candidates.json" if suffix else "collab/t003-batch-002-candidates.json")
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))["problems"]
    missing = {number(item["id"]) for item in catalog if not item.get("test_cases")}
    excluded = skipped() | made_numbers()
    candidates = {}
    for source in SOURCES:
        for local, title, codes, samples, outputs in sections(source):
            if local not in missing or local in excluded or local in candidates:
                continue
            usable = [code for code in codes if "import " in code or "def " in code]
            if not usable or not samples:
                continue
            sample_in, sample_out = split_labelled(samples[0].strip() + "\n")
            if sample_out is None and outputs:
                block = outputs[0].strip() + "\n"
                head, tail = split_labelled(block)
                # 无标签时 split_labelled 原样返回，整块就是样例输出
                sample_out = tail or (block if head == block else None)
            if sample_out is None:
                continue                       # 没有样例输出就无法校验题解，不进候选池
            candidates[local] = {
                "local_number": local,
                "title": title,
                "source": str(locate_source(str(source))),
                "source_heading": f"{local}: {title}",
                "python_solution_count": len(usable),
                "sample_input": sample_in,
                "sample_output": sample_out,
                "sample_reproduced": None,        # 下面统一填，顺带可能修正 sample_output
                "selection_source": "solution-backed candidate pool",
                "_codes": usable,
            }
    for entry in candidates.values():
        ok, corrected, was_trimmed = reproduces(entry.pop("_codes"),
                                                entry["sample_input"], entry["sample_output"])
        entry["sample_reproduced"] = ok
        entry["sample_output"] = corrected
        entry["sample_output_trimmed"] = was_trimmed
    ordered = [candidates[key] for key in sorted(candidates)]
    buildable = [x for x in ordered if x["sample_reproduced"]]
    manifest = {
        "batch": batch_name,
        "selection_rule": ("catalog test_cases empty, no existing _made directory, special-judge skip excluded, "
                           "Python solution AND sample present, and the solution actually reproduces the sample"),
        "candidate_count": len(ordered),
        "buildable_count": len(buildable),
        "unbuildable": [x["local_number"] for x in ordered if not x["sample_reproduced"]],
        "selected_count": min(20, len(buildable)),
        "excluded_special_judge": sorted(skipped()),
        "excluded_existing_made": sorted(made_numbers()),
        "entries": buildable[:20],
    }
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    pool_out.write_text(json.dumps({"batch": batch_name, "candidates": ordered}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"selected {len(buildable[:20])} of {len(buildable)} buildable ({len(ordered)} candidates scanned)")
    print("batch:", ", ".join(f"{x['local_number']:05d}" for x in buildable[:20]))
    if manifest["unbuildable"]:
        print("题解跑不出样例、已排除:", ", ".join(f"{n:05d}" for n in manifest["unbuildable"]))


if __name__ == "__main__":
    main()
