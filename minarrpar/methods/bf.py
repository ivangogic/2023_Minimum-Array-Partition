import numpy as np
from itertools import combinations, product
from tqdm.notebook import tqdm
from minarrpar.common.instance import Instance


def bf(instance: Instance):
    result = float('inf')
    result_h, result_v = [], []
    combs = combinations(range(1, instance.n), instance.p - 1)
    combs = [[0] + list(comb) + [instance.n] for comb in list(combs)]
    print(f'Number of combinations: {len(combs) ** 2}')

    dp = np.empty(shape=instance.matrix.shape)
    dp[0][0] = instance.matrix[0][0]
    for i in range(0, dp.shape[0]):
        dp[i][0] = instance.matrix[i][0] + dp[i - 1][0]
        dp[0][i] = instance.matrix[0][i] + dp[0][i - 1]
    for i in range(1, dp.shape[0]):
        for j in range(1, dp.shape[1]):
            dp[i][j] = instance.matrix[i][j] + dp[i - 1][j] + dp[i][j - 1] - dp[i - 1][j - 1]

    iteration = 0
    for (comb_h, comb_v) in tqdm(list(product(combs, combs))):
        curr = 0
        for i in range(len(comb_h) - 1):
            for j in range(len(comb_v) - 1):
                curr = max(calc(dp, (comb_h[i], comb_h[i + 1] - 1), (comb_v[j], comb_v[j + 1] - 1)), curr)
        result = min(curr, result)

        if result == curr:
            result_h, result_v = comb_h, comb_v
        
        if iteration % 1000 == 0:
            print(result)
        iteration += 1

    print()
    print(result)
    print(result_h)
    print(result_v)


def calc(m, b_h, b_v):
    h0, h1 = b_h[0], b_h[1]
    v0, v1 = b_v[0], b_v[1]

    r = m[h1][v1]
    if 0 < h0:
        r -= m[h0 - 1][v1]
    if 0 < v0:
        r -= m[h1][v0 - 1]
    if 0 < h0 and 0 < v0:
        r += m[h0 - 1][v0 - 1]
    
    return r
