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

#include "command_log_writer.h"

#include "morsel/utils/timestamp.h"

#include <stdexcept>

using namespace std;

/*****************************************************************************/
/* Constructors and Destructor                                               */
/*****************************************************************************/

CommandLogWriter::CommandLogWriter(string name, PyObject* actuator,
    string filename, bool binary, bool logTimestamps) :
  LogWriter(name, binary),
  actuator(actuator),
  filename(filename),
  logTimestamps(logTimestamps) {
  Py_XINCREF(actuator);
}

CommandLogWriter::~CommandLogWriter() {
  Py_XDECREF(actuator);
}

/*****************************************************************************/
/* Methods                                                                   */
/*****************************************************************************/

void CommandLogWriter::writeHeader() {
  LogWriter::writeHeader();
  
  if (!binary) {
    (*this) << "# Timestamps: " << logTimestamps << "\n";
    (*this) << "# Command format: c_0 [c_1 [...]]\n";
  }
  else 
    (*this) << logTimestamps;
}

void CommandLogWriter::writeData(double time) {
  PyObject* command = PyObject_GetAttrString(actuator, "command");

  if (!command)
    throw runtime_error("Python object has no command attribute");
  
  Py_XINCREF(command);
  unsigned int numValues = PyList_Size(command);

  open(filename, time);
  if (binary) {
    (*this) << numValues;
    if (logTimestamps)
      (*this) << time;
  }
  else {
    (*this) << "# Number of values: " << numValues << "\n";
    if (logTimestamps)
      (*this) << "# Timestamp: " << Timestamp::toString(time).c_str() << "\n";
  }
  
  for (int i = 0; i < numValues; ++i) {
    PyObject* p_i = PyList_GetItem(command, i);
    Py_XINCREF(p_i);

    PyObject* f_i = PyNumber_Float(p_i);
    if (!f_i)
      throw runtime_error("Python value is not of numeric type");
      
    Py_XINCREF(f_i);

    if (binary)
      (*this) << PyFloat_AsDouble(f_i);
    else {
      if (i)
        (*this) << " ";
      (*this) << PyFloat_AsDouble(f_i);
    }

    Py_XDECREF(f_i);
    Py_XDECREF(p_i);
  }
  
  if (!binary)
    (*this) << "\n";
  flush();

  Py_XDECREF(command);
}
