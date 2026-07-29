#!/usr/bin/env python3
"""Run a T-028 round through the real local judge and update its report."""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from judge import judge  # noqa: E402


def main():
    ap=argparse.ArgumentParser();ap.add_argument('round',type=int);opt=ap.parse_args()
    manifest_path=ROOT/'collab'/f't028-round{opt.round}-manifest.json'
    report_path=ROOT/'collab'/f't028-round{opt.round}-report.json'
    manifest=json.loads(manifest_path.read_text());report=json.loads(report_path.read_text())
    catalog=json.loads((ROOT/'data/openjudge/catalog.json').read_text())['problems']
    by_number={}
    for item in catalog:
        m=re.search(r'(\d+)$',item['id'])
        if m and item.get('test_cases'):by_number.setdefault(int(m.group(1)),item)
    report_rows={int(x['local_number']):x for x in report['entries']};failed=[]
    results=[]
    for entry in manifest['entries']:
        n=int(entry['local_number']);item=by_number[n]
        source=(ROOT/'data/openjudge'/entry['made_dir']/'samplecode.py').read_text()
        verdict=judge(item['book'],item['id'],'python',source)
        merged={'status':'passed' if verdict['status']=='Accepted' else 'FAILED',
                'verdict':verdict['status'],'book':item['book'],'problem':item['id'],
                'merged_cases':verdict.get('cases',item.get('test_count')),
                'total_ms':verdict.get('time_ms')}
        report_rows[n]['merged_judge']=merged
        if verdict['status']!='Accepted':failed.append(n);report_rows[n]['status']='FAILED'
        results.append({'local_number':n,**merged})
        print(f"{n:05d} {verdict['status']} cases={merged['merged_cases']} total_ms={merged['total_ms']}",flush=True)
    report['entries']=[report_rows[int(x['local_number'])] for x in report['entries']]
    report['failed']=sorted(set(report.get('failed',[]))|set(failed));report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    out=ROOT/'collab'/f't028-round{opt.round}-localjudge.json'
    out.write_text(json.dumps({'task':'T-028','round':opt.round,'accepted':len(results)-len(failed),'total':len(results),
                               'not_accepted':failed,'results':results},ensure_ascii=False,indent=2)+'\n')
    return 1 if failed else 0


if __name__=='__main__':raise SystemExit(main())
