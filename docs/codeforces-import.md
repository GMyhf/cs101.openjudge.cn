# Codeforces 题解导入记录

- 导入源：`/home/rocky/git/2020fall-cs101/2020fall_Codeforces_problems.md`
- 导入源 SHA-256：`940fb9d066ca956ef4ee3775eba8841c288a5787de56c0e9702863aea4625e4f`
- 标准题：158 道；其中已有条目保留、缺失条目补入 Codeforces 题库。
- 判题数据：仅已有数据的题目可提交判题；其余条目展示题解摘要和官方原题链接。

## 测试数据状态

只导入原文中明确标记的 input/output 样例。交互和多解输出题不会被错误地接入
token 精确判题；无可提取样例的普通题也保留为待补完整数据。

| 状态 | 数量 | 是否在判 |
| --- | ---: | --- |
| generated_tests | 113 | 是 |
| rebuilt_tests | 2 | 是（单题流水线重建，见下） |
| sample_tests | 2 | 是（只有 2 组，仍低于 20 组的线） |
| interactive_requires_judge | 5 | 否 |
| multiple_output_requires_special_judge | 7 | 否 |
| no_extractable_sample | 9 | 否 |
| withheld_pending_rework | 19 | 否（复核打回，见下） |

（另有 `4A` 未列入本表，21 组、在判。）`withheld_pending_rework` 表示曾接入但复核发现
判不出真本事，已从判题队列撤出；原始数据文件保留作离线参考，只有完成逐题参考解、
独立 oracle 和至少 20 组验证后才能恢复。

### 已按单题流水线重建、恢复判题的两道（2026-09-10，T-038）

| 题目 | 原来错在哪 | 重建后 |
| --- | --- | --- |
| 698A | 中央生成器的递推求的是「最少活动天数」（全休息就是 0），21 组期望答案全为 0；一次修补改成 `len(days) - min(...)`，又变成恒等于 `len(days)` | 自带 `samplecode.py`（三状态 DP）+ `producecase.py`（固定种子、8 种形状、含 n=1 与 n=100 两端）；另写穷举 oracle 对 9 组小规模用例交叉验证 0 不一致；参考解 21/21 Accepted，「恒 0」「恒 n」「固定优先写题的贪心」三种错法分别在第 1、1、8 组挂 |
| 1374C | 输入漏写题面要求的 `n` 行、括号串左右不等，正解直接 Runtime Error；答案 `removed + opened` 在均衡串上恒等于正确值的 2 倍 | 同样自带 `samplecode.py` + `producecase.py`；21 组共 2,460 个测试用例经另写的「反复消去 `()`」oracle 交叉验证 0 不一致；**含 t=2000 的上界组**（整批数据此前 t 恒为 1）；参考解 21/21 Accepted，「答案翻倍」「不读 n」「只处理第一组」三种错法全挂 |

两题已从 `scripts/build_codeforces_basic_data.py` 的注册表里摘除，数据只由各自的
`producecase.py` 产出；该脚本同时加了一道保险：`data_status` 为 `withheld_pending_rework`
的题一律跳过，**不生成数据、也不改 catalog**，免得谁跑一次就把撤下的题连同坏数据重新打开。

### 复核打回、等返工的十九道（2026-09-10，T-038）

**数据或判据造错的两道**：

| 题目 | 打回原因 |
| --- | --- |
| 903C | 数据造错题：题面是 Boxes Packing（`n` 个整数），生成器造的是随机小写字符串 + 最大字符频次，正解 Runtime Error |
| 2140B | special checker `concat_divisible` 把首行的 `t` 当成了 `x`，正解 Wrong Answer，19/21 组连库内期望输出都判不过（checker 本身已修，数据待按单题流水线重建） |

**判别力为零的十七道** —— 一个不读输入、只 `print` 常量的程序就能拿 Accepted：

| 打回原因 | 题目 |
| --- | --- |
| 21 组期望输出完全相同 | `270A`（全 NO）、`456A`（全 Happy Alex）、`1374B`（全 -1）、`1475A`（全 YES）、`1742A`／`1829D`／`2227B`（全 NO） |
| 整题只有 1 组样例数据 | `986D`、`1764C`、`1883D`、`1970E1`、`2171G`、`2192D`、`2195E`、`2205D`、`2208C`、`2228D` |

`894E` 与 `1000E` 各只有 2 组，仍在判 —— 常量程序过不了，但同样低于 20 组的线，
应随「至少 20 组」那道闸门一起处理。

## 全部 Codeforces 题目状态

（`4A` 未列入：21 组、在判。）

| 题目 | 状态 | 官方链接 |
| --- | --- | --- |
| 1A | generated_tests | https://codeforces.com/problemset/problem/1/A |
| 1B | generated_tests | https://codeforces.com/problemset/problem/1/B |
| 20B | generated_tests | https://codeforces.com/problemset/problem/20/B |
| 20C | generated_tests | https://codeforces.com/problemset/problem/20/C |
| 25A | generated_tests | https://codeforces.com/problemset/problem/25/A |
| 34B | generated_tests | https://codeforces.com/problemset/problem/34/B |
| 37C | multiple_output_requires_special_judge | https://codeforces.com/problemset/problem/37/C |
| 50A | generated_tests | https://codeforces.com/problemset/problem/50/A |
| 58A | generated_tests | https://codeforces.com/problemset/problem/58/A |
| 69A | generated_tests | https://codeforces.com/problemset/problem/69/A |
| 71A | generated_tests | https://codeforces.com/problemset/problem/71/A |
| 96A | generated_tests | https://codeforces.com/problemset/problem/96/A |
| 112A | generated_tests | https://codeforces.com/problemset/problem/112/A |
| 118A | generated_tests | https://codeforces.com/problemset/problem/118/A |
| 122A | generated_tests | https://codeforces.com/problemset/problem/122/A |
| 131A | generated_tests | https://codeforces.com/problemset/problem/131/A |
| 151A | generated_tests | https://codeforces.com/problemset/problem/151/A |
| 158A | generated_tests | https://codeforces.com/problemset/problem/158/A |
| 158B | generated_tests | https://codeforces.com/problemset/problem/158/B |
| 160A | generated_tests | https://codeforces.com/problemset/problem/160/A |
| 189A | generated_tests | https://codeforces.com/problemset/problem/189/A |
| 200B | generated_tests | https://codeforces.com/problemset/problem/200/B |
| 230A | generated_tests | https://codeforces.com/problemset/problem/230/A |
| 230B | generated_tests | https://codeforces.com/problemset/problem/230/B |
| 231A | generated_tests | https://codeforces.com/problemset/problem/231/A |
| 236A | generated_tests | https://codeforces.com/problemset/problem/236/A |
| 263A | generated_tests | https://codeforces.com/problemset/problem/263/A |
| 266A | generated_tests | https://codeforces.com/problemset/problem/266/A |
| 270A | withheld_pending_rework | https://codeforces.com/problemset/problem/270/A |
| 281A | generated_tests | https://codeforces.com/problemset/problem/281/A |
| 282A | generated_tests | https://codeforces.com/problemset/problem/282/A |
| 313B | generated_tests | https://codeforces.com/problemset/problem/313/B |
| 339A | generated_tests | https://codeforces.com/problemset/problem/339/A |
| 339B | generated_tests | https://codeforces.com/problemset/problem/339/B |
| 363B | generated_tests | https://codeforces.com/problemset/problem/363/B |
| 368B | generated_tests | https://codeforces.com/problemset/problem/368/B |
| 427A | generated_tests | https://codeforces.com/problemset/problem/427/A |
| 431C | generated_tests | https://codeforces.com/problemset/problem/431/C |
| 433B | generated_tests | https://codeforces.com/problemset/problem/433/B |
| 455A | generated_tests | https://codeforces.com/problemset/problem/455/A |
| 456A | withheld_pending_rework | https://codeforces.com/problemset/problem/456/A |
| 460A | generated_tests | https://codeforces.com/problemset/problem/460/A |
| 460B | generated_tests | https://codeforces.com/problemset/problem/460/B |
| 466A | generated_tests | https://codeforces.com/problemset/problem/466/A |
| 466C | generated_tests | https://codeforces.com/problemset/problem/466/C |
| 474A | generated_tests | https://codeforces.com/problemset/problem/474/A |
| 474D | generated_tests | https://codeforces.com/problemset/problem/474/D |
| 479A | generated_tests | https://codeforces.com/problemset/problem/479/A |
| 489B | generated_tests | https://codeforces.com/problemset/problem/489/B |
| 492B | generated_tests | https://codeforces.com/problemset/problem/492/B |
| 508A | generated_tests | https://codeforces.com/problemset/problem/508/A |
| 545C | generated_tests | https://codeforces.com/problemset/problem/545/C |
| 545D | generated_tests | https://codeforces.com/problemset/problem/545/D |
| 550C | generated_tests | https://codeforces.com/problemset/problem/550/C |
| 579A | generated_tests | https://codeforces.com/problemset/problem/579/A |
| 580A | generated_tests | https://codeforces.com/problemset/problem/580/A |
| 580C | generated_tests | https://codeforces.com/problemset/problem/580/C |
| 584A | generated_tests | https://codeforces.com/problemset/problem/584/A |
| 615A | generated_tests | https://codeforces.com/problemset/problem/615/A |
| 698A | rebuilt_tests | https://codeforces.com/problemset/problem/698/A |
| 705A | generated_tests | https://codeforces.com/problemset/problem/705/A |
| 706B | generated_tests | https://codeforces.com/problemset/problem/706/B |
| 723A | generated_tests | https://codeforces.com/problemset/problem/723/A |
| 803A | generated_tests | https://codeforces.com/problemset/problem/803/A |
| 893C | generated_tests | https://codeforces.com/problemset/problem/893/C |
| 894E | sample_tests | https://codeforces.com/problemset/problem/894/E |
| 903C | withheld_pending_rework | https://codeforces.com/problemset/problem/903/C |
| 986B | generated_tests | https://codeforces.com/problemset/problem/986/B |
| 986D | withheld_pending_rework | https://codeforces.com/problemset/problem/986/D |
| 996A | generated_tests | https://codeforces.com/problemset/problem/996/A |
| 1000B | generated_tests | https://codeforces.com/problemset/problem/1000/B |
| 1000E | sample_tests | https://codeforces.com/problemset/problem/1000/E |
| 1154A | generated_tests | https://codeforces.com/problemset/problem/1154/A |
| 1163B2 | generated_tests | https://codeforces.com/problemset/problem/1163/B2 |
| 1195C | generated_tests | https://codeforces.com/problemset/problem/1195/C |
| 1221A | generated_tests | https://codeforces.com/problemset/problem/1221/A |
| 1327A | generated_tests | https://codeforces.com/problemset/problem/1327/A |
| 1328A | generated_tests | https://codeforces.com/problemset/problem/1328/A |
| 1335A | generated_tests | https://codeforces.com/problemset/problem/1335/A |
| 1352A | generated_tests | https://codeforces.com/problemset/problem/1352/A |
| 1352C | generated_tests | https://codeforces.com/problemset/problem/1352/C |
| 1364A | generated_tests | https://codeforces.com/problemset/problem/1364/A |
| 1366D | generated_tests | https://codeforces.com/problemset/problem/1366/D |
| 1374B | withheld_pending_rework | https://codeforces.com/problemset/problem/1374/B |
| 1374C | rebuilt_tests | https://codeforces.com/problemset/problem/1374/C |
| 1398C | generated_tests | https://codeforces.com/problemset/problem/1398/C |
| 1425A | generated_tests | https://codeforces.com/problemset/problem/1425/A |
| 1427B | generated_tests | https://codeforces.com/problemset/problem/1427/B |
| 1443C | generated_tests | https://codeforces.com/problemset/problem/1443/C |
| 1475A | withheld_pending_rework | https://codeforces.com/problemset/problem/1475/A |
| 1520D | generated_tests | https://codeforces.com/problemset/problem/1520/D |
| 1526C1 | generated_tests | https://codeforces.com/problemset/problem/1526/C1 |
| 1729C | generated_tests | https://codeforces.com/problemset/problem/1729/C |
| 1742A | withheld_pending_rework | https://codeforces.com/problemset/problem/1742/A |
| 1749C | generated_tests | https://codeforces.com/problemset/problem/1749/C |
| 1764C | withheld_pending_rework | https://codeforces.com/problemset/problem/1764/C |
| 1793C | multiple_output_requires_special_judge | https://codeforces.com/problemset/problem/1793/C |
| 1829D | withheld_pending_rework | https://codeforces.com/problemset/problem/1829/D |
| 1829E | generated_tests | https://codeforces.com/problemset/problem/1829/E |
| 1833B | generated_tests | https://codeforces.com/problemset/problem/1833/B |
| 1843D | generated_tests | https://codeforces.com/problemset/problem/1843/D |
| 1850H | generated_tests | https://codeforces.com/problemset/problem/1850/H |
| 1868A | generated_tests | https://codeforces.com/problemset/problem/1868/A |
| 1875D | generated_tests | https://codeforces.com/problemset/problem/1875/D |
| 1879B | generated_tests | https://codeforces.com/problemset/problem/1879/B |
| 1881C | generated_tests | https://codeforces.com/problemset/problem/1881/C |
| 1883D | withheld_pending_rework | https://codeforces.com/problemset/problem/1883/D |
| 1970E1 | withheld_pending_rework | https://codeforces.com/problemset/problem/1970/E1 |
| 1970E2 | no_extractable_sample | https://codeforces.com/problemset/problem/1970/E2 |
| 1970E3 | no_extractable_sample | https://codeforces.com/problemset/problem/1970/E3 |
| 1985H1 | generated_tests | https://codeforces.com/problemset/problem/1985/H1 |
| 2033D | generated_tests | https://codeforces.com/problemset/problem/2033/D |
| 2075C | generated_tests | https://codeforces.com/problemset/problem/2075/C |
| 2109C1 | interactive_requires_judge | https://codeforces.com/problemset/problem/2109/C1 |
| 2109C2 | interactive_requires_judge | https://codeforces.com/problemset/problem/2109/C2 |
| 2109C3 | interactive_requires_judge | https://codeforces.com/problemset/problem/2109/C3 |
| 2131C | generated_tests | https://codeforces.com/problemset/problem/2131/C |
| 2132B | generated_tests | https://codeforces.com/problemset/problem/2132/B |
| 2140B | withheld_pending_rework | https://codeforces.com/problemset/problem/2140/B |
| 2146D1 | multiple_output_requires_special_judge | https://codeforces.com/problemset/problem/2146/D1 |
| 2167F | no_extractable_sample | https://codeforces.com/problemset/problem/2167/F |
| 2171D | generated_tests | https://codeforces.com/problemset/problem/2171/D |
| 2171E | generated_tests | https://codeforces.com/problemset/problem/2171/E |
| 2171F | multiple_output_requires_special_judge | https://codeforces.com/problemset/problem/2171/F |
| 2171G | withheld_pending_rework | https://codeforces.com/problemset/problem/2171/G |
| 2173E | interactive_requires_judge | https://codeforces.com/problemset/problem/2173/E |
| 2184F | generated_tests | https://codeforces.com/problemset/problem/2184/F |
| 2192D | withheld_pending_rework | https://codeforces.com/problemset/problem/2192/D |
| 2193D | generated_tests | https://codeforces.com/problemset/problem/2193/D |
| 2193E | generated_tests | https://codeforces.com/problemset/problem/2193/E |
| 2194E | no_extractable_sample | https://codeforces.com/problemset/problem/2194/E |
| 2195E | withheld_pending_rework | https://codeforces.com/problemset/problem/2195/E |
| 2195H | multiple_output_requires_special_judge | https://codeforces.com/problemset/problem/2195/H |
| 2196A | generated_tests | https://codeforces.com/problemset/problem/2196/A |
| 2196B | generated_tests | https://codeforces.com/problemset/problem/2196/B |
| 2200G | generated_tests | https://codeforces.com/problemset/problem/2200/G |
| 2201G | multiple_output_requires_special_judge | https://codeforces.com/problemset/problem/2201/G |
| 2205D | withheld_pending_rework | https://codeforces.com/problemset/problem/2205/D |
| 2208C | withheld_pending_rework | https://codeforces.com/problemset/problem/2208/C |
| 2208D1 | multiple_output_requires_special_judge | https://codeforces.com/problemset/problem/2208/D1 |
| 2209C | interactive_requires_judge | https://codeforces.com/problemset/problem/2209/C |
| 2209E | generated_tests | https://codeforces.com/problemset/problem/2209/E |
| 2218A | generated_tests | https://codeforces.com/problemset/problem/2218/A |
| 2218B | generated_tests | https://codeforces.com/problemset/problem/2218/B |
| 2218C | generated_tests | https://codeforces.com/problemset/problem/2218/C |
| 2218D | generated_tests | https://codeforces.com/problemset/problem/2218/D |
| 2218E | generated_tests | https://codeforces.com/problemset/problem/2218/E |
| 2218F | generated_tests | https://codeforces.com/problemset/problem/2218/F |
| 2218G | no_extractable_sample | https://codeforces.com/problemset/problem/2218/G |
| 2227A | generated_tests | https://codeforces.com/problemset/problem/2227/A |
| 2227B | withheld_pending_rework | https://codeforces.com/problemset/problem/2227/B |
| 2227C | generated_tests | https://codeforces.com/problemset/problem/2227/C |
| 2227D | no_extractable_sample | https://codeforces.com/problemset/problem/2227/D |
| 2227E | no_extractable_sample | https://codeforces.com/problemset/problem/2227/E |
| 2227F | no_extractable_sample | https://codeforces.com/problemset/problem/2227/F |
| 2227H | no_extractable_sample | https://codeforces.com/problemset/problem/2227/H |
| 2228D | withheld_pending_rework | https://codeforces.com/problemset/problem/2228/D |

## 未导入题目

以下题目位于题解文档的 April Fools 专题。它们包含非标准或娱乐性判题机制，
在没有逐题 special judge 策略前不进入本站的精确输出判题库。

| 题目 | 文档行号 | 专题 | 官方链接 |
| --- | ---: | --- | --- |
| 2095A | 22159 | April Fools 2025 TANG | https://codeforces.com/problemset/problem/2095/A |
| 2095B | 22182 | April Fools 2025 TANG | https://codeforces.com/problemset/problem/2095/B |
| 2095C | 22199 | April Fools 2025 TANG | https://codeforces.com/problemset/problem/2095/C |
| 2095D | 22213 | April Fools 2025 TANG | https://codeforces.com/problemset/problem/2095/D |
| 2095E | 22235 | April Fools 2025 TANG | https://codeforces.com/problemset/problem/2095/E |
| 2095F | 22294 | April Fools 2025 TANG | https://codeforces.com/problemset/problem/2095/F |
| 2095G | 22312 | April Fools 2025 TANG | https://codeforces.com/problemset/problem/2095/G |
| 2095H | 22351 | April Fools 2025 TANG | https://codeforces.com/problemset/problem/2095/H |
| 2095I | 22402 | April Fools 2025 TANG | https://codeforces.com/problemset/problem/2095/I |
| 2214A | 22506 | April Fools 2026 TANG | https://codeforces.com/problemset/problem/2214/A |
| 2214B | 22520 | April Fools 2026 TANG | https://codeforces.com/problemset/problem/2214/B |
| 2214D | 22534 | April Fools 2026 TANG | https://codeforces.com/problemset/problem/2214/D |
| 2214E | 22574 | April Fools 2026 TANG | https://codeforces.com/problemset/problem/2214/E |
| 2214H | 22636 | April Fools 2026 TANG | https://codeforces.com/problemset/problem/2214/H |
| 2214J | 22650 | April Fools 2026 TANG | https://codeforces.com/problemset/problem/2214/J |
