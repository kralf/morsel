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

#ifndef IMAGE_SENSOR_H
#define IMAGE_SENSOR_H

/** Image sensor implementation
  * @author Ralf Kaestner ETHZ Autonomous Systems Lab.
  */

#include "morsel/morsel.h"

#include <nodePath.h>
#include <pnmImage.h>
#include <texture.h>
#include <graphicsOutput.h>

#include <string>

class ImageSensor :
  public NodePath {
PUBLISHED:
  /** Constructors
    */
  ImageSensor(std::string name, const LVecBase2f& resolution, const
    LVecBase2f& rangeLimits, const LVecBase2f& filmSize, double focalLength,
    const BitMask32& cameraMask = BitMask32::all_on());

  /** Destructor
    */
  virtual ~ImageSensor();

  const LVecBase2f& getResolution() const;
  const Texture& getColorMap() const;
  double getTimestamp() const;
  const PNMImage& getImage() const;
  const Camera& getCamera() const;
  
  bool update(double time);
  void showFrustum();
  void hideFrustum();
protected:
  LVecBase2f resolution;
  LVecBase2f rangeLimits;
  LVecBase2f filmSize;
  double focalLength;
  BitMask32 cameraMask;

  PointerTo<GraphicsOutput> colorBuffer;
  Texture colorMap;
  PointerTo<Camera> cameraNode;
  NodePath camera;

  double timestamp;
  mutable double lastTimestamp;
  mutable PNMImage colorTexels;
  
  void setupCamera();
};

#endif
