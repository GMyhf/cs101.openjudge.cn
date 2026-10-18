"""Course-owned two-sum: retain official data and run function submissions safely."""
import importlib.util
import json
from pathlib import Path
import shutil
import unittest

import judge
from scripts import index_tests

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/openjudge/tests/30000-/31428_GMyhf'


class TwoSum31428Tests(unittest.TestCase):
    def test_official_data_and_catalog(self):
        spec = importlib.util.spec_from_file_location('verify_31428', DATA / 'verify.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.verify()['subcases'], 100)
        item = judge.catalog_item('practice', '31428')
        self.assertEqual(item['global_number'], 31428)
        self.assertEqual(item['test_count'], 1)
        self.assertTrue(item['code_suffix'].endswith('/preset_suffix.py'))
        self.assertEqual(item['sample_cases'], json.loads((DATA / 'samples.json').read_text()))
        hooks = index_tests.judge_hooks(item['test_cases'])
        for field in ('code_prefix', 'code_suffix', 'code_languages', 'sample_cases'):
            self.assertEqual(hooks[field], item[field])
        self.assertEqual(judge.problem_limits(31428)['total_ms'], 100)

    def test_python_function_and_all_public_samples(self):
        source = (DATA / 'samplecode.py').read_text()
        self.assertEqual(judge.judge('practice', '31428', 'python', source)['status'], 'Accepted')
        for case in json.loads((DATA / 'samples.json').read_text()):
            result = judge.run_sample('practice', '31428', 'python', source, case['input'])
            self.assertEqual(result['status'], 'OK', result)
            self.assertEqual(result['stdout'], case['output'])

    @unittest.skipUnless(shutil.which('g++'), 'g++ unavailable')
    def test_cpp_function_may_return_reversed_indices(self):
        source = (DATA / 'samplecode.cpp').read_text()
        result = judge.judge('practice', '31428', 'cpp', source)
        self.assertEqual(result['status'], 'Accepted', result)
        sample = judge.run_sample('practice', '31428', 'cpp', source, '4 9\n2 7 11 15\n0 0\n')
        self.assertEqual((sample['status'], sample['stdout']), ('OK', '0 1\n'))

    def test_wrong_function_and_unsupported_language_are_rejected(self):
        result = judge.judge('practice', '31428', 'python', 'def two_sum(nums, target):\n    return 0, 0\n')
        self.assertEqual(result['status'], 'Wrong Answer')
        self.assertEqual(judge.judge('practice', '31428', 'c', 'int main(){}')['status'], 'Language Unavailable')

    def test_python_runtime_error_points_to_student_line(self):
        result = judge.run_sample('practice', '31428', 'python', 'def two_sum(nums, target):\n    raise ValueError("probe")\n', '2 6\n3 3\n0 0\n')
        self.assertEqual(result['status'], 'Runtime Error')
        self.assertRegex(result['message'], r'main\.py", line 2\b')
