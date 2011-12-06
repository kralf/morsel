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
  timestamp(0.0),
  lastTimestamp(0.0),
  rays(numRays[0]*numRays[1]) {
  setupCameras();
}

RangeSensor::~RangeSensor() {
  for (int i = 0; i < cameras.size(); ++i)
    delete cameras[i];
}

/*****************************************************************************/
/* Accessors                                                                 */
/*****************************************************************************/

const LVecBase2f& RangeSensor::getMinAngles() const {
  return minAngles;
}

const LVecBase2f& RangeSensor::getMaxAngles() const {
  return maxAngles;
}

const LVecBase2f& RangeSensor::getResolution() const {
  return resolution;
}

const LVecBase2f& RangeSensor::getRangeLimits() const {
  return rangeLimits;
}

const LVecBase2f& RangeSensor::getFOV() const {
  return fov;
}

size_t RangeSensor::getNumCameras() const {
  return numCameras[0]*numCameras[1];
}

const RangeCamera& RangeSensor::getCamera(int index) const {
  return *cameras[index];
}

size_t RangeSensor::getNumRays() const {
  return numRays[0]*numRays[1];
}

const RangeSensor::Ray& RangeSensor::getRay(int index) const {
  if (timestamp > lastTimestamp) {
    updateRays();
    lastTimestamp = timestamp;
  }

  return rays[index];
}

double RangeSensor::getTimestamp() const {
  return timestamp;
}

/*****************************************************************************/
/* Methods                                                                   */
/*****************************************************************************/

bool RangeSensor::update(double time) {
  timestamp = time;
  
  for (int i = 0; i < cameras.size(); ++i)
    cameras[i]->update(time);
  
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

  numCameras[0] = hFOVs.size();
  numCameras[1] = vFOVs.size();
    
  for (int i = 0; i < numCameras[1]; ++i) {
    for (int j = 0; j < numCameras[0]; ++j) {
      stringstream stream;
      stream << get_name() << "_" << i << "x" << j;

      RangeCamera* camera;
      if (spherical)
        camera = new SphericalRangeCamera(stream.str(),
          LVecBase2f(hAngles[j], vAngles[i]), LVecBase2f(hFOVs[j], vFOVs[i]),
          LVecBase2f(hNumRays[j], vNumRays[i]), rangeLimits, cameraResolution,
          acquireColor, acquireLabel);
      else
        camera = new PerspectiveRangeCamera(stream.str(),
          LVecBase2f(hAngles[j], vAngles[i]), LVecBase2f(hFOVs[j], vFOVs[i]),
          LVecBase2f(hNumRays[j], vNumRays[i]), rangeLimits, cameraResolution,
          acquireColor, acquireLabel);
          
      camera->reparent_to(*this);
      cameras.push_back(camera);
    }
  }
}

void RangeSensor::updateRays() const {
  int c_i = 0;
  int i_c = 0;
  for (int i = 0; i < numRays[1]; ++i, ++i_c) {
    int c_ij = c_i*numCameras[0];
    if (i_c >= cameras[c_ij]->getNumVerticalRays()) {
      i_c = 0;
      ++c_i;
      c_ij += numCameras[0];
    }
    
    int c_j = 0;
    int j_c = 0;
    for (int j = 0; j < numRays[0]; ++j, ++j_c) {
      int ij = i*numRays[0]+j;
      if (j_c >= cameras[c_ij]->getNumHorizontalRays()) {
        j_c = 0;
        ++c_j;
        ++c_ij;
      }
      int ij_c = i_c*cameras[c_ij]->getNumHorizontalRays()+j_c;

      rays[ij].point = get_relative_point(*cameras[c_ij],
        cameras[c_ij]->getPoint(ij_c));

      double radius = rays[ij].point.length();
      if ((radius <= rangeLimits[0]) || (radius >= rangeLimits[1]))
        rays[ij].valid = false;
      else
        rays[ij].valid = true;

      if (acquireColor)
        rays[ij].color = cameras[c_ij]->getColor(ij_c);
      else
        rays[ij].color.fill(0.0);

      if (!acquireLabel.empty())
        rays[ij].label = cameras[c_ij]->getLabel(ij_c);
      else
        rays[ij].label = 0;
    }
  }
}
