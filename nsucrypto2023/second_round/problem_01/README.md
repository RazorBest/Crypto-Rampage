# Problem 01 - Affine cipher

## Explanation

It is known that the affine cipher is insecure against known-plaintext attack.
Even if the substitution is performed on bigrams, we can consider the alphabet
to be all the pairs of characters (841 in total). The affine transformation
has two unknown variables. They can be found with two linear equations, given
from (plaintext, ciphertext) pairs. In general, 4 characters are enough to
find the secret key.

The solution is implemented in `solve.sage`. Running the script, finds the
plaintext of "KEUDCR", which is "CRYPTO".

Given two plaintext-ciphertext pairs: (p1, c1), (p2, c2)
Where p1, p2, c1, c2 are in Z/841Z

The system of equations is:
    a*p1 + b = c1 (mod 841)
    a*p2 + b = c2 (mod 841)

The symbolic solution computed with sage:
    a = (c1 - c2)/(p1 - p2) (mod 841)
    b = (c2 * p1 - c1 * p2)/(p1 - p2) (mod 841)

The formulas work as long as p2 != p1 (mod 29), which is true for the first
of our two plaintexts: "TH" and "HE".

## Solution

Running the script, finds a and b:
```
(a, b) = (15, 10)
```

Broken plaintext: CRYPTO
