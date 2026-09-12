# Codeforces 原题题面

题面由 `scripts/fetch_codeforces_statements.py` 抓取、`scripts/build_codeforces_pages.py` 渲染成 `data/openjudge/pages/codeforces__*.html`。
抓回来的原文留在 `data/openjudge/statements/<题号>.json`，页面可以随时按它重建、复核。

## 来源

`codeforces.com` 对本机返回 Cloudflare 403，`m1.codeforces.com` 镜像把每个页面都挡在登录后，
所以题面取自洛谷的 Codeforces 远程评测镜像：它的页面数据里带 Codeforces 英文原文
（`content`：description / formatI / formatO / hint）、全部官方样例和官方时限内存。
每条记录都同时保留 `source_url`（Codeforces 原题）和 `mirror_url`（抓取地址）。

交叉验证：4A 的时限内存（1 秒 / 64 MB）与本站此前人工核对过的 4A 页面逐字相同；
158 道题的样例全部能被 `server.py:sample_io()` 原样切回抓取到的官方样例。

## 重新抓取与重建

```bash
python3 scripts/fetch_codeforces_statements.py            # 只抓缺的；--refresh 全部重抓
python3 scripts/build_codeforces_pages.py                 # 重建题面页并刷新本文件
python3 scripts/mirror_openjudge_images.py                # 新题面引入的插图要进本地镜像
```

`4A` 的页面不由本脚本覆盖（`--keep`），它是此前人工核对过的那一版。

## 覆盖

- 题目：158 道
- 有 Note（官方样例解释）：109 道
- 多组样例：60 道
- 带插图：23 道

| 题目 | 标题 | 时限 | 内存 | 样例 | 抓取日期 | 官方链接 |
| --- | --- | ---: | ---: | ---: | --- | --- |
| 1A | Theatre Square | 1 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1/A |
| 1B | Spreadsheets | 10 s | 64 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1/B |
| 4A | Watermelon | 1 s | 64 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/4/A |
| 20B | Equation | 1 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/20/B |
| 20C | Dijkstra? | 1 s | 64 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/20/C |
| 25A | IQ test | 2 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/25/A |
| 34B | Sale | 2 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/34/B |
| 37C | Old Berland Language | 2 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/37/C |
| 50A | Domino piling | 2 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/50/A |
| 58A | Chat room | 1 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/58/A |
| 69A | Young Physicist | 2 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/69/A |
| 71A | Way Too Long Words | 1 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/71/A |
| 96A | Football | 2 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/96/A |
| 112A | Petya and Strings | 2 s | 256 MB | 3 | 2026-09-12 | https://codeforces.com/problemset/problem/112/A |
| 118A | String Task | 2 s | 256 MB | 3 | 2026-09-12 | https://codeforces.com/problemset/problem/118/A |
| 122A | Lucky Division | 2 s | 256 MB | 3 | 2026-09-12 | https://codeforces.com/problemset/problem/122/A |
| 131A | cAPS lOCK | 0.5 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/131/A |
| 151A | Soft Drinking | 2 s | 256 MB | 3 | 2026-09-12 | https://codeforces.com/problemset/problem/151/A |
| 158A | Next Round | 3 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/158/A |
| 158B | Taxi | 3 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/158/B |
| 160A | Twins | 2 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/160/A |
| 189A | Cut Ribbon | 1 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/189/A |
| 200B | Drinks | 2 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/200/B |
| 230A | Dragons | 2 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/230/A |
| 230B | T-primes | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/230/B |
| 231A | Team | 2 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/231/A |
| 236A | Boy or Girl | 1 s | 256 MB | 3 | 2026-09-12 | https://codeforces.com/problemset/problem/236/A |
| 263A | Beautiful Matrix | 2 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/263/A |
| 266A | Stones on the Table | 2 s | 256 MB | 3 | 2026-09-12 | https://codeforces.com/problemset/problem/266/A |
| 270A | Fancy Fence | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/270/A |
| 281A | Word Capitalization | 2 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/281/A |
| 282A | Bit++ | 1 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/282/A |
| 313B | Ilya and Queries | 2 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/313/B |
| 339A | Helpful Maths | 2 s | 256 MB | 3 | 2026-09-12 | https://codeforces.com/problemset/problem/339/A |
| 339B | Xenia and Ringroad | 2 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/339/B |
| 363B | Fence | 1 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/363/B |
| 368B | Sereja and Suffixes | 1 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/368/B |
| 427A | Police Recruits | 1 s | 256 MB | 3 | 2026-09-12 | https://codeforces.com/problemset/problem/427/A |
| 431C | k-Tree | 1 s | 256 MB | 4 | 2026-09-12 | https://codeforces.com/problemset/problem/431/C |
| 433B | Kuriyama Mirai's Stones | 2 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/433/B |
| 455A | Boredom | 1 s | 256 MB | 3 | 2026-09-12 | https://codeforces.com/problemset/problem/455/A |
| 456A | Laptops | 1 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/456/A |
| 460A | Vasya and Socks | 1 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/460/A |
| 460B | Little Dima and Equation | 1 s | 256 MB | 3 | 2026-09-12 | https://codeforces.com/problemset/problem/460/B |
| 466A | Cheap Travel | 1 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/466/A |
| 466C | Number of Ways | 2 s | 256 MB | 3 | 2026-09-12 | https://codeforces.com/problemset/problem/466/C |
| 474A | Keyboard | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/474/A |
| 474D | Flowers | 1.5 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/474/D |
| 479A | Expression | 1 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/479/A |
| 489B | BerSU Ball | 1 s | 256 MB | 3 | 2026-09-12 | https://codeforces.com/problemset/problem/489/B |
| 492B | Vanya and Lanterns | 1 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/492/B |
| 508A | Pasha and Pixels | 2 s | 256 MB | 3 | 2026-09-12 | https://codeforces.com/problemset/problem/508/A |
| 545C | Woodcutters | 1 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/545/C |
| 545D | Queue | 1 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/545/D |
| 550C | Divisibility by Eight | 2 s | 256 MB | 3 | 2026-09-12 | https://codeforces.com/problemset/problem/550/C |
| 579A | Raising Bacteria | 1 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/579/A |
| 580A | Kefa and First Steps | 2 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/580/A |
| 580C | Kefa and Park | 2 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/580/C |
| 584A | Olesya and Rodion | 1 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/584/A |
| 615A | Bulbs | 1 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/615/A |
| 698A | Vacations | 1 s | 256 MB | 3 | 2026-09-12 | https://codeforces.com/problemset/problem/698/A |
| 705A | Hulk | 1 s | 256 MB | 3 | 2026-09-12 | https://codeforces.com/problemset/problem/705/A |
| 706B | Interesting drink | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/706/B |
| 723A | The New Year: Meeting Friends | 1 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/723/A |
| 803A | Maximal Binary Matrix | 1 s | 256 MB | 3 | 2026-09-12 | https://codeforces.com/problemset/problem/803/A |
| 893C | Rumor | 2 s | 256 MB | 3 | 2026-09-12 | https://codeforces.com/problemset/problem/893/C |
| 894E | Ralph and Mushrooms | 2.5 s | 512 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/894/E |
| 903C | Boxes Packing | 1 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/903/C |
| 986B | Petr and Permutations | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/986/B |
| 986D | Perfect Encoding | 2 s | 256 MB | 3 | 2026-09-12 | https://codeforces.com/problemset/problem/986/D |
| 996A | Hit the Lottery | 1 s | 256 MB | 3 | 2026-09-12 | https://codeforces.com/problemset/problem/996/A |
| 1000B | Light It Up | 1 s | 256 MB | 3 | 2026-09-12 | https://codeforces.com/problemset/problem/1000/B |
| 1000E | We Need More Bosses | 2 s | 256 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/1000/E |
| 1154A | Restoring Three Numbers | 1 s | 256 MB | 3 | 2026-09-12 | https://codeforces.com/problemset/problem/1154/A |
| 1163B2 | Cat Party (Hard Edition) | 1 s | 256 MB | 5 | 2026-09-12 | https://codeforces.com/problemset/problem/1163/B2 |
| 1195C | Basketball Exercise | 2 s | 256 MB | 3 | 2026-09-12 | https://codeforces.com/problemset/problem/1195/C |
| 1221A | 2048 Game | 1 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1221/A |
| 1327A | Sum of Odd Integers | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1327/A |
| 1328A | Divisibility Problem | 1 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1328/A |
| 1335A | Candies and Two Sisters | 1 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1335/A |
| 1352A | Sum of Round Numbers | 1 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1352/A |
| 1352C | K-th Not Divisible by n | 1 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1352/C |
| 1364A | XXXXX | 1 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1364/A |
| 1366D | Two Divisors | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1366/D |
| 1374B | Multiply by 2, divide by 6 | 1 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1374/B |
| 1374C | Move Brackets | 1 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1374/C |
| 1398C | Good Subarrays | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1398/C |
| 1425A | Arena of Greed | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1425/A |
| 1427B | Chess Cheater | 1 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1427/B |
| 1443C | The Delivery Dilemma | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1443/C |
| 1475A | Odd Divisor | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1475/A |
| 1520D | Same Differences | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1520/D |
| 1526C1 | Potions (Easy Version) | 1 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1526/C1 |
| 1729C | Jumping on Tiles | 1 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1729/C |
| 1742A | Sum | 1 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1742/A |
| 1749C | Number Game | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1749/C |
| 1764C | Doremy's City Construction | 1 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1764/C |
| 1793C | Dora and Search | 1 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1793/C |
| 1829D | Gold Rush | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1829/D |
| 1829E | The Lakes | 3 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1829/E |
| 1833B | Restore the Weather | 1 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1833/B |
| 1843D | Apple Tree | 4 s | 512 MB | 2 | 2026-09-12 | https://codeforces.com/problemset/problem/1843/D |
| 1850H | The Third Letter | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1850/H |
| 1868A | Fill in the Matrix | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1868/A |
| 1875D | Jellyfish and Mex | 1 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1875/D |
| 1879B | Chips on the Board | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1879/B |
| 1881C | Perfect Square | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1881/C |
| 1883D | In Love | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1883/D |
| 1970E1 | Trails (Easy) | 1 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1970/E1 |
| 1970E2 | Trails (Medium) | 1 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1970/E2 |
| 1970E3 | Trails (Hard) | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1970/E3 |
| 1985H1 | Maximize the Largest Component (Easy Version) | 2 s | 512 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/1985/H1 |
| 2033D | Kousuke's Assignment | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2033/D |
| 2075C | Two Colors | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2075/C |
| 2109C1 | Hacking Numbers (Easy Version) | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2109/C1 |
| 2109C2 | Hacking Numbers (Medium Version) | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2109/C2 |
| 2109C3 | Hacking Numbers (Hard Version) | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2109/C3 |
| 2131C | Make it Equal | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2131/C |
| 2132B | The Secret Number | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2132/B |
| 2140B | Another Divisibility Problem | 1 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2140/B |
| 2146D1 | Max Sum OR (Easy Version) | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2146/D1 |
| 2167F | Tree, TREE!!! | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2167/F |
| 2171D | Rae Taylor and Trees (easy version) | 3 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2171/D |
| 2171E | Anisphia Wynn Palettia and Good Permutations | 3 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2171/E |
| 2171F | Rae Taylor and Trees (hard version) | 3 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2171/F |
| 2171G | Sakura Adachi and Optimal Sequences | 4 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2171/G |
| 2173E | Shiro's Mirror Duel | 3 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2173/E |
| 2184F | Cherry Tree | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2184/F |
| 2192D | Cost of Tree | 3 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2192/D |
| 2193D | Monster Game | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2193/D |
| 2193E | Product Queries | 3 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2193/E |
| 2194E | The Turtle Strikes Back | 2 s | 512 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2194/E |
| 2195E | Idiot First Search | 2 s | 512 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2195/E |
| 2195H | Codeforces Heuristic Contest 001 | 4 s | 1024 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2195/H |
| 2196A | Game with a Fraction | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2196/A |
| 2196B | Another Problem about Beautiful Pairs | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2196/B |
| 2200G | Operation Permutation | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2200/G |
| 2201G | Codeforces Heuristic Contest 1001 | 9 s | 1001 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2201/G |
| 2205D | Simons and Beating Peaks | 2 s | 512 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2205/D |
| 2208C | Stamina and Tasks | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2208/C |
| 2208D1 | Tree Orientation (Easy Version) | 3 s | 1024 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2208/D1 |
| 2209C | Find the Zero | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2209/C |
| 2209E | A Trivial String Problem | 4 s | 1024 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2209/E |
| 2218A | The 67th Integer Problem | 1 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2218/A |
| 2218B | The 67th 6-7 Integer Problem | 1 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2218/B |
| 2218C | The 67th Permutation Problem | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2218/C |
| 2218D | The 67th OEIS Problem | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2218/D |
| 2218E | The 67th XOR Problem | 3 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2218/E |
| 2218F | The 67th Tree Problem | 4 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2218/F |
| 2218G | The 67th Iteration of "Counting is Fun" | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2218/G |
| 2227A | Koshary | 1 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2227/A |
| 2227B | Party Monster | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2227/B |
| 2227C | Snowfall | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2227/C |
| 2227D | Palindromex | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2227/D |
| 2227E | It All Went Sideways | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2227/E |
| 2227F | It Just Keeps Going Sideways | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2227/F |
| 2227H | Fallen Leaves | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2227/H |
| 2228D | Sanae, Cross and Color | 2 s | 256 MB | 1 | 2026-09-12 | https://codeforces.com/problemset/problem/2228/D |
