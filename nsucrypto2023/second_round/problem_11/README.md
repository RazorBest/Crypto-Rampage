# Problem 11 - AntCipher

The boolean expression is small enough to be evaluated by Z3. It turns out
the truth table of (x9, x10) (depending on x1 and x2) is:

    x1: False, x2: False, x9: True, x10: False
    x1: False, x2: True, x9: True, x10: True
    x1: True, x2: False, x9: False, x10: False
    x1: True, x2: True, x9: False, x10: True

The above results were obtained by running solve.py. We can observe that
x9 depends only on x1, and x10 depends only on x2. The truth table can be
expressed like the following:

    (x1 | x9) & (x2 & x10 | ~x2 & ~x10) = True

Converting the expression to CNF with sympy, we get:

    (x1 | x9) & (x10 | ~x2) & (x2 | ~x10) = True

The above expression, in CNF, is equivalent to the initial one.
