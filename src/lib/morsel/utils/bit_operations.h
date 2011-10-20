#ifndef BIT_OPERATIONS_H
#define BIT_OPERATIONS_H

#include "morsel/morsel.h"

class BitOperations
{
PUBLISHED:
  static unsigned int revertInt( unsigned int val );
  static unsigned short revertShort( unsigned short val );
  static unsigned char revertByte( unsigned char val );
};

#endif /*BIT_OPERATIONS_H*/
