# 论文投稿前的关键路径

私有题号 `1000003`，2026-11-08 由用户要求以“写论文的任务依赖”为场景出题（AOE 网关键路径，含判环）。
样例的 8 项任务取自当时真实的研究流程：下载模型、写判定标准、生成数据、稳健性检验、语义多样性分析、
调用前沿模型 API、写论文、第二轮审稿。

题面约束：1 ≤ n ≤ 10000，0 ≤ m ≤ 50000，1 ≤ tᵢ ≤ 1000，u ≠ v，同一对 (u, v) 最多一次；
有环输出 `-1`，否则输出总工期和全部关键任务（ESᵢ = LSᵢ，按编号升序）。总时间限制 2000ms，内存 65536kB。

- `samplecode.py`：Kahn 拓扑排序求最早开始时间，逆拓扑序求最迟开始时间（仓库交接件，Claude 编写）。
- `producecase.py`：答案由 `oracle()` 用迭代 DFS 判环并求最长路，算法与参考实现不同；第 0 组是题面样例，
  `build()` 逐字断言；`valid()` 照题面写输入契约；固定种子 1000003。
- 测试 `tests/test_private_1000003.py` 另有第三个独立依据：对 n ≤ 60 的数据按定义逐个把任务推迟 1 小时，
  看总工期是否变长。

21 组数据：样例；单任务；无依赖（长者关键 / 全部并列）；4 组带环（2 环、大图中 500 环、孤立分量里的环、
随机图加回边）；10000 个任务的深链（卡递归）；两支等长的菱形；40×40 网格（大量等长路径）；
孤立任务加长链；并列最长汇点的星形；最大规模随机 DAG（耗时随机 / 全 1 / 全 1000）；逆拓扑序给边；
两个大分量。

验证记录见 `collab/private-1000003-review.json`：参考实现与 C++ 正解本地判题 Accepted；五种错解全部被判错，
逐组统计：用后继最早开始算最迟完成时间挂 8 组，不判环挂 4 组，按编号顺序递推挂 9 组，
只找一条关键路径挂 6 组，递归 DFS 在深链上 Runtime Error。

重建数据：

```bash
python3 data/openjudge/tests/private/1000003_made/producecase.py
python3 tools/activate_private_problems.py private 1000003
python3 scripts/index_tests.py && python3 scripts/extract_problem_limits.py && python3 scripts/build_input_domains.py
```
