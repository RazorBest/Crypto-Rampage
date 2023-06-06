# polyRSA

- CTF: cryptoctf2022 - https://ctftime.org/event/1573
- difficulty: easy
- tags: galois field, matrix, groups, math

## Writeup

We are given a group GL(p, n) which represents the set of inversible nxn
matrices that have elements in GF(p). Given a matrix M from that group,
we are required to compute the order of M wihtin the group.

The problem of finding the order of element in a group is not an easy one.
But, it can be solved as long as we know the size of the group. We can
use Lagrange's theorem to prove that the order of M divides N, the order
of the group. This simplifies our search because we only haave to look
through the divisors of N.

Iterating through the divisors of N is still very slow. What we do instead,
is try to find which prime factors of N are found within ord(M).

Sage also has a function for computing the order.

References:
- https://yutsumura.com/group-of-invertible-matrices-over-a-finite-field-and-its-stabilizer/
- https://en.wikipedia.org/wiki/Lagrange%27s_theorem_(group_theory)

