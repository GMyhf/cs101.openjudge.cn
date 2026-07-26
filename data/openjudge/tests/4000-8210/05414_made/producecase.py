import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = 'def build_preorder(inorder, postorder):\n    if not inorder or not postorder:\n        return []\n\n    root = postorder[-1]  # 后序遍历的最后一个节点是根节点\n    root_index = inorder.index(root)  # 在中序遍历中找到根节点\n\n    # 递归构造左子树和右子树的前序遍历\n    left_preorder = build_preorder(inorder[:root_index], postorder[:root_index])\n    right_preorder = build_preorder(inorder[root_index + 1:], postorder[root_index:-1])\n\n    return [root] + left_preorder + right_preorder \n\n\ninorder = list(map(int, input().split())) \npostorder = list(map(int, input().split()))  \npreorder = build_preorder(inorder, postorder)\nprint(*preorder)'
SAMPLE = '9 5 32 67\n9 32 67 5\n'
GENERATOR_NAME = 'g5414'
def g5414(r):
    z=r.sample(range(65535),r.randint(2,10))
    def walk(a):
        if not a: return [],[],[]
        l,i,_=walk(a[1::2]); rr,p,_=walk(a[2::2])
        return l+[a[0]]+rr,i+p+[a[0]],[a[0]]+i+p
    i,p,_=walk(z)
    return " ".join(map(str,i))+"\n"+" ".join(map(str,p))+"\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"
        p.write_text(REFERENCE, encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text, encoding="utf-8")
        (data/f"{i}.out").write_text(run(text), encoding="utf-8")
if __name__=="__main__": main()
