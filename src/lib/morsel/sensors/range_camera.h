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

#ifndef RANGE_CAMERA_H
#define RANGE_CAMERA_H

/** Abstract range camera class
  * @author Ralf Kaestner ETHZ Autonomous Systems Lab.
  */

#include "morsel/morsel.h"

#include <nodePath.h>
#include <pnmImage.h>
#include <texture.h>
#include <shader.h>
#include <graphicsOutput.h>

#include <string>

class RangeCamera :
  public NodePath {
public:
  /** Types and non-static subclasses
    */
  struct Ray {
    double x;
    double y;
    double z;
    double radius;
    double column;
    double row;
    double hAngle;
    double vAngle;
    double red;
    double green;
    double blue;
    size_t label;
  };

  struct RayInfo {
    double hAngle;
    double vAngle;
    double row;
    double column;
    double hTan;
    double vTan;
  };

  /** Constructors
    */
  RangeCamera(std::string name, const LVecBase2f& angles, const LVecBase2f&
    fov, const LVecBase2f& numRays, const LVecBase2f& rangeLimits, const
    LVecBase2f& resolution = LVecBase2f(128, 128), bool acquireColor = false,
    std::string acquireLabel = "");

  /** Destructor
    */
  virtual ~RangeCamera();

  const Lens& getLens() const;
  size_t getNumRays() const;
  const Texture& getDepthMap() const;
  const Texture& getColorMap() const;
  const Texture& getLabelMap() const;
  const RayInfo& getRayInfo(int index) const;
  const Ray& getRay(int index) const;
  double getDepth(int column, int row) const;
  void setActive(bool active);

  bool update(double time);
  void showFrustum();
  void hideFrustum();
protected:
  LVecBase2f angles;
  LVecBase2f fov;
  LVecBase2f numRays;
  LVecBase2f rangeLimits;
  LVecBase2f resolution;
  bool acquireColor;
  std::string acquireLabel;

  RayInfo* rayInfo;
  Ray* rays;

  PointerTo<GraphicsOutput> buffer;
  Texture depthMap;
  Texture colorMap;
  Texture labelMap;
  PNMImage depthTexels;
  PNMImage colorTexels;
  PNMImage labelTexels;
  PointerTo<Camera> cameraNode;
  NodePath camera;
  PointerTo<Shader> labelShader;

  void setupCamera(PointerTo<Lens> lens);
  void updateRays();

  virtual void setupLens() = 0;
};

#endif
