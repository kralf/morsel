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

#include "timestamp.h"

#include <ctime>

using namespace std;

/*****************************************************************************/
/* Methods                                                                   */
/*****************************************************************************/

string Timestamp::toString(double timestamp) {
  char date[1024];
  char usecs[256];

  time_t local = timestamp;
  struct tm* time = localtime(&local);

  strftime(date, sizeof(date), "%Y-%m-%d-%H%M%S", time);
  sprintf(usecs, "%06d", (int)((timestamp-(int)timestamp)*1e6));
  ostringstream stream;
  stream << date << "-" << usecs;

  return stream.str();
}
