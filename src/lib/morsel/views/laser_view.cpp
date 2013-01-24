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

#include "laser_view.h"

#include "morsel/sensors/range_sensor.h"
#include "morsel/utils/color.h"

#include <geomVertexWriter.h>
#include <geomVertexFormat.h>
#include <geomVertexData.h>
#include <geomNode.h>
#include <geom.h>
#include <geomLines.h>
#include <geomPoints.h>

#include <limits>

using namespace std;

/*****************************************************************************/
/* Constructors and Destructor                                               */
/*****************************************************************************/

LaserView::LaserView(std::string name, NodePath& sensor, ShaderProgram&
    program, const Colorf& color, bool showPoints, bool showLines,
    bool showColors, bool showLabels, bool useAlpha) :
  NodePath(name),
  sensor(static_cast<RangeSensor&>(sensor)),
  color(color),
  showPoints(showPoints),
  showLines(showLines),
  showColors(showColors),
  showLabels(showLabels),
  useAlpha(useAlpha),
  shader(0) {
  set_two_sided(true);
  set_depth_write(false);
  set_color_off();
  set_transparency(TransparencyAttrib::M_alpha);
  setupGeometries();
  if (program.isEmpty())
    set_texture_off(numeric_limits<int>::max());
  else
    setupShader(program);
}

LaserView::~LaserView() {
}

/*****************************************************************************/
/* Methods                                                                   */
/*****************************************************************************/

bool LaserView::update(double time) {
  if (!shader && sensor.getTimestamp())
    updateGeometries();
  
  return true;
}

void LaserView::setupGeometries() {
  set_light_off(numeric_limits<int>::max());
  
  for (int ci = 0; ci < sensor.getNumCameras(); ++ci) {
    stringstream stream;
    stream << get_name() << "Geometries" << ci;
    
    nodes.push_back(new PandaNode(stream.str()));
    nodes[ci]->adjust_draw_mask(PandaNode::get_all_camera_mask(),
      BitMask32(1), BitMask32(0));
    NodePath path = attach_new_node(nodes[ci]);
    path.set_hpr(sensor.getCamera(ci).get_hpr());
    
    geomData.push_back(new GeomVertexData("Geometry",
      GeomVertexFormat::get_v3c4t2(), Geom::UH_dynamic));
    GeomVertexWriter v(geomData[ci], "vertex");
    GeomVertexWriter c(geomData[ci], "color");
    GeomVertexWriter t(geomData[ci], "texcoord");

    double width = sensor.getCamera(ci).getDepthMap().get_x_size();
    double height = sensor.getCamera(ci).getDepthMap().get_y_size();
    
    v.add_data3f(0.0, 0.0, 0.0);
    c.add_data4f(0.0, 0.0, 0.0, 0.0);
    t.add_data2f(0.0, 0.0);
    for (int ri = 0; ri < sensor.getCamera(ci).getNumRays(); ++ri) {
      v.add_data3f(sensor.getCamera(ci).getRay(ri).hTan,
        sensor.getCamera(ci).getRay(ri).vTan, 1.0);
      c.add_data4f(color);
      t.add_data2f(sensor.getCamera(ci).getRay(ri).column/width,
        1.0-sensor.getCamera(ci).getRay(ri).row/height);
    }

    PointerTo<Geom> geom = 0;
    if (showLines) {
      stringstream lineStream;
      lineStream << get_name() << "Lines" << ci;
      
      PointerTo<GeomLines> line = new GeomLines(GeomLines(Geom::UH_static));
      for (int ri = 0; ri < sensor.getCamera(ci).getNumRays(); ++ri) {
        line->add_vertex(0);
        line->add_vertex(ri+1);
        line->close_primitive();
      }

      geom = new Geom(geomData[ci]);
      geom->add_primitive(line);
      geom->set_bounds(sensor.getCamera(ci).getLens().make_bounds());
      
      GeomNode* lineNode = new GeomNode(lineStream.str());
      lineNode->add_geom(geom);
      path.attach_new_node(lineNode);
    }
    if (showPoints) {
      stringstream pointStream;
      pointStream << get_name() << "Points" << ci;

      PointerTo<GeomPoints> points =
        new GeomPoints(GeomPoints(Geom::UH_static));
      for (int ri = 0; ri < sensor.getCamera(ci).getNumRays(); ++ri) {
        points->add_vertex(ri+1);
        points->close_primitive();
      }

      geom = new Geom(geomData[ci]);
      geom->add_primitive(points);
      geom->set_bounds(sensor.getCamera(ci).getLens().make_bounds());

      GeomNode* pointNode = new GeomNode(pointStream.str());
      pointNode->add_geom(geom);
      NodePath pointPath = path.attach_new_node(pointNode);
      pointPath.set_render_mode_thickness(3);
    }
    
    PointerTo<TextureStage> depthMap = new TextureStage("DepthMap");
    path.set_texture(depthMap, (Texture*)&sensor.getCamera(ci).getDepthMap());
    if (showColors) {
      PointerTo<TextureStage> colorMap = new TextureStage("ColorMap");
      path.set_texture(colorMap, (Texture*)&sensor.getCamera(ci).getColorMap());
    }
    else if (showLabels) {
      PointerTo<TextureStage> labelMap = new TextureStage("LabelMap");
      path.set_texture(labelMap, (Texture*)&sensor.getCamera(ci).getLabelMap());
    }
  }
}

void LaserView::setupShader(ShaderProgram& program) {
  if ((showColors && sensor.acquiresColor()) ||
      (showLabels && sensor.acquiresLabel()))
    program.define("HAVE_COLOR");

  shader = program.make();

  set_shader(shader);
  set_shader_input("rangeLimits", LVecBase4f(sensor.getRangeLimits()[0],
    sensor.getRangeLimits()[1], 0.0, 0.0));
}

void LaserView::updateGeometries() {
  const LVecBase2f& rangeLimits = sensor.getRangeLimits();
  
  for (int ci = 0; ci < sensor.getNumCameras(); ++ci) {
    const RangeCamera& camera = sensor.getCamera(ci);
    GeomVertexWriter v(geomData[ci], "vertex");
    v.set_row(1);
    GeomVertexWriter c(geomData[ci], "color");
    c.set_row(1);
    
    for (int ri = 0; ri < camera.getNumRays(); ++ri) {
      LPoint3f point = camera.getPoint(ri);
      Colorf color = this->color;

      if (showColors && sensor.acquiresColor())
        color = camera.getColor(ri);
      else if (showLabels && sensor.acquiresLabel())
        color = camera.getLabelColor(ri);

      if (useAlpha) {
        double radius = point.length();
        if ((radius > rangeLimits[0]) && (radius < rangeLimits[1]))
          color[3] = 1.0-radius/rangeLimits[1];
        else
          color[3] = 0.0;
      }
      else
        color[3] = 1.0;

      v.set_data3f(point);
      c.set_data4f(color);
    }
  }
}
