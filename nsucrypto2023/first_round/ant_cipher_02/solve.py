from sympy import *

x = [None]
for i in range(1, 11):
    x.append(symbols("x" + str(i)))


f = \
(x[1] | x[2] | x[9]) &\
(~x[1] | ~x[2] | ~x[9]) &\
(~x[1] | x[2] | ~x[9]) &\
(x[1] | ~x[2] | x[9]) &\
(x[1] | x[2] | x[3]) &\
(~x[9] | ~x[10] | ~x[3]) &\
(x[1] | ~x[2] | x[4]) &\
(~x[9] | x[10] | ~x[4]) &\
(~x[1] | x[2] | x[5]) &\
(x[9] | ~x[10] | ~x[5]) &\
(~x[1] | ~x[2] | x[6]) &\
(x[9] | x[10] | ~x[6]) &\
(x[1] | x[2] | x[3] | x[4] | ~x[7]) &\
(x[2] | x[3] | x[4] | ~x[7] | ~x[8]) == 1

print(simplify_logic(f, form='cnf'))
