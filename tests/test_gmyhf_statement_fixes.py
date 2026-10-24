"""题面修复的自产夹具：参数推导、约束澄清与独立解法。"""
import html,itertools,json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import gmyhf_statement_fixes as recipes
import repair_gmyhf_sample_findings as pipeline

class StatementFixTests(unittest.TestCase):
    def test_missing_window_size_is_unique_and_verified(self):
        f={'sampleInput':'2 1 4 3','sampleOutput':'2 4 4'}
        self.assertEqual(['2 1 4 3\n2'],recipes.recovered_samples(31303,f))
        self.assertEqual('2 1 4 3\n2',pipeline.repaired_form(31303,f,['2 4 4'])['sampleInput'])
        for out in ('2 4','9 9 9',''):
            with self.assertRaises(AssertionError):
                recipes.recovered_samples(31303,dict(f,sampleOutput=out))

    def test_wealth_sample_translation_keeps_minimum_gap(self):
        f={'sampleInput':'3\n1 3 7','sampleOutput':'3\n错误解释'}
        given=recipes.recovered_samples(25685,f)[0]
        m,*a=map(int,given.split())
        self.assertTrue(all(x>=m for x in a))
        best=min(max(z)-min(z) for signs in itertools.product((-1,1),repeat=len(a))
                 for z in [[x+m*s for x,s in zip(a,signs)]])
        self.assertEqual(2,best)
        result=pipeline.repaired_form(25685,f,['2'])
        self.assertTrue(result['sampleOutput'].startswith('2\n'))
        self.assertIn('[6,8,6]',result['sampleOutput'])
        with self.assertRaises(AssertionError):pipeline.repaired_form(25685,f,['3'])

    def test_meeting_and_pass_change_only_the_conflicting_clause(self):
        f={'input':'前文 1 <= N <= K <= 10^6 后文','sampleInput':'4 2 4\n1 2 3 4','sampleOutput':'0'}
        r=pipeline.repaired_form(29329,f,['0'])
        self.assertEqual('前文 1 <= K <= N <= 10^6 后文',r['input'])
        self.assertEqual(f['sampleInput'],r['sampleInput'])
        old='每行包含三个值：玩家名字、意图（需求Need, 贪婪Greed, 或放弃Pass）和掷骰点数（1 到 100 间的整数）。'
        r=pipeline.repaired_form(30125,{'input':old,'sampleOutput':'X'},['X'])
        self.assertIn('Pass可省略',r['input']);self.assertEqual('X',r['sampleOutput'])
        with self.assertRaises(AssertionError):recipes.changed_form(29329,{'input':'规则已被改动'},['0'])
        with self.assertRaises(AssertionError):recipes.changed_form(30125,{'input':'规则已被改动'},['X'])

    def test_missing_parameter_sample_cannot_change_the_original_output(self):
        source="import sys\nsys.stdout.write('2 4 4\\n')\n"
        entry={'authored_reference':{'source':source,'sha256':pipeline.sha(source.encode())},
               'checks':{'answers':{'official_sample_checks':[]}}}
        f={'sampleInput':'2 1 4 3','sampleOutput':'2 4 4'}
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(['2 4 4'],pipeline.compute_samples(31303,entry,f,Path(t))[0])
            source=source.replace('2 4 4','4 4 4');entry['authored_reference']={'source':source,'sha256':pipeline.sha(source.encode())}
            with self.assertRaises(ValueError):pipeline.compute_samples(31303,entry,f,Path(t))

class FollowupWriterTests(unittest.TestCase):
    def setUp(self):
        import contextlib,io
        from unittest.mock import patch
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        self.root=Path(temp.name);self.work=self.root/'work';self.number=31303
        self.fields={k:'自产夹具' for k in pipeline.FIELDS}
        self.fields.update(sampleInput='2 1 4 3',sampleOutput='2 4 4',id='31303',timeLimit='1000')
        self.files={'a.in':b'2 1 4 3\n2\n','a.out':b'2 4 4\n','note.txt':b'fixture'}
        self.posts=[]
        source="print('2 4 4')\n"
        entry={'global_number':31303,'authored_reference':{'source':source,'sha256':pipeline.sha(source.encode())},
               'checks':{'statement':{'field_sha256':{k:pipeline.sha(html.unescape(self.fields[k]).encode()) for k in pipeline.FIELDS}},
                         'readback':{'files':[{'filename':n,'sha256':pipeline.sha(v)} for n,v in self.files.items() if n.endswith(('.in','.out'))]},
                         'answers':{'official_sample_checks':[]}}}
        pipeline.save(self.root/'collab/gmyhf-pending-batch15-review.json',{'entries':[entry]})
        pipeline.save(self.root/'collab/gmyhf-sample-repairs.json',{'historical':True})
        stack=contextlib.ExitStack();self.addCleanup(stack.close)
        stack.enter_context(patch.object(pipeline,'ROOT',self.root))
        stack.enter_context(patch.object(pipeline,'FOLLOWUP',{31303:15}))
        stack.enter_context(patch.object(pipeline.subprocess,'check_output',return_value='fixture\n'))
        session=stack.enter_context(patch.object(pipeline.platform.oj_submit,'Session')).return_value
        session.login.return_value=session;session._get.side_effect=lambda url:self.page()
        def post(url,fields):
            self.posts.append(dict(fields));self.fields={k:html.escape(v) if k=='hint' else v for k,v in fields.items()}
        session._post.side_effect=post
        stack.enter_context(patch.object(pipeline.platform,'download',side_effect=lambda s,n,name:self.files[name]))
        stack.enter_context(contextlib.redirect_stdout(io.StringIO()))

    def page(self):
        text=''.join(f'<textarea name="{k}">{v}</textarea>' for k,v in self.fields.items() if k in pipeline.FIELDS)
        text+=''.join(f'<input name="{k}" value="{v}">' for k,v in self.fields.items() if k not in pipeline.FIELDS)
        text+=''.join(f'<a href="/admin/download?problem_id={self.number}&filename={n}">下载</a>' for n in self.files)
        return '<form action="/api/global-problem/modify/">'+text+'</form>'

    def test_batch_selection_readback_retry_and_historical_receipt(self):
        files=dict(self.files)
        pipeline.run(self.work,True,8)
        self.assertEqual('2 1 4 3\n2',self.fields['sampleInput'])
        self.assertEqual(files,self.files)
        receipt=json.loads((self.root/'collab/gmyhf-statement-repairs-batch8.json').read_text())
        self.assertEqual(8,receipt['batch']);self.assertTrue(receipt['applied'])
        self.assertEqual({'sampleInput'},set(receipt['problems'][0]['changed_fields']))
        self.assertEqual({'historical':True},json.loads((self.root/'collab/gmyhf-sample-repairs.json').read_text()))
        pipeline.run(self.work,True,8);self.assertEqual(1,len(self.posts))

    def test_followup_default_readonly_and_drift_guard(self):
        pipeline.run(self.work,False,8)
        self.assertEqual([],self.posts)
        self.assertFalse((self.root/'collab/gmyhf-statement-repairs-batch8.json').exists())
        self.fields['input']='漂移'
        with self.assertRaises(ValueError):pipeline.run(self.work,True,8)
        self.assertEqual([],self.posts)

    def test_previous_data_repair_is_bound_before_wealth_sample_update(self):
        self.number=25685
        pipeline.FOLLOWUP.clear();pipeline.FOLLOWUP[25685]=12
        self.fields.update(id='25685',sampleInput='3\n1 3 7',sampleOutput='3')
        self.files['a.in']=b'3\n3 5 9\n';self.files['a.out']=b'2\n'
        source="print(2)\n"
        entry={'global_number':25685,'authored_reference':{'source':source,'sha256':pipeline.sha(source.encode())},
               'checks':{'statement':{'field_sha256':{k:pipeline.sha(html.unescape(self.fields[k]).encode()) for k in pipeline.FIELDS}},
                         'readback':{'files':[{'filename':n,'sha256':pipeline.sha(b'original')} for n in ('a.in','a.out')]},
                         'answers':{'official_sample_checks':[{'oracle_sha256':pipeline.sha(b'2')}]}}}
        pipeline.save(self.root/'collab/gmyhf-pending-batch12-review.json',{'entries':[entry]})
        prior={'problems':[{'global_number':25685,'final_files':{n:pipeline.sha(v) for n,v in self.files.items()}}]}
        pipeline.save(self.root/'collab/gmyhf-review-fixes-batch7.json',prior)
        before=dict(self.files);pipeline.run(self.work,True,8)
        self.assertEqual(before,self.files)
        self.assertEqual('3\n3 5 9',self.fields['sampleInput'])
        self.assertTrue(self.fields['sampleOutput'].startswith('2\n'))
        report=json.loads((self.root/'collab/gmyhf-statement-repairs-batch8.json').read_text())
        self.assertEqual(pipeline.sha((self.root/'collab/gmyhf-review-fixes-batch7.json').read_bytes()),
                         report['problems'][0]['prior_repair_sha256'])
