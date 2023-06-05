# Baphomet

- CTF: cryptoctf2022 - https://ctftime.org/event/1573
- difficulty: easy
- tags: base64, xor, z3

## Writeup

We are give an encryption algorithm in cipher.py that's actually an encoding.
We have to reverse it somehow. I used Z3 to fully reverse to algorithm. The
advandage of this approach is that it doesn't use any information about the
plaintext, except the fact that it is encoded in base64.

References:
- https://ericpony.github.io/z3py-tutorial/guide-examples.htm
- https://infosecadalid.com/2021/08/27/my-introduction-to-z3-and-solving-satisfiability-problems/
