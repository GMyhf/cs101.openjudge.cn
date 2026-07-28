"""systemd 单元文件的结构检查。

起因：给 `cs101.service` 加 `LimitNOFILE` 时用了一次朴素的字符串替换，
而 `Restart=on-failure` 这段文字**同时出现在一条注释里**，替换命中了注释那一处。
结果 `LimitNOFILE` 落进了 `[Unit]`（systemd 直接忽略），一条注释被截成了非注释行。

systemd 其实说得很清楚：

    cs101.service:10: Unknown key name 'LimitNOFILE' in section 'Unit', ignoring.

但它只写在 journal 里 —— 服务照常起来了，`systemctl is-active` 是 active，
冒烟也全过，唯独那条限制**根本没生效**。不专门去看 journal 就发现不了。
所以把它变成一条会红的检查。
"""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEPLOY = ROOT / "deploy"

# 只列我们实际用到的键，避免把这份清单变成 systemd 文档的副本。
UNIT_ONLY = {"Description", "Documentation", "After", "Before", "Wants", "Requires", "OnFailure"}
SERVICE_ONLY = {"Type", "User", "Group", "WorkingDirectory", "Environment", "EnvironmentFile",
                "ExecStart", "ExecStop", "Restart", "RestartSec", "KillMode", "TimeoutStopSec",
                "LimitNOFILE", "PrivateTmp", "NoNewPrivileges", "ProtectSystem", "StandardOutput",
                "StandardError"}
TIMER_ONLY = {"OnCalendar", "Persistent", "RandomizedDelaySec", "OnBootSec", "OnUnitActiveSec"}
INSTALL_ONLY = {"WantedBy", "RequiredBy"}
EXPECTED_SECTION = {}
for key in UNIT_ONLY:
    EXPECTED_SECTION[key] = "[Unit]"
for key in SERVICE_ONLY:
    EXPECTED_SECTION[key] = "[Service]"
for key in TIMER_ONLY:
    EXPECTED_SECTION[key] = "[Timer]"
for key in INSTALL_ONLY:
    EXPECTED_SECTION[key] = "[Install]"


def parse(path):
    """返回 [(section, key, lineno)]，并对结构不合法的行抛错。"""
    entries, section = [], None
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith(";"):
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line
            continue
        if "=" not in line:
            raise AssertionError(f"{path.name}:{number} 既不是注释也不是 Key=Value：{raw!r}")
        key, _, value = line.partition("=")
        entries.append((section, key.strip(), number, value.strip()))
    return entries


class UnitFileTests(unittest.TestCase):
    def unit_files(self):
        files = sorted(DEPLOY.glob("*.service")) + sorted(DEPLOY.glob("*.timer"))
        self.assertTrue(files, "deploy/ 下应当有单元文件")
        return files

    def test_every_directive_sits_in_the_right_section(self):
        for path in self.unit_files():
            for section, key, number, _ in parse(path):
                expected = EXPECTED_SECTION.get(key)
                if expected is None:
                    continue                       # 不认识的键交给 systemd 自己判断
                self.assertEqual(section, expected,
                                 f"{path.name}:{number} `{key}` 出现在 {section}，"
                                 f"应当在 {expected} —— systemd 会静默忽略它")

    def test_no_stray_lines(self):
        """被截断的注释会变成解析不了的行，而服务照样能起来。"""
        for path in self.unit_files():
            parse(path)                            # 结构不对就抛错

    def test_service_units_declare_what_this_deployment_needs(self):
        """这几条都是踩过坑才加上的，缺一条就是一次线上退化。

        只看**解析出来的指令**，不对原文做字符串匹配 —— 这个文件里到处都是
        「不要写 X」的注释，拿原文匹配会把注释当成指令。
        本测试第一版就栽在这里：断言「不含 StandardOutput=append:」，
        结果命中的正是那句叮嘱不要用它的注释。
        """
        directives = {}
        for _, key, _, value in parse(DEPLOY / "cs101.service"):
            directives.setdefault(key, []).append(value)

        paths = [v for v in directives.get("Environment", []) if v.startswith("PATH=")]
        self.assertTrue(paths, "缺 Environment=PATH=：systemd 不继承登录 shell 的 PATH")
        self.assertIn("/.local/bin", paths[0], "PATH 里要含 ~/.local/bin，否则找不到 pypy3")

        self.assertIn("LimitNOFILE", directives, "并发判题吃描述符，默认 1024 不够")
        self.assertEqual(directives.get("KillMode"), ["control-group"],
                         "判题子进程要随服务一起收掉，不能留孤儿")
        self.assertIn("OnFailure", directives, "崩溃循环不该静默")

        for value in directives.get("StandardOutput", []) + directives.get("StandardError", []):
            self.assertFalse(value.startswith("append:"),
                             "SELinux 下 systemd 打不开 home 里的文件，服务会 209/STDOUT 起不来")
        self.assertNotIn("ProtectHome", directives,
                         "工作目录就在 /home 下，加了它服务直接起不来")


if __name__ == "__main__":
    unittest.main()
