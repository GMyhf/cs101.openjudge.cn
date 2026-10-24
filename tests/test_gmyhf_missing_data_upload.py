"""补数据只能增加已审核文件；默认不写，禁止改题号、配置或覆盖漂移文件。"""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import upload_gmyhf_missing_data as uploader


class FakeSession:
    def __init__(self):
        self.files={};self.selected=set();self.posts=[];self.title='原题';self.number=31200

    def _get(self,url):
        html=(f'<form action="/api/global-problem/modify/"><input name="problemId" value="{self.number}">'
              f'<input name="title" value="{self.title}"><input name="timeLimit" value="1000">')
        for name in self.files:
            html+=f'<input name="filenames[{name}]" value="{int(name in self.selected)}">'
        html+='</form>'
        for name in self.files:html+=f'<a href="/admin/download?problem_id={self.number}&amp;filename={name}">下载</a>'
        return html

    def _post(self,url,fields):
        if not url.endswith('/api/global-problem/modify/'):raise AssertionError(url)
        self.posts.append(dict(fields));self.selected={n for n in self.files if fields.get(f'filenames[{n}]')=='1'}
        return '{"result":"SUCCESS"}'


class MissingDataUploadTests(unittest.TestCase):
    def setUp(self):
        self.work=tempfile.TemporaryDirectory();self.addCleanup(self.work.cleanup)
        self.paths=[]
        for i in range(21):
            for extension,body in (('in',b'100 500\n'),('out',b'153 370 371 407\n')):
                p=Path(self.work.name)/f'{i}.{extension}';p.write_bytes(body);self.paths.append(p)
        self.session=FakeSession();self.baseline=uploader.fields_digest(uploader.common.platform.parse_form(self.session._get('')))
        self.uploads=[]

    def run_sync(self,apply=False):
        def upload(session,number,name,payload):
            self.assertIs(session,self.session);self.assertEqual(31200,number)
            self.uploads.append(name);session.files[name]=payload
        with patch.object(uploader.common.platform,'upload',side_effect=upload), \
                patch.object(uploader.common.platform,'download',side_effect=lambda s,n,name:s.files[name]):
            return uploader.sync_problem(self.session,31200,self.paths,self.baseline,apply)

    def test_plan_upload_selection_and_resume(self):
        plan=self.run_sync();self.assertFalse(plan['applied']);self.assertEqual([],self.uploads)
        self.assertEqual([],self.session.posts)
        report=self.run_sync(True)
        self.assertTrue(report['applied']);self.assertTrue(report['all_files_readback_matched'])
        self.assertEqual(42,len(self.uploads));self.assertEqual(42,len(self.session.selected))
        self.assertEqual(1,len(self.session.posts));self.assertEqual('原题',self.session.posts[0]['title'])
        repeated=self.run_sync(True)
        self.assertEqual([],repeated['planned_new_files']);self.assertEqual(42,len(self.uploads))
        self.assertEqual(1,len(self.session.posts))

    def test_changed_form_wrong_number_or_existing_data_stops_before_write(self):
        for kind in ('form','number','contents','unexpected_file'):
            with self.subTest(kind=kind):
                self.session=FakeSession()
                if kind=='form':self.session.title='上游已改题'
                elif kind=='number':self.session.number=31201
                elif kind=='contents':self.session.files['0.out']=b'wrong\n'
                else:self.session.files['attachment.py']=b'not executable'
                with self.assertRaises(ValueError):self.run_sync(True)
                self.assertEqual([],self.uploads);self.assertEqual([],self.session.posts)

    def test_incomplete_local_files_rejected(self):
        self.paths.pop()
        with self.assertRaisesRegex(ValueError,'不完整'):self.run_sync(True)
        self.assertEqual([],self.uploads)

    def test_corrupted_uploaded_body_is_rejected(self):
        def corrupt(session,number,name,payload):session.files[name]=b'bad\n'
        with patch.object(uploader.common.platform,'upload',side_effect=corrupt), \
                patch.object(uploader.common.platform,'download',side_effect=lambda s,n,name:s.files[name]):
            with self.assertRaisesRegex(ValueError,'回读哈希不符'):
                uploader.sync_problem(self.session,31200,self.paths,self.baseline,True)
        self.assertEqual([],self.session.posts)


if __name__=='__main__':unittest.main()
