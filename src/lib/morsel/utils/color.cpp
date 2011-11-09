/***************************************************************************
*  Copyright (C) 2011 by Ralf Kaestner                                   *
*  ralf.kaestner@gmail.com                                               *
*                                                                        *
*  This program is free software; you can redistribute it and/or modify  *
*  it under the terms of the GNU General Public License as published by  *
*  the Free Software Foundation; either version 2 of the License, or     *
*  (at your option) any later version.                                   *
*                                                                        *
*  This program is distributed in the hope that it will be useful,       *
*  but WITHOUT ANY WARRANTY; without even the implied warranty of        *
*  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
*  GNU General Public License for more details.                          *
*                                                                        *
*  You should have received a copy of the GNU General Public License     *
*  along with this program; if not, write to the                         *
*  Free Software Foundation, Inc.,                                       *
*  59 Temple Place-Suite 330, Boston, MA  02111-1307, USA.             *
 ***************************************************************************/

#include "color.h"

#include "bit_operations.h"

#include <cmath>
#include <limits>
#include <stdexcept>
#include <string>

using namespace std;

/*****************************************************************************/
/* Methods                                                                   */
/*****************************************************************************/

float Color::intToHue(unsigned int val) {
  if (val > numeric_limits<unsigned char>::max()) {
    ostringstream stream;
    stream << "Integer value out of bounds: " << val;
    throw runtime_error(stream.str());
  }
  else
    return (float)BitOperations::revertByte(val) /
      numeric_limits<unsigned char>::max()*2.0*M_PI;
}

unsigned int Color::hueToInt(float hue) {
  return BitOperations::revertByte((unsigned int)round(hue /
    (2.0*M_PI)*numeric_limits<unsigned char>::max()));
}

Colorf Color::hsvToRgb(const Colorf & hsv) {
  Colorf rgb;
  rgb[3] = hsv[3];

  if (hsv[2] > 0.0) {
    float hue = hsv[0]/(60.0*M_PI/180.0);
    int i = floor(hue);
    float f = hue-i;
    float p = hsv[2]*(1.0-hsv[1]);
    float q = hsv[2]*(1.0-hsv[1]*f);
    float t = hsv[2]*(1.0-hsv[1]*(1.0-f));

    switch (i) {
      case 0:
        rgb[0] = hsv[2];
        rgb[1] = t;
        rgb[2] = p;
        break;
      case 1:
        rgb[0] = q;
        rgb[1] = hsv[2];
        rgb[2] = p;
        break;
      case 2:
        rgb[0] = p;
        rgb[1] = hsv[2];
        rgb[2] = t;
        break;
      case 3:
        rgb[0] = p;
        rgb[1] = q;
        rgb[2] = hsv[2];
        break;
      case 4:
        rgb[0] = t;
        rgb[1] = p;
        rgb[2] = hsv[2];
        break;
      default:
        rgb[0] = hsv[2];
        rgb[1] = p;
        rgb[2] = q;
        break;
    }
  }
  else {
    rgb[0] = hsv[2];
    rgb[1] = hsv[2];
    rgb[2] = hsv[2];
  }

  return rgb;
}

Colorf Color::rgbToHsv(const Colorf & rgb) {
  Colorf hsv;
  hsv[3] = rgb[3];
  
  float min = fmin(rgb[0], fmin(rgb[1], rgb[2]));
  float max = fmax(rgb[0], fmax(rgb[1], rgb[2]));
  hsv[2] = max;
  float delta = max-min;

  if (max != 0.0) {
    hsv[1] = delta/max;
    
    if(rgb[0] == max)
      hsv[0] = (rgb[1]-rgb[2])/delta;
    else if(rgb[1] == max)
      hsv[0] = 2.0+(rgb[2]-rgb[0])/delta;
    else
      hsv[0] = 4.0+(rgb[0]-rgb[1])/delta;

    hsv[0] *= 60.0*M_PI/180.0;
    if (hsv[0] < 0.0)
      hsv[0] += 2.0*M_PI;
  }
  else {
    hsv[0] = -1.0;
    hsv[1] = 0.0;
  }

  return hsv;
}

Colorf Color::intToRgb(unsigned int val) {
  return roundRgb(hsvToRgb(Colorf(intToHue(val), 1.0, 1.0, 1.0)));
}

unsigned int Color::rgbToInt(const Colorf & rgb) {
    return hueToInt(rgbToHsv(rgb)[0]);
}

unsigned int Color::rgbToInt(const Colord & rgb) {
  return rgbToInt(Colorf(rgb[0], rgb[1], rgb[2], rgb[3]));
}

Colorf Color::roundRgb(const Colorf & rgb) {
  Colorf result;
  for (int i = 0; i < 4; ++i)
    result[i] = round(rgb[i]*255.0)/255.0;

  return result;
}
