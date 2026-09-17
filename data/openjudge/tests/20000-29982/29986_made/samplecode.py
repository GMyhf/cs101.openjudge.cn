# 29986 猜数 —— 参考解（仓库交接件，未套用外部许可）。
# 平台把 preset_code.py 拼在这段代码前面：query(i) 返回 i 与秘密数的大小关系，最多 15 次。
# [0, 1000] 共 1001 个数，二分最多 10 次。
lo, hi = 0, 1000
while True:
    mid = (lo + hi) // 2
    reply = query(mid)
    if reply == 0:
        break
    if reply > 0:
        hi = mid - 1
    else:
        lo = mid + 1
