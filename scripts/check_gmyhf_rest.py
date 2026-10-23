#!/usr/bin/env python3
"""剩余183题只读独立答案复核；每题完成即保存证据，不执行参考代码。"""
import argparse
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import signal
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
from gmyhf_oracles_basic import SOLVERS
import gmyhf_oracles_middle
import gmyhf_oracles_structures
import gmyhf_oracles_graphs
import gmyhf_oracles_advanced
import gmyhf_oracles_final


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def review(output,numbers=None):
    baseline=json.loads((ROOT/'collab/gmyhf-download-followup.json').read_text())
    rows=[r for r in baseline['entries']if 'independent'not in r and (not numbers or r['global_number']in numbers)]
    materialized={r['global_number']:r for r in json.loads((ROOT/'collab/gmyhf-download-materialize.json').read_text())['materialized']}
    result={'policy':'只读；不调用参考实现。未覆盖、超时和算法异常均不计为通过。','sources':{},'entries':[]}
    def expired(*_):raise TimeoutError('独立算法超过单文件120秒预算')
    signal.signal(signal.SIGALRM,expired)
    for row in rows:
        number=row['global_number']
        if number not in SOLVERS:continue
        source=materialized[number]; directory=ROOT/'data/openjudge/tests'/source['bucket']/(source['local_id']+'_GMyhf/data')
        entry={'global_number':number,'title':row['title'],'method':SOLVERS[number].__name__,'files':[]}
        for path in sorted(directory.glob('*.in'),key=lambda p:int(p.stem)):
            output_path=path.with_suffix('.out'); record={'input':str(path.relative_to(ROOT)),'input_sha256':digest(path),'output_sha256':digest(output_path)}
            start=time.monotonic()
            try:
                signal.alarm(120)
                actual=SOLVERS[number](path.read_text(encoding='utf-8-sig'))
                expected=output_path.read_text(encoding='utf-8-sig')
                record['matches']=(list(map(Decimal,actual.split()))==list(map(Decimal,expected.split())) if number==19546 else actual.split()==expected.split())
                if not record['matches']:record.update(computed=actual,recorded=expected)
            except Exception as exc:record['unproved']=f'{type(exc).__name__}: {exc}'
            finally:signal.alarm(0)
            record['elapsed_seconds']=round(time.monotonic()-start,3);entry['files'].append(record)
        entry['cases']=len(entry['files']);result['entries'].append(entry)
        result['sources']={str(p.relative_to(ROOT)):digest(p)for p in (Path(__file__),*Path(__file__).parent.glob('gmyhf_oracles_*.py'))}
        output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        print(number,len(entry['files']),sum(f.get('matches')is False for f in entry['files']),sum('unproved'in f for f in entry['files']),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('output',type=Path);parser.add_argument('--numbers',type=int,nargs='+')
    args=parser.parse_args();review(args.output,args.numbers)
