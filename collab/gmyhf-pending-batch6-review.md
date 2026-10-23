# 未接入课题组数据：第6批复核

基线`9f3164145`，详细逐文件哈希、原valid()定义、独立算法、自检、变异及平台回执见[gmyhf-pending-batch6-review.json](gmyhf-pending-batch6-review.json)。

本批20题、908对数据；1题全部核对通过，19题保留疑点。题面字段、后台文件清单及SHA256均已实时回读；本地用当前judge.py的原有限制复判，平台提交现有公开参考源码；若需拆分多题分派器，另附单题分支提取及逐文件等价证明。未修改平台数据、未激活_GMyhf、未改变valid()或索引。

独立复算通过27个题面样例、1905组小域穷举/对拍，23种错误变异均被检出。

| 题号 | 标题 | 数据对数 | 独立方法 | 本地/时限余量 | 平台回执 |
| --- | --- | --- | --- | --- | --- |
| 25274 | 赋值、浅拷贝与深拷贝 | 1 | 显式对象编号图模拟引用共享 | Accepted，最慢0.15% | [Python3 Accepted · 53582411](http://cs101.openjudge.cn/practice/solution/53582411/) |
| 27307 | 大佬相助 | 20 | 带后缀剪枝的覆盖量记忆化搜索 | Accepted，最慢1.13% | [Python3 Accepted · 53582412](http://cs101.openjudge.cn/practice/solution/53582412/) |
| 27318 | k个逆序对数组 | 20 | 生成函数对数导数系数递推 | Accepted，最慢5.34% | [Python3 Accepted · 53582413](http://cs101.openjudge.cn/practice/solution/53582413/) |
| 28013 | 堆路径 | 20 | 枚举叶子回溯父节点并排序路径分支码 | Accepted，最慢0.29% | [Python3 Accepted · 53582414](http://cs101.openjudge.cn/practice/solution/53582414/) |
| 28336 | 消消乐 | 20 | 双向链表删除与邻接事件队列 | Accepted，最慢0.19% | [Python3 Accepted · 53582415](http://cs101.openjudge.cn/practice/solution/53582415/) |
| 28701 | 炸鸡排 | 100 | 整数刻度二分工作量后恢复精确分数 | Accepted，最慢0.20% | [Python3 Accepted · 53582416](http://cs101.openjudge.cn/practice/solution/53582416/) |
| 28906 | 数的划分 | 20 | 按含1与全体减1的整数划分递推 | Accepted，最慢0.55% | [Python3 Accepted · 53582417](http://cs101.openjudge.cn/practice/solution/53582417/) |
| 28908 | PASCAL代码 | 20 | 正则词法扫描依序覆盖赋值 | Accepted，最慢0.19% | [Python3 Accepted · 53582418](http://cs101.openjudge.cn/practice/solution/53582418/) |
| 28969 | 解密 | 100 | 显式区间栈恢复中轴字符位置 | Accepted，最慢0.85% | [Python3 Accepted · 53582419](http://cs101.openjudge.cn/practice/solution/53582419/) |
| 28970 | 预测赢家 | 100 | 一维区间博弈差值递推 | Accepted，最慢0.47% | [Python3 Accepted · 53582420](http://cs101.openjudge.cn/practice/solution/53582420/) |
| 28972 | 海拔 | 100 | 最小化最大边权的Dijkstra | Accepted，最慢2.60% | [Python3 Accepted · 53582423](http://cs101.openjudge.cn/practice/solution/53582423/) |
| 28973 | 蛇入迷宫 | 100 | 显式二格状态图分层搜索 | Accepted，最慢0.64% | [Python3 Accepted · 53582424](http://cs101.openjudge.cn/practice/solution/53582424/) |
| 29895 | 分解因数 | 20 | 完整试除质因子分解取最小因子商 | Accepted，最慢0.17% | [Python3 Accepted · 53582425](http://cs101.openjudge.cn/practice/solution/53582425/) |
| 30172 | 嘎啦给木里不是这样的 | 26 | 全图三色DFS与逆拓扑最优路径 | Accepted，最慢2.25% | [Python3 Accepted · 53582426](http://cs101.openjudge.cn/practice/solution/53582426/) |
| 30222 | 量子芯片研发 | 50 | 依赖图显式DFS计算完成时间 | Accepted，最慢0.31% | [Python3 Accepted · 53582428](http://cs101.openjudge.cn/practice/solution/53582428/) |
| 30646 | 缺失的第一个正数 | 20 | 原地置换定位缺失正数 | Accepted，最慢0.47% | [Python3 Accepted · 53582429](http://cs101.openjudge.cn/practice/solution/53582429/) |
| 30874 | 匹配队友 | 50 | 按职责出现次数直接确定组号 | Accepted，最慢0.81% | [Python3 Accepted · 53582430](http://cs101.openjudge.cn/practice/solution/53582430/) |
| 30878 | 力场叠加模拟 | 50 | 独立平方根分块与懒增量；大数据复算编译同算法C++，源码随证据保存；正式本地/平台仍用原Python参考 | Accepted，最慢37.23% | [Python3 Accepted · 53582437](http://cs101.openjudge.cn/practice/solution/53582437/) |
| 30930 | 猫猫水群聊 | 50 | 截断频数反向累加求h因子 | Accepted，最慢7.15% | [Python3 Accepted · 53582439](http://cs101.openjudge.cn/practice/solution/53582439/) |
| 31193 | 倒排文档 | 21 | 文档倒排映射和词频序列选择 | Accepted，最慢0.16% | [Python3 Accepted · 53582441](http://cs101.openjudge.cn/practice/solution/53582441/) |

原valid()完整保留；后台包含sample0.in等名称，驱动只将文件遍历排序从数字改为文件名，没有修改校验逻辑。平台原始提交与公开origin/main源码哈希一致；若存在platform_specialization，则保留原始回执、提取源码哈希与逐文件输出等价证明。

本批证据不能代表全部359题已完成答案验收。总进度见[gmyhf-pending-progress.json](gmyhf-pending-progress.json)；接入仍须保留原_made契约与针对性覆盖。


## 保留疑点

- 27307：原valid拒绝6对；尚须区分排版/生成器额外约束/题面违规。
- 27318：原valid拒绝20对；尚须区分排版/生成器额外约束/题面违规。
- 28013：原valid拒绝20对；尚须区分排版/生成器额外约束/题面违规。
- 28336：原valid拒绝20对；尚须区分排版/生成器额外约束/题面违规。
- 28701：原valid拒绝100对；尚须区分排版/生成器额外约束/题面违规。
- 28906：原valid拒绝20对；尚须区分排版/生成器额外约束/题面违规。
- 28908：原valid拒绝20对；尚须区分排版/生成器额外约束/题面违规。
- 28969：原valid拒绝100对；尚须区分排版/生成器额外约束/题面违规。
- 28970：原valid拒绝100对；尚须区分排版/生成器额外约束/题面违规。
- 28972：原valid拒绝100对；尚须区分排版/生成器额外约束/题面违规。
- 28973：原valid拒绝100对；尚须区分排版/生成器额外约束/题面违规。
- 29895：原valid拒绝20对；尚须区分排版/生成器额外约束/题面违规。
- 30172：原valid拒绝8对；尚须区分排版/生成器额外约束/题面违规。
- 30222：原valid拒绝5对；尚须区分排版/生成器额外约束/题面违规；声明边数少于实际边数，按声明截断则与后台答案一致、读取全部边则不一致：46.in,47.in,48.in,49.in,50.in。
- 30646：原valid拒绝20对；尚须区分排版/生成器额外约束/题面违规。
- 30874：原valid拒绝50对；尚须区分排版/生成器额外约束/题面违规。
- 30878：原valid拒绝50对；尚须区分排版/生成器额外约束/题面违规。
- 30930：原valid拒绝1对；尚须区分排版/生成器额外约束/题面违规。
- 31193：原valid拒绝18对；尚须区分排版/生成器额外约束/题面违规；未核定答案（输入已超出题面定义）：10.in,11.in,12.in,13.in,14.in,15.in,16.in,17.in,18.in,19.in,2.in,20.in,3.in,5.in,6.in,7.in,8.in,9.in。

原valid拒绝时，另用逐行规范空白的文本调用原函数并跟踪False返回位置；两次结果及原始代码行均在contract_diagnostic。规范空白后通过只说明排版差异，未修改原始输入、valid或接入状态；仍拒绝的条目须按具体题面继续区分数值范围、结构约束与生成器额外约束。

30222有5对输入各多出1条未计入M的边；按声明M截断与后台答案一致，读取全部边则不同，属于原valid已拒绝的结构违规，不计作合法输入下算法错误。JSON的edge_count_resolution含逐文件证明及自造最小反例。30878独立分块审核程序以g++ -O2 -std=c++17编译加速，C++源码在独立复算器的CPP_ORACLE_SOURCE；与100组小数组直接模拟核对通过，另检出2种原生错误变异。正式本地和平台仍使用原Python参考与原资源限制。31193有18对输入的频次排名超出词表，题面未定义答案；保持原valid拒绝并将matches记为null，不以参考解兜底0代作正确答案。
