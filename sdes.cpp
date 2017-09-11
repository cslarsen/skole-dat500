#include <stdio.h>
#include <stdint.h>

// CHECKED
static uint16_t p10(const uint16_t& n)
{
  return (n &  0x80) << 2  // bit  3
       | (n & 0x020) << 3  // bit  5
       | (n & 0x100) >> 1  // bit  2
       | (n &   0x8) << 3  // bit  7
       | (n &  0x40) >> 1  // bit  4
       | (n &   0x1) << 4  // bit 10
       | (n & 0x200) >> 6  // bit  1
       | (n &   0x2) << 1  // bit  9
       | (n &   0x4) >> 1  // bit  8
       | (n &  0x10) >> 4; // bit  6
}

// CHECKED
static uint8_t p8(const uint16_t& n)
{
    return (n & 0x10) << 3  // bit  6
         | (n & 0x80) >> 1  // bit  3
         | (n &  0x8) << 2  // bit  7
         | (n & 0x40) >> 2  // bit  4
         | (n &  0x4) << 1  // bit  8
         | (n & 0x20) >> 3  // bit  5
         | (n &  0x1) << 1  // bit 10
         | (n &  0x2) >> 1; // bit  9
}

// CHECKED
static uint8_t p4(const uint8_t& n)
{
    return (n & 0x4) << 1  // bit 2
         | (n & 0x1) << 2  // bit 4
         | (n & 0x2)       // bit 3
         | (n & 0x8) >> 3; // bit 1
}

// CHECKED
static uint8_t ip(const uint8_t& n)
{
    return (n & 0x40) << 1  // bit 2
         | (n &  0x4) << 4  // bit 6
         | (n & 0x20)       // bit 3
         | (n & 0x80) >> 3  // bit 1
         | (n & 0x10) >> 1  // bit 4
         | (n &  0x1) << 2  // bit 8
         | (n &  0x8) >> 2  // bit 5
         | (n &  0x2) >> 1; // bit 7
}

// CHECKED
static uint8_t revip(const uint8_t& n)
{
  return (n & 0x10) >> 3  // bit 4
       | (n & 0x80) >> 1  // bit 1
       | (n & 0x20)       // bit 3
       | (n &  0x8) << 1  // bit 5
       | (n &  0x2) << 2  // bit 7
       | (n & 0x40) >> 4  // bit 2
       | (n &  0x1) << 1  // bit 8
       | (n &  0x4) >> 2; // bit 6
}

// CHECKED
static uint8_t ep(const uint8_t& n)
{
  return (n & 0x1) << 7  // bit 4
       | (n & 0x8) << 3  // bit 1
       | (n & 0x4) << 3  // bit 2
       | (n & 0x2) << 3  // bit 3
       | (n & 0x4) << 1  // bit 2
       | (n & 0x2) << 1  // bit 3
       | (n & 0x1) << 1  // bit 4
       | (n & 0x8) >> 3; // bit 1
}

// CHECKED
// Interchanges the upper and lower 4 bits (nibbles).
static uint8_t sw(const uint8_t& n)
{
  return ((n & 0xf) << 4) | ((n & 0xf0) >> 4);
}

// CHECKED VIA shiftl4
// Rotate/roll left 5 LSBs
static uint8_t rol5(uint8_t n)
{
  return ((n & 0x0f) << 1)  // shift 4 LSBs left
       | ((n & 0x10) >> 4); // and carry into LSB
}

// CHECKED
// Rotates upper and lower 5 bits separately
static uint16_t shiftl5(const uint16_t& n)
{
  return rol5((n & 0x3e0) >> 5) << 5 // upper five
       | rol5(n & 0x1f); // lower five
}

// CHECKED
static uint8_t S0(const uint8_t& row, const uint8_t& col)
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
static uint8_t S1(const uint8_t& row, const uint8_t& col)
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
static uint32_t create_subkeys(const uint32_t& key)
{
  uint16_t k2 = shiftl5(p10(key));
  const uint16_t k1 = p8(k2);
  k2 = p8(shiftl5(shiftl5(k2)));
  return (k1 << 10) | k2;
}


static uint8_t Fmap(uint8_t n, const uint8_t& sk)
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

  // bits
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

  const uint8_t row1 = S0(p00 << 1 | p03, p01 << 1 | p02);
  const uint8_t row2 = S1(p10 << 1 | p13, p11 << 1 | p12);

  return p4(row1 << 2 | row2);
}

// CHECKED
static uint8_t f(const uint16_t& sk, const uint8_t& n)
{
  const uint8_t l = (n & 0xf0) >> 4;
  const uint8_t r = (n & 0x0f);
  return ((l ^ Fmap(r, sk)) << 4) | r;
}

static uint8_t encrypt(const uint32_t& key, const uint8_t& plaintext)
{
  const uint32_t sks = create_subkeys(key);
  const uint16_t k1 = (sks & 0xffc00) >> 10;
  const uint16_t k2 = (sks & 0x3ff);
  return revip(f(k2, sw(f(k1, ip(plaintext)))));
}

static uint8_t decrypt(const uint32_t& key, const uint8_t& ciphertext)
{
  const uint32_t sks = create_subkeys(key);
  const uint16_t k1 = (sks & 0xffc00) >> 10;
  const uint16_t k2 = (sks & 0x3ff);
  return revip(f(k1, sw(f(k2, ip(ciphertext)))));
}

int main(int, char**)
{
  // Read binary file
  FILE *fp = fopen("ctx1.bin", "rb");
  if (fp == NULL) {
    perror("ctx1.bin");
    return 1;
  }
  unsigned char buffer[60] = {0};
  fread(buffer, sizeof(unsigned char), sizeof(buffer)/sizeof(unsigned char),
      fp);
  fclose(fp);

  printf("Ciphertext:\n");
  for ( int n=0; n<60; ++n ) {
    printf("%2.2x ", buffer[n]);
  }
  printf("\n");

  // Decode with known key
  const uint16_t k1 = 0x15f;
  const uint16_t k2 = 0x3ea;
  const uint32_t key = (k1 << 10) | k2; // 0xfa95f

  printf("\nPlaintext:\n");
  for ( int n=0; n<60; ++n ) {
    const unsigned char plain = decrypt(key, buffer[n]);
    printf("%c", plain);
  }
  printf("\n");

  return 0;
}
