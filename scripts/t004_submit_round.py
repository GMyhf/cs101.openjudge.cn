#!/usr/bin/env python3
"""把某一轮入库的参考实现逐题提交到平台，核对是否 Accepted。

**为什么值得有这个脚本。** 平台裁决是这条流水线上唯一「不由我们自己判定」的验收：
本地六项自检验的是数据与实现自洽，只有平台能说实现到底对不对、快不快。
可它一直是复核方临时拼命令行发起的——也就是说，它挂在「有人记得做」上。
round11 的 21520 就是从这个缝里漏过去的：六项自检全绿，参考实现平台 TLE 19967ms，
报告里既无裁决字段也无 blocked 标记。

固化成脚本之后，交付方自己就能跑，不必等复核方来发现。

**口令（红线 2）**：只从环境变量 `OJ_USER` / `OJ_PASS` 读，本脚本不接受口令参数、
不落盘、不回显。

用法：
    OJ_USER=... OJ_PASS=... python3 scripts/t004_submit_round.py 14
    OJ_USER=... OJ_PASS=... python3 scripts/t004_submit_round.py 14 --only 27312,28200
    python3 scripts/t004_submit_round.py 14 --dry-run     # 只列要提交什么，不联网
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

TESTS = ROOT / "data" / "openjudge" / "tests"
# 命名约定见 t004_common.samplecode_recompute：C++ 在场时它就是参考实现那一档。
CANDIDATES = (("samplecode.py", "Python3"), ("samplecode.cpp", "G++"))


def jobs_for(round_number, only=None):
    manifest = ROOT / "collab" / f"t004-round{round_number}-manifest.json"
    if not manifest.is_file():
        raise SystemExit(f"找不到清单：{manifest}")
    entries = json.loads(manifest.read_text(encoding="utf-8"))["entries"]
    jobs, missing = [], []
    for entry in entries:
        number = int(entry["local_number"])
        if only and number not in only:
            continue
        made = sorted(TESTS.glob(f"**/{number:05d}_made"))
        if not made:
            missing.append((number, "没有 _made 目录"))
            continue
        for name, language in CANDIDATES:
            path = made[0] / name
            if path.is_file():
                jobs.append({
                    "number": number,
                    "language": language,
                    "path": path,
                    "group": entry.get("submit_group", "practice"),
                })
                break
        else:
            missing.append((number, "目录里没有 samplecode.py / samplecode.cpp"))
    return jobs, missing


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("round", help="轮次编号，例如 14")
    parser.add_argument("--only", help="只提交这些题号，逗号分隔")
    parser.add_argument("--dry-run", action="store_true", help="只列清单，不联网")
    opts = parser.parse_args()

    only = {int(x) for x in opts.only.split(",")} if opts.only else None
    jobs, missing = jobs_for(opts.round, only)
    for number, why in missing:
        print(f"  跳过 {number}: {why}")
    if not jobs:
        raise SystemExit("没有可提交的题")

    if opts.dry_run:
        for job in jobs:
            print(f"  {job['number']:05d} {job['language']:<8} "
                  f"{job['path'].relative_to(ROOT)}  -> /{job['group']}/")
        print(f"共 {len(jobs)} 题（--dry-run，未联网）")
        return 0

    import oj_submit  # 延后导入：--dry-run 时不必要求口令

    try:
        session = oj_submit.Session().login()
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"登录失败：{type(exc).__name__}: {exc}") from None
    print(f"登录成功，共 {len(jobs)} 题待提交")
    results, rejected, errored = [], [], []
    for index, job in enumerate(jobs, 1):
        source = job["path"].read_text(encoding="utf-8", errors="replace")
        # 逐题兜住异常。网络抖动是常态（ConnectionResetError / Connection refused 都撞见过），
        # 让第 15 题的一次抖动带走前 14 题的结果是不值当的；而且「提交失败」和「判为不通过」
        # 必须分开记——当初「6 题不可提交」那个错误结论，就是把前者当成了后者。
        verdict, error = {}, None
        for attempt in range(3):
            try:
                verdict = session.run(f"{job['number']:05d}", source, job["language"], job["group"])
                error = None
                break
            except Exception as exc:  # noqa: BLE001 —— 网络层什么都可能抛
                error = f"{type(exc).__name__}: {exc}"[:120]
        mark = verdict.get("verdict", f"提交失败（{error}）" if error else "?")
        row = {"local_number": job["number"], "language": job["language"], **verdict}
        if error:
            row["submit_error"] = error
        results.append(row)
        # 「没提交上去」和「提交了但没通过」是两件事，分开记。
        # 当初「6 题不可提交」那个错误结论，就是把网络故障当成了平台裁决。
        if error:
            errored.append(job["number"])
        elif mark != "Accepted":
            rejected.append(job["number"])
        spent = f"{verdict['ms']}ms" if verdict.get("ms") else ""
        print(f"[{index:2d}/{len(jobs)}] {job['number']:05d} {job['language']:<8} -> {mark}"
              f"  {spent} (#{verdict.get('solution_id','?')})", flush=True)

    out = ROOT / "collab" / f"t004-round{opts.round}-platform.json"
    accepted = len(results) - len(rejected) - len(errored)
    out.write_text(json.dumps({"round": opts.round, "accepted": accepted,
                               "total": len(results), "not_accepted": rejected,
                               "submit_failed": errored, "results": results},
                              ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\n合计 Accepted {accepted}/{len(results)}；结果写入 {out.name}")
    if rejected:
        print(f"**平台判为不通过：{rejected}** —— 按交付规矩，这些题要么换实现，"
              f"要么标 blocked 说明卡在哪，不得静默交付")
    if errored:
        print(f"**没提交上去（网络故障，不是平台裁决）：{errored}** —— 重跑这几题再下结论，"
              f"不要当成不通过")
    return 1 if (rejected or errored) else 0


if __name__ == "__main__":
    sys.exit(main())
