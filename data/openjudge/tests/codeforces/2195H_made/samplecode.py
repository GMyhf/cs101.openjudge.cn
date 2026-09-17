# Codeforces 2195H Codeforces Heuristic Contest 001 -- reference solution.
# Written for this repository as a hand-off artifact; no external license.
#
# 9n^2 points and 3 per triangle bound the answer by 3n^2.  It is reached for n >= 2:
#   * a 3x2 block (3 columns, 2 rows) holds two disjoint unit triangles
#       (x,y) (x,y+1) (x+1,y)   and   (x+1,y+1) (x+2,y+1) (x+2,y);
#   * 3n even  -> tile the whole square with 3x2 blocks;
#   * 3n odd   -> a hand-searched perfect 9x9 packing (27 triangles, found by exhaustive
#     backtracking) in the corner, columns 10..3n of rows 1..9 with 2x3 blocks
#     (transposed), rows 10..3n with 3x2 blocks (3n-9 is divisible by 6).
# n = 1: the 3x3 grid holds at most 2 (exhaustive search), as in the sample.
import sys

NINE = ("112112 314122 516132 718152 917282 422333 624353 927383 131424 634454 937484 "
        "341525 644555 947585 351626 654656 957686 361727 664757 967787 371828 675859 "
        "977888 381929 483949 686979 988999").split()


def blocks32(x0, x1, y0, y1, out, transpose=False):
    """tile columns x0..x1, rows y0..y1 with 3-wide 2-tall blocks (or 2-wide 3-tall)."""
    if not transpose:
        for x in range(x0, x1 + 1, 3):
            for y in range(y0, y1 + 1, 2):
                out.append(f"{x} {y} {x} {y + 1} {x + 1} {y}")
                out.append(f"{x + 1} {y + 1} {x + 2} {y + 1} {x + 2} {y}")
    else:
        for x in range(x0, x1 + 1, 2):
            for y in range(y0, y1 + 1, 3):
                out.append(f"{x} {y} {x + 1} {y} {x} {y + 1}")
                out.append(f"{x + 1} {y + 1} {x + 1} {y + 2} {x} {y + 2}")


def solve(n, out):
    s = 3 * n
    if n == 1:
        out.append("2")
        out.append("1 1 1 2 2 1")
        out.append("2 3 3 2 3 3")
        return
    out.append(str(3 * n * n))
    if s % 2 == 0:
        blocks32(1, s, 1, s, out)
    else:
        for tri in NINE:
            out.append(" ".join(tri))
        blocks32(10, s, 1, 9, out, transpose=True)
        blocks32(1, s, 10, s, out)


def main():
    data = sys.stdin.read().split()
    out = []
    for k in range(int(data[0])):
        solve(int(data[1 + k]), out)
    sys.stdout.write("\n".join(out) + "\n")


main()
