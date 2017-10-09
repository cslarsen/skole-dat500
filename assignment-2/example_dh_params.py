from app import generate_dh_params, show

if __name__ == "__main__":
    for bits in (8, 128, 256):
        q, p, g = generate_dh_params(bits)
        print("Example %d-bit Diffie-Hellman global parameters:" % bits)
        print("  q = %d" % q)
        print("    = 0x%x" % q)
        print("  p = %d" % p)
        print("    = 0x%x" % p)
        print("  g = %d" % g)
