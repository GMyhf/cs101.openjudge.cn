#!/usr/bin/env python3
"""修复已审核的越界输入与答案格式；默认只生成计划，--apply 才回填。"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

import repair_gmyhf_pending_answers as common
from repair_gmyhf_pending_answers import (ROOT, sha, save, require, listed_files,
                                         form_sha, audit_statement, sanitized, platform, judge)
from gmyhf_review_fixes import repair_input, no_leading_zero_reference

BATCHES = {1: {19964: 16, 19968: 16, 30825: 15, 30920: 16, 31415: 15, 31435: 15},
           2: {27945: 13, 28014: 13, 28191: 13, 28339: 13, 29905: 14},
           3: {21471: 9, 25563: 11, 25577: 11, 27946: 13, 30177: 14},
           5: {28187: 13, 28188: 13, 28189: 13, 28682: 13, 28696: 13},
           6: {25579: 11}, 7: {25685: 12}, 9: {28277: 13, 28680: 13},
           10: {21729: 11, 30236: 16}, 11: {28016: 13}, 12: {31241: 10}, 13: {31239: 10}}


def reference_command(source, language, target):
    """仅用于已经核对来源哈希的自写参考，不接受平台附件源码。"""
    require(language in ('python3', 'cpp'), '未知自写参考语言')
    reference = target / ('reference.cpp' if language == 'cpp' else 'reference.py')
    reference.write_text(source)
    if language == 'cpp':
        binary = target / 'reference-bin'
        compiled = subprocess.run(['g++', '-std=c++17', '-O2', str(reference), '-o', str(binary)],
                                  capture_output=True, timeout=120)
        require(compiled.returncode == 0, '自写C++参考编译失败')
        return reference, [str(binary)]
    return reference, [sys.executable, '-I', str(reference)]


def prepare(batch, work):
    groups = []
    for number, audit_batch in BATCHES[batch].items():
        evidence = ROOT / f'collab/gmyhf-pending-batch{audit_batch}-review.json'
        if number == 30236:
            # 用户补充规则后重绑题面；原始数据及参考源码的审核证据保持不变。
            evidence = ROOT / 'collab/gmyhf-30236-rule-review.json'
        if number in (31239, 31241):
            # 原审核仅含公开注入题面；后台载荷核对一致后补齐六字段绑定。
            evidence = ROOT / f'collab/gmyhf-{number}-admin-form-review.json'
        entry = next(e for e in json.loads(evidence.read_text())['entries']
                     if e['global_number'] == number)
        proof = entry['authored_reference']
        require(sha(proof['source'].encode()) == proof['sha256'], '参考源码哈希不符')
        source = proof['source']
        if number == 30236:
            source = no_leading_zero_reference(source)
        if number == 31435:
            # 把自产格式化函数一并写入独立参考，隔离判题不依赖仓库导入。
            source = (ROOT / 'scripts/gmyhf_review_fixes.py').read_text() + (
                "\nimport sys\nsys.stdout.write(canonical_ranges(sys.stdin.read()) + '\\n')\n")
        baseline = {r['filename']: r['sha256'] for r in entry['checks']['readback']['files']}
        prior = None
        if number == 19964:
            prior_path = ROOT / 'collab/gmyhf-answer-repairs-batch1.json'
            prior = next(p for p in json.loads(prior_path.read_text())['problems']
                         if p['global_number'] == number)
            baseline.update(prior['final_files'])
        target = ROOT / f'data/openjudge/tests/admin_review_repaired/{number}'
        (target / 'data').mkdir(parents=True, exist_ok=True)
        language = proof.get('language', 'python3')
        reference, command = reference_command(source, language, target)
        changes, cases = [], []
        altered_inputs = 0
        for record in entry['checks']['answers']['files']:
            given_name, out_name = record['input'], record['output']
            base = ROOT / f'data/openjudge/tests/admin_download/{number}'
            given, answer = (base / given_name).read_bytes(), (base / out_name).read_bytes()
            require(sha(given) == record['input_sha256'] and sha(answer) == record['output_sha256'],
                    '原始审核快照变化')
            if prior:
                prior_base = ROOT / prior['local_dataset'] / 'data'
                given, answer = (prior_base / given_name).read_bytes(), (prior_base / out_name).read_bytes()
            require(sha(given) == baseline[given_name] and sha(answer) == baseline[out_name],
                    '上一轮修正集与回执不符')
            repaired = repair_input(number, given)
            altered_inputs += repaired != given
            output = answer
            if repaired != given or number in (31415, 31435, 30236):
                result = subprocess.run(command, input=repaired,
                                        capture_output=True, timeout=120)
                require(result.returncode == 0, f'{number}: 自写参考失败')
                output = result.stdout
                require(0 < len(output) <= 2 * 1024 * 1024, '输出大小越界')
            for name, before, after in ((given_name, given, repaired), (out_name, answer, output)):
                (target / 'data' / name).write_bytes(after)
                if before != after:
                    changes.append({'filename': name, 'input': given_name, 'output': out_name,
                                    'before_sha256': sha(before), 'after_sha256': sha(after),
                                    'pair_before': {given_name: sha(given), out_name: sha(answer)},
                                    'pair_after': {given_name: sha(repaired), out_name: sha(output)}})
            cases.append({'input': str(target / 'data' / given_name),
                          'output': str(target / 'data' / out_name)})
        expected_inputs = {19964: 8, 19968: 7, 30825: 2, 30920: 2, 31415: 0, 31435: 0,
                           27945: 1, 28014: 1, 28191: 4, 28339: 1, 29905: 20,
                           21471: 19, 25563: 19, 25577: 1, 27946: 10, 30177: 1,
                           28187: 17, 28188: 14, 28189: 13, 28682: 20, 28696: 18,
                           25579: 12, 25685: 17, 28277: 1, 28680: 5,
                           21729: 1, 30236: 1, 28016: 6, 31241: 1, 31239: 18}
        require(altered_inputs == expected_inputs[number], '越界输入数量与审核证据不符')
        item = {'book': 'practice', 'id': str(number), 'global_number': number,
                'tests': True, 'test_count': len(cases), 'test_cases': cases}
        with patch.object(judge, 'catalog_item', return_value=item):
            receipt = judge.judge('practice', str(number), language, source, collect_case_times=True)
        require(receipt['status'] == 'Accepted', f'{number}: 本地复判未通过')
        require(receipt['timing_audit']['status'] == 'passed', f'{number}: 时限余量不足')
        group = {'global_number': number, 'evidence': str(evidence.relative_to(ROOT)),
                 'evidence_sha256': sha(evidence.read_bytes()), 'reference_sha256': sha(source.encode()),
                 'reference_source': source, 'reference_language': language,
                 'reference_file': reference.name, 'baseline_files': baseline, 'changes': changes,
                 'local_dataset': str(target.relative_to(ROOT)), 'local': sanitized(receipt),
                 'verified_legal_pairs': len(cases), 'repaired_inputs': altered_inputs}
        if number == 30236:
            group['reference_policy'] = {'rule':'操作数不能包含前导零；用户已明确确认',
                                         'original_reference_sha256':proof['sha256']}
        if number == 31239:
            group['input_policy'] = '仅移除首行第2～4项旧参数，保留N及后续数量表的全部字节。'
        if prior:
            group['prior_repair'] = {'path': str(prior_path.relative_to(ROOT)),
                                     'sha256': sha(prior_path.read_bytes())}
        save(target / 'SOURCE.json', group)
        groups.append((group, entry))
        print(number, '本地复判通过', len(cases), '对，修正文件', len(changes), flush=True)
    return groups


def run(batch, work, apply=False):
    work = work / f'batch{batch}'
    groups = prepare(batch, work)
    session = platform.oj_submit.Session().login()
    report = {'batch': batch, 'baseline': subprocess.check_output(
        ['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'procedure_sha256': sha(Path(__file__).read_bytes()),
        'rules_sha256': sha((ROOT / 'scripts/gmyhf_review_fixes.py').read_bytes()),
        'common_sha256': sha(Path(common.__file__).read_bytes()), 'applied': False,
        'policy': '修复明确越界输入和输出格式；保留原始及上一轮修正快照，不自动接入题库。',
        'changed_files': sum(len(g['changes']) for g, _ in groups), 'problems': [], 'uploads': []}
    # 全批预检完成后才写入；本地备份支持失败重试及回滚。
    for group, entry in groups:
        number = group['global_number']
        page = session._get(platform.oj_submit.HOST + f'/admin/problems/edit/?id={number}')
        audit_statement(page, entry)
        names = listed_files(page, number)
        directory = work / 'before' / str(number)
        directory.mkdir(parents=True, exist_ok=True)
        form = directory / 'form.sha256'
        fingerprint = form_sha(page)
        if form.exists():
            require(form.read_text() == fingerprint, f'{number}: 配置变化')
        else:
            form.write_text(fingerprint)
        audited = group['baseline_files']
        require({n for n in names if n.endswith(('.in', '.out'))} == {n for n in audited if n.endswith(('.in', '.out'))}, '测试文件清单变化')
        changes = {r['filename']: r for r in group['changes']}
        before = {}
        for name in names:
            live = platform.download(session, number, name)
            path = directory / name
            if not path.exists():
                require(name not in changes or sha(live) == changes[name]['before_sha256'],
                        f'{number}/{name}: 缺少原始平台备份')
                path.write_bytes(live)
            old = path.read_bytes()
            if name in audited:
                require(sha(old) == audited[name], f'{number}/{name}: 原件不符合审核哈希')
            expected = changes[name]['after_sha256'] if name in changes else sha(old)
            require(sha(live) in (sha(old), expected), f'{number}/{name}: 上游变化')
            before[name] = sha(old)
        group.update(form_sha256=fingerprint, before_files=before)
        report['problems'].append(group)
        print(number, '全文件预检及备份通过', len(names), flush=True)
    save(work / 'plan.json', report)
    if not apply:
        return
    for group, _ in groups:
        number = group['global_number']
        page = session._get(platform.oj_submit.HOST + f'/admin/problems/edit/?id={number}')
        require(form_sha(page) == group['form_sha256'] and
                listed_files(page, number) == sorted(group['before_files']), '写前题面配置或文件清单变化')
        for change in group['changes']:
            name = change['filename']
            # 输入和答案可以先后写入；仅接受本次计划绑定的旧/新字节。
            for pair_name, before_hash in change['pair_before'].items():
                current = sha(platform.download(session, number, pair_name))
                require(current in (before_hash, change['pair_after'][pair_name]), '写前测试对变化')
            payload = (ROOT / group['local_dataset'] / 'data' / name).read_bytes()
            require(sha(payload) == change['after_sha256'], '本地目标变化')
            live = sha(platform.download(session, number, name))
            require(live in (change['before_sha256'], change['after_sha256']), '写前答案变化')
            if live != change['after_sha256']:
                platform.upload(session, number, name, payload)
            require(sha(platform.download(session, number, name)) == change['after_sha256'], '上传回读不符')
            report['uploads'].append({'global_number': number, 'filename': name,
                                      'sha256': change['after_sha256'], 'verified': True})
            save(work / 'progress.json', report)
            print(number, name, '回读一致', flush=True)
    for group, _ in groups:
        number = group['global_number']
        page = session._get(platform.oj_submit.HOST + f'/admin/problems/edit/?id={number}')
        require(form_sha(page) == group['form_sha256'] and
                listed_files(page, number) == sorted(group['before_files']), '最终配置或清单变化')
        changes = {c['filename']: c['after_sha256'] for c in group['changes']}
        checked = {}
        for name, old_sha in group['before_files'].items():
            expected = changes.get(name, old_sha)
            observed = sha(platform.download(session, number, name))
            require(observed == expected, f'{number}/{name}: 最终回读不符')
            if name.endswith(('.in', '.out')):
                require(sha((ROOT / group['local_dataset'] / 'data' / name).read_bytes()) == observed,
                        '平台与本地字节不符')
            checked[name] = observed
        group.update(final_files=checked, form_unchanged=True, file_list_unchanged=True)
        print(number, '平台全部文件与本地答案最终核验通过', flush=True)
    report.update(applied=True, verified_at=datetime.now(timezone.utc).isoformat())
    save(work / 'result.json', report)
    save(ROOT / f'collab/gmyhf-review-fixes-batch{batch}.json', report)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', type=int, required=True, choices=BATCHES)
    parser.add_argument('--work', type=Path, default=Path('/tmp/gmyhf-review-fixes'))
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    run(args.batch, args.work, args.apply)
