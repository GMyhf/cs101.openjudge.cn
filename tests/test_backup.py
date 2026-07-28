"""数据库备份的回归测试。

备份是「平时没人看、真出事时唯一指望」的东西 —— 正因为平时没人看，
它坏掉的时候不会有任何信号。所以这里不只测「能不能生成文件」，
重点测**自检能不能真的抓住坏备份**：一个抓不出损坏的校验，比没有校验更危险，
因为它给出的是虚假的安心。

写这些用例时踩到的一个坑值得留着：第一次拿**空库**做损坏测试，
抹掉 60 字节后 `integrity_check` 照样返回 ok —— 因为那片是未使用的页空间。
损坏测试必须打在有真实内容的库上，并且抹掉整整一页。
"""
import gzip
import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "backup_db.py"


def make_database(path, users=120, submissions=800):
    """造一个有真实内容的库：空库上的损坏测试是假的（见模块说明）。"""
    with sqlite3.connect(path) as db:
        db.execute("create table users(username text primary key, password_hash text,"
                   " email text, active int)")
        db.execute("create table submissions(id integer primary key, user text, problem text,"
                   " result text, created text, source text)")
        db.execute("create table settings(key text primary key, value text not null)")
        for index in range(users):
            db.execute("insert into users values (?,?,?,1)",
                       (f"stu{index}", "pbkdf2$120000$aa$bb" * 4, f"s{index}@example.edu"))
        for index in range(submissions):
            db.execute("insert into submissions(user,problem,result,created,source)"
                       " values (?,?,?,?,?)",
                       (f"stu{index % users}", f"{index % 900:05d}", "Accepted",
                        "2026-07-28 10:00:00", "print(1)\n" * 20))
        db.execute("insert into settings values ('quotas','{}')")


def run(*args, database=None, backup_dir=None, keep=None):
    environment = os.environ.copy()
    if database:
        environment["CS101_DB"] = str(database)
    if backup_dir:
        environment["CS101_BACKUP_DIR"] = str(backup_dir)
    if keep is not None:
        environment["CS101_BACKUP_KEEP"] = str(keep)
    return subprocess.run([sys.executable, str(TOOL), *args], cwd=ROOT, env=environment,
                          capture_output=True, text=True, timeout=120)


class BackupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.database = self.root / "course.db"
        self.backups = self.root / "backups"
        make_database(self.database)

    def backup_files(self):
        return sorted(self.backups.glob("course-*.db.gz"))

    def test_backup_round_trips_every_row(self):
        result = run(database=self.database, backup_dir=self.backups)
        self.assertEqual(result.returncode, 0, result.stderr)
        files = self.backup_files()
        self.assertEqual(len(files), 1)

        restored = self.root / "restored.db"
        result = run("--restore", str(files[0]), "--to", str(restored),
                     database=self.database, backup_dir=self.backups)
        self.assertEqual(result.returncode, 0, result.stderr)
        with sqlite3.connect(restored) as db:
            self.assertEqual(db.execute("select count(*) from users").fetchone()[0], 120)
            self.assertEqual(db.execute("select count(*) from submissions").fetchone()[0], 800)

    def test_corrupted_backup_is_rejected(self):
        """核心用例：抓不出损坏的校验比没有校验更危险。"""
        run(database=self.database, backup_dir=self.backups)
        good = self.backup_files()[0]

        raw = bytearray(gzip.decompress(good.read_bytes()))
        middle = len(raw) // 2
        raw[middle:middle + 4096] = b"\x00" * 4096      # 抹掉整整一页
        broken = self.backups / "broken.db.gz"
        broken.write_bytes(gzip.compress(bytes(raw)))

        result = run("--verify", str(broken), database=self.database, backup_dir=self.backups)
        self.assertEqual(result.returncode, 1, "损坏的备份必须校验不过")

        restored = self.root / "nope.db"
        result = run("--restore", str(broken), "--to", str(restored),
                     database=self.database, backup_dir=self.backups)
        self.assertEqual(result.returncode, 1, "校验不过的备份必须拒绝还原")
        self.assertFalse(restored.exists(), "拒绝还原时不该留下半个文件")

    def test_rotation_keeps_only_the_configured_count(self):
        import time
        for _ in range(5):
            run(database=self.database, backup_dir=self.backups, keep=3)
            time.sleep(1.05)          # 文件名精确到秒，跨秒才是不同的一份
        self.assertEqual(len(self.backup_files()), 3)

    def test_backups_are_not_world_readable(self):
        """里面是口令哈希：同机其他用户不该读得到。"""
        run(database=self.database, backup_dir=self.backups)
        self.assertEqual(self.backups.stat().st_mode & 0o777, 0o700)
        for path in self.backup_files():
            self.assertEqual(path.stat().st_mode & 0o777, 0o600, path.name)

    def _shim_path(self, rsync_body, ssh_body):
        """造一对假的 rsync/ssh 放进 PATH。

        异地推送真正要验的逻辑是「rsync 说成功了，但对面那份是不是完好的」——
        这条不需要真实 SSH 也能验，而真实 SSH 需要动开发机的密钥配置，不该为跑测试去动。
        """
        binaries = self.root / "bin"
        binaries.mkdir(exist_ok=True)
        for name, body in (("rsync", rsync_body), ("ssh", ssh_body)):
            path = binaries / name
            path.write_text("#!/bin/sh\n" + body + "\n", encoding="utf-8")
            path.chmod(0o755)
        return f"{binaries}:{os.environ['PATH']}"

    def _run_with_path(self, path_value, remote):
        environment = os.environ.copy()
        environment.update({"CS101_DB": str(self.database), "CS101_BACKUP_DIR": str(self.backups),
                            "CS101_BACKUP_REMOTE": remote, "PATH": path_value})
        return subprocess.run([sys.executable, str(TOOL)], cwd=ROOT, env=environment,
                              capture_output=True, text=True, timeout=120)

    def test_offsite_push_rejects_a_mismatching_remote_copy(self):
        """rsync 退出 0 只说明传输没报错，不说明对面那份是好的。"""
        path_value = self._shim_path("exit 0", 'echo "0000000000000000000000000000000000000000000000000000000000000000  x"')
        result = self._run_with_path(path_value, "u@h:/tmp/remote")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("远端校验和不一致", result.stdout + result.stderr)

    def test_offsite_push_accepts_a_matching_remote_copy(self):
        # 假 ssh 直接算本地那份的校验和：模拟「远端确实和本地一致」
        ssh_body = ('f=$(ls -t %s/course-*.db.gz | head -1); sha256sum "$f"' % self.backups)
        result = self._run_with_path(self._shim_path("exit 0", ssh_body), "u@h:/tmp/remote")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("远端已核对一致", result.stdout)

    def test_offsite_failure_does_not_discard_the_local_backup(self):
        """异地失败要非零退出（触发告警），但本地那份必须留下。"""
        result = self._run_with_path(self._shim_path("exit 23", "exit 1"), "u@h:/tmp/remote")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(len(self.backup_files()), 1, "本地备份不该因为推不出去而丢失")

    def test_missing_source_fails_loudly(self):
        result = run(database=self.root / "not-here.db", backup_dir=self.backups)
        self.assertEqual(result.returncode, 1)
        self.assertFalse(self.backups.exists() and self.backup_files())


if __name__ == "__main__":
    unittest.main()
