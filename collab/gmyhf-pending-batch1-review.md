# 未接入课题组数据：首批十题复核

任务T-057，基线`7c54a2c29`。详细文件哈希、回执和完整复核程序见[gmyhf-pending-batch1-review.json](gmyhf-pending-batch1-review.json)。

本批10题、200对下载数据未发现需要修正的输入或答案。这里只记录复核，不激活数据：原_made、valid()、题库索引及平台文件均未修改。

匿名回读平台题面，描述、输入、输出、两个样例字段与本地镜像一致；后台逐文件重新下载400个.in/.out，文件清单及SHA256均与原快照一致。

全部200份输入通过原有valid()。独立算法复算200份答案全部一致，并通过19个题面样例及2817组小域自检；每种算法改坏一处，10项变异均被检出。

| 题号 | 标题 | 独立复算方法 | 本地结果 | 最慢单点/时限 |
| --- | --- | --- | --- | --- |
| 19942 | 二维矩阵上的卷积运算 | 正负系数分离的整数打包多项式乘法 | 20/20 Accepted | 0.16% |
| 19943 | 图的拉普拉斯矩阵 | 邻接计数与行和度数重建 | 20/20 Accepted | 0.15% |
| 19946 | 汉堡王v0.2 | 阈值二分图的Hall最大亏量 | 20/20 Accepted | 0.16% |
| 19949 | 提取实体 | 正则匹配各句连续标注词段 | 20/20 Accepted | 0.15% |
| 20137 | 贪吃蛇custom v0.2 | 几何轨迹模拟，记录整数点及对角线中点 | 20/20 Accepted | 0.15% |
| 23555 | 节省存储的矩阵乘法 | 稠密矩阵行列整数内积 | 20/20 Accepted | 0.40% |
| 23556 | 小青蛙跳荷叶 | 精确整数二项式求和 | 20/20 Accepted | 0.17% |
| 25684 | 食堂找座位 | 按到达时间扫描，用最小堆释放到期组 | 20/20 Accepted | 0.17% |
| 26998 | 最长奇异子序列 | 按DP长度分层、聚合末项按位或后查最长可接层 | 20/20 Accepted | 8.57% |
| 27237 | 体育游戏跳房子 | 深度迭代与精确可达上下界剪枝，H优先保证字典序 | 20/20 Accepted | 3.06% |

本地真实判题只临时替换catalog_item返回值中的测试文件列表，运行当前judge.py原有编译、CPU/内存/文件/总时限和隔离链路；未修改判题器或生产目录。每题均通过75%逐点余量检查，最慢26998为8.57%。

20137另以线段严格相交检查核对小地图，覆盖整数点之外的身体交叉；27237用小域前向BFS核对最短长度和H优先字典序；19946用通用增广匹配核对Hall亏量算法。23556全程使用精确整数。26998的分层算法只作独立答案审核，最坏二次，不作为线上参考解替换。

用户补充明确授权后，10题现有参考源码均以Python3提交到OpenJudge，全部Accepted，源码SHA256与本地AC证据一致，无需切换PyPy3。上一轮审批因授权不足拒绝的提交已完成补验。

| 题号 | 平台结果 | 提交回执 |
| --- | --- | --- |
| 19942 | Python3 Accepted | [53582014](http://cs101.openjudge.cn/practice/solution/53582014/) |
| 19943 | Python3 Accepted | [53582015](http://cs101.openjudge.cn/practice/solution/53582015/) |
| 19946 | Python3 Accepted | [53582016](http://cs101.openjudge.cn/practice/solution/53582016/) |
| 19949 | Python3 Accepted | [53582017](http://cs101.openjudge.cn/practice/solution/53582017/) |
| 20137 | Python3 Accepted | [53582018](http://cs101.openjudge.cn/practice/solution/53582018/) |
| 23555 | Python3 Accepted | [53582019](http://cs101.openjudge.cn/practice/solution/53582019/) |
| 23556 | Python3 Accepted | [53582022](http://cs101.openjudge.cn/practice/solution/53582022/) |
| 25684 | Python3 Accepted | [53582023](http://cs101.openjudge.cn/practice/solution/53582023/) |
| 26998 | Python3 Accepted | [53582024](http://cs101.openjudge.cn/practice/solution/53582024/) |
| 27237 | Python3 Accepted | [53582025](http://cs101.openjudge.cn/practice/solution/53582025/) |

已推送基线`7c54a2c29`的[CI gate](https://github.com/GMyhf/cs101.openjudge.cn/actions/runs/39976668440)已通过。本轮仅补充collab复核记录。

平台参考解复验已完成；接入仍须设计保留原_made有效契约与针对性覆盖的合并方式；不能删valid()或把现有边界组替换掉。61题候选中，本批10题完成上述本地、只读核对及平台AC复验，另51题尚待同等复核；359题仍不是全部验收完成。
