# 未接入课题组数据：第8批复核

基线`8b365cf92`，详细逐文件哈希、原valid()定义、独立算法、自检、变异及平台回执见[gmyhf-pending-batch8-review.json](gmyhf-pending-batch8-review.json)。

本批11题、156对数据；0题全部核对通过，11题保留疑点。题面字段、后台文件清单及SHA256均已实时回读；本地用当前judge.py的原有限制复判，平台只提交已有公开参考或本次自写独立算法程序；自写源码随证据保存且不包含后台测试内容。未修改平台数据、未激活_GMyhf、未改变valid()或索引。

独立复算通过18个题面样例、2317组小域穷举/对拍，24种错误变异均被检出。

| 题号 | 标题 | 数据对数 | 独立方法 | 本地/时限余量 | 平台回执 |
| --- | --- | --- | --- | --- | --- |
| 19965 | 海贼王路飞v0.2 | 11 | 按每轮最小饱腹肉块数模拟战力跃迁 | Accepted，最慢0.39% | [Python3 Accepted · 53582467](http://cs101.openjudge.cn/practice/solution/53582467/) |
| 19967 | 数组增删改查 | 10 | 动态数组执行操作，与独立整数键模型对拍 | Accepted，最慢0.32% | [Python3 Accepted · 53582468](http://cs101.openjudge.cn/practice/solution/53582468/) |
| 19971 | 组合数 | 5 | 标准库精确整数组合数 | Output Limit Exceeded | [Python3 Accepted · 53582487](http://cs101.openjudge.cn/practice/solution/53582487/) |
| 19974 | 看电影 | 2 | 反射原理组合计数，与格点DP对拍 | Wrong Answer | [Python3 Wrong Answer · 53582472](http://cs101.openjudge.cn/practice/solution/53582472/) |
| 19984 | 合成路线 | 15 | 精确有理数比较每阶段成本，整数余数实现五成双 | Wrong Answer | [Python3 Wrong Answer · 53582474](http://cs101.openjudge.cn/practice/solution/53582474/) |
| 19998 | 教科书般的亵渎 | 20 | 逐次扣血模拟自动重放，与生命值缺口计数对拍 | Accepted，最慢0.34% | [Python3 Accepted · 53582475](http://cs101.openjudge.cn/practice/solution/53582475/) |
| 27699 | Wide Swap | 10 | 逆排列不可交换次序的DAG，以最大位置汇点逆向编号 | Time Limit Exceeded | [Python3 Presentation Error · 53582477](http://cs101.openjudge.cn/practice/solution/53582477/) |
| 30193 | 哈密顿激活层 | 5 | 原SPJ占位符分类；构造实际路径后独立逐格验证覆盖、邻接与时序锁 | Accepted，最慢0.31% | [Python3 Accepted · 53582479](http://cs101.openjudge.cn/practice/solution/53582479/) |
| 30547 | LLM 递推生成卡片 | 52 | 精确递推前10项、首项排名区间及直接前缀累计排名；任意精度整数比较有限足够长后缀 | Accepted，最慢22.73% | [G++ Accepted · 53582486](http://cs101.openjudge.cn/practice/solution/53582486/) |
| 30497 | 无限回廊的瓷砖 | 25 | 直接核公开输出语法及已公开固定undecidable参考，不声称解决一般铺砖问题 | Accepted，最慢0.22% | [Python3 Accepted · 53582480](http://cs101.openjudge.cn/practice/solution/53582480/) |
| 31428 | 两数之和 | 1 | Counter计数证明唯一数对，并独立核索引、和值与既有100组封装 | Accepted，最慢2.03% | [Python3 Accepted · 53582481](http://cs101.openjudge.cn/practice/solution/53582481/) |

已有valid()完整保留；没有既有参考的题按独立复算器extra_contract核题面。已有公开参考的提交与origin/main字节一致；本次自写参考以authored_reference保存完整源码及SHA256。未改变判题器或资源限制。

本批证据不能代表全部359题已完成答案验收。总进度见[gmyhf-pending-progress.json](gmyhf-pending-progress.json)；接入仍须保留原_made契约与针对性覆盖。


## 保留疑点

- 19965：保留原接入边界：no_bucket；不把答案核对通过等同于可以直接接入；输入契约检查拒绝5对；尚须区分排版/生成器额外约束/题面违规；完整题面补查发现5对输入异常：10.in 容量战力肉块数范围不符；11.in 容量战力肉块数范围不符；6.in 容量战力肉块数范围不符；7.in 容量战力肉块数范围不符；8.in 容量战力肉块数范围不符；未核定答案（输入已超出题面定义）：10.in,11.in,6.in,7.in,8.in。
- 19967：保留原接入边界：no_bucket；不把答案核对通过等同于可以直接接入。
- 19971：保留原接入边界：no_bucket；不把答案核对通过等同于可以直接接入；本地判题或时限余量未通过。
- 19974：保留原接入边界：no_bucket；不把答案核对通过等同于可以直接接入；输入契约检查拒绝2对；尚须区分排版/生成器额外约束/题面违规；完整题面补查发现2对输入异常：1.in 组数或终点正数约束不符；2.in 组数或终点正数约束不符；未核定答案（输入已超出题面定义）：1.in,2.in；本地判题或时限余量未通过；平台复判为Wrong Answer。
- 19984：保留原接入边界：no_bucket；不把答案核对通过等同于可以直接接入；输入契约检查拒绝1对；尚须区分排版/生成器额外约束/题面违规；完整题面补查发现1对输入异常：4.in 产物级数或概率范围不符；未核定答案（输入已超出题面定义）：4.in；本地判题或时限余量未通过；平台复判为Wrong Answer。
- 19998：保留原接入边界：no_bucket；不把答案核对通过等同于可以直接接入。
- 27699：保留原接入边界：output_over_2MiB；不把答案核对通过等同于可以直接接入；输入契约检查拒绝5对；尚须区分排版/生成器额外约束/题面违规；完整题面补查发现5对输入异常：0.in 不是合法N,K及排列；13.in 不是合法N,K及排列；19.in 不是合法N,K及排列；2.in 不是合法N,K及排列；8.in 不是合法N,K及排列；未核定答案（输入已超出题面定义）：0.in,13.in,19.in,2.in,8.in；本地判题或时限余量未通过；平台复判为Presentation Error。
- 30193：保留原接入边界：special_judge；不把答案核对通过等同于可以直接接入；输入契约检查拒绝5对；尚须区分排版/生成器额外约束/题面违规；后台输出是SPJ占位符，必须保留专用检查器。
- 30547：保留原接入边界：contract_protected；不把答案核对通过等同于可以直接接入。
- 30497：保留原接入边界：contract_protected；不把答案核对通过等同于可以直接接入；输入契约检查拒绝25对；尚须区分排版/生成器额外约束/题面违规；独立答案不匹配：0.in,1.in,10.in,11.in,12.in,13.in,14.in,15.in,16.in,17.in,18.in,19.in,2.in,20.in,21.in,22.in,23.in,24.in,3.in,4.in,5.in,6.in,7.in,8.in,9.in。
- 31428：保留原接入边界：manual_exclusion；不把答案核对通过等同于可以直接接入；题面字段变化：输入。

30193原输出为SPJ占位0，不能按普通答案接入；另构造真实路径并独立核每步的邻接、覆盖与锁定时间，不发布后台路径内容。30547既有参考为C++，完整排名另以直接累计前缀约束计数及精确整数后缀比较复核，并非只校前10项；审核加速程序自带非负任意精度整数，202组大整数算术及180张卡片穷举均通过，另有3种原生错误变异。19971初始math.comb参考Python3超时、旧PyPy运行错误；按b分组的Pascal精确整数程序与全部下载答案一致后另附平台回执，原本地大输出失败记录保留。31428保持原函数模板、前缀和后缀，只提交自写two_sum函数。30497按公开YES/NO语法检查；非常规固定undecidable输出保留疑点，不擅改成无依据的YES/NO。
