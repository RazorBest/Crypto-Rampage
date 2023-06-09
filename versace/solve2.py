from primefac import *
from Crypto.Util.number import *
from sympy.ntheory import discrete_log
import gmpy2

def solve(c1, c2, c3, c4, n, fact, e, fi, th):
    """Don't ask me how I found the math for that."""
    p = fact
    e_inv = pow(e, -1, p - 1)
    b = pow(c1, e_inv, p)
    b2 = pow(b, -1, p)
    sol = c4 * pow(b2 + 1, e, n) * pow(b + b2 + 2, -e, p) % p

    c4 = sol
    u = discrete_log(p, c2, 5)
    v = discrete_log(p, c3, 13)
    sol = c4 * pow(fi, -u, p) * pow(th, -v, p) % p

    return sol

def pollard_p_1(n, B=600):
    start = 2
    a = 2
    for i in range(B):
        a = pow(a, i, n)
        g = gcd(a - 1, n)
        if g > 1:
            if g == n:
                start += 1
                a = start
            else:
                return g

    return None

with open("output.txt") as f:
    for line in f.readlines():
        if "pubkey" in line:
            line = line.split('(')[1]
            line = line.split(')')[0]
            numbers = line.split(',')
            numbers = [int(x) for x in numbers]
            pubkey = (numbers[0], numbers[1], numbers[2], numbers[3])
        if "enc" in line:
            line = line.split('(')[1]
            line = line.split(')')[0]
            numbers = line.split(',')
            numbers = [int(x) for x in numbers]
            enc = (numbers[0], numbers[1], numbers[2], numbers[3])

n, e, fi, th = pubkey
c1, c2, c3, c4 = enc

fact1 = pollard_p_1(n)

fact2 = pollard_p_1(n // fact1)

# sol1 = message (mod fact1)
sol1 = solve(c1, c2, c3, c4, n, fact1, e, fi, th)

# Do CRT with the fact that the message ends in '}'
sol1 = sol1 + (125 - sol1) * fact1 * pow(fact1, -1, 256)
sol1 = sol1 % (fact1 * 256)
fact1 *= 256

# sol2 = message (mod fact1)
sol2 = solve(c1, c2, c3, c4, n, fact2, e, fi, th)
# Do CRT again with fact2
sol1 = sol1 + (sol2 - sol1) * fact1 * pow(fact1, -1, fact2)
sol1 = sol1 % (fact1 * fact2)
fact1 *= fact2

sol = sol1
fact = fact1

"""
# That's for the case we know the second factor
sol2 = solve(c1, c2, c3, c4, n, second_factor, e, fi, th)

sol = sol + (sol2 - sol) * fact * pow(fact, -1, q)
sol = sol % (fact * q)
fact *= q
"""

for i in range(100000000):
    m = long_to_bytes(sol)
    if b'CCTF{' in m:
        try:
            m = m.decode("utf8")
            print(f"pos: {i}")
            print(m)
        except:
            pass

    wanted = b"CCTF{" + b"\x00" * (len(m) - len("CCTF{"))
    limit = b"CCTF|" + b"\x00" * (len(m) - len("CCTF{"))
    if sol > bytes_to_long(limit):
        print(f"exceeded {len(m)}")
        wanted += b"\x00"
    wanted = bytes_to_long(wanted)

    coeff = (wanted - sol) // fact

    if coeff <= 0:
        coeff = 1
    sol += coeff*fact

