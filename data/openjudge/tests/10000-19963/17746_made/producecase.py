import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='// External reference: cs101.openjudge.cn practice/17746 statistics, Accepted solution 52515040.\n// Source: http://cs101.openjudge.cn/practice/solution/52515040/\n// Statistics: http://cs101.openjudge.cn/practice/17746/statistics/\n// License: not declared on submission page; no license inferred\n#include<iostream>\n#include<cstdio>\n#include<string>\n#include<cstring>\n#include<vector>\n#include<queue>\n#include<stack>\n#include<unordered_map>\n#include<unordered_set>\n#include<algorithm>\n#include<climits>\n#include<sstream>\n#include<set>\n#include<map>\n\nusing namespace std;\n\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    int n, m, c;\n    cin >> n >> m >> c;\n    vector<int> v(n + 1);\n    for (int i = 1;i <= n;++i)cin >> v[i];\n    deque<int> max_st, min_st;\n    bool flag = false;\n    for (int i = 1;i <= n;++i) {\n        while (!max_st.empty() && v[i] > max_st.back()) {\n            max_st.pop_back();\n        }\n        max_st.push_back(v[i]);\n        if (i > m) {\n            if (v[i - m] == max_st.front()) {\n                max_st.pop_front();\n            }\n        }\n        while (!min_st.empty() && v[i] < min_st.back()) {\n            min_st.pop_back();\n        }\n        min_st.push_back(v[i]);\n        if (i > m) {\n            if (v[i - m] == min_st.front()) {\n                min_st.pop_front();\n            }\n        }\n        if (i >= m) {\n            if (max_st.front() - min_st.front() <= c) {\n                cout << i-m+1 << \'\\n\';\n                flag = true;\n            }\n        }\n    }\n    if (!flag)cout << "NONE";\n    return 0;\n}\n'
LANGUAGE='G++'
SAMPLE='7 2 0\n0 1 1 2 3 2 2\n'
GENERATOR_NAME='g17746'
def g17746(r):
    n=r.randint(5,60); m=r.randint(1,min(10,n)); c=r.randint(0,20)
    return f"{n} {m} {c}\n"+" ".join(str(r.randint(0,100)) for _ in range(n))+"\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        d=Path(d); src=d/'main.cpp'
        src.write_text(REFERENCE); cmd=[sys.executable,str(src)]
        if LANGUAGE=="G++":
            exe=d/"main"; subprocess.run(["g++","-std=c++17","-O2",str(src),"-o",str(exe)],check=True)
            cmd=[str(exe)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text)
        (data/f"{i}.out").write_text(run(text))
if __name__=="__main__": main()
