# 交互判题EOF因果顺序修复

用户2026-10-23授权，任务T-055。完整证据见[interactive-eof-review.json](interactive-eof-review.json)。

旧逻辑靠poll()判断谁先退出，但交互器关闭stdout与进程退出之间存在间隔：
学生读到EOF后抛异常，交互器仍在等待学生stdout的EOF，此时旧逻辑会把WA或Judge Error误判为RE。
新回归夹具用双向EOF依赖确定性触发这个间隔，无需等待偶发调度或靠sleep碰运气；旧代码稳定失败两项。

修复后，双向_pump在关闭对端stdin前用同一把锁记录第一个EOF。
这样学生因读到EOF而崩溃，必定发生在交互器EOF记录之后；学生自身崩溃引起交互器EOF也有对应顺序。
poll()仅用于回收进程，不再用来决定谁应为异常负责。

| 情况 | 判定 |
| --- | --- |
| 学生先自行崩溃，交互器随后报提前结束 | RE |
| 交互器先结束输出并返回42，学生读EOF崩溃 | WA |
| 交互器先结束输出并异常返回，学生读EOF崩溃 | Judge Error |
| 交互器返回成功，但学生异常退出 | RE |

判题模块65项回归通过；针对EOF与延迟轮询的两项测试各重复50次，合计100项全过。
四种变异全部检出：漏记交互器EOF、漏记学生EOF、掩盖学生先崩溃、交互器成功掩盖学生异常。
完整`python3 tools/handoff.py --verify`退出码0，单元测试、语法、待返工、全库扫描全部通过；详细输出记在JSON的gate字段中。

AST对比确认_limits、_run、prepare_program和_pump完全未变；两个Popen调用参数也完全未变。
CPU限制、2MiB文件上限、768MiB内存、环境白名单、python3 -I与临时目录隔离均保留。
