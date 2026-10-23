# 未接入课题组数据：第7批复核

基线`98f36523a`，详细逐文件哈希、原valid()定义、独立算法、自检、变异及平台回执见[gmyhf-pending-batch7-review.json](gmyhf-pending-batch7-review.json)。

本批11题、249对数据；0题全部核对通过，11题保留疑点。题面字段、后台文件清单及SHA256均已实时回读；本地用当前judge.py的原有限制复判，平台提交现有公开参考源码；若需拆分多题分派器，另附单题分支提取及逐文件等价证明。未修改平台数据、未激活_GMyhf、未改变valid()或索引。

独立复算通过17个题面样例、1101组小域穷举/对拍，12种错误变异均被检出。

| 题号 | 标题 | 数据对数 | 独立方法 | 本地/时限余量 | 平台回执 |
| --- | --- | --- | --- | --- | --- |
| 18159 | 个位为 1 的质数个数 | 6 | 埃氏筛个位1质数及批次输出 | Output Limit Exceeded | [Python3 Accepted · 53582444](http://cs101.openjudge.cn/practice/solution/53582444/) |
| 27150 | Divisibility by Eight 加强版 | 20 | 子序列模8自动机与证书验证 | Accepted，最慢0.18% | [Python3 Accepted · 53582446](http://cs101.openjudge.cn/practice/solution/53582446/) |
| 28190 | 奶牛排队 | 25 | 下一不大于边界加区间最早最大值查询 | Accepted，最慢47.00% | [Python3 Accepted · 53582448](http://cs101.openjudge.cn/practice/solution/53582448/) |
| 28203 | 【模板】单调栈 | 20 | 逆向后继跳跃求首个更大元素 | Output Limit Exceeded | [Python3 Accepted · 53582449](http://cs101.openjudge.cn/practice/solution/53582449/) |
| 30179 | 数字华容道（Hard Version） | 10 | 完整棋盘置换交换奇偶与空格曼哈顿不变量 | Accepted，最慢40.04% | [Python3 Accepted · 53582450](http://cs101.openjudge.cn/practice/solution/53582450/) |
| 30550 | 勾股数 | 10 | Berggren三叉树生成本原三元组及倍数 | Output Limit Exceeded | [Python3 Accepted · 53582451](http://cs101.openjudge.cn/practice/solution/53582451/) |
| 30720 | 败方树的构建与维护 | 21 | 按完全二叉树堆编号及叶子从左到右位置，自底向上完全重算 | Output Limit Exceeded | [Python3 Accepted · 53582452](http://cs101.openjudge.cn/practice/solution/53582452/) |
| 30908 | 力场叠加模拟 (在线版) | 31 | 分段常数隐式Treap在线区间操作 | Accepted，最慢20.93% | [Python3 Accepted · 53582453](http://cs101.openjudge.cn/practice/solution/53582453/) |
| 30921 | 猫猫搭积木 | 52 | 虚拟合并节点与失效根懒拆分 | Output Limit Exceeded | [Python3 Accepted · 53582456](http://cs101.openjudge.cn/practice/solution/53582456/) |
| 30937 | 01最小生成树 (new data) | 33 | 补图连通分量数减一 | Accepted，最慢41.94% | [Python3 Accepted · 53582457](http://cs101.openjudge.cn/practice/solution/53582457/) |
| 31454 | 第一个 AA 型子串 | 21 | 倒序精确LCP判相邻同长块 | Accepted，最慢0.63% | [G++ Accepted · 53582458](http://cs101.openjudge.cn/practice/solution/53582458/) |

原valid()完整保留；后台包含sample0.in等名称，驱动只将文件遍历排序从数字改为文件名，没有修改校验逻辑。平台原始提交与公开origin/main源码哈希一致；若存在platform_specialization，则保留原始回执、提取源码哈希与逐文件输出等价证明。

本批证据不能代表全部359题已完成答案验收。总进度见[gmyhf-pending-progress.json](gmyhf-pending-progress.json)；接入仍须保留原_made契约与针对性覆盖。


## 保留疑点

- 18159：保留原接入边界：output_over_2MiB；不把答案核对通过等同于可以直接接入；本地判题或时限余量未通过。
- 27150：保留原接入边界：special_judge；不把答案核对通过等同于可以直接接入；原valid拒绝20对；尚须区分排版/生成器额外约束/题面违规。
- 28190：题面明确答案不会为1，严格递减的两头牛没有合法区间；保留原接入边界：runtime_margin；不把答案核对通过等同于可以直接接入。
- 28203：保留原接入边界：output_over_2MiB；不把答案核对通过等同于可以直接接入；本地判题或时限余量未通过。
- 30179：保留原接入边界：runtime_margin；不把答案核对通过等同于可以直接接入。
- 30550：保留原接入边界：output_over_2MiB；不把答案核对通过等同于可以直接接入；本地判题或时限余量未通过。
- 30720：按题面完全二叉树及叶子从左到右排列，FIFO合并叶子在非2幂时生成不同树形；保留原接入边界：output_over_2MiB；不把答案核对通过等同于可以直接接入；本地判题或时限余量未通过。
- 30908：保留原接入边界：runtime_margin；不把答案核对通过等同于可以直接接入；原valid拒绝28对；尚须区分排版/生成器额外约束/题面违规。
- 30921：保留原接入边界：output_over_2MiB；不把答案核对通过等同于可以直接接入；本地判题或时限余量未通过。
- 30937：保留原接入边界：runtime_margin；不把答案核对通过等同于可以直接接入。
- 31454：保留原接入边界：manual_exclusion；不把答案核对通过等同于可以直接接入；题面字段变化：描述。

本批为专用判题、资源边界及人工排除题，全部保留原接入排除状态；答案文件是否正确另见answers.files，不能将保留排除误记为答案失败。27150同时验证独立构造和后台输出各自为合法证书，不要求两份YES答案字符串相同。原checker完整保留；超过2MiB的输出不放宽沙箱，仍记录真实本地判题结果。31454使用仓库已有C++参考与G++平台复判。28190自造合法递减反例的正确答案0、原参考输出1；30720自造5叶子反例下完全二叉树与原FIFO合并树不同。两个反例仅用自造输入复现并保留，不发布后台内容。30921审核复算器对失效根仍压缩整条父链；自造120元素链式操作以父指针遍历次数证明不会逐个查询退化为平方复杂度，删除压缩的变异会被检出。
