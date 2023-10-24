from math import log, gcd
from random import randint
from Crypto.Util.number import isPrime

start_prime = [2, 3, 5, 11, 13, 17]
MOD = 1
for p in start_prime:
    MOD *= p

vprime = []
for x in range(MOD):
    if gcd(x, MOD) == 1:
        vprime.append(x)

def simulate_choice_ndigits(ndigits, limit=20000):
    # Let k be chosen randomly between low an high
    # Let i be chosen randomly between 0 and 7 - an index of the vprime list
    # We will choose x = MOD*k + vprime[i] = MOD*k + r, r < MOD
    # We want x to have about n digits:
    # 10^(n-1) <= MOD*k + r < 10^(n)
    # (10^(n-1) - r)/MOD <= k < (10^n - r)/MOD
    # (10^(n-1) - 29)/MOD <= k < (10^n - 1)/MOD
    # We can approximate, is n is big enough:
    # 10^(n-1)/MOD <= k < 10^n/MOD
    low = int(10**(ndigits-1) / MOD)
    high = int(10**ndigits / MOD - 1)

    longest_line = 0
    curr_count = 0
    for _ in range(limit):
        k = randint(low, high)
        i = randint(0, len(vprime) - 1)
        x = MOD*k + vprime[i]

        if isPrime(x):
            curr_count += 1
            continue

        longest_line = max(longest_line, curr_count)
        curr_count = 0

    return longest_line

for i in range(4, 20):
    line = simulate_choice_ndigits(i)
    print(f"ndigits={i}; longest: {line}")
