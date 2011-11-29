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

#include "range_camera.h"

#include "morsel/utils/color.h"

#include <cmath>
#include <string>
#include <limits>

using namespace std;

/*****************************************************************************/
/* Constructors and Destructor                                               */
/*****************************************************************************/

RangeCamera::RangeCamera(string name, const LVecBase2f& angles, const
    LVecBase2f& fov, const LVecBase2f& numRays, const LVecBase2f& rangeLimits,
    const LVecBase2f& resolution, bool acquireColor, string acquireLabel) :
  NodePath(name),
  angles(angles),
  fov(fov),
  numRays(numRays),
  rangeLimits(rangeLimits),
  resolution(resolution),
  acquireColor(acquireColor),
  acquireLabel(acquireLabel),
  rays(numRays[0]*numRays[1]),
  timestamp(0.0),
  lastDepthTimestamp(0.0),
  lastColorTimestamp(0.0),
  lastLabelTimestamp(0.0) {
}

RangeCamera::~RangeCamera() {
}

/*****************************************************************************/
/* Accessors                                                                 */
/*****************************************************************************/

const Lens& RangeCamera::getLens() const {
  return *cameraNode->get_lens();
}

const Texture& RangeCamera::getDepthMap() const {
  return depthMap;
}

const Texture& RangeCamera::getColorMap() const {
  return colorMap;
}

const Texture& RangeCamera::getLabelMap() const {
  return labelMap;
}

size_t RangeCamera::getNumRays() const {
  return numRays[0]*numRays[1];
}

size_t RangeCamera::getNumHorizontalRays() const {
  return numRays[0];
}

size_t RangeCamera::getNumVerticalRays() const {
  return numRays[1];
}

const RangeCamera::Ray& RangeCamera::getRay(int index) const {
  return rays[index];
}

double RangeCamera::getTimestamp() const {
  return timestamp;
}

double RangeCamera::getDepth(int index) const {
  const Ray& ray = rays[index];
  
  if (timestamp > lastDepthTimestamp) {
    depthMap.store(depthTexels);
    lastDepthTimestamp = timestamp;
  }
  
  return rangeLimits[1]*rangeLimits[0]/(rangeLimits[1]-depthTexels.get_gray(
    ray.column, ray.row)*(rangeLimits[1]-rangeLimits[0]));
}

LPoint3f RangeCamera::getPoint(int index) const {
  const Ray& ray = rays[index];
  LPoint3f point;

  point[1] = getDepth(index);
  point[0] = point[1]*ray.hTan;
  point[2] = point[1]*ray.vTan;

  return point;
}

Colorf RangeCamera::getColor(int index) const {
  const Ray& ray = rays[index];
  Colorf color;
  
  if (timestamp > lastColorTimestamp) {
    colorMap.store(colorTexels);
    lastColorTimestamp = timestamp;
  }
  
  color[0] = colorTexels.get_red(ray.column, ray.row);
  color[1] = colorTexels.get_green(ray.column, ray.row);
  color[2] = colorTexels.get_blue(ray.column, ray.row);
  color[3] = 1.0;

  return color;
}

size_t RangeCamera::getLabel(int index) const {
  const Ray& ray = rays[index];
  
  if (timestamp > lastLabelTimestamp) {
    labelMap.store(labelTexels);
    lastLabelTimestamp = timestamp;
  }

  return Color::rgbToInt(labelTexels.get_xel_a(ray.column, ray.row));
}

void RangeCamera::setActive(bool active) {
  cameraNode->set_active(active);
}

/*****************************************************************************/
/* Methods                                                                   */
/*****************************************************************************/

bool RangeCamera::update(double time) {
  timestamp = time;
  return true;
}

void RangeCamera::showFrustum() {
  cameraNode->show_frustum();
}

void RangeCamera::hideFrustum() {
  cameraNode->hide_frustum();
}
                                          
void RangeCamera::setupCamera(PointerTo<Lens> lens) {
  depthMap.set_format(Texture::F_depth_component);
  depthMap.set_component_type(Texture::T_unsigned_short);
  depthMap.set_minfilter(Texture::FT_nearest);
  depthMap.set_magfilter(Texture::FT_nearest);
  colorMap.set_minfilter(Texture::FT_nearest);
  colorMap.set_magfilter(Texture::FT_nearest);
  labelMap.set_minfilter(Texture::FT_nearest);
  labelMap.set_magfilter(Texture::FT_nearest);

  buffer = Morsel::getWindow(0)->make_texture_buffer("depthmap",
    resolution[0], resolution[1], &depthMap, true);
  
  cameraNode = new Camera("cam");
  cameraNode->set_camera_mask(BitMask32(1));
  cameraNode->set_scene(Morsel::getGSG()->get_scene()->get_scene_root());
  cameraNode->set_lens(lens);

  camera = attach_new_node(cameraNode);
  camera.set_light_off(true);
  camera.set_material_off(true);
  camera.set_color_off(true);

  PointerTo<DisplayRegion> drd = buffer->make_display_region();
  drd->set_sort(0);
  drd->set_camera(camera);
  
  if (acquireColor) {
    buffer->add_render_texture(&colorMap, GraphicsOutput::RTM_copy_ram,
      DrawableRegion::RTP_color);
  }
  else if (!acquireLabel.empty()) {
    buffer->add_render_texture(&labelMap, GraphicsOutput::RTM_copy_ram,
      DrawableRegion::RTP_color);
    
    ostringstream stream;
    stream << "void vshader(uniform float4x4 mat_modelproj," << endl;
    stream << "    in float4 vtx_position : POSITION," << endl;
    stream << "    out float4 l_position : POSITION) {" << endl;
    stream << "  l_position = mul(mat_modelproj, vtx_position);" << endl;
    stream << "}" << endl;
    stream << "void fshader(uniform float4 " << acquireLabel << "," << endl;
    stream << "    out float4 o_color : COLOR) {" << endl;
    stream << "  o_color = " << acquireLabel << ";" << endl;
    stream << "}" << endl;
    labelShader = Shader::make(stream.str(), Shader::SL_Cg);
    
    NodePath shaderAttrib("shader label");
    shaderAttrib.set_shader(labelShader);
    shaderAttrib.set_shader_input(acquireLabel, Color::intToRgb(0));
    cameraNode->set_initial_state(shaderAttrib.get_state());
    buffer->set_clear_color(Color::intToRgb(0));
  }
}
