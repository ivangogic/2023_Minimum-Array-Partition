import random
from copy import deepcopy
from tqdm.notebook import tqdm
from minarrpar.common.instance import Instance
from minarrpar.common.solution import Solution


def sa(instance: Instance, num_iters, disabled_pbar=True):
    solution = Solution(instance)
    value = solution.value()
    best_solution = [deepcopy(solution.h), deepcopy(solution.v)]
    best_value = value

    for i in tqdm(range(1, num_iters + 1), disable=disabled_pbar):
        new_choices = solution.make_small_change()

        for choice in new_choices:
            if choice[0] == 0:
                solution.h[choice[1]] += choice[2]
            else:
                solution.v[choice[1]] += choice[2]

            new_value = solution.value()

            if new_value < value:
                value = new_value

                if new_value < best_value:
                    best_value = new_value
                    best_solution[0], best_solution[1] = deepcopy(solution.h), deepcopy(solution.v)

                break

            else:
                p = 1 / i ** 0.5
                q = random.random()
                if q < p:
                    value = new_value
                else:
                    if choice[0] == 0:
                        solution.h[choice[1]] -= choice[2]
                    else:
                        solution.v[choice[1]] -= choice[2]

    # print('--------------------')
    # print(f'h = {list(best_solution[0])}')
    # print(f'v = {list(best_solution[1])}')
    # print(f'result = {best_value}')

    return Solution(instance, list(best_solution[0]), list(best_solution[1]))


def shake(solution, choices, k):
    chosen = random.sample(range(len(choices)), k)
    for resource in chosen:
        if choices[resource][0] == 0:
            solution.h[choices[resource][1]] += choices[resource][2]
        else:
            solution.v[choices[resource][1]] += choices[resource][2]

    return chosen


def revert(solution, choices, chosen):
    for resource in chosen:
        if choices[resource][0] == 0:
            solution.h[choices[resource][1]] -= choices[resource][2]
        else:
            solution.v[choices[resource][1]] -= choices[resource][2]


def vns(instance: Instance, num_iters, k_max, move_prob, disabled_pbar=True):
    solution = Solution(instance)
    value = solution.value()

    for _ in tqdm(range(1, num_iters + 1), disable=disabled_pbar):
        new_choices = solution.make_small_change()
        k_curr = min(k_max, len(new_choices))

        for k in range(1, k_curr + 1):
            choice = shake(solution, new_choices, k)
            new_value = solution.value()

            if new_value < value or (new_value == value and random.random() < move_prob):
                value = new_value
                break
            else:
                revert(solution, new_choices, choice)

    # print('--------------------')
    # print(f'h = {list(solution.h)}')
    # print(f'v = {list(solution.v)}')
    # print(f'result = {value}')

    return solution
