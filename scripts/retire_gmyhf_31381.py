#!/usr/bin/env python3
"""OpenJudge不支持SPJ：只解绑测试课程的31381，保留全局题目和本地SPJ。

默认只回读生成计划，--apply才撤下课程题目；不删除全局题目或下载文件。
"""
import argparse
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts import repair_gmyhf_pending_answers as common

COURSE = '2026fallcs101testing'
CONTEST_ID = '25952'
NUMBER = 'E31381'
GLOBAL_NUMBER = '31381'
EDIT_PATH = '/admin/contests/edit-problems/?id=' + CONTEST_ID


class CourseForms(HTMLParser):
    """只解析实际HTML表单，忽略script中的新增行模板。"""
    def __init__(self):
        super().__init__()
        self.current = None
        self.rows = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'form':
            if self.current is not None:
                raise ValueError('课程表单嵌套')
            if attrs.get('action') == '/api/contest/modify-problems/':
                self.current = {}
        elif tag == 'input' and self.current is not None:
            name = attrs.get('name')
            if name:
                if name in self.current:
                    raise ValueError('课程表单字段重复')
                self.current[name] = attrs.get('value', '')

    def handle_endtag(self, tag):
        if tag == 'form' and self.current is not None:
            self.rows.append(self.current)
            self.current = None


def course_mapping(page):
    parser = CourseForms()
    parser.feed(page)
    common.require(parser.current is None and parser.rows, '未获得完整课程题目表单')
    result = {}
    for row in parser.rows:
        common.require(set(row) == {'contestId', 'originalNumber', 'problemNumber', 'problemId'},
                       '课程表单字段发生变化')
        common.require(row['contestId'] == CONTEST_ID, '课程ID不符')
        number = row['problemNumber']
        common.require(row['originalNumber'] == number and
                       re.fullmatch(r'[A-Za-z0-9_-]+', number) is not None and
                       re.fullmatch(r'[0-9]+', row['problemId']) is not None,
                       '课程题号绑定不完整')
        common.require(number not in result, '课程题号重复')
        result[number] = row['problemId']
    return result


def retirement_plan(before):
    common.require(before.get(NUMBER) in (None, GLOBAL_NUMBER), '目标路由已改绑，停止解绑')
    common.require([n for n, g in before.items() if g == GLOBAL_NUMBER] in ([], [NUMBER]),
                   '31381出现其他别名，停止解绑')
    return {n: g for n, g in before.items() if n != NUMBER}


def verify_retirement(before, after):
    common.require(after == retirement_plan(before), '解绑回读不一致或其他题目绑定变化')


def run(work, apply=False, session=None):
    platform = common.platform
    session = session or platform.oj_submit.Session().login()
    host = platform.oj_submit.HOST
    work.mkdir(parents=True, exist_ok=True)
    before_page = session._get(host + EDIT_PATH)
    before = course_mapping(before_page)
    planned = retirement_plan(before)
    common.require(before, '课程为空，拒绝修改')
    globals_before = {}
    for number in (31381, 27952, 28341):
        page = session._get(host + f'/admin/problems/edit/?id={number}')
        fields = platform.parse_form(page)
        common.require(fields.get('problemId') == str(number), '全局题号不符')
        common.require(fields.get('privacy') == 'private', '全局题已公开，须重新核查范围')
        globals_before[number] = common.form_sha(page)
    page = session._get(host + '/admin/problems/edit/?id=31381')
    files = common.listed_files(page, 31381)
    file_hashes = {name: common.sha(platform.download(session, 31381, name)) for name in files}
    # 原始后台页面只备份到操作者指定的工作目录，不放入审核回执。
    (work / 'course-before.html').write_text(before_page)
    report = {'checked_at': datetime.now(timezone.utc).isoformat(), 'applied': False,
              'course': COURSE, 'contest_id': CONTEST_ID, 'global_number': 31381,
              'before_mapping': before, 'planned_mapping': planned,
              'removed_routes': [NUMBER] if NUMBER in before else [],
              'global_form_sha256': globals_before, 'test_file_sha256': file_hashes,
              'global_problem_deletions': 0, 'test_file_writes': 0,
              'local_spj_changes': 0,
              'reason': '用户确认OpenJudge不支持SPJ；该课程撤下31381，本地SPJ保留。'}
    common.save(work / 'plan.json', report)
    if not apply:
        return report
    current = course_mapping(session._get(host + EDIT_PATH))
    common.require(current == before, '写入前课程绑定变化，停止解绑')
    if NUMBER in before:
        response = json.loads(session._post(host + '/api/contest/delete-problem/',
                                            {'contestId': CONTEST_ID, 'problemNumber': NUMBER}))
        common.require(response.get('result') == 'SUCCESS', '课程解绑请求未成功')
    after = course_mapping(session._get(host + EDIT_PATH))
    verify_retirement(before, after)
    for number, digest in globals_before.items():
        page = session._get(host + f'/admin/problems/edit/?id={number}')
        common.require(common.form_sha(page) == digest, '全局题面或配置发生变化')
        if number == 31381:
            common.require(common.listed_files(page, number) == files, '31381文件清单变化')
    for name, digest in file_hashes.items():
        common.require(common.sha(platform.download(session, 31381, name)) == digest,
                       '31381测试文件变化')
    index = session._get(host + '/' + COURSE + '/')
    common.require(re.search(r'href=["\x27]/' + COURSE + '/' + NUMBER + r'/', index) is None,
                   '课程列表仍提供31381路由')
    report.update(applied=True, after_mapping=after, other_bindings_unchanged=True,
                  global_forms_unchanged=True, test_files_unchanged=True,
                  course_index_sha256=common.sha(index.encode()))
    common.save(work / 'receipt.json', report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    report = run(args.work, args.apply)
    print(json.dumps({'applied': report['applied'], 'removed_routes': report['removed_routes']},
                     ensure_ascii=False))


if __name__ == '__main__':
    main()
