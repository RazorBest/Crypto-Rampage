from base64 import b64decode
from z3 import *

with open("flag.enc", "rb") as f:
    enc = f.read()

def SwitchCase(A):
    return If(And(A >= ord('a'), A <= ord('z')),
            A - 32, If(And(A >= ord('A'), A <= ord('Z')),
                    A + 32, A))

N = len(enc)

B = [BitVec(f"B_{i}", 8) for i in range(N)]
B2 = [BitVec(f"B2_{i}", 8) for i in range(N)]
K = [BitVec(f"K_{i}", 8) for i in range(N // 8)]
Enc = [BitVec(f"Enc_{i}", 8) for i in range(N)]

s = Solver()

for i in range(N):
    s.add(Or(And(B[i] >= ord('a'), B[i] <= ord('z')), And(B[i] >= ord('A'), B[i] <= ord('Z')),
        B[i] == ord('='), B[i] == ord('/'), B[i] == ord('+'), And(B[i] >= ord('0'), B[i] <= ord('9'))))

lim = N
if lim % 8 != 0:
    lim -= lim % 8

for i in range(lim):
    idx = 7 - (i % 8)
    s.add(If(And(B[i] >= ord('a'), B[i] <= ord('z')),
            Extract(idx, idx, K[i // 8]) == 0, Extract(idx, idx, K[i // 8]) == 1))

for i in range(N):
    s.add(B2[i] == (SwitchCase(B[i])))
    s.add(Enc[i] == B2[i] ^ K[i % len(K)])
    s.add(Enc[i] == enc[i])

s.check()
m = s.model()

msg = ''.join([chr(int(f"{m.evaluate(B[i])}")) for i in range(N)])
msg = b64decode(msg.encode('utf8')).decode('utf8')
print(msg)
