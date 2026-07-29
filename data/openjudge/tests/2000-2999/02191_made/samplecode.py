# External reference: http://cs101.openjudge.cn/practice/02191/statistics/
# Accepted submission: 51717401
# Source: http://cs101.openjudge.cn/practice/solution/51717401/
# License: not declared on the submission page; no license is inferred.

l = [(11, '23 * 89'), (23, '47 * 178481'), (29, '233 * 1103 * 2089'), (37, '223 * 616318177'), (41, '13367 * 164511353'), (43, '431 * 9719 * 2099863'), (47, '2351 * 4513 * 13264529'), (53, '6361 * 69431 * 20394401'), (59, '179951 * 3203431780337')]
k = int(input())
for p, line in l:
    if p > k:
        break
    print(f'{line} = {2**p-1} = ( 2 ^ {p} ) - 1')
