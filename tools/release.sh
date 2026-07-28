#!/usr/bin/env bash
# 部署机上的发版例行动作：拉代码 → 同步 systemd 单元 → 重启 → 等健康 → 全语言冒烟。
#
# 为什么要把冒烟绑进来：2026-07-28 改用 systemd 托管之后，PyPy3 静默失效了 ——
# 代码一行没动，但 systemd 不继承登录 shell 的 PATH，判题器就再也找不到
# ~/.local/bin/pypy3，学生选 PyPy3 只会得到 Language Unavailable。
# **换部署方式会悄悄改变判题器能看见什么**，而单元测试在开发机上跑，看不见这件事。
# 所以「重启完跑一次冒烟」必须是发版的一部分，不是想起来才做的事。
#
# 用法：  sudo -u rocky tools/release.sh      （或直接以服务用户身份执行）
set -euo pipefail

cd "$(dirname "$0")/.."
UNIT_SRC="deploy/cs101.service"
UNIT_DST="/etc/systemd/system/cs101.service"
BASE="${CS101_SMOKE_BASE:-http://127.0.0.1:8000}"

echo "==> 拉取代码"
git pull --ff-only

# 单元文件入库，但装在 /etc 下；改了就得同步，否则改动不生效且无人察觉。
if ! sudo diff -q "$UNIT_SRC" "$UNIT_DST" >/dev/null 2>&1; then
  echo "==> systemd 单元有变化，同步并 daemon-reload"
  sudo cp "$UNIT_SRC" "$UNIT_DST"
  sudo systemctl daemon-reload
fi

echo "==> 重启服务"
sudo systemctl restart cs101

echo "==> 等待健康"
for _ in $(seq 1 30); do
  if curl -fsS -o /dev/null --max-time 5 "$BASE/api/me"; then
    echo "    起来了"
    break
  fi
  sleep 1
done
curl -fsS -o /dev/null --max-time 5 "$BASE/api/me" || {
  echo "!!! 服务没起来，看 journalctl -u cs101 -n 50" >&2
  exit 1
}

echo "==> 全语言冒烟（--require-all：工具链缺失算失败，不是跳过）"
python3 scripts/smoke_languages.py --require-all --base "$BASE"

echo
echo "==> 发版完成：$(git rev-parse --short HEAD)"
