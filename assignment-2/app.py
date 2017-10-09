import math
import random
import sys

# Local imports
import bbs
from galois import GF
import csdes
import miller_rabin as mr
import modp

def is_prime(n, accuracy=None):
    if accuracy is None:
        accuracy = mr.estimate_accuracy(numbits(n))
    return mr.probably_prime(n, accuracy)

def block_print(number, columns=6, indent="    "):
    modp.block_print(hex(number)[2:-1], columns=columns, indent=indent)

def get_global_params(bits):
    # Domain parameters
    # Choose a prime q so that p=2q+1 is also prime

    acc1 = mr.estimate_accuracy(bits-1)
    acc2 = mr.estimate_accuracy(bits)

    # TODO: This is not entirely correct
    generator = 2

    while True:
        q = mr.find_prime(bits-1, acc1)
        p = 2*q + 1 # used to prevent small subgroup attacks, se Stallings
        if mr.probably_prime(p, acc2):
            return q, p, generator

def numbits(n):
    """Returns the number of bits requires to represent n."""
    return int(math.ceil(math.log(n, 2)))

def dh_exchange(address, puba):
    pass

def generate_keypair(prng, generator, p, q, priv=None):
    if priv is None:
        # Allow to use a predefined private key
        priv = prng.randint(2, q-1)

    F = GF(p)
    g = F(generator)
    pub = g**priv
    return priv, pub

def create_csprng(seed, bits):
    return bbs.BlumBlumShub.create(prime_bits=bits, seed=int(seed))

def encrypt(key, plaintext):
    k1 = (key & 0b11111111110000000000) >> 10
    k2 =  key & 0b1111111111
    return csdes.triplesdes_encrypt_buffer(k1, k2, plaintext)

def encrypt_with_csprng(q, p, seed, plaintext):
    prng = bbs.BlumBlumShub(seed=seed, bits=10, q=q, p=p)
    ciphertext = ""
    for plainbyte in plaintext:
        k1 = prng.get_random_bits(10)
        k2 = prng.get_random_bits(10)
        cipherbyte = csdes.triplesdes_encrypt(k1, k2, plainbyte)
        ciphertext = ciphertext + chr(cipherbyte)
    return ciphertext

def decrypt_with_csprng(q, p, seed, ciphertext):
    prng = bbs.BlumBlumShub(seed=seed, bits=10, q=q, p=p)
    plaintext = ""
    for cipherbyte in map(ord, ciphertext):
        k1 = prng.get_random_bits(10)
        k2 = prng.get_random_bits(10)
        plainbyte = csdes.triplesdes_decrypt(k1, k2, cipherbyte)
        plaintext = plaintext + chr(plainbyte)
    return plaintext

def decrypt(key, ciphertext):
    k1 = (key & 0b11111111110000000000) >> 10
    k2 =  key & 0b1111111111
    return csdes.triplesdes_decrypt_buffer(k1, k2, ciphertext)

def create_shared_key(pubkey, privkey):
    return privkey**pubkey

def send(address, data):
    pass

def log(message):
    sys.stdout.write(message)
    sys.stdout.flush()

def show(label, number, decimal=False, indent="  "):
    number = int(number)
    print("%s%s (%d bits)" % (indent, label, numbits(number)))

    if decimal:
        print("%sHex:" % indent)

    block_print(number)

    if decimal:
        print("")
        print("%sDecimal:" % indent)
        print(number)

def read_file(filename):
    with open(filename, "rb") as f:
        return f.read()

def main():
    bob = "some remote host"
    bits = 128

    log("Finding global %d-bit parameters ... " % bits)
    #q, p, generator = get_global_params(bits)
    group = modp.groups[2048]
    p = group["value"]
    q = (p - 1) // 2

    # Require resistance to sub-group attacks
    assert(2*q + 1 == p)

    # Require usability with Blum Blum Shub CSPRNG
    assert(p != q)
    assert((q % 4) == 3)
    assert((p % 4) == 3)

    generator = group["generator"]
    log("\n")
    #q = 761
    #p = 2*q + 1

    acc = 10
    log("Checking if q is prime (%d rounds) ... " % acc)
    primeq = is_prime(q, acc)
    log("%s\n" % primeq)
    if not primeq:
        raise ValueError("q is not prime: %d" % q)

    log("Checking if p=2q+1 is prime (%d rounds) ... " % acc)
    primep = is_prime(p, acc)
    log("%s\n" % primep)
    if not primep:
        raise ValueError("p is not prime: %d" % q)

    log("Finding Blum Blum Shub q and p=2q+1 %d-bit primes ... " % bits)
    csprng_key = bbs.BlumBlumShub.create(bits)
    log("\n")

    log("Generating %d-bit keypair for Alice ... " % bits)
    #priva, puba = generate_keypair(p, q, 312)
    priva, puba = generate_keypair(csprng_key, generator, p, q)
    log("\n")

    log("Generating %d-bit keypair for Bob ... " % bits)
    #privb, pubb = generate_keypair(p, q, 24)
    privb, pubb = generate_keypair(csprng_key, generator, p, q)
    log("\n")
    log("\n")

    print("Global parameters")
    print("  g = %d (generator)" % generator)
    print("")
    show("q", q)
    print("  prime(q, %d): %s" % (acc, primeq))
    print("")
    show("p (2q+1)", p)
    print("  prime(p, %d): %s" % (acc, primep))
    print("")

    print("Blum Blum Shub parameters")
    show("p", csprng_key.p)
    print("")
    show("q", csprng_key.q)
    print("")
    show("m (Blum number)", csprng_key.m)
    print("")

    print("Alice's keys")
    show("Alice privkey", priva)
    print("")
    show("Alice pubkey", puba)
    print("")

    print("Bob's keys")
    show("Bob privkey", privb)
    print("")
    show("Bob pubkey", pubb)
    print("")

    #pubb = dh_exchange(bob, puba)

    aliceKab = create_shared_key(priva, pubb)
    bobKab = create_shared_key(privb, puba)
    assert(aliceKab == bobKab)
    Kab = aliceKab
    if aliceKab == bobKab:
        show("Shared key", Kab)
        print("")

        if not bbs.is_coprime(Kab, q):
            print("WARNING: Global parameter q is not coprime to shared key")
        if not bbs.is_coprime(Kab, p):
            print("WARNING: Global parameter p is not coprime to shared key")

    log("Initializing %d-bit Blum Blum Shub with shared key as seed ... " % bits)
    csprng = create_csprng(Kab, bits)
    log("\n")
    key = csprng.get_random_bits(20)
    show("20-bit TriplSDES key", key)

    plaintext = read_file("plaintext")
    origplain = plaintext
    print("Plaintext: %r" % plaintext)
    plaintext = map(ord, plaintext)

    ciphertext = encrypt_with_csprng(q, p, key, plaintext)
    print("Ciphertext: %r" % ciphertext)
    # TODO: sha1sum
    #send(cipher, bob)
    plainagain = decrypt_with_csprng(q, p, key, ciphertext)
    print("Plaintext: %r" % plainagain)
    assert(origplain == plainagain)
    print("ROUNDTRIP OK")

if __name__ == "__main__":
    main()
