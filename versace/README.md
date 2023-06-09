# Baphomet

- CTF: cryptoctf2022 - https://ctftime.org/event/1573
- difficulty: medium
- tags: RSA, discrete log, factoring, crt

## Writeup

Looking at the code, we see that the encryption is a combination of
exponantiation and a polynomial, are equivalent to the discrete log prolem and
the RSA problem. We can efficiently solve these problems if we know the prime
factors of n.

Trying to run primefac(python) on n, gave me one factor p, but not the others.
If m was small enough, than we could've extracted m mod p. Let's say
m' = m mod p => m = c * p + m' for some integer c'. Knowing that m is ascii
encoded, we can try to bruteforce c. In our case, p i 33 bytes. We can
effectively bruteforce at most 8 bytes of c. So, if m would've been at most
41 bytes, we could get it. Sadly, in this challenge, it is bigger.

After more fiddling with prime factorisation, it turned out you can easily
factor n with pollard's p-1. For some reason, primefac's algorithm for
pollard p-1 doesn't work for our n. But the simple implementation of this
algorithm works.

n = p * q * r

We can find m1 = m mod p, m2 = m mod q, and with CRT find m12 = m mod pq, which
is a good enough upper bound for our flag.

References:
- https://pypi.org/project/primefac/
