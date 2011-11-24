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

#ifndef RANGE_SENSOR_H
#define RANGE_SENSOR_H

/** Range sensor implementation
  * @author Ralf Kaestner ETHZ Autonomous Systems Lab.
  */

#include "morsel/morsel.h"
#include "morsel/sensors/range_camera.h"

#include <nodePath.h>

#include <string>
#include <deque>
#include <cstring>
#include <cmath>

class RangeSensor :
  public NodePath {
public:
  /** Types and non-static subclasses
    */
  struct Ray {
    bool valid;
    LPoint3f point;
    Colorf color;
    size_t label;
  };
PUBLISHED:
  /** Constructors
    */
  RangeSensor(std::string name, const LVecBase2f& minAngles,
    const LVecBase2f& maxAngles, const LVecBase2f& resolution,
    const LVecBase2f& rangeLimits, const LVecBase2f&
    cameraMaxFOV = LVecBase2f(60.0*M_PI/180.0, 60.0*M_PI/180.0),
    const LVecBase2f& cameraResolution = LVecBase2f(128, 128),
    bool spherical = false, bool acquireColor = false,
    std::string acquireLabel = "");

  /** Destructor
    */
  virtual ~RangeSensor();

  const LVecBase2f& getRangeLimits() const;
  const LVecBase2f& getFOV() const;
  size_t getNumCameras() const;
  const RangeCamera& getCamera(int index) const;
  size_t getNumRays() const;
  const Ray& getRay(int index) const;
  double getTimestamp() const;
  
  bool update(double time);
  void showFrustums();
  void hideFrustums();
protected:
  LVecBase2f minAngles;
  LVecBase2f maxAngles;
  LVecBase2f resolution;
  LVecBase2f rangeLimits;
  LVecBase2f fov;
  LVecBase2f numCameras;
  LVecBase2f numRays;
  LVecBase2f cameraMaxFOV;
  LVecBase2f cameraResolution;
  bool spherical;
  bool acquireColor;
  std::string acquireLabel;
  std::vector<RangeCamera*> cameras;

  double timestamp;
  mutable double lastTimestamp;
  mutable std::vector<Ray> rays;
  
  void computeParameters(double minAngle, double maxAngle, size_t totalNumRays,
    double cameraMaxFOV, std::deque<double>& fovs, std::deque<double>& angles,
    std::deque<size_t>& numRays);
  void setupCameras();

  void updateRays() const;
};

#endif
