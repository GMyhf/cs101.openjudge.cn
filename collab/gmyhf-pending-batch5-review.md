# 未接入课题组数据：第5批复核

基线`1b30aa09f`，详细逐文件哈希、原valid()定义、独立算法、自检、变异及平台回执见[gmyhf-pending-batch5-review.json](gmyhf-pending-batch5-review.json)。

本批20题、444对数据；1题全部核对通过，19题保留疑点。题面字段、后台文件清单及SHA256均已实时回读；本地用当前judge.py的原有限制复判，平台提交现有公开参考源码；若需拆分多题分派器，另附单题分支提取及逐文件等价证明。未修改平台数据、未激活_GMyhf、未改变valid()或索引。

独立复算通过42个题面样例、5266组小域穷举/对拍，20种错误变异均被检出。

| 题号 | 标题 | 数据对数 | 独立方法 | 本地/时限余量 | 平台回执 |
| --- | --- | --- | --- | --- | --- |
| 28750 | 倾斜方块 | 55 | 独立扁平重力模拟、KMP周期与增量CRT | Accepted，最慢44.06% | [Python3 Accepted · 53582369](http://cs101.openjudge.cn/practice/solution/53582369/) |
| 18071 | 成环 | 20 | 并查集检出网格新增边闭环 | Accepted，最慢0.22% | [Python3 Accepted · 53582370](http://cs101.openjudge.cn/practice/solution/53582370/) |
| 18076 | 链状基团大小判定 | 20 | 递归比较局部原子序列和最大支链 | Wrong Answer | [Python3 Accepted · 53582371](http://cs101.openjudge.cn/practice/solution/53582371/) |
| 18209 | 计算信息熵 | 20 | 60位Decimal自然对数换底求熵 | Accepted，最慢0.26% | [Python3 Accepted · 53582374](http://cs101.openjudge.cn/practice/solution/53582374/) |
| 19947 | 新型材料v0.2 | 22 | 圆弧半周配对的可行性条件 | Accepted，最慢0.53% | [Python3 Accepted · 53582375](http://cs101.openjudge.cn/practice/solution/53582375/) |
| 19948 | 因材施教 | 22 | 保留最小n-m个相邻差 | Accepted，最慢0.86% | [Python3 Accepted · 53582376](http://cs101.openjudge.cn/practice/solution/53582376/) |
| 19962 | 快递点 | 20 | 选择中位数后直接求绝对偏差 | Accepted，最慢0.65% | [Python3 Accepted · 53582377](http://cs101.openjudge.cn/practice/solution/53582377/) |
| 20004 | 最大回撤率Biggest Drawdown | 24 | 80位Decimal前向峰值回撤 | Accepted，最慢0.42% | [Python3 Accepted · 53582378](http://cs101.openjudge.cn/practice/solution/53582378/) |
| 20103 | 繁荣的步行街v0.2 | 20 | 筛合法申请后按右端点区间调度 | Accepted，最慢2.30% | [Python3 Accepted · 53582379](http://cs101.openjudge.cn/practice/solution/53582379/) |
| 20123 | 7-友好数 | 20 | 数字子序列模7可达状态 | Accepted，最慢0.17% | [Python3 Accepted · 53582381](http://cs101.openjudge.cn/practice/solution/53582381/) |
| 21535 | 打怪兽II | 20 | 可击杀生命值频数预算分配 | Accepted，最慢0.30% | [Python3 Accepted · 53582382](http://cs101.openjudge.cn/practice/solution/53582382/) |
| 21727 | 湾仔码头 | 20 | 0/1背包求最大件数 | Accepted，最慢0.22% | [Python3 Accepted · 53582383](http://cs101.openjudge.cn/practice/solution/53582383/) |
| 21728 | 排队做实验 | 20 | 各时长等待贡献加权和 | Accepted，最慢0.24% | [Python3 Accepted · 53582384](http://cs101.openjudge.cn/practice/solution/53582384/) |
| 23554 | 小朋友春游 | 20 | 编号频次缺失及乱入排序 | Accepted，最慢0.31% | [Python3 Accepted · 53582393](http://cs101.openjudge.cn/practice/solution/53582393/) |
| 23563 | 多项式时间复杂度 | 21 | 同次幂合并系数后取非零最高次 | Accepted，最慢0.23% | [Python3 Accepted · 53582386](http://cs101.openjudge.cn/practice/solution/53582386/) |
| 25570 | 洋葱 | 20 | 按到边界最短距离分层累加 | Accepted，最慢0.35% | [Python3 Accepted · 53582394](http://cs101.openjudge.cn/practice/solution/53582394/) |
| 25573 | 红蓝玫瑰 | 20 | 前缀反转奇偶两状态动态规划 | Accepted，最慢1.18% | [Python3 Accepted · 53582388](http://cs101.openjudge.cn/practice/solution/53582388/) |
| 25580 | 木板掉落 | 20 | Decimal速度次序阈值推导高度 | Accepted，最慢0.23% | [Python3 Accepted · 53582389](http://cs101.openjudge.cn/practice/solution/53582389/) |
| 27301 | 给植物浇水 | 20 | 分配两人已定路径独立记账 | Accepted，最慢0.19% | [Python3 Accepted · 53582390](http://cs101.openjudge.cn/practice/solution/53582390/) |
| 27306 | 植物观察 | 20 | 异或约束图逐分量染色 | Accepted，最慢0.20% | [Python3 Accepted · 53582391](http://cs101.openjudge.cn/practice/solution/53582391/) |

原valid()完整保留；后台包含sample0.in等名称，驱动只将文件遍历排序从数字改为文件名，没有修改校验逻辑。平台原始提交与公开origin/main源码哈希一致；若存在platform_specialization，则保留原始回执、提取源码哈希与逐文件输出等价证明。

本批证据不能代表全部359题已完成答案验收。总进度见[gmyhf-pending-progress.json](gmyhf-pending-progress.json)；接入仍须保留原_made契约与针对性覆盖。


## 保留疑点

- 18071：原valid拒绝20对；尚须区分排版/生成器额外约束/题面违规。
- 18076：原valid拒绝20对；尚须区分排版/生成器额外约束/题面违规；独立答案不匹配：18.in；本地判题或时限余量未通过。
- 18209：原valid拒绝20对；尚须区分排版/生成器额外约束/题面违规。
- 19947：原valid拒绝22对；尚须区分排版/生成器额外约束/题面违规。
- 19948：原valid拒绝22对；尚须区分排版/生成器额外约束/题面违规。
- 19962：原valid拒绝20对；尚须区分排版/生成器额外约束/题面违规。
- 20004：原valid拒绝24对；尚须区分排版/生成器额外约束/题面违规。
- 20103：原valid拒绝20对；尚须区分排版/生成器额外约束/题面违规。
- 20123：原valid拒绝20对；尚须区分排版/生成器额外约束/题面违规。
- 21535：原valid拒绝20对；尚须区分排版/生成器额外约束/题面违规。
- 21727：原valid拒绝18对；尚须区分排版/生成器额外约束/题面违规。
- 21728：原valid拒绝20对；尚须区分排版/生成器额外约束/题面违规。
- 23554：原valid拒绝20对；尚须区分排版/生成器额外约束/题面违规。
- 23563：原valid拒绝20对；尚须区分排版/生成器额外约束/题面违规。
- 25570：原valid拒绝18对；尚须区分排版/生成器额外约束/题面违规。
- 25573：原valid拒绝20对；尚须区分排版/生成器额外约束/题面违规。
- 25580：原valid拒绝6对；尚须区分排版/生成器额外约束/题面违规。
- 27301：原valid拒绝20对；尚须区分排版/生成器额外约束/题面违规。
- 27306：原valid拒绝2对；尚须区分排版/生成器额外约束/题面违规。

原valid拒绝时，另用逐行规范空白的文本调用原函数并跟踪False返回位置；两次结果及原始代码行均在contract_diagnostic。规范空白后通过只说明排版差异，未修改原始输入、valid或接入状态；仍拒绝的条目须按具体题面继续区分数值范围、结构约束与生成器额外约束。

23554、25570的原公开程序为多题分派器，平台先判Compile Error；按oj_submit.py记载的pylint限制提取对应AST分支，逐文件完整输出与原程序一致后，单题程序均获Python3 Accepted。两个原CE回执与提取程序一并保留。
