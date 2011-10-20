#ifndef COLOR_H
#define COLOR_H

#include "morsel/morsel.h"

#include <lvecBase4.h>

class Color
{
PUBLISHED:
  static float intToHue( unsigned int val );
  static unsigned int hueToInt( float hue );
  
  static Colorf hsvToRgb( const Colorf & hsv );
  static Colorf rgbToHsv( const Colorf & rgb );
  
  static Colorf intToRgb( unsigned int val );
  static unsigned int rgbToInt( const Colorf & rgb );
  static unsigned int rgbToInt( const Colord & rgb );

  static Colorf roundRgb( const Colorf & rgb );
};

#endif /*COLOR_H*/
