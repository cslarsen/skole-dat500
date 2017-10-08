"""
Checks how well the Blum Blum Shub CSPRNG gives out uniform numbers.
"""

from bbs import BlumBlumShub
import collections
import sys

prime_bits = 64
nums = 100000
start = 999
stop = start+20-1

print("Initializing CSPRNG w/%d-bit primes" % prime_bits)
rnd = BlumBlumShub.create(prime_bits)

print("Building frequency table of %d numbers ... " % nums)
print("Range: [%d, %d]" % (start, stop))

freqs = collections.Counter()

for n in range(nums):
    number = rnd.randint(start, stop)
    assert(start <= number <= stop)
    freqs.update({number: 1})

    if (n % 10) == 0:
        sys.stdout.write("\r%5.1f%%\r" % (100.0*n/float(nums)))
        sys.stdout.flush()

for k,v in sorted(freqs.items()):
    print("%d: %d times or %f" % (k, v, v/float(nums)))

print("Expected: %f" % (1.0/(stop - start + 1)))
