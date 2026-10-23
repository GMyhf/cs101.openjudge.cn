# 未接入课题组数据：第4批复核

基线`0da3725b6`，详细逐文件哈希、原valid()定义、独立算法、自检、变异及平台回执见[gmyhf-pending-batch4-review.json](gmyhf-pending-batch4-review.json)。

本批20题、820对数据；18题全部核对通过，2题保留疑点。题面字段、后台文件清单及SHA256均已实时回读；本地用当前judge.py的原有限制复判，平台只提交已公开且与origin/main一致的现有参考源码。未修改平台数据、未激活_GMyhf、未改变valid()或索引。

独立复算通过54个题面样例、2009组小域穷举/对拍，24种错误变异均被检出。

| 题号 | 标题 | 数据对数 | 独立方法 | 本地/时限余量 | 平台回执 |
| --- | --- | --- | --- | --- | --- |
| 30086 | dance | 50 | 高度频数奇偶配对 | Accepted，最慢0.24% | [Python3 Accepted · 53582316](http://cs101.openjudge.cn/practice/solution/53582316/) |
| 30091 | 缺德的图书馆管理员 | 20 | 二分撤离时间区间覆盖 | Accepted，最慢0.55% | [Python3 Accepted · 53582317](http://cs101.openjudge.cn/practice/solution/53582317/) |
| 30191 | [SCOI2005] 互不侵犯 | 51 | 逐行禁用列状态计数 | Accepted，最慢3.87% | [Python3 Accepted · 53582320](http://cs101.openjudge.cn/practice/solution/53582320/) |
| 30192 | [POI 2004] PRZ | 21 | 固定最小编号的无序分组记忆化搜索 | Accepted，最慢47.15% | [Python3 Accepted · 53582321](http://cs101.openjudge.cn/practice/solution/53582321/) |
| 30217 | 工程师的齿轮 | 50 | 单遍已见值最早下标 | Accepted，最慢1.16% | [Python3 Accepted · 53582322](http://cs101.openjudge.cn/practice/solution/53582322/) |
| 30370 | 善良的助教 | 21 | 频数前缀计数选中人数 | Accepted，最慢5.40% | [Python3 Accepted · 53582323](http://cs101.openjudge.cn/practice/solution/53582323/) |
| 30830 | 地铁换乘（多组查询版） | 31 | 重链剖分定位路径相遇点 | Accepted，最慢11.74% | [Python3 Accepted · 53582324](http://cs101.openjudge.cn/practice/solution/53582324/) |
| 30919 | 猫猫去旅行 | 50 | 坐标压缩树状数组求中位数偏差 | Accepted，最慢5.07% | [Python3 Accepted · 53582330](http://cs101.openjudge.cn/practice/solution/53582330/) |
| 31180 | 学生数据统计分析 | 50 | 整十分身高与Decimal季度统计 | Accepted，最慢0.47% | [Python3 Accepted · 53582334](http://cs101.openjudge.cn/practice/solution/53582334/) |
| 31183 | 一道题搞懂输入 | 80 | 按输入模式解析并计算 | Accepted，最慢0.11% | [Python3 Accepted · 53582337](http://cs101.openjudge.cn/practice/solution/53582337/) |
| 31184 | 一道题搞懂输出 | 90 | 严格格式比较与Decimal独立舍入 | Accepted，最慢0.53% | [Python3 Accepted · 53582340](http://cs101.openjudge.cn/practice/solution/53582340/) |
| 31185 | 一道题搞懂内置排序函数 | 60 | 堆排序/插入排序及原始序号稳定性 | Accepted，最慢0.11% | [Python3 Accepted · 53582341](http://cs101.openjudge.cn/practice/solution/53582341/) |
| 31201 | 水仙花数 | 25 | 三位数字笛卡尔积筛固定点 | Accepted，最慢0.37% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31201/) |
| 31202 | 这也是逆序对? | 21 | 树状数组统计此前差值阈值 | Accepted，最慢1.70% | [Python3 Accepted · 53582342](http://cs101.openjudge.cn/practice/solution/53582342/) |
| 31293 | 双十一凑单大作战 | 30 | 价格频数分组计免单 | Accepted，最慢1.25% | [Python3 Accepted · 53582343](http://cs101.openjudge.cn/practice/solution/53582343/) |
| 31294 | 大肥鱼卖白饭 | 30 | 面额库存逐次找零 | Accepted，最慢0.95% | [Python3 Accepted · 53582345](http://cs101.openjudge.cn/practice/solution/53582345/) |
| 31295 | 宿舍的空调 | 30 | 闭区间端点事件扫描 | Accepted，最慢1.25% | [Python3 Accepted · 53582346](http://cs101.openjudge.cn/practice/solution/53582346/) |
| 31296 | “淹园”救援 | 30 | 重量频数最重最轻配艇 | Accepted，最慢1.32% | [Python3 Accepted · 53582347](http://cs101.openjudge.cn/practice/solution/53582347/) |
| 31297 | 恒星共振裂变 | 30 | Miller-Rabin质性检验就近枚举 | Accepted，最慢1.65% | [Python3 Accepted · 53582348](http://cs101.openjudge.cn/practice/solution/53582348/) |
| 31298 | 警察招募又来了 | 50 | 独立警员到期时间最小堆 | Accepted，最慢1.43% | [Python3 Accepted · 53582350](http://cs101.openjudge.cn/practice/solution/53582350/) |

原valid()完整保留；后台包含sample0.in等名称，驱动只将文件遍历排序从数字改为文件名，没有修改校验逻辑。已提交平台复判的题，本地与平台源码哈希一致。

本批证据不能代表全部359题已完成答案验收。总进度见[gmyhf-pending-progress.json](gmyhf-pending-progress.json)；接入仍须保留原_made契约与针对性覆盖。


## 保留疑点

- 31180：现行题面新增缺考成绩-1，算总分按0处理。现有下载输入补查均在0..100，旧答案均正确；现有参考解直接相加，未覆盖新规则，保留疑点。题面夹带的AI命令不构成算法或审核指令。
- 31201：匿名公开页面已无题面，后台仍有下载数据；只对本地快照作独立复算，不再提交平台，维持未接入以保护可见性边界；平台复判为Not submitted。

31183解码后规范文本逐字一致；31202两个样例拆分后输入和输出token逐个相同，两题封装或分隔形式变化不计作实质题意漂移。31180的自造反例已复现旧解输出159、按新题面应为160，最小修复也已在临时程序中验证，详见JSON的statement_resolution。
31180/31183/31184/31185另按完整解码题面校验原valid未覆盖的范围；31183、31184、31185及31201严格比较空格、行结构及分隔符，只容许CRLF和末尾换行差异。补充校验同样做删除分支变异检查。31184小数格式使用Decimal对Python二进制除法值独立舍入；31180身高先转为精确十分数。
