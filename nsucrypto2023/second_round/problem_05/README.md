# Problem 05 - Primes

Just analyze the equation, modulo 2.

Let p, q b primes, n = pq, and m = p + q.

The equation:
    m*n ends in 2023

Implies:
    m*n = 1 (mod 2)
    pq(p + q) = 1 (mod 2)

Try every combination of p and q, chosen from Z/2Z:

I. p = 0, q = 0 (both even)

   0 * 0 * (0 + 0) = 0 (mod 2)

II. p = 0, q = 1 (second, odd)

    0 * 1 * (0 + 1) = 0 (mod 2)

III. p = 1, q = 0 (first, odd)

    1 * 0 * (1 + 0) = 0 (mod 2)

IV. p = 1, q = 1 (both odd)

    1 * 1 * (1 + 1) = 1 * 1 * 0 = 0 (mod 2)

So, for and p and q, mn = 0 (mod 2). So, the equation is never satisfied.


