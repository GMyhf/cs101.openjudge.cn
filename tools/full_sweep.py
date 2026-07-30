#!/usr/bin/env python3
"""全库横扫：把「偶尔越出流程看一眼」变成每次跑闸门都做的事。

**为什么要有它。** 每轮复核问的是「这一轮怎么样」，而缺陷的范围是「这个仓库」。
2026-07-27 收官时我临时把全部报告扫了一遍，捞出两条挂了很久的：round5 的 4140 与
round9 的 15291 —— 它们的 `self_audit.failed` 一直非空，只是当轮没处理、之后每轮的
复核又只看当轮。`tools/check_pending_rework.py` 也管不到，因为它只管被显式记进
`pending_rework` 的项，而这两条当时根本没被记下来。

所以这里扫的是**已知失败模式在全库的残留**，每一条都对应一次真实事故：

  1. 任何轮次报告里 `self_audit.failed` 非空          （4140 / 15291）
  2. 退化约束：判据措辞像「非空」且反例是空串         （round14 的 27378 / 27778）
  3. `.out` 超过判题器 `RLIMIT_FSIZE` 2MB            （00000 因此被永久排除）
  4. 浮点输出里的循环小数                             （28748：题面允许 10^-6 容差，
                                                       我们却精确比对，会误杀）

**它不发现新的失败模式**，只保证旧的不复发。发现新模式这件事，到目前为止仍然靠人
偶尔越出流程去看一眼 —— 这条我没能变成规则，也不打算假装它变成了。

用法：
    python3 tools/full_sweep.py           # 有残留则退出码 1
    python3 tools/full_sweep.py --list    # 连干净的项目也列出来
"""
import argparse
import glob
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
from gmyhf_validators import analyze_27150_case
TESTS = ROOT / "data" / "openjudge" / "tests"
FSIZE_LIMIT = 2 * 1024 * 1024          # judge.py 的 RLIMIT_FSIZE
DEGENERATE = re.compile(r"is present|nonempty|non-?empty", re.I)
FLOAT_TOKEN = re.compile(r"^-?\d+\.\d+$")
# 小数位超过这个数就当成「循环小数四舍五入」——1/6、1/3 之类都会落在这边。
TERMINATING_DECIMALS = 6

# 已经算过账的例外。**不是把检查删掉，是把结论记下来**——
# 一个缺陷被接受和被忽略，从代码上看一模一样，区别只在有没有写下来。
ACCEPTED_REPEATING = {
    1001: "Exponentiation 要求输出 R^n 的 exact value，并明确规定前导零与无意义尾零的"
          "规范化格式；长小数是精确十进制，不是容差浮点，token 精确比对符合题意。",
    4140: "方程求解：答案是方程的根，题面明写「精确到小数点后9位」——"
          "9 位有效小数是题目本身的要求，不是四舍五入凑出来的。"
          "平台对它同样按精确值判，我们与平台一致。",
}


def report_entries():
    for path in sorted(ROOT.glob("collab/t0*-round*-report.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        entries = data["entries"] if isinstance(data, dict) and "entries" in data else data
        if isinstance(entries, dict):
            entries = [dict(v, local_number=k) for k, v in entries.items()]
        for entry in entries or []:
            yield path.name, entry


def made_dirs():
    """自产数据目录。**报告类判据用这个** —— 报告写的就是 `_made` 里的数字。"""
    for path in sorted(TESTS.glob("*/*_made")):
        match = re.search(r"/0*(\d+)_made$", str(path))
        if match:
            yield int(match.group(1)), path


def active_dirs():
    """**真正在判学生代码的**数据目录，按 catalog 实际引用的算，不靠目录名后缀猜。

    2026-07-30 加的。T-030 引入 `_GMyhf`（优先级 `_GMyhf > _made > legacy`）之后，
    `made_dirs()` 只 glob `*_made`，于是**320 条 catalog 记录正在用的数据，
    全库横扫一份都没看过** —— 2MB 上限、循环小数、多解题这三条判据全部落空，闸门照样绿。
    更糟的是 27150：它的多解豁免是拿**已经不判的** `_made` 副本（输出清一色 `NO`）
    去核对的，而真正在判的 `_GMyhf` 是有 YES 分支的真多解数据。
    **判据必须盯着真正生效的那份数据**，否则豁免会替错文件背书。

    所以这里从 `catalog.json` 反推：每道题的 `test_cases` 指向哪个目录，哪个就是活的。
    `made_dirs()` 保留原样给报告类判据用（第 9 条要拿报告里的数字和 `_made` 重算对账，
    换成活目录反而对不上）。
    """
    catalog_path = ROOT / "data" / "openjudge" / "catalog.json"
    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return
    seen = {}
    for problem in catalog.get("problems", []):
        for case in problem.get("test_cases") or []:
            parts = str(case.get("input", "")).split("/")
            if len(parts) < 3:
                continue
            # 用目录名里的题号，和 `made_dirs()` 同一口径 —— 调用方（多解判据）
            # 是拿镜像题面文件名 `<题库>__<题号>.html` 去对的。
            match = re.match(r"0*(\d+)", parts[2])
            if match:
                seen.setdefault((int(match.group(1)), TESTS / parts[1] / parts[2]), None)
    for number, directory in sorted(seen, key=lambda item: (item[0], str(item[1]))):
        yield number, directory


def check_reported_failures():
    """1. 任何轮次的 self_audit.failed 非空。"""
    bad = []
    for source, entry in report_entries():
        failed = (entry.get("self_audit") or {}).get("failed")
        if failed:
            bad.append(f"{entry.get('local_number')}（{source}）: {failed}")
    return "报告里 self_audit.failed 非空", bad


def check_degenerate_constraints():
    """2. Catch empty non-constraints and one-label-for-the-whole-round checks.

    只看措辞会误伤 —— 30932 的 `tree root is present` 反例是 `"null\\n"`，空树是那题
    合法的输入格式，真实数据保持 True、反例翻 False，这条是好的。所以两个条件都要满足。
    """
    bad, by_source = [], {}
    for source, entry in report_entries():
        labels_list = [str(c[0]).strip() for c in (entry.get("constraints") or [])]
        labels = " ".join(labels_list)
        counter = entry.get("constraint_counterexample")
        if isinstance(counter, (list, tuple)):
            counter = counter[0] if counter else ""
        counter_text = str(counter or "").strip()
        if DEGENERATE.search(labels) and not counter_text:
            bad.append(f"{entry.get('local_number')}（{source}）: {labels[:50]!r} 反例={counter_text!r}")
        by_source.setdefault(source, []).append((entry.get("local_number"), set(labels_list)))

    for source, rows in by_source.items():
        if len(rows) < 2:
            continue
        shared = set.intersection(*(labels for _number, labels in rows)) if rows else set()
        for label in sorted(shared):
            bad.append(f"{source}: {len(rows)} 题共用同一约束 {label[:80]!r}")
    return "退化约束（非空占位+空反例，或整轮共用同一判据）", bad


def check_output_size():
    """3. .out 超过判题器 2MB —— 学生的正确解法会被 Output Limit Exceeded 打掉。"""
    bad = []
    for number, made in active_dirs():
        for path in (made / "data").glob("*.out"):
            if path.stat().st_size > FSIZE_LIMIT:
                bad.append(f"{number}: {path.name} {path.stat().st_size / 1048576:.2f}MB")
                break
    return f"输出超过判题器 {FSIZE_LIMIT // 1048576}MB 上限", bad


def check_merged_judge():
    """5. T-028 的报告必须带「合并后真判过」的实测，而且是 passed。

    为什么是机械判据而不是复核时人眼看：**交叉验证只验「答案对不对」，
    验不出「对但太慢」。** 2026-07-29 的 01384 就是这么溜过去的 ——
    参考解法逐 token 复算出了全部存档输出、平台也判 Accepted，
    但在本地合并后的数据上是 Time Limit Exceeded（卡在一份 117KB 的 2008 压测文件上）。
    当轮报告写的是「20/20 Accepted」，因为那一步根本没跑。

    人已定复核改成「攒几轮一起看」，所以这条更不能留给人眼：
    **字段缺了就是红**，等同于「你没跑这一步」。
    只查 T-028 起的批次，早于这条规则的 t002/t003/t004 不追溯。
    """
    bad = []
    for source, entry in report_entries():
        if not source.startswith("t028-"):
            continue
        merged = entry.get("merged_judge") or {}
        if not merged:
            bad.append(f"{entry.get('local_number')}（{source}）: 没有 merged_judge —— 合并后真判这一步没跑")
        elif merged.get("status") != "passed":
            bad.append(f"{entry.get('local_number')}（{source}）: merged_judge="
                       f"{merged.get('status')} verdict={merged.get('verdict')}")
    return "T-028 报告缺「合并后真判」的实测或未通过", bad


# 判据要抓的是「随便哪个都算对」，不是「存在多个解」。这两者差别很大：
#   04012「If there exists multiple solutions, output the one whose first number is
#          the smallest」—— 题面自己消歧了，答案唯一，精确比对没问题。
#   30931「对任意一个右括号，它必须…」—— 「任意一」在这里是语法用词，跟输出无关。
# 第一版判据把这两条都误报了。所以只认「any / 任意」直接修饰「输出」的那几种说法。
MULTI_ANSWER = re.compile(
    r"any one of them|any of them is acceptable|any one is acceptable"
    r"|(?:output|print)\s+any\b"
    r"|输出任意一|任意输出一|任选一|输出其中任意|输出移除某些数字的结果"
    r"|任意一[个种组].{0,6}(?:即可|均可|都(?:算)?可以)", re.I)


def check_multi_answer_problems():
    """6. 题面明说「多解任选其一」的题，不能生成精确比对数据。

    判题器是 token 精确比对。题面写着 any one of them 的题，**学生给出另一个同样正确的
    答案会被判 Wrong Answer** —— 而 WA 长得就像他自己错了，他不会想到是数据的问题。

    2026-07-29 实测：01426 Find The Multiple（「If there are multiple solutions …
    any one of them is acceptable」）生成了精确数据之后，另写一份同样合法、只是输出
    第二小 0/1 倍数的解法，判定是 Wrong Answer。03151 Pots 同理。两题已移出。

    **构建期的「语义校验」解决不了这件事** —— 那只让 oracle 交叉验证过得去，
    判题这一头仍然是精确比对。要收这类题得先有 special judge。
    """
    made_paths = {number: path for number, path in active_dirs()}
    made = set(made_paths)
    exemptions = {}
    for _source, entry in report_entries():
        if entry.get("multi_answer_exemption"):
            exemptions[int(entry["local_number"])] = entry["multi_answer_exemption"]
    try:
        gmyhf_audit = json.loads((ROOT / "collab" / "gmyhf-data-audit.json")
                                  .read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        gmyhf_audit = {}
    for entry in gmyhf_audit.get("entries", []):
        if entry.get("multi_answer_exemption"):
            exemptions[int(entry["global_number"])] = entry["multi_answer_exemption"]
    bad = []
    for page in sorted((ROOT / "data" / "openjudge" / "pages").glob("*.html")):
        match = re.search(r"__(\d+)\.html$", page.name)
        if not match or int(match.group(1)) not in made:
            continue
        text = re.sub(r"<[^>]+>", " ", page.read_text(encoding="utf-8", errors="replace"))
        text = re.sub(r"\s+", " ", text)
        start = text.find("输出")
        window = text[start:start + 900] if start > 0 else text[:900]
        found = MULTI_ANSWER.search(window)
        if found:
            outputs = sorted((made_paths[int(match.group(1))] / "data").glob("*.out"))
            exemption = exemptions.get(int(match.group(1)))
            if (int(match.group(1)) == 27150 and isinstance(exemption, dict) and
                    exemption.get("validator") ==
                    "all divisible-by-8 subsequences of length 1..3 are enumerated"):
                inputs = sorted((made_paths[27150] / "data").glob("*.in"))
                analyses = [analyze_27150_case(
                    input_path.read_text(encoding="utf-8", errors="replace"),
                    input_path.with_suffix(".out").read_text(encoding="utf-8", errors="replace"))
                    for input_path in inputs if input_path.with_suffix(".out").is_file()]
                if (inputs and len(analyses) == len(inputs) and
                        all(analysis["valid_unique"] for analysis in analyses) and
                        sum(analysis["kind"] == "YES" for analysis in analyses) ==
                        exemption.get("unique_yes_cases") and
                        sum(analysis["kind"] == "NO" for analysis in analyses) ==
                        exemption.get("no_answer_cases")):
                    continue
            unique_output = (exemption.get("unique_output_tokens")
                             if isinstance(exemption, dict) else ["-1"])
            if (exemption and isinstance(unique_output, list) and outputs and
                    all(path.read_text(encoding="utf-8", errors="replace").split() == unique_output
                        for path in outputs)):
                continue
            bad.append(f"{int(match.group(1))}: 题面写着「{found.group(0)}」，"
                       f"却生成了精确比对数据（需 special judge，先排除）")
    return "多解题却生成了精确比对数据", sorted(set(bad))


def check_archive_oracle_is_auditable():
    """7. round8 起：报告要记下**用了哪些存档目录**当 oracle，不能只记排除了谁。

    round6/7 引入了「按标题匹配历史存档」——不再只按题号找。技术本身合理（2008 存档
    很多目录是按题名起的），但它能伸手到任意目录：1789 Truck History 那轮就够到了
    `tests/1000-1999/1798`（数字转置），Codex 自己发现是「无关的德语编码存档」并排除。

    **这次是排掉了，但复核方无法核对没排掉的那些** —— 报告只记 `excluded`，
    不记实际用了哪几个目录。oracle 是这套流程里最强的一道验证，它必须可回查。

    只对 round8 及以后生效：早于这条规则的轮次不追溯（也无法追溯 —— 用了哪些目录
    已经无从得知，这本身就是这条判据要防的事）。
    """
    bad = []
    for source, entry in report_entries():
        match = re.match(r"t028-round(\d+)-report\.json$", source)
        if not match or int(match.group(1)) < 8:
            continue
        check = entry.get("archive_cross_check") or entry.get("scraped_cross_check") or {}
        if not check.get("dirs") and not check.get("no_archive_reason"):
            bad.append(f"{entry.get('local_number')}（{source}）: "
                       f"archive_cross_check 没记 dirs（没有存档就写 no_archive_reason）")
    return "T-028 报告未记录 oracle 用了哪些存档目录（round8 起）", bad


def statement_text(book, problem_id):
    """镜像题面的纯文本，用于「原话必须逐字出现」的核对。

    `re.sub(r"<(?![/a-zA-Z!])", ...)` 那一步是必须的：题面里的 `1<=n<=20` 在 HTML 里
    就是裸的 `<`，按标签剥会把整段范围声明连同后文一起吃掉 —— 而范围声明**正是**
    这条检查要读的东西。2026-07-30 复核 18106 时就是先被这一口吃掉、差点判成「题面没写上界」。
    """
    page = ROOT / "data" / "openjudge" / "pages" / f"{book}__{problem_id}.html"
    if not page.is_file():
        return ""
    raw = page.read_text(encoding="utf-8", errors="replace")
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    raw = re.sub(r"<(?![/a-zA-Z!])", "&lt;", raw)
    text = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    return " ".join(text.split())


def generated_extremes(made_dir):
    """从 `data/*.in` 重算整数极值。口径写死在这里，报告必须按同一口径填。

    token 定义：按空白切开后能整体匹配 `-?\\d+` 且长度不超过 18 位的片段。
    18 位是为了把「不是数量、只是长串数字」（题号、超长整数题的输入）挡在外面。
    """
    values = []
    for path in sorted((made_dir / "data").glob("*.in")):
        for token in path.read_text(encoding="utf-8", errors="replace").split():
            if re.fullmatch(r"-?\d{1,18}", token):
                values.append(int(token))
    if not values:
        return {"integer_tokens": 0}
    return {"max_int": max(values), "min_int": min(values)}


def check_input_domain_is_anchored():
    """10. round20 起：每题要记下**题面对输入范围的原话**，以及生成数据的实际极值。

    2026-07-30 复核 round15-19 时抓到七题，生成的数据跑到了题面保证的范围之外：
    18106 题面写 `1<=n<=20`、数据到 100；27625 题面写 `0<n<50`、数据到 1000；
    18159 每个 n 题面写 `2<=n<=10001`、数据到 199700；4100 题面写起止时间「不超过 100」、
    数据到 10^9；4044 题面写 `1<N<100`、数据到 990；27122 题面写 `1<=position[i]<=10^9`、
    数据里全是负数；21458 题面写 `0<w_i`、数据里有 0。

    **这正是这个仓库最不能出的错**：学生按题面写的正确解法，在平台 Accepted，
    在我们这里 RE 或 WA。实测过两条 —— 按 `1<=n<=20` 静态开数组的 18106 解法越界崩了
    7/21 组；用 `long long`（在 `0<n<50` 内绰绰有余）的 27625 解法在 6/21 组上溢出。

    为什么之前没红：`valid()` 校的是「生成器合不合自己写的 LABEL」，而 LABEL 是照着
    生成器写的 —— 这是个闭环，题面从没进过这个环。`archive_cross_check` 只覆盖存档里
    那些本来就合规的输入，也够不着。

    这条判据**不判「原话是否蕴含这些极值合法」** —— 那要人读题，我没有把它变成规则。
    它做的是把两件事钉进同一条记录并各自可验：
      - `input_domain.statement_quote` 必须在镜像题面里**逐字**出现（防转述、防凭印象）；
      - `input_domain.generated_extremes` 必须能从 `data/` 按 `generated_extremes()`
        的口径重算出来（防写一个好看的数字）。
    两半并排摆着，矛盾就藏不住了 —— 上面七条里有六条一眼可见。

    只对 round20 及以后生效（外加任何已经填了这个字段的条目）：round15-19 那七题
    要在返工时补上，其余轮次不追溯。
    """
    manifests = {}
    for path in sorted(ROOT.glob("collab/t028-round*-manifest.json")):
        match = re.search(r"round(\d+)-manifest", path.name)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if match:
            manifests[int(match.group(1))] = {
                int(row["local_number"]): row for row in data.get("entries", [])
                if "local_number" in row}
    bad = []
    for source, entry in report_entries():
        match = re.match(r"t028-round(\d+)-report\.json$", source)
        if not match:
            continue
        round_number = int(match.group(1))
        domain = entry.get("input_domain")
        if round_number < 20 and not domain:
            continue
        number = entry.get("local_number")
        if not isinstance(domain, dict):
            bad.append(f"{number}（{source}）: 没有 input_domain")
            continue
        row = manifests.get(round_number, {}).get(int(number), {})
        quote = str(domain.get("statement_quote") or "")
        text = statement_text(row.get("submit_group", ""), row.get("submit_id", ""))
        if not quote:
            bad.append(f"{number}（{source}）: input_domain.statement_quote 为空")
        elif not text:
            bad.append(f"{number}（{source}）: 找不到镜像题面，无法核对 statement_quote")
        elif " ".join(quote.split()) not in text:
            bad.append(f"{number}（{source}）: statement_quote 在题面里找不到原话")
        made = ROOT / "data" / "openjudge" / str(row.get("made_dir", ""))
        actual = generated_extremes(made) if row.get("made_dir") else None
        recorded = domain.get("generated_extremes")
        if actual is None:
            bad.append(f"{number}（{source}）: 无法从 data/ 重算极值")
        elif not isinstance(recorded, dict) or any(
                recorded.get(key) != value for key, value in actual.items()):
            bad.append(f"{number}（{source}）: generated_extremes 记的是 {recorded}，"
                       f"从 data/ 重算是 {actual}")
    return "T-028 报告未把题面范围与生成极值钉在一起（round20 起）", bad


def check_priority_gaps_are_recorded():
    """8. T-028 按 priority 顺序做，**跳过可以，不留痕不行**。

    round8-10 覆盖 priority 121-180，实际只建了 57 题 —— 131/141/173 被跳过，
    而清单里一条记录都没有。三个决定后来查下来都是对的（00000 输出超 2MB、
    02982 Sudoku 是「print any」多解题、01729 疑为多解/浮点），
    **但没有记录就等于没有人在跟着它们** —— 下一轮要么重新踩一遍，要么永远忘掉。

    判据：把各轮 manifest 里的 priority 取并集，凡是落在 [最小, 最大] 区间内、
    既没建也没记进 `selection_exclusions` 的，就报出来。
    """
    built, excluded = set(), set()
    for path in sorted(ROOT.glob("collab/t028-round*-manifest.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        built |= {row["priority"] for row in data.get("entries", []) if "priority" in row}
        excluded |= {row["priority"] for row in data.get("selection_exclusions", [])
                     if isinstance(row, dict) and "priority" in row}
    if not built:
        return "T-028 priority 有缺口却没有记录", []
    gaps = sorted(p for p in range(min(built), max(built) + 1)
                  if p not in built and p not in excluded)
    return "T-028 priority 有缺口却没有记录", [
        f"priority {p}: 既没构建也没记进 selection_exclusions" for p in gaps]


def check_self_audit_numbers_are_measured():
    """9. 报告里的自检数字必须能从 `data/` 重算出来。

    T-002 立过一条：**自检字段必须是实测值，不得写字面量常量**
    （Decision Log 2026-07-25 第五代自检项②）。它一直靠复核时人眼重算 ——
    而复核已改成攒几轮一起看，人眼最不该承担这件事。

    2026-07-30 实测抓到 02800：报告写 `constant_output_probe.frequency = 2`，
    而 20 组输出两两不同，真实频次是 1。方向上偏保守、没掩盖缺陷，
    但它说明那个数不是量出来的。

    **判据对「含不含第 0 组」两种口径都放行** —— 报告里这两种都出现过
    （02800 的 total 是 20/21 组，03259 的 total 是 20/20 组）。
    这条判据管的是「数字是不是量出来的」，不是「口径统不统一」；
    口径不一致另记，不在这里罚。
    """
    import collections
    made = dict(made_dirs())
    bad = []
    for source, entry in report_entries():
        if not source.startswith("t028-"):
            continue
        audit = entry.get("self_audit") or {}
        probe, distinct = audit.get("constant_output_probe") or {}, audit.get("distinct_cases") or {}
        path = made.get(entry.get("local_number"))
        if path is None or not probe:
            continue
        cases = sorted((path / "data").glob("*.in"), key=lambda p: int(p.stem))
        if not cases:
            continue
        for label, reported, values in (
            ("constant_output_probe.total", probe.get("total"),
             [p.with_suffix(".out").read_bytes() for p in cases]),
            ("distinct_cases.total", distinct.get("total"), [p.read_bytes() for p in cases]),
        ):
            if reported is not None and reported not in (len(values), len(values) - 1):
                bad.append(f"{entry.get('local_number')}（{source}）: {label} 写的是 {reported}，"
                           f"data/ 里是 {len(values)} 组（含样例）/{len(values) - 1}（不含）")
        outs = [p.with_suffix(".out").read_bytes() for p in cases]
        ins = [p.read_bytes() for p in cases]
        for label, reported, allowed in (
            ("constant_output_probe.frequency", probe.get("frequency"),
             {collections.Counter(outs).most_common(1)[0][1],
              collections.Counter(outs[1:]).most_common(1)[0][1] if outs[1:] else 0}),
            ("distinct_cases.distinct", distinct.get("distinct"),
             {len(set(ins)), len(set(ins[1:]))}),
        ):
            if reported is not None and reported not in allowed:
                bad.append(f"{entry.get('local_number')}（{source}）: {label} 写的是 {reported}，"
                           f"从 data/ 重算只可能是 {sorted(allowed)}")
    return "报告自检数字与 data/ 重算不符（必须是实测值）", bad


def check_repeating_decimals():
    """4. 浮点输出里的循环小数。

    题面给容差（如 28748 的「绝对误差不超过 10^-6」）而判题器只有 token 精确比对时，
    像 1/6 = 0.166666667 这种值会误杀 —— 另一个同样正确、只是累加顺序不同的实现
    可能给出 0.166666666。数据这头躲开就没这问题。
    """
    bad = []
    for number, made in made_dirs():
        outs = sorted((made / "data").glob("*.out"))
        repeating = 0
        total = 0
        for path in outs[:6]:
            for token in path.read_text(errors="replace").split()[:400]:
                if not FLOAT_TOKEN.match(token):
                    continue
                total += 1
                if len(token.split(".")[1].rstrip("0")) > TERMINATING_DECIMALS:
                    repeating += 1
        if total and repeating / total > 0.2 and number not in ACCEPTED_REPEATING:
            bad.append(f"{number}: {repeating}/{total} 个浮点输出是循环小数")
    return "浮点输出里的循环小数（token 精确比对会误杀）", bad


def check_annotated_sample_outputs():
    """Guard the parser's # truncation precondition for every mirrored statement."""
    from html import unescape
    from server import SAMPLE_ANY, parse_sample_sections

    catalog_path = ROOT / "data" / "openjudge" / "catalog.json"
    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return "标记式样例输出的首行安全前提", ["catalog.json 不可读"]
    bad = []
    marked = 0
    for item in catalog.get("problems", []):
        page = ROOT / "data" / "openjudge" / "pages" / f"{item['book']}__{item['id']}.html"
        try:
            text = page.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        match = re.search(r'<dt>样例输入</dt>\s*<dd>(.*?)</dd>\s*<dt>样例输出</dt>\s*<dd>(.*?)</dd>', text, re.S)
        if not match:
            continue
        plain = lambda chunk: unescape(re.sub(r"</?pre[^>]*>|<[^>]+>", "", chunk.strip())).strip("\n")
        raw_input, raw_output = plain(match.group(1)), plain(match.group(2))
        if not (SAMPLE_ANY.search(raw_input) or SAMPLE_ANY.search(raw_output)):
            continue
        marked += 1
        # 必须关掉截断再看：截断会把「首行就是 #」的输出削成空串，
        # 拿截断后的结果去验，这个检查永远看不见自己要防的那件事。
        sections = parse_sample_sections(raw_input + "\n" + raw_output,
                                         truncate_explanations=False)
        for index, case in enumerate(sections, 1):
            first = next((line.strip() for line in case["output"].splitlines() if line.strip()), "")
            if first.startswith("#"):
                bad.append(f"{item['book']}__{item['id']} 样例 {index}: 输出首行 {first!r}")
    return f"标记式样例输出的首行安全前提（已扫描 {marked} 题）", bad


CHECKS = (check_reported_failures, check_degenerate_constraints,
          check_output_size, check_repeating_decimals, check_annotated_sample_outputs,
          check_merged_judge, check_multi_answer_problems,
          check_archive_oracle_is_auditable, check_priority_gaps_are_recorded,
          check_self_audit_numbers_are_measured, check_input_domain_is_anchored)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true", help="连干净的项目也列出来")
    opts = parser.parse_args()

    total = 0
    for check in CHECKS:
        label, bad = check()
        total += len(bad)
        if bad or opts.list:
            mark = f"**{len(bad)} 处**" if bad else "干净"
            print(f"  [{mark}] {label}")
            for line in bad[:12]:
                print(f"      {line}")
            if len(bad) > 12:
                print(f"      …另有 {len(bad) - 12} 处")
    if total:
        print(f"全库横扫：**{total} 处残留**")
        return 1
    print(f"全库横扫：{len(set(p for _n, p in active_dirs()))} 份在判数据，{sum(1 for _ in report_entries())} 条报告记录，干净")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
