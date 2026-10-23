#!/usr/bin/env python3
"""同步已审定的六题题面及30162/30281文件；默认只生成计划，--apply才写平台。

既有后台快照和题面修改放在--work目录；登录仅复用oj_submit的环境变量。
拒绝未审核的上游变化，逐项写后回读；不打印、存储登录凭据或上传令牌。
"""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import urllib.parse
import uuid

import oj_submit

ROOT = Path(__file__).resolve().parents[1]


class Controls(HTMLParser):
    def __init__(self):
        super().__init__(); self.fields = {}; self.select = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs); name = attrs.get('name')
        if tag == 'input' and name and attrs.get('type') != 'file':
            if re.search('token|password|timestamp', name, re.I):
                return
            if attrs.get('type') not in ('radio', 'checkbox') or 'checked' in attrs:
                self.fields[name] = attrs.get('value', '')
        if tag == 'select':
            self.select = name
        if tag == 'option' and self.select and 'selected' in attrs:
            self.fields[self.select] = attrs.get('value', '')

    def handle_endtag(self, tag):
        if tag == 'select': self.select = None


def parse_form(page):
    match = re.search(r'<form\b[^>]*action="/api/global-problem/modify/"[^>]*>(.*?)</form>', page, re.S)
    if not match: raise ValueError('后台未提供题目编辑表单')
    form = match[1]; fields = {}
    for attrs, body in re.findall(r'<textarea\b([^>]*)>(.*?)</textarea>', form, re.S):
        name = re.search(r'name="([^"]+)"', attrs)[1]
        # 平台直接把题面HTML写进textarea，没有再转义一层；解码会破坏原有&lt;等实体。
        fields[name] = body
    # textarea是原始文本，内含图片HTML或裸小于号；不能让HTMLParser把它当页面标签解析。
    controls = Controls(); controls.feed(re.sub(r'<textarea\b.*?</textarea>', '', form, flags=re.S))
    return {**controls.fields, **fields}


def normalized(fields):
    return {key: value.replace('\r\n', '\n') for key, value in fields.items()}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def download(session, number, name):
    url = oj_submit.HOST + '/admin/download?' + urllib.parse.urlencode(
        {'problem_id': number, 'filename': name})
    with session._opener.open(session._request(url), timeout=60) as response:
        return response.read()


def upload(session, number, name, payload):
    page = session._get(oj_submit.HOST+f'/admin/problems/edit/?id={number}')
    fields = {key: re.search(r"'"+key+r"'\s*:\s*'([^']+)'", page)[1]
              for key in ('folder', 'timestamp', 'token')}
    if fields['folder'] != f'/{number}': raise ValueError('上传目标目录不符')
    boundary = '----cs101-' + uuid.uuid4().hex
    chunks = []
    for key, value in fields.items():
        chunks.append((f'--{boundary}\r\nContent-Disposition: form-data; name="{key}"\r\n\r\n{value}\r\n').encode())
    chunks.append((f'--{boundary}\r\nContent-Disposition: form-data; name="Filedata"; '
                   f'filename="{name}"\r\nContent-Type: application/octet-stream\r\n\r\n').encode())
    chunks.extend((payload, f'\r\n--{boundary}--\r\n'.encode()))
    request = session._request(oj_submit.HOST+'/api/doajaxfileupload/upload/', b''.join(chunks))
    request.add_header('Content-Type', 'multipart/form-data; boundary='+boundary)
    with session._opener.open(request, timeout=60) as response:
        response.read()


def run(work, apply=False):
    session = oj_submit.Session().login()
    before = json.loads((work/'forms-before.json').read_text())
    after = json.loads((work/'forms-after.json').read_text())
    forms = []
    for number, fields in before.items():
        current = parse_form(session._get(oj_submit.HOST+f'/admin/problems/edit/?id={number}'))
        if normalized(current) not in (normalized(fields), normalized(after[number])):
            raise ValueError(f'{number}: 题面或配置变化，停止同步')
        changed = [key for key in fields if normalized(fields)[key] != normalized(after[number])[key]]
        forms.append({'global_number': int(number), 'changed_fields': changed,
                      'before_sha256': digest(json.dumps(normalized(fields), sort_keys=True).encode()),
                      'after_sha256': digest(json.dumps(normalized(after[number]), sort_keys=True).encode())})
    files = []
    all_before = {}
    for number in (30162, 30281, 28912):
        directory = work/'platform-before'/str(number)
        for path in directory.iterdir():
            old = path.read_bytes(); all_before[number, path.name] = old
            live = download(session, number, path.name)
            target = old
            if number in (30162, 30281):
                base = ROOT/f'data/openjudge/tests/30000-/{number}_GMyhf'
                source = json.loads((base/'SOURCE.json').read_text())
                for row in source['files']:
                    for kind, suffix in [('input', 'in'), ('output', 'out')]:
                        if row['original_'+kind] == path.name:
                            target = (base/'data'/f'{row["case"]}.{suffix}').read_bytes()
                if number == 30281 and path.name in ('producecase.py', 'samplecode1.py', 'samplecode2.py'):
                    name = 'producecase.py' if path.name == 'producecase.py' else 'samplecode.py'
                    target = (ROOT/'data/openjudge/tests/30000-/30281_made'/name).read_bytes()
            if live not in (old, target): raise ValueError(f'{number}/{path.name}: 平台文件变化')
            if target != old:
                files.append({'global_number': number, 'filename': path.name,
                              'before_sha256': digest(old), 'after_sha256': digest(target), 'bytes': len(target)})
    result = {'applied': False, 'forms': forms, 'files': files}
    (work/'sync-plan.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print('同步计划：',len(forms),'题题面，',len(files),'个文件',flush=True)
    if not apply: return result
    for item in forms:
        number = str(item['global_number'])
        current = parse_form(session._get(oj_submit.HOST+f'/admin/problems/edit/?id={number}'))
        if normalized(current) not in (normalized(before[number]), normalized(after[number])):
            raise ValueError(f'{number}: 写入前题面变化')
        if normalized(current) != normalized(after[number]):
            session._post(oj_submit.HOST+'/api/global-problem/modify/', after[number])
        observed = parse_form(session._get(oj_submit.HOST+f'/admin/problems/edit/?id={number}'))
        if normalized(observed) != normalized(after[number]): raise ValueError(f'{number}: 题面回读不一致')
        print(number, '题面和配置回读校验通过',flush=True)
    planned = {(r['global_number'], r['filename']): r for r in files}
    for (number, name), old in all_before.items():
        live = download(session, number, name)
        if (number, name) in planned:
            item = planned[number, name]
            if digest(live) != item['after_sha256']:
                if digest(live) != item['before_sha256']: raise ValueError('写入前文件变化')
                # 计划生成后再次绑定本地目标字节，避免向平台提交变化后的未审核内容。
                base = ROOT/f'data/openjudge/tests/30000-/{number}_GMyhf'
                source = json.loads((base/'SOURCE.json').read_text())
                targets = {row['original_'+kind]: base/'data'/f'{row["case"]}.{suffix}'
                           for row in source['files'] for kind, suffix in [('input','in'),('output','out')]}
                targets.update({key: ROOT/'data/openjudge/tests/30000-/30281_made'/value
                                for key, value in [('producecase.py','producecase.py'),
                                                   ('samplecode1.py','samplecode.py'),('samplecode2.py','samplecode.py')]})
                payload = targets[name].read_bytes()
                if digest(payload) != item['after_sha256']: raise ValueError('本地目标在审核后变化')
                upload(session, number, name, payload)
            if digest(download(session, number, name)) != item['after_sha256']: raise ValueError('文件回读不一致')
            print(number,name,'回读校验通过',flush=True)
        elif live != old:
            raise ValueError(f'{number}/{name}: 非目标文件变化')
    result['applied'] = True
    (work/'sync-result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, default=Path('/tmp/gmyhf-fixes'))
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args(); run(args.work, args.apply)
