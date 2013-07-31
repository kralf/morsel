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

#include "log_reader.h"

#include "morsel/utils/timestamp.h"

#include <stdexcept>

using namespace std;

/*****************************************************************************/
/* Constructors and Destructor                                               */
/*****************************************************************************/

LogReader::LogReader(string name, bool binary, string placeholder) :
  NodePath(name),
  binary(binary),
  placeholder(placeholder) {
}

LogReader::~LogReader() {
  close();
}

/*****************************************************************************/
/* Accessors                                                                 */
/*****************************************************************************/

const string& LogReader::getLogFilename() const {
  return logFilename;
}

istream& LogReader::getStream() {
  if (logFile.is_open())
    return logFile;
  else if (logFileGz.is_open())
    return logFileGz;
  else
    throw runtime_error("Bad log reader stream");
}

bool LogReader::isOpen() const {
  return logFile.is_open() || logFileGz.is_open();
}

/*****************************************************************************/
/* Methods                                                                   */
/*****************************************************************************/

bool LogReader::open(string filename) {
  close();

  logFilename = filename;
  string suffixGz = ".gz";
  ios_base::openmode mode = ios::in;
  if (binary)
    mode |= ios::binary;
  
  if (equal(suffixGz.rbegin(), suffixGz.rend(), logFilename.rbegin()))
    logFileGz.open(filename.c_str(), mode);
  else
    logFile.open(filename.c_str(), mode);

  if (logFile.is_open() || logFileGz.is_open()) {
    readHeader();
    return true;
  }
  else {
    logFilename.clear();
    return false;
  }
}

bool LogReader::open(string filename, double timestamp) {
  int pos = filename.find(placeholder);
  if (pos != string::npos)
    filename.replace(pos, placeholder.length(),
      Timestamp::toString(timestamp));

  if (logFilename != filename)
    return open(filename);
  else
    return isOpen();
}

void LogReader::close() {
  if (logFile.is_open())
    logFile.close();
  else if (logFileGz.is_open())
    logFileGz.close();

  logFilename.clear();
}

LogReader& LogReader::operator>>(char& value) {
  if (binary)
    getStream().read((char*)&value, sizeof(value));
  else
    getStream() >> value;

  return *this;
}

LogReader& LogReader::operator>>(bool& value) {
  if (!binary) {
    string buffer;
    (*this) >> buffer;

    value = (buffer == "true");
  }
  else
    getStream().read((char*)&value, sizeof(value));

  return *this;
}

LogReader& LogReader::operator>>(unsigned char& value) {
  if (binary)
    getStream().read((char*)&value, sizeof(value));
  else
    getStream() >> value;

  return *this;
}

LogReader& LogReader::operator>>(int& value) {
  if (binary)
    getStream().read((char*)&value, sizeof(value));
  else
    getStream() >> value;

  return *this;
}

LogReader& LogReader::operator>>(unsigned int& value) {
  if (binary)
    getStream().read((char*)&value, sizeof(value));
  else
    getStream() >> value;

  return *this;
}

LogReader& LogReader::operator>>(long& value) {
  if (binary)
    getStream().read((char*)&value, sizeof(value));
  else
    getStream() >> value;

  return *this;
}

LogReader& LogReader::operator>>(unsigned long& value) {
  if (binary)
    getStream().read((char*)&value, sizeof(value));
  else
    getStream() >> value;

  return *this;
}

LogReader& LogReader::operator>>(float& value) {
  if (binary)
    getStream().read((char*)&value, sizeof(value));
  else
    getStream() >> value;

  return *this;
}

LogReader& LogReader::operator>>(double& value) {
  if (binary)
    getStream().read((char*)&value, sizeof(value));
  else
    getStream() >> value;

  return *this;
}

LogReader& LogReader::operator>>(string& value) {
  char c;

  value.clear();
  if (binary) {
    while (getStream().read(&c, 1) && (c != '\0'))
      value.push_back(c);
  }
  else {
    while ((getStream().peek() != ' ') && (getStream().peek() != '\n')) {
      if (getStream().read(&c, 1))
        value.push_back(c);
      else
        break;
    }
  }

  return *this;
}

LogReader& LogReader::skip(const string& value) {
  size_t size = value.size();
  char buffer[size+1];
  buffer[size] = '\0';
  
  if (!getStream().read(buffer, size) || (value != buffer))
    throw runtime_error("Bad log file format");

  return *this;
}

void LogReader::readHeader() {  
  if (!binary) {
    string version;
    
    skip("# File version: ").skip(Morsel::getName()).skip(" ");
    (*this) >> version;
    skip("\n");
  }
  else {
    string name;
    unsigned int major, minor, patch;
    
    (*this) >> name;
    if (name != Morsel::getName())
      throw runtime_error("Bad log file format");

    (*this) >> major >> minor >> patch;
  }
}
