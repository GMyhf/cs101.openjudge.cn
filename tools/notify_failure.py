#!/usr/bin/env python3
"""systemd 单元失败时发一封告警邮件，顺带把失败写进 journal。

为什么需要：`Restart=on-failure` 会把服务自动拉起来 —— 好事，但也意味着
**崩溃循环是静默的**。除非有人恰好去看 `systemctl status`，否则没有任何信号。
备份定时器同理：它失败了最不该是「没人知道」。

复用 data/.smtp.env（服务端本来就从这里读邮件配置），所以不需要另配一套。
收件人取 CS101_ALERT_EMAIL，没设就退回 CS101_SMTP_FROM / CS101_SMTP_USER。
发不出去也不算失败：至少 journal 里留下了记录。
"""
import os
import smtplib
import subprocess
import sys
from email.message import EmailMessage
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_dotenv():
    path = ROOT / "data" / ".smtp.env"
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def main():
    unit = sys.argv[1] if len(sys.argv) > 1 else "unknown.service"
    load_dotenv()

    status = subprocess.run(["systemctl", "status", "--no-pager", "-n", "30", unit],
                            capture_output=True, text=True).stdout
    # 先写 journal：邮件可能发不出去，这条一定留得下
    print(f"[alert] {unit} 失败\n{status}", flush=True)

    host = os.environ.get("CS101_SMTP_HOST")
    recipient = (os.environ.get("CS101_ALERT_EMAIL")
                 or os.environ.get("CS101_SMTP_FROM")
                 or os.environ.get("CS101_SMTP_USER"))
    if not host or not recipient:
        print("[alert] 未配 SMTP 或收件人，只写了 journal", flush=True)
        return 0

    message = EmailMessage()
    message["Subject"] = f"[CS101] {unit} 失败"
    message["From"] = os.environ.get("CS101_SMTP_FROM", os.environ.get("CS101_SMTP_USER", ""))
    message["To"] = recipient
    message.set_content(f"{unit} 进入失败状态。\n\n{status}\n")
    try:
        port = int(os.environ.get("CS101_SMTP_PORT", "465"))
        if port == 465:
            server = smtplib.SMTP_SSL(host, port, timeout=20)
        else:
            server = smtplib.SMTP(host, port, timeout=20)
            server.starttls()
        with server:
            user = os.environ.get("CS101_SMTP_USER")
            if user:
                server.login(user, os.environ.get("CS101_SMTP_PASSWORD", ""))
            server.send_message(message)
        print(f"[alert] 已通知 {recipient}", flush=True)
    except (OSError, smtplib.SMTPException) as error:
        # 告警发不出去不该让这个单元也失败，否则 OnFailure 可能自我触发
        print(f"[alert] 邮件发送失败（journal 已留记录）：{type(error).__name__}: {error}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
