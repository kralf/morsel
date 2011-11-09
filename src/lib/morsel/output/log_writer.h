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

#ifndef LOG_WRITER_H
#define LOG_WRITER_H

/** Abstract log writer definition
  * @author Ralf Kaestner ETHZ Autonomous Systems Lab.
  */

#include "morsel/morsel.h"

#include "morsel/utils/gzfstream.h"

#include <nodePath.h>

class LogWriter :
  public NodePath {
PUBLISHED:
  /** Constructors
    */
  LogWriter(std::string name, bool binary = true, std::string
    placeholder = "%");
  
  /** Destructor
    */
  virtual ~LogWriter();

  const std::string& getLogFilename() const;
  std::ostream& getStream();
  bool isOpen() const;

  bool open(std::string filename);
  bool open(std::string filename, double timestamp);
  void close();

  std::string timestampToString(double time) const;
public:
  LogWriter& operator<<(char value);
  LogWriter& operator<<(unsigned char value);
  LogWriter& operator<<(int value);
  LogWriter& operator<<(unsigned int value);
  LogWriter& operator<<(long value);
  LogWriter& operator<<(unsigned long value);
  LogWriter& operator<<(float value);
  LogWriter& operator<<(double value);
  LogWriter& operator<<(const char* value);

  virtual bool writeData(double time) = 0;
protected:
  std::string logFilename;
  bool binary;
  std::string placeholder;
  
  std::ofstream logFile;
  gzofstream logFileGz;
};

#endif
