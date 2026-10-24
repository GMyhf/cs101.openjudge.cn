"""自写参考的语言调度与真实编译；夹具不依赖抓取数据。"""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import repair_gmyhf_review_findings as repair


def cpp_works():
    try:
        with tempfile.TemporaryDirectory() as work:
            binary=Path(work)/'probe'
            result=subprocess.run(['g++','-x','c++','-','-o',str(binary)],
                                  input=b'int main(){return 0;}',capture_output=True,timeout=20)
            return result.returncode==0 and subprocess.run([str(binary)],capture_output=True,timeout=5).returncode==0
    except (OSError,subprocess.TimeoutExpired):
        return False


HAS_CPP=cpp_works()


class ReferenceCommandTests(unittest.TestCase):
    def test_python_isolated_and_unknown_language_rejected(self):
        with tempfile.TemporaryDirectory() as work:
            target=Path(work)
            ref,command=repair.reference_command('print(int(input())+1)','python3',target)
            self.assertEqual([sys.executable,'-I',str(ref)],command)
            self.assertEqual(b'42\n',subprocess.run(command,input=b'41',capture_output=True,check=True).stdout)
            with self.assertRaises(ValueError):repair.reference_command('','ruby',target)

    @unittest.skipUnless(HAS_CPP,'本机不能编译并运行C++')
    def test_cpp_prepare_recomputes_changed_case_and_uses_cpp_judge(self):
        source='#include <iostream>\nint main(){long long n,m,k,v,s=0;std::cin>>n>>m>>k;for(int i=0;i<n*m;++i){std::cin>>v;s+=v;}std::cout<<s<<"\\n";}\n'
        with tempfile.TemporaryDirectory() as work:
            root=Path(work);base=root/'data/openjudge/tests/admin_download/31241';base.mkdir(parents=True)
            before=b'2 2 1\n1000000000 1\n1 0\n1 2\n';answer=b'1000000002\n'
            for name,data in [('19.in',before),('19.out',answer)]: (base/name).write_bytes(data)
            hashes={name:repair.sha(data) for name,data in [('19.in',before),('19.out',answer)]}
            entry={'global_number':31241,'authored_reference':{'source':source,'sha256':repair.sha(source.encode()),'language':'cpp'},
                   'checks':{'readback':{'files':[{'filename':n,'sha256':v} for n,v in hashes.items()]},
                             'answers':{'files':[{'input':'19.in','output':'19.out','input_sha256':hashes['19.in'],'output_sha256':hashes['19.out']}]}}}
            evidence=root/'collab/gmyhf-31241-admin-form-review.json';evidence.parent.mkdir();evidence.write_text(json.dumps({'entries':[entry]}))
            receipt={'status':'Accepted','timing_audit':{'status':'passed'}}
            with patch.object(repair,'ROOT',root),patch.object(repair.judge,'judge',return_value=receipt) as judge:
                groups=repair.prepare(12,root/'work')
            group=groups[0][0];target=root/group['local_dataset']
            self.assertEqual('cpp',group['reference_language'])
            self.assertEqual('reference.cpp',group['reference_file'])
            self.assertEqual(source,(target/'reference.cpp').read_text())
            self.assertEqual(b'500000002\n',(target/'data/19.out').read_bytes())
            self.assertEqual('cpp',judge.call_args.args[2])
            self.assertEqual(source,judge.call_args.args[3])
            self.assertEqual({'19.in','19.out'},{c['filename'] for c in group['changes']})
            entry['authored_reference']['sha256']='0'*64;evidence.write_text(json.dumps({'entries':[entry]}))
            with patch.object(repair,'ROOT',root),patch.object(repair,'reference_command') as command:
                with self.assertRaises(ValueError):repair.prepare(12,root/'work')
                command.assert_not_called()

    @unittest.skipUnless(HAS_CPP,'本机不能编译并运行C++')
    def test_failed_compilation_never_returns_stale_binary(self):
        with tempfile.TemporaryDirectory() as work:
            target=Path(work)
            repair.reference_command('int main(){return 0;}','cpp',target)
            with self.assertRaises(ValueError):repair.reference_command('这不是C++源码','cpp',target)
