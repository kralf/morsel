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

#include "perspective_range_camera.h"

#include <perspectiveLens.h>
#include <graphicsEngine.h>
#include <cmath>
#include <string>

using namespace std;

/*****************************************************************************/
/* Constructors and Destructor                                               */
/*****************************************************************************/

PerspectiveRangeCamera::PerspectiveRangeCamera(const string& name, const
    ShaderProgram& program, const LVecBase2f& angles, const LVecBase2f& fov,
    const LVecBase2f& numRays, const LVecBase2f& rangeLimits, const
    LVecBase2f& resolution, bool acquireColor, string acquireLabel, const
    BitMask32& cameraMask) :
  RangeCamera(name, program, angles, fov, numRays, rangeLimits, resolution,
    acquireColor, acquireLabel, cameraMask) {
  setupLens();
  setupRays();
}

PerspectiveRangeCamera::~PerspectiveRangeCamera() {
}

/*****************************************************************************/
/* Methods                                                                   */
/*****************************************************************************/

void PerspectiveRangeCamera::setupLens() {
  PointerTo<Lens> lens = new PerspectiveLens();
  lens->set_near_far(rangeLimits[0], rangeLimits[1]);
  lens->set_fov(fov[0]*180.0/M_PI, fov[1]*180.0/M_PI);

  setupCamera(lens);

  set_hpr(angles[0]*180.0/M_PI-90.0, angles[1]*180.0/M_PI, 0.0);
}

void PerspectiveRangeCamera::setupRays() {
  LVecBase2f angle;
  LVecBase2f deltaAngle;
  
  deltaAngle[0] = fov[0];
  angle[0] = 0.0;
  if (numRays[0] > 1) {
    deltaAngle[0] = fov[0]/numRays[0];
    angle[0] = 0.5*(-fov[0]+deltaAngle[0]);
  }

  deltaAngle[1] = fov[1];
  if (numRays[1] > 1)
    deltaAngle[1] = fov[1]/numRays[1];

  int index = 0;
  while (angle[0] < 0.5*fov[0]) {
    angle[1] = 0.0;
    if (numRays[1] > 1)
      angle[1] = 0.5*(-fov[1]+deltaAngle[1]);

    while (angle[1] < 0.5*fov[1]) {
      LPoint3f point, dist;
      point[0] = rangeLimits[1]*tan(angle[0]);
      point[1] = rangeLimits[1];
      point[2] = rangeLimits[1]*tan(angle[1]);
      cameraNode->get_lens()->project(point, dist);

      double column = 0.5*resolution[0]*(1.0+dist[0]);
      double row = 0.5*resolution[1]*(1.0-dist[1]);

      Ray ray;
      ray.row = round(row);
      ray.column = round(column);
      ray.hAngle = angle[0];
      ray.vAngle = angle[1];
      ray.hTan = tan(ray.hAngle);
      ray.vTan = tan(ray.vAngle);

      rays[index] = ray;
      ++index;

      angle[1] += deltaAngle[1];
    }
    angle[0] += deltaAngle[0];
  }
}
