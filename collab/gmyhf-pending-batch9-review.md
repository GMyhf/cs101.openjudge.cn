# 未接入课题组数据：第9批复核

基线`edba174f9`，详细逐文件哈希、原valid()定义、独立算法、自检、变异及平台回执见[gmyhf-pending-batch9-review.json](gmyhf-pending-batch9-review.json)。

本批20题、540对数据；0题全部核对通过，20题保留疑点。管理员题面字段、后台文件清单及SHA256均已实时回读；本地用当前judge.py的原有限制执行自写参考，未向平台提交源码；自写源码随证据保存且不包含后台测试内容。未修改平台数据、未激活_GMyhf、未改变valid()或索引。

独立复算通过40个题面样例、1133组小域穷举/对拍，40种错误变异均被检出。

| 题号 | 标题 | 数据对数 | 独立方法 | 本地/时限余量 | 平台回执 |
| --- | --- | --- | --- | --- | --- |
| 18208 | 两种矩阵乘法 | 20 | 有理数矩阵乘法与max-min乘法、精确四舍五入 | Accepted，最慢1.55% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/18208/) |
| 18210 | 跳远 | 30 | 分层可达前缀闭包 | Accepted，最慢1.20% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/18210/) |
| 18221 | 字符串加密 | 10 | 逐字符循环移位与逆序词序 | Accepted，最慢1.15% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/18221/) |
| 21433 | 仲夏夜 (implementation) | 20 | 任意精度累乘的十进制位数 | Accepted，最慢22.00% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/21433/) |
| 21457 | 棋室 (matrices) | 20 | 逐空位四方向连续白子计数 | Accepted，最慢1.23% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/21457/) |
| 21470 | 吃水果 (greedy, math) | 100 | 最大频次冷却调度下界 | Accepted，最慢1.12% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/21470/) |
| 21471 | Self-Attention (matrices) | 38 | 先算Gram矩阵再乘原矩阵 | Accepted，最慢1.35% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/21471/) |
| 21472 | 礼物盒 (dp) | 90 | 等长逆序排序加严格LIS | Accepted，最慢1.38% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/21472/) |
| 21533 | 双十一的麻烦 (data structures) | 20 | 出入集合差与单链完整性 | Accepted，最慢0.97% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/21533/) |
| 21534 | 胆小的维恩 | 20 | 最小最大边权Dijkstra | Accepted，最慢1.35% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/21534/) |
| 21552 | 多维数组中元素的位置 (implementation) | 20 | 混合进位行优先地址 | Accepted，最慢1.12% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/21552/) |
| 21555 | 分平安果 (dp) | 20 | 整数拆分最优2和3分解 | Accepted，最慢0.95% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/21555/) |
| 21726 | 赛博朋克 (math) | 20 | 精确幂与战力总和比较 | Accepted，最慢1.15% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/21726/) |
| 23557 | 人工智能？ | 10 | 多重解释表排序及独立轮询计数 | Accepted，最慢0.97% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/23557/) |
| 23561 | 探测地形 | 20 | 局部极小单元连通分量 | Accepted，最慢1.32% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/23561/) |
| 23567 | 共同富裕 | 10 | 固定首行后的全部循环位移搜索 | Accepted，最慢1.07% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/23567/) |
| 25564 | Gamma 编码 | 21 | 二进制位宽一元前缀 | Accepted，最慢1.23% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/25564/) |
| 25574 | 生日排序 | 20 | 忽略同生日的正反序逆序对 | Accepted，最慢1.07% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/25574/) |
| 27308 | 粉刷栅栏 | 20 | 双区间并集长度 | Accepted，最慢1.18% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/27308/) |
| 27309 | MOO操作 | 11 | 枚举保留三字子串及端点修改 | Accepted，最慢0.97% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/27309/) |

本批采用自写参考与输入契约；未调用其他题目的valid，也未修改既有valid。参考以authored_reference保存完整源码及SHA256；判题器与原有资源限制保持不变。

本批证据不能代表全部359题已完成答案验收。总进度见[gmyhf-pending-progress.json](gmyhf-pending-progress.json)；接入仍须保留原_made契约与针对性覆盖。


## 保留疑点

- 18208：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 18210：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 18221：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 21433：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 21457：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 21470：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 21471：19对矩阵阶数超过题面n≤20，元素数量与声明阶数一致；明确属于尺寸上限违规；保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入；输入契约检查拒绝19对；完整题面补查发现19对输入异常：19.in 矩阵尺寸；20.in 矩阵尺寸；21.in 矩阵尺寸；22.in 矩阵尺寸；23.in 矩阵尺寸；24.in 矩阵尺寸；25.in 矩阵尺寸；26.in 矩阵尺寸；未核定答案（输入已超出题面定义）：19.in,20.in,21.in,22.in,23.in,24.in,25.in,26.in,27.in,28.in,29.in,30.in,31.in,32.in,33.in,34.in,35.in,36.in,37.in。
- 21472：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 21533：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 21534：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 21552：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 21555：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 21726：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 23557：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 23561：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 23567：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 25564：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 25574：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 27308：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 27309：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。

本批逐文件独立答案核对一致521对，不一致0对，输入异常而未核定19对。保留接入排除状态不是把答案一致记为答案失败。

本批题面只在管理员视角读取；以管理员全局题号和下载链接核对身份，不把practice不可见当作没有题意。未向平台提交源码。报告只保留各字段哈希、自写程序、审核结论与逐文件哈希，不发布管理员题面、后台输入输出或页面表单。原本缺失的公开题库映射保持原状；独立答案通过不等于可以直接接入。
