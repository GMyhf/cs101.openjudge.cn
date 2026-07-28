#!/usr/bin/env python3
"""备份 data/course.db —— 这套系统里唯一不可重建的东西。

代码在 git，题面能重抓，测试数据入库，配置能重写。只有账号（含口令哈希）
和全部提交记录，丢了就是丢了。

三个刻意的设计：

**用 SQLite 的在线备份 API，不用 `cp`。** 服务是一直在跑的，`cp` 可能拷到写了一半
的库；`Connection.backup()` 走的是 SQLite 自己的备份接口，能拿到一致快照。

**备份完立刻验。** 一堆没验过的文件不叫备份。这里对**备份文件本身**跑
`PRAGMA integrity_check`，再把关键表的行数和源库比一遍 —— 截断或写坏都会被抓住。

**存在仓库之外，权限 600。** 里面是口令哈希：不该被误提交，也不该被同机其他用户读到。

用法：
    python3 tools/backup_db.py                 # 备份到默认目录
    python3 tools/backup_db.py --list          # 看现有备份
    python3 tools/backup_db.py --verify <文件> # 单独验一份
    python3 tools/backup_db.py --restore <文件> --to /tmp/restored.db

环境变量：`CS101_BACKUP_DIR`（默认 ~/backups/cs101）、`CS101_BACKUP_KEEP`（默认 14）。
"""
import argparse
import gzip
import os
import shutil
import sqlite3
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = Path(os.environ.get("CS101_DB", ROOT / "data" / "course.db"))
BACKUP_DIR = Path(os.environ.get("CS101_BACKUP_DIR", Path.home() / "backups" / "cs101"))
KEEP = int(os.environ.get("CS101_BACKUP_KEEP", "14"))
CHECKED_TABLES = ("users", "submissions", "settings")


def table_counts(path):
    with sqlite3.connect(f"file:{path}?mode=ro", uri=True) as db:
        counts = {}
        for table in CHECKED_TABLES:
            try:
                counts[table] = db.execute(f"select count(*) from {table}").fetchone()[0]
            except sqlite3.Error:
                counts[table] = None
        return counts


def verify(path):
    """对备份文件本身做完整性检查，返回 (ok, 说明, 行数)。"""
    opener = gzip.open if str(path).endswith(".gz") else open
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as handle:
        plain = Path(handle.name)
    try:
        with opener(path, "rb") as src, plain.open("wb") as dst:
            shutil.copyfileobj(src, dst)
        with sqlite3.connect(f"file:{plain}?mode=ro", uri=True) as db:
            result = db.execute("pragma integrity_check").fetchone()[0]
        if result != "ok":
            return False, f"integrity_check: {result}", {}
        return True, "ok", table_counts(plain)
    except (sqlite3.Error, OSError) as error:
        return False, f"{type(error).__name__}: {error}", {}
    finally:
        plain.unlink(missing_ok=True)


def make_backup():
    if not SOURCE.is_file():
        print(f"源库不存在：{SOURCE}", file=sys.stderr)
        return 1
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    os.chmod(BACKUP_DIR, 0o700)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    final = BACKUP_DIR / f"course-{stamp}.db.gz"
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False, dir=BACKUP_DIR) as handle:
        staging = Path(handle.name)

    try:
        # 在线备份：服务正在写也能拿到一致快照
        with sqlite3.connect(f"file:{SOURCE}?mode=ro", uri=True) as src, \
                sqlite3.connect(staging) as dst:
            src.backup(dst)

        ok, note, counts = verify(staging)
        if not ok:
            print(f"备份自检失败，不落盘：{note}", file=sys.stderr)
            return 1
        live = table_counts(SOURCE)
        # 服务可能在备份期间又写了几行，所以备份只需 <= 源库，不能反过来少一大截
        for table in CHECKED_TABLES:
            if counts.get(table) is None or live.get(table) is None:
                continue
            if counts[table] > live[table]:
                print(f"备份的 {table} 比源库还多，异常，不落盘", file=sys.stderr)
                return 1

        with staging.open("rb") as src, gzip.open(final, "wb") as dst:
            shutil.copyfileobj(src, dst)
        os.chmod(final, 0o600)
    finally:
        staging.unlink(missing_ok=True)

    size = final.stat().st_size
    summary = "  ".join(f"{t}={counts.get(t)}" for t in CHECKED_TABLES)
    print(f"✅ {final.name}  {size} 字节  {summary}")

    existing = sorted(BACKUP_DIR.glob("course-*.db.gz"))
    for stale in existing[:-KEEP] if KEEP > 0 else []:
        stale.unlink()
        print(f"   轮转删除 {stale.name}")
    print(f"   保留 {len(sorted(BACKUP_DIR.glob('course-*.db.gz')))} 份于 {BACKUP_DIR}")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--verify", metavar="文件")
    parser.add_argument("--restore", metavar="文件")
    parser.add_argument("--to", metavar="目标")
    options = parser.parse_args()

    if options.list:
        files = sorted(BACKUP_DIR.glob("course-*.db.gz"))
        if not files:
            print(f"{BACKUP_DIR} 下没有备份")
            return 1
        for path in files:
            age = (time.time() - path.stat().st_mtime) / 3600
            print(f"  {path.name}  {path.stat().st_size} 字节  {age:.1f} 小时前")
        return 0

    if options.verify:
        ok, note, counts = verify(Path(options.verify))
        summary = "  ".join(f"{t}={counts.get(t)}" for t in CHECKED_TABLES)
        print(("✅ " if ok else "❌ ") + note + ("  " + summary if ok else ""))
        return 0 if ok else 1

    if options.restore:
        if not options.to:
            print("--restore 需要配合 --to 指定目标路径", file=sys.stderr)
            return 2
        ok, note, _ = verify(Path(options.restore))
        if not ok:
            print(f"这份备份自检不过，拒绝还原：{note}", file=sys.stderr)
            return 1
        with gzip.open(options.restore, "rb") as src, open(options.to, "wb") as dst:
            shutil.copyfileobj(src, dst)
        os.chmod(options.to, 0o600)
        print(f"✅ 已还原到 {options.to}（不会自动替换线上库，请自行停服后替换）")
        return 0

    return make_backup()


if __name__ == "__main__":
    sys.exit(main())
