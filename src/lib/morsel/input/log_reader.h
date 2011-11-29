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

#ifndef LOG_READER_H
#define LOG_READER_H

/** Abstract log reader definition
  * @author Ralf Kaestner ETHZ Autonomous Systems Lab.
  */

#include "morsel/morsel.h"

#include "morsel/utils/gzfstream.h"

#include <nodePath.h>

class LogReader :
  public NodePath {
PUBLISHED:
  /** Constructors
    */
  LogReader(std::string name, bool binary = true, std::string
    placeholder = "%");
  
  /** Destructor
    */
  virtual ~LogReader();

  const std::string& getLogFilename() const;
  std::istream& getStream();
  bool isOpen() const;

  bool open(std::string filename);
  bool open(std::string filename, double timestamp);
  void close();
public:
  LogReader& operator>>(char& value);
  LogReader& operator>>(bool& value);
  LogReader& operator>>(unsigned char& value);
  LogReader& operator>>(int& value);
  LogReader& operator>>(unsigned int& value);
  LogReader& operator>>(long& value);
  LogReader& operator>>(unsigned long& value);
  LogReader& operator>>(float& value);
  LogReader& operator>>(double& value);
  LogReader& operator>>(std::string& value);

  LogReader& skip(const std::string& value);

  virtual void readHeader();
  virtual void readData(double time) = 0;
protected:
  std::string logFilename;
  bool binary;
  std::string placeholder;
  
  std::ifstream logFile;
  gzifstream logFileGz;
};

#endif
