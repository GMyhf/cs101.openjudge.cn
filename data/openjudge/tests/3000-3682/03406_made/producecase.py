import random
import subprocess
import tempfile
from pathlib import Path
SAMPLE_IN = '6 40\n6\n18\n11\n13\n19\n11\n'
SAMPLE_OUT = '3\n'
CASES = ['6 40\n6\n18\n11\n13\n19\n11\n', '2 44\n54\n17\n', '28 203\n25\n49\n59\n30\n26\n40\n84\n45\n62\n55\n98\n30\n44\n60\n49\n54\n84\n13\n74\n67\n81\n74\n5\n45\n8\n41\n60\n86\n', '26 870\n8\n90\n68\n51\n12\n7\n41\n50\n55\n20\n88\n78\n38\n98\n74\n76\n12\n56\n91\n2\n83\n98\n90\n36\n86\n51\n', '30 1529\n35\n8\n60\n63\n29\n13\n97\n96\n62\n19\n78\n13\n28\n38\n49\n93\n43\n43\n42\n34\n69\n64\n96\n9\n80\n48\n78\n35\n94\n63\n', '2 20\n33\n10\n', '15 584\n30\n5\n40\n81\n78\n46\n23\n70\n54\n23\n96\n47\n3\n2\n82\n', '28 1257\n34\n30\n63\n36\n40\n24\n25\n7\n97\n64\n100\n77\n16\n94\n24\n94\n72\n60\n7\n8\n57\n41\n66\n80\n71\n22\n52\n64\n', '16 700\n61\n8\n47\n80\n54\n80\n13\n100\n20\n66\n70\n23\n21\n57\n45\n1\n', '11 332\n46\n85\n93\n46\n63\n61\n44\n70\n3\n63\n85\n', '20 608\n76\n77\n6\n93\n64\n10\n60\n41\n23\n54\n6\n25\n72\n34\n75\n67\n77\n74\n48\n30\n', '12 505\n51\n78\n14\n47\n25\n25\n21\n91\n20\n19\n87\n28\n', '5 43\n18\n11\n16\n67\n47\n', '8 250\n34\n58\n21\n9\n1\n28\n94\n7\n', '13 199\n54\n80\n26\n73\n64\n47\n1\n75\n81\n6\n61\n59\n84\n', '15 252\n43\n51\n43\n33\n45\n79\n53\n39\n24\n96\n76\n77\n41\n99\n1\n', '27 630\n37\n30\n16\n32\n73\n26\n7\n92\n41\n42\n35\n85\n43\n81\n81\n100\n31\n23\n28\n41\n87\n19\n75\n48\n67\n10\n31\n', '24 321\n28\n81\n98\n70\n26\n27\n63\n35\n96\n77\n76\n81\n34\n96\n77\n94\n39\n70\n82\n68\n14\n86\n29\n4\n', '12 257\n18\n62\n80\n76\n24\n82\n67\n73\n31\n19\n37\n28\n', '5 122\n63\n41\n73\n37\n7\n']
REFERENCE_SOURCE = '# 蒋子轩23工学院\ndef min_cows_to_reach(N, B):\n\t# 二分查找变形，找大于等于B的最小索引\n    left, right = 1, N\n    while left < right:  #注意不能取等\n        mid = (left + right) // 2 #左偏\n        if prefix_sum[mid]>=B:  #等于时继续向左找\n            right = mid   #注意不-1，\n        else:\n            left = mid + 1\n    return left  #return不取等的那个\nN, B = map(int, input().split())\ncows = [int(input()) for _ in range(N)]\n#优先选择高的\ncows.sort(reverse=True)\n#计算前缀和\nprefix_sum = [0] * (len(cows) + 1)\nfor i in range(1, len(cows)+1):\n    prefix_sum[i] = prefix_sum[i-1] + cows[i-1]\nprint(min_cows_to_reach(N, B))\n'
assert SAMPLE_IN.strip()
assert SAMPLE_OUT.strip()
random.seed(3406)
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
