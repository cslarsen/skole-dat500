import collections
import csdes

def counter(n=0, mod=256):
    """Yields numbers but swaps two and two numbers:

    0,2,1,4,3,6,5,8,...
    """
    yield n % mod
    n += 2
    while True:
        yield n % mod
        n -= 1
        yield n % mod
        n += 3

for i,n in enumerate(counter()):
        break

def csprng(seed):
    key1 = seed & 0b11111111110000000000
    key2 = seed & 0b00000000001111111111

    new_digit = counter()
    buflen = 100
    while True:
        # Fill up a buffer of digits
        digits = [0]*buflen
        for n in range(buflen):
            digits[n] = new_digit.next()

        # Encrypt buffer
        encrypted = csdes.triplesdes_decrypt_buffer(key1, key2,
                "".join(map(chr, digits)))
        for n in encrypted:
            yield ord(n)

    # Old slow way:
    #digits = []
    #for n in range(buflen):
    #for digit in counter():
        #yield csdes.triplesdes_encrypt(key1, key2, digit)

def create_seed(length):
    # Read three bytes and use that to produce a 20-bit seed
    with open("/dev/urandom", "rb") as f:
        bytes = f.read(length)
        seed = 0
        for n in range(length):
            seed = seed << 8 | ord(bytes[n])
        return seed

if __name__ == "__main__":
    seed = create_seed(3) & 0xfffff
    print("seed: 0x%x" % seed)

    count = 100000
    print("Generating %d digits" % count)
    digits = []

    for i, n in enumerate(csprng(seed)):
        digits.append(n)
        if i >= count:
            break

    print("First 10 digits: %s" % " ".join(map(str, digits[:10])))

    print("Frequency table:")
    unique_counts = set()
    for digit, occurrences in sorted(collections.Counter(digits).items()):
        unique_counts.add(occurrences)

    print("Unique counts:")
    for n in sorted(unique_counts):
        print(n)

