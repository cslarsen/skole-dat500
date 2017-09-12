// Simplified DES (SDES) primitive library with a fast key recovery capability.
//
// This source is written in pure C++11 source, and can be compiled both as a
// program and a shared library. There is a ctypes-based Python library to
// drive it, if needed.
//
// NOTE: This program expects to read the file in *binary* format. But you can
// use a Python driver program to do that.
//
// On an old 2010 Core i7 machine, it finds a 20-bit TripleSDES key and
// retrieves the plaintext in 60 milliseconds.
//
// This program is part of the coursework for DAT-510 at University of
// Stavanger autumn 2017.
//
// Written by Christian Stigen

// TODO: Use uint8_t instead of unsigned char, everywhere

#include <bitset>
#include <set>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Create a few typedefs to make it clear which bit widths the various
// functions operate with.

typedef uint8_t uint2_t;
typedef uint8_t uint4_t;

// Define a few structs for returning results

struct bruteforce_result {
  uint32_t count;
  uint32_t key;
};

struct buffer {
  uint32_t length;
  uint8_t* data;
};

extern "C"
uint16_t p10(const uint16_t n)
{
  return uint16_t(
      (n &  0x80) << 2  // bit  3
    | (n & 0x020) << 3  // bit  5
    | (n & 0x100) >> 1  // bit  2
    | (n &   0x8) << 3  // bit  7
    | (n &  0x40) >> 1  // bit  4
    | (n &   0x1) << 4  // bit 10
    | (n & 0x200) >> 6  // bit  1
    | (n &   0x2) << 1  // bit  9
    | (n &   0x4) >> 1  // bit  8
    | (n &  0x10) >> 4  // bit  6
  );
}

extern "C"
uint8_t p8(const uint16_t n)
{
  return uint8_t(
      (n & 0x10) << 3  // bit  6
    | (n & 0x80) >> 1  // bit  3
    | (n &  0x8) << 2  // bit  7
    | (n & 0x40) >> 2  // bit  4
    | (n &  0x4) << 1  // bit  8
    | (n & 0x20) >> 3  // bit  5
    | (n &  0x1) << 1  // bit 10
    | (n &  0x2) >> 1  // bit  9
  );
}

extern "C"
uint8_t p4(const uint4_t n)
{
  return uint8_t(
      (n & 0x4) << 1  // bit 2
    | (n & 0x1) << 2  // bit 4
    | (n & 0x2)       // bit 3
    | (n & 0x8) >> 3  // bit 1
  );
}

extern "C"
uint8_t ip(const uint8_t n)
{
  return uint8_t(
      (n & 0x40) << 1  // bit 2
    | (n &  0x4) << 4  // bit 6
    | (n & 0x20)       // bit 3
    | (n & 0x80) >> 3  // bit 1
    | (n & 0x10) >> 1  // bit 4
    | (n &  0x1) << 2  // bit 8
    | (n &  0x8) >> 2  // bit 5
    | (n &  0x2) >> 1  // bit 7
  );
}

extern "C"
uint8_t revip(const uint8_t n)
{
  return uint8_t(
      (n & 0x10) << 3  // bit 4
    | (n & 0x80) >> 1  // bit 1
    | (n & 0x20)       // bit 3
    | (n &  0x8) << 1  // bit 5
    | (n &  0x2) << 2  // bit 7
    | (n & 0x40) >> 4  // bit 2
    | (n &  0x1) << 1  // bit 8
    | (n &  0x4) >> 2  // bit 6
  );
}

extern "C"
uint8_t ep(const uint4_t n)
{
  return uint8_t(
      (n & 0x1) << 7  // bit 4
    | (n & 0x8) << 3  // bit 1
    | (n & 0x4) << 3  // bit 2
    | (n & 0x2) << 3  // bit 3
    | (n & 0x4) << 1  // bit 2
    | (n & 0x2) << 1  // bit 3
    | (n & 0x1) << 1  // bit 4
    | (n & 0x8) >> 3  // bit 1
  );
}

// Interchanges the upper and lower 4 bits (nibbles).
extern "C"
uint8_t sw(const uint8_t n)
{
  return uint8_t((n & 0x0f) << 4)
              | ((n & 0xf0) >> 4);
}

// Rotate/roll left 5 LSBs
extern "C"
uint8_t rol5(uint8_t n)
{
  return uint8_t(((n & 0x0f) << 1)   // shift 4 LSBs left
               | ((n & 0x10) >> 4)); // and carry into LSB
}

// Rotates upper and lower 5 bits separately
extern "C"
uint16_t shiftl5(const uint16_t n)
{
  return uint16_t(
      rol5((n & 0x3e0) >> 5) << 5 // upper five
    | rol5(n & 0x1f));            // lower five
}

// The S0 s-box
extern "C"
uint2_t S0(const uint2_t row, const uint2_t col)
{
  static uint8_t box[4][4] = {
    {1, 0, 3, 2},
    {3, 2, 1, 0},
    {0, 2, 1, 3},
    {3, 1, 3, 2}
  };

  return box[row][col];
}

// The S1 s-box
extern "C"
uint2_t S1(const uint2_t row, const uint2_t col)
{
  static uint8_t box[4][4] = {
    {0, 1, 2, 3},
    {2, 0, 1, 3},
    {3, 0, 1, 0},
    {2, 1, 0, 3}
  };

  return box[row][col];
}

// Generates two 10-bit keys (figure G.2 in SDES paper).
extern "C"
uint32_t create_subkeys(const uint16_t key)
{
  uint16_t k2 = shiftl5(p10(key));
  const uint16_t k1 = p8(k2);
  k2 = p8(shiftl5(shiftl5(k2)));
  return (uint32_t(k1) << 10) | k2;
}

extern "C"
uint8_t Fmap(uint4_t n, const uint8_t sk)
{
  n = ep(n);

  // All of the following variables hold single bits.

  const uint8_t n4 = (n & 0x80) >> 7;
  const uint8_t n1 = (n & 0x40) >> 6;
  const uint8_t n2 = (n & 0x20) >> 5;
  const uint8_t n3 = (n & 0x10) >> 4;

  const uint8_t k11 = (sk & 0x80) >> 7;
  const uint8_t k12 = (sk & 0x40) >> 6;
  const uint8_t k13 = (sk & 0x20) >> 5;
  const uint8_t k14 = (sk & 0x10) >> 4;
  const uint8_t k15 = (sk & 0x08) >> 3;
  const uint8_t k16 = (sk & 0x04) >> 2;
  const uint8_t k17 = (sk & 0x02) >> 1;
  const uint8_t k18 = (sk & 0x01);

  const uint8_t p00 = n4 ^ k11;
  const uint8_t p01 = n1 ^ k12;
  const uint8_t p02 = n2 ^ k13;
  const uint8_t p03 = n3 ^ k14;

  const uint8_t p10 = n2 ^ k15;
  const uint8_t p11 = n3 ^ k16;
  const uint8_t p12 = n4 ^ k17;
  const uint8_t p13 = n1 ^ k18;

  const uint2_t row1 = S0(uint8_t(p00 << 1 | p03),
                          uint8_t(p01 << 1 | p02));

  const uint2_t row2 = S1(uint8_t(p10 << 1 | p13),
                          uint8_t(p11 << 1 | p12));

  return p4(uint4_t(row1 << 2) | uint4_t(row2));
}

extern "C"
uint8_t fK(const uint8_t sk, const uint8_t n)
{
  const uint4_t l = (n & 0xf0) >> 4;
  const uint4_t r = (n & 0x0f);
  return uint8_t(r | (l ^ Fmap(r, sk)) << 4);
}

extern "C"
uint8_t encrypt(const uint16_t key, const uint8_t plaintext)
{
  const uint32_t sks = create_subkeys(key);
  const uint16_t k1 = (sks & 0xffc00) >> 10;
  const uint16_t k2 = (sks & 0x3ff);
  return revip(fK(k2 & 0xff, sw(fK(k1 & 0xff, ip(plaintext)))));
}

extern "C"
uint8_t decrypt(const uint16_t key, const uint8_t ciphertext)
{
  const uint32_t sks = create_subkeys(key);
  const uint16_t k1 = (sks & 0xffc00) >> 10;
  const uint16_t k2 = (sks & 0x3ff);
  return revip(fK(k1 & 0xff, sw(fK(k2 & 0xff, ip(ciphertext)))));
}

extern "C"
uint8_t triplesdes_encrypt(
    const uint16_t k1,
    const uint16_t k2,
    const uint8_t p)
{
  return encrypt(k1, decrypt(k2, encrypt(k1, p)));
}

extern "C"
uint8_t triplesdes_decrypt(
    const uint16_t k1,
    const uint16_t k2,
    const uint8_t c)
{
  return decrypt(k1, encrypt(k2, decrypt(k1, c)));
}

extern "C"
struct buffer* malloc_buffer(const uint32_t size)
{
  struct buffer* p = static_cast<struct buffer*>(malloc(sizeof(struct buffer)));
  p->length = 0;
  p->data = static_cast<uint8_t*>(malloc(sizeof(uint8_t)*size));
  return p;
}

extern "C"
void free_buffer(struct buffer* p)
{
  if ( p != NULL ) {
    if ( p->data != NULL )
      free(p->data);
    free(p);
  }
}

extern "C"
struct buffer* triplesdes_decrypt_buffer(
    const uint16_t k1,
    const uint16_t k2,
    const uint32_t length,
    const uint8_t* ciphertext)
{
  struct buffer* out = malloc_buffer(length);
  out->length = length;

  for ( size_t n = 0; n < length; ++n )
    out->data[n] = triplesdes_decrypt(k1, k2, ciphertext[n]);

  return out;
}

extern "C"
struct bruteforce_result bruteforce_sdes_key(
    const uint8_t* ciphertext,
    const uint32_t length,
    const uint8_t filter_start,
    const uint8_t filter_end)
{
  std::bitset<1024> keyspace;
  keyspace.flip(); // All keys are initially candidates

  // Find unique cipher text bytes. This set is usually very small: The 60-byte
  // ciphertext is now reduced to 18 bytes. TripleSDES also seems to have very
  // low entropy, since a good symmetric cipher would use the full range of 256
  // bytes. Of course, it's an educational cipher.
  unsigned char unique[length];
  size_t unique_len = 0;
  {
    std::set<unsigned char> unique_bytes;

    for ( size_t n = 0; n < length;  ++n )
      unique_bytes.insert(ciphertext[n]);

    for ( auto chr : unique_bytes )
      unique[unique_len++] = chr;
  }

  for ( size_t key = 0; key < 1024; ++key ) {
    for ( size_t n = 0; n < unique_len; ++n) {
      const auto byte = decrypt(key, unique[n]);
      if ( byte < filter_start || byte > filter_end )
        keyspace[key] = 0;
    }
    if ( keyspace.count() <= 1 )
      break;
  }

  bruteforce_result r;
  r.count = uint32_t(keyspace.count());
  r.key = 0;

  for ( size_t n = 0; n < 1024; ++n ) {
    if ( keyspace[n] == 1 ) {
      r.key = n;
      break;
    }
  }

  return r;
}

// Finds a 20-bit TripleSDES key by brute force
//
// Args:
//   - ciphertext: Raw binary ciphertext to break
//   - length: Number of bytes in ciphertext
//   - filter_start, filter_end: Discard decrypted bytes that fall outside of
//       this range. A good defaul is to use 32 and 126, i.e. discard any keys
//       that do not produce decrypted bytes that fall within the visible ASCII
//       range.
//
//  Returns:
//    A struct containing number of 20-keys found to produce decrypted bytes in
//    the given range, and the first of those keys. Tweak the filter range so
//    that you get one key, then try to decrypt the ciphertext using that key.
extern "C"
struct bruteforce_result bruteforce_3sdes_key(
    const uint8_t* ciphertext,
    const uint32_t length,
    const uint8_t filter_start,
    const uint8_t filter_end)
{
  // Number of keys left in candidate set. Using a counter is faster than
  // continually doing a popcount on the bitset.
  int keysleft = (1<<20) - 1;

  // Use a bitset to contain candidate 20-bit keys (consisting of k1 and k2).
  // If a bit is set, it is still a candidate. Using a bitset takes only ~128
  // kb of memory and has constant lookups.
  std::bitset< ((1<<20) - 1)> keyspace;
  keyspace.flip(); // All keys are initially candidates

  // Find unique cipher text bytes. This set is usually very small: The 60-byte
  // ciphertext is now reduced to 18 bytes. TripleSDES also seems to have very
  // low entropy, since a good symmetric cipher would use the full range of 256
  // bytes. Of course, it's an educational cipher.
  unsigned char unique[60];
  size_t unique_len = 0;
  {
    std::set<unsigned char> unique_bytes;

    for ( size_t n = 0; n < length;  ++n )
      unique_bytes.insert(ciphertext[n]);

    for ( auto chr : unique_bytes )
      unique[unique_len++] = chr;
  }

  // Make encryption lookup table. It only takes 256 kb, and memory is cheap.
  uint8_t encrypted[1024][256]; // (key, byte)
  for ( uint16_t key = 0; key < 1024; ++key )
    for ( uint16_t b = 0; b < 256; ++b )
      encrypted[key][b] = encrypt(key, uint8_t(b));

  // Try all k1 keys
  for ( uint16_t k1 = 0; k1 < 1024; ++k1 ) {
    // Populate lookup table for use in innerloops. Since we only scan k1 once,
    // we don't win anything by calculating this before this loop.
    unsigned char decrypted[256]; // (k1, byte)
    for ( unsigned n = 0; n < 256; ++n )
      decrypted[n] = decrypt(k1, uint8_t(n));

    // Try all k2 keys
    for ( uint16_t k2 = 0; k2 < 1024; ++k2 ) {
      for ( size_t n = 0; n < unique_len; ++n ) {
        // Perform triplesdes_decrypt in steps. This is faster than doing:
        //     auto byte = triplesdes_decrypt(k1, k2, unique[n])
        uint8_t byte = unique[n];
        byte = decrypted[byte];     // decrypt(k1, byte)
        byte = encrypted[k2][byte]; // encrypt(k2, byte);
        byte = decrypted[byte];     // decrypt(k1, byte)

        // Does the keys k1 and k2 decrypt this ciphertext byte a *visible*
        // 7-bit ASCII character?
        if ( byte < filter_start || byte > filter_end ) {
          const uint32_t key = uint32_t(k1) << 10 | k2;
          keyspace[key] = 0; // remove key from candidate set
          keysleft -= 1;
          goto NEXT_K2;
        }
      }
NEXT_K2:
      // This exactly when GOTO is considered beneficial. When we've found a
      // single key-pair that seem to work, we bail out.
      if ( keysleft <= 1 )
        goto DONE;
    }
  }

DONE:
  bruteforce_result result;
  result.count = uint32_t(keyspace.count());
  result.key = 0;

  // Unfortunately, std::bitset doesn't have any nice way of finding the MSB,
  // so we'll just iterate.
  for ( uint32_t k=0; k < (1<<20)-1; ++k ) {
    if ( keyspace[k] == 1 ) {
      result.key = k;
      break;
    }
  }

  return result;
}

size_t readfile(const char* filename, unsigned char* buffer, const size_t length)
{
  FILE *fp = fopen(filename, "rb");

  if ( fp == NULL ) {
    perror(filename);
    exit(1);
  }

  size_t result = fread(buffer, sizeof(unsigned char), length, fp);
  fclose(fp);

  if ( result != length ) {
    perror(filename);
    return 0;
  }

  return result;
}

int main(int, char**)
{
  const size_t length = 60;
  unsigned char ciphertext[length];
  readfile("ctx2.bin", ciphertext, length);

  printf("Ciphertext:\n  ");
  for ( size_t n = 0; n < length; ++n )
    printf("%2.2x%s", ciphertext[n], !((n+1) % 16) ? "\n  " : " ");
  printf("\n\n");

  printf("Brute-forcing 20-bit key ... ");
  fflush(stdout);

  const auto bf = bruteforce_3sdes_key(ciphertext, length, 32, 126);

  printf("found %u keys\n", bf.count);
  fflush(stdout);

  const uint16_t k1 = (bf.key & 0xffc00) >> 10;
  const uint16_t k2 = (bf.key & 0x003ff);

  printf("  20-bit key: 0x%5.5x\n", bf.key);
  printf("  10-bit k1:    0x%3.3x\n", k1);
  printf("  10-bit k2:    0x%3.3x\n", k2);
  printf("\n");

  printf("Plaintext:\n");

  printf("  ");
  for ( size_t n = 0; n < length; ++n ) {
    const auto plaintext = triplesdes_decrypt(k1, k2, ciphertext[n]);
    printf("%2.2x%s", plaintext, !((n+1) % 16) ? "\n  " : " ");
  }
  printf("\n\n");

  printf("ASCII:\n  '");
  for ( size_t n = 0; n < length; ++n ) {
    const auto plaintext = triplesdes_decrypt(k1, k2, ciphertext[n]);
    printf("%c", plaintext);
  }
  printf("'\n\n");

  return 0;
}
