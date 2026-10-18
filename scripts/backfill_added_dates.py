#!/usr/bin/env python3
"""Backfill first catalog appearance dates from Git history; keep earlier known dates."""
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
CATALOG = 'data/openjudge/catalog.json'
DEST = ROOT / 'data/openjudge/added_dates.json'


def main():
    current = json.loads((ROOT / CATALOG).read_text())['problems']
    wanted = {f"{p['book']}/{p['id']}" for p in current}
    dates = json.loads(DEST.read_text()) if DEST.exists() else {}
    history = subprocess.check_output(
        ['git', 'log', '--reverse', '--format=%H %cs', '--', CATALOG], cwd=ROOT, text=True)
    for line in history.splitlines():
        commit, day = line.split()
        catalog = json.loads(subprocess.check_output(
            ['git', 'show', f'{commit}:{CATALOG}'], cwd=ROOT))
        for p in catalog.get('problems', []):
            key = f"{p['book']}/{p['id']}"
            if key in wanted:
                dates.setdefault(key, day)
    for p in current:
        key = f"{p['book']}/{p['id']}"
        if p.get('added_at'):
            dates.setdefault(key, p['added_at'])
    DEST.write_text(json.dumps(dict(sorted(dates.items())), ensure_ascii=False, indent=2) + '\n')
    print(f'{len(wanted & dates.keys())}/{len(wanted)} current records dated')


if __name__ == '__main__':
    main()
