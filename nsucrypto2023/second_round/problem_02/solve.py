import time
from Crypto.Util.number import isPrime, getPrime
from random import randint

def gen1():
    x = ""
    i = 1
    while True:
        x = str(i) + x
        yield int(x)
        i += 1

def gen2(a, b):
    x = ""
    while True:
        x += str(b) + str(b) + str(b)
        yield int(str(a) + x + str(a))

def gen3(start, injection_pos: int, inside_generator, limit=20):
    start = str(start)
    if start[:injection_pos] == '':
        first_part = 0
    else:
        first_part = int(start[:injection_pos])

    if start[injection_pos:] == '':
        second_part = 0
    else:
        second_part = int(start[injection_pos:])
    lsecond = len(str(second_part))
    psecond = 10**lsecond
    l = []

    l.append(int(start))

    for mid in inside_generator:
        smid = str(mid)
        l.append(first_part * (10**(len(smid) + lsecond)) + mid*psecond + second_part)

    return l

def gen4(start, injection_pos: int, inside_generator, limit=20):
    start = str(start)
    if start[:injection_pos] == '':
        first_part = 0
    else:
        first_part = int(start[:injection_pos])

    if start[injection_pos:] == '':
        second_part = 0
    else:
        second_part = int(start[injection_pos:])
    lsecond = len(str(start)) - len(str(first_part))
    psecond = 10**lsecond
    l = []

    l.append(int(start))

    for mid in inside_generator:
        smid = str(mid)
        first_part = first_part * (10**(len(smid) + lsecond)) + mid(psecond)
        l.append(first_part + second_part)

    return l

# Below, there are generators that yield sequences of numbers divisible
# by three
def three_gen_1(start=0):
    i = start
    while True:
        yield i
        i += 3

def three_gen_2(start=0, step=3, limit=20):
    l = []
    for i in range(start, start + step*limit, step):
        l.append(i)

    return l

def three_gen_3(start=3, fact=3, limit=20):
    l = []
    x = start
    for i in range(limit):
        l.append(x)
        x *= fact

    return l

def three_gen_4(base=1, sq=3, limit=20):
    x = base * sq
    l = []
    for _ in range(limit):
        l.append(x)
        sq *= sq
        x *= sq

    return l

def three_gen_5(limit=20):
    l = []
    a = 14
    b = 5
    for i in range(limit):
        l.append(a - b)
        a *= 14
        b *= 5

    return l

def three_gen_6(limit=15):
    yield 3
    x = 30
    for i in range(limit):
        yield x + 3
        x *= 10

def three_gen_7(base, mod=9, limit=15):
    x = base
    for i in range(limit):
        yield x - (x % 3)
        x = (x * base) % mod

def rev_numbers(gen):
    l = []
    for x in gen:
        l.append(int(''.join(list(reversed(str(x))))))

    return l


def check_sequence(itr, limit=100):
    max_len = 0
    curr_len = 0
    for index, x in enumerate(itr):
        #print(f'{x} {isPrime(x)}')
        curr_len += 1
        if not isPrime(x):
            curr_len = 0

        max_len = max(max_len, curr_len)

        if index >= limit:
            break

    return max_len

"""
Found 
len1, p, pos, start, step = 7, 9137, 0, 1440, 1953
len1, p, pos, start, step = 7, 15359, 2, 483, 1899
FACT: len1, p, pos, start, step = 7, 10429, 2, 762, 16
len1, p, pos, start, step = 8, 9283, 0, 648, 2310
REV: len1, p, pos, start, step = 8, 15727, 1, 267, 3
REV: len1, p, pos, start, step = 8, 9587, 1, 405, 15
len1, p, pos, start, step = 8, 11903, 2, 210, 21
len1, p, pos, start, step = 7, 11467, 4, 1482, 333
FACT: len1, p, pos, start, step = 8, 19483, 3, 391, 13
REV: len1, p, pos, start, step = 7, 24281, 3, 189, 9
REV: len1, p, pos, start, step = 8, 32441, 3, 435, 3
REV: len1, p, pos, start, step = 8, 31847, 0, 831, 3
REV: len1, p, pos, start, step = 7, 22787, 3, 198, 3
REV: len1, p, pos, start, step = 9, 42463, 4, 1689, 24
REV: len1, p, pos, start, step = 9, 62201, 2, 339, 18
REV: len1, p, pos, start, step = 9, 64007, 2, 276, 9
len1, p, pos, start, step = 10, 593, 1, 813, 21
REV: len1, p, pos, start, step = 10, 971, 0, 1200, 24
"""

def main():
    p, pos, start, step = 593, 1, 813, 21
    len1 = check_sequence(gen3(p, pos, three_gen_2(start, step, limit=2000)), limit=2000)
    print(len1)

    a = time.time()
    for i in range(100):
        p = getPrime(16)
        for j in range(25):
            for k in (3, 6, 9, 12, 15, 18, 21, 24, 27):
                len1 = check_sequence(gen3(p, pos, three_gen_2(start, step)), limit=30)
                if len1 > 8:
                    print(f"{len1}, {p}, {pos}, {start}, {step}")
    b = time.time()

    print(f"Time: {b - a}")

    for i in range(100):
        p = getPrime(9)
        print(p)
        # Don't insert at the end
        for pos in range(len(str(p))):
            len1 = check_sequence(gen3(p, pos, three_gen_5(limit=30)))
            if len1 > 9:
                print(f"gen5: {len1}, {p}, {pos}")

            len1 = check_sequence(gen3(p, pos, rev_numbers(three_gen_5(limit=15))))
            if len1 > 9:
                print(f"rev_gen5: {len1}, {p}, {pos}")

            len1 = check_sequence(gen3(p, pos, three_gen_6()), limit=15)
            if len1 > 9:
                print(f"gen6: {len1}, {p}, {pos}")

            len1 = check_sequence(gen3(p, pos, three_gen_7(123, 2011)), limit=30)
            if len1 > 9:
                print(f"gen7: {len1}, {p}, {pos}")

            for j in range(25):
                start = randint(0, 300) * 3
                for k in (3, 6, 9, 12, 15, 18, 21, 24, 27, 30):
                    #step = randint(1, 1000) * 3
                    step = k

                    len1 = check_sequence(gen3(p, pos, three_gen_2(start, step, limit=30)))
                    if len1 > 9:
                        print(f"{len1}, {p}, {pos}, {start}, {step}")

                    len1 = check_sequence(gen3(p, pos, rev_numbers(three_gen_2(start, step, limit=30))))
                    if len1 > 9:
                        print(f"rev: {len1}, {p}, {pos}, {start}, {step}")


                for k in range(5):
                    start += 3
                    fact = randint(2, 20)
                    len1 = check_sequence(gen3(p, pos, three_gen_3(start, fact, limit=15)))

                    if len1 > 9:
                        print(f"fact: {len1}, {p}, {pos}, {start}, {fact}")



if __name__ == "__main__":
    main()
