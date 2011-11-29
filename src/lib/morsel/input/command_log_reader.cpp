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

#include "command_log_reader.h"

#include <stdexcept>

using namespace std;

/*****************************************************************************/
/* Constructors and Destructor                                               */
/*****************************************************************************/

CommandLogReader::CommandLogReader(string name, PyObject* actuator,
    string filename, bool binary) :
  LogReader(name, binary),
  actuator(actuator),
  filename(filename),
  hasTimestamps(false) {
  Py_XINCREF(actuator);
}

CommandLogReader::~CommandLogReader() {
  Py_XDECREF(actuator);
}

/*****************************************************************************/
/* Methods                                                                   */
/*****************************************************************************/

void CommandLogReader::readHeader() {
  LogReader::readHeader();

  if (!binary) {    
    skip("# Timestamps: ") >> hasTimestamps;
    skip("\n# Command format: c_0 [c_1 [...]]\n");
  }
  else
    (*this) << hasTimestamps;
}

void CommandLogReader::readData(double time) {
  unsigned int numValues;

  open(filename, time);
  if (getStream().eof())
    return;
  
  try {
    if (binary)
      (*this) >> numValues;
    else
      skip("# Number of values: ") >> numValues;
      skip("\n");
  }
  catch (runtime_error& error) {
    return;
  }
  
  if (hasTimestamps) {
    if (!binary) {
      string buffer;
      
      skip("# Timestamp: ") >> buffer;
      skip("\n");
    }
    else
      (*this) >> time;
  }

  PyObject* command = PyList_New(numValues);
  Py_XINCREF(command);
  
  for (int i = 0; i < numValues; ++i) {
    double f_i;
    (*this) >> f_i;
    
    PyObject* p_i = PyFloat_FromDouble(f_i);
    Py_XINCREF(p_i);
    PyList_SetItem(command, i, p_i);
    Py_XDECREF(p_i);
  }

  if (!binary)
    skip("\n");

  PyObject_SetAttrString(actuator, "command", command);
  Py_XDECREF(command);
}
