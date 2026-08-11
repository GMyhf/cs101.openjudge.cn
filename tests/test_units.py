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
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
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


class HandbookBuildTests(unittest.TestCase):
    """网页版手册必须与 Markdown 同步。

    `docs/dev-handbook.html` 是产物，`docs/DEV_HANDBOOK.md` 是事实源。
    改了 Markdown 忘了重新构建，公开页就会停在旧版本 —— 而且没有任何征兆，
    页面照样打得开。所以这里重新构建一遍，和已提交的产物逐字节比。
    """

    def test_generated_page_is_up_to_date(self):
        import subprocess, sys
        built = ROOT / "docs" / "dev-handbook.html"
        self.assertTrue(built.is_file(), "缺 docs/dev-handbook.html，跑 tools/build_handbook.py")
        before = built.read_bytes()
        result = subprocess.run([sys.executable, "tools/build_handbook.py"],
                                cwd=ROOT, capture_output=True, text=True, timeout=120)
        self.assertEqual(result.returncode, 0, result.stderr)
        after = built.read_bytes()
        if before != after:
            built.write_bytes(before)          # 测试不该改动工作区
            self.fail("dev-handbook.html 与 DEV_HANDBOOK.md 不同步："
                      "请跑 `python3 tools/build_handbook.py` 并提交产物")


PAGES = ("index.html", "problems.html", "book.html", "history.html", "admin.html")
THEME_CSS = ROOT / "static" / "theme.css"

# 颜色字面量。`#f4f7f4` 这类必须落进 theme.css，页面里出现就是一次深色漏色。
HEX_COLOR = re.compile(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b")
CSS_VAR_USE = re.compile(r"var\(\s*(--[a-z0-9-]+)")
CSS_VAR_DEF = re.compile(r"(--[a-z0-9-]+)\s*:")
STYLE_BLOCK = re.compile(r"<style[^>]*>(.*?)</style>", re.S)
CSS_COMMENT = re.compile(r"/\*.*?\*/", re.S)
CLASS_SELECTOR = re.compile(r"\.([a-zA-Z][\w-]*)")


def page_sources():
    """所有会被送给浏览器的页面文本：5 个 `.html` + `server.py` 里的模板。"""
    for name in PAGES:
        yield name, (ROOT / name).read_text(encoding="utf-8")
    yield "server.py", (ROOT / "server.py").read_text(encoding="utf-8")


class ThemeConsistencyTests(unittest.TestCase):
    """页面配色必须全部走 theme.css 的变量。

    这两条判据各自对应一次真实的漏网：
    ①激活页与重置密码页 link 了 theme.css、也写了 `data-theme`，却又把
      `#f4f7f4`/`#16231d`/`#fff` 硬编码在自己的 `<style>` 里 —— **深色模式下是白底**。
    ②`server.py` 里 4 处 `var(--red)`、`history.html` 里 1 处 `var(--bad)` 指向
      **theme.css 从未定义过的变量**，写了等于没写：错误提示不是红的，
      WA 徽章的字和正文同色。悬空变量不会报错，只会安静地什么都不做。
    """

    def test_pages_hold_no_hardcoded_colors(self):
        for name, text in page_sources():
            with self.subTest(page=name):
                found = sorted(set(HEX_COLOR.findall(text)))
                self.assertEqual([], found, f"{name} 里有硬编码色，应改用 theme.css 的变量")

    def test_pages_only_use_variables_theme_css_defines(self):
        theme = THEME_CSS.read_text(encoding="utf-8")
        defined = set(CSS_VAR_DEF.findall(theme))
        self.assertIn("--danger", defined)          # 判据自身的自检：名单读出来了
        for name, text in page_sources():
            with self.subTest(page=name):
                local = set(CSS_VAR_DEF.findall(text))
                dangling = sorted(set(CSS_VAR_USE.findall(text)) - defined - local)
                self.assertEqual([], dangling, f"{name} 用了 theme.css 没定义的变量")

    def test_theme_boot_lives_in_exactly_one_place(self):
        """主题引导脚本只有 `THEME_HEAD` 一份，页面里只留占位符。

        改动前它在 `server.py` 里逐字复制了 9 份、5 个页面各一份。十几份里挑错
        的那一份只能靠肉眼 —— 而写错的代价是那个页面在深色下闪一帧白。
        """
        import server
        for name, text in page_sources():
            with self.subTest(page=name):
                copies = text.count("localStorage.getItem('cs101-theme')")
                if name == "server.py":
                    self.assertEqual(1, copies, "server.py 里应只剩 THEME_HEAD 那一份")
                else:
                    self.assertEqual(0, copies, f"{name} 应改用 __THEME_HEAD__ 占位符")
                self.assertIn(server.THEME_HEAD_SLOT, text, f"{name} 缺主题引导占位符")
        self.assertIn("data-theme", server.THEME_HEAD.replace("dataset.theme", "data-theme"))
        self.assertIn('href="/static/theme.css"', server.THEME_HEAD)


class PageStructureTests(unittest.TestCase):
    """页面结构上的几条硬约束。"""

    def test_style_blocks_define_no_dead_classes(self):
        """CSS 里定义的类，markup 或 JS 里必须真的用得上。

        起因：`index.html` 留着约 1.6KB 的 `.hero`/`.stats` 规则，而对应的
        markup 早就删了 —— 谁来改这页都得先分辨哪些规则还活着。
        动态拼出来的类名（``t-${kind}``）按前缀算用过，否则这条判据会误伤高亮器。
        """
        for name in PAGES:
            text = (ROOT / name).read_text(encoding="utf-8")
            styles = "\n".join(STYLE_BLOCK.findall(text))
            markup = text.replace(styles, "")
            dead = []
            for cls in sorted(set(CLASS_SELECTOR.findall(CSS_COMMENT.sub("", styles)))):
                if cls in markup:
                    continue
                if any(cls[:i] in markup for i in range(2, len(cls)) if cls[i - 1] == "-"):
                    continue
                dead.append(cls)
            with self.subTest(page=name):
                self.assertEqual([], dead, f"{name} 里这些类没人用了")

    def test_tables_can_scroll_on_narrow_screens(self):
        """表格要能自己横向滚，否则窄屏上会把整个页面撑宽、顶栏一起跑出视口。"""
        self.assertIn(".table-wrap", THEME_CSS.read_text(encoding="utf-8"))
        for name in PAGES:
            text = (ROOT / name).read_text(encoding="utf-8")
            segments = text.split("<table")
            for index, before in enumerate(segments[:-1], start=1):
                with self.subTest(page=name, table=index):
                    self.assertIn("table-wrap", before[-200:],
                                  f"{name} 第 {index} 个表格没放进 .table-wrap")

    def test_theme_css_covers_keyboard_focus_and_reduced_motion(self):
        """焦点环要覆盖真正能聚焦的那几类控件，而不只是某一个组件。"""
        theme = THEME_CSS.read_text(encoding="utf-8")
        self.assertIn("prefers-reduced-motion", theme)
        for selector in ("a:focus-visible", "button:focus-visible",
                         "input:focus-visible", "select:focus-visible"):
            self.assertIn(selector, theme)

    def test_each_page_has_exactly_one_top_level_heading(self):
        """首页原先只有 h2/h3，没有 h1 —— 读屏和搜索引擎都拿不到页面主标题。"""
        for name in PAGES:
            text = (ROOT / name).read_text(encoding="utf-8")
            with self.subTest(page=name):
                self.assertEqual(1, len(re.findall(r"<h1[\s>]", text)), f"{name} 的 h1 数量不对")


if __name__ == "__main__":
    unittest.main()
