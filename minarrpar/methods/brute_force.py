import random
import numpy as np
from random import shuffle
from itertools import combinations, product
from tqdm.notebook import tqdm
from minarrpar.common.instance import Instance
from minarrpar.common.solution import Solution


def bf(instance: Instance, disabled_pbar=True):
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
    evaluated_blocks = 0

    for (comb_h, comb_v) in tqdm(product(combs_h, combs_v), total=total_combinations, disable=disabled_pbar):
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
            if result > curr:
                result = curr
                result_h, result_v = comb_h, comb_v

        evaluated_blocks += visited_block_count

    # percentage_cut = 100 * (1 - evaluated_blocks / (total_block_count * total_combinations))
    # print(f'{percentage_cut:.2f}% cut')

    # print('--------------------')
    # print(f'h = {list(result_h)}')
    # print(f'v = {list(result_v)}')
    # print(f'result = {result}')

    return Solution(instance, list(result_h), list(result_v))
