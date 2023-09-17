# Minimum Array Partition

### Problem statement

> [NP compendium entry](https://www.csc.kth.se/tcs/compendium/node156.html)

Given a $n \times n$ array $A$ of non-negative integers, and a positive integer $p$, choose
$p - 1$ horizontal dividers $0 = h_0 < h_1 < \dots < h_p = n$ and 
$p - 1$ vertical dividers $0 = v_0 < v_1 < \dots < v_p = n$
partitioning $A$ into $p^2$ blocks, so as to minimize the following expression:
```math
\max_{\substack{1 \leq i \leq p \\ 1 \leq j \leq p}} \enspace
\sum_{\substack{v_{i-1} \leq x \leq v_i \\ h_{j-1} \leq y \leq h_j}}
A[x, y]
```

### Required libraries

> Python 3.6+

- `jupyter`
- `numpy`
- `tqdm` (for progress bars)
