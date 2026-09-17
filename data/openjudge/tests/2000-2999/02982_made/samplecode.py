# 02982 Sudoku 参考解。为本仓库判题数据而写的交接产物（2026-09-17），不来自任何外部提交，无外部许可证。
# 位掩码 + 最少候选优先（MRV）回溯；每组打印找到的第一个解（解不唯一时任一即可，由 checker 判）。
import sys


def solve(grid):
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    empty = []
    for i in range(81):
        v = grid[i]
        r, c = divmod(i, 9)
        if v:
            bit = 1 << v
            rows[r] |= bit
            cols[c] |= bit
            boxes[r // 3 * 3 + c // 3] |= bit
        else:
            empty.append(i)
    full = 0b1111111110

    def dfs():
        best = -1
        best_mask = 0
        best_count = 10
        for idx, i in enumerate(empty):
            if grid[i]:
                continue
            r, c = divmod(i, 9)
            mask = full & ~(rows[r] | cols[c] | boxes[r // 3 * 3 + c // 3])
            count = bin(mask).count("1")
            if count < best_count:
                best, best_mask, best_count = i, mask, count
                if count <= 1:
                    break
        if best < 0:
            return True
        if best_count == 0:
            return False
        r, c = divmod(best, 9)
        b = r // 3 * 3 + c // 3
        mask = best_mask
        while mask:
            bit = mask & -mask
            mask ^= bit
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
            grid[best] = bit.bit_length() - 1
            if dfs():
                return True
            rows[r] ^= bit
            cols[c] ^= bit
            boxes[b] ^= bit
            grid[best] = 0
        return False

    return dfs()


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for k in range(t):
        grid = [int(ch) for line in data[1 + 9 * k:10 + 9 * k] for ch in line]
        solve(grid)
        for r in range(9):
            out.append("".join(map(str, grid[9 * r:9 * r + 9])))
    print("\n".join(out))


main()
