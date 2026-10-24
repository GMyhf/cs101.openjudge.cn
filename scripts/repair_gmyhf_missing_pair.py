#!/usr/bin/env python3
"""从已核验的错名原件补齐孤立答案的输入；只允许27934/3.in这一项新增。"""
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch
import gmyhf_review_fixes as rules
import repair_gmyhf_pending_answers as common
from repair_gmyhf_pending_answers import ROOT,sha,save,require,listed_files,audit_statement,sanitized,platform,judge

NUMBER=27934
NEW_INPUT='3.in'
OUTPUT='3.out'


def configuration_sha(page):
    fields=platform.normalized(platform.parse_form(page))
    fields.pop('filenames[3.in]',None)
    return sha(json.dumps(fields,ensure_ascii=False,sort_keys=True).encode())


def prepare():
    evidence=ROOT/'collab/gmyhf-27934-pairing-review.json'
    review=json.loads(evidence.read_text())
    entry=next(e for e in json.loads(evidence.read_text())['entries'] if e['global_number']==NUMBER)
    require([r['filename'] for r in entry['checks']['pairing']['unpaired']]==[OUTPUT],'孤立文件与审核不符')
    proof=entry['authored_reference'];source=proof['source']
    require(sha(source.encode())==proof['sha256'] and proof.get('language','python3')=='python3','自写参考来源或语言不符')
    baseline={r['filename']:r['sha256'] for r in entry['checks']['readback']['files']}
    require(NEW_INPUT not in baseline and OUTPUT in baseline,'审核未证明缺少目标输入')
    target=ROOT/f'data/openjudge/tests/admin_review_repaired/{NUMBER}'
    (target/'data').mkdir(parents=True,exist_ok=True)
    for name,digest in baseline.items():
        raw=(ROOT/review['local_snapshot']/name).read_bytes()
        require(sha(raw)==digest,'原始审核快照变化')
        (target/'data'/name).write_bytes(raw)
    given=rules.validate_missing_deque_input((target/'data/3,in').read_bytes())
    reference=target/'reference.py';reference.write_text(source)
    result=subprocess.run([sys.executable,'-I',str(reference)],input=given,capture_output=True,timeout=120)
    require(result.returncode==0 and 0<len(result.stdout)<=2*1024*1024,'自产输入参考运行失败或输出越界')
    answer=result.stdout
    require(answer==(target/'data'/OUTPUT).read_bytes(),'错名输入与原孤立答案不匹配')
    (target/'data'/NEW_INPUT).write_bytes(given)
    changes=[{'filename':NEW_INPUT,'before_sha256':None,'after_sha256':sha(given)}]
    records=entry['checks']['answers']['files']
    cases=[{'input':str(target/'data'/r['input']),'output':str(target/'data'/r['output'])} for r in records]
    cases.append({'input':str(target/'data'/NEW_INPUT),'output':str(target/'data'/OUTPUT)})
    item={'book':'practice','id':str(NUMBER),'global_number':NUMBER,'tests':True,'test_count':len(cases),'test_cases':cases}
    with patch.object(judge,'catalog_item',return_value=item):
        receipt=judge.judge('practice',str(NUMBER),'python3',source,collect_case_times=True)
    require(receipt['status']=='Accepted' and receipt['timing_audit']['status']=='passed','本地全量复判或75%余量未通过')
    group={'global_number':NUMBER,'evidence':str(evidence.relative_to(ROOT)),'evidence_sha256':sha(evidence.read_bytes()),
           'reference_source':source,'reference_sha256':proof['sha256'],'local_dataset':str(target.relative_to(ROOT)),
           'baseline_files':baseline,'changes':changes,'added_files':{NEW_INPUT:sha(given)},'local':sanitized(receipt),
           'verified_legal_pairs':len(cases),'repaired_inputs':1,
           'input_policy':'将已核验的3,in原样复制为3.in；原答案和全部原文件保持，错名原件不删除，附件不执行。'}
    save(target/'SOURCE.json',group)
    return group,entry


def run(work,apply=False):
    group,entry=prepare();baseline=group['baseline_files'];old_names=sorted(baseline);final_names=sorted([*baseline,NEW_INPUT])
    target=ROOT/group['local_dataset'];after={c['filename']:c['after_sha256'] for c in group['changes']}
    expected={**baseline,**after};session=platform.oj_submit.Session().login()
    page=session._get(platform.oj_submit.HOST+f'/admin/problems/edit/?id={NUMBER}');audit_statement(page,entry)
    names=listed_files(page,NUMBER);fingerprint=configuration_sha(page)
    require(names in (old_names,final_names),'出现未经审核的文件增删')
    binding={'evidence_sha256':group['evidence_sha256'],'procedure_sha256':sha(Path(__file__).read_bytes()),
             'rules_sha256':sha(Path(rules.__file__).read_bytes()),'configuration_sha256':fingerprint,
             'original_files':baseline,'added_files':group['added_files']}
    directory=work/'before'/str(NUMBER);directory.mkdir(parents=True,exist_ok=True)
    binding_path=directory/'absence.json'
    if binding_path.exists():require(json.loads(binding_path.read_text())==binding,'缺失状态备份与当前计划或配置变化')
    else:require(names==old_names,'没有原始缺失证明，不接管已经存在的3.in')
    if NEW_INPUT in names:
        require(sha(platform.download(session,NUMBER,NEW_INPUT))==expected[NEW_INPUT],'新增输入不是本计划字节')
    for name,digest in baseline.items():
        live=platform.download(session,NUMBER,name);backup=directory/name
        if not backup.exists():
            require(sha(live)==digest,'缺少原始文件备份，禁止接管已变化文件');backup.write_bytes(live)
        require(sha(backup.read_bytes())==digest,'原始文件备份不符')
        require(sha(live) in (digest,expected[name]),'已有文件出现未审核变化')
    if not binding_path.exists():save(binding_path,binding)
    report={'batch':14,'baseline':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            'procedure_sha256':binding['procedure_sha256'],'rules_sha256':binding['rules_sha256'],
            'common_sha256':sha(Path(common.__file__).read_bytes()),'applied':False,'problems':[group],
            'policy':'仅为27934从错名原件恢复3.in；原答案和全部原文件保持，不改题面或配置。','uploads':[]}
    group.update(before_files=baseline,configuration_sha256=fingerprint,absence_binding_sha256=sha(binding_path.read_bytes()))
    save(work/'plan.json',report)
    if not apply:return
    for name in (NEW_INPUT,):
        page=session._get(platform.oj_submit.HOST+f'/admin/problems/edit/?id={NUMBER}')
        require(configuration_sha(page)==fingerprint and listed_files(page,NUMBER) in (old_names,final_names),'写前配置或清单变化')
        current_names=listed_files(page,NUMBER)
        if NEW_INPUT in current_names:
            require(sha(platform.download(session,NUMBER,NEW_INPUT))==expected[NEW_INPUT],
                    '写前配套输入变化')
        payload=(target/'data'/name).read_bytes();require(sha(payload)==expected[name],'本地目标在审核后变化')
        if name not in current_names:
            require(name==NEW_INPUT,'出现计划外缺失');platform.upload(session,NUMBER,name,payload)
        else:
            observed=sha(platform.download(session,NUMBER,name))
            require(observed in (baseline.get(name),expected[name]),'写前文件变化')
            if observed!=expected[name]:platform.upload(session,NUMBER,name,payload)
        require(sha(platform.download(session,NUMBER,name))==expected[name],'上传后回读不符')
        report['uploads'].append({'filename':name,'sha256':expected[name],'verified':True})
        save(work/'progress.json',report)
        print(NUMBER,name,'回读一致',flush=True)
    page=session._get(platform.oj_submit.HOST+f'/admin/problems/edit/?id={NUMBER}')
    require(configuration_sha(page)==fingerprint and listed_files(page,NUMBER)==final_names,'最终配置或清单变化')
    final={}
    for name,digest in expected.items():
        raw=platform.download(session,NUMBER,name);require(sha(raw)==digest,'最终全文件回读不符')
        require(sha((target/'data'/name).read_bytes())==digest,'本地与平台不符');final[name]=digest
    group.update(final_files=final,form_unchanged=False,configuration_unchanged=True,file_list_unchanged=False,only_expected_files_added=True)
    report.update(applied=True,verified_at=datetime.now(timezone.utc).isoformat())
    save(work/'result.json',report);save(ROOT/'collab/gmyhf-review-fixes-batch14.json',report)
    print(NUMBER,'新增缺失输入及全部文件最终核验通过',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--work',type=Path,default=Path('/tmp/gmyhf-missing-pair-batch14'));parser.add_argument('--apply',action='store_true');args=parser.parse_args();run(args.work,args.apply)
