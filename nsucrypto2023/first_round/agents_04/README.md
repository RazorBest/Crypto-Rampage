Let x be the secret known both by Alice and Bob.
Bob chooses randomly a, such that it is prime with phi(N).
Bob sends to Alice c1 = x * a (mod N).
Alice computes a = x^(-1) * c (mod N)
Alice sends c2 = x^a (mod N).
Bob computes x^a (mod N) and verifies with c2.

The role of N is to easily change the secret, if needed. If N is chosen, wisely, and big enough,
the quadratic residue of a number should be hard to compute.
