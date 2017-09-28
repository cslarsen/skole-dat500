def counter(n=0):
    """Yields numbers but swaps two and two numbers:

    0,2,1,4,3,6,5,8,...
    """
    yield n
    n += 2
    while True:
        yield n
        n -= 1
        yield n
        n += 3

for i,n in enumerate(counter()):
    print("%20s %d" % (bin(n)[2:], n))
    if i > 100:
        break
