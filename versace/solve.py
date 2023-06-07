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
# fact = multifactor(n, methods=(pollardrho_brent, pollard_pm1, williams_pp1, ecm, siqs))
# fact = fact[0]
fact = 106618752612001652530923691512073519044983443846656721126867402977583225110529

sol = solve(c1, c2, c3, c4, n, fact, e, fi, th)
print(long_to_bytes(sol))

# Do CRT with the fact that the message ends in '}'
sol = sol + (125 - sol) * fact * pow(fact, -1, 256)
sol = sol % (fact * 256)
fact *= 256

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

