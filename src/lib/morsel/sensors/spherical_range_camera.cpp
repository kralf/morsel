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

#include "spherical_range_camera.h"

#include <perspectiveLens.h>
#include <graphicsEngine.h>
#include <cmath>
#include <string>

using namespace std;

/*****************************************************************************/
/* Constructors and Destructor                                               */
/*****************************************************************************/

SphericalRangeCamera::SphericalRangeCamera(const string& name, const
    ShaderProgram& program, const LVecBase2f& angles, const LVecBase2f& fov,
    const LVecBase2f& numRays, const LVecBase2f& rangeLimits, const
    LVecBase2f& resolution, bool acquireColor, string acquireLabel) :
  RangeCamera(name, program, angles, fov, numRays, rangeLimits, resolution,
    acquireColor, acquireLabel) {
  setupLens();
  setupRays();
}

SphericalRangeCamera::~SphericalRangeCamera() {
}

/*****************************************************************************/
/* Methods                                                                   */
/*****************************************************************************/

void SphericalRangeCamera::setupLens() {
  PointerTo<Lens> lens = new PerspectiveLens();
  lens->set_near_far(rangeLimits[0], rangeLimits[1]);
  setupCamera(lens);
  
  double minHAngle = angles[0]-0.5*fov[0];
  double maxHAngle = angles[0]+0.5*fov[0];
  double minVAngle = angles[1]-0.5*fov[1];
  double maxVAngle = angles[1]+0.5*fov[1];

  LPoint3f ll(
    cos(maxHAngle)*cos(minVAngle),
    sin(maxHAngle)*cos(minVAngle),
    sin(minVAngle));
  LPoint3f lr(
    cos(minHAngle)*cos(minVAngle),
    sin(minHAngle)*cos(minVAngle),
    sin(minVAngle));
  LPoint3f ul(
    cos(maxHAngle)*cos(maxVAngle),
    sin(maxHAngle)*cos(maxVAngle),
    sin(maxVAngle));
  LPoint3f ur(
    cos(minHAngle)*cos(maxVAngle),
    sin(minHAngle)*cos(maxVAngle),
    sin(maxVAngle));

  lens->set_frustum_from_corners(
    camera.get_relative_point(get_parent(), ul),
    camera.get_relative_point(get_parent(), ur),
    camera.get_relative_point(get_parent(), ll),
    camera.get_relative_point(get_parent(), lr),
    Lens::FC_aspect_ratio | Lens::FC_off_axis);
  set_hpr(lens->get_view_hpr());
  lens->set_view_hpr(0.0, 0.0, 0.0);
}

void SphericalRangeCamera::setupRays() {
  LVecBase2f angle;
  LVecBase2f deltaAngle;

  deltaAngle[0] = fov[0];
  angle[0] = 0.0;
  if (numRays[0]  > 1) {
    deltaAngle[0] = fov[0]/numRays[0];
    angle[0] = 0.5*(-fov[0]+deltaAngle[0]) ;
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
      LPoint3f point = camera.get_relative_point(get_parent(), LPoint3f(
        cos(angles[0]+angle[0])*cos(angles[1]+angle[1]),
        sin(angles[0]+angle[0])*cos(angles[1]+angle[1]),
        sin(angles[1]+angle[1])));
      LPoint2f dist;
      cameraNode->get_lens()->project(point, dist);

      double column = 0.5*resolution[0]*(1.0+dist[0]);
      double row = 0.5*resolution[1]*(1.0-dist[1]);
      
      Ray ray;
      ray.row = round(row);
      ray.column = round(column);
      ray.hAngle = atan2(point[0], point[1]);
      ray.vAngle = atan2(point[2], point[1]);
      ray.hTan = tan(ray.hAngle);
      ray.vTan = tan(ray.vAngle);

      rays[index] = ray;
      ++index;

      angle[1] += deltaAngle[1];
    }
    angle[0] += deltaAngle[0];
  }
}
