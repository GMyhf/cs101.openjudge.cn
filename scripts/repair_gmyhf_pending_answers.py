#!/usr/bin/env python3
"""回填逐题审核确认的错误答案；默认只备份和生成计划，--apply 才写平台。

原始 admin_download 快照保留，修正后的完整本地数据放在被忽略的
admin_repaired/；入库的报告绑定审核证据、自写参考及所有文件哈希。
不修改输入、题面、附件、题库绑定或既有 valid() 契约。
"""
import argparse
from datetime import datetime, timezone
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess
import sys
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

import sync_gmyhf_followup as platform

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import judge

BATCHES = {1: {19964: 16, 19966: 16}, 2: {30205: 14},
           3: {30827: 15, 30828: 15}, 4: {20124: 11, 20126: 11, 23665: 11}}
COUNTS = {1: 3, 2: 11, 3: 51, 4: 22}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(path)


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def listed_files(page, number):
    names = set()
    for href in re.findall(r'href="(/admin/download[^\"]*)"', page):
        query = parse_qs(urlparse(html.unescape(href)).query)
        require(query.get('problem_id') == [str(number)], '下载链接题号不符')
        name = query['filename'][0]
        require(name not in ('', '.', '..') and len(name) <= 200 and
                not any(ord(c) < 32 or c in '/\\' for c in name), '非法文件名')
        names.add(name)
    require(names, '未获得文件清单')
    return sorted(names)


def form_sha(page):
    fields = platform.normalized(platform.parse_form(page))
    return sha(json.dumps(fields, ensure_ascii=False, sort_keys=True).encode())


def audit_statement(page, entry):
    fields = {name: html.unescape(value) for name, value in re.findall(
        r'<textarea[^>]*name=[\"\x27]([^\"\x27]+)[\"\x27][^>]*>(.*?)</textarea>', page, re.S)}
    observed = {name: sha(value.encode()) for name, value in fields.items()}
    require(observed == entry['checks']['statement']['field_sha256'],
            f'{entry["global_number"]}: 审核后题面变化，停止回填')


def sanitized(receipt):
    result = dict(receipt)
    for key in ('actual_output', 'expected_output', 'failing_input', 'message'):
        if key in result:
            raw = str(result.pop(key)).encode()
            result[key + '_sha256'] = sha(raw)
            result[key + '_bytes'] = len(raw)
    return result


def prepare(batch, work):
    groups = []
    for number, audit_batch in BATCHES[batch].items():
        evidence = ROOT / f'collab/gmyhf-pending-batch{audit_batch}-review.json'
        entry = next(e for e in json.loads(evidence.read_text())['entries']
                     if e['global_number'] == number)
        proof = entry['authored_reference']
        require(sha(proof['source'].encode()) == proof['sha256'], '参考源码哈希不符')
        base = ROOT / f'data/openjudge/tests/admin_download/{number}'
        target = ROOT / f'data/openjudge/tests/admin_repaired/{number}'
        (target / 'data').mkdir(parents=True, exist_ok=True)
        reference = target / 'reference.py'
        reference.write_text(proof['source'])
        files = []
        valid_cases = []
        for record in entry['checks']['answers']['files']:
            given = (base / record['input']).read_bytes()
            old = (base / record['output']).read_bytes()
            require(sha(given) == record['input_sha256'] and
                    sha(old) == record['output_sha256'], f'{number}: 原始快照变化')
            payload = old
            if record['matches'] is False:
                result = subprocess.run([sys.executable, '-I', str(reference)],
                                        input=given, capture_output=True, timeout=120)
                require(result.returncode == 0, f'{number}: 自写参考运行失败')
                payload = result.stdout
                require(0 < len(payload) <= 2 * 1024 * 1024, '答案大小越界')
                require(payload.split() != old.split(), '拟修正答案未产生实际差异')
                files.append({'input': record['input'], 'output': record['output'],
                              'input_sha256': sha(given), 'before_sha256': sha(old),
                              'after_sha256': sha(payload), 'bytes': len(payload)})
            (target / 'data' / record['input']).write_bytes(given)
            (target / 'data' / record['output']).write_bytes(payload)
            if record['matches'] is not None:
                valid_cases.append({'input': str(target / 'data' / record['input']),
                                    'output': str(target / 'data' / record['output'])})
        item = {'book': 'practice', 'id': str(number), 'global_number': number,
                'tests': True, 'test_count': len(valid_cases), 'test_cases': valid_cases}
        with patch.object(judge, 'catalog_item', return_value=item):
            receipt = judge.judge('practice', str(number), 'python3', proof['source'],
                                  collect_case_times=True)
        require(receipt['status'] == 'Accepted', f'{number}: 修正后本地复判未通过')
        group = {'global_number': number, 'evidence': str(evidence.relative_to(ROOT)),
                 'evidence_sha256': sha(evidence.read_bytes()),
                 'reference_sha256': proof['sha256'], 'changes': files,
                 'local_dataset': str(target.relative_to(ROOT)),
                 'local': sanitized(receipt), 'verified_legal_pairs': len(valid_cases),
                 'unresolved_inputs': [r['input'] for r in entry['checks']['answers']['files']
                                       if r['matches'] is None]}
        save(target / 'SOURCE.json', group)
        groups.append((group, entry))
        print(number, '本地复判通过', len(valid_cases), '对，拟修正', len(files), '份答案', flush=True)
    require(sum(len(g['changes']) for g, _ in groups) == COUNTS[batch], '修正数量与授权范围不符')
    return groups


def run(batch, work, apply=False):
    work = work / f'batch{batch}'
    groups = prepare(batch, work)
    session = platform.oj_submit.Session().login()
    report = {'batch': batch, 'baseline': subprocess.check_output(
        ['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'procedure_sha256': sha(Path(__file__).read_bytes()), 'applied': False,
        'policy': '只回填审核为错误的答案；原始快照不变，修正数据在admin_repaired；'
                  '逐文件写前核对、写后回读，所有输入附件及题面配置保持；不自动接入题库。',
        'answer_files': COUNTS[batch], 'problems': [], 'uploads': []}
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
        audited = {r['filename']: r['sha256'] for r in entry['checks']['readback']['files']}
        require({n for n in names if n.endswith(('.in', '.out'))} == set(audited), '测试文件清单变化')
        changes = {r['output']: r for r in group['changes']}
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
            name = change['output']
            # 同时再次绑定输入，避免把答案写入审核后变化的测试。
            require(sha(platform.download(session, number, change['input'])) == change['input_sha256'],
                    '写前输入变化')
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
        changes = {c['output']: c['after_sha256'] for c in group['changes']}
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
    save(ROOT / f'collab/gmyhf-answer-repairs-batch{batch}.json', report)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', type=int, required=True, choices=BATCHES)
    parser.add_argument('--work', type=Path, default=Path('/tmp/gmyhf-pending-answer-repairs'))
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    run(args.batch, args.work, args.apply)
