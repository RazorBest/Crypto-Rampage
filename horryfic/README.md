# Horryfic 

- CTF: CyDEx 2023
- difficulty: medium
- tags: elliptic curves, equations, blockwise bruteforce

## Writeup

We are given the script `ElSamal.py`, which generates a key and encrypts
the flag with AES. The script outputs the encrypted flag, and also `x*y`, where
`x` and `y` are the parameters used to generate the key. The key is a hash of
the x coordinate of a point on the curve. The `generate_key` method returns
some parameters `x` (integer) and `P` (point on the curve). The actual key
supposedly being `x * P`. A more thourough inspection of the source code 
reveals that a bug has been planted after calling `generate_key`:
```python
def generate_key():
    ...
    return (x,y,Q,P)

def encrypt():
    x,y,P,Q = self.generate_key()
    key = x * P
```

We can observe that `P` and `Q` have been swapped in the function `encrypt`.
So, `key = x * (x * P256.G) = (x * x) * P256.G`, where P256.G is a generator of
the P-256 curve. Here, the multiplication operation has two meanings, depending
on the operands. Since x is an integer, we permform the first multiplication
in the integer space. But P256.G is a curve point, so x * P256.G means adding
P256.G to itself x times (in the elliptic curve group).

We are given `prod = x*y`, which is `x * (x ^ (P256.q + C))`, where P256.q is
the order of the P-256 curve and C is a constant in the source code. So we have
to solve:
```
    x * (x ^ (P256.q + C)) = prod
```

The above equation is true even in modular arithmetic, when N=2^k.
```
    x * (x ^ (P256.q + C)) = prod (mod N)
```

So, we can construct a system of equations that can be solved incrementally:
```
    x * (x ^ (P256.q + C)) = prod (mod 2)
    x * (x ^ (P256.q + C)) = prod (mod 4)
    x * (x ^ (P256.q + C)) = prod (mod 8)
    x * (x ^ (P256.q + C)) = prod (mod 16)
    ...
```

Where, at each new equation, we find a new bit of x. The equations are not
linear, and in some cases, there might be multiple solutions for x, in a given
equation. Experminatally, I determined that, instead of bruteforcing one bit
at a time, doing the same thing 4 bits at a time (16 possibilities) seemed to
lead to a single solution.

The solution is in `solve.py`. The flag is:
CYDEX{bdba2eaf6e94fbd0f277647b68f7e358a1c493234f805d5d8e742a034366d654}
