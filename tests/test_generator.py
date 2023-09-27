import random
import sys

"""
Run the script like this from the tests folder:
    python test_generator.py n p function
where function is one of the generator function keys below:
"""

generators = {
    'ones' : lambda r, c: 1,
    'random' : lambda r, c: random.randint(1, n//2),
    'linear' : lambda r, c: r+c+1,
    'squared' : lambda r, c: r**2+c**2+1
}

n, p = map(int, sys.argv[1:3])
g = sys.argv[3]

matrix = [
    [
        generators[g](row, col)
        for col in range(n)
    ]
    for row in range(n)
]

with open(f'{g}_n{n}_p{p}.in', 'w') as file:
    file.write(f'{n}\n')
    file.write(f'{p}\n')
    
    M = max(map(max, matrix))
    w = len(str(M))

    for row in matrix:
        for cell in row:
            file.write(str(cell).rjust(w+1, ' '))
        file.write('\n')
