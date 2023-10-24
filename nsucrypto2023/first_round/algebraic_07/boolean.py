import sympy
from sympy.logic import boolalg

def set_bit_positions(x: int):
    positions = []

    index = 0
    p = 1
    while x:
        if x & p:
            x -= p
            positions.append(index)

        index += 1
        p *= 2

    return positions

class BooleanFunctionANF:
    def __init__(self, symbols=None, truthvalues=None, anf=None):
        if anf is not None:
            self.anf = anf
            self.f_symbols = list(anf.free_symbols)
            self.size = len(self.f_symbols)
        elif truthvalues is not None:
            self.f_symbols = symbols
            self.anf = boolalg.ANFform(symbols, truthvalues)
            self.size = len(symbols)
        else:
            raise Exception

    def __str__(self):
        return str(self.anf)

    def __repr__(self):
        return str(self)

    def __call__(self, x):
        if isinstance(x, int):
            bits = bin(x)[2:].zfill(self.size)[::-1]
            bits = [int(b) for b in bits]
            return self.anf.subs(list(zip(self.f_symbols, bits)))

        if isinstance(x, list):
            return self.anf.subs(list(zip(self.f_symbols, x)))

        raise Exception

    def __xor__(self, x):
        if isinstance(x, BooleanFunctionANF):
            return BooleanFunctionANF(anf=boolalg.to_anf(self.anf ^ x.anf))

        if isinstance(x, int) or isinstance(x, bool):
            return BooleanFunctionANF(anf=boolalg.to_anf(self.anf ^ x))

        raise Exception

    def __and__(self, func):
        return BooleanFunctionANF(anf=boolalg.to_anf(self.anf & func.anf))



class VectorialBooleanFunctionANF:
    def __init__(self, f_list=None, f_symbols=None):
        self.f_list = list(f_list)

        extracted_symbols = set()
        for func in f_list:
            extracted_symbols |= set(func.free_symbols)

        if f_symbols:
            if not extracted_symbols <= set(f_symbols):
                raise Exception
            self.f_symbols = f_symbols
        else:
            self.f_symbols = list(extracted_symbols)

        self.size = (len(self.f_symbols), len(self.f_list))

    def __str__(self):
        return str(tuple(self.f_list))

    def __call__(self, x):
        if isinstance(x, int):
            bits = bin(x)[2:].zfill(self.size[0])[::-1]
            bits = [int(b) for b in bits]
            sub_dict = list(zip(self.f_symbols, bits))
        elif isinstance(x, list):
            sub_dict = list(zip(self.f_symbols, x))
        else:
            raise Exception

        result = tuple(func.subs(sub_dict) for func in self.f_list)

        if isinstance(x, int):
            bit_list = [str(int(bool(bit))) for bit in reversed(result)]
            result = int(''.join(bit_list), 2)

        return result
        
    def __xor__(self, vbf):
        result = []
        for f1, f2 in zip(self.f_list, vbf.f_list):
            result.append(boolalg.to_anf(f1 ^ f2))

        f_symbols = tuple(set(self.f_symbols + vbf.f_symbols))

        return VectorialBooleanFunctionANF(f_list=result, f_symbols=f_symbols)


def integer_add_bfunction_bit(vbf1, vbf2, pos):
    f1 = vbf1.f_list
    f2 = vbf2.f_list
    if pos == 0:
        return f1[0] ^ f2[0]

    carry = f1[pos-1] ^ f2[pos-1] ^ integer_add_bfunction_bit(vbf1, vbf2, pos - 1)
    return f1[pos] ^ f2[pos] ^ (f1[pos-1] & f2[pos-1]) ^ (f1[pos-1] & carry) ^ (f2[pos-1] & carry)

def integer_add_bfunction(vbf1, vbf2):
    carry = 0
    result = []

    for i in range(vbf1.size[1]):
        result.append(boolalg.to_anf(integer_add_bfunction_bit(vbf1, vbf2, i)))

    return VectorialBooleanFunctionANF(f_list=result, f_symbols=vbf1.f_symbols + vbf2.f_symbols)

from sympy import symbols
from random import randint

X = symbols("x0:6")
S = symbols("y0:36")
#f1 = BooleanFunctionANF(X, [0, 1, 0, 1, 1, 0, 1] + [0] * 9)
#f2 = BooleanFunctionANF(X, [0, 1, 0, 0, 1, 0, 0, 1] + [0] * 8)

#F = [BooleanFunctionANF(X, [randint(0, 1) for _ in range(16)]) for i in range(4)]
#F1 = VectorialBooleanFunctionANF(F)
#F = [BooleanFunctionANF(X, [randint(0, 1) for _ in range(16)]) for i in range(4)]
#F2 = VectorialBooleanFunctionANF(F)


rounds = 1
As = symbols("A0:4")
Bs = symbols("B0:4")
Cs = symbols("C0:4")
Ss = symbols("S0:36")

A = VectorialBooleanFunctionANF(As, f_symbols=As)
B = VectorialBooleanFunctionANF(Bs, f_symbols=Bs)
C = VectorialBooleanFunctionANF(Cs, f_symbols=Cs)
S = [VectorialBooleanFunctionANF(Ss[i:i+4], f_symbols=Ss[i:i+4]) for i in range(0, 36, 4)]

A = integer_add_bfunction(A, S[0])
B = integer_add_bfunction(B, S[1])
for i in range(1, rounds + 1):
    A = integer_add_bfunction(A ^ B, S[2*i])
    B = integer_add_bfunction(A ^ B, S[2*i + 1])
A1 = A
B1 = B

B = VectorialBooleanFunctionANF(Bs, f_symbols=Bs)

A = integer_add_bfunction(C, S[0])
B = integer_add_bfunction(B, S[1])
for i in range(1, rounds + 1):
    A = integer_add_bfunction(A ^ B, S[2*i])
    B = integer_add_bfunction(A ^ B, S[2*i + 1])

Ax = A1^A
Bx = B1^B
print(Ax^Bx)

print(Ax.f_list[1] ^ Bx.f_list[1])
