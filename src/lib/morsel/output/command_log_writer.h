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

#ifndef COMMAND_LOG_WRITER_H
#define COMMAND_LOG_WRITER_H

/** Command log writer
  * @author Ralf Kaestner ETHZ Autonomous Systems Lab.
  */

#include "morsel/output/log_writer.h"

class CommandLogWriter :
  public LogWriter {
PUBLISHED:
  /** Constructors
    */
  CommandLogWriter(std::string name, PyObject* actuator, std::string
    filename, bool binary = true, bool logTimestamps = true);
  
  /** Destructor
    */
  virtual ~CommandLogWriter();

  virtual void writeHeader();
  virtual void writeData(double time);
protected:
  PyObject* actuator;
  std::string filename;
  bool logTimestamps;
};

#endif
