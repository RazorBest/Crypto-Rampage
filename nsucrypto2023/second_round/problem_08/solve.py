from sympy import *

def random_generator(k: list[int]):
    assert len(k) == 8
    assert all(val == 0 or val == 1 for val in k)

    b = list(k)

    while True:
        gen = (b[0] * b[2]) ^ b[7]
        yield gen

        b_new = b[-1] ^ b[-8]
        b.append(b_new)
        b.pop(0)


def verify_solution(k: list[int], start, length, expected):
    """Verify a sequence with seed k, starting at position
        start (counting from 0), of given length."""
    rng = random_generator(k)
    # Discard first bits, until start
    for i, val in enumerate(rng):
        if i >= start:
            break

    actual = [val]
    for i, val in enumerate(rng):
        if i >= length - 1:
            break

        actual.append(val)

    expected = [int(c) for c in expected]

    assert actual == expected

k = symbols("k0:8")

b = list(k)
sec = [b[0] & b[2] ^ b[7]]
i = 8
while True:
    print(sec[-1])
    b_new = b[i - 1] ^ b[i - 8]
    sec_new = (b[i - 7] & b[i - 5]) ^ b_new
    if b[-7:] + [b_new] == b[:8]:
        #if i >= 1500:
        break
    b.append(b_new)
    sec.append(sec_new)
    i += 1

period = i - 7
print(f"Period {period}")

known = "00100001"

lost_bits = 1200

i = lost_bits % period
sols = []
solution = None
for j in range(2**8):
    vals = [int(x) for x in list(f"{j:08b}")]

    out = []
    for i2 in range(8):
        bit = 1 if sec[i + i2].subs(zip(k, vals)) else 0
        out.append(bit)
    out = "".join(str(int(b)) for b in out)

    if out == known:
        print(f"One solution {vals}")
        sols.append(vals)

for sol in sols:
    print(sol)
    verify_solution(sol, lost_bits, len(known), known)


if len(sols) <= 1:
    exit()

# Solutions
i = 0
k1 = sols[0]
k2 = sols[1]
w = 0
for v1, v2 in zip(random_generator(k1), random_generator(k2)):
    if i >= period:
        break
    w += (v1 ^ v2)
    i += 1

print(f"Weight difference between first two solutions: {w}")
