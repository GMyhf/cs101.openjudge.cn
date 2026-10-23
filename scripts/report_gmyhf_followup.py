#!/usr/bin/env python3
"""汇总只读审核证据；旧 AC 必须与当前代码和全部活跃输入输出哈希一致才可复用。

用法：report_gmyhf_followup.py 独立检查.json 契约筛查.json 补充四题.json 格点图.json
输出到标准输出，不修改测试数据。先按 followup.md 中的命令生成四份证据。
"""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import judge
from build_input_domains import statement_text


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bound_files(files):
    """证据过期立即拒绝，避免把历史 AC 或推导套到变化后的数据上。"""
    for item in files:
        path = ROOT/item['input']
        if sha(path) != item['input_sha256'] or sha(path.with_suffix('.out')) != item['output_sha256']:
            raise ValueError(f'{path}: 审核证据已经过期')


def build(independent, contracts, supplemental, graph):
    from check_gmyhf_remaining import SOLVERS
    sources = {'scripts/check_gmyhf_remaining.py': independent['script_sha256'],
               'scripts/check_gmyhf_supplemental_answers.py': supplemental['script_sha256']}
    for path, digest in sources.items():
        if sha(ROOT/path) != digest:
            raise ValueError(f'{path}: 算法已变化，须重新运行审核')
    old = json.loads((ROOT/'collab/gmyhf-download-acceptance.json').read_text())
    repaired = json.loads((ROOT/'collab/gmyhf-input-repairs.json').read_text())
    refs = {r['global_number']: r for r in old['reference_judges']['entries']}
    refs.update({r['global_number']: r for r in repaired['verification']['reference_judges']})
    specific = {r['global_number']: r for r in independent['entries']+supplemental['entries']}
    checks = {r['global_number']: r for r in contracts}
    rows = json.loads((ROOT/'collab/gmyhf-download-materialize.json').read_text())['materialized']
    catalog = json.loads((ROOT/'data/openjudge/catalog.json').read_text())['problems']
    result = []
    for row in rows:
        number = row['global_number']; ref = refs[number]
        aliases = [p for p in catalog if p.get('global_number') == number and p.get('source', 'openjudge') == 'openjudge']
        problem = next((p for p in aliases if p['book'] == 'practice'), aliases[0])
        page = ROOT/'data/openjudge/pages'/f"{problem['book']}__{problem['id']}.html"
        item = judge.catalog_item(problem['book'], problem['id'])
        pairs = [{'input': c['input'], 'input_sha256': sha(judge.MIRROR/c['input']),
                  'output': c['output'], 'output_sha256': sha(judge.MIRROR/c['output'])} for c in item['test_cases']]
        snapshot = hashlib.sha256(json.dumps(pairs, sort_keys=True).encode()).hexdigest()
        if ref['case_snapshot_sha256'] != snapshot or (ref['reference'] and sha(ROOT/ref['reference']) != ref['reference_sha256']):
            raise ValueError(f'{number}: 参考解或活跃数据已变化，历史判题结果不可复用')
        directory = ROOT/'data/openjudge/tests'/row['bucket']/(row['local_id']+'_GMyhf/data')
        downloaded = [{'input': str(p.relative_to(ROOT)), 'input_sha256': sha(p),
                       'output_sha256': sha(p.with_suffix('.out'))} for p in sorted(directory.glob('*.in'))]
        entry = {'global_number': number, 'title': row['title'], 'drift': row['drift'],
                 'statement': str(page.relative_to(ROOT)), 'statement_sha256': sha(page),
                 'download_cases': len(downloaded),
                 'download_snapshot_sha256': hashlib.sha256(json.dumps(downloaded, sort_keys=True).encode()).hexdigest(),
                 'reference_evidence': ref, 'contract_scan': checks[number],
                 'answer_review': '仅参考解一致，尚无本轮独立答案验证'}
        if number in specific:
            evidence = specific[number]; bound_files(evidence['files'])
            if {f['input'] for f in evidence['files']} != {f['input'] for f in downloaded}:
                raise ValueError(f'{number}: 独立验证没有覆盖全部下载文件')
            entry['independent'] = evidence
            entry['method'] = (SOLVERS[number].__name__ if number in SOLVERS else
                               '数织提示约束传播并核对答案' if number in (30159, 30160) else '补充四题独立算法')
            entry['answer_review'] = '独立逐文件核对，结论见 files；不代表覆盖充分或沙箱时限验收'
        entry['repaired_pairs_previously_verified'] = sum(r['global_number'] == number for r in repaired['entries'])
        result.append(entry)
    by_number = {r['global_number']: r for r in result}
    for number, quote in {
        16531: '空行与全零不一样',
        30162: '即使出现问题，表达式中也只会有数字、小数点',
        30281: '他每一次可以移动到相邻的 8 个格点处',
        30274: '经过若干次操作后，剩下的铀块总质量最大可能是多少',
        30363: '1 ≤ x ≤ y ≤ N',
    }.items():
        entry = by_number[number]
        text = statement_text(entry['reference_evidence']['book'], entry['reference_evidence']['problem'])
        if quote not in text:
            raise ValueError(f'{number}: 题面引文失效')
        entry['statement_quote'] = quote
    route = by_number[30281]['independent']['files']
    if {r['input'] for r in graph} != {r['input'] for r in route} or not all(
            r['pairs'] == 10 and r['graph_dijkstra_matches'] and
            r['input_sha256'] == sha(ROOT/r['input']) and
            r['script_sha256'] == independent['script_sha256'] for r in graph):
        raise ValueError('格点图交叉检查不完整')
    return {'policy': '只报告，不改数据、不发布。覆盖209题契约及历史参考解证据；独立答案覆盖26题，其他题不宣称完整验收。',
            'sources': {**sources, 'scripts/recheck_gmyhf_references.py': sha(ROOT/'scripts/recheck_gmyhf_references.py'),
                        'scripts/report_gmyhf_followup.py': sha(Path(__file__))},
            'summary': {'problems': len(result), 'download_pairs': sum(r['download_cases'] for r in result),
                        'independent_problems': len(specific), 'independent_pairs': sum(r['cases'] for r in specific.values()),
                        'without_full_independent_answer_review': len(result)-len(specific),
                        'new_invalid_inputs': sum('input_issue' in f for r in independent['entries'] for f in r['files']),
                        'new_wrong_outputs': sum(f.get('matches') is False for r in independent['entries'] for f in r['files']),
                        'route_ties': sum(len(f['optimal_orders']) > 1 for f in route)},
            'manual_findings': {
                '16531': '题面提示明确允许空答题行；21份均独立核对一致，关闭旧歧义。',
                '18104': '0<=g,s<=100 与正整数矛盾；允许0时答案均一致，合法性仍待澄清。',
                '20102': '题面未写n下界；允许n=0时按区域公式得1，合法性仍待澄清。',
                '30162': '9.in含等号，违反注2对错误表达式也适用的字符白名单；其余10份答案一致。',
                '30281': '参考解及上一轮复核漏算两个反向对角移动；9份费用偏大。4份有两种最优顺序，题面未要求唯一，不能定为非法输入；当前token比较会拒绝另一个合法答案。',
                '30274': '题面经过若干次操作未说明必须合并至不能操作；样例总质量6而输出1。需明确停止条件，未据此断言下载答案错误。',
                '30363': '正文x<=y包含自配对，样例和提示C(k,2)排除自配对；需把不等号澄清为x<y。未据此修改答案。',
            }, 'lattice_graph_checks': graph, 'entries': result}


if __name__ == '__main__':
    if len(sys.argv) != 5:
        raise SystemExit(__doc__)
    print(json.dumps(build(*(json.loads(Path(p).read_text()) for p in sys.argv[1:])), ensure_ascii=False, indent=2))
