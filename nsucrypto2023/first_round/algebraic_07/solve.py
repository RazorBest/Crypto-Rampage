from sympy import *

k = symbols("k0:8")

b = list(k)
sec = [b[0] & b[2] ^ b[7]]
i = 8
while True:
    print(sec[-1])
    b_new = b[i - 1] ^ b[i - 8]
    sec_new = b[i-7] & b[i-5] ^ (b[i - 1] ^ b[i - 8])
    if sec[0] == sec_new:
        break
    b.append(b_new)
    sec.append(sec_new)
    i += 1

period = i - 8
print(f"Period {i}")

known = "00100001"

lost_bits = 1200
i = lost_bits % period
solution = None
for j in range(2**8):
    vals = [int(x) for x in list(bin(j)[2:])]

    out = []
    for i2 in range(8):
        bit = 1 if sec[i + i2].subs(zip(k, vals)) else 0
        out.append(bit)
    out = "".join(str(int(b)) for b in out)

    if out == known:
        print(f"One solution {vals}")
        solution = vals

