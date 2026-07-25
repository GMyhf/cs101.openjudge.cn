#!/usr/bin/env python3
"""把 _made/producecase.py 从「内嵌 CASES 回放」改回「固定种子重新生成」。

背景：人的模版 `tests/4000-8210/4102_made/producecase.py` 本来就是真生成器
（`generate_random_case(epoch)` + 随机），agent 生成的四批却把 20 组输入原样内嵌成
`CASES = [...]`，等于同一份输入在仓库里存两份（全仓库 2.23MB，其中 001d 占 1.88MB）。
本脚本按各批 build 脚本里**原样的生成循环**重写 producecase.py，并以
「重跑后 data/ 字节不变」作为验收。

  python3 scripts/slim_producecase.py            # 只改写，不重跑
  python3 scripts/slim_producecase.py --verify    # 改写后逐题重跑并比对字节
"""
import ast, importlib, inspect, json, subprocess, sys, types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "data/openjudge/tests"

# 各批的生成循环形状必须逐字复刻，否则重跑出来的数据不是同一份。
#   001a/001b: cases = [sample] + [gen(random.Random(number + i)) for i in 1..19]
#   001c/001d: 带去重重试, seed = number + i + attempt * 1000
BATCHES = {
    "001a": {"module": "build_001a", "table": "GENERATORS", "dedup": False},
    "001b": {"module": "build_001b", "table": "GENERATORS", "dedup": False},
    "001c": {"module": "build_001c", "table": "GENERATORS", "dedup": True},
    "001d": {"module": "build_001d", "table": "G", "dedup": True},
}

TEMPLATE = '''"""{number} 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：{source}
生成器与循环取自 scripts/{module}.py（批次 {batch}），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = {number}
SAMPLE_IN = {sample_in!r}
SAMPLE_OUT = {sample_out!r}
REFERENCE_SOURCE = {code!r}

{generator}

def build_cases():
{loop}

def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=120, check=True)
    return result.stdout


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
    assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split(), "参考解法跑不出样例输出"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        (root / f"{{index}}.in").write_text(content, encoding="utf-8")
        (root / f"{{index}}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
'''

LOOP_DEDUP = '''    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = {call}(random.Random(NUMBER + i + attempt * 1000))
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
    return cases'''

LOOP_PLAIN = '''    return [SAMPLE_IN] + [{call}(random.Random(NUMBER + i)) for i in range(1, 20)]'''


def literals(path):
    """从旧 producecase.py 里取出字面量赋值，不执行它（执行会重写 data/）。"""
    out = {}
    for node in ast.parse(path.read_text(encoding="utf-8")).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                out[node.targets[0].id] = ast.literal_eval(node.value)
            except ValueError:
                pass
    return out


CONST_TYPES = (str, int, float, bool, tuple, list, dict, set, frozenset)


def closure(module, fn):
    """生成器 + 它传递依赖到的模块级函数**和常量**，按定义顺序返回源码。

    只抓函数是不够的：g5430 引用 build_001b 的 EXPRESSIONS、number_words 引用
    build_001c 的 ONES，漏掉常量会让改写后的 producecase.py 直接 NameError。
    """
    found, consts, stack = {}, {}, [fn]
    while stack:
        current = stack.pop()
        for name in current.__code__.co_names:
            target = getattr(module, name, None)
            if isinstance(target, types.FunctionType):
                if name not in found and target is not fn:
                    found[name] = target
                    stack.append(target)
            elif isinstance(target, CONST_TYPES) and not isinstance(target, type) and name not in consts:
                consts[name] = target
    parts = [f"{name} = {value!r}" for name, value in sorted(consts.items())]
    helpers = sorted(found.values(), key=lambda f: f.__code__.co_firstlineno)
    parts += [inspect.getsource(f).rstrip() for f in helpers + [fn]]
    return "\n\n".join(parts)


def rewrite(batch, number, directory):
    spec = BATCHES[batch]
    module = importlib.import_module(spec["module"])
    generator = getattr(module, spec["table"])[number]
    old = literals(directory / "producecase.py")
    if "CASES" not in old:
        return None                            # 已经是新式（种子重生成），幂等跳过
    cases = old["CASES"]
    code = old.get("REFERENCE_SOURCE") or old["SOURCE"]
    sample_in = old.get("SAMPLE_IN", cases[0])
    sample_out = old.get("SAMPLE_OUT") or (directory / "data" / "0.out").read_text(encoding="utf-8")

    if generator is None:                      # 001a 少数题没有生成器：20 组全是样例
        body, call = "def repeat_sample(r):\n    return SAMPLE_IN", "repeat_sample"
    else:
        body, call = closure(module, generator), generator.__name__
    loop = (LOOP_DEDUP if spec["dedup"] else LOOP_PLAIN).format(call=call)
    text = TEMPLATE.format(number=number, source=spec["module"], module=spec["module"], batch=batch,
                           sample_in=sample_in, sample_out=sample_out, code=code,
                           generator=body, loop=loop)
    before = (directory / "producecase.py").stat().st_size
    (directory / "producecase.py").write_text(text, encoding="utf-8")
    return before, len(text.encode())


def main():
    sys.path.insert(0, str(ROOT / "scripts"))
    saved = 0
    for batch in BATCHES:
        report = ROOT / f"collab/t002-{batch}-report.json"
        for entry in json.loads(report.read_text(encoding="utf-8"))["entries"]:
            number = entry["local_number"]
            directory = next(TESTS.glob(f"*/{number:05d}_made"), None)
            if directory is None or not (directory / "producecase.py").is_file():
                print(f"  跳过 {number}: 没有 producecase.py"); continue
            changed = rewrite(batch, number, directory)
            if changed is None:
                continue
            before, after = changed
            saved += before - after
            print(f"  {batch} {number}: {before/1024:.0f}K -> {after/1024:.0f}K")
    print(f"producecase.py 合计省下 {saved/1024/1024:.2f} MB" if saved else "producecase.py 已全部是新式，无需改写")

    if "--verify" in sys.argv:
        print("\n重跑每题的 producecase.py，data/ 必须逐字节不变：")
        bad = []
        for batch in BATCHES:
            report = ROOT / f"collab/t002-{batch}-report.json"
            for entry in json.loads(report.read_text(encoding="utf-8"))["entries"]:
                number = entry["local_number"]
                directory = next(TESTS.glob(f"*/{number:05d}_made"), None)
                if directory is None: continue
                result = subprocess.run([sys.executable, "producecase.py"], cwd=directory,
                                        capture_output=True, text=True, timeout=900)
                if result.returncode:
                    bad.append((number, "跑失败: " + result.stderr.strip()[-200:])); continue
                diff = subprocess.run(["git", "status", "--porcelain", str(directory / "data")],
                                      cwd=ROOT, capture_output=True, text=True).stdout.strip()
                if diff: bad.append((number, "数据变了:\n" + diff[:300]))
        print("字节不变" if not bad else f"有问题 {len(bad)} 题:")
        for number, why in bad: print(f"  {number}: {why}")
        return 1 if bad else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
