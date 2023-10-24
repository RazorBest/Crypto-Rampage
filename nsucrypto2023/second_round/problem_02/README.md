# Problem 02 - Simple ideas for primes

I propose the following simple construction method: start from a prime number.
Take a sequence whose elements are divisible by 3. Insert the number of the
sequence between the digits of the prime number. Example:
    2011, 29011, 215011, 221011, 227011, 233011, 239011, ...

Where the above sequence is generating by starting from the prime number 2011.
Insert at the second position the arithmetic sequence 9, 15, 21, 27, ... In
this case, the parameters of the arithmetic sequence are (9, 6).

With this generic method of constructing possible prime sequences, I tried
to use it in multiple ways. Generated a random prime number, a random insertion
position, and random parameters for the auxilary sequence.


## Solution

The solve.py script tries a lot of these sequences and prints those with a
high sequence primality parameter. The best sequence found with this method
has the parameter 10, starts from 593, inserting the auxilary sequence after the
first digit. The auxiliary sequence is an arithmetic progression starting from
813, with difference 21. The final sequence is:
    593, 581393, 583493, 585593, 587693, 589793, 591893, 593993, 596093, 598193

The next number is divisible by 11.

## Generalization 

The above mechanism can be generalized. The sequence can be a random number
generator. The nice property about it is that it isn't necessarily increasing. 
I also made sure the number is of some form MOD * k + r. E.g. if we don't want
numbers divisible by 2, 3, 5, we choose 30 * k + r, where r is chosen from
{1, 7, 11, 13, 17, 19, 23, 29}. With this method, we coould find, among
4 digit numbers, even sequences of length 16 (rand_pick.py)

