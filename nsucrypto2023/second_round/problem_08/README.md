# Problem 08 - Algebraic cryptanalysis

I generated all the symbolic representations, using
sympy. The random number generator has a period of 63. The seed is given by
k0, k1, k2, ..., k7. Its 63 terms are:
```
k7 ^ (k0 & k2)
k0 ^ k7 ^ (k1 & k3)
k0 ^ k1 ^ k7 ^ (k2 & k4)
k0 ^ k1 ^ k2 ^ k7 ^ (k3 & k5)
k0 ^ k1 ^ k2 ^ k3 ^ k7 ^ (k4 & k6)
k0 ^ k1 ^ k2 ^ k3 ^ k4 ^ k7 ^ (k5 & k7)
k0 ^ k1 ^ k2 ^ k3 ^ k4 ^ k5 ^ k7 ^ (k6 & (k0 ^ k7))
k0 ^ k1 ^ k2 ^ k3 ^ k4 ^ k5 ^ k6 ^ k7 ^ (k7 & (k0 ^ k1 ^ k7))
k0 ^ k1 ^ k2 ^ k3 ^ k4 ^ k5 ^ k6 ^ ((k0 ^ k7) & (k0 ^ k1 ^ k2 ^ k7))
k1 ^ k2 ^ k3 ^ k4 ^ k5 ^ k6 ^ k7 ^ ((k0 ^ k1 ^ k7) & (k0 ^ k1 ^ k2 ^ k3 ^ k7))
k0 ^ k2 ^ k3 ^ k4 ^ k5 ^ k6 ^ ((k0 ^ k1 ^ k2 ^ k7) & (k0 ^ k1 ^ k2 ^ k3 ^ k4 ^ k7))
k1 ^ k3 ^ k4 ^ k5 ^ k6 ^ k7 ^ ((k0 ^ k1 ^ k2 ^ k3 ^ k7) & (k0 ^ k1 ^ k2 ^ k3 ^ k4 ^ k5 ^ k7))
k0 ^ k2 ^ k4 ^ k5 ^ k6 ^ ((k0 ^ k1 ^ k2 ^ k3 ^ k4 ^ k7) & (k0 ^ k1 ^ k2 ^ k3 ^ k4 ^ k5 ^ k6 ^ k7))
k1 ^ k3 ^ k5 ^ k6 ^ k7 ^ ((k0 ^ k1 ^ k2 ^ k3 ^ k4 ^ k5 ^ k6) & (k0 ^ k1 ^ k2 ^ k3 ^ k4 ^ k5 ^ k7))
k0 ^ k2 ^ k4 ^ k6 ^ ((k1 ^ k2 ^ k3 ^ k4 ^ k5 ^ k6 ^ k7) & (k0 ^ k1 ^ k2 ^ k3 ^ k4 ^ k5 ^ k6 ^ k7))
k1 ^ k3 ^ k5 ^ k7 ^ ((k0 ^ k2 ^ k3 ^ k4 ^ k5 ^ k6) & (k0 ^ k1 ^ k2 ^ k3 ^ k4 ^ k5 ^ k6))
k0 ^ k2 ^ k4 ^ k6 ^ k7 ^ ((k1 ^ k3 ^ k4 ^ k5 ^ k6 ^ k7) & (k1 ^ k2 ^ k3 ^ k4 ^ k5 ^ k6 ^ k7))
k0 ^ k1 ^ k3 ^ k5 ^ ((k0 ^ k2 ^ k4 ^ k5 ^ k6) & (k0 ^ k2 ^ k3 ^ k4 ^ k5 ^ k6))
k1 ^ k2 ^ k4 ^ k6 ^ ((k1 ^ k3 ^ k5 ^ k6 ^ k7) & (k1 ^ k3 ^ k4 ^ k5 ^ k6 ^ k7))
k2 ^ k3 ^ k5 ^ k7 ^ ((k0 ^ k2 ^ k4 ^ k6) & (k0 ^ k2 ^ k4 ^ k5 ^ k6))
k0 ^ k3 ^ k4 ^ k6 ^ k7 ^ ((k1 ^ k3 ^ k5 ^ k7) & (k1 ^ k3 ^ k5 ^ k6 ^ k7))
k0 ^ k1 ^ k4 ^ k5 ^ ((k0 ^ k2 ^ k4 ^ k6) & (k0 ^ k2 ^ k4 ^ k6 ^ k7))
k1 ^ k2 ^ k5 ^ k6 ^ ((k0 ^ k1 ^ k3 ^ k5) & (k1 ^ k3 ^ k5 ^ k7))
k2 ^ k3 ^ k6 ^ k7 ^ ((k1 ^ k2 ^ k4 ^ k6) & (k0 ^ k2 ^ k4 ^ k6 ^ k7))
k0 ^ k3 ^ k4 ^ ((k0 ^ k1 ^ k3 ^ k5) & (k2 ^ k3 ^ k5 ^ k7))
k1 ^ k4 ^ k5 ^ ((k1 ^ k2 ^ k4 ^ k6) & (k0 ^ k3 ^ k4 ^ k6 ^ k7))
k2 ^ k5 ^ k6 ^ ((k0 ^ k1 ^ k4 ^ k5) & (k2 ^ k3 ^ k5 ^ k7))
k3 ^ k6 ^ k7 ^ ((k1 ^ k2 ^ k5 ^ k6) & (k0 ^ k3 ^ k4 ^ k6 ^ k7))
k0 ^ k4 ^ ((k0 ^ k1 ^ k4 ^ k5) & (k2 ^ k3 ^ k6 ^ k7))
k1 ^ k5 ^ ((k0 ^ k3 ^ k4) & (k1 ^ k2 ^ k5 ^ k6))
k2 ^ k6 ^ ((k1 ^ k4 ^ k5) & (k2 ^ k3 ^ k6 ^ k7))
k3 ^ k7 ^ ((k0 ^ k3 ^ k4) & (k2 ^ k5 ^ k6))
k0 ^ k4 ^ k7 ^ ((k1 ^ k4 ^ k5) & (k3 ^ k6 ^ k7))
k0 ^ k1 ^ k5 ^ k7 ^ ((k0 ^ k4) & (k2 ^ k5 ^ k6))
k0 ^ k1 ^ k2 ^ k6 ^ k7 ^ ((k1 ^ k5) & (k3 ^ k6 ^ k7))
k0 ^ k1 ^ k2 ^ k3 ^ ((k0 ^ k4) & (k2 ^ k6))
k1 ^ k2 ^ k3 ^ k4 ^ ((k1 ^ k5) & (k3 ^ k7))
k2 ^ k3 ^ k4 ^ k5 ^ ((k2 ^ k6) & (k0 ^ k4 ^ k7))
k3 ^ k4 ^ k5 ^ k6 ^ ((k3 ^ k7) & (k0 ^ k1 ^ k5 ^ k7))
k4 ^ k5 ^ k6 ^ k7 ^ ((k0 ^ k4 ^ k7) & (k0 ^ k1 ^ k2 ^ k6 ^ k7))
k0 ^ k5 ^ k6 ^ ((k0 ^ k1 ^ k2 ^ k3) & (k0 ^ k1 ^ k5 ^ k7))
k1 ^ k6 ^ k7 ^ ((k1 ^ k2 ^ k3 ^ k4) & (k0 ^ k1 ^ k2 ^ k6 ^ k7))
k0 ^ k2 ^ ((k0 ^ k1 ^ k2 ^ k3) & (k2 ^ k3 ^ k4 ^ k5))
k1 ^ k3 ^ ((k1 ^ k2 ^ k3 ^ k4) & (k3 ^ k4 ^ k5 ^ k6))
k2 ^ k4 ^ ((k2 ^ k3 ^ k4 ^ k5) & (k4 ^ k5 ^ k6 ^ k7))
k3 ^ k5 ^ ((k0 ^ k5 ^ k6) & (k3 ^ k4 ^ k5 ^ k6))
k4 ^ k6 ^ ((k1 ^ k6 ^ k7) & (k4 ^ k5 ^ k6 ^ k7))
k5 ^ k7 ^ ((k0 ^ k2) & (k0 ^ k5 ^ k6))
k0 ^ k6 ^ k7 ^ ((k1 ^ k3) & (k1 ^ k6 ^ k7))
k0 ^ k1 ^ ((k0 ^ k2) & (k2 ^ k4))
k1 ^ k2 ^ ((k1 ^ k3) & (k3 ^ k5))
k2 ^ k3 ^ ((k2 ^ k4) & (k4 ^ k6))
k3 ^ k4 ^ ((k3 ^ k5) & (k5 ^ k7))
k4 ^ k5 ^ ((k4 ^ k6) & (k0 ^ k6 ^ k7))
k5 ^ k6 ^ ((k0 ^ k1) & (k5 ^ k7))
k6 ^ k7 ^ ((k1 ^ k2) & (k0 ^ k6 ^ k7))
k0 ^ ((k0 ^ k1) & (k2 ^ k3))
k1 ^ ((k1 ^ k2) & (k3 ^ k4))
k2 ^ ((k2 ^ k3) & (k4 ^ k5))
k3 ^ ((k3 ^ k4) & (k5 ^ k6))
k4 ^ ((k4 ^ k5) & (k6 ^ k7))
k5 ^ (k0 & (k5 ^ k6))
k6 ^ (k1 & (k6 ^ k7))
```

## Solution

The solution is in solve.py.

In our case, 1200 are lost. So, we know the 1201st bit, and the next 7. Since
the period is 63, it means we actually know the 4th bit and the next 7. This
means the known bits "00100001", are generated from equations 4 to 11, above.
Bruteforcing the seed for the given equations, gives us two solutions:

    [0, 0, 1, 1, 1, 1, 0, 0]
    [0, 1, 1, 0, 1, 1, 0, 0]


So, the key can't be completly recovered from those 8 bits. The sequences
generated from the above two seeds, differ in 23 bits out of 63.
