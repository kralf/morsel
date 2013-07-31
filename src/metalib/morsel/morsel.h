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

#ifndef MORSEL_H
#define MORSEL_H

/** Morsel global operations
  * @author Ralf Kaestner ETHZ Autonomous Systems Lab.
  */

#include <panda.h>
#include <graphicsEngine.h>

#include <string.h>
#include <cstring>
#include <cstdlib>

class Morsel {
public:
  static std::string getName();
  static unsigned int getMajorVersion();
  static unsigned int getMinorVersion();
  static unsigned int getPatchVersion();
  static std::string getFullName();
  
  static GraphicsStateGuardian* getGSG();
  static GraphicsEngine* getEngine();
  static GraphicsOutput* getWindow(int index);
};

#endif
