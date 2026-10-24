#!/usr/bin/env python3
"""只读复核30497：提示允许固定回答；末尾缺LF不等于输入语义越界。

保留原报告、既有valid和题库绑定，不改平台文件或题面。
"""
import argparse
from datetime import datetime, timezone
import html
import importlib.util
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
HINT = '如果你认为此类问题是不可判定的，请在所有样例下输出"undecidable"。'


def plain(text):
    # 题面里的裸小于号是数学符号，不能连同后面的范围一起当HTML标签删除。
    text = re.sub(r'<(?![/a-zA-Z!])', '&lt;', text)
    return ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', text)).split())


def permitted_hint_response(fields):
    """仅核对本题明确允许的回答，不据此判定具体瓷砖能否铺满平面。"""
    if HINT not in plain(fields.get('hint', '')):
        raise ValueError('题面提示没有明确允许固定回答，不能沿用undecidable金标')
    return 'undecidable'


def input_domain(payload):
    """独立核对逐行结构及数值范围，允许最后一行直接以EOF结束。"""
    lines = payload.decode('utf-8').splitlines()
    if not lines or not re.fullmatch(r'[0-9]+', lines[0]):
        raise ValueError('缺少单独一行的N')
    n = int(lines[0])
    if not 1 <= n <= 100 or len(lines) != n + 1:
        raise ValueError('瓷砖种数或行数不符')
    colors = []
    for line in lines[1:]:
        tokens = line.split()
        if len(tokens) != 4 or any(not re.fullmatch(r'[0-9]+', token) for token in tokens):
            raise ValueError('每块瓷砖必须提供四个非负整数')
        row = list(map(int, tokens))
        if any(not 0 <= value <= 1000 for value in row):
            raise ValueError('颜色超出0..1000')
        colors.extend(row)
    return {'n': n, 'min_color': min(colors), 'max_color': max(colors)}


def verify_pair(fields, given, gold):
    response = permitted_hint_response(fields)
    domain = input_domain(given)
    if gold.split() != [response.encode()]:
        raise ValueError('金标不是提示明确允许的固定回答；其他回答需另行证明')
    return domain


def run(work):
    # 网络与账号依赖只在显式运行审计时加载，离线单元测试不登录后台。
    sys.path.insert(0, str(ROOT / 'scripts'))
    import repair_gmyhf_pending_answers as common
    import judge
    sha = common.sha
    session = common.platform.oj_submit.Session().login()
    url = common.platform.oj_submit.HOST + '/admin/problems/edit/?id=30497'
    before = session._get(url)
    fields = common.platform.parse_form(before)
    common.require(fields.get('problemId') == '30497', '后台题号不符')
    permitted_hint_response(fields)
    local = (ROOT / 'data/openjudge/pages/practice__30497.html').read_text()
    hint = re.search(r'<dt>提示</dt>\s*<dd>(.*?)</dd>', local, re.S)[1]
    common.require(plain(hint) == plain(fields['hint']), '本地与平台提示不一致')
    original_path = ROOT / 'collab/gmyhf-pending-batch8-review.json'
    original = next(row for row in json.loads(original_path.read_text())['entries']
                    if row['global_number'] == 30497)
    expected = {row['filename']: row['sha256'] for row in original['checks']['readback']['files']}
    names = common.listed_files(before, 30497)
    common.require(set(expected) <= set(names), '原后台测试文件缺失')
    extra = sorted(set(names) - set(expected))
    common.require(all(not name.endswith(('.in', '.out')) for name in extra), '新增测试数据需另行审核')
    work.mkdir(parents=True, exist_ok=True)
    payloads = {}
    for name in names:
        payload = common.platform.download(session, 30497, name)
        if name in expected:
            common.require(sha(payload) == expected[name], '原后台文件已变：' + name)
        (work / name).write_bytes(payload)
        payloads[name] = payload
    directory = ROOT / 'data/openjudge/tests/30000-/30497_made'
    spec = importlib.util.spec_from_file_location('tile_generator', directory / 'producecase.py')
    generator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generator)
    checks = []
    for name in names:
        if not name.endswith('.in'):
            continue
        given, gold = payloads[name], payloads[name[:-3] + '.out']
        domain = verify_pair(fields, given, gold)
        checks.append({'input': name, 'domain': domain,
                       'strict_valid': generator.valid(given.decode()),
                       'valid_after_final_lf': generator.valid(given.decode() + '\n'),
                       'hint_permitted_answer': True})
    made = []
    for path in sorted((directory / 'data').glob('*.in')):
        verify_pair(fields, path.read_bytes(), path.with_suffix('.out').read_bytes())
        made.append({'input': path.name, 'input_sha256': sha(path.read_bytes()),
                     'output_sha256': sha(path.with_suffix('.out').read_bytes())})
    result = judge.judge('practice', '30497', 'python', (directory / 'samplecode.py').read_text())
    common.require(result['status'] == 'Accepted', '本地原绑定参考解未通过')
    after = session._get(url)
    common.require(common.form_sha(before) == common.form_sha(after), '后台表单发生变化')
    common.require(common.listed_files(after, 30497) == names, '后台文件清单发生变化')
    return {'task': 'T-060', 'batch': 25, 'global_number': 30497,
            'checked_at': datetime.now(timezone.utc).isoformat(),
            'scope': '纠正漏读提示的输出误报；缺末尾LF不违反题面语义，既有valid及接入排除保持',
            'hint': plain(fields['hint']), 'public_hint_matches_admin': True,
            'original_report': str(original_path.relative_to(ROOT)),
            'original_report_sha256': sha(original_path.read_bytes()),
            'admin_form_sha256': common.form_sha(after), 'admin_form_unchanged': True,
            'readback_files': {name: sha(payload) for name, payload in payloads.items()},
            'original_test_files_unchanged': True, 'additional_attachments_not_executed': extra,
            'download_pairs': len(checks), 'checks': checks,
            'made_pairs': len(made), 'made_files': made, 'local_judge': result,
            'platform_writes': 0, 'preserve_existing_validator_and_exclusion': True,
            'sources_sha256': {str(path.relative_to(ROOT)): sha(path.read_bytes()) for path in
                               (Path(__file__), ROOT / 'tests/test_30497_review.py',
                                directory / 'producecase.py', directory / 'samplecode.py')}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, default=Path('/tmp/gmyhf-30497-readback'))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    report = run(args.work)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(f"30497：{report['download_pairs']}组后台数据、{report['made_pairs']}组自产数据核验通过；零写入")


if __name__ == '__main__':
    main()
