"""语义验收以独立小域穷举校准；不读取抓取数据、不改题库配置。"""
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import gmyhf_semantic_checkers as checks
import gmyhf_review_fixes as rules
import repair_gmyhf_review_findings as repair


def max_path_mex(n, edges, labels):
    graph = [[] for _ in range(n)]
    for (u, v), label in zip(edges, labels):
        graph[u-1].append((v-1, label)); graph[v-1].append((u-1, label))
    answer = 0
    for start in range(n):
        queue = [(start, -1, frozenset())]
        while queue:
            v, parent, path = queue.pop()
            mex = 0
            while mex in path: mex += 1
            answer = max(answer, mex)
            queue.extend((u, v, path | {label}) for u, label in graph[v] if u != parent)
    return answer


def prufer_edges(n, sequence):
    degrees = [1] * n
    for v in sequence: degrees[v] += 1
    result = []
    for v in sequence:
        leaf = next(i for i, degree in enumerate(degrees) if degree == 1)
        result.append((leaf+1, v+1)); degrees[leaf] -= 1; degrees[v] -= 1
    if n > 1: result.append(tuple(i+1 for i, degree in enumerate(degrees) if degree == 1))
    return result


def brute_words(words):
    dictionary = set(words); result = set()
    for word in words:
        for cuts in itertools.product((False, True), repeat=len(word)-1):
            pieces = []; start = 0
            for i, cut in enumerate(cuts, 1):
                if cut: pieces.append(word[start:i]); start = i
            pieces.append(word[start:])
            if len(pieces) >= 2 and all(piece in dictionary for piece in pieces):
                result.add(word); break
    return result


class SemanticCheckerTests(unittest.TestCase):
    def test_mex_against_all_small_labelled_trees_and_all_label_permutations(self):
        count = 0
        for n in range(1, 6):
            for sequence in itertools.product(range(n), repeat=max(0, n-2)):
                edges = prufer_edges(n, sequence)
                given = str(n)+'\n'+'\n'.join(f'{u} {v}' for u, v in edges)
                scores = [(labels, max_path_mex(n, edges, labels)) for labels in itertools.permutations(range(n-1))]
                optimum = min(score for _, score in scores)
                for labels, score in scores:
                    self.assertEqual(score == optimum, checks.mex_tree(given, ' '.join(map(str, labels))),
                                     (given, labels, score, optimum))
                    count += 1
        self.assertGreater(count, 3000)

    def test_mex_rejects_invalid_tree_labels_and_large_steiner_path(self):
        given = '5\n1 2\n2 3\n3 4\n2 5\n'
        for answer in ('0 1 2 3', '0 0 1 2', '0 1 2', '0 1 2 3 4', '-1 0 1 2', 'x', '9'*5000):
            self.assertFalse(checks.mex_tree(given, answer))
        self.assertFalse(checks.mex_tree('3 1 2 2 3', '0 0'))
        self.assertTrue(checks.mex_tree(given, '0 1 3 2'))
        for bad in ('0', '10001', '3 1 2 1 2', '3 1 1 1 2', '3 0 2 1 3', '3 1 4 1 2', '3 1 2'):
            self.assertFalse(checks.mex_tree(bad, '0 1'))
        # 三条低标号边不必共用一个顶点，剪叶判据须接受中间带长臂的分叉。
        given = '7\n1 2\n2 3\n1 4\n4 5\n1 6\n6 7'
        self.assertTrue(checks.mex_tree(given, '3 0 4 1 5 2'))
        self.assertFalse(checks.mex_tree(given, '0 1 2 3 4 5'))

    def test_words_against_all_segment_partitions_and_output_orders(self):
        vocabulary = ['a', 'b', 'aa', 'ab', 'ba', 'aaa', 'aab']
        for mask in range(1, 1 << len(vocabulary)):
            words = [w for i, w in enumerate(vocabulary) if mask & (1 << i)]
            expected = sorted(brute_words(words)); given = ' '.join(words)
            for answer in itertools.permutations(expected):
                self.assertTrue(checks.concatenated_words(given, ' '.join(answer) if answer else 'None'))
            if expected:
                self.assertFalse(checks.concatenated_words(given, ' '.join(expected[:-1])))
                self.assertFalse(checks.concatenated_words(given, ' '.join(expected+[expected[0]])))
                self.assertFalse(checks.concatenated_words(given, 'None'))
            else:
                self.assertFalse(checks.concatenated_words(given, ''))
            self.assertFalse(checks.concatenated_words(given, ' '.join(expected+['zzzz'])))

    def test_words_reject_invalid_input_and_handle_self_repetition(self):
        for given in ('', 'a a aa', 'A a', '中', 'a1', 'a'*31, ' '.join(['a']*10001)):
            self.assertFalse(checks.concatenated_words(given, 'None'))
        self.assertFalse(checks.concatenated_words('a a aa', 'aa'))
        self.assertTrue(checks.concatenated_words('a aa aaa', 'aaa aa'))
        self.assertFalse(checks.concatenated_words('a aa aaa', 'a aa aaa'))
        self.assertTrue(checks.concatenated_words('a'*30, 'None'))
        self.assertTrue(checks.concatenated_words('a '+'a'*30, 'a'*30))
        self.assertFalse(checks.concatenated_words('cat dog', 'none'))
        self.assertFalse(checks.concatenated_words('cat dog', 'None None'))

    def test_repairs_preserve_forest_and_first_word_occurrence(self):
        before = b'6\n2 3\n3 4\n4 2\n5 6\n6 5\n'
        self.assertEqual(b'6\n2 3\n3 4\n5 6\n1 2\n1 5\n', rules.repair_input(27952, before))
        given = b'4\r\n1 2\r\n1 3\r\n1 4\r\n'
        self.assertIs(given, rules.repair_input(27952, given))
        self.assertEqual(b'1\r\n', rules.repair_input(27952, b'1\r\n'))
        self.assertEqual(b'bb a aa\n', rules.repair_input(28341, b'bb a bb aa a'))
        given = b'bb  a\r\naa\r\n'
        self.assertIs(given, rules.repair_input(28341, given))
        for number, given in ((27952,b'0'),(27952,b'10001'),(27952,b'3 1 2'),(28341,b''),
                              (28341,b'A'),(28341,b'a1'),(28341,b'a'*31)):
            with self.assertRaises(AssertionError): rules.repair_input(number, given)

    def test_copied_cli_accepts_alternative_answers_and_rejects_wrong_bytes(self):
        with tempfile.TemporaryDirectory() as work:
            root = Path(work); given = root/'input'; actual = root/'actual'; expected = root/'expected'
            expected.write_text('无关参考文本')
            for number, text, accepted, rejected in ((27952,'4 1 2 1 3 1 4','2 1 0','0 0 1'),
                                                     (28341,'a aa aaa','aaa aa','a aa aaa')):
                checker = root/'checker.py'
                checker.write_text(Path(checks.__file__).read_text()+f'\nif __name__ == "__main__": checker_main({number})\n')
                given.write_text(text)
                for answer, status in ((accepted,0),(rejected,42)):
                    actual.write_text(answer)
                    result = subprocess.run([sys.executable,'-I',str(checker),str(given),str(actual),str(expected)],capture_output=True)
                    self.assertEqual(status, result.returncode, result.stderr)
                actual.write_bytes(b'\xff')
                self.assertEqual(42,subprocess.run([sys.executable,'-I',str(checker),str(given),str(actual),str(expected)],capture_output=True).returncode)

    def test_prepare_uses_local_checker_preserves_alternative_stored_answers(self):
        with tempfile.TemporaryDirectory() as work:
            root = Path(work); entries = []
            sources = {27952:'print("0 1 2")\n',28341:'print("aa")\n'}
            for number in (27952,28341):
                base = root/f'data/openjudge/tests/admin_download/{number}'; base.mkdir(parents=True)
                fixtures = ([(b'4 1 2 2 3 3 1',b'old')]*8+[(b'4 1 2 1 3 1 4',b'2 1 0')]
                            if number==27952 else [(b'a aa aa',b'aa aa'),(b'aa a aaa',b'aaa aa')])
                files = []; records = []
                for i,(given,answer) in enumerate(fixtures):
                    for name,payload in ((f'{i}.in',given),(f'{i}.out',answer)):
                        (base/name).write_bytes(payload); files.append({'filename':name,'sha256':repair.sha(payload)})
                    records.append({'input':f'{i}.in','output':f'{i}.out','input_sha256':repair.sha(given),'output_sha256':repair.sha(answer)})
                entries.append({'global_number':number,'authored_reference':{'source':sources[number],'sha256':repair.sha(sources[number].encode())},
                                'checks':{'readback':{'files':files},'answers':{'files':records}}})
            evidence = root/'collab/gmyhf-pending-batch13-review.json'; evidence.parent.mkdir(); evidence.write_text(json.dumps({'entries':entries}))
            observed = []
            def judge(*args,**kwargs):
                item = repair.judge.catalog_item('practice',args[1]); observed.append(item)
                self.assertTrue((root/'data/openjudge'/item['checker']).is_file())
                return {'status':'Accepted','timing_audit':{'status':'passed'}}
            with patch.object(repair,'ROOT',root),patch.object(repair.judge,'MIRROR',root/'data/openjudge'),patch.object(repair.judge,'judge',side_effect=judge):
                groups = repair.prepare(16,root/'work')
            self.assertEqual(2,len(observed))
            # 原答案即使输入未改，也必须通过语义；不可仅校新生成的答案。
            bad = entries[0]['checks']['answers']['files'][-1]
            bad['output_sha256'] = repair.sha(b'0 0 1')
            for row in entries[0]['checks']['readback']['files']:
                if row['filename'] == '8.out': row['sha256'] = bad['output_sha256']
            (root/'data/openjudge/tests/admin_download/27952/8.out').write_bytes(b'0 0 1')
            evidence.write_text(json.dumps({'entries':entries}))
            with patch.object(repair,'ROOT',root),patch.object(repair.judge,'MIRROR',root/'data/openjudge'),patch.object(repair.judge,'judge',side_effect=judge):
                with self.assertRaises(ValueError): repair.prepare(16,root/'work')
            for group,_ in groups:
                target=root/group['local_dataset']; n=group['global_number']; i=8 if n==27952 else 1
                self.assertEqual(b'2 1 0' if n==27952 else b'aaa aa',(target/f'data/{i}.out').read_bytes())
                self.assertEqual(repair.sha(Path(checks.__file__).read_bytes()),group['semantic_checker']['rules_sha256'])
                self.assertEqual(group['semantic_checker']['source'],(target/'checker.py').read_text())
                self.assertEqual(group['semantic_checker']['sha256'],repair.sha((target/'checker.py').read_bytes()))
