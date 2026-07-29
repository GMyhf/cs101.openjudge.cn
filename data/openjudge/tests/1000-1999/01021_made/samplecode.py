# External reference: http://cs101.openjudge.cn/practice/01021/statistics/
# Accepted submission: 48421084
# Source: http://cs101.openjudge.cn/practice/solution/48421084/
# License: not declared on the submission page; no license is inferred.

import sys
from collections import deque

def find_clusters(points):
    visited = set()
    clusters = []
    points = set(points)
    for point in points:
        if point not in visited:
            queue = deque()
            queue.append(point)
            visited.add(point)
            cluster = []
            while queue:
                x, y = queue.popleft()
                cluster.append((x, y))
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    neighbor = (x + dx, y + dy)
                    if neighbor in points and neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            clusters.append(cluster)
    return clusters

def get_feature(cluster):
    transforms = [
        lambda x, y: (x, y),
        lambda x, y: (y, -x),
        lambda x, y: (-x, -y),
        lambda x, y: (-y, x),
        lambda x, y: (-x, y),
        lambda x, y: (y, x),
        lambda x, y: (x, -y),
        lambda x, y: (-y, -x),
    ]
    min_feature = None
    for t in transforms:
        transformed = [t(x, y) for x, y in cluster]
        min_x = min(p[0] for p in transformed)
        min_y = min(p[1] for p in transformed)
        normalized = [(p[0] - min_x, p[1] - min_y) for p in transformed]
        normalized.sort()
        feature = tuple(normalized)
        if (min_feature is None) or (feature < min_feature):
            min_feature = feature
    return min_feature

def main():
    t = int(sys.stdin.readline())
    for _ in range(t):
        W, H, n = map(int, sys.stdin.readline().split())
        points1 = list(map(int, sys.stdin.readline().split()))
        points1 = [(points1[i], points1[i+1]) for i in range(0, 2*n, 2)]
        points2 = list(map(int, sys.stdin.readline().split()))
        points2 = [(points2[i], points2[i+1]) for i in range(0, 2*n, 2)]
        clusters1 = find_clusters(points1)
        clusters2 = find_clusters(points2)
        features1 = [get_feature(cluster) for cluster in clusters1]
        features2 = [get_feature(cluster) for cluster in clusters2]
        features1.sort()
        features2.sort()
        print("YES" if features1 == features2 else "NO")

if __name__ == "__main__":
    main()
