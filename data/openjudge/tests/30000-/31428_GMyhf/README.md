# 31428 两数之和

课题组自出题，用户于 2026-10-18 明确授权直接使用官方测试数据。
后台 `/admin/problems/` 显示编辑入口 `/admin/problems/edit/?id=31428`，作者 FuYn。
题面：<http://cs101.openjudge.cn/practice/31428/>。

- `data/0.in`、`data/0.out` 是后台下载的原始文件，未修改字节；SHA-256 与体积见 `manifest.json`。
- 一对文件包含 100 个子样例，每个输入为 `length target`、一行数组，以 `0 0` 结束；输出每个子样例的两个升序下标。
- `verify.py` 校验原始哈希、全部输入约束、唯一解和期望答案；数组长度覆盖 2 到 9960。
- `preset_code.py`、`preset_suffix.py` 原样保留上游的 Python/C++ 共用预设代码，学生仅提交 `two_sum` / `twoSum` 函数。
- `preset_languages.json` 指定 Python 3、PyPy3、C++；其他语言不使用这份预设代码。
- `samples.json` 仅含题面公开的三个样例，供“运行样例”使用，不向页面下发完整判题输入。
- `samplecode.py`、`samplecode.cpp` 是本项目的哈希表参考实现；C++ 故意返回逆序下标，验证上游预设代码会按题意排序。
- 官方文件以一个进程批量测试 100 个子样例，按 1 组原始文件登记到 `collab/tests-below-20.json`；不拆文件或生成额外数据。

运行 `python3 data/openjudge/tests/30000-/31428_GMyhf/verify.py` 校验数据。

2026-10-18 接入验证：官方 100 个子样例约束、唯一解和答案全部通过；Python 3、PyPy3、C++ 参考函数均 Accepted；新增题及预设代码、沙箱兼容性的 28 项针对性测试通过。线上题面、提交页和最近新增接口返回正常。完整单元测试 377 项中 376 项通过，唯一失败为既有 31270、31421 少于 20 组且未登记；语法检查通过。额外 full_sweep 在既有 04091 输入契约上长时间运行后停止，未报告全库检查通过。
