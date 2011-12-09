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

#ifndef SPHERICAL_RANGE_CAMERA_H
#define SPHERICAL_RANGE_CAMERA_H

/** Spherical range camera implementation
  * @author Ralf Kaestner ETHZ Autonomous Systems Lab.
  */

#include "morsel/sensors/range_camera.h"

class SphericalRangeCamera :
  public RangeCamera {
public:
  /** Constructors
    */
  SphericalRangeCamera(const std::string& name, const ShaderProgram&
    program, const LVecBase2f& angles, const LVecBase2f& fov, const
    LVecBase2f& numRays, const LVecBase2f& rangeLimits, const
    LVecBase2f& resolution = LVecBase2f(256, 256), bool
    acquireColor = false, std::string acquireLabel = "");
    
  /** Destructor
    */
  virtual ~SphericalRangeCamera();
protected:
  virtual void setupLens();
  virtual void setupRays();
};

#endif
