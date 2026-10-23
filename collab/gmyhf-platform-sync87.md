# 剩余87对课题组数据的平台同步

此前本地修正中的30281六对已随`842b253f7`对应修复同步，本轮完成另外19题87对。
87份输入、57份答案共144个文件已上传，30份答案与原件一致，无需重复上传。
19题原有778个文件先备份、后完整回读；其中740份输入输出与审核来源清单一致，38份附件保留。
所有非目标数据、附件、文件名、题面、语言与时空限制等配置均未改变。

逐文件修正前后哈希、全部文件与配置校验、平台提交回执见[gmyhf-platform-sync87.json](gmyhf-platform-sync87.json)。
原始字节继续使用[既有修正清单](gmyhf-input-repairs.json)约束；未经审核的上游变化会停止同步。

## 验证

`python3 -m unittest tests.test_gmyhf_input_repairs`四项回归通过，覆盖全部93对的独立答案、输入合法性、来源和重抓保护。
本轮没有修改代码和本地题目数据；19题参考解源码与既有审核哈希一致，并全部在更新后的平台以Python3获Accepted。
上一轮修复已提交`842b253f7`并推送到`origin/main`，[CI gate成功](https://github.com/GMyhf/cs101.openjudge.cn/actions/runs/39971210117)。

| 题号 | 同步对数 | 平台Accepted提交 |
| --- | ---: | --- |
| 18109 | 2 | [53581622](http://cs101.openjudge.cn/practice/solution/53581622/) |
| 18223 | 20 | [53581623](http://cs101.openjudge.cn/practice/solution/53581623/) |
| 20074 | 3 | [53581624](http://cs101.openjudge.cn/practice/solution/53581624/) |
| 20089 | 1 | [53581625](http://cs101.openjudge.cn/practice/solution/53581625/) |
| 20136 | 2 | [53581626](http://cs101.openjudge.cn/practice/solution/53581626/) |
| 20162 | 1 | [53581627](http://cs101.openjudge.cn/practice/solution/53581627/) |
| 21458 | 17 | [53581628](http://cs101.openjudge.cn/practice/solution/53581628/) |
| 21532 | 1 | [53581629](http://cs101.openjudge.cn/practice/solution/53581629/) |
| 25301 | 1 | [53581631](http://cs101.openjudge.cn/practice/solution/53581631/) |
| 26971 | 1 | [53581632](http://cs101.openjudge.cn/practice/solution/53581632/) |
| 26976 | 1 | [53581633](http://cs101.openjudge.cn/practice/solution/53581633/) |
| 27373 | 1 | [53581634](http://cs101.openjudge.cn/practice/solution/53581634/) |
| 27862 | 1 | [53581635](http://cs101.openjudge.cn/practice/solution/53581635/) |
| 28012 | 1 | [53581636](http://cs101.openjudge.cn/practice/solution/53581636/) |
| 28193 | 12 | [53581637](http://cs101.openjudge.cn/practice/solution/53581637/) |
| 28664 | 1 | [53581638](http://cs101.openjudge.cn/practice/solution/53581638/) |
| 29256 | 19 | [53581640](http://cs101.openjudge.cn/practice/solution/53581640/) |
| 29740 | 1 | [53581641](http://cs101.openjudge.cn/practice/solution/53581641/) |
| 30942 | 1 | [53581642](http://cs101.openjudge.cn/practice/solution/53581642/) |
