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

#ifndef RANGE_SENSOR_LOG_WRITER_H
#define RANGE_SENSOR_LOG_WRITER_H

/** Range sensor log writer
  * @author Ralf Kaestner ETHZ Autonomous Systems Lab.
  */

#include "morsel/output/log_writer.h"

class RangeSensor;

class RangeSensorLogWriter :
  public LogWriter {
PUBLISHED:
  /** Constructors
    */
  RangeSensorLogWriter(std::string name, NodePath& sensor, std::string
    filename, bool binary = true, bool logTimestamps = true, bool
    logPoses = true, bool logColors = false, bool logLabels = false,
    bool logInvalids = false);
  
  /** Destructor
    */
  virtual ~RangeSensorLogWriter();

  virtual void writeHeader();
  virtual void writeData(double time);
protected:
  RangeSensor& sensor;
  std::string filename;
  bool logTimestamps;
  bool logPoses;
  bool logColors;
  bool logLabels;
  bool logInvalids;
};

#endif
