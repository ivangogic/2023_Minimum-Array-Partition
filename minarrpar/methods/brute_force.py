import random
import numpy as np
from random import shuffle
from itertools import combinations, product
from tqdm.notebook import tqdm, trange
from minarrpar.common.instance import Instance


def bf(instance: Instance):
    result = float('inf')
    result_h, result_v = [], []
    combs = list(combinations(range(1, instance.n), instance.p - 1))
    combs_h = [[0] + list(comb) + [instance.n] for comb in combs]
    combs_v = [[0] + list(comb) + [instance.n] for comb in combs]
    random.shuffle(combs_h)
    random.shuffle(combs_v)
    total_combinations = len(combs) ** 2
    total_sum = np.sum(instance.matrix)
    total_block_count = instance.p ** 2

    for (comb_h, comb_v) in tqdm(product(combs_h, combs_v), total=total_combinations):
        curr = 0
        visited_block_count = 0
        visited_block_sum = 0
        for i in range(instance.p):
            for j in range(instance.p):
                b_h = (comb_h[i], comb_h[i + 1] - 1)
                b_v = (comb_v[j], comb_v[j + 1] - 1)
                block_value = instance.calc_block_value(b_h, b_v)
                visited_block_sum += block_value
                visited_block_count += 1
                if result < block_value:
                    break
                if result < (total_sum - visited_block_sum) / max(total_block_count - visited_block_count, 1):
                    break
                curr = max(curr, block_value)
            else:
                continue
            break
        else:
            result = min(curr, result)

        if result == curr:
            result_h, result_v = comb_h, comb_v

    print('--------------------')
    print(f'h = {list(result_h)}')
    print(f'v = {list(result_v)}')
    print(f'result = {result}')
