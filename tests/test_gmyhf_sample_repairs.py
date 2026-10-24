"""样例与讲解回填的字段边界、并发变化和完整回读；自产离线夹具。"""
import contextlib
import io
import html
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import repair_gmyhf_sample_findings as repair


class SampleRepairTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.fields = {k:'fixture' for k in repair.FIELDS}
        self.fields.update(sampleInput='3 2 8',sampleOutput='10\n\n解释：共7种。',id='30176',timeLimit='1000')
        self.live = {'a.in':b'fixture input','a.out':b'fixture output','attachment.txt':b'untouched'}
        self.posts = []
        source = 'print(7)\n'
        entry = {'global_number':30176,'authored_reference':{'source':source,'sha256':repair.sha(source.encode())},
                 'checks':{'statement':{'field_sha256':{k:repair.sha(html.unescape(self.fields[k]).encode()) for k in repair.FIELDS}},
                           'readback':{'files':[{'filename':n,'sha256':repair.sha(v)} for n,v in self.live.items() if n.endswith(('.in','.out'))]},
                           'answers':{'official_sample_checks':[{'oracle_sha256':repair.sha(b'7')}]}}}
        repair.save(self.root/'collab/gmyhf-pending-batch14-review.json',{'entries':[entry]})
        self.stack = contextlib.ExitStack()
        self.addCleanup(self.stack.close)
        self.stack.enter_context(patch.object(repair,'ROOT',self.root))
        self.stack.enter_context(patch.object(repair,'PROBLEMS',{30176:14}))
        self.stack.enter_context(patch.object(repair.subprocess,'check_output',return_value='fixture\n'))
        session = self.stack.enter_context(patch.object(repair.platform.oj_submit,'Session')).return_value
        session.login.return_value = session
        session._get.side_effect = lambda url:self.page()
        session._post.side_effect = self.post
        self.session = session
        self.stack.enter_context(patch.object(repair.platform,'download',side_effect=lambda s,n,f:self.live[f]))
        self.stack.enter_context(contextlib.redirect_stdout(io.StringIO()))

    def page(self):
        fields = ''.join(f'<textarea name="{k}">{v}</textarea>' for k,v in self.fields.items() if k in repair.FIELDS)
        controls = ''.join(f'<input name="{k}" value="{v}">' for k,v in self.fields.items() if k not in repair.FIELDS)
        files = ''.join(f'<a href="/admin/download?problem_id=30176&filename={n}">下载</a>' for n in self.live)
        return '<form action="/api/global-problem/modify/">'+fields+controls+'</form>'+files

    def post(self,url,fields):
        self.posts.append(dict(fields))
        self.fields = {k:html.escape(v) if k == 'hint' else v for k,v in fields.items()}

    def run_repair(self,apply=True):
        repair.run(self.root/'work',apply)

    def test_allowed_fields_only_and_idempotent_full_readback(self):
        before = dict(self.fields)
        files = dict(self.live)
        self.run_repair()
        self.assertEqual('7\n\n解释：共7种。',self.fields['sampleOutput'])
        before['sampleOutput'] = self.fields['sampleOutput']
        self.assertEqual(before,self.fields)
        self.assertEqual(files,self.live)
        self.assertEqual(1,len(self.posts))
        report = json.loads((self.root/'collab/gmyhf-sample-repairs.json').read_text())
        self.assertTrue(report['applied'])
        self.assertEqual({'sampleOutput'},set(report['problems'][0]['changed_fields']))
        self.assertTrue(report['problems'][0]['local_matches'])
        self.run_repair()
        self.assertEqual(1,len(self.posts))

    def test_entity_roundtrip_preserves_existing_description(self):
        original = '<p>x &lt; y</p>'
        self.fields['description'] = original
        self.fields['hint'] = 'x &lt;= 3 &amp; y &gt; 0'
        path = self.root/'collab/gmyhf-pending-batch14-review.json'
        entry = json.loads(path.read_text())
        entry['entries'][0]['checks']['statement']['field_sha256']['description'] = repair.sha(html.unescape(original).encode())
        entry['entries'][0]['checks']['statement']['field_sha256']['hint'] = repair.sha(html.unescape(self.fields['hint']).encode())
        repair.save(path,entry)
        self.run_repair()
        self.assertEqual(original,self.fields['description'])
        self.assertEqual('x &lt;= 3 &amp; y &gt; 0',self.fields['hint'])

    def test_default_readonly(self):
        self.run_repair(False)
        self.assertEqual([],self.posts)
        self.assertFalse((self.root/'collab/gmyhf-sample-repairs.json').exists())

    def test_statement_drift_stops_before_post(self):
        self.fields['description'] = 'changed'
        with self.assertRaises(ValueError):self.run_repair()
        self.assertEqual([],self.posts)

    def test_data_drift_stops_before_post(self):
        self.live['a.in'] = b'changed'
        with self.assertRaises(ValueError):self.run_repair()
        self.assertEqual([],self.posts)

    def test_failed_post_readback_cannot_claim_success(self):
        self.session._post.side_effect = lambda url,fields:None
        with self.assertRaises(ValueError):self.run_repair()
        self.assertFalse((self.root/'collab/gmyhf-sample-repairs.json').exists())

    def test_data_drift_during_post_cannot_claim_success(self):
        def post(url,fields):
            self.post(url,fields)
            self.live['a.out'] = b'changed'
        self.session._post.side_effect = post
        with self.assertRaises(ValueError):self.run_repair()
        self.assertFalse((self.root/'collab/gmyhf-sample-repairs.json').exists())

    def test_reference_bound_to_audit(self):
        path = self.root/'collab/gmyhf-pending-batch14-review.json'
        evidence = json.loads(path.read_text())
        evidence['entries'][0]['authored_reference']['source'] = 'print(9)\n'
        repair.save(path,evidence)
        with self.assertRaises(ValueError):self.run_repair()
        self.assertEqual([],self.posts)


    def test_recomputed_reference_cannot_change_proven_sample_answer(self):
        path = self.root/'collab/gmyhf-pending-batch14-review.json'
        evidence = json.loads(path.read_text())
        source = 'print(9)\n'
        evidence['entries'][0]['authored_reference'] = {'source':source,'sha256':repair.sha(source.encode())}
        repair.save(path,evidence)
        with self.assertRaises(ValueError):self.run_repair()
        self.assertEqual([],self.posts)

    def test_local_statement_drift_cannot_claim_success(self):
        def post(url,fields):
            self.post(url,fields)
            path = self.root/'data/openjudge/tests/admin_review_statements/30176/fields.json'
            local = json.loads(path.read_text())
            local['sampleOutput'] = '9'
            repair.save(path,local)
        self.session._post.side_effect = post
        with self.assertRaises(ValueError):self.run_repair()
        self.assertFalse((self.root/'collab/gmyhf-sample-repairs.json').exists())


class SampleRecipeTests(unittest.TestCase):
    def test_browser_submission_decodes_textarea_entities_exactly_once(self):
        fields = {'description':'<p>A &lt; B</p>','hint':'A &amp;lt; B','title':'A & B'}
        self.assertEqual({'description':'<p>A &lt; B</p>','hint':'A &lt; B','title':'A & B'},repair.submitted_form(fields))

    def test_numeric_output_replacements_preserve_explanations(self):
        for n,old,new in ((30176,'10','7'),(30916,'6','28'),(28698,'900','800'),(29951,'2','3')):
            fields = {'sampleOutput':old+'\r\n\r\n说明保留','title':'fixture'}
            result = repair.repaired_form(n,fields,[new])
            self.assertEqual(new+'\r\n\r\n说明保留',result['sampleOutput'])
            self.assertEqual('fixture',result['title'])
        fields = {'sampleOutput':'6','hint':'贪心+双指针\r\n【数据范围】\r\n保持'}
        result = repair.repaired_form(30205,fields,['2'])
        self.assertEqual('2',result['sampleOutput'])
        self.assertTrue(result['hint'].endswith('\r\n【数据范围】\r\n保持'))
        self.assertIn('二项式',result['hint'])

    def test_labeled_examples_and_explanation_consistency(self):
        fields = {'sampleInput':'sample1:\n2 13\n1 -9\n5 -3\n\nsample2:\n1 3\n1 0',
                  'sampleOutput':'sample1:\nYES\n\nsample2:\nNO\n'}
        self.assertEqual(['2 13\n1 -9\n5 -3','1 3\n1 0'],repair.sample_inputs(30078,fields))
        self.assertEqual('sample1:\nYES\n\nsample2:\nYES\n',repair.repaired_form(30078,fields,['YES','YES'])['sampleOutput'])
        fields = {'sampleInput':'Sample Input1:\n1 2 3 4\n\nSample Output1:\n5\n\n解释40',
                  'sampleOutput':'Sample Input2:\n2 5\n\nSample Output2:\n15\n\n解释:[2,5]->[2] 10+5=15'}
        self.assertEqual(['1 2 3 4','2 5'],repair.sample_inputs(25576,fields))
        result = repair.repaired_form(25576,fields,['40','15'])
        self.assertIn('Sample Output1:\n40\n',result['sampleInput'])
        self.assertIn('[2,5]->[5]',result['sampleOutput'])
        self.assertIn('10+5=15',result['sampleOutput'])

    def test_ambiguous_answer_lines_are_rejected(self):
        with self.assertRaises(ValueError):repair.replace_line('6\n6','6','2')
        with self.assertRaises(ValueError):repair.replace_line('60','6','2')
