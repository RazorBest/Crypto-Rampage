# polyRSA

- CTF: cryptoctf2022 - https://ctftime.org/event/1573
- difficulty: easy
- tags: RSA, polynomials, sage

## Writeup

We are give an encryption algorithm in cipher.py. It's textbook RSA with
a custom key generation function. The primes p and q are generated from a
polynomial. After knowing n, we can solve the polynomial and find the root.
