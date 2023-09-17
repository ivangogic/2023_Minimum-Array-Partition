import numpy as np


class Instance:

    def __init__(self, file: str):
        with open(file, 'r') as data:
            n, p, *matrix_lines = data.readlines()
            self.n = int(n)
            self.p = int(p)
            self.matrix = np.array([
                [int(cell) for cell in row.split()]
                for row in matrix_lines
            ])

    def __repr__(self):
        result = ''
        result += f'n = {self.n}\n'
        result += f'p = {self.p}\n'
        result += '\n'.join([
            ' '.join(map(str, row))
            for row in self.matrix
        ])
        return result

    def __getitem__(self, item):
        return self.matrix[item]
