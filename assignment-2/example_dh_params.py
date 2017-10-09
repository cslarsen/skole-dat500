from app import generate_dh_params, show
import miller_rabin as mr
import galois

if __name__ == "__main__":
    for bits in (8, 10, 16, 24, 128, 256):
        q, p, g = generate_dh_params(bits)
        print("Example %d-bit Diffie-Hellman global parameters:" % bits)
        print("         q = %d" % q)
        print("           = 0x%x" % q)
        print("  p (2q+1) = %d" % p)
        print("           = 0x%x" % p)

        # find generator
        found = False
        for a in range(2, 10):
            nums = set([n for n in range(q)])
            try:
                for x in range(1, q):
                    num = mr.pow_mod(a, x, q)
                    nums.remove(num)
                if nums == set([0]):
                    found = a
                    break
            except KeyError:
                continue
        if found:
            print("   found g = %d" % found)
        else:
            print("   did not find g in given range")
        print("")
