import string

from Crypto.Util.number import *
from pwn import *
from sympy.polys.domains import ZZ
from sympy.polys.matrices import DM
from itertools import permutations

HOST = "archive.cryptohack.org"
PORT = 45400
e = 253

def mapped(s, perm):
    ret = ""
    for x in s:
        ret += perm[int(x, 16)]
    return ret

def solve_pow(s):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        answer = ''.join(random.choices(alphabet, k=10))
        hash = hashlib.sha256((s + answer).encode()).hexdigest()
        if hash[:6] == "000000":
            return answer

n = "21636464540933977792792361905538805843519561439488449285033922064828661242739616752331789463942467825052958849425917458921350419542610848885293295656202019182749002943128257920136084713585078050982830847212016400845955362325576933132881335854504464909627324210819862581236399456811821715287012809211150435199542240960545478516376080179902141238764477372488294436481565320485543841552654825461458974969869455940617035027063780976313753301556456469104879656759340179716521914525457152167194933915844401409396069562450604988981014055515589899621672492475948696124689405147667764188600646757178408906478253893386463502591"
dp_hex = "576cab9f9e588e6a1ff2754bad55c777e89a87d94990d8fab45328b87516d520e512d2273ce15a727e9fa41c5ddc0e2bb53f2ad60aa8415f128dbe87398dfb0e06e8047a9ea879f7b8e7be57d3222e65a8b67b5ecc58bb7877cb60432038469d50213b7eb0d7d8c8723c07b4ff607b776f2083a349e043beb9f4513e53957172"
dq_hex = "60055053c4a5df8359e1564046a197b21626a332ab047daa1a77eacb5f8aa57b802483ea7b5361134ec2487775fc663d8bbb3bf2434486f372d03f3c184ddcac27b7672e50a04743787c8221721974d19c545ac400284f4172c62d42e93516f58d0fdcba1f8d47120d90a5bf0d45722d4206740cc8c221068219ff08dbeff428"

n = int(n)

"""
conn = remote(HOST, PORT)
line = conn.recvline()
line = conn.recvline().strip(b'\n')

print(line)
proof = solve_pow(line.decode("utf8"))
conn.send(proof.encode("utf8") + b"\r\n")

line = conn.recvline()
print(line)
line = conn.recvline()
print(line)
line = conn.recvline()
print(line)
"""
p = 22699
q = 55117
n = p * q
dp = pow(e, -1, p - 1)
dq = pow(e, -1, q - 1)

print(f"kp = {(dp * e - 1) / (p - 1)}")

dp_hex = long_to_bytes(dp).hex()
dq_hex = long_to_bytes(dq).hex()

alphabet = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

pos_map = {c: len(dp_hex) for c in alphabet}
for idx, c in enumerate(dp_hex):
    pos_map[c] = min(pos_map[c], idx)

#alphabet = sorted(alphabet, key=lambda x: pos_map[x])

coeff1 = 1
e_inv = pow(e, -1, n)

print(f"dp = {bytes.fromhex(dp_hex)}")

for perm in permutations(alphabet):
    dp = bytes.fromhex(mapped(dp_hex, perm))
    dq = bytes.fromhex(mapped(dq_hex, perm))
    print(f"permed dp = {dp}")
    # The known prefix of dp - the first 6 bytes
    A = bytes_to_long(dp[:1] + b"\x00" * (len(dp) - 1))

    #for kp in range(e):
    kp = 123
    coeff0 = (A - e_inv*(1 - kp)) % n

    print(f"x = {bytes_to_long(dp[1:])}")
    assert (coeff1 * bytes_to_long(dp[1:]) + coeff0) % p == 0
    #assert (coeff1 * bytes_to_long(dp[1:]) + coeff0) % n == 0

    from math import gcd, sqrt
    print(f"gcd: {gcd(coeff0, coeff1)}")
    m = DM([[4, coeff0, 0], [0, coeff1, coeff0], [0, 0, n]], ZZ)
    print(m)
    print(f"norm limit: {2**(1/4)*pow(m.det(), 1/2)}")
    min_m = m.lll()
    print(min_m)
    coeff2 = min_m.to_list()[0][0]
    coeff1 = min_m.to_list()[0][1]
    coeff0 = min_m.to_list()[0][2]
    print(f"norm found: {sqrt(coeff0**2+coeff1**2)}")


    print(coeff2*27**2 - coeff1*27 +coeff0)

    assert (coeff2 * bytes_to_long(dp[1:])**2 + coeff1 * bytes_to_long(dp[1:]) + coeff0) % p == 0

    for i in range(100000):
        if (i*p-coeff0) % coeff1 == 0:
            print(f"index = {i}")
            sol = (i*p - coeff0) // coeff1
            print(f"sol = {sol}")
            break

        delta = coeff1**2 - 4*coeff2*coeff0

        """
        if delta >= 0:
            x1 = (-coeff1 + sqrt(delta)) / (2*coeff2)
            x2 = (-coeff1 - sqrt(delta)) / (2*coeff2)

            print(f"x1 = {x1}")
            print(f"x2 = {x2}")
            """

    exit()
    sol = -coeff0 / coeff1
    sol_int = -coeff0 // coeff1

    print(f"min_norm = {n // q}")
    print(f"norm = {sqrt(coeff0**2 + coeff1**2)}")
    print(f"sol = {sol}")
    print(f"sol_int {sol_int}")
    print(f"modulo {-coeff0 % coeff1}")

    exit()
