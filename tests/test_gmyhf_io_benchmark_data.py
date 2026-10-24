"""完整300万行平台夹具，不能用小样例替代大数据，也不能接入本地2MiB判题。"""
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts import gmyhf_io_benchmark_data as benchmark
from scripts import materialize_gmyhf_downloads as materializer


class IoBenchmarkDataTests(unittest.TestCase):
    def test_complete_unique_input_and_reference_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);report=benchmark.build(root)
            self.assertEqual(list(range(31028,31033)),report['problems'])
            self.assertEqual(1,report['cases_per_problem'])
            self.assertFalse(report['local_enabled'])
            size=sum(len(str(i))+1 for i in range(1,3_000_001))
            self.assertEqual(size,(root/'0.in').stat().st_size)
            self.assertGreater(size,2*1024*1024)
            self.assertTrue(benchmark.validate_file(root/'0.in'))
            reference=root/'samplecode.py';actual=root/'actual.out'
            with (root/'0.in').open('rb') as given,actual.open('wb') as output:
                completed=subprocess.run([sys.executable,'-I',str(reference)],stdin=given,stdout=output,timeout=20)
            self.assertEqual(0,completed.returncode)
            self.assertEqual(benchmark.digest(root/'0.out'),benchmark.digest(actual))
            with (root/'0.in').open('r+b') as stream:stream.write(b'0\n')
            self.assertFalse(benchmark.validate_file(root/'0.in'))
            for payload in (b'1\n',b'01\n',b'1\n2\nextra\n'):
                (root/'invalid.in').write_bytes(payload)
                self.assertFalse(benchmark.validate_file(root/'invalid.in'))


    def test_future_mapping_still_excludes_full_size_benchmark_outputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);downloads=root/'tests/admin_download';downloads.mkdir(parents=True)
            (root/'collab').mkdir();(root/'collab/valid-contracts.json').write_text('{"dirs": []}')
            files=[{'filename':name,'bytes':22_888_896,'sha256':'0'*64} for name in ('0.in','0.out')]
            manifest={'fetched_at':'fixture','problems':{str(n):{'files':files} for n in range(31028,31033)}}
            (downloads/'manifest.json').write_text(json.dumps(manifest));report=root/'report.json'
            with patch.multiple(materializer,ROOT=root,TESTS=root/'tests',DL=downloads,REPORT=report), \
                    patch.object(materializer,'local_id_map',return_value={n:str(n) for n in range(31028,31033)}), \
                    patch.object(materializer,'load_repairs',return_value={}), \
                    patch.object(materializer,'repair_pair',side_effect=AssertionError('不能接入本地')) as repair, \
                    contextlib.redirect_stdout(io.StringIO()):
                materializer.main();repair.assert_not_called()
            result=json.loads(report.read_text())
            self.assertEqual([],result['materialized'])
            self.assertEqual(set(range(31028,31033)),{r['global_number'] for r in result['skipped']['output_over_2MiB']})


if __name__=='__main__':unittest.main()
