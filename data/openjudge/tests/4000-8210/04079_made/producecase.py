import random
import subprocess
import tempfile
from pathlib import Path
SAMPLE_IN = '41 467 334 500 169 724 478 358 962 464 705 145 281 827 961 491 995 942 827 436\n'
SAMPLE_OUT = '41 467 334 169 145 281 358 464 436 500 478 491 724 705 962 827 961 942 995\n'
CASES = ['41 467 334 500 169 724 478 358 962 464 705 145 281 827 961 491 995 942 827 436\n', '408 498 585 378 978 230 977 297 745 933 910 800 989 470 492 723 331 646 192 444 704 468 319 334 157 466 802 353 264 115 396 268 261 826\n', '997 881 323 23 317 681 558 105 950 659 897 97 164 442 926 165 336 87 401 15 820 307\n', '703 107 795 339 60 130 431 521 522 217 907 877 258\n', '388 653 190 153 802 390 409 642 357 570 627 845 385 326 189 291 473 835 493 606 346 240 44 476 197 112 452 578 296 538 580 38 677 106 307\n', '908 689 572 856 690 136 709 198 468 265 386 934 573 807 610 921 758 950\n', '811 821 146 474 462 624 26 629 452 35 555 39 389 633 441 406 781 54 248 285 189 196 144 209 661 47 775 827 67 932\n', '968 596 478 749 298 457 250 451 485\n', '12 487 3 502 210 672 646 547 427 963 817 359 813 688 624 100 356 917 252\n', '239 280 681 830\n', '705 929 389 356 826 299 926 664 238 80 358 769 964 451 274 824\n', '430 59 994 33 896 332 625 684 388 473 855 526 413 671 961 898 402 74 551 73 574 243 428 897 595 947 179 634 355 971 109 700 781 39 113 229\n', '176 888 462 643 97 721 635 510 851 799 285 916 427 177 879 852 47 116 938 232 550 42 224 432 121 507 837 600 702 335 307 449 792 971\n', '224 115 256 784 517 157 919 438 287 807 688 847 649 155 580 830 573 972 260 642 641 961 277 280 350 772 299 48 714 745 389 72 601 251 914 489 439 253 213 892\n', '86 918 55 238 955 401 505 116 774 512 473 501 626 137 172 22 333 990 247 422 198 745 140 748 602 903 124\n', '429 301 595 186 550 920 964 280 76 392 141 734 828 426 214 557 175 596 541 972 247 559\n', '186 886 604 615 523 804 770 999 970 784 537 561 944 690 276 441 630 793 710 246 513 285 602 472 559 170 299 439 762 187 303\n', '832 906 997 959 769 675 608 322\n', '460 195 550 883 457 506 128 192 203 908 456 138 14 765 758 139\n', '131 59 637 586 435 724 102 554 389 405 453 723 125 376 296 62 959 474 852 622 85 913 633 589 900 312 183 798 488 317 997\n']
REFERENCE_SOURCE = "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef insert_into_bst(root, val):\n    if root is None:\n        return TreeNode(val)\n    if val < root.val:\n        root.left = insert_into_bst(root.left, val)\n    elif val > root.val:\n        root.right = insert_into_bst(root.right, val)\n    return root\n\ndef preorder_traversal(root):\n    return [root.val] + preorder_traversal(root.left) + preorder_traversal(root.right) if root else []\n\ndef preorderTraversal(root):\n    if root is None:\n        return []\n\n    stack = []\n    result = []\n    stack.append(root)\n\n    while stack:\n        node = stack.pop()\n        result.append(node.val)\n\n        # 先将右子节点入栈，再将左子节点入栈\n        if node.right:\n            stack.append(node.right)\n        if node.left:\n            stack.append(node.left)\n\n    return result\n\n# 读取输入并转换成整数列表\nnumbers = list(map(int, input().split()))\n\n# 构造二叉搜索树\nbst_root = None\nfor num in numbers:\n    bst_root = insert_into_bst(bst_root, num)\n\n# 前序遍历二叉搜索树并输出\n#print(' '.join(map(str, preorder_traversal(bst_root))))\nprint(' '.join(map(str, preorderTraversal(bst_root))))\n"
assert SAMPLE_IN.strip()
assert SAMPLE_OUT.strip()
random.seed(4079)
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
