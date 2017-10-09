"""
DAT-510 Assignment 2, autumn 2017

All code written by Christian Stigen
"""

import argparse
import pickle
import math
import random
import socket
import sys
import threading

# Local imports
import bbs
from galois import GF, IntMod
import csdes
import miller_rabin as mr
import modp

class Connection(object):
    def __init__(self, q, p, bits, privkey, pubkey, port, remote_host=None):
        self.q = q
        self.p = p
        self.bits = bits
        self.privkey = privkey
        self.pubkey = pubkey
        self.port = port
        self.remote_host = remote_host

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("localhost", self.port))
        server.listen(1)
        log("Waiting for connections on port %d\n" % self.port)

        while True:
            connection, address = server.accept()
            self.exchange_keys(connection)
            connection.close()
        server.close()

    def start_client(self):
        log("Connecting to remote host %s:%d ... " % (self.remote_host,
            self.port))
        remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote.connect((self.remote_host, self.port))
        log("\n")
        self.exchange_keys(remote)

    def prompt(self, prefix):
        if sys.version_info.major <= 3:
            return raw_input(prefix)
        else:
            return input(prefix)

    def exchange_keys(self, remote, buflen=4096):
        log("Sending our public key\n")
        remote.send(pickle.dumps({"pubkey": int(self.pubkey)}))
        print("")

        log("Receiving remote public key\n")
        reply = pickle.loads(remote.recv(buflen))
        if "pubkey" in reply:
            remote_pubkey = reply["pubkey"]
            remote_pubkey = IntMod(remote_pubkey, self.pubkey.mod)

            show("Remote pubkey", remote_pubkey)
            print("")

            log("Creating shared key\n")
            Kab = create_shared_key(self.privkey, remote_pubkey)
            show("Shared key Kab", Kab)
            print("")

            # Create a shared CSPRNG for use in communication.
            # NOTE: Since this is a CHAT and not a one-off file transfer, we
            # may QUICKLY get into syncing issues, as in the position in the
            # PRNG may drift.
            seed = int(Kab)
            shared_prng = bbs.BlumBlumShub(seed, self.p, self.q, bits=10)

            def encrypt(plaintext):
                return encrypt_with_csprng(shared_prng, map(ord, plaintext))

            def decrypt(ciphertext):
                return decrypt_with_csprng(shared_prng, ciphertext)

            # Start chat
            self.chat(encrypt, decrypt, remote)

    def chat(self, encrypt, decrypt, remote, buffer_length=4096):
        log("*** Entering encrypted chat. Hit CTRL+D to exit ***\n\n")

        def receive():
            while True:
                reply = remote.recv(buffer_length)
                if len(reply) > 0:
                    print("Encrypted reply: %r" % reply)
                    reply = decrypt(reply)
                    print("Decrypted reply: %s" % reply)

        try:
            # Start a background thread to receive
            thread = threading.Thread(target=receive)
            thread.start()

            while True:
                message = encrypt(self.prompt("You: "))
                print("Encrypted message: %r" % message)
                remote.send(message)
        finally:
            sys.exit(0)

def is_prime(n, accuracy=None):
    if accuracy is None:
        accuracy = mr.estimate_accuracy(numbits(n))
    return mr.probably_prime(n, accuracy)

def block_print(number, columns=6, indent="    "):
    modp.block_print(hex(number)[2:-1], columns=columns, indent=indent)

def generate_dh_params(bits):
    """Generates Diffie-Hellman global parameters p and q.

    Returns:
        A tuple of integers (q, p, generator)
    """
    # Domain parameters
    # Choose a prime q so that p=2q+1 is also prime

    acc1 = mr.estimate_accuracy(bits-1)
    acc2 = mr.estimate_accuracy(bits)

    # TODO: THis is not correct, must use discrete logarithm approach to
    # actually find it. See example_dh_params.py
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

def create_csprng(q, p, seed, bits):
    return bbs.BlumBlumShub.create(q=q, p=p, prime_bits=bits, seed=int(seed))
    return bbs.BlumBlumSHub(int(seed), p, q)

def encrypt(key, plaintext):
    k1 = (key & 0b11111111110000000000) >> 10
    k2 =  key & 0b1111111111
    return csdes.triplesdes_encrypt_buffer(k1, k2, plaintext)

def encrypt_with_csprng(prng, plaintext):
    ciphertext = ""
    for plainbyte in plaintext:
        k1 = prng.next()
        k2 = prng.next()
        cipherbyte = csdes.triplesdes_encrypt(k1, k2, plainbyte)
        ciphertext = ciphertext + chr(cipherbyte)
    return ciphertext

def decrypt_with_csprng(prng, ciphertext):
    plaintext = ""
    for cipherbyte in map(ord, ciphertext):
        k1 = prng.next()
        k2 = prng.next()
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

def show(label, number, indent="  "):
    number = int(number)
    print("%s%s (%d bits)" % (indent, label, numbits(number)))
    block_print(number, indent=indent*2)

def read_file(filename):
    with open(filename, "rb") as f:
        return f.read()

def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument("-b", "--bits", type=int, default=512,
            help="Number of bits for Blum Blum Shub (default 512)")

    p.add_argument("--filename", type=str, default="plaintext",
            help="File to send between the two parties")

    p.add_argument("--group", type=int, default=2048,
            help="IKE cyclic group to use: %s (default 2048)" %
                ", ".join(map(str, modp.groups.keys())))

    p.add_argument("--port", type=int, default=45678,
            help="Port number (default 45678)")

    p.add_argument("--remote-host", type=str, default=None,
            help="Address of remote host")

    opts = p.parse_args()
    return opts

def main(opts):
    bits = opts.bits

    log("Finding global %d-bit parameters ... " % bits)
    #q, p, generator = generate_dh_params(bits)
    group = modp.groups[opts.group]
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

    print("Blum Blum Shub parameters for generating keys")
    show("p", csprng_key.p)
    print("")
    show("q", csprng_key.q)
    print("")
    show("m (Blum number)", csprng_key.m)
    print("")

    print("Global Diffie-Hellman (mod p) parameters")
    print("  g = %d (generator)" % generator)
    print("")
    show("q", q)
    print("  prime(q, %d): %s" % (acc, primeq))
    print("")
    show("p (2q+1)", p)
    print("  prime(p, %d): %s" % (acc, primep))
    print("")

    log("Generating %d-bit keypair ... " % bits)
    privkey, pubkey = generate_keypair(csprng_key, generator, p, q)
    log("\n")

    print("Our keys")
    show("privkey", privkey)
    print("")
    show("pubkey", pubkey)
    print("")

    # Exchange keys over TCP/IP
    net = Connection(q, p, bits, privkey, pubkey, opts.port, opts.remote_host)
    if net.remote_host is None:
        net.start_server()
    else:
        net.start_client()

if __name__ == "__main__":
    if sys.version_info.major >= 3:
        print("WARNING: This program currently only supports Python 2.7")
        print("         You have Python 3. It will stop at the chat part!")
        print("")

    opts = parse_args()
    main(opts)
