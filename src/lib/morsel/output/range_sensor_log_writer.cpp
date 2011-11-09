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

#include <limits>

using namespace std;

/*****************************************************************************/
/* Constructors and Destructor                                               */
/*****************************************************************************/

RangeSensorLogWriter::RangeSensorLogWriter(string name, NodePath& sensor,
    string filename, bool binary, bool logTimestamps, bool logColors,
    bool logLabels) :
  LogWriter(name, binary),
  sensor(static_cast<RangeSensor&>(sensor)),
  filename(filename),
  logTimestamps(logTimestamps),
  logColors(logColors),
  logLabels(logLabels) {
}

RangeSensorLogWriter::~RangeSensorLogWriter() {
}

/*****************************************************************************/
/* Methods                                                                   */
/*****************************************************************************/

bool RangeSensorLogWriter::writeData(double time) {
  open(filename, time);

  unsigned int numPoints = sensor.getNumRays();
  unsigned int numValidPoints = 0;
  for (int i = 0; i < numPoints; ++i)
    if (sensor.getRay(i).valid)
      ++numValidPoints;

  if (binary) {
    (*this) << numValidPoints;
    if (logTimestamps)
      (*this) << time;
  }
  else {
    (*this) << "# Number of points: " << numValidPoints << "\n";
    if (logTimestamps)
      (*this) << "# Timestamp: " << timestampToString(time).c_str() << "\n";
    (*this) << "# Point format: x y z";
    if (logColors)
      (*this) << " r g b";
    if (logLabels)
      (*this) << " label";
    (*this) << "\n";
  }

  for (int i = 0; i < numPoints; ++i) {
    const RangeSensor::Ray& ray = sensor.getRay(i);
    if (ray.valid) {
      if (binary) {
        (*this) << ray.x << ray.y << ray.z;
        if (logColors)
          (*this) << ray.red << ray.green << ray.blue;
        if (logLabels)
          (*this) << (unsigned int)ray.label;
      }
      else {
        if (ray.radius < numeric_limits<double>::infinity())
          (*this) << ray.x << " " << ray.y << " " << ray.z;
        if (logColors)
          (*this) << " " << ray.red << " " << ray.green << " " << ray.blue;
        if (logLabels)
          (*this) << " " << ray.label;
        (*this) << "\n";
      }
    }
  }
}
