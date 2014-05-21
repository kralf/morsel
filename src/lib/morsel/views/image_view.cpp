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

#include "image_view.h"
#include "morsel/sensors/image_sensor.h"

#include <pandaFramework.h>
#include <orthographicLens.h>
#include <cardMaker.h>

using namespace std;

/*****************************************************************************/
/* Constructors and Destructor                                               */
/*****************************************************************************/

ImageView::ImageView(string name, NodePath& sensor) :
  NodePath(name),
  sensor(static_cast<ImageSensor&>(sensor)) {
  setupRendering();
}

ImageView::~ImageView() {
}

/*****************************************************************************/
/* Methods                                                                   */
/*****************************************************************************/

bool ImageView::update(double time) {
  return true;
}

void ImageView::setupRendering() {
  PointerTo<GraphicsOutput> window = Morsel::getWindow(0);
  PointerTo<GraphicsEngine> engine = Morsel::getEngine();

  FrameBufferProperties fbProps = FrameBufferProperties::get_default();
  WindowProperties winProps = WindowProperties::get_default();
  winProps.set_size(sensor.getResolution()[0], sensor.getResolution()[1]);
  winProps.set_title(get_name());
  int flags = GraphicsPipe::BF_require_window |
    GraphicsPipe::BF_fb_props_optional;

  window = engine->make_output(window->get_pipe(), "Window", 0, fbProps,
    winProps, flags, window->get_gsg());

  sceneNode = new PandaNode("Scene");
  scene = NodePath(sceneNode);

  cameraNode = new Camera("Camera");
  cameraNode->set_scene(scene);
  camera = scene.attach_new_node(cameraNode);

  PointerTo<Lens> lens = new OrthographicLens();
  lens->set_film_size(2.0, 2.0);
  lens->set_near_far(-1.0, 1.0);
  cameraNode->set_lens(lens);

  scene.set_depth_test(false);
  scene.set_depth_write(false);

  PointerTo<DisplayRegion> drc = window->make_display_region();
  drc->set_camera(camera);

  CardMaker cm("Canvas");
  cm.set_frame(-1.0, 1.0, -1.0, 1.0);
  card = scene.attach_new_node(cm.generate());
  card.set_texture((Texture*)&sensor.getColorMap());
}
