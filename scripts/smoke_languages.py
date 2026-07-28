#!/usr/bin/env python3
"""对每一种提交语言跑一次端到端冒烟：正确解要出正确答案，坏代码要出 Compile Error。

为什么需要它：`judge.prepare_program` 里**每种语言各有一条分支**，而
`tests/test_judge.py` 里 .NET / Swift / Objective-C 的用例都带
`@skipUnless(shutil.which(...))` —— 在没装工具链的机器上是**静默跳过**的。
闸门全绿并不代表那几条分支被验过。

2026-07-28 的教训：T-010 把 `prepare_program` 抽出去时，gcc/g++ 分支有一句
`return` 漏改成二元组，导致 C/C++ 编译错误把服务端打成 500，闸门全绿了整整一轮，
最后是读代码时偶然发现的。这个脚本就是把「每条分支都真的跑一次」变成一条命令。

走 `/api/run`（运行样例）而不是 `/api/submit`：两者共用同一个 `prepare_program`
和同一套沙箱，但运行样例**不写 submissions 表**，不会往判题记录里灌测试数据。

用法（在部署机上跑）：

    CS101_SMOKE_USER=GMyhf CS101_SMOKE_PASSWORD=... python3 scripts/smoke_languages.py

可选：`--base http://127.0.0.1:8000`、`--book practice`、`--problem 02942`。
退出码 0 表示全部通过。
"""
import argparse
import http.cookiejar
import json
import os
import sys
import urllib.error
import urllib.request

# 02942「吃糖果」：读一个 n，输出斐波那契第 n 项（每天吃 1 或 2 块的方案数）。
# 选它是因为输入输出都极短，各语言实现都能一眼看懂。
SAMPLE_INPUT = "4"
EXPECTED = "5"

WORKING = {
    "python": "n=int(input())\na,b=1,1\nfor _ in range(n):\n    a,b=b,a+b\nprint(a)\n",
    "pypy3": "n=int(input())\na,b=1,1\nfor _ in range(n):\n    a,b=b,a+b\nprint(a)\n",
    "c": '#include <stdio.h>\nint main(){int n,i;long a=1,b=1,t;scanf("%d",&n);'
         'for(i=0;i<n;i++){t=a+b;a=b;b=t;}printf("%ld\\n",a);return 0;}\n',
    "cpp": '#include <cstdio>\nint main(){int n,i;long a=1,b=1,t;scanf("%d",&n);'
           'for(i=0;i<n;i++){t=a+b;a=b;b=t;}printf("%ld\\n",a);return 0;}\n',
    "objc": '#include <stdio.h>\nint main(){int n,i;long a=1,b=1,t;scanf("%d",&n);'
            'for(i=0;i<n;i++){t=a+b;a=b;b=t;}printf("%ld\\n",a);return 0;}\n',
    "csharp": 'using System;\nclass Program{static void Main(){'
              'int n=int.Parse(Console.ReadLine().Trim());long a=1,b=1;'
              'for(int i=0;i<n;i++){long t=a+b;a=b;b=t;}Console.WriteLine(a);}}\n',
    "fsharp": '[<EntryPoint>]\nlet main _ =\n'
              '    let n = int ((System.Console.ReadLine()).Trim())\n'
              '    let mutable a = 1L\n    let mutable b = 1L\n'
              '    for _ in 1 .. n do\n'
              '        let t = a + b\n        a <- b\n        b <- t\n'
              '    printfn "%d" a\n    0\n',
    "vbnet": 'Module Program\n    Sub Main()\n'
             '        Dim n As Integer = Integer.Parse(System.Console.ReadLine().Trim())\n'
             '        Dim a As Long = 1\n        Dim b As Long = 1\n'
             '        For i As Integer = 1 To n\n'
             '            Dim t As Long = a + b\n            a = b\n            b = t\n'
             '        Next\n        System.Console.WriteLine(a)\n'
             '    End Sub\nEnd Module\n',
    "swift": 'import Foundation\n'
             'let n = Int(readLine()!.trimmingCharacters(in: .whitespacesAndNewlines))!\n'
             'var a = 1, b = 1\nfor _ in 0..<n { let t = a + b; a = b; b = t }\nprint(a)\n',
}

# 每种语言一份**编译期**就该失败的代码。这一路正是 C/C++ 那个 bug 藏身的地方。
BROKEN = {
    "python": "def broken(:\n    pass\n",
    "pypy3": "def broken(:\n    pass\n",
    "c": "int main(){ this is not valid c }\n",
    "cpp": "int main(){ this is not valid c++ }\n",
    "objc": "int main(){ this is not valid objective c }\n",
    "csharp": "class Program { static void Main() { this is not c# } }\n",
    "fsharp": "let main _ = this is not f#\n",
    "vbnet": "Module Program\n    Sub Main()\n        this is not vb\n    End Sub\nEnd Module\n",
    "swift": "func broken( { this is not swift }\n",
}

ORDER = ["python", "pypy3", "cpp", "c", "csharp", "fsharp", "vbnet", "swift", "objc"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="http://127.0.0.1:8000")
    parser.add_argument("--book", default="practice")
    parser.add_argument("--problem", default="02942")
    parser.add_argument("--require-all", action="store_true",
                        help="工具链缺失也算失败。部署机上应当加这个 —— "
                             "「静默跳过」正是 PyPy3 那次回归藏身的方式")
    options = parser.parse_args()

    user = os.environ.get("CS101_SMOKE_USER")
    password = os.environ.get("CS101_SMOKE_PASSWORD")
    if not user or not password:
        print("需要 CS101_SMOKE_USER 与 CS101_SMOKE_PASSWORD 环境变量", file=sys.stderr)
        return 2

    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

    def post(path, payload, timeout=180):
        request = urllib.request.Request(
            options.base + path, data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"})
        try:
            response = opener.open(request, timeout=timeout)
            return response.status, json.loads(response.read())
        except urllib.error.HTTPError as error:
            try:
                return error.code, json.loads(error.read())
            except ValueError:
                return error.code, {}

    status, _ = post("/api/user/login", {"username": user, "password": password})
    if status != 200:
        print(f"登录失败：HTTP {status}", file=sys.stderr)
        return 2

    failures = []
    print(f"{'语言':<9} {'正确解':<26} {'坏代码':<26}")
    print("-" * 64)
    for language in ORDER:
        base = {"book": options.book, "problem": options.problem, "language": language}
        _, good = post("/api/run", {**base, "source": WORKING[language], "stdin": SAMPLE_INPUT})
        _, bad = post("/api/run", {**base, "source": BROKEN[language], "stdin": SAMPLE_INPUT})

        good_status, produced = good.get("status"), (good.get("stdout") or "").strip()
        if good_status == "Language Unavailable":
            if options.require_all:
                good_note, good_ok = "✗ 工具链不可用", False
            else:
                good_note, good_ok = "工具链未安装（跳过）", None
        elif good_status == "OK" and produced == EXPECTED:
            good_note, good_ok = f"OK  输出 {produced}", True
        else:
            good_note, good_ok = f"✗ {good_status} 输出 {produced!r}", False

        bad_status = bad.get("status")
        if good_ok is None:
            bad_note, bad_ok = "—", None
        elif bad_status == "Compile Error":
            bad_note, bad_ok = "Compile Error ✓", True
        else:
            bad_note, bad_ok = f"✗ 期望 Compile Error，得到 {bad_status}", False

        print(f"{language:<9} {good_note:<26} {bad_note:<26}")
        if good_ok is False and good_status == "Language Unavailable":
            failures.append(f"{language}：服务进程看不到工具链（检查 systemd 单元里的 PATH）")
        elif good_ok is False:
            failures.append(f"{language} 正确解：{good_status} 输出 {produced!r}")
        if bad_ok is False:
            failures.append(f"{language} 坏代码：期望 Compile Error，得到 {bad_status}")

    print("-" * 64)
    if failures:
        print(f"\n{len(failures)} 项失败：")
        for item in failures:
            print("  -", item)
        return 1
    print("全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
