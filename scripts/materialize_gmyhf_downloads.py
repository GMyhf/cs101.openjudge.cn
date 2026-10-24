#!/usr/bin/env python3
"""把 fetch_gmyhf_testdata.py 抓回的平台原始数据落成 `_GMyhf` 判题数据目录。

只落地同时满足以下条件的题（每条都对应一条真实闸门判据或既有决定）：
- 全局题号落在非存档桶（4000-8210 / 10000-19963 / 20000-29982 / 30000-），
  存档桶里 `_GMyhf` 会被 index_tests.is_archive 忽略，落了也不生效；
- 不在 index_tests.SPECIAL_JUDGE_GLOBAL_NUMBERS（多解题，精确比对判不了）；
- 不在 audit_gmyhf_data.RUNTIME_MARGIN_REJECTIONS（已知本地跑不稳）；
- 所有 .out ≤ 2MiB（judge.py RLIMIT_FSIZE，full_sweep.check_output_size）；
- 在 catalog 里有唯一本地题号（不在镜像题库的题接了也不判）；
- 现有活数据目录没有 valid() 输入契约（否则棘轮 check_contract_coverage_ratchet 红，
  201 题留给维护者拍板，见报告 contract_protected）；
- 题面没有「输出任意一…」多解措辞（full_sweep.MULTI_ANSWER 同一判据）。

落盘即替换：已有 `_GMyhf` 整目录换成平台当前数据，内容漂移记入报告
（exact / line_endings_only / content_changed / new）。
已审核的93对输入修正及继续验收的11对修正由gmyhf_input_repairs合并清单重放；输入或答案出现
未审核的变化时，在删除该题旧目录前报错。详见 collab/gmyhf-input-repairs.md。
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tools"))

import full_sweep                                  # noqa: E402
from audit_gmyhf_data import RUNTIME_MARGIN_REJECTIONS  # noqa: E402
from index_tests import SPECIAL_JUDGE_GLOBAL_NUMBERS    # noqa: E402
from gmyhf_input_repairs import load_repairs, repair_pair  # noqa: E402

OPENJUDGE = ROOT / "data" / "openjudge"
TESTS = OPENJUDGE / "tests"
DL = TESTS / "admin_download"
REPORT = ROOT / "collab" / "gmyhf-download-materialize.json"
LOCAL_OUTPUT_LIMIT = 2 * 1024 * 1024
BUCKET_RANGES = ((4000, 8210, "4000-8210"), (10000, 19963, "10000-19963"),
                 (20000, 29982, "20000-29982"), (30000, 10**9, "30000-"))
# 31454：2026-10-22 人拍板用 31454_made 复用私有题 1000002 的校验链
# （README 在 _made 目录）。平台下载内容虽逐字节相同，落成 _GMyhf 会把
# 活目录换走、valid() 契约悄悄失效 —— 不动它。
# 31428：手工配置的函数题（preset_code/preset_suffix/samples.json/verify.py），
# 目录里全是判题钩子，不是可替换的纯数据。
# 28912：继续验收确认平台当前20组正确，旧参考解错误地访问非整数折点；
# 修复参考解并独立复核后解除排除，见 collab/gmyhf-followup-repairs.json。
# 19945/20139：2026-10-24 用户确认废弃题保持排除，不再等待题意澄清。
# 27952/28341：OpenJudge不支持SPJ；保持后台数据排除，本地启用须另行绑定checker。
# 28979/31248为测试占位，31195题名明确to remove；用户选择占位/废弃题保持排除。
MANUAL_EXCLUSIONS = {28979: "2026-10-24 审核：test60测试占位，保持排除",
                     31195: "2026-10-24 审核：题名标记to remove，废弃题保持排除",
                     31248: "2026-10-24 审核：占位模板题，保持排除",
                     27952: "2026-10-24 人拍板：OpenJudge不支持SPJ，本地须另行绑定checker",
                     28341: "2026-10-24 人拍板：OpenJudge不支持SPJ，本地须另行绑定checker",
                     19945: "2026-10-24 人拍板：废弃题保持排除",
                     20139: "2026-10-24 人拍板：废弃题保持排除",
                     31454: "2026-10-22 人拍板 31454_made 复用私有题校验链，不覆盖",
                     31428: "手工配置的函数题（preset/samples/verify），非纯数据目录"}


def bucket_of(number):
    for low, high, name in BUCKET_RANGES:
        if low <= number <= high:
            return name
    return None


def local_id_map():
    """全局题号 → 本地目录名（practice 优先，否则要求数字后缀唯一）。"""
    catalog = json.loads((OPENJUDGE / "test_index.json").read_text(encoding="utf-8"))["catalog"]
    by_global = {}
    for item in catalog["problems"]:
        if "global_number" not in item or item.get("source", "openjudge") != "openjudge":
            continue
        by_global.setdefault(int(item["global_number"]), []).append((item["book"], item["id"]))
    result = {}
    for number, entries in by_global.items():
        practice = [i for b, i in entries if b == "practice"]
        if practice:
            result[number] = practice[0]
            continue
        suffixes = {}
        for _book, item_id in entries:
            match = re.search(r"(\d+)$", item_id)
            if match:
                suffixes.setdefault(match.group(1), item_id)
        if len(suffixes) == 1:
            result[number] = next(iter(suffixes.values()))
    return result


def multi_answer_hit(local_id):
    for page in (OPENJUDGE / "pages").glob(f"*__{local_id}.html"):
        text = re.sub(r"<[^>]+>", " ", page.read_text(encoding="utf-8", errors="replace"))
        text = re.sub(r"\s+", " ", text)
        start = text.find("输出")
        window = text[start:start + 900] if start > 0 else text[:900]
        found = full_sweep.MULTI_ANSWER.search(window)
        if found:
            return found.group(0)
    return None


def norm_hashes(directory):
    result = set()
    for path in directory.rglob("*"):
        if path.is_file() and path.suffix in (".in", ".out"):
            result.add(hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest())
    return result


def stem_key(stem):
    return (0, int(stem)) if stem.isdigit() else (1, stem)


def main():
    manifest = json.loads((DL / "manifest.json").read_text(encoding="utf-8"))
    local_ids = local_id_map()
    ledger = json.loads((ROOT / "collab" / "valid-contracts.json").read_text(encoding="utf-8"))
    contract_dirs = set(ledger["dirs"])
    input_repairs = load_repairs()

    report = {"policy": __doc__.strip().splitlines()[0],
              "download_manifest": str((DL / "manifest.json").relative_to(ROOT)),
              "fetched_at": manifest["fetched_at"],
              "materialized": [], "skipped": {}}
    skipped = report["skipped"]

    def skip(number, reason, **extra):
        skipped.setdefault(reason, []).append({"global_number": number, **extra})

    for num_s, problem in sorted(manifest["problems"].items(), key=lambda kv: int(kv[0])):
        files = problem.get("files") or []
        number = int(num_s)
        title = problem.get("title", "")
        if number in MANUAL_EXCLUSIONS:
            skip(number, "manual_exclusion", detail=MANUAL_EXCLUSIONS[number])
            continue
        if not files:
            skip(number, "no_download_links")
            continue
        bucket = bucket_of(number)
        if bucket is None:
            skip(number, "no_bucket")
            continue
        if number in SPECIAL_JUDGE_GLOBAL_NUMBERS:
            skip(number, "special_judge")
            continue
        if number in RUNTIME_MARGIN_REJECTIONS:
            skip(number, "runtime_margin")
            continue
        oversized = [f["filename"] for f in files
                     if f["filename"].endswith(".out") and f["bytes"] > LOCAL_OUTPUT_LIMIT]
        if oversized:
            skip(number, "output_over_2MiB", files=oversized[:3])
            continue
        local = local_ids.get(number)
        if local is None:
            skip(number, "not_in_catalog")
            continue
        inputs = {f["filename"][:-3]: f for f in files if f["filename"].endswith(".in")}
        outputs = {f["filename"][:-4]: f for f in files if f["filename"].endswith(".out")}
        unpaired = sorted(set(inputs) ^ set(outputs))
        stems = sorted(set(inputs) & set(outputs), key=stem_key)
        if f"tests/{bucket}/{local}_made" in contract_dirs:
            # 活 `_made` 带 valid() 契约。merge_short_gmyhf 只在「_GMyhf 不足 20 组
            # 且 _made 还有非重复输入」时继续引用 _made；两条都不满足时 _made
            # 掉出活目录，棘轮判据（check_contract_coverage_ratchet）当场红。
            # 25274 就是后者：平台只有 1 组退化数据，_made 的 40 组全是它的复制。
            if len(stems) >= 20:
                skip(number, "contract_protected", local_id=local)
                continue
            made_dir = TESTS / bucket / f"{local}_made"
            made_inputs = ([p.read_bytes() for p in made_dir.glob("*.in")]
                           + [p.read_bytes() for p in (made_dir / "data").glob("*.in")])
            downloaded_inputs = {(DL / num_s / inputs[stem]["filename"]).read_bytes()
                                 for stem in stems}
            if made_inputs and all(payload in downloaded_inputs for payload in made_inputs):
                skip(number, "contract_protected", local_id=local,
                     detail="平台数据逐字节覆盖全部 _made 输入，合并后 _made 会掉出活目录")
                continue
        hit = multi_answer_hit(local)
        if hit:
            skip(number, "multi_answer", local_id=local, phrase=hit)
            continue

        if not stems:
            skip(number, "no_paired_cases")
            continue

        # 在删除旧目录前校验全部修正，远端同名文件发生其他变化时保留现有数据并报错。
        prepared = {}
        for stem in stems:
            prepared[stem] = repair_pair(
                number, inputs[stem]["filename"],
                (DL / num_s / inputs[stem]["filename"]).read_bytes(),
                (DL / num_s / outputs[stem]["filename"]).read_bytes(), input_repairs)
        destination = TESTS / bucket / f"{local}_GMyhf"
        drift = "new"
        if destination.is_dir():
            old = norm_hashes(destination)
            new = {hashlib.sha256(payload.replace(b"\r\n", b"\n")).hexdigest()
                   for stem in stems for payload in prepared[stem][:2]}
            raw_old = {hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in destination.rglob("*") if p.suffix in (".in", ".out")}
            raw_new = {hashlib.sha256(payload).hexdigest()
                       for stem in stems for payload in prepared[stem][:2]}
            drift = ("exact" if raw_old == raw_new
                     else "line_endings_only" if old == new else "content_changed")
            shutil.rmtree(destination)
        data = destination / "data"
        data.mkdir(parents=True)
        records = []
        for index, stem in enumerate(stems):
            record = {"case": index}
            fixed_input, fixed_output, correction = prepared[stem]
            for kind, entry, payload in (("input", inputs[stem], fixed_input),
                                         ("output", outputs[stem], fixed_output)):
                target = data / f"{index}.{'in' if kind == 'input' else 'out'}"
                target.write_bytes(payload)
                record[f"original_{kind}"] = entry["filename"]
                record[f"{kind}_bytes"] = len(payload)
                record[f"{kind}_sha256"] = hashlib.sha256(payload).hexdigest()
            if correction is not None:
                record["correction"] = {key: correction[key] for key in
                                        ("reason", "before_input_sha256", "before_output_sha256")}
                record["correction"]["ledger"] = correction.get(
                    "ledger", "collab/gmyhf-input-repairs.json")
            records.append(record)
        provenance = {
            "owner": "GMyhf",
            "provenance": "admin_download",
            "ownership_evidence": ("后台列表行含 /admin/problems/edit/ 且编辑页渲染出 "
                                   "/admin/download 链接（scripts/fetch_gmyhf_testdata.py）"),
            "global_number": number,
            "local_id": local,
            "title": title,
            "fetched_at": manifest["fetched_at"],
            "files": records,
        }
        corrected_pairs = sum("correction" in record for record in records)
        if corrected_pairs:
            ledgers = sorted({record["correction"]["ledger"] for record in records
                              if "correction" in record})
            provenance["correction_ledgers"] = ledgers
            provenance["correction_ledger"] = ("collab/gmyhf-input-repairs.json"
                if "collab/gmyhf-input-repairs.json" in ledgers else ledgers[0])
        if unpaired:
            provenance["unpaired_files_dropped"] = unpaired
        (destination / "SOURCE.json").write_text(
            json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        report["materialized"].append({
            "global_number": number, "local_id": local, "bucket": bucket,
            "title": title, "cases": len(stems),
            "bytes": sum(r["input_bytes"] + r["output_bytes"] for r in records),
            "drift": drift,
            "unpaired_dropped": len(unpaired),
            "contract_preserved_via_merge": f"tests/{bucket}/{local}_made" in contract_dirs,
        })
        if corrected_pairs:
            report["materialized"][-1]["corrected_pairs"] = corrected_pairs

    summary = {}
    for reason, rows in skipped.items():
        summary[reason] = len(rows)
    report["summary"] = {"materialized": len(report["materialized"]), **summary}
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False))
    drift_counts = {}
    for row in report["materialized"]:
        drift_counts[row["drift"]] = drift_counts.get(row["drift"], 0) + 1
    print("drift:", json.dumps(drift_counts, ensure_ascii=False))
    print(f"report: {REPORT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
