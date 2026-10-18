"""Author, publish and judge function-only problems through the normal sandbox."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

import judge
from tools import configure_function_problem as configure
from tools import activate_private_problems as private
from tools import activate_codeforces_rebuilds as codeforces

EXAMPLES = Path(__file__).resolve().parents[1] / "examples/function-submission"


class FunctionSubmissionTests(unittest.TestCase):
    def setUp(self):
        work = tempfile.TemporaryDirectory()
        self.addCleanup(work.cleanup)
        self.mirror = Path(work.name)
        self.directory = self.mirror / "tests/private/1000002_made"
        data = self.directory / "data"
        data.mkdir(parents=True)
        for index, (stdin, stdout) in enumerate((("2 3\n", "5\n"), ("10 20\n", "30\n"))):
            (data / f"{index}.in").write_text(stdin)
            (data / f"{index}.out").write_text(stdout)
        (self.directory / "producecase.py").write_text("# fixture\n")
        (self.directory / "samplecode.py").write_text((EXAMPLES / "python/solution.py").read_text())
        (self.mirror / "pages").mkdir()
        (self.mirror / "pages/private__1000002.html").write_text("fixture")
        self.catalog = self.mirror / "catalog.json"
        cases = [{"input": str(p.relative_to(self.mirror)),
                  "output": str(p.with_suffix('.out').relative_to(self.mirror))}
                 for p in sorted(data.glob('*.in'))]
        self.catalog.write_text(json.dumps({"count": 1, "problems": [{
            "book": "private", "id": "1000002", "source": "private", "test_cases": cases}]}))
        patcher = patch.object(judge, "LIMITS_CACHE", {})
        patcher.start()
        self.addCleanup(patcher.stop)
        for module in (configure, judge, private):
            patcher = patch.object(module, "MIRROR", self.mirror)
            patcher.start()
            self.addCleanup(patcher.stop)
        patcher = patch.object(private, "CATALOG", self.catalog)
        patcher.start()
        self.addCleanup(patcher.stop)

    def configure(self, language="python"):
        folder = "cpp" if language == "cpp" else "python"
        extension = "cpp" if language == "cpp" else "py"
        return configure.configure("private", "1000002", EXAMPLES / folder / f"prefix.{extension}",
                                   EXAMPLES / folder / f"suffix.{extension}", [language],
                                   EXAMPLES / "samples.json")

    def test_python_function_runs_samples_and_hidden_tests_after_publication(self):
        before = [p.read_bytes() for p in sorted((self.directory / "data").iterdir())]
        with patch.object(sys, "argv", ["configure_function_problem.py", "private", "1000002",
                "--prefix", str(EXAMPLES / "python/prefix.py"),
                "--suffix", str(EXAMPLES / "python/suffix.py"), "--languages", "python",
                "--samples", str(EXAMPLES / "samples.json")]):
            configure.main()
        # Also cover first publication from the on-disk configuration files.
        initial = json.loads(self.catalog.read_text())
        for key in ("code_prefix", "code_suffix", "code_languages", "sample_cases"):
            initial["problems"][0].pop(key, None)
        self.catalog.write_text(json.dumps(initial))
        with patch.object(sys, "argv", ["activate_private_problems.py", "private", "1000002"]):
            private.main()
        row = judge.catalog_item("private", "1000002")
        self.assertEqual(row["code_languages"], ["python"])
        self.assertEqual(row["sample_cases"], [{"input": "2 3\n", "output": "5\n"}])
        self.assertTrue(row["code_suffix"].endswith("/preset_suffix.py"))
        source = (EXAMPLES / "python/solution.py").read_text()
        self.assertEqual(judge.judge("private", "1000002", "python", source)["status"], "Accepted")
        sample = judge.run_sample("private", "1000002", "python", source, "2 3\n")
        self.assertEqual((sample["status"], sample["stdout"]), ("OK", "5\n"))
        self.assertEqual(judge.judge("private", "1000002", "python", "def add(a,b): return 5")["status"], "Wrong Answer")
        self.assertEqual(judge.judge("private", "1000002", "cpp", "int add(int a,int b){return a+b;}")["status"], "Language Unavailable")
        self.assertEqual(before, [p.read_bytes() for p in sorted((self.directory / "data").iterdir())])

    @unittest.skipUnless(shutil.which("g++"), "g++ unavailable")
    def test_cpp_function_compiles_with_its_own_prefix_and_suffix(self):
        self.configure("cpp")
        source = (EXAMPLES / "cpp/solution.cpp").read_text()
        result = judge.judge("private", "1000002", "cpp", source)
        self.assertEqual(result["status"], "Accepted", result)
        broken = judge.judge("private", "1000002", "cpp", "int add(int a,int b) {\nreturn missing;\n}")
        self.assertEqual(broken["status"], "Compile Error")
        self.assertIn("main.cpp:2:", broken["message"])

    def test_codeforces_republication_keeps_function_configuration(self):
        row = self.configure()
        row.update({"book": "codeforces", "id": "test"})
        unpublished = {key: value for key, value in row.items()
                       if key not in {"code_prefix", "code_suffix", "code_languages", "sample_cases"}}
        self.catalog.write_text(json.dumps({"count": 1, "problems": [unpublished]}))
        with patch.object(codeforces, "MIRROR", self.mirror), patch.object(codeforces, "CATALOG", self.catalog), \
                patch.object(codeforces, "cases_for", return_value=row["test_cases"]), \
                patch.object(codeforces, "allows_any_case", return_value=False), \
                patch.object(sys, "argv", ["activate_codeforces_rebuilds.py", "test"]):
            # The publisher resolves hooks from its normal Codeforces directory.
            destination = self.mirror / "tests/codeforces/test_made"
            destination.parent.mkdir()
            shutil.copytree(self.directory, destination)
            codeforces.main()
        published = json.loads(self.catalog.read_text())["problems"][0]
        self.assertEqual(published["code_languages"], ["python"])
        self.assertTrue(published["code_suffix"].endswith("test_made/preset_suffix.py"))
        self.assertEqual(published["sample_cases"], row["sample_cases"])

    def test_invalid_configuration_does_not_write_files_or_catalog(self):
        original = self.catalog.read_bytes()
        bad = self.mirror / "bad.json"
        for samples in ([], [{"input": 1, "output": "5"}], [{"input": "x" * 65537, "output": "5"}]):
            bad.write_text(json.dumps(samples))
            with self.assertRaises(ValueError):
                configure.configure("private", "1000002", EXAMPLES / "python/prefix.py",
                                    EXAMPLES / "python/suffix.py", ["python"], bad)
            self.assertEqual(self.catalog.read_bytes(), original)
            self.assertFalse((self.directory / "preset_code.py").exists())
        with self.assertRaisesRegex(ValueError, "提交语言"):
            configure.configure("private", "1000002", EXAMPLES / "python/prefix.py",
                                EXAMPLES / "python/suffix.py", ["unknown"], EXAMPLES / "samples.json")
