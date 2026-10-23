# 未接入课题组数据：第2批复核

基线`737c08091`，详细逐文件哈希、原valid()定义、独立算法、自检、变异及平台回执见[gmyhf-pending-batch2-review.json](gmyhf-pending-batch2-review.json)。

本批10题、206对数据；10题全部核对通过，0题保留疑点。题面字段、后台文件清单及SHA256均已实时回读；本地用当前judge.py的原有限制复判，平台只提交已公开且与origin/main一致的现有参考源码。未修改平台数据、未激活_GMyhf、未改变valid()或索引。

独立复算通过16个题面样例、1088组小域穷举/对拍，10种错误变异均被检出。

| 题号 | 标题 | 数据对数 | 独立方法 | 本地/时限余量 | 平台回执 |
| --- | --- | --- | --- | --- | --- |
| 25394 | 获得的牌的张数最多 | 21 | 三选一差值DP最大化用牌数 | Accepted，最慢8.30% | [Python3 Accepted · 53582230](http://cs101.openjudge.cn/practice/solution/53582230/) |
| 27217 | 有多少种合法的出栈顺序 | 22 | 精确整数Catalan闭式 | Accepted，最慢1.84% | [Python3 Accepted · 53582231](http://cs101.openjudge.cn/practice/solution/53582231/) |
| 27273 | 简单的数学题 | 20 | 整数位长计算幂次几何级数 | Accepted，最慢0.18% | [Python3 Accepted · 53582219](http://cs101.openjudge.cn/practice/solution/53582219/) |
| 27274 | 字符串提炼 | 20 | 直接计算交替抽取位置 | Accepted，最慢0.21% | [Python3 Accepted · 53582221](http://cs101.openjudge.cn/practice/solution/53582221/) |
| 27277 | 凑硬币 | 20 | 金额图BFS最少边数 | Accepted，最慢0.56% | [Python3 Accepted · 53582222](http://cs101.openjudge.cn/practice/solution/53582222/) |
| 27278 | 完美的备考策略 | 20 | 倒序积累复习债务与二分天数 | Accepted，最慢3.18% | [Python3 Accepted · 53582224](http://cs101.openjudge.cn/practice/solution/53582224/) |
| 27310 | 积木 | 20 | 字母与积木的增广匹配 | Accepted，最慢0.19% | [Python3 Accepted · 53582225](http://cs101.openjudge.cn/practice/solution/53582225/) |
| 27421 | 接雨水 II | 22 | 高度激活并查集连通外界时结算蓄水 | Accepted，最慢1.73% | [Python3 Accepted · 53582233](http://cs101.openjudge.cn/practice/solution/53582233/) |
| 27635 | 判断无向图是否连通有无回路(同23163) | 21 | 并查集统计分量及成环边 | Accepted，最慢0.21% | [Python3 Accepted · 53582234](http://cs101.openjudge.cn/practice/solution/53582234/) |
| 27932 | Less or Equal | 20 | 答案数值域二分计数首次达到k | Accepted，最慢0.35% | [Python3 Accepted · 53582228](http://cs101.openjudge.cn/practice/solution/53582228/) |

输入契约仅使用原valid()；后台包含sample0.in等名称，驱动只将文件遍历排序从数字改为文件名，没有修改校验逻辑。每题本地与平台源码哈希一致。

本批证据不能代表全部359题已完成答案验收。总进度见[gmyhf-pending-progress.json](gmyhf-pending-progress.json)；接入仍须保留原_made契约与针对性覆盖。
