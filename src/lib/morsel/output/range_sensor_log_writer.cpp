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

#include "range_sensor_log_writer.h"

#include "morsel/sensors/range_sensor.h"
#include "morsel/utils/timestamp.h"

using namespace std;

/*****************************************************************************/
/* Constructors and Destructor                                               */
/*****************************************************************************/

RangeSensorLogWriter::RangeSensorLogWriter(string name, NodePath& sensor,
    string filename, bool binary, bool logTimestamps, bool logPoses, bool
    logColors, bool logLabels, bool logInvalids) :
  LogWriter(name, binary),
  sensor(static_cast<RangeSensor&>(sensor)),
  filename(filename),
  logTimestamps(logTimestamps),
  logPoses(logPoses),
  logColors(logColors),
  logLabels(logLabels),
  logInvalids(logInvalids) {
}

RangeSensorLogWriter::~RangeSensorLogWriter() {
}

/*****************************************************************************/
/* Methods                                                                   */
/*****************************************************************************/

void RangeSensorLogWriter::writeHeader() {
  LogWriter::writeHeader();
  
  if (!binary) {
    (*this) << "# Timestamps: " << logTimestamps << "\n";
    (*this) << "# Poses: " << logPoses << "\n";
    (*this) << "# Colors: " << logColors << "\n";
    (*this) << "# Labels: " << logLabels << "\n";
    (*this) << "# Ivalids: " << logInvalids << "\n";
    (*this) << "# Point format: x y z";
    if (logColors)
      (*this) << " r g b";
    if (logLabels)
      (*this) << " label";
    if (logInvalids)
      (*this) << " valid";
    (*this) << "\n";
  }
  else
    (*this) << logTimestamps << logPoses << logColors << logLabels <<
      logInvalids;
}

void RangeSensorLogWriter::writeData(double time) {
  double timestamp = sensor.getTimestamp();
  LVecBase3f position = sensor.getPosition();
  LVecBase3f orientation = sensor.getOrientation();

  unsigned int numRays = sensor.getNumRays();
  if (!logInvalids) {
    numRays = 0;
    for (int i = 0; i < sensor.getNumRays(); ++i)
      if (sensor.getRay(i).valid)
        ++numRays;
  }

  open(filename, timestamp);
  if (binary) {
    (*this) << numRays;
    if (logTimestamps)
      (*this) << timestamp;
    if (logPoses)
      (*this) << position[0]  << position[1] << position[2] <<
        float(orientation[0]*M_PI/180.0) <<
        float(orientation[1]*M_PI/180.0) <<
        float(orientation[2]*M_PI/180.0);
  }
  else {
    (*this) << "# Number of points: " << numRays << "\n";
    if (logTimestamps)
      (*this) << "# Timestamp: " << Timestamp::toString(timestamp).c_str() <<
        "\n";
    if (logPoses)
      (*this) << "# Pose: " << position[0] << " " << position[1] << " " <<
        position[2] << " " << orientation[0] << " " <<  orientation[1] <<
        " " << orientation[2] << "\n";
  }

  for (int i = 0; i < sensor.getNumRays(); ++i) {
    RangeSensor::Ray ray = sensor.getRay(i);
    if (logInvalids || ray.valid) {
      if (binary) {
        (*this) << ray.point[0] << ray.point[1] << ray.point[2];
        if (logInvalids)
          (*this) << ray.valid;
        if (logColors)
          (*this) << ray.color[0] << ray.color[1] << ray.color[2];
        if (logLabels)
          (*this) << (unsigned int)ray.label;
      }
      else {
        (*this) << ray.point[0] << " " << ray.point[1] << " " << ray.point[2];
        if (logInvalids)
          (*this) << " " << ray.valid;
        if (logColors)
          (*this) << " " << ray.color[0] << " " << ray.color[1] << " " <<
            ray.color[2];
        if (logLabels)
          (*this) << " " << ray.label;
        (*this) << "\n";
      }
    }
  }

  flush();
}
