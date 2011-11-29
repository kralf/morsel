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

#ifndef COMMAND_LOG_READER_H
#define COMMAND_LOG_READER_H

/** Command log reader
  * @author Ralf Kaestner ETHZ Autonomous Systems Lab.
  */

#include "morsel/input/log_reader.h"

class CommandLogReader :
  public LogReader {
PUBLISHED:
  /** Constructors
    */
  CommandLogReader(std::string name, PyObject* actuator, std::string
    filename, bool binary = true);
  
  /** Destructor
    */
  virtual ~CommandLogReader();

  virtual void readHeader();
  virtual void readData(double time);
protected:
  PyObject* actuator;
  std::string filename;
  bool hasTimestamps;
};

#endif
