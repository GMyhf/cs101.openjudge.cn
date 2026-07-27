import random
REFERENCE='// External reference: /practice/30547/statistics/\n// Accepted submission: 52762423\n// Source: http://cs101.openjudge.cn/practice/solution/52762423/\n// License: not declared on the submission page; no license is inferred.\n\n#include <algorithm>\n#include <cstring>\n#include <iostream>\n#include <map>\n#include <vector>\nusing namespace std;\n\nint64_t memo1[51];\nint64_t count1(int64_t n) {\n  if (n == 0) return 1;\n  int64_t& ret = memo1[n];\n  if (ret) return ret;\n  for (int64_t a = 1; a <= n; a++)\n  for (int64_t c = 1; a*c <= n; c++) {\n    ret += count1(n - a*c);\n  }\n  return ret;\n}\n\n// Returns # of possible next elements for generated sequences matching "seq".\nmap<pair<vector<int64_t>, vector<int64_t>>, map<int64_t,int64_t>> memo;\nvector<int64_t> curc, cura;\nvector<tuple<vector<int64_t>, vector<int64_t>, vector<int64_t>>> saved;\nconst map<int64_t,int64_t>& count(vector<int64_t> seq, vector<int64_t> prev, bool save) {\n  static map<int64_t,int64_t> empty{}, base{{0,1}};\n  if (seq[0] == 0) {\n    for (int i = 1; i < seq.size(); i++) if (seq[i]) return empty;\n    if (save) {\n      vector<int64_t> curs = cura;\n      while (curs.size() < curc.size()+30) {\n        int64_t x = 0;  // There may be some overflow, but this shouldn\'t affect relative sorting.\n        for (int i = 0; i < curc.size(); i++) x += curs[curs.size()-curc.size()+i] * curc[i];\n        curs.push_back(x);\n      }\n      curs.erase(curs.begin(), curs.begin()+curc.size());\n      saved.push_back({curs, curc, cura});\n    }\n    return base;\n  }\n  for (auto x : seq) if (x <= 0) return empty;\n\n  if (seq.size() >= 2) {\n    vector<int64_t> seq2 = seq, prev2 = prev;\n    seq2.pop_back(); prev2.pop_back();\n    auto it = memo.find({seq2, prev2});\n    if (it == memo.end() || !it->second.count(seq.back())) return empty;\n  }\n\n  auto [it, inserted] = memo.insert({{seq, prev}, empty});\n  map<int64_t,int64_t>& ret = it->second;\n  if (save) { ret.clear(); inserted = true; }\n  if (!inserted) return ret;\n\n  prev.insert(prev.begin(), 0);\n  for (int64_t c = 1;   c <= seq[0]; c++)\n  for (int64_t a = 1; a*c <= seq[0]; a++) {\n    prev[0] = a;\n    for (int i = 0; i < seq.size(); i++) seq[i] -= prev[i]*c;\n    int64_t tmp = prev.back();\n    prev.pop_back();\n\n    if (save) { curc.insert(curc.begin(), c); cura.insert(cura.begin(), a); }\n    for (auto [v, n] : count(seq, prev, save)) ret[v + tmp*c] += n;\n    if (save) { curc.erase(curc.begin()); cura.erase(cura.begin()); }\n\n    prev.push_back(tmp);\n    for (int i = 0; i < seq.size(); i++) seq[i] += prev[i]*c;\n  }\n  return ret;\n}\n\nint main() {\n  int64_t N;\n  while (cin >> N) {\n    memo.clear(); cura.clear(); curc.clear(); saved.clear();\n\n    vector<int64_t> seq;\n    for (int64_t n = 1; ; n++) {\n      if (count1(n) < N) N -= count1(n); else { seq.push_back(n); break; }\n    }\n    while (seq.size() < 30 && seq.back() < 1e16) {\n      auto m = count(seq, seq, false);\n      int64_t tot = 0;\n      for (auto [v, n] : m) {\n        if (n < N) {\n          N -= n;\n        } else {\n          seq.push_back(v);\n          if (n <= 20) goto done;  // Small enough to brute force.\n          break;\n        }\n      }\n    }\ndone:\n\n    count(seq, seq, true);\n    sort(saved.begin(), saved.end());\n    auto [sv, cv, av] = saved[N-1];\n    cout << cv.size() << endl;\n    for (int i = 0; i < cv.size(); i++) { if (i) cout << \' \'; cout << cv[i]; }\n    cout << endl;\n    for (int i = 0; i < av.size(); i++) { if (i) cout << \' \'; cout << av[i]; }\n    cout << endl;\n    for (int i = 0; i < 10; i++) { if (i) cout << \' \'; cout << sv[i]; }\n    cout << endl;\n  }\n}'
SAMPLE='3\n'
GENERATOR_NAME='g30547'
CPP=True
def g30547(r): return f"{r.randint(1, 30)}\n"

from pathlib import Path
import subprocess, sys, tempfile
def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/('main.cpp' if CPP else 'main.py'); p.write_text(REFERENCE)
        if CPP:
            exe=Path(d)/'main'; c=subprocess.run(['g++','-O2','-std=c++17',str(p),'-o',str(exe)],capture_output=True,text=True,timeout=30)
            if c.returncode: raise SystemExit(c.stderr)
            cmd=[str(exe)]
        else: cmd=[sys.executable,str(p)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=120)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (data/f'{i}.in').write_text(c); (data/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
