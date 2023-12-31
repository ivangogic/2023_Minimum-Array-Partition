from random import sample, shuffle
import numpy as np
from minarrpar.common.instance import Instance


class Solution:

    def __init__(self, instance: Instance, h=None, v=None):
        self.instance = instance
        self.n = instance.n
        self.p = instance.p
        self.h = np.array(list(h) if h else self.__generate_dividers())
        self.v = np.array(list(v) if v else self.__generate_dividers())
        self.name = instance.name

    def __repr__(self):
        return (
                f'Solution(\n' +
                f'  h = {self.h}\n' +
                f'  v = {self.v}\n' +
                f'  result = {self.value()}\n' +
                f')'
        )

    def __generate_dividers(self):
        return sorted(sample(range(1, self.n), self.p - 1) + [0, self.n])

    def __block_value(self, h: (int, int), v: (int, int)) -> int:
        return self.instance.calc_block_value(h, v)

    def value(self) -> int:
        largest = 0
        for i in range(0, self.p):
            for j in range(0, self.p):
                h = (self.h[j], self.h[j + 1] - 1)
                v = (self.v[i], self.v[i + 1] - 1)
                current = self.__block_value(h, v)
                largest = max(largest, current)
        return int(largest)

    def make_small_change(self):
        choices = []

        for i in range(1, self.p):
            if self.h[i] - 1 > self.h[i - 1]:
                choices.append((0, i, -1))
            if self.h[i] + 1 < self.h[i + 1]:
                choices.append((0, i, 1))
            if self.v[i] - 1 > self.v[i - 1]:
                choices.append((1, i, -1))
            if self.v[i] + 1 < self.v[i + 1]:
                choices.append((1, i, 1))

        shuffle(choices)
        return choices

    def fix(self):
        unique = set(self.v)
        duplicate = len(self.v) - len(unique)
        choices = set(range(1, self.n)).difference(unique)
        part = sorted(list(unique) + sample(list(choices), duplicate))
        self.v = np.array(part)

        unique = set(self.h)
        duplicate = len(self.h) - len(unique)
        choices = set(range(1, self.n)).difference(unique)
        part = sorted(list(unique) + sample(list(choices), duplicate))
        self.h = np.array(part)
