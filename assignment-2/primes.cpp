// Prime number generator
// Written by Christian Stigen
//
// To compile, you need GNU MP (GMP), and you need to link with it:
// g++ primes.cpp -oprimes -I/.../include -L/.../lib -lgmp -lgmpxx

#include <gmpxx.h>
#include <iostream>
#include <math.h>
#include <stdio.h>

static gmp_randclass *rnd = NULL;

// Calculates a^x mod n
mpz_class pow_mod(mpz_class a, mpz_class x, const mpz_class& n)
{
  // This algorithm is taken from Bruce Schneier's book "Applied Cryptography".
  // See http://en.wikipedia.org/wiki/Modular_exponentiation
  mpz_class r = 1;

  while (x > 0) {
    if ((x & 1) == 1) {
      r = a*r % n;
    }
    x >>= 1;
    a = a*a % n;
  }

  return r;
}

// Sets the random seed.
void initialize_seed(const size_t bytes)
{
  if (!rnd)
    rnd = new gmp_randclass(gmp_randinit_default);

  FILE *f = fopen("/dev/urandom", "rb");
  if (!f) {
    perror("/dev/urandom");
    exit(1);
    return;
  }

  mpz_class seed = 0;
  for ( size_t i = 0; i < bytes; ++i ) {
    int n = fgetc(f);
    seed = (seed << 8) | n;
  }

  fclose(f);
  rnd->seed(seed);
}

mpz_class randint(const mpz_class& lowest, const mpz_class& highest)
{
  if (!rnd)
    initialize_seed(256/8);
  return rnd->get_z_range(highest - lowest) + lowest;
}

// Miller-Rabin primality test
bool prob_prime(const mpz_class& n, const size_t rounds)
{

  if (n <= 1)
    return false;

  if (n == 2 || n == 3)
    return true;

  // Even numbers cannot be prime
  if ((n & 1) == 0)
    return false;

  // Write n-1 as d*2^s by factoring powers of 2 from n-1
  size_t s = 0;
  mpz_class m = n - 1;
  while ((m & 1) == 0) {
    ++s;
    m >>= 1;
  }
  mpz_class d = (n - 1) / (mpz_class(1) << s);

  for (size_t i = 0; i < rounds; ++i) {
    mpz_class a = randint(2, n - 2);
    mpz_class x = pow_mod(a, d, n);

    if (x ==1 || x == (n - 1))
      continue;

    for (size_t r = 0; r < (s-1); ++r) {
      x = pow_mod(x, 2, n);
      if (x == 1)
        return false;
      if (x == n - 1)
        break;
    }

    if (x != (n - 1))
      return false;
  }

  // Probably prime
  return true;
}

int main()
{
  const size_t bits = 256;
  const size_t accuracy = bits/2;

  std::cout << "Finding two " << bits
    << "-bit prime number q and p so that p=2q+1" << std::endl;

  mpz_class low = 1;
  low <<= (bits-1);

  mpz_class high = 1;
  high <<= bits;
  high -= 1;

  for (;;) {
    mpz_class q = randint(low, high);

    // Skip even numbers
    if ((q & 1) == 0)
      continue;

    // Speed up by simple check
    if (!prob_prime(q, 5))
      continue;

    if (prob_prime(q, accuracy)) {
      mpz_class p = 2*q + 1;

      if (prob_prime(p, accuracy)) {
        std::cout << q << std::endl;
        std::cout << p << std::endl;
        break;
      }
    }
  }
}
