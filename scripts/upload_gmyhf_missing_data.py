#!/usr/bin/env python3
"""补齐已审核11题的缺失平台文件；默认只计划，--apply才上传并逐文件回读。

仅允许原表单保持不变、现有文件属于本批且字节一致的题；不删文件、不改题面或课程。
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import repair_gmyhf_pending_answers as common
import gmyhf_io_benchmark_data as benchmark

NORMAL=(27207,29337,29893,29894,31178,31200)
BENCHMARK=benchmark.NUMBERS


def fields_digest(fields):
    fields={k:v for k,v in fields.items() if not k.startswith('filenames[')}
    return common.sha(json.dumps(common.platform.normalized(fields),ensure_ascii=False,sort_keys=True).encode())


def file_list(page,number):
    try:return common.listed_files(page,number)
    except ValueError as exc:
        if str(exc)!='未获得文件清单':raise
        return []


def sync_problem(session,number,paths,baseline_sha,apply=False):
    common.require(number in NORMAL+BENCHMARK,'不在授权补数据题号内')
    names={p.name:p for p in paths}
    expected_names={f'{i}.{ext}' for i in range(21 if number in NORMAL else 1) for ext in ('in','out')}
    common.require(set(names)==expected_names,'本批测试文件不完整')
    hashes={name:benchmark.digest(path) for name,path in names.items()}
    host=common.platform.oj_submit.HOST;url=host+f'/admin/problems/edit/?id={number}'
    page=session._get(url);fields=common.platform.parse_form(page)
    common.require(fields.get('problemId')==str(number),'后台全局题号不符')
    common.require(fields_digest(fields)==baseline_sha,'审核后表单变化，停止补数据')
    existing=file_list(page,number)
    common.require(set(existing)<=set(names),'出现未审核文件，停止补数据')
    for name in existing:
        common.require(common.sha(common.platform.download(session,number,name))==hashes[name],
                       '平台已有同名文件与拟上传内容不同')
    missing=sorted(set(names)-set(existing))
    report={'global_number':number,'applied':False,'baseline_form_sha256':baseline_sha,
            'pairs':len(names)//2,'before_files':existing,'planned_new_files':missing,
            'files':[{'filename':name,'bytes':names[name].stat().st_size,'sha256':hashes[name]} for name in sorted(names)]}
    if not apply:return report
    # 每份上传前重新确认表单及清单，禁止夹带其他变更；每次成功后立即回读正文。
    known=set(existing)
    for name in missing:
        page=session._get(url);current=common.platform.parse_form(page)
        common.require(fields_digest(current)==baseline_sha and set(file_list(page,number))==known,
                       '写入前平台配置或清单变化')
        common.platform.upload(session,number,name,names[name].read_bytes())
        known.add(name)
        common.require(common.sha(common.platform.download(session,number,name))==hashes[name],
                       '新增文件回读哈希不符')
    page=session._get(url);current=common.platform.parse_form(page)
    common.require(fields_digest(current)==baseline_sha and set(file_list(page,number))==set(names),
                   '上传后表单或文件清单不一致')
    selected=dict(current)
    for name in names:selected[f'filenames[{name}]']='1'
    selection_written=selected!=current
    if selection_written:
        result=json.loads(session._post(host+'/api/global-problem/modify/',selected))
        common.require(result.get('result')=='SUCCESS','保存测试文件选择失败')
    final=common.platform.parse_form(session._get(url))
    common.require(fields_digest(final)==baseline_sha,'最终题面或配置变化')
    common.require(all(final.get(f'filenames[{name}]')=='1' for name in names),'测试文件未全部选中')
    common.require({k:v for k,v in final.items() if k.startswith('filenames[')}==
                   {f'filenames[{name}]':'1' for name in names},'最终选中文件清单不符')
    for name in names:
        common.require(common.sha(common.platform.download(session,number,name))==hashes[name],
                       '最终回读文件哈希不符')
    report.update(applied=True,selection_written=selection_written,all_files_selected=True,
                  all_files_readback_matched=True,statement_and_limits_unchanged=True)
    return report


def run(batch,work,apply=False):
    work.mkdir(parents=True,exist_ok=True)
    evidence=json.loads((ROOT/'collab/gmyhf-placeholder-exclusions.json').read_text())
    baseline={e['global_number']:e['form_sha256'] for e in evidence['entries']}
    numbers=NORMAL if batch=='normal' else BENCHMARK
    if batch=='benchmark':benchmark.build(work/'benchmark-data')
    session=common.platform.oj_submit.Session().login()
    report={'created_at':datetime.now(timezone.utc).isoformat(),'batch':batch,'applied':apply,
            'statement_writes':0,'course_writes':0,'deleted_files':0,'problems':[]}
    for number in numbers:
        directory=(ROOT/'data/openjudge/tests'/('20000-29982' if number<30000 else '30000-')/f'{number}_made/data'
                   if batch=='normal' else work/'benchmark-data')
        paths=sorted(p for p in directory.iterdir() if p.suffix in ('.in','.out'))
        result=sync_problem(session,number,paths,baseline[number],apply)
        report['problems'].append(result)
        common.save(work/(batch+('-receipt.json' if apply else '-plan.json')),report)
        print(number,'已回读' if apply else '计划',result['pairs'],'组，新增',len(result['planned_new_files']),'文件',flush=True)
    report['procedure_sha256']=common.sha(Path(__file__).read_bytes())
    common.save(work/(batch+('-receipt.json' if apply else '-plan.json')),report)
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch',choices=('normal','benchmark'),required=True)
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--apply',action='store_true')
    args=parser.parse_args();run(args.batch,args.work,args.apply)


if __name__=='__main__':main()
