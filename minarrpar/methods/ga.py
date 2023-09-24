import random
import numpy as np
from copy import deepcopy
from tqdm.notebook import tqdm
from minarrpar.common.instance import Instance
from minarrpar.common.solution import Solution


class Individual(Solution):

    def __init__(self, instance: Instance):
        super().__init__(instance, h=None, v=None)
        self.fitness = self.calc_fitness()

    def calc_fitness(self):
        return 1 / self.value()


def selection(population, tournament_size, forbidden=None):
    allowed = list(set(range(len(population))).difference({forbidden}))
    chosen = random.sample(allowed, tournament_size)
    max_fitness = float('-inf')
    best_idx = -1
    for i in chosen:
        if population[i].fitness > max_fitness:
            max_fitness = population[i].fitness
            best_idx = i
    return best_idx


def mutation(child: Individual, mutation_prob):
    for partition in [child.h, child.v]:
        for i in range(1, child.p):
            choices = []
            if partition[i] - 1 > partition[i - 1]:
                choices.append((i, -1))
            if partition[i] + 1 < partition[i + 1]:
                choices.append((i, 1))
            if choices and random.random() < mutation_prob:
                idx, delta = random.choice(choices)
                partition[idx] = partition[idx] + delta


def crossover(parent1: Individual, parent2: Individual, child: Individual):
    child.h = np.array(list(map(lambda x: round(x + random.choice([-0.1, 0.1])), (parent1.h + parent2.h) / 2)))
    child.v = np.array(list(map(lambda x: round(x + random.choice([-0.1, 0.1])), (parent1.v + parent2.v) / 2)))


def ga(instance: Instance, pop_size, num_iters, tournament_size, mutation_prob, elitism_size=0, verbose=False):
    if elitism_size > 0 and (pop_size - elitism_size) % 2 == 1:
        elitism_size += 1

    population = [Individual(instance) for _ in range(pop_size)]
    new_population = [Individual(instance) for _ in range(pop_size)]

    for iteration in tqdm(range(num_iters)):
        if elitism_size > 0:
            population.sort(key=lambda x: x.fitness, reverse=True)
            new_population[:elitism_size] = deepcopy(population[:elitism_size])

        for i in range(elitism_size, pop_size):
            parent1_idx = selection(population, tournament_size)
            parent2_idx = selection(population, tournament_size, forbidden=parent1_idx)

            crossover(population[parent1_idx],
                      population[parent2_idx],
                      new_population[i])

            mutation(new_population[i], mutation_prob * (num_iters - iteration/2) / num_iters)

            new_population[i].fitness = new_population[i].calc_fitness()

        population = deepcopy(new_population)

        # display progress
        if verbose:
            best = max(population, key=lambda x: x.fitness)
            prob = mutation_prob * (num_iters - iteration/2) / num_iters
            padding = len(str(num_iters))
            print(f'{iteration:>{padding}} / {num_iters} : mutation_prob={prob:.2f} best_value={best.value()}')

    best_individual = max(population, key=lambda x: x.fitness)
    h = best_individual.h
    v = best_individual.v
    value = best_individual.value()

    print('--------------------')
    print(f'h = {list(h)}')
    print(f'v = {list(v)}')
    print(f'result = {value}')
