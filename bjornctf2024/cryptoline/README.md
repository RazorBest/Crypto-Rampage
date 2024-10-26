# Cryptoline

- CTF: BjörnCTF 2024 - https://björnc.tf/ (Organized by flagbot - https://flagbot.ch/)
- difficulty: easy
- tags: linear algebra, abstract algebra, CPA


## Statement
Fast encryption. Server is listening at nc line.björnc.tf 1338 or nc line.ctf.flagbot.ch 1338

## Writeup

### Introduction

We are given the source code of the server, server.py and an endpoint to interact with.
If we connect to the endpoint, we receive the following message:
```
Welcome to my new encryption machine. It can encrypt 28 character text messages
28 character message to encrypt:
```
Typing something in the terminal yields to the following message:
```
Bad message
```

### Source code first glance

If we look at server.py, we see one class, `Line`, with an encrypt method, and
some main code.

In the main, we see the printed message, then a loop that repeats the following:
   - Reads input from the user
   - Encrypts the input
   - If the encryption succeeds, it prints the encrypted message

The loop iterates a fixed number of times. After that, it prints the encrypted flag.

Note that the same encryption function is used for both input and the flag.
So, just by looking at the main, we might assume this is a chosen-plaintext attack.

Chosen-plaintext means that we can choose m_1, m_2, ..., m_N messages, for which
we are given their encryption c_1, c_2, ... c_N i.e. c_i = E(m_i), E(...) being
the encryption function. The scope is to find some M, given C, such that E(M) = C.


### Looking at the encrypt function

After the first glance, it is pretty clear that the weakness is in the
`encrypt` function.

The code is a little obfuscated with list comprehensions. So, first, I
turned it into something that's easier to understand. I also added some comments
that indicated my thoughts, while reading the code.

This is the original code:
```python
def __init__(self):
    self.sk = [secrets.randbelow(P) for _ in range(MESSAGE_SIZE**2)]

def encrypt(self,message):
    message_list = [ ord(l)-(SHIFT-1) for l in message]
    assert(len(message_list)**2==len(self.sk))
    ct_list = [sum([message_list[i]*self.sk[j+len(message_list)*i] for i in range (len(message_list))])%P for j in range (len(message_list))]
    ct= "".join([chr(c+(SHIFT-1)) for c in ct_list])
    return(ct)
```

After manual analysis:
```python
def __init__(self):
    # Random array of ints below P
    self.sk = [secrets.randbelow(P) for _ in range(MESSAGE_SIZE**2)]

def encrypt(self,message):
    # Rots the whole message by (SHIFT-1) to the left
    message_list = [ ord(l)-(SHIFT-1) for l in message]
    # The message must be of length MESSAGE_SIZE
    assert(len(message_list)**2==len(self.sk))

    ct_list = []
    for j in range (len(message_list)):
        s = 0
        for i in range(len(message_list)):
            s += message_list[i]*self.sk[j+len(message_list)*i]

        # s is m0 * s0 + m1 * s1 + m2 * s2 + ... + mk*sk
        # but s0, s1, ..., sk are taken as jumps from self.sk


        ct_list.append(s%p)

    #ct_list = [sum([message_list[i]*self.sk[j+len(message_list)*i] for i in range (len(message_list))])%P for j in range (len(message_list))]

    # This is reversible
    ct= "".join([chr(c+(SHIFT-1)) for c in ct_list])
    return(ct)
```

The first and the last parts are pretty easy to reverse. So, let's focus
on the middle one:
```python
    ct_list = []
    for j in range (len(message_list)):
        s = 0
        for i in range(len(message_list)):
            s += message_list[i]*self.sk[j+len(message_list)*i]
        ct_list.append(s%p)
                
```

For some, it might already be clear what this operation is. But, you can
always list the operations one by one. The inner loop computes the sum of
products of two elements, in which, the first element comes from the message
and the second comes from the secret key.

For j = 0, this will be:
```
# m is message_list and sk is self.sk
# Assume len(message_list) == 28, like in the real example
s = m[0]*sk[0] + m[1]*sk[28] + m[2]*sk[56] + ... + m[27]*sk[28*27]
```

Then, `ct_list` is just an array of these sums (modulo P), given that j changes.
```
ct_list[0] = m[0]*sk[0] + m[1]*sk[28] + m[2]*sk[56] + ... + m[27]*sk[28*27]
ct_list[1] = m[0]*sk[1] + m[1]*sk[29] + m[2]*sk[57] + ... + m[27]*sk[1 + 28*27]
ct_list[2] = m[0]*sk[2] + m[1]*sk[30] + m[2]*sk[58] + ... + m[27]*sk[2 + 28*27]
...
ct_list[27] = m[0]*sk[27] + m[1]*sk[55] + m[2]*sk[83] + ... + m[27]*sk[27 + 28*27]
```

The equations above can be generally written as:
```
ct_list[j] = m[0]*sk[j] + m[1]*sk[j + 28] + m[2]*sk[j + 56] + ... + m[27]*sk[j + 28*27]
```

What we can observe is that each element of sk is used once, but the elements
of m are used multiple times. But, this sequence of operations is just a matrix
multiplication

Let SK be the matrix that has the values from the array sk. The first line
will correspond to the first 28 elements of sk. The next line corresponds to
the next 28, and so on:
```
# This just corresponds to self.sk[j+len(message_list)*i] from the source code
SK[i][j] = sk[j+28*i]
```


Given SK, we can write ct_list[j] like this:
```
ct_list[j] = m[0]*SK[0][j] + m[1]*SK[1][j] + m[2]*SK[2][j] + ... + m[27]*SK[27][j]
```

Now, some linear algebra. Assume m is a column vector, and ct_list, also a
column vector:
```
ct_list = SK^T * m
```
Where `*` is matrix multiplication, and `SK^T` is the matrix transpose of
`SK`. We could've got rid of the tranpose by using row vectors instead. But,
usually, people are more familiar with column vectors.


Now, back to our problem. We are given the encrypted flag, which we know is:
```
# x is the actual flag. We labeled it like this because it is an unknown.
SK^T * x = enc_f
```

But this is just a system of linear equations. We just solve it and the challenge
is done.

The flag is...


### Wait, but SK is secret. How do we know it?

That's where the chosen-plaintext part comes in. We can choose some messages
such that:
```
SK^T * m0 = c0
SK^T * m1 = c1
...
SK^T * m27 = c27
```
It would be nice if these pairs would reveal SK. If you wanna come up
with a solution alone, ask yourself the following: how can I find SK[0][0]?
Then, build up from that, to find the whole SK.


---


The solution is to choose `m_i` such that:
```
m_i[j] == 0 for any j != i
m_i[i] == 1
```

This, way, `c_i` will exactly be made of the i-th column of SK^T. By using
the general formula for `ct_list`:
```
c_i[j] = m_i[0]*SK[0][j] + m_i[1]*SK[1][j] + m_i[2]*SK[2][j] + ... + m_i[27]*SK[27][j]
```
Using the above properties of `m_i`, we can reduce the above equation to:
```
c_i[j] = m_i[i]*SK[i][j] = SK[i][j] = SK^T[j][i]
```

Then, as stated earlier `c_i` will be made out of the i-th column of SK^T:
```
c_i = [SK^T[0][i], SK^T[1][i], SK^T[2][i], SK^T[3][i], ..., SK^T[27][i]]
```

Which is a known ciphertext. If `c_i` gives us the i-th column, then
`c0, c1, ..., c27` altogether will give us the 28 columns of SK^T.

In other words, we can determine SK^T like this:
```
SK^T[j][i] = c_i[j]
```

Returning to the linear equation, now we can solve it, knowing SK^T.

The flag is ...


### What is a group?

Well, there's one more thing (I promise). When I derived the equations for
`ct_list`, I mentioned that all the operations are done modulo P. This is
also true for the system of linear equations we want to solve:
```
SK^T * x = enc_f
```

The elements of SK^T, enc_f and x are between 0 and P-1. And the additions
and multiplications that come from the matrix operation are all happening
modulo P. This is the same as saying that the elements of the matrices and
vectors are in the ring `Z_P`. In our case, `P` is 89, which is a prime number,
so `Z_P` isn't just a ring, but a field. This means that every non-zero element
has an multiplicative inverse.

Using numpy for the above system doesn't work, because it will yield a solution
made out of floating points, which aren't in the ring `Z_P`. Sadly, when I
solved the challenge, I knew there was some way of using sagemath to solve the
equation, but I didn't find out how. So, I made my own solver that was using
Gaussian elimination, since `SK^T` is a square matrix.

The difference between real numbers and the field `Z_P` is that division is
done differently. In `Z_P`, `a / b` is actually `a * b^(-1)`, where `b^(-1)`
is the multiplicative inverse of `b`, i.e. `b * b^(-1) = 1 (mod P)`. Python
has an easy way to compute this, which is `pow(b, -1, P)`. Now, with all
this information, we can do Gaussian elmination in the field `Z_P`:
```python
def solve_the_system(A, b):
    # Assume A is a square matrix
    n = len(A)
    for i in range(n):
        # The only case this fails is when A[i][i] is 0
        # If this happens, just start the challenge again
        inv = pow(int(A[i][i]), -1, P)

        # Force A[i][i] to become 1
        A[i] = (A[i] * inv) % P
        b[i] = (b[i] * inv) % P
        for j in range(n):
            if j == i:
                continue

            ct = A[j][i]
            # Force A[j][i] to become 0
            A[j] = (A[j] - A[i] * ct) % P
            b[j] = (b[j] - b[i] * ct) % P

    return b
```

Now, calling `solve_the_system` on `SK^T` and `enc_flag` will yield `x`, which
is the real flag.

The solution is in `break.py`.
