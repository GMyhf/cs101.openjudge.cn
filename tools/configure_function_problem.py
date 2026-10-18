#!/usr/bin/env python3
"""为已收录的题目配置函数提交：前置代码 + 学生函数 + 后置代码。"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIRROR = ROOT / "data/openjudge"
LANGUAGES = ("python", "pypy3", "cpp", "c", "csharp", "fsharp", "vbnet", "swift", "objc")


def configure(book, problem, prefix, suffix, languages, samples):
    """只配置现有题目；测试数据、题面和其他判题钩子保持原样。"""
    catalog_path = MIRROR / "catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    row = next((r for r in catalog["problems"] if r["book"] == book and r["id"] == problem), None)
    if row is None or not row.get("test_cases"):
        raise ValueError("请先收录题面和测试数据，再配置函数提交")
    roots = {(MIRROR / case[key]).resolve().parent.parent
             for case in row["test_cases"] for key in ("input", "output")}
    if len(roots) != 1:
        raise ValueError("函数题的测试数据必须位于同一个数据目录")
    directory = roots.pop()
    if not directory.is_relative_to((MIRROR / "tests").resolve()):
        raise ValueError("测试数据目录必须位于 data/openjudge/tests 内")
    languages = list(dict.fromkeys(languages))
    if not languages or any(lang not in LANGUAGES for lang in languages):
        raise ValueError("请选择支持的提交语言")
    prefix_text = Path(prefix).read_text(encoding="utf-8")
    suffix_text = Path(suffix).read_text(encoding="utf-8")
    if not suffix_text.strip():
        raise ValueError("后置代码不能为空，需负责读入、调用函数和输出")
    public = json.loads(Path(samples).read_text(encoding="utf-8"))
    if not isinstance(public, list) or not public:
        raise ValueError("公开样例必须是非空数组")
    for case in public:
        if (not isinstance(case, dict) or set(case) != {"input", "output"}
                or any(not isinstance(case[k], str) or len(case[k].encode()) > 64 * 1024
                       for k in ("input", "output"))):
            raise ValueError("公开样例需含 input/output 字符串，每项不超过 64 KiB")
    # 所有参数先校验，再写入配置；绝不从隐藏测试自动生成公开样例。
    files = {"preset_code.py": prefix_text, "preset_suffix.py": suffix_text,
             "preset_languages.json": json.dumps(languages, ensure_ascii=False, indent=2) + "\n",
             "samples.json": json.dumps(public, ensure_ascii=False, indent=2) + "\n"}
    for name, text in files.items():
        (directory / name).write_text(text, encoding="utf-8")
    relative = directory.relative_to(MIRROR.resolve())
    row.update({"code_prefix": str(relative / "preset_code.py"),
                "code_suffix": str(relative / "preset_suffix.py"),
                "code_languages": languages, "sample_cases": public})
    catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("book")
    parser.add_argument("problem")
    parser.add_argument("--prefix", required=True, type=Path, help="前置代码文件（可为空文件）")
    parser.add_argument("--suffix", required=True, type=Path, help="读入、调用函数并输出的后置代码")
    parser.add_argument("--languages", required=True, nargs="+", choices=LANGUAGES)
    parser.add_argument("--samples", required=True, type=Path, help="公开样例 JSON，不能使用隐藏测试")
    args = parser.parse_args()
    try:
        configure(args.book, args.problem, args.prefix, args.suffix, args.languages, args.samples)
    except (ValueError, OSError) as error:
        parser.exit(1, f"配置失败：{error}\n")
    print(f"configured function submission: {args.book}/{args.problem}")


if __name__ == "__main__":
    main()
