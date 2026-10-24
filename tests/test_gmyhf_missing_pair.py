"""错名输入的恢复、原件备份和重试保护；只用自产文件及离线后台。"""
import contextlib
import copy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import gmyhf_review_fixes as rules
import repair_gmyhf_missing_pair as repair


class MissingPairProofTests(unittest.TestCase):
    def test_prepare_restores_alias_and_preserves_all_answers(self):
        entry=next(e for e in json.loads((repair.ROOT/'collab/gmyhf-pending-batch12-review.json').read_text())['entries'] if e['global_number']==27934)
        with tempfile.TemporaryDirectory() as work:
            root=Path(work);base=root/'data/openjudge/tests/admin_pairing_review/27934';base.mkdir(parents=True)
            originals={'0.in':b'2 2\n1 2\n1\n100\n','0.out':b'1 2\n2 1\n','3.out':b'1 2\n','3,in':b'2 1\n1 2\n1\n'}
            for name,raw in originals.items():(base/name).write_bytes(raw)
            hashes={n:repair.sha(b) for n,b in originals.items()}
            entry['checks']['pairing']['unpaired']=[{'filename':'3.out'}]
            entry['checks']['readback']['files']=[{'filename':n,'sha256':v} for n,v in hashes.items()]
            entry['checks']['answers']['files']=[{'input':'0.in','output':'0.out'}]
            evidence=root/'collab/gmyhf-27934-pairing-review.json';evidence.parent.mkdir();evidence.write_text(json.dumps({'entries':[entry],'local_snapshot':'data/openjudge/tests/admin_pairing_review/27934'}))
            with patch.object(repair,'ROOT',root),patch.object(repair.judge,'judge',return_value={'status':'Accepted','timing_audit':{'status':'passed'}}) as judge:
                group,_=repair.prepare()
            target=root/group['local_dataset']/'data'
            self.assertEqual(2,group['verified_legal_pairs'])
            self.assertEqual('python3',judge.call_args.args[2])
            for name in ('0.in','0.out'):self.assertEqual(originals[name],(target/name).read_bytes())
            self.assertEqual(originals['3.out'],(base/'3.out').read_bytes())
            self.assertEqual(originals['3,in'],(target/'3.in').read_bytes())
            self.assertEqual(originals['3.out'],(target/'3.out').read_bytes())
            self.assertEqual({'3.in'},{r['filename'] for r in group['changes']})
            (base/'3.out').write_bytes(b'wrong-answer')
            for row in entry['checks']['readback']['files']:
                if row['filename']=='3.out':row['sha256']=repair.sha(b'wrong-answer')
            evidence.write_text(json.dumps({'entries':[entry],'local_snapshot':'data/openjudge/tests/admin_pairing_review/27934'}))
            with patch.object(repair,'ROOT',root),patch.object(repair.judge,'judge') as judge:
                with self.assertRaises(ValueError):repair.prepare()
                judge.assert_not_called()
            entry['authored_reference']['sha256']='0'*64;evidence.write_text(json.dumps({'entries':[entry],'local_snapshot':'data/openjudge/tests/admin_pairing_review/27934'}))
            with patch.object(repair,'ROOT',root),patch.object(repair.subprocess,'run') as run:
                with self.assertRaises(ValueError):repair.prepare()
                run.assert_not_called()

    def test_alias_contract_rejects_malformed_or_out_of_range_content(self):
        self.assertEqual(b'2 0\n0 1',rules.validate_missing_deque_input(b'2 0\n0 1'))
        for raw in (b'1 1 0 1',b'2 -1 0 1',b'2 1 0 1',b'2 1 0 1000000001 1',
                    b'2 1 -1 0 1',b'2 1 0 1 0',b'2 1 0 1 1000000000000000001',b'2 0 0 1 2'):
            with self.assertRaises(AssertionError):rules.validate_missing_deque_input(raw)

    def test_authored_case_and_reference_against_direct_deque_steps(self):
        e=next(e for e in json.loads((repair.ROOT/'collab/gmyhf-pending-batch12-review.json').read_text())['entries'] if e['global_number']==27934)
        source=e['authored_reference']['source'];self.assertEqual(repair.sha(source.encode()),e['authored_reference']['sha256'])
        ns={};exec(source.split('import sys\nsys.stdout.write')[0],ns)
        raw=b'7 5\n0 7 7 1000000000 1 0 1000000000\n1\n2\n3\n999999999999999999\n1000000000000000000\n';self.assertEqual(raw,rules.validate_missing_deque_input(raw));v=list(map(int,raw.split()));n,q=v[:2];values=v[2:2+n];queries=v[2+n:]
        self.assertEqual(q,len(queries));self.assertTrue(2<=n<=100000 and 1<=q<=300000)
        self.assertTrue(all(0<=x<=10**9 for x in values));self.assertTrue(all(1<=x<=10**18 for x in queries))
        self.assertIn(0,values);self.assertGreater(values.count(max(values)),1);self.assertIn(10**18,queries)
        board=list(values);answers=[];seen={}
        while tuple(board) not in seen:
            seen[tuple(board)]=len(answers);a,b=board[:2];answers.append(f'{a} {b}')
            board=([a]+board[2:]+[b]) if a>b else ([b]+board[2:]+[a])
        start=seen[tuple(board)];period=len(answers)-start
        expected=[answers[x-1] if x<=len(answers) else answers[start+(x-1-start)%period] for x in queries]
        self.assertEqual(expected,ns['valeriy'](raw.decode()).splitlines())
        for step in range(1,150):
            query=f'{n} 1\n'+ ' '.join(map(str,values))+f'\n{step}'
            index=step-1 if step<=len(answers) else start+(step-1-start)%period
            self.assertEqual(answers[index],ns['valeriy'](query))


class MissingPairWriterTests(unittest.TestCase):
    def setUp(self):
        self.stack=contextlib.ExitStack();self.addCleanup(self.stack.close)
        self.root=Path(self.stack.enter_context(tempfile.TemporaryDirectory()));self.work=self.root/'work'
        self.original={'0.in':b'fixture-in','0.out':b'fixture-out','3.out':b'orphan','3,in':b'alias-content'}
        self.live=dict(self.original);self.title='original';self.uploads=[];self.hook=None
        self.new=self.original['3,in'];self.answer=self.original['3.out']
        target=self.root/'data/openjudge/tests/admin_review_repaired/27934/data';target.mkdir(parents=True)
        for n,b in {**self.original,'3.in':self.new,'3.out':self.answer}.items():(target/n).write_bytes(b)
        baseline={n:repair.sha(b) for n,b in self.original.items()}
        self.group={'global_number':27934,'evidence_sha256':'audit','baseline_files':baseline,
                    'local_dataset':'data/openjudge/tests/admin_review_repaired/27934',
                    'changes':[{'filename':'3.in','before_sha256':None,'after_sha256':repair.sha(self.new)}],
                    'added_files':{'3.in':repair.sha(self.new)},'verified_legal_pairs':2}
        self.stack.enter_context(patch.object(repair,'ROOT',self.root))
        self.stack.enter_context(patch.object(repair,'prepare',side_effect=lambda:(copy.deepcopy(self.group),{})))
        self.stack.enter_context(patch.object(repair,'audit_statement'))
        session=self.stack.enter_context(patch.object(repair.platform.oj_submit,'Session')).return_value.login.return_value
        session._get.side_effect=self.get
        self.stack.enter_context(patch.object(repair.platform,'parse_form',side_effect=self.form))
        self.stack.enter_context(patch.object(repair,'listed_files',side_effect=lambda p,n:sorted(self.live)))
        self.stack.enter_context(patch.object(repair.platform,'download',side_effect=lambda s,n,f:self.live[f]))
        self.stack.enter_context(patch.object(repair.platform,'upload',side_effect=self.upload))
        self.stack.enter_context(patch.object(repair.subprocess,'check_output',return_value='fixture-commit\n'))
        self.stack.enter_context(contextlib.redirect_stdout(io.StringIO()))

    def form(self,page):
        return {'title':self.title,**({'filenames[3.in]':'3.in'} if '3.in' in self.live else {})}

    def get(self,url):
        if self.hook:self.hook()
        return 'page'

    def upload(self,session,number,name,payload):
        self.assertEqual(27934,number);self.uploads.append(name);self.live[name]=payload

    def apply(self):repair.run(self.work,True)

    def test_default_is_readonly_and_saves_original_absence(self):
        repair.run(self.work)
        self.assertEqual(self.original,self.live);self.assertEqual([],self.uploads)
        saved=json.loads((self.work/'before/27934/absence.json').read_text())
        self.assertNotIn('3.in',saved['original_files'])
        self.assertEqual(self.original['3.out'],(self.work/'before/27934/3.out').read_bytes())
        self.assertFalse((self.root/'collab/gmyhf-review-fixes-batch14.json').exists())

    def test_apply_retry_preserves_others_and_original_backup(self):
        self.apply();self.apply()
        self.assertEqual(['3.in'],self.uploads)
        self.assertEqual({**self.original,'3.in':self.new,'3.out':self.answer},self.live)
        self.assertEqual(b'orphan',(self.work/'before/27934/3.out').read_bytes())
        report=json.loads((self.root/'collab/gmyhf-review-fixes-batch14.json').read_text());g=report['problems'][0]
        self.assertTrue(report['applied'] and g['only_expected_files_added'] and g['configuration_unchanged'])
        self.assertEqual({'3.in'},set(g['final_files'])-set(g['before_files']))

    def test_existing_new_input_without_absence_proof_is_rejected(self):
        self.live['3.in']=self.new
        with self.assertRaises(ValueError):self.apply()
        self.assertEqual([],self.uploads)

    def test_original_file_drift_prevents_all_writes(self):
        repair.run(self.work)
        self.live['0.out']=b'changed'
        with self.assertRaises(ValueError):self.apply()
        self.assertEqual([],self.uploads)

    def test_failed_upload_never_claims_completion(self):
        def broken(s,n,name,data):self.live[name]=b'broken'
        with patch.object(repair.platform,'upload',side_effect=broken):
            with self.assertRaises(ValueError):self.apply()
        self.assertFalse((self.root/'collab/gmyhf-review-fixes-batch14.json').exists())
        self.assertFalse((self.work/'progress.json').exists())

    def test_configuration_change_stops_completion_then_retry_resumes(self):
        self.hook=lambda:setattr(self,'title','changed') if '3.in' in self.live else None
        with self.assertRaises(ValueError):self.apply()
        self.assertEqual(['3.in'],self.uploads);self.assertEqual(b'orphan',self.live['3.out'])
        self.title='original';self.hook=None;self.apply()
        self.assertEqual(['3.in'],self.uploads)

    def test_changed_new_input_never_claims_completion(self):
        def changed():
            if '3.in' in self.live:self.live['3.in']=b'changed'
        self.hook=changed
        with self.assertRaises(ValueError):self.apply()
        self.assertEqual(['3.in'],self.uploads);self.assertEqual(b'orphan',self.live['3.out'])

    def test_final_unrelated_file_drift_never_claims_completion(self):
        original=self.upload
        def corrupt(s,n,name,data):
            original(s,n,name,data)
            if name=='3.in':self.live['0.out']=b'changed'
        with patch.object(repair.platform,'upload',side_effect=corrupt):
            with self.assertRaises(ValueError):self.apply()
        self.assertFalse((self.root/'collab/gmyhf-review-fixes-batch14.json').exists())

    def test_modified_absence_binding_prevents_writes(self):
        repair.run(self.work)
        path=self.work/'before/27934/absence.json';record=json.loads(path.read_text());record['rules_sha256']='changed';path.write_text(json.dumps(record))
        with self.assertRaises(ValueError):self.apply()
        self.assertEqual([],self.uploads)
