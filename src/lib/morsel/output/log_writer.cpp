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

#include "log_writer.h"

#include "morsel/utils/timestamp.h"

#include <stdexcept>

using namespace std;

/*****************************************************************************/
/* Constructors and Destructor                                               */
/*****************************************************************************/

LogWriter::LogWriter(string name, bool binary, string placeholder) :
  NodePath(name),
  binary(binary),
  placeholder(placeholder) {
}

LogWriter::~LogWriter() {
  close();
}

/*****************************************************************************/
/* Accessors                                                                 */
/*****************************************************************************/

const string& LogWriter::getLogFilename() const {
  return logFilename;
}

ostream& LogWriter::getStream() {
  if (logFile.is_open())
    return logFile;
  else if (logFileGz.is_open())
    return logFileGz;
  else
    throw runtime_error("Bad log writer stream");
}

bool LogWriter::isOpen() const {
  return logFile.is_open() || logFileGz.is_open();
}

/*****************************************************************************/
/* Methods                                                                   */
/*****************************************************************************/

bool LogWriter::open(string filename) {
  close();

  logFilename = filename;
  string suffixGz = ".gz";
  ios_base::openmode mode = ios::out;
  if (binary)
    mode |= ios::binary;
  
  if (equal(suffixGz.rbegin(), suffixGz.rend(), logFilename.rbegin()))
    logFileGz.open(filename.c_str(), mode);
  else
    logFile.open(filename.c_str(), mode);

  if (logFile.is_open() || logFileGz.is_open()) {
    writeHeader();
    return true;
  }
  else {
    logFilename.clear();
    return false;
  }
}

bool LogWriter::open(string filename, double timestamp) {
  int pos = filename.find(placeholder);
  if (pos != string::npos)
    filename.replace(pos, placeholder.length(),
      Timestamp::toString(timestamp));

  if (logFilename != filename)
    return open(filename);
  else
    return isOpen();
}

void LogWriter::close() {
  if (logFile.is_open())
    logFile.close();
  else if (logFileGz.is_open())
    logFileGz.close();

  logFilename.clear();
}

void LogWriter::flush() {
  if (logFile.is_open())
    logFile.flush();
  else if (logFileGz.is_open())
    logFileGz.flush();
}

LogWriter& LogWriter::operator<<(char value) {
  if (binary)
    getStream().write((const char*)&value, sizeof(value));
  else
    getStream() << value;

  return *this;
}

LogWriter& LogWriter::operator<<(bool value) {
  if (!binary) {
    if (value)
      getStream() << "true";
    else
      getStream() << "false";
  }
  else
    getStream().write((const char*)&value, sizeof(value));

  return *this;
}

LogWriter& LogWriter::operator<<(unsigned char value) {
  if (binary)
    getStream().write((const char*)&value, sizeof(value));
  else
    getStream() << value;

  return *this;
}

LogWriter& LogWriter::operator<<(int value) {
  if (binary)
    getStream().write((const char*)&value, sizeof(value));
  else
    getStream() << value;

  return *this;
}

LogWriter& LogWriter::operator<<(unsigned int value) {
  if (binary)
    getStream().write((const char*)&value, sizeof(value));
  else
    getStream() << value;

  return *this;
}

LogWriter& LogWriter::operator<<(long value) {
  if (binary)
    getStream().write((const char*)&value, sizeof(value));
  else
    getStream() << value;

  return *this;
}

LogWriter& LogWriter::operator<<(unsigned long value) {
  if (binary)
    getStream().write((const char*)&value, sizeof(value));
  else
    getStream() << value;

  return *this;
}

LogWriter& LogWriter::operator<<(float value) {
  if (binary)
    getStream().write((const char*)&value, sizeof(value));
  else
    getStream() << value;

  return *this;
}

LogWriter& LogWriter::operator<<(double value) {
  if (binary)
    getStream().write((const char*)&value, sizeof(value));
  else
    getStream() << value;

  return *this;
}

LogWriter& LogWriter::operator<<(const char* value) {
  return LogWriter::operator<<(string(value));
}

LogWriter& LogWriter::operator<<(const string& value) {
  if (binary)
    getStream().write(value.c_str(), value.length()+1);
  else
    getStream() << value.c_str();

  return *this;
}

void LogWriter::writeHeader() {
  if (!binary)
    (*this) << "# File version: " << Morsel::getFullName() << "\n";
  else
    (*this) << Morsel::getName() << Morsel::getMajorVersion() <<
      Morsel::getMinorVersion() << Morsel::getPatchVersion();
}
