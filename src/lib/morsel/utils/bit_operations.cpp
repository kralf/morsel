#include "bit_operations.h"

using namespace std;

//------------------------------------------------------------------------------

unsigned int
BitOperations::revertInt( unsigned int val )
{
  unsigned int reverse = val;
  unsigned int shift = sizeof( unsigned int ) * CHAR_BIT - 1;

  for ( val >>= 1; val; val >>= 1 ) {
    reverse <<= 1;
    reverse |= val & 1;
    --shift;
  }
  reverse <<= shift;

  return reverse;
}

//------------------------------------------------------------------------------

unsigned short
BitOperations::revertShort( unsigned short val )
{
  unsigned short reverse = val;
  unsigned short shift = sizeof( unsigned short ) * CHAR_BIT - 1;

  for ( val >>= 1; val; val >>= 1 ) {
    reverse <<= 1;
    reverse |= val & 1;
    --shift;
  }
  reverse <<= shift;

  return reverse;
}

//------------------------------------------------------------------------------

unsigned char
BitOperations::revertByte( unsigned char val )
{
  unsigned char reverse = val;
  unsigned char shift = sizeof( unsigned char ) * CHAR_BIT - 1;

  for ( val >>= 1; val; val >>= 1 ) {
    reverse <<= 1;
    reverse |= val & 1;
    --shift;
  }
  reverse <<= shift;

  return reverse;
}
