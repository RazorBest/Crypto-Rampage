import galois
from numpy.linalg import matrix_power
from itertools import accumulate
from primefac import primefac

def group_factors(factors):
    mapped_factors = {}
    for x in factors:
        if x not in mapped_factors:
            mapped_factors[x] = 0
        mapped_factors[x] += 1

    return mapped_factors


p = 127
GF = galois.GF(p)
M = GF([[117, 99, 48], [8, 67, 122], [29, 103, 82]])
n = len(M)
lim = n * (n - 1) // 2

# The order of the group is p^(n(n-1)/2) * PROD((p^i - 1) for i in range(1, n))
# Factorize the order
N = p**lim
for i in range(1, n + 1):
    N *= (p**i - 1)

factors = primefac(N)
factors = group_factors(factors)

ord_fact = {}
for fact, cnt in factors.items():
    is_identity = True
    ord_fact[fact] = 0
    for i in range(1, cnt + 1):
        e = N // (fact**i)
        Mp = matrix_power(M, e)
        is_identity = True
        for j in range(len(Mp)):
            if Mp[j][j] != 1:
                is_identity = False
                break

        if not is_identity:
            ord_fact[fact] = cnt - i + 1
            break

order = 1
for fact, cnt in ord_fact.items():
    order *= fact**cnt

print(f"Order: {order}")
