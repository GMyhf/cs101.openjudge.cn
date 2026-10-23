# 未接入课题组数据：第15批复核

基线`443e40d4c`，详细逐文件哈希、原valid()定义、独立算法、自检、变异及平台回执见[gmyhf-pending-batch15-review.json](gmyhf-pending-batch15-review.json)。

本批50题、1672对数据；0题全部核对通过，50题保留疑点。管理员题面字段、后台文件清单及SHA256均已实时回读；本地用当前judge.py的原有限制执行自写参考，未向平台提交源码；自写源码随证据保存且不包含后台测试内容。未修改平台数据、未激活_GMyhf、未改变valid()或索引。

独立复算通过71个题面样例、5823组小域穷举/对拍，102种错误变异均被检出。

| 题号 | 标题 | 数据对数 | 独立方法 | 本地/时限余量 | 平台回执 |
| --- | --- | --- | --- | --- | --- |
| 30647 | 打家劫舍（力扣 M198） | 20 | 相邻互斥两状态DP | Accepted，最慢0.67% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/30647/) |
| 30659 | 最小覆盖子串（力扣 T76） | 20 | 计数缺口滑动窗口 | Accepted，最慢1.80% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/30659/) |
| 30660 | 每日温度（力扣 M739） | 20 | 严格升温单调栈 | Accepted，最慢0.73% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/30660/) |
| 30661 | 划分字母区间（力扣 M763） | 20 | 最后出现位置封闭分段 | Accepted，最慢0.57% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/30661/) |
| 30675 | 冗余连接（力扣 M684） | 20 | 并查集扫描唯一冗余边 | Accepted，最慢0.75% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/30675/) |
| 30686 | 标签验证器 | 20 | 标签栈及CDATA原样跳过 | Accepted，最慢0.77% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/30686/) |
| 30825 | 窗口特征提取 | 50 | 滑动频次和惰性最小堆 | Accepted，最慢5.58% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/30825/) |
| 30826 | 任务调度 | 50 | 拓扑最早开始和最长依赖路径 | Accepted，最慢7.95% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/30826/) |
| 30827 | 受限能量下的多点采样 | 50 | 层序能量与采样掩码BFS，同状态仅入队更高能量 | Wrong Answer | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/30827/) |
| 30828 | 回溯优先级库 | 50 | 持久栈和逐次有效操作前状态，undo自身也入历史 | Wrong Answer | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/30828/) |
| 30829 | 天赋树最大权能 | 50 | 树先序加跳过完整子树的精确K个选择DP | Accepted，最慢5.63% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/30829/) |
| 30854 | 最大城市巡游 | 32 | 迭代Kosaraju缩点和DAG最大权路径 | Accepted，最慢10.37% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/30854/) |
| 30870 | “山峰”特征提取 | 50 | 左右严格坡长合成 | Accepted，最慢2.15% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/30870/) |
| 30873 | 粒子能级跃迁 | 50 | 最小素因子分解及只向右的最短路DP | Accepted，最慢8.97% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/30873/) |
| 30875 | 平衡战力 | 50 | 按选中人数分组的双半子集和与二分 | Accepted，最慢44.95% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/30875/) |
| 30876 | 摆乱的图书 | 50 | 图书ID集合成员判断 | Accepted，最慢7.52% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/30876/) |
| 30877 | 平稳区间 | 50 | 双单调队列的最大合法左边界累计 | Accepted，最慢19.75% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/30877/) |
| 30916 | 猫猫写作业 | 50 | 二分第S个凸增量斜率并精确累计整数代价 | Accepted，最慢13.28% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/30916/) |
| 30946 | 智能传送带的路径数 | 32 | 区间前驱和DP | Accepted，最慢1.47% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/30946/) |
| 31181 | 测试题目 | 1 | 静态解码确认仅排版演示，不核定后台答案 | Not run | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31181/) |
| 31194 | 单词争夺战 | 40 | 字典树逆序极小极大，成词立即胜 | Accepted，最慢5.12% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31194/) |
| 31196 | 科技展的展牌筛选 | 24 | 带删除轮数的单调栈 | Accepted，最慢3.82% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31196/) |
| 31199 | 整除问题 | 30 | 精确整数模的最小补数 | Accepted，最慢1.10% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31199/) |
| 31232 | 验证身份证（暗黑版） | 50 | 至多11候选逐一校日期、地址首位及权重余数 | Accepted，最慢1.43% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31232/) |
| 31233 | 警察招募（暗黑版） | 50 | 按入伍顺序维护到期批次并消耗最早空闲 | Accepted，最慢1.77% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31233/) |
| 31243 | 每日温度 | 30 | 严格升温单调栈 | Accepted，最慢1.82% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31243/) |
| 31244 | 网络延迟时间 | 30 | 非负边Dijkstra最远最短路 | Runtime Error | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31244/) |
| 31245 | 和为K的子数组 | 30 | 前缀和频数 | Accepted，最慢1.05% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31245/) |
| 31246 | 课程表 | 30 | 拓扑入度消除 | Runtime Error | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31246/) |
| 31247 | 前K个高频元素 | 30 | 频次排序并独立校边界并列 | Accepted，最慢1.70% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31247/) |
| 31259 | 接雨水 | 30 | 左右最高水位双指针 | Accepted，最慢1.85% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31259/) |
| 31260 | 单词搜索 | 30 | 字典树剪枝及不重复格子DFS | Runtime Error | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31260/) |
| 31262 | 冗余连接 | 30 | 入度二冲突候选和并查集环联合判定 | Wrong Answer | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31262/) |
| 31269 | 赛马大会 | 35 | 双端速度贪心与牺牲最慢马 | Accepted，最慢2.90% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31269/) |
| 31271 | 售货机找零 | 34 | 固定面额从大到小整除找零 | Accepted，最慢1.05% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31271/) |
| 31272 | 树洞热词 | 30 | 全词频率降序、同频字典序 | Accepted，最慢6.53% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31272/) |
| 31273 | 讲座冲突 | 30 | 结束时间优先贪心，允许端点相接 | Accepted，最慢2.80% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31273/) |
| 31274 | 游戏日常 | 33 | 相邻互斥非负上界两状态DP | Accepted，最慢1.45% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31274/) |
| 31275 | 歌词接龙 | 30 | 已用片段掩码与可行末字母位集 | Accepted，最慢3.85% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31275/) |
| 31292 | 放气球 | 40 | 逐轮同时删除平方序号 | Accepted，最慢1.55% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31292/) |
| 31303 | 滑动窗口最大值 | 30 | 过期索引与单调最大队列 | Accepted，最慢1.60% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31303/) |
| 31381 | Special Judge 测试 | 1 | 排序自造答案，独立校字符多重集 | Wrong Answer | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31381/) |
| 31413 | 柱形图中的最大矩形 | 30 | 递增高度栈出栈时结算最大宽度 | Accepted，最慢1.92% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31413/) |
| 31414 | 分发饼干 | 30 | 升序最小胃口和可满足最小饼干匹配 | Accepted，最慢1.30% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31414/) |
| 31415 | 跳跃游戏 | 30 | 最远可达前缀贪心 | Wrong Answer | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31415/) |
| 31416 | 跳跃游戏2.0 | 30 | 分层可达区间给最少跳数 | Accepted，最慢0.83% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31416/) |
| 31417 | 省份数量 | 30 | 逐连通分量图搜索 | Accepted，最慢2.48% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31417/) |
| 31435 | 汇总区间 | 30 | 连续整数最大段分解 | Wrong Answer | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31435/) |
| 31436 | 腐烂的橘子 | 30 | 多源腐烂层次BFS | Accepted，最慢0.95% | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31436/) |
| 31437 | 城市天际线 | 30 | 按端点事件扫描的最高活跃楼堆 | Wrong Answer | [未提交 Not submitted · 无](https://cs101.openjudge.cn/practice/31437/) |

本批采用自写参考与输入契约；未调用其他题目的valid，也未修改既有valid。参考以authored_reference保存完整源码及SHA256；判题器与原有资源限制保持不变。

本批证据不能代表全部359题已完成答案验收。总进度见[gmyhf-pending-progress.json](gmyhf-pending-progress.json)；接入仍须保留原_made契约与针对性覆盖。


## 保留疑点

- 30647：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 30659：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 30660：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 30661：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 30675：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 30686：题面样例与规则独立复算不一致：[1, 2]；原始题面代码标签直接成为HTML元素，可见样例丢失标签，与true输出矛盾；不擅补造原始代码；保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 30825：2份窗口输入未满足题面完整取值范围；正式参考在这些额外输入下可运行不等于合法输入验收。具体违规类别见逐文件布尔项。；保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入；输入契约检查拒绝2对；完整题面补查发现2对输入异常：2.in 窗口参数、序列数量或范围；3.in 窗口参数、序列数量或范围；未核定答案（具体原因见JSON）：2.in,3.in。
- 30826：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 30827：6份合法输入的后台答案误把非补给站采样点也当作补给；不做能量支配剪枝的全状态BFS逐份复现当前题意答案，另一补能模型与这6份后台答案全部吻合。；保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入；独立答案不匹配：1.in,15.in,18.in,32.in,41.in,5.in；本地判题或时限余量未通过。
- 30828：45份后台答案不符合题面undo本身也可撤销的规则；50份都符合不记录undo、只连续撤销push/pop的传统模型。未用后台生成器行为改写当前题意。；保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入；独立答案不匹配：10.in,11.in,12.in,13.in,14.in,15.in,16.in,17.in,18.in,19.in,20.in,21.in,22.in,23.in,24.in,25.in,26.in,27.in,28.in,29.in,30.in,31.in,32.in,33.in,34.in,35.in,36.in,37.in,38.in,39.in,40.in,41.in,42.in,43.in,44.in,45.in,46.in,47.in,48.in,49.in,5.in,50.in,7.in,8.in,9.in；本地判题或时限余量未通过。
- 30829：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 30854：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 30870：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 30873：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 30875：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 30876：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 30877：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 30916：题面样例与规则独立复算不一致：[1]；全科满分的独立精确平方计价与样例6不符；保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 30946：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 31181：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入；未核定答案（具体原因见JSON）：0.in；本地判题或时限余量未通过。
- 31194：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 31196：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 31199：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 31232：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 31233：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 31243：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 31244：初始审核程序误拒绝省略外层括号的单行二维数组，已用安全literal_eval及单行归一化重新核对：全部输入契约及答案通过。初始RE保留，不能将审核器解析缺陷当作数据违规。；保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入；本地判题或时限余量未通过。
- 31245：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 31246：初始审核程序误拒绝省略外层括号的单行二维数组，已用安全literal_eval及单行归一化重新核对：全部输入契约及答案通过。初始RE保留，不能将审核器解析缺陷当作数据违规。；保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入；本地判题或时限余量未通过。
- 31247：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 31259：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 31260：初始审核程序误拒绝省略外层括号的单行二维数组，已用安全literal_eval及单行归一化重新核对：全部输入契约及答案通过。初始RE保留，不能将审核器解析缺陷当作数据违规。；保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入；本地判题或时限余量未通过。
- 31262：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入；本地判题或时限余量未通过。
- 31269：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 31271：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 31272：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 31273：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 31274：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 31275：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 31292：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 31303：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 31381：题面明确为Special Judge；后台.out不是输入字符的合法排列，不能当作唯一正确答案或直接认定SPJ判错。原生SPJ源码与协议未获取，后台占位输出不作答案证书验收；自写排列证书检查仍保留。；保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入；未核定答案（具体原因见JSON）：0.in；本地判题或时限余量未通过。
- 31413：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 31414：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 31415：30份后台用0/1表示是否可达，题面描述和样例使用true/false；映射后可达性全部吻合，保留输出格式冲突，不报成贪心算法错误。；保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入；未核定答案（具体原因见JSON）：1.in,10.in,11.in,12.in,13.in,14.in,15.in,16.in,17.in,18.in,19.in,2.in,20.in,21.in,22.in,23.in,24.in,25.in,26.in,27.in,28.in,29.in,3.in,30.in,4.in,5.in,6.in,7.in,8.in,9.in；本地判题或时限余量未通过。
- 31416：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 31417：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 31435：30份后台省略区间字符串列表最外层方括号，单区间解析成字符串、多区间为元组；归一化后区间分段全部吻合，保留样例与后台格式差异。；保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入；未核定答案（具体原因见JSON）：1.in,10.in,11.in,12.in,13.in,14.in,15.in,16.in,17.in,18.in,19.in,2.in,20.in,21.in,22.in,23.in,24.in,25.in,26.in,27.in,28.in,29.in,3.in,30.in,4.in,5.in,6.in,7.in,8.in,9.in；本地判题或时限余量未通过。
- 31436：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入。
- 31437：保留原接入边界：not_in_catalog；不把答案核对通过等同于可以直接接入；本地判题或时限余量未通过。

本批逐文件独立答案核对一致1557对，不一致51对，输入或题意异常而未核定64对。保留接入排除状态不是把答案一致记为答案失败。

本批题面只在管理员视角读取；以管理员全局题号和下载链接核对身份，不把practice不可见当作没有题意。未向平台提交源码。报告只保留各字段哈希、自写程序、审核结论与逐文件哈希，不发布管理员题面、后台输入输出或页面表单。原本缺失的公开题库映射保持原状；独立答案通过不等于可以直接接入。

30827有6份后台答案误把采样点当作补给；30828有45份后台答案未遵守undo自身可撤销。31415的0/1与true/false、31435列表外层括号差异另列格式条件核对，未混成算法错误。31244/31246/31260初始单行二维数组解析缺陷已补正，修正参考全部AC；31262/31437去除结构化输出空格后也全部AC。31381后台SPJ输出不是字符排列证书，保留原SPJ协议待核。31181静态解码后为排版导航演示，没有可执行输入输出任务，全部答案保留未核定；31303题面样例缺少窗口大小，不擅补造样例通过。31247对频率并列允许任一合法前K集合，但必须升序输出；31381独立检查后台答案和自写输出的字符多重集。两种证书检查均以删去后台侧校验的变异证明不会只验证自写输出。
