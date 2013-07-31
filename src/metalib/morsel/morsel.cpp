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

#include "morsel.h"

#include "config.h"

#include <pandaFramework.h>

/*****************************************************************************/
/* Methods                                                                   */
/*****************************************************************************/

string Morsel::getName() {
  return PROJECT_NAME;
}

unsigned int Morsel::getMajorVersion() {
  return PROJECT_MAJOR;
}

unsigned int Morsel::getMinorVersion() {
  return PROJECT_MINOR;
}

unsigned int Morsel::getPatchVersion() {
  return PROJECT_PATCH;
}

string Morsel::getFullName() {
  stringstream stream;
  
  stream << PROJECT_NAME << " " << PROJECT_MAJOR << "." <<
    PROJECT_MINOR << "." << PROJECT_PATCH;

  return stream.str();
}

GraphicsStateGuardian* Morsel::getGSG() {
  return static_cast<GraphicsStateGuardian*>(
    GraphicsStateGuardianBase::get_default_gsg());
}

GraphicsEngine* Morsel::getEngine() {
  return getGSG()->get_engine();
}

GraphicsOutput* Morsel::getWindow(int index) {
  return getEngine()->get_window(index);
}
