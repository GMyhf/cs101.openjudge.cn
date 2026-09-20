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
  5. 第 0 组是题面样例、期望输出却和题面对不上         （01830：参考实现漏了对角线，
                                                       21 组自洽地全错，别的闸门全绿）

**它不发现新的失败模式**，只保证旧的不复发。发现新模式这件事，到目前为止仍然靠人
偶尔越出流程去看一眼 —— 这条我没能变成规则，也不打算假装它变成了。

用法：
    python3 tools/full_sweep.py           # 有残留则退出码 1
    python3 tools/full_sweep.py --list    # 连干净的项目也列出来
"""
import argparse
import concurrent.futures
import glob
import hashlib
import html
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
TESTS = ROOT / "data" / "openjudge" / "tests"
FSIZE_LIMIT = 2 * 1024 * 1024          # judge.py 的 RLIMIT_FSIZE
DEGENERATE = re.compile(r"is present|nonempty|non-?empty", re.I)
FLOAT_TOKEN = re.compile(r"^-?\d+\.\d+$")
# 小数位超过这个数就当成「循环小数四舍五入」——1/6、1/3 之类都会落在这边。
TERMINATING_DECIMALS = 6

# 引文里必须真的含一条数值范围，否则「逐字引用」只是引了段输入格式，锚不住任何东西。
QUOTE_BOUND = re.compile(
    r"(?:<=|>=|≤|≥|<|>|不超过|不少于|不大于|不小于|至多|最多|至少|小于|大于|以内|以下|范围|之间)")

# 引文确实无界的题 —— 2026-07-30 Claude 复核时**逐题拿题面真正的约束核过生成极值，
# 全部在范围内**，所以不是缺陷，是「这段题面本来就没写上界」。记在这里而不是放宽判据：
# 新出现的无界引文仍然会红，这 21 条则是已经算过账的。
# 其中 27018（题面上界写在「提示」里的 1≤N≤10^6，引文只引了输入格式，数据 max 200000）
# 和 20134（约束写在「数据范围与约定」段，引文引的是输入格式，n=19 远小于 5000）
# 最能说明问题：**引文选错段落，闸门是看不出来的。**
QUOTES_WITHOUT_BOUND = {
    8210: "L/N/M 的范围写在描述段，引文引的是输入格式；数据 max 10^9 = 题面 L 上界",
    18164: "N/Li 范围写在描述段末尾；数据 max 50000 = 题面 Li 上界",
    20140: "重复次数 1<=x<=100 写在描述段；输入是纯字符串，无独立整数 token",
    4018: "题面对 s/t 没有任何长度或取值约束",
    4030: "单词与文章长度写在【数据范围】段；输入是纯字符串，无独立整数 token",
    12560: "1<=n,m<=100 写在描述段；数据 max 100",
    20134: "全部约束写在「数据范围与约定」段；n=19，题面允许 0<=n<=5000",
    27103: "M<=10000、N<=100000 写在描述段；数据 max 100000",
    19963: "题面对 n 与坐标价格都没有写上界",
    27018: "1≤N≤10^6 写在「提示」段；数据 max 200000",
    18108: "题面对 T/N/M 没有写上界；数据 max 100",
    18160: "题面对 T/N/M 没有写上界；数据 max 100",
    18188: "题面对 M/N 与像素值都没有写上界",
    28700: "整数范围 1~3999 写在描述段与提示段；数据 92..2948",
    4069: "四个属性「取值都在 10000 以内」就写在引文里但不含比较符；数据 max 9999",
    12557: "题面对版本号段数与数值没有写上界",
    18104: "s/g/个数的 <=100 写在描述段；数据 max 100",
    18105: "题面对引用次数没有写上界",
    27862: "题面对节点数与收益没有写上界",
    29468: "题面对散列表大小与元素没有写上界",
    29982: "题面对 m/n/k 没有写上界；输入是逗号分隔，无空白分隔的整数 token",
    23421: "题面对 N/B 与价格重量都没有写上界",
    18161: "题面对矩阵行列数与元素都没有写上界",
    27653: "题面只说分母是任意大于 0 的整数，对分子分母大小没有写上界",
    19960: "转子/反射器行数由题面固定为 18/3 行，数值 1..6 是线路编号，没有可越的上界",
    26572: "题面对表达式长度与数值都没有写上界",
    29917: "题面只约束迭代终止精度 1E-6，对输入的数值大小没有写上界",
    18177: "题面对品种数 N、天数 D 与价格都没有写上界",
    4020: "题面对测试组数 N 没有写上界；每组固定 53 张牌",
    16527: "题面只保证 A/B 可连接，对字符串长度没有写上界",
    20025: "题面对 n 没有写上界（引文引的是「不混有数字的单词」这条格式保证）",
    30894: "题面对字符集大小 n 与编码长度都没有写上界",
}

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
        match = re.search(r"/((?:0*\d+)(?:[A-Za-z]\d*)?)_made$", str(path))
        if match:
            identifier = match.group(1)
            # Reports identify OpenJudge problems with integers. Keep external
            # alphanumeric IDs intact so their directories are not skipped or
            # conflated (for example, 1A and 1B).
            yield (int(identifier) if identifier.isdigit() else identifier), path


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
    bad = []
    for page in sorted((ROOT / "data" / "openjudge" / "pages").glob("*.html")):
        match = re.search(r"__(\d+)\.html$", page.name)
        if not match or int(match.group(1)) not in made:
            continue
        if (made_paths[int(match.group(1))] / "checker.py").is_file():
            continue                       # 有逐题 checker，正是这条判据要的 special judge
        text = re.sub(r"<[^>]+>", " ", page.read_text(encoding="utf-8", errors="replace"))
        text = re.sub(r"\s+", " ", text)
        start = text.find("输出")
        window = text[start:start + 900] if start > 0 else text[:900]
        found = MULTI_ANSWER.search(window)
        if found:
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


_STATEMENT_CACHE = {}


def statement_text(book, problem_id):
    """镜像题面的纯文本，用于「原话必须逐字出现」的核对。

    `re.sub(r"<(?![/a-zA-Z!])", ...)` 那一步是必须的：题面里的 `1<=n<=20` 在 HTML 里
    就是裸的 `<`，按标签剥会把整段范围声明连同后文一起吃掉 —— 而范围声明**正是**
    这条检查要读的东西。2026-07-30 复核 18106 时就是先被这一口吃掉、差点判成「题面没写上界」。
    """
    # 缓存键带上 ROOT：用例会把 ROOT 指到临时目录，只按题号缓存会串味
    # （2026-09-20 加缓存时 `test_a_quote_with_a_bound_passes` 当场变红）。
    key = (str(ROOT), book, problem_id)
    if key in _STATEMENT_CACHE:
        return _STATEMENT_CACHE[key]
    page = ROOT / "data" / "openjudge" / "pages" / f"{book}__{problem_id}.html"
    if not page.is_file():
        _STATEMENT_CACHE[key] = ""
        return ""
    raw = page.read_text(encoding="utf-8", errors="replace")
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    raw = re.sub(r"<(?![/a-zA-Z!])", "&lt;", raw)
    text = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", raw)).split())
    _STATEMENT_CACHE[key] = text
    return text


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

    最初只对 round20 及以后生效；2026-07-30 发版收口时已回填 round15-19，现从
    round15 起强制检查。更早轮次不追溯。
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
        if round_number < 15 and not domain:
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
        elif not QUOTE_BOUND.search(quote) and int(number) not in QUOTES_WITHOUT_BOUND:
            bad.append(f"{number}（{source}）: statement_quote 里没有任何数值范围 —— "
                       f"逐字引一段不含约束的输入格式，这条锚等于没锚。"
                       f"确实无界就把题号记进 QUOTES_WITHOUT_BOUND 并写明理由")
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
    # A catalog opt-in to float_tokens is the established exception to exact
    # token comparison. Derive it from the active contract rather than keeping
    # a second hand-maintained problem-number exemption list.
    float_directories = set()
    catalog_path = ROOT / "data" / "openjudge" / "catalog.json"
    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        catalog = {"problems": []}
    for problem in catalog.get("problems", []):
        if problem.get("comparison") != "float_tokens":
            continue
        for case in problem.get("test_cases") or []:
            parts = str(case.get("input", "")).split("/")
            if len(parts) >= 3:
                float_directories.add((parts[1], parts[2]))

    bad = []
    for number, made in made_dirs():
        try:
            directory_key = tuple(made.relative_to(TESTS).parts[:2])
        except ValueError:
            directory_key = ()
        if directory_key in float_directories:
            continue
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


def check_sample_anchor():
    """第 0 组若是题面样例，它的期望输出必须和题面的样例输出对得上。

    2026-09-12 加的，对应 01830：参考实现漏掉「操作一个开关会翻转它自己」的对角线，
    生成器拿它产 21 组答案，数据**自洽地全错** —— 参考解 21/21 Accepted、重跑逐字节
    不变、组数够、判别力看着也有，所有既有闸门全绿。唯一能证伪它的是题面样例，
    而「生成完先跟题面样例逐字对一遍」当时只写在手册里，没有任何东西在查。

    判据只认**前缀冲突**：镜像页的样例输出块经常在答案后面接一段「解释：…」或
    `# …` 的说明（37 题），02698 的样例输出则被原站截成「…以下省略」。这两种情况下
    短的那一边是长的那一边的前缀，放过；答案本身就对不上才算残留。
    """
    catalog_path = ROOT / "data" / "openjudge" / "catalog.json"
    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return "第 0 组与题面样例输出的锚定", ["catalog.json 不可读"]
    mirror = ROOT / "data" / "openjudge"
    plain = lambda chunk: html.unescape(
        re.sub(r"</?pre[^>]*>|<[^>]+>", "", chunk.strip())).strip("\n")
    bad, anchored = [], 0
    for problem in catalog.get("problems", []):
        cases = problem.get("test_cases") or []
        if not cases:
            continue
        first_in, first_out = mirror / str(cases[0]["input"]), mirror / str(cases[0]["output"])
        page = mirror / "pages" / f"{problem.get('book')}__{problem['id']}.html"
        if not (first_in.exists() and first_out.exists() and page.exists()):
            continue
        match = re.search(r"<dt>样例输入</dt>\s*<dd>(.*?)</dd>\s*<dt>样例输出</dt>\s*<dd>(.*?)</dd>",
                          page.read_text(encoding="utf-8", errors="replace"), re.S)
        if not match:
            continue
        sample_in, sample_out = plain(match.group(1)).split(), plain(match.group(2)).split()
        if first_in.read_text(encoding="utf-8", errors="replace").split() != sample_in:
            continue                       # 第 0 组不是题面样例，这条判据不适用
        anchored += 1
        if sample_out and sample_out[-1].endswith("以下省略"):
            sample_out = sample_out[:-1]   # 原站自己截断的样例输出，只比对它给出的那截
        if problem.get("interactor"):
            anchored -= 1                  # 交互题的「样例输出」是交互记录，不是 .out
            continue
        if problem.get("checker"):
            # 答案不唯一：题面给的是其中一个正确答案，交给该题 checker 判，而不是逐字比
            sys.path.insert(0, str(ROOT))
            import judge
            verdict, message = judge.run_checker(problem["checker"], first_in.read_bytes(),
                                                 plain(match.group(2)).encode(), first_out.read_bytes())
            if verdict is not True:
                bad.append(f"{problem.get('book')}__{problem['id']}: checker 不接受题面样例输出（{message}）")
            continue
        if problem.get("special_checker"):
            # 同上，只是特判写在 judge.py 里（`concat_divisible` 这类命名口径）。
            # 2026-09-20 加：此前这条分支不存在，2140B 把第 0 组换成官方样例之后，
            # 判据拿「另一个同样合法的答案」去逐字比，红得毫无道理。
            # 反过来这也给特判器本身加了一条锚：它必须接受题面给的那个答案。
            sys.path.insert(0, str(ROOT))
            import judge
            if not judge.special_output_matches(problem["special_checker"],
                                                first_in.read_bytes(), plain(match.group(2))):
                bad.append(f"{problem.get('book')}__{problem['id']}: "
                           f"特判 {problem['special_checker']} 不接受题面样例输出")
            continue
        expected = first_out.read_text(encoding="utf-8", errors="replace").split()
        shared = min(len(expected), len(sample_out))
        if expected[:shared] != sample_out[:shared]:
            bad.append(f"{problem.get('book')}__{problem['id']}: "
                       f"题面 {sample_out[:5]}… vs 数据 {expected[:5]}…")
    return f"第 0 组与题面样例输出的锚定（已锚定 {anchored} 题）", bad


def check_short_data_is_recorded():
    """12. 每题至少 20 组；做不到的必须记进 `collab/tests-below-20.json` 并写明原因。

    2026-09-17 人要求「少于 20 组测试用例的题目增加到至少 20 组，实在没法增加的标记下来」。
    当时 176 条 catalog 记录不足 20 组，其中 53 道是 `_GMyhf` 整份顶替 `_made` 顶掉的，
    **没有任何闸门在看组数**。判据两头都查：没登记的短数据要报，登记了但已补够
    （或组数与登记不符）的也要报 —— 否则登记表会悄悄变成过期的豁免清单。
    OpenJudge 按全局题号登记（覆盖全部题库别名），外部题库按 `来源:题号`。
    """
    label = "少于 20 组测试数据却没有登记原因"
    registry_path = ROOT / "collab" / "tests-below-20.json"
    catalog_path = ROOT / "data" / "openjudge" / "catalog.json"
    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return label, [f"读不到登记表或 catalog：{error}"]
    minimum = registry.get("min_cases", 20)
    recorded = {row["key"]: row for row in registry.get("entries", [])}
    actual = {}
    for item in catalog.get("problems", []):
        source = item.get("source", "openjudge")
        key = (f"openjudge:{item['global_number']}" if source == "openjudge"
               else f"{source}:{item['id']}")
        actual.setdefault(key, (item.get("test_count", 0), f"{item['book']}/{item['id']}"))
    bad = []
    for key, (count, example) in sorted(actual.items()):
        row = recorded.get(key)
        if count < minimum and row is None:
            bad.append(f"{key}（{example}）只有 {count} 组，没登记原因")
        elif row is not None and count >= minimum:
            bad.append(f"{key}（{example}）已有 {count} 组，登记表里的条目该删了")
        elif row is not None and row.get("test_count") != count:
            bad.append(f"{key}（{example}）登记 {row.get('test_count')} 组，实际 {count} 组")
        if row is not None and not str(row.get("reason", "")).strip():
            bad.append(f"{key}：登记了但没写原因")
    bad += [f"{key}：登记表里有，catalog 里没有" for key in sorted(recorded.keys() - actual.keys())]
    return label, bad



# ---------------------------------------------------------------- 输入契约

VALID_DRIVER = r"""
import importlib.util, inspect, json, sys
from pathlib import Path
module_path, data_dir, identifier = sys.argv[1], sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location("producecase_under_test", module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
valid = module.valid
parameters = list(inspect.signature(valid).parameters)
key = None
for attribute in ("NUMBER", "PROBLEM", "PROBLEM_ID", "ID"):
    if hasattr(module, attribute):
        key = getattr(module, attribute)
        break
if key is None:
    key = int(identifier) if identifier.isdigit() else identifier
bad = []
for path in sorted(Path(data_dir).glob("*.in"), key=lambda item: int(item.stem)):
    text = path.read_text(encoding="utf-8", errors="replace")
    try:
        verdict = valid(text) if len(parameters) == 1 else valid(key, text)
    except Exception as error:
        verdict = "raised %r" % (error,)
    if verdict is not True:
        bad.append("%s: valid() -> %r" % (path.name, verdict))
print(json.dumps(bad))
"""


def contract_dirs():
    """活目录里带 `valid()` 的那些，连同目录名里的题号。"""
    for number, directory in active_dirs():
        module = directory / "producecase.py"
        if not module.is_file():
            continue
        try:
            source = module.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if re.search(r"^def valid\(", source, re.M):
            match = re.search(r"/0*(\d+[A-Za-z]?\d*)_made$", str(directory))
            yield (match.group(1) if match else str(number)), directory


def _run_contract(item):
    identifier, directory = item
    module = directory / "producecase.py"
    with tempfile.TemporaryDirectory(prefix="valid-contract-") as work:
        # 临时 CWD：个别生成器把 `Path("data")` 当相对路径用，跑契约时不能让它写到仓库里。
        result = subprocess.run([sys.executable, "-c", VALID_DRIVER, str(module),
                                 str(directory / "data"), identifier],
                                capture_output=True, text=True, cwd=work, timeout=600)
    rel = directory.relative_to(ROOT / "data" / "openjudge")
    if result.returncode:
        tail = (result.stderr.strip().splitlines() or ["(无输出)"])[-1]
        return f"{rel}: valid() 跑不起来 —— {tail[:140]}"
    bad = json.loads(result.stdout)
    if bad:
        return f"{rel}: {len(bad)} 组不满足自己的 valid() —— {bad[0]}"
    return None


def check_input_contracts_hold():
    """13. 生成器写了 `valid()`，就必须对**自己产出的每一组输入**成立。

    2026-09-20 加的。在此之前 `valid()` 是一份没人跑的文档：117 个活目录里写了它，
    而闸门一次都没调用过 —— 生成器改了、数据被手改了、契约自己写错了，都不会红。
    （同一天修的 `7f6a07bd` 正是「手改 `.in/.out`、生成器没动」，1850H 的输入被写成
    `1 NaN`；那种数据在这条判据下当场就是红的。）

    **它证明不了什么**：契约是照着生成器写的，两边一起错仍然自洽（见
    `data-self-consistency`）。要拿题面说话的是 `tests/test_input_constraints.py`
    里逐题手写的那份契约。这条只保证「生成器和它自己的契约没有漂移」，很便宜，所以常跑。
    """
    items = sorted(set(contract_dirs()), key=lambda item: str(item[1]))
    bad = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for message in pool.map(_run_contract, items):
            if message:
                bad.append(message)
    return f"生成器的 valid() 在自己的数据上不成立（{len(items)} 个目录）", bad


def check_contract_coverage_ratchet():
    """14. 输入契约的覆盖率只能涨，不能跌。

    2026-09-20 立的规矩（人拍板）：**新增或重建数据的题必须带 `valid()`**，
    见 `docs/管理员手册.md` 的「新增一道题」。规矩要有闸门盯着才算数，
    所以这里记一个基线：`collab/valid-contracts.json` 写着当时带契约的目录清单
    和「有 `producecase.py` 却没有 `valid()`」的数量。

    判据只看两件事：清单里的目录不许把 `valid()` 删掉；没契约的目录数不许比基线多。
    数字降了就更新基线（脚本会提示），这样棘轮只往一个方向走。
    """
    ledger_path = ROOT / "collab" / "valid-contracts.json"
    try:
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return "输入契约覆盖率棘轮", [f"读不到 {ledger_path.relative_to(ROOT)}"]
    have = {str(directory.relative_to(ROOT / "data" / "openjudge"))
            for _identifier, directory in contract_dirs()}
    missing = []
    for entry in ledger.get("dirs", []):
        if entry not in have:
            missing.append(f"{entry}: 基线里有 `valid()`，现在没了")
    without = 0
    for _number, directory in active_dirs():
        module = directory / "producecase.py"
        if module.is_file() and not re.search(
                r"^def valid\(", module.read_text(encoding="utf-8", errors="replace"), re.M):
            without += 1
    baseline = ledger.get("without_contract")
    if isinstance(baseline, int) and without > baseline:
        missing.append(f"没有 `valid()` 的活目录 {without} 个，基线是 {baseline} —— "
                       f"新增/重建的数据必须带输入契约")
    if isinstance(baseline, int) and without < baseline:
        missing.append(f"没有 `valid()` 的活目录降到 {without} 个（基线 {baseline}）—— "
                       f"把 collab/valid-contracts.json 的 without_contract 改成 {without}，棘轮才收紧")
    return "输入契约覆盖率棘轮（collab/valid-contracts.json）", missing



def data_digest(directory):
    """与 `scripts/build_input_domains.py` 同一口径的数据指纹。

    第 15 条核指纹而不是重算极值：重算要把全库 260MB 输入逐 token 解析一遍，
    实测让 `full_sweep` 从 20 秒涨到 2 分钟。指纹对上就说明账本里的极值
    是从**这些字节**量出来的，数据一变指纹就变，账本必须跟着重建。
    """
    digest = hashlib.sha256()
    cases = sorted((directory / "data").glob("*.in"),
                   key=lambda item: (len(item.stem), item.stem))
    for path in cases:
        digest.update(path.name.encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
    return len(cases), digest.hexdigest()


def codeforces_statement_input(problem_id):
    """Codeforces 题面的输入格式段。镜像页只有样例，约束在结构化题面里。"""
    path = ROOT / "data" / "openjudge" / "statements" / f"{problem_id}.json"
    if not path.is_file():
        return ""
    try:
        statement = json.loads(path.read_text(encoding="utf-8"))["statement"]
    except (OSError, json.JSONDecodeError, KeyError):
        return ""
    return " ".join(statement.get("formatI", "").split())


def check_input_domains_are_ledgered():
    """15. **全库**每份在判数据都要有「题面原话 + 实测极值」的记账。

    第 10 条只覆盖 T-028 各轮报告里的题；这一条把同样的两半推广到 catalog 引用的
    每一个目录，账本是 `collab/input-domains.json`（由 `scripts/build_input_domains.py`
    生成）。判据仍然只判两件可验的事：引文在题面里**逐字**出现、极值能从 `data/` 重算。

    **它不判「极值是否合法」** —— 那需要把约束绑到输入里的位置，能绑的已经写成
    `tests/test_input_constraints.py` 的逐题契约；绑不了的（题面没写上界、约束在提示段）
    机械判只会制造噪音。这条判据保证的是：这两个数字**摆在一起、各自为真**，
    而且数据一重建，极值的变化会连同题面原话一起出现在 diff 里。
    """
    ledger_path = ROOT / "collab" / "input-domains.json"
    try:
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return "全库输入范围记账（collab/input-domains.json）", [
            f"读不到 {ledger_path.relative_to(ROOT)}，跑 scripts/build_input_domains.py"]
    entries = ledger.get("entries", {})
    bad = []
    seen = set()
    for _number, directory in active_dirs():
        rel = str(directory.relative_to(ROOT / "data" / "openjudge"))
        if rel in seen:
            continue
        seen.add(rel)
        row = entries.get(rel)
        if row is None:
            bad.append(f"{rel}: 账本里没有这份在判数据")
            continue
        quote = " ".join(str(row.get("statement_quote") or "").split())
        if not quote:
            bad.append(f"{rel}: statement_quote 为空")
        else:
            text = (codeforces_statement_input(row.get("id", ""))
                    if row.get("source") == "codeforces_statement"
                    else statement_text(row.get("book", ""), row.get("id", "")))
            if not text:
                bad.append(f"{rel}: 找不到题面，无法核对引文")
            elif quote not in text:
                bad.append(f"{rel}: statement_quote 在题面里找不到原话")
        count, digest = data_digest(directory)
        if row.get("data_digest") != digest:
            bad.append(f"{rel}: 数据变了（{count} 组，指纹 {digest[:12]}…），"
                       f"账本记的是 {str(row.get('data_digest'))[:12]}… —— "
                       f"重跑 scripts/build_input_domains.py 把极值重新量一遍")
    stale = sorted(set(entries) - seen)
    for rel in stale[:5]:
        bad.append(f"{rel}: 账本里有，但已经不在判了 —— 重跑 scripts/build_input_domains.py")
    return (f"全库输入范围记账（{len(seen)} 份在判数据，"
            f"引文无数值范围 {ledger.get('without_bound')} 条）"), bad


CHECKS = (check_reported_failures, check_degenerate_constraints,
          check_output_size, check_repeating_decimals, check_annotated_sample_outputs,
          check_sample_anchor,
          check_merged_judge, check_multi_answer_problems,
          check_archive_oracle_is_auditable, check_priority_gaps_are_recorded,
          check_self_audit_numbers_are_measured, check_input_domain_is_anchored,
          check_short_data_is_recorded,
          check_input_contracts_hold, check_contract_coverage_ratchet,
          check_input_domains_are_ledgered)


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
