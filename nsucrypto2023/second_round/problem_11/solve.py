from z3 import Bool, Solver, Or, Not, And, sat

x = [None]
x.extend(Bool(f'x{i}')for i in range(1, 11))

e = []
e.append(Or(x[1], x[2], x[9]))
e.append(Or(Not(x[1]), Not(x[2]), Not(x[9])))
e.append(Or(Not(x[1]), x[2], Not(x[9])))
e.append(Or(x[1], Not(x[2]), x[9]))

e.append(Or(x[1], x[2], x[3]))
e.append(Or(Not(x[9]), Not(x[10]), Not(x[3])))
e.append(Or(x[1], Not(x[2]), x[4]))
e.append(Or(Not(x[9]), x[10], Not(x[4])))

e.append(Or(Not(x[1]), x[2], x[5]))
e.append(Or(x[9], Not(x[10]), Not(x[5])))
e.append(Or(Not(x[1]), Not(x[2]), x[6]))
e.append(Or(x[9], x[10], Not(x[6])))

e.append(Or(x[1], x[2], x[3], x[4], Not(x[7])))
e.append(Or(x[2], x[3], x[4], Not(x[7]), Not(x[8])))

s = Solver()
s.add(e)

for val1, val2 in ((0, 0), (0, 1), (1, 0), (1, 1)):
    s.push()
    s.add(And(x[1] == bool(val1), x[2] == bool(val2)))
    res = s.check()
    m = s.model()
    print(f"{x[1]}: {m[x[1]]}, {x[2]}: {m[x[2]]}, {x[9]}: {m[x[9]]}, {x[10]}: {m[x[10]]}")
    s.pop()

from sympy import symbols, simplify_logic
X1, X2, X9, X10 = symbols("X1 X2 X9 X10")
e = (X1 | X9) & (X2 & X10 | ~X2 & ~X10)
e = simplify_logic(e, form='cnf')
print(f"Simplified: {e}")
