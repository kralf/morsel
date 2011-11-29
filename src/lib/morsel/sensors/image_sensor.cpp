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

#include "image_sensor.h"

#include <perspectiveLens.h>
#include <numeric>
#include <sstream>

using namespace std;

/*****************************************************************************/
/* Constructors and Destructor                                               */
/*****************************************************************************/

ImageSensor::ImageSensor(std::string name, const LVecBase2f& resolution,
    const LVecBase2f& rangeLimits, const LVecBase2f& filmSize, double
    focalLength) :
  NodePath(name),
  resolution(resolution),
  rangeLimits(rangeLimits),
  filmSize(filmSize),
  focalLength(focalLength),
  timestamp(0.0),
  lastTimestamp(0.0) {
  setupCamera();
}

ImageSensor::~ImageSensor() {
}

/*****************************************************************************/
/* Accessors                                                                 */
/*****************************************************************************/

const LVecBase2f& ImageSensor::getResolution() const {
  return resolution;
}

const Texture& ImageSensor::getColorMap() const {
  return colorMap;
}

double ImageSensor::getTimestamp() const {
  return timestamp;
}

const PNMImage& ImageSensor::getImage() const {
  if (timestamp > lastTimestamp) {
    colorMap.store(colorTexels);
    lastTimestamp = timestamp;
  }
  
  return colorTexels;
}

/*****************************************************************************/
/* Methods                                                                   */
/*****************************************************************************/

bool ImageSensor::update(double time) {
  timestamp = time;
  return true;
}

void ImageSensor::showFrustum() {
  cameraNode->show_frustum();
}

void ImageSensor::hideFrustum() {
  cameraNode->hide_frustum();
}

void ImageSensor::setupCamera() {
  PointerTo<GraphicsOutput> window = Morsel::getWindow(0);
  colorBuffer = window->make_texture_buffer("colormap", resolution[0],
    resolution[1], &colorMap, true);

  PointerTo<Lens> lens = new PerspectiveLens();
  lens->set_near_far(rangeLimits[0], rangeLimits[1]);
  lens->set_view_vector(1.0, 0.0, 0.0, 0.0, 0.0, 1.0);
  lens->set_film_size(filmSize[0], filmSize[1]);
  lens->set_focal_length(focalLength);

  cameraNode = new Camera("cam");
  cameraNode->set_camera_mask(BitMask32(1));
  cameraNode->set_scene(Morsel::getGSG()->get_scene()->get_scene_root());
  camera = attach_new_node(cameraNode);
  cameraNode->set_lens(lens);

  PointerTo<DisplayRegion> drc = colorBuffer->make_display_region();
  drc->set_sort(0);
  drc->set_camera(camera);
}
