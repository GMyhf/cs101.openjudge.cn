#!/usr/bin/env python3
"""只读核对课程路由与31381排列语义；--submit才提交选定的自产判题探针。

不改题面、测试数据、配置、题库绑定或既有valid()；不读取平台附件源码。
课程页需登录，仅记录当前会话可见映射，不据此声明匿名可见或自动接入。
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import html
import json
from pathlib import Path
import re

import repair_gmyhf_pending_answers as common

COURSE = '2026fallcs101testing'
NUMBER = 31381
ROUTE = 'E31381'
FIELDS = ('description','input','output','hint','sampleInput','sampleOutput')


def course_routes(page):
    """保留字母前缀与别名，只跟随同课程下的题目路由。"""
    matches = re.findall(r'href=[\"\x27](/'+COURSE+r'/[A-Za-z0-9_]+/)[\"\x27]',page)
    navigation = {f'/{COURSE}/{name}/' for name in ('ranking','status','clarify')}
    return sorted(set(matches)-navigation)


def global_number(page):
    matches = re.findall(r'<dt>\s*全局题号\s*</dt>\s*<dd>\s*(\d+)\s*</dd>',page)
    common.require(len(matches)==1,'课程页没有唯一明示的全局题号')
    return int(matches[0])


def is_permutation(given, actual):
    """题面模型：仅去掉行结束符，保留空格及字符重复次数。"""
    return Counter(given.rstrip('\r\n')) == Counter(actual.rstrip('\r\n'))


def probe_sources():
    prefix="import sys\ns = sys.stdin.read().rstrip('\\r\\n')\n"
    return {'identity':prefix+'print(s)\n',
            'reverse':prefix+'print(s[::-1])\n',
            'sorted':prefix+"print(''.join(sorted(s)))\n",
            'append_invalid':prefix+"print(s + '~')\n",
            'replace_invalid':prefix+"print(chr(ord(s[0]) ^ 1) + s[1:] if s else '~')\n",
            'drop_invalid':prefix+"print(s[1:] if s else '~')\n"}


def run(work, submit=False, probes=None):
    work.mkdir(parents=True,exist_ok=True)
    session=common.platform.oj_submit.Session().login()
    index=session._get(common.platform.oj_submit.HOST+f'/{COURSE}/')
    (work/'course-index.html').write_text(index)
    mappings=[]
    for route in course_routes(index):
        page=session._get(common.platform.oj_submit.HOST+route)
        number=global_number(page)
        (work/(route.rstrip('/').rsplit('/',1)[-1]+'.html')).write_text(page)
        mappings.append({'route':route,'global_number':number,'page_sha256':common.sha(page.encode())})
    common.require(any(row['route']==f'/{COURSE}/{ROUTE}/' and row['global_number']==NUMBER for row in mappings),'SPJ课程路由与全局题号不符')
    evidence=common.ROOT/'collab/gmyhf-pending-batch15-review.json'
    entry=next(e for e in json.loads(evidence.read_text())['entries'] if e['global_number']==NUMBER)
    before=session._get(common.platform.oj_submit.HOST+f'/admin/problems/edit/?id={NUMBER}')
    common.audit_statement(before,entry)
    names=common.listed_files(before,NUMBER)
    expected={row['filename']:row['sha256'] for row in entry['checks']['readback']['files']}
    common.require(names==sorted(expected),'SPJ题后台文件清单变化')
    hashes={};payloads={}
    for name in names:
        payload=common.platform.download(session,NUMBER,name)
        common.require(common.sha(payload)==expected[name],'SPJ题后台数据已变化')
        (work/name).write_bytes(payload);hashes[name]=common.sha(payload);payloads[name]=payload
    common.require(names==['0.in','0.out'],'SPJ探针范围只绑定原一对数据')
    given=payloads['0.in'].decode();gold=payloads['0.out'].decode()
    results=[]
    sources=probe_sources()
    selected=list(sources) if probes is None else probes
    common.require(selected and len(set(selected))==len(selected) and set(selected)<=set(sources),'未知或重复探针')
    if submit:
        for name in selected:
            source=sources[name]
            solution=session.submit(ROUTE,source,'Python3',group=COURSE)
            receipt=session.poll(solution,group=COURSE)
            wanted='Wrong Answer' if name.endswith('_invalid') else 'Accepted'
            results.append({'probe':name,'source':source,'source_sha256':common.sha(source.encode()),
                            'expected_verdict':wanted,'observed':receipt,
                            'matches_statement_expectation':receipt['verdict']==wanted,
                            'url':f'http://cs101.openjudge.cn/{COURSE}/solution/{solution}/'})
            print(name,receipt['verdict'],solution,flush=True)
    after=session._get(common.platform.oj_submit.HOST+f'/admin/problems/edit/?id={NUMBER}')
    common.require(common.form_sha(after)==common.form_sha(before) and common.listed_files(after,NUMBER)==names,'探针期间后台表单或清单变化')
    for name,digest in hashes.items():
        common.require(common.sha(common.platform.download(session,NUMBER,name))==digest,'探针期间测试数据变化')
    report={'scope':'课程的会话可见映射及31381实际判题探针，不代表匿名公开映射或完整SPJ协议。',
            'checked_at':datetime.now(timezone.utc).isoformat(),'course':COURSE,
            'index_sha256':common.sha(index.encode()),'routes':mappings,
            'global_numbers':sorted({row['global_number'] for row in mappings}),
            'anonymous_visibility_verified':False,'catalog_changed':False,
            'evidence':str(evidence.relative_to(common.ROOT)),'evidence_sha256':common.sha(evidence.read_bytes()),
            'global_number':NUMBER,'readback_files':hashes,'form_sha256':common.form_sha(before),
            'stored_output_is_permutation_certificate':is_permutation(given,gold),
            'requested_probes':selected if submit else [],'probes':results,'all_probes_match_statement':bool(results) and all(row['matches_statement_expectation'] for row in results),
            'test_data_writes':0,'statement_writes':0,'configuration_writes':0,'submission_writes':len(results),
            'preserve_existing_spj_exclusion':True,'procedure_sha256':common.sha(Path(__file__).read_bytes())}
    common.save(common.ROOT/'collab/gmyhf-course-spj-recheck.json',report)
    print('课程路由',len(mappings),'全局题号',len(report['global_numbers']),'后台数据及配置保持',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work',type=Path,default=Path('/tmp/gmyhf-course-spj-recheck'))
    parser.add_argument('--submit',action='store_true')
    parser.add_argument('--probe',nargs='+',choices=tuple(probe_sources()),help='只提交指定探针，避免重复已完成的测试')
    args=parser.parse_args();run(args.work,args.submit,args.probe)
