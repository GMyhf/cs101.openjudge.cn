"""仓库自产参考：只去掉行末换行，保留字符串其余字符；非外部提交。"""
def solve(text):
    return text[:-2] if text.endswith('\r\n') else text[:-1] if text.endswith('\n') else text

if __name__=='__main__':
    import sys
    sys.stdout.write(solve(sys.stdin.read())+'\n')
