/***************************************************************************
 *   Copyright (C) 2011 by Ralf Kaestner                                   *
 *   ralf.kaestner@gmail.com                                               *
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 *   This program is distributed in the hope that it will be useful,       *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU General Public License for more details.                          *
 *                                                                         *
 *   You should have received a copy of the GNU General Public License     *
 *   along with this program; if not, write to the                         *
 *   Free Software Foundation, Inc.,                                       *
 *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
 ***************************************************************************/

#ifndef COLOR_H
#define COLOR_H

/** Morsel color operations
  * @author Ralf Kaestner ETHZ Autonomous Systems Lab.
  */

#include "morsel/morsel.h"

#include <lvecBase4.h>

class Color {
PUBLISHED:
  static float intToHue(unsigned int val);
  static unsigned int hueToInt(float hue);
  
  static Colorf hsvToRgb(const Colorf & hsv);
  static Colorf rgbToHsv(const Colorf & rgb);
  
  static Colorf intToRgb(unsigned int val);
  static unsigned int rgbToInt(const Colorf & rgb);
  static unsigned int rgbToInt(const Colord & rgb);

  static Colorf roundRgb(const Colorf & rgb);
};

#endif
