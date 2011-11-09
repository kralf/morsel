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

#include "range_sensor.h"
#include "perspective_range_camera.h"
#include "spherical_range_camera.h"

#include <lpoint3.h>
#include <lvecBase3.h>
#include <numeric>
#include <sstream>
#include <limits>

using namespace std;

/*****************************************************************************/
/* Constructors and Destructor                                               */
/*****************************************************************************/

RangeSensor::RangeSensor(std::string name, const LVecBase2f& minAngles,
    const LVecBase2f& maxAngles, const LVecBase2f& resolution, const
    LVecBase2f& rangeLimits, const LVecBase2f& cameraMaxFOV, const
    LVecBase2f& cameraResolution, bool spherical, bool acquireColor,
    std::string acquireLabel) :
  NodePath(name),
  minAngles(minAngles),
  maxAngles(maxAngles),
  resolution(resolution),
  rangeLimits(rangeLimits),
  fov(maxAngles[0]-minAngles[0], maxAngles[1]-minAngles[1]),
  numRays(floor(fov[0]/resolution[0]), floor(fov[1]/resolution[1])),
  cameraMaxFOV(cameraMaxFOV),
  cameraResolution(cameraResolution),
  spherical(spherical),
  acquireColor(acquireColor),
  acquireLabel(acquireLabel),
  rays(new RangeSensor::Ray[(size_t)(numRays[0]*numRays[1])]) {
  setupCameras();
  getEngine()->render_frame();
}

RangeSensor::~RangeSensor() {
  delete[] rays;
  for (int i = 0; i < cameras.size(); ++i)
    delete cameras[i];
}

/*****************************************************************************/
/* Accessors                                                                 */
/*****************************************************************************/

size_t RangeSensor::getNumCameras() const {
  return cameras.size();
}

const RangeCamera& RangeSensor::getCamera(int index) const {
  return *cameras[index];
}

size_t RangeSensor::getNumRays() const {
  return numRays[0]*numRays[1];
}

const RangeSensor::Ray& RangeSensor::getRay(int index) const {
  return rays[index];
}

const LVecBase2f& RangeSensor::getRangeLimits() const {
  return rangeLimits;
}

const LVecBase2f& RangeSensor::getFOV() const {
  return fov;
}

double RangeSensor::getRayLength(int index) const {
  if (index >= (numRays[0]*numRays[1]))
    return -1.0;
  else
    return rays[index].radius;
}

/*****************************************************************************/
/* Methods                                                                   */
/*****************************************************************************/

bool RangeSensor::update(double time) {
  int rayIndex = 0;
  
  for (int ci = 0; ci < cameras.size(); ++ci) {
    RangeCamera* c = cameras[ci];
    c->update(time);
    
    for (int ri = 0; ri < c->getNumRays(); ++ri) {
      const RangeCamera::Ray& ray1 = c->getRay(ri);
      LPoint3f p = get_relative_point(*c, LVecBase3f(ray1.x, ray1.y, ray1.z));
      Ray& ray2 = rays[rayIndex++];

      ray2.row = ray1.row;
      ray2.column = ray1.column;
      ray2.index = rayIndex;
      ray2.hAngle = atan2(p[1], p[0]);
      ray2.vAngle = atan2(p[2], sqrt(p[0]*p[0]+p[1]*p[1]));
      ray2.x = p[0];
      ray2.y = p[1];
      ray2.z = p[2];
      if (ray1.radius >= rangeLimits[1]) {
        ray2.valid = false;
        ray2.radius = numeric_limits<double>::infinity();
      }
      else if (ray1.radius <= rangeLimits[0]) {
        ray2.valid = false;
        ray2.radius = -numeric_limits<double>::infinity();
      }
      else
        ray2.valid = true;
      if (acquireColor) {
        ray2.red = ray1.red;
        ray2.green = ray1.green;
        ray2.blue = ray1.blue;
      } else {
        ray2.red = 0;
        ray2.green = 0;
        ray2.blue = 0;
      }
      if (!acquireLabel.empty())
        ray2.label = ray1.label;
      else
        ray2.label = 0;
    }
  }
  
  return true;
}

void RangeSensor::showFrustums() {
  for (int i = 0; i < cameras.size(); ++i)
    cameras[i]->showFrustum();
}

void RangeSensor::hideFrustums() {
  for (int i = 0; i < cameras.size(); ++i)
    cameras[i]->hideFrustum();
}

void RangeSensor::computeParameters(double minAngle, double maxAngle,
    size_t totalNumRays, double cameraMaxFOV, std::deque<double>& fovs,
    std::deque<double>& angles, std::deque<size_t>& numRays) {
  fovs.clear();
  angles.clear();
  numRays.clear();
  
  double fov = maxAngle-minAngle;
  double rayFOV = fov/totalNumRays;
  size_t numCameras = ceil(fov/cameraMaxFOV);
  double cameraFOV = fov/numCameras;

  for (int i = totalNumRays; i > 0; ) {
    size_t cameraNumRays = fmin(round(cameraFOV/rayFOV), i);
    numRays.push_back(cameraNumRays);
    fovs.push_back(cameraNumRays*rayFOV);
    i -= cameraNumRays;
  }

  double angle = minAngle;
  for (int i = 0; i < numRays.size(); ++i) {
    angles.push_back(angle+0.5*fovs[i]);
    angle += fovs[i];
  }
}

void RangeSensor::setupCameras() {
  deque<double> hFOVs, vFOVs;
  deque<double> hAngles, vAngles;
  deque<size_t> hNumRays, vNumRays;
  
  computeParameters(minAngles[0], maxAngles[0], numRays[0], cameraMaxFOV[0],
    hFOVs, hAngles, hNumRays);
  computeParameters(minAngles[1], maxAngles[1], numRays[1], cameraMaxFOV[1],
    vFOVs, vAngles, vNumRays);

  for (int i = 0; i < hFOVs.size(); ++i) {
    for (int j = 0; j < vFOVs.size(); ++j) {
      stringstream stream;
      stream << get_name() << "_" << i << "x" << j;

      RangeCamera* c;
      if (spherical)
        c = new SphericalRangeCamera(stream.str(),
          LVecBase2f(hAngles[i], vAngles[j]), LVecBase2f(hFOVs[i], vFOVs[j]),
          LVecBase2f(hNumRays[i], vNumRays[j]), rangeLimits, cameraResolution,
          acquireColor, acquireLabel);
      else
        c = new PerspectiveRangeCamera(stream.str(),
          LVecBase2f(hAngles[i], vAngles[j]), LVecBase2f(hFOVs[i], vFOVs[j]),
          LVecBase2f(hNumRays[i], vNumRays[j]), rangeLimits, cameraResolution,
          acquireColor, acquireLabel);
      c->reparent_to(*this);
      cameras.push_back(c);
    }
  }
}
