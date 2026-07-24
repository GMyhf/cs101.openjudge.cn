import random
import subprocess
import tempfile
from pathlib import Path
SAMPLE_IN = '4\n1 1 3 5\n'
SAMPLE_OUT = '17\n'
CASES = ['4\n1 1 3 5\n', '10\n997 881 323 23 317 681 558 105 950 659\n', '27\n945 168 703 107 795 339 60 130 431 521 522 217 907 877 258 940 754 727 814 959 970 806 564 509 993 234 708\n', '17\n388 653 190 153 802 390 409 642 357 570 627 845 385 326 189 291 473\n', '23\n835 250 908 689 572 856 690 136 709 198 468 265 386 934 573 807 610 921 758 950 859 360 330\n', '14\n811 821 146 474 462 624 26 629 452 35 555 39 821 389\n', '4\n968 596 478 749\n', '9\n12 487 3 502 210 672 646 547 427\n', '1\n239\n', '27\n212 705 929 389 356 826 299 926 664 238 80 358 769 964 451 274 824 769 845 199 777 479 55 343 890 204 47\n', '17\n430 59 994 33 896 332 625 684 388 473 855 526 413 671 961 898 402\n', '16\n176 888 462 643 97 721 635 510 851 799 285 916 427 1000 177 879\n', '29\n600 224 115 256 784 517 157 919 438 287 807 688 847 649 155 580 830 573 972 260 642 641 961 277 280 350 772 299 48\n', '23\n385 86 918 55 238 955 401 505 116 774 512 473 501 626 137 172 22 333 990 247 422 198 745\n', '10\n429 301 595 186 550 920 964 280 76 392\n', '15\n186 886 604 615 523 804 770 999 970 784 537 561 944 690 276\n', '22\n81 832 906 997 959 769 675 608 322 431 207 874 131 94 619 350 863 943 251 873 277 50\n', '7\n460 195 550 883 457 506 128\n', '15\n131 59 637 586 435 724 102 554 389 405 453 723 125 376 296\n', '13\n386 26 370 396 690 737 222 421 679 990 118 146 485\n']
REFERENCE_SOURCE = 'import heapq\n\ndef min_weighted_path_length(n, weights):\n    heapq.heapify(weights)\n    total = 0\n    while len(weights) > 1:\n        a = heapq.heappop(weights)\n        b = heapq.heappop(weights)\n        combined = a + b\n        total += combined\n        heapq.heappush(weights, combined)\n    return total\n\n# 读取输入\nn = int(input())\nweights = list(map(int, input().split()))\nprint(min_weighted_path_length(n, weights))\n'
assert SAMPLE_IN.strip()
assert SAMPLE_OUT.strip()
random.seed(4080)
assert CASES[0] == SAMPLE_IN
def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=5, check=True)
    return result.stdout
assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split()
def generate_case(index):
    return CASES[index]
root = Path(__file__).parent / "data"
for index in range(20):
    content = generate_case(index)
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")
