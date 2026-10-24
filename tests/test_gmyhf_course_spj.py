"""课程路由不能靠数字猜全局号；SPJ探针只使用自产字符串。"""
from pathlib import Path
import json
import tempfile
from unittest.mock import patch
import subprocess
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import audit_gmyhf_course_spj as audit


class CourseSpjTests(unittest.TestCase):
    def test_routes_keep_prefix_aliases_and_reject_external_or_navigation(self):
        page=''.join(f'<a href="{path}">题目</a>' for path in (
            '/2026fallcs101testing/E3417/','/2026fallcs101testing/test/',
            '/2026fallcs101testing/30686/','/2026fallcs101testing/E3417/',
            '/2026fallcs101testing/ranking/','/2026fallcs101testing/status/',
            '/2026fallcs101testing/clarify/','https://evil.test/2026fallcs101testing/E31381/',
            '/other/E31381/','/2026fallcs101testing/../'))
        self.assertEqual(['/2026fallcs101testing/30686/','/2026fallcs101testing/E3417/','/2026fallcs101testing/test/'],audit.course_routes(page))

    def test_global_number_is_unique_explicit_metadata(self):
        page='<a href="/2026fallcs101testing/E3417/">3417</a><dt>全局题号</dt><dd>31417</dd>'
        self.assertEqual(31417,audit.global_number(page))
        for bad in ('',page+page,'<dt>全局题号</dt><dd>text</dd>'):
            with self.assertRaises(ValueError):audit.global_number(bad)

    def test_permutation_preserves_multiplicity_spaces_and_unicode(self):
        for given,actual in [('aab','baa\n'),('a b',' ba\r\n'),('甲甲乙','乙甲甲'),('','\n')]:
            self.assertTrue(audit.is_permutation(given,actual))
        for given,actual in [('aab','abb'),('a b','ab'),('ab','abc'),('甲乙','甲甲')]:
            self.assertFalse(audit.is_permutation(given,actual))

    def test_audit_defaults_to_no_submission_and_records_probe_disagreement(self):
        for scenario in ('read','submit','file_drift','form_drift','route_drift','prelist_drift','list_drift','statement_drift'):
            submit=scenario!='read'
            with self.subTest(scenario=scenario),tempfile.TemporaryDirectory() as work:
                root=Path(work);(root/'collab').mkdir()
                fields={key:'自造字段' for key in audit.FIELDS}
                form='<form action="/api/global-problem/modify/">'+''.join(f'<textarea name="{key}">{value}</textarea>' for key,value in fields.items())+'</form>'
                form+=''.join(f'<a href="/admin/download?problem_id=31381&amp;filename={name}">文件</a>' for name in ('0.in','0.out'))
                payloads={'0.in':b'aba\n','0.out':b'0\n'}
                entry={'global_number':31381,'checks':{'statement':{'field_sha256':{key:audit.common.sha(value.encode()) for key,value in fields.items()}},'readback':{'files':[{'filename':name,'sha256':audit.common.sha(value)} for name,value in payloads.items()]}}}
                (root/'collab/gmyhf-pending-batch15-review.json').write_text(json.dumps({'entries':[entry]}))
                class Session:
                    def __init__(self):self.submitted=[];self.admin_reads=0
                    def login(self):return self
                    def _get(self,url):
                        if '/admin/' in url:
                            self.admin_reads+=1
                            if scenario=='statement_drift' or (scenario=='form_drift' and self.admin_reads>1):return form.replace('自造字段','漂移')
                            if scenario=='prelist_drift' or (scenario=='list_drift' and self.admin_reads>1):return form+'<a href="/admin/download?problem_id=31381&amp;filename=1.in">新增</a>'
                            return form
                        if url.endswith('/E31381/'):return '<dt>全局题号</dt><dd>'+('31382' if scenario=='route_drift' else '31381')+'</dd>'
                        return '<a href="/2026fallcs101testing/E31381/">题目</a>'
                    def submit(self,number,source,language,group):
                        self.submitted.append((number,source,language,group));return str(len(self.submitted))
                    def poll(self,solution,group):return {'verdict':'Wrong Answer','solution_id':solution,'ms':1}
                session=Session()
                with patch.object(audit.common,'ROOT',root),patch.object(audit.common.platform.oj_submit,'Session',return_value=session),patch.object(audit.common.platform,'download',side_effect=lambda s,n,name:b'drift' if scenario=='file_drift' else payloads[name]):
                    if scenario not in ('read','submit'):
                        with self.assertRaises(ValueError):audit.run(root/'work',submit=submit)
                        self.assertFalse((root/'collab/gmyhf-course-spj-recheck.json').exists())
                        self.assertEqual(6 if scenario in ('form_drift','list_drift') else 0,len(session.submitted))
                        continue
                    audit.run(root/'work',submit=submit)
                report=json.loads((root/'collab/gmyhf-course-spj-recheck.json').read_text())
                self.assertEqual(6 if submit else 0,len(session.submitted))
                self.assertEqual(len(session.submitted),report['submission_writes'])
                self.assertEqual((0,0,0),(report['test_data_writes'],report['statement_writes'],report['configuration_writes']))
                self.assertFalse(report['stored_output_is_permutation_certificate'])
                self.assertFalse(report['all_probes_match_statement'])
                if submit:
                    self.assertEqual([False,False,False,True,True,True],[p['matches_statement_expectation'] for p in report['probes']])
                    self.assertEqual(list(audit.probe_sources().values()),[args[1] for args in session.submitted])
                self.assertTrue(report['preserve_existing_spj_exclusion'])

    def test_real_probe_programs_have_expected_semantics(self):
        sources=audit.probe_sources();self.assertEqual({'identity','reverse','sorted','append_invalid','replace_invalid','drop_invalid'},set(sources))
        for given in ('aab\n','b a\r\n','乙甲甲\n','\n'):
            for name,source in sources.items():
                run=subprocess.run([sys.executable,'-I','-c',source],input=given.encode(),capture_output=True,check=True,timeout=5)
                self.assertEqual(not name.endswith('_invalid'),audit.is_permutation(given,run.stdout.decode()))
