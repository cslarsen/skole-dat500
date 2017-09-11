// Written by Christian Stigen

#include <stdio.h>
#include <stdint.h>
#include <set>
#include <bitset>

// Create a few typedefs to make it clear what bit width we are operating with.
typedef uint8_t uint2_t;
typedef uint8_t uint4_t;

// CHECKED
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

// CHECKED
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

// CHECKED
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

// CHECKED
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

// CHECKED
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

// CHECKED
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

// CHECKED
// Interchanges the upper and lower 4 bits (nibbles).
extern "C"
uint8_t sw(const uint8_t n)
{
  return uint8_t((n & 0x0f) << 4)
              | ((n & 0xf0) >> 4);
}

// CHECKED VIA shiftl4
// Rotate/roll left 5 LSBs
extern "C"
uint8_t rol5(uint8_t n)
{
  return uint8_t(((n & 0x0f) << 1)   // shift 4 LSBs left
               | ((n & 0x10) >> 4)); // and carry into LSB
}

// CHECKED
// Rotates upper and lower 5 bits separately
extern "C"
uint16_t shiftl5(const uint16_t n)
{
  return uint16_t(
      rol5((n & 0x3e0) >> 5) << 5 // upper five
    | rol5(n & 0x1f));            // lower five
}

// CHECKED
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

// CHECKED
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

// CHECKED
// Generate two 10-bit keys (figure G.2 in paper)
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

  // bits
  // The two here should be equal, but they are not
  //uint8_t n2 = (n & 0x4) >> 2; // bit 2
  //uint8_t n3 = (n & 0x2) >> 1; // bit 3
  //uint8_t n4 = (n & 0x1);      // bit 4
  //uint8_t n1 = (n & 0x8) >> 3; // bit 1

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

// CHECKED
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

int main(int, char**)
{
  triplesdes_encrypt(0,0,0); // silence compiler warning

  // Read binary file
  FILE *fp = fopen("ctx2.bin", "rb");
  if (fp == NULL) {
    perror("ctx1.bin");
    return 1;
  }
  unsigned char buffer[60];
  fread(buffer, sizeof(unsigned char), sizeof(buffer)/sizeof(unsigned char),
      fp);
  fclose(fp);

  printf("Ciphertext:\n");
  for ( size_t n=0; n < sizeof(buffer)/sizeof(unsigned char); ++n ) {
    printf("%2.2x ", buffer[n]);
  }
  printf("\n");

  // Find 20-bit key by brute force.
  int left = (1<<20) - 1; // this is faster than doing a popcount
  std::bitset< ((1<<20) - 1)> keyspace; // takes ~127kb of memory
  keyspace.flip(); // put all keys into the keyspace

  // Find unique ciphertext bytes, to reduce the innerloop
  unsigned char unique[60];
  size_t unique_len = 0;
  {
    std::set<unsigned char> unique_bytes;
    for ( size_t n = 0; n < sizeof(buffer) / sizeof(char); ++n )
      unique_bytes.insert(buffer[n]);
    for ( auto chr : unique_bytes )
      unique[unique_len++] = chr;
  }

  for ( uint16_t k1 = 0; k1 < 1024; ++k1 ) {
    for ( uint16_t k2 = 0; k2 < 1024; ++k2 ) {
      for ( size_t n = 0; n < unique_len; ++n ) {
        const uint8_t out = triplesdes_decrypt(k1, k2, unique[n]);
        if ( out < 32 || out > 126 ) {
          const uint32_t key = uint32_t(k1) << 10 | k2;
          keyspace[key] = 0; // key is not viable, remove it
          left -= 1;
          goto NEXT_K2;
        }
      }
NEXT_K2:
      if ( left <= 1 )
        goto DONE;
      continue;
    }
  }
DONE:
  // Print found key (we could list all candidates here as well, but that
  // usually means we've not really found the right one.)
  uint32_t found_key = 0;
  for ( uint32_t k=0; k < (1<<20)-1; ++k ) {
    if ( keyspace[k] == 1 ) {
      found_key = k;
      if ( left > 1 )
        printf("brute-forced key candidate: 0x%x", k);
      else
        break;
    }
  }

  const uint16_t k1 = (found_key & 0xffc00) >> 10;
  const uint16_t k2 = (found_key & 0x003ff);

  printf("\nusing candidate 20-bit key: 0x%x\n", found_key);
  printf("  k1: 0x%x\n", k1);
  printf("  k2: 0x%x\n", k2);

  printf("\nPlaintext:\n'");
  for ( size_t n=0; n < sizeof(buffer)/sizeof(unsigned char); ++n ) {
    const unsigned char plain = triplesdes_decrypt(k1, k2, buffer[n]);
    printf("%c", plain);
  }
  printf("'\n");

  return 0;
}
