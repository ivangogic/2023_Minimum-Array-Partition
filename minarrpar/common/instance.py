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
        self.name = file

        dp = np.empty(shape=self.matrix.shape)
        dp[0][0] = self.matrix[0][0]
        for i in range(0, dp.shape[0]):
            dp[i][0] = self.matrix[i][0] + dp[i - 1][0]
            dp[0][i] = self.matrix[0][i] + dp[0][i - 1]
        for i in range(1, dp.shape[0]):
            for j in range(1, dp.shape[1]):
                dp[i][j] = self.matrix[i][j] + dp[i - 1][j] + dp[i][j - 1] - dp[i - 1][j - 1]
        self.dp = dp

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

    def calc_block_value(self, b_h, b_v) -> int:
        h0, h1 = b_h[0], b_h[1]
        v0, v1 = b_v[0], b_v[1]

        r = self.dp[h1][v1]
        if 0 < h0:
            r -= self.dp[h0 - 1][v1]
        if 0 < v0:
            r -= self.dp[h1][v0 - 1]
        if 0 < h0 and 0 < v0:
            r += self.dp[h0 - 1][v0 - 1]

        return r
