# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# 数学科学学院 王镜廷 2300010724
def find_leftmost_node(son, u):
    while son[u][0] != -1:
        u = son[u][0]
    return u

def main():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())

        son = [-1] * (n + 1)  # 存储每个节点的子节点
        parent = {}  # 存储每个节点的父节点和方向，{节点: (父节点, 方向)}

        for _ in range(n):
            i, u, v = map(int, input().split())
            son[i] = [u, v]
            parent[u] = (i, 0)  # 左子节点
            parent[v] = (i, 1)  # 右子节点

        for _ in range(m):
            s = input().split()
            if s[0] == "1":
                u, v = map(int, s[1:])
                fu, diru = parent[u]
                fv, dirv = parent[v]
                son[fu][diru] = v
                son[fv][dirv] = u
                parent[v] = (fu, diru)
                parent[u] = (fv, dirv)
            elif s[0] == "2":
                u = int(s[1])
                root = find_leftmost_node(son, u)
                print(root)

if __name__ == "__main__":
    main()
