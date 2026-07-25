#!/usr/bin/env python3
"""Run targeted conceptual mutants against the independent T-004 oracles.

This is evidence about the concrete reference/oracle pair. It is deliberately
not replaced by a boolean contract field.
"""
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_t004_round1 import GENERATORS, MANIFEST, REFERENCE, oracle, run  # noqa: E402

MUTANTS = {
    3263: ("max(nrows[i][j],f(i+1,j),f(i+1,j+1))", "nrows[i][j]+max(f(i+1,j),f(i+1,j+1))"),
    3376: ("if i>j or s[i]<=s[j]:", "if i>j or s[i]>=s[j]:"),
    3421: ("for j in range(rr,l-1,-1): yield b,j", "for j in range(l,rr+1): yield b,j"),
    3527: ("c.get(x+2,0)", "c.get(x+3,0)"),
    3708: ('bin(int(x)).count("1")', 'bin(int(x)).count("0")'),
    3709: ("n%3", "n%2"),
    3710: ("bin(x^y).count(\"1\")", "bin(x|y).count(\"1\")"),
    3711: ("a in b+b or b in a+a", "a in b or b in a"),
    3712: ("m[y]", 'm.get(str(int(y)+1),"")'),
    3714: ("range(cap,p-1,-1)", "range(p,cap+1)"),
}


def cases_for(number, entry):
    cases = [entry["sample_input"]]
    for index in range(1, 21):
        for attempt in range(100):
            value = GENERATORS[number](random.Random(number + index + attempt * 1000))
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError(f"insufficient mutation cases: {number}")
    return cases


def check():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows = []
    failures = []
    for entry in manifest["entries"]:
        number = entry["local_number"]
        old, new = MUTANTS[number]
        mutated = REFERENCE[number].replace(old, new, 1)
        if mutated == REFERENCE[number]:
            raise AssertionError(f"mutant did not apply: {number}")
        caught = None
        total = 0
        for case in cases_for(number, entry):
            total += 1
            if run(mutated, case).split() != oracle(number, case).split():
                caught = total
                break
        passed = caught is not None
        rows.append({"local_number": number, "mutation": f"{old} -> {new}",
                     "cases_checked_until_first_difference": total,
                     "oracle_caught_mutation": passed,
                     "status": "passed" if passed else "failed"})
        if not passed:
            failures.append(number)
    result = {"batch": "T-004-r1", "criterion": "targeted conceptual reference mutation must be caught by oracle",
              "entries": rows, "failed": failures}
    (ROOT / "collab/t004-round1-mutation-report.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        print(f"{row['local_number']}: {row['status']} (first difference case {row['cases_checked_until_first_difference']})")
    return not failures


if __name__ == "__main__":
    raise SystemExit(0 if check() else 1)

