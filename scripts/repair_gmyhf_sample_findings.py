#!/usr/bin/env python3
"""回填审核确认的样例、讲解与输入说明冲突；默认只备份和生成计划，--apply才写平台。"""
import argparse
from datetime import datetime, timezone
import html
import json
from pathlib import Path
import re
import subprocess
import sys

from repair_gmyhf_pending_answers import (ROOT, sha, save, require, listed_files,
                                         platform)

import gmyhf_statement_fixes as statement_rules
from gmyhf_statement_fixes import recovered_samples, changed_form

FOLLOWUP = {25685:12,29329:13,30125:14,31303:15}

PROBLEMS = {30205:14, 30176:14, 30916:15, 28698:13, 29951:14, 30078:14, 25576:11}
FIELDS = {'description','input','output','hint','sampleInput','sampleOutput'}


def fingerprint(fields):
    return sha(json.dumps(platform.normalized(fields), ensure_ascii=False, sort_keys=True).encode())


def submitted_form(fields):
    """本批后台hint回读做实体转义；解码一次，其余HTML字段保持原文。"""
    return {key:html.unescape(value) if key == 'hint' else value
            for key,value in fields.items()}


def sample_inputs(number, fields):
    if number in FOLLOWUP:
        return recovered_samples(number, fields)
    if number == 25576:
        result = []
        for i, key in ((1,'sampleInput'),(2,'sampleOutput')):
            match = re.search(rf'Sample Input{i}:\s*(.*?)\s*Sample Output{i}:',fields[key],re.S)
            require(match is not None,'乘法游戏样例标签变化')
            result.append(match[1].strip())
        return result
    if number == 30078:
        pieces = re.split(r'sample[12]:',fields['sampleInput'],flags=re.I)
        require(len(pieces)==3 and not pieces[0].strip(),'课程作业样例标签变化')
        return [p.strip() for p in pieces[1:]]
    return [fields['sampleInput'].strip()]


def replace_line(text, old, new):
    result, count = re.subn(r'(?m)^'+re.escape(old)+r'(?=\r?$)',new,text)
    require(count==1,'待修正样例答案行不唯一')
    return result


def repaired_form(number, fields, answers):
    result = dict(fields)
    if number in FOLLOWUP:
        result = changed_form(number, fields, answers)
    elif number == 25576:
        require(len(answers)==2 and answers[1]=='15','乘法游戏第二样例变化')
        result['sampleInput'] = replace_line(result['sampleInput'],'5',answers[0])
        old = '[2,5]->[2]'
        require(result['sampleOutput'].count(old)==1,'乘法游戏解释变化')
        result['sampleOutput'] = result['sampleOutput'].replace(old,'[2,5]->[5]')
    else:
        old = {30205:'6',30176:'10',30916:'6',28698:'900',29951:'2',30078:'NO'}[number]
        result['sampleOutput'] = replace_line(result['sampleOutput'],old,answers[-1])
        if number == 30205:
            old_hint = '贪心+双指针'
            require(result['hint'].count(old_hint)==1,'显存优化提示变化')
            result['hint'] = result['hint'].replace(old_hint,
                '先求全局最大加载价值，再按临界分数统计最优配置；使用二项式计数，全程采用精确整数运算。')
    changed = {k for k in fields if fields[k]!=result[k]}
    followup_allowed = {25685:{'sampleInput','sampleOutput'},29329:{'input'},30125:{'input'},31303:{'sampleInput'}}
    allowed = followup_allowed[number] if number in FOLLOWUP else {'sampleInput','sampleOutput'} if number==25576 else (
        {'sampleOutput','hint'} if number==30205 else {'sampleOutput'})
    require(changed==allowed,'修改字段不符合本题修复计划')
    return result


def compute_samples(number, entry, fields, target):
    proof = entry['authored_reference']
    require(sha(proof['source'].encode())==proof['sha256'],'自写参考哈希变化')
    target.mkdir(parents=True,exist_ok=True)
    reference = target/'reference.py'
    reference.write_text(proof['source'])
    inputs = sample_inputs(number,fields)
    checks = entry['checks']['answers']['official_sample_checks']
    require(len(inputs)==len(checks) or (number==31303 and len(inputs)==1 and not checks),'样例组数与审核不符')
    if number==31303:
        checks=[{'statement_output_sha256':sha(fields['sampleOutput'].strip().encode())}]
    answers, receipts = [], []
    for given,check in zip(inputs,checks):
        result = subprocess.run([sys.executable,'-I',str(reference)],input=given.encode(),
                                capture_output=True,timeout=60)
        require(result.returncode==0,'样例参考运行失败')
        answer = result.stdout.decode().strip()
        expected = check['statement_output_sha256'] if number == 31303 else check['oracle_sha256']
        require(sha(answer.encode())==expected,'样例复算与独立审核或原样例输出不符')
        answers.append(answer)
        receipts.append({'input_sha256':sha(given.encode()),'answer_sha256':sha(answer.encode()),
                         'audit_matches':number != 31303,
                         'restored_source_matches_statement_output':number == 31303})
    return answers, receipts


def run(work, apply=False, batch=4):
    session = platform.oj_submit.Session().login()
    require(batch in (4,8),'未知题面修复批次')
    report = {'batch':batch,'recipes_sha256':sha(Path(statement_rules.__file__).read_bytes()),'procedure_sha256':sha(Path(__file__).read_bytes()),'applied':False,
              'baseline':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
              'policy':'只修复所选批次已核定的题面冲突；全文件备份和最终回读，不改测试数据或题目配置。',
              'problems':[]}
    plans = []
    for number,audit_batch in (PROBLEMS if batch==4 else FOLLOWUP).items():
        evidence = ROOT/f'collab/gmyhf-pending-batch{audit_batch}-review.json'
        entry = next(e for e in json.loads(evidence.read_text())['entries'] if e['global_number']==number)
        page = session._get(platform.oj_submit.HOST+f'/admin/problems/edit/?id={number}')
        observed = platform.parse_form(page)
        directory = work/'before'/str(number)
        directory.mkdir(parents=True,exist_ok=True)
        form_path = directory/'form.json'
        (directory/'files').mkdir(exist_ok=True)
        if not form_path.exists():
            hashes = {k:sha(html.unescape(observed[k]).encode()) for k in FIELDS}
            require(hashes==entry['checks']['statement']['field_sha256'],'审核后题面变化')
            save(form_path,observed)
        before = json.loads(form_path.read_text())
        require({k:sha(html.unescape(before[k]).encode()) for k in FIELDS}==entry['checks']['statement']['field_sha256'],
                '原题面备份与审核不符')
        local = ROOT/f'data/openjudge/tests/admin_review_statements/{number}'
        answers,checks = compute_samples(number,entry,before,local)
        after = repaired_form(number,before,answers)
        require(fingerprint(observed) in (fingerprint(before),fingerprint(after)),'题面或配置出现未审核变化')
        names = listed_files(page,number)
        audited = {r['filename']:r['sha256'] for r in entry['checks']['readback']['files']}
        if number in (30205,25685):
            prior = ROOT/('collab/gmyhf-answer-repairs-batch2.json' if number==30205 else 'collab/gmyhf-review-fixes-batch7.json')
            group = next(g for g in json.loads(prior.read_text())['problems'] if g['global_number']==number)
            audited.update(group['final_files'])
        require({n for n in names if n.endswith(('.in','.out'))}=={n for n in audited if n.endswith(('.in','.out'))},
                '测试文件清单变化')
        files = {}
        for name in names:
            live = platform.download(session,number,name)
            path = directory/'files'/name
            if not path.exists():path.write_bytes(live)
            old = path.read_bytes()
            require(live==old,'平台文件与备份变化')
            if name in audited:require(sha(live)==audited[name],'平台数据与审核或已修正答案不符')
            files[name] = sha(live)
        save(local/'fields.json',after)
        group = {'global_number':number,'evidence':str(evidence.relative_to(ROOT)),
                 'evidence_sha256':sha(evidence.read_bytes()),'reference_sha256':entry['authored_reference']['sha256'],
                 'samples':checks,'before_form_sha256':fingerprint(before),'after_form_sha256':fingerprint(after),
                 'changed_fields':{k:{'before_sha256':sha(before[k].encode()),'after_sha256':sha(after[k].encode())}
                                   for k in FIELDS if before[k]!=after[k]},
                 'before_files':files,'local_statement':str(local.relative_to(ROOT))}
        if number in (30205,25685):group['prior_repair_sha256']=sha(prior.read_bytes())
        report['problems'].append(group)
        plans.append((group,before,after))
        print(number,'样例复算及全文件预检通过',len(files),flush=True)
    save(work/'plan.json',report)
    if not apply:return
    for group,before,after in plans:
        number = group['global_number']
        page = session._get(platform.oj_submit.HOST+f'/admin/problems/edit/?id={number}')
        current = platform.parse_form(page)
        require(fingerprint(current) in (fingerprint(before),fingerprint(after)),'写前题面或配置变化')
        require(listed_files(page,number)==sorted(group['before_files']),'写前文件清单变化')
        if fingerprint(current)!=fingerprint(after):
            session._post(platform.oj_submit.HOST+'/api/global-problem/modify/',submitted_form(after))
        current = platform.parse_form(session._get(platform.oj_submit.HOST+f'/admin/problems/edit/?id={number}'))
        require(fingerprint(current)==fingerprint(after),'题面写后回读不符')
        print(number,'题面写后回读一致',flush=True)
    for group,before,after in plans:
        number = group['global_number']
        page = session._get(platform.oj_submit.HOST+f'/admin/problems/edit/?id={number}')
        require(fingerprint(platform.parse_form(page))==fingerprint(after),'最终题面回读不符')
        require(listed_files(page,number)==sorted(group['before_files']),'最终文件清单变化')
        final = {name:sha(platform.download(session,number,name)) for name in group['before_files']}
        require(final==group['before_files'],'题面修复期间后台文件变化')
        local = ROOT/group['local_statement']
        require(fingerprint(json.loads((local/'fields.json').read_text()))==fingerprint(after),'本地题面与平台不符')
        group.update(final_files=final,only_allowed_fields_changed=True,local_matches=True)
        save(local/'SOURCE.json',group)
        print(number,'本地题面与平台全部文件最终核验通过',flush=True)
    report.update(applied=True,verified_at=datetime.now(timezone.utc).isoformat())
    save(work/'result.json',report)
    output = 'gmyhf-sample-repairs.json' if batch==4 else 'gmyhf-statement-repairs-batch8.json'
    save(ROOT/'collab'/output,report)


if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch',type=int,choices=(4,8),default=4)
    parser.add_argument('--work',type=Path,default=Path('/tmp/gmyhf-sample-repairs'))
    parser.add_argument('--apply',action='store_true')
    args = parser.parse_args()
    run(args.work,args.apply,args.batch)
