"""
c1 = a*P + b (mod N) - encryption
c1 = c*29 + d (mod N), c < 29, d < 29 - decoding

a*P1 + b = c1*29 + d1 (mod N)
a*P2 + b = c2*29 + d2 (mod N)

[P1 1]   [a]   [c1*29 + d1]
       *     =
[P2 1]   [b]   [c2*29 + d2]

"""
from string import ascii_uppercase

ALPHABET = ascii_uppercase + "αβγ"
LEN = len(ALPHABET) # 29
MOD = LEN * LEN # 841
KNOWN_PLAINTEXTS = ["TH", "HE", "IN"]
KNOWN_CIPHERTEXTS = ["βγ", "UM", "LC"]

CIPHERTEXT_TO_BREAK = "KEUDCR"

R = IntegerModRing(MOD)

def symbolic_solve():
    p1, p2 = var("p1 p2")
    c1, c2 = var("c1 c2")
    A = Matrix([[p1, 1], [p2, 1]])
    c = Matrix([[c1],  [c2]])

    x = A.solve_right(c)
    a = x[0][0].full_simplify()
    b = x[1][0].full_simplify()
    return a, b

def solve_from_two(P1, P2, C1, C2):
    A = Matrix([[P1, 1], [P2, 1]])
    c = Matrix([[C1],  [C2]])

    x = A.solve_right(c)
    a = x[0][0]
    b = x[1][0]

    return a, b

def solve(P_list, C_list):
    P1, P2, P3, *_ = P_list
    C1, C2, C3, *_ = C_list

    # Convert to finite ring
    P1, P2, P3 = R(P1), R(P2), R(P3)
    C1, C2, C3 = R(C1), R(C2), R(C3)

    a1, b1 = solve_from_two(P1, P2, C1, C2)
    a2, b2 = solve_from_two(P1, P3, C1, C3)

    assert a1 == a2
    assert b1 == b2

    return int(a1), int(b1)

def pair_to_int(pair):
    assert len(pair) == 2
    return (ALPHABET.find(pair[0]) * LEN + ALPHABET.find(pair[1])) % MOD

def int_to_pair(val):
    return ALPHABET[val // LEN], ALPHABET[val % LEN]

def decrypt(c: str, a: int, b: int):
    assert len(c) % 2 == 0

    a_inv = int(pow(a, -1, MOD))
    m = ""
    for c_pair in [c[i:i+2] for i in range(0, len(c), 2)]:
        p = ((pair_to_int(c_pair) - b) * a_inv) % MOD
        p1, p2 = int_to_pair(p)
        m += p1 + p2

    return m

def main():
    print(f"Symbolic solution from two equations:\n{symbolic_solve()}\n")
    P_list = list(map(pair_to_int, KNOWN_PLAINTEXTS))
    C_list = list(map(pair_to_int, KNOWN_CIPHERTEXTS))
    a, b = solve(P_list, C_list)

    print(f"(a, b) = ({a}, {b})")
    plaintext = decrypt(CIPHERTEXT_TO_BREAK, a, b)

    print(f"Ciphertext: {CIPHERTEXT_TO_BREAK}")
    print(f"Broken plaintext: {plaintext}")


if __name__ == "__main__":
    main()

