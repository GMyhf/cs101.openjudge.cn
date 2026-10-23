# 未接入课题组数据：第3批复核

基线`8f146eead`，详细逐文件哈希、原valid()定义、独立算法、自检、变异及平台回执见[gmyhf-pending-batch3-review.json](gmyhf-pending-batch3-review.json)。

本批20题、599对数据；20题全部核对通过，0题保留疑点。题面字段、后台文件清单及SHA256均已实时回读；本地用当前judge.py的原有限制复判，平台只提交已公开且与origin/main一致的现有参考源码。未修改平台数据、未激活_GMyhf、未改变valid()或索引。

独立复算通过36个题面样例、2000组小域穷举/对拍，20种错误变异均被检出。

| 题号 | 标题 | 数据对数 | 独立方法 | 本地/时限余量 | 平台回执 |
| --- | --- | --- | --- | --- | --- |
| 27933 | Okabe and Boxes | 20 | 实际重排整个栈的物理模拟 | Accepted，最慢0.35% | [Python3 Accepted · 53582261](http://cs101.openjudge.cn/practice/solution/53582261/) |
| 28678 | 角谷猜想 | 20 | 先生成精确整数轨迹再格式化 | Accepted，最慢0.16% | [Python3 Accepted · 53582262](http://cs101.openjudge.cn/practice/solution/53582262/) |
| 28681 | 奖学金 | 20 | 重复选最大者的前五名选择 | Accepted，最慢0.17% | [Python3 Accepted · 53582263](http://cs101.openjudge.cn/practice/solution/53582263/) |
| 28699 | 买水果 | 20 | 通用矩形匈牙利指派求最小/最大费用 | Accepted，最慢0.22% | [Python3 Accepted · 53582265](http://cs101.openjudge.cn/practice/solution/53582265/) |
| 28748 | PKU游戏 | 100 | 逆序集合归属计数与Decimal精确舍入 | Accepted，最慢0.63% | [Python3 Accepted · 53582284](http://cs101.openjudge.cn/practice/solution/53582284/) |
| 28776 | 国王游戏 | 21 | 逆向选择末位并从总乘积回推 | Accepted，最慢0.33% | [Python3 Accepted · 53582266](http://cs101.openjudge.cn/practice/solution/53582266/) |
| 28780 | 零钱兑换3 | 20 | 位集分层BFS最少硬币 | Accepted，最慢67.89% | [Python3 Accepted · 53582268](http://cs101.openjudge.cn/practice/solution/53582268/) |
| 29334 | Excel表列序号 | 20 | 按列字母位置直接求26进制多项式 | Accepted，最慢0.16% | [Python3 Accepted · 53582269](http://cs101.openjudge.cn/practice/solution/53582269/) |
| 29622 | 清北学术走廊规划 | 20 | Prim优先队列最小生成树 | Accepted，最慢0.18% | [Python3 Accepted · 53582270](http://cs101.openjudge.cn/practice/solution/53582270/) |
| 29647 | 没有上司的宴会 | 20 | 树的二分图最大权独立集转最小割 | Accepted，最慢0.19% | [Python3 Accepted · 53582271](http://cs101.openjudge.cn/practice/solution/53582271/) |
| 29662 | 沉没孤岛 | 20 | 并查集合并陆地及边界标记 | Accepted，最慢0.19% | [Python3 Accepted · 53582272](http://cs101.openjudge.cn/practice/solution/53582272/) |
| 29739 | P 大 LLM 驯龙赛 · 脉冲密语对齐 | 47 | 扩展KMP分别求模式Z与各后缀LCP | Accepted，最慢9.04% | [Python3 Accepted · 53582273](http://cs101.openjudge.cn/practice/solution/53582273/) |
| 29741 | 神经网络之国 | 21 | 整数打包多项式乘法的循环卷积幂 | Accepted，最慢4.17% | [Python3 Accepted · 53582274](http://cs101.openjudge.cn/practice/solution/53582274/) |
| 29853 | 小蓝和小桥 | 20 | 差值答案域二分可行区间 | Accepted，最慢0.16% | [Python3 Accepted · 53582275](http://cs101.openjudge.cn/practice/solution/53582275/) |
| 29940 | 机器猫斗恶龙 | 20 | 逆序推回最小所需血量 | Accepted，最慢0.53% | [Python3 Accepted · 53582276](http://cs101.openjudge.cn/practice/solution/53582276/) |
| 29945 | 神秘数字的宇宙旅行 | 20 | 先生成精确整数轨迹再格式化 | Accepted，最慢0.40% | [Python3 Accepted · 53582277](http://cs101.openjudge.cn/practice/solution/53582277/) |
| 29946 | 删数问题 | 20 | 固定保留位数逐位枚举最小后继 | Accepted，最慢0.47% | [Python3 Accepted · 53582278](http://cs101.openjudge.cn/practice/solution/53582278/) |
| 30061 | 春游集合 | 50 | 多重集差集补齐未到学生 | Accepted，最慢0.17% | [Python3 Accepted · 53582280](http://cs101.openjudge.cn/practice/solution/53582280/) |
| 30062 | 非递减子序列 | 50 | 枚举全部位置子集并按数值序列去重 | Accepted，最慢0.24% | [Python3 Accepted · 53582281](http://cs101.openjudge.cn/practice/solution/53582281/) |
| 30085 | 纪念品分组 | 50 | 价格频次表逐组取最大与可配最小 | Accepted，最慢0.26% | [Python3 Accepted · 53582282](http://cs101.openjudge.cn/practice/solution/53582282/) |

输入契约仅使用原valid()；后台包含sample0.in等名称，驱动只将文件遍历排序从数字改为文件名，没有修改校验逻辑。每题本地与平台源码哈希一致。

本批证据不能代表全部359题已完成答案验收。总进度见[gmyhf-pending-progress.json](gmyhf-pending-progress.json)；接入仍须保留原_made契约与针对性覆盖。

28748按题面允许的绝对误差≤10^-6比较概率，并另查每项恰有九位小数及概率和；计数和分母使用精确整数，独立复算用Decimal。
