from itertools import combinations, product
from tqdm.notebook import tqdm
from minarrpar.common.instance import Instance


def bf(instance: Instance, verbose=False):
    result = float('inf')
    result_h, result_v = [], []
    combs = combinations(range(1, instance.n), instance.p - 1)
    combs = [[0] + list(comb) + [instance.n] for comb in list(combs)]

    iteration = 0
    for (comb_h, comb_v) in tqdm(list(product(combs, combs))):
        curr = 0
        for i in range(len(comb_h) - 1):
            for j in range(len(comb_v) - 1):
                b_h = (comb_h[i], comb_h[i + 1] - 1)
                b_v = (comb_v[j], comb_v[j + 1] - 1)
                curr = max(curr, instance.calc_block_value(b_h, b_v))
        result = min(curr, result)

        if result == curr:
            result_h, result_v = comb_h, comb_v
        
        if verbose and iteration % 1000 == 0:
            # print(result)
            num_iters = len(combs) ** 2
            padding = len(str(num_iters))
            print(f'{iteration:>{padding}} / {num_iters} : curr_result={result}')
        iteration += 1

    print(f'----------\n{result_h = }\n{result_v = }\n{result = }')
