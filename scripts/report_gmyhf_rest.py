#!/usr/bin/env python3
"""合并其余183题的独立检查；拒绝缺文件、重复、代码或数据已变化的证据。"""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
GROUPS = ('basic', 'middle', 'structures', 'graphs', 'advanced', 'final')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bind_files(files, directory):
    expected = {str(p.relative_to(ROOT)) for p in directory.glob('*.in')}
    paths = [f['input'] for f in files]
    if len(paths) != len(set(paths)) or set(paths) != expected:
        raise ValueError(f'{directory}: 检查文件不完整或重复')
    for record in files:
        path = ROOT / record['input']
        if (sha(path) != record['input_sha256'] or
                sha(path.with_suffix('.out')) != record['output_sha256']):
            raise ValueError(f'{path}: 文件证据过期')
    return hashlib.sha256(json.dumps(sorted(
        ({k: f[k] for k in ('input', 'input_sha256', 'output_sha256')} for f in files),
        key=lambda f: f['input']), sort_keys=True).encode()).hexdigest()


def build(reports):
    baseline_path = ROOT / 'collab/gmyhf-download-followup.json'
    baseline = json.loads(baseline_path.read_text())
    expected = {r['global_number'] for r in baseline['entries'] if 'independent' not in r}
    source_paths = {'scripts/check_gmyhf_rest.py'} | {
        f'scripts/gmyhf_oracles_{group}.py' for group in GROUPS}
    sources = {path: sha(ROOT / path) for path in source_paths}
    entries = {}
    for report in reports:
        if report['sources'] != sources:
            raise ValueError('审核算法已变化或来源不完整，须重新运行')
        for entry in report['entries']:
            number = entry['global_number']
            if number in entries:
                raise ValueError(f'{number}: 重复的题目证据')
            for record in entry['files']:
                if (('matches' in record) == ('unproved' in record) or
                        ('matches' in record and type(record['matches']) is not bool)):
                    raise ValueError(f'{number}: 文件缺少唯一的检查结论')
            entries[number] = entry
    if set(entries) != expected:
        raise ValueError(f'题目覆盖不完整：缺少{sorted(expected-set(entries))}，多出{sorted(set(entries)-expected)}')
    matrix = []
    materialized = {r['global_number']: r for r in json.loads(
        (ROOT / 'collab/gmyhf-download-materialize.json').read_text())['materialized']}
    for prior in baseline['entries']:
        number = prior['global_number']
        if sha(ROOT / prior['statement']) != prior['statement_sha256']:
            raise ValueError(f'{number}: 题面证据已过期')
        entry = entries.get(number, prior.get('independent'))
        row = materialized[number]
        directory = ROOT / 'data/openjudge/tests' / row['bucket'] / (row['local_id'] + '_GMyhf/data')
        snapshot = bind_files(entry['files'], directory)
        if snapshot != prior['download_snapshot_sha256'] or entry['cases'] != len(entry['files']):
            raise ValueError(f'{number}: 数据快照或计数不一致')
        matrix.append({'global_number': number, 'title': prior['title'],
                       'download_cases': entry['cases'],
                       'evidence': '本轮' if number in entries else '前轮26题',
                       'mismatched_files': sum(f.get('matches') is False for f in entry['files']),
                       'invalid_input_files': sum('input_issue' in f for f in entry['files']),
                       'unproved_files': sum('unproved' in f for f in entry['files'])})
    for path, digest in baseline['sources'].items():
        if sha(ROOT / path) != digest:
            raise ValueError(f'{path}: 前轮审核实现已变化')
    new_files = [f for e in entries.values() for f in e['files']]
    return {
        'policy': '只读独立答案核对，不执行参考解，不改数据、不发布；算法一致不等于输入覆盖充分或全部题意已澄清。',
        'baseline': {'path': str(baseline_path.relative_to(ROOT)), 'sha256': sha(baseline_path)},
        'sources': {**sources, 'scripts/report_gmyhf_rest.py': sha(Path(__file__))},
        'summary': {'new_problems': len(entries), 'new_pairs': len(new_files),
                    'matching_pairs': sum(f.get('matches') is True for f in new_files),
                    'mismatched_pairs': sum(f.get('matches') is False for f in new_files),
                    'unproved_pairs': sum('unproved' in f for f in new_files),
                    'total_reviewed_problems': len(matrix),
                    'total_reviewed_pairs': sum(r['download_cases'] for r in matrix)},
        'interpretation_limits': {
            '20075': '按样例及现有数据的一基坐标解释查询位置；题面仅写左上角为原点，未明确坐标起点。',
            '30274': '按继续操作直至不能合并解释，21份一致；正文未明确停止条件，仍待澄清。',
            '30363': '按样例和C(k,2)提示排除自配对，22份一致；正文x<=y仍待改正或澄清。',
            '30276': '按多柱汉诺塔分层策略的二项式边际公式核对23份；未独立证明任意柱数、任意策略的全局最优性下界。',
        },
        'closed_candidates': {'18146': '同一窝可分坐不同座位块。精确块枚举和聚合算法交叉验证后20份一致，不能据初始候选差异判错。'},
        'prior_findings': baseline['manual_findings'],
        'matrix': matrix,
        'entries': sorted(entries.values(), key=lambda r: r['global_number']),
    }


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit('用法：report_gmyhf_rest.py 检查结果.json [...]')
    print(json.dumps(build([json.loads(Path(p).read_text()) for p in sys.argv[1:]]),
                     ensure_ascii=False, indent=2))
