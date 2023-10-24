Trying to bruteforce the cipher, and looking at bigrams, I noticed some words:
	- newest
	- atrise
	- airseen

Breaking these words, we get NEW, AT, RISE, AIR, SEEN.

The cubes, in 2D, look like below:

R T S
  A
  I
  E

E S E
  A
  N
  W

With the sides numbered like this:

The first cube:
5 1 6
  2
  3
  4

The second cube:
11 7 12
  8
  9
  10

After trying by hand combinations of the found words (the ones that are above), I got: SEE NEWS AT AIR.

The walking order would be: 6 -> 4 -> (jump) 12 -> 9 -> 11 -> 10 -> 7 -> 8 -> (jump) 1 -> 2 -> 3 -> 5.

The jumps happen between 4 and 12, and 8 and 1. Both edges are valid.

