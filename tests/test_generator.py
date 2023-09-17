import random
import sys

n, p = map(int, sys.argv[1:3])

# n = int(input("n = "))
# p = int(input("p = "))

matrix = [
    [
        random.randrange(1, 11)
        for col in range(n)
    ]
    for row in range(n)
]

with open(f'generated_n{n}_p{p}.in', 'w') as file:
    file.write(f'{n}\n')
    file.write(f'{p}\n')
    for row in matrix:
        for cell in row:
            file.write(str(cell).rjust(3, ' '))
        file.write('\n')
