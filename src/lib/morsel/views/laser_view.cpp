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

LaserView::LaserView(std::string name, NodePath& sensor, const Colorf&
    color, bool showPoints, bool showLines, bool showColors, bool showLabels) :
  NodePath(name),
  sensor(static_cast<RangeSensor&>(sensor)),
  color(color),
  showPoints(showPoints),
  showLines(showLines),
  showColors(showColors),
  showLabels(showLabels) {
  set_two_sided(true);
  set_depth_write(false);
  set_transparency(TransparencyAttrib::M_alpha);
  setupRendering();
}

LaserView::~LaserView() {
}

/*****************************************************************************/
/* Methods                                                                   */
/*****************************************************************************/

bool LaserView::update(double time) {
  return true;
}

void LaserView::setupRendering() {
  for (int ci = 0; ci < sensor.getNumCameras(); ++ci) {
    stringstream stream;
    stream << get_name() << "GeomNode" << ci;
    
    nodes.push_back(new GeomNode(stream.str()));
    nodes[ci]->adjust_draw_mask(PandaNode::get_all_camera_mask(),
      BitMask32(1), BitMask32(0));
    NodePath path = attach_new_node(nodes[ci]);
    path.set_hpr(sensor.getCamera(ci).get_hpr());
    geomData.push_back(new GeomVertexData("geometry",
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
      PointerTo<GeomLines> line = new GeomLines(GeomLines(Geom::UH_static));
      for (int ri = 0; ri < sensor.getCamera(ci).getNumRays(); ++ri) {
        line->add_vertex(0);
        line->add_vertex(ri+1);
        line->close_primitive();
      }

      geom = new Geom(geomData[ci]);
      geom->add_primitive(line);
      nodes[ci]->add_geom(geom);
    }
    else if (showPoints) {
      PointerTo<GeomPoints> points =
        new GeomPoints(GeomPoints(Geom::UH_static));
      for (int ri = 0; ri < sensor.getCamera(ci).getNumRays(); ++ri) {
        points->add_vertex(ri+1);
        points->close_primitive();
      }

      geom = new Geom(geomData[ci]);
      geom->add_primitive(points);
      path.set_render_mode_thickness(3);
      nodes[ci]->add_geom(geom);
    }
    if (geom)
      geom->set_bounds(sensor.getCamera(ci).getLens().make_bounds());
    
    PointerTo<TextureStage> depthMap = new TextureStage("depthmap");
    path.set_texture(depthMap, (Texture*)&sensor.getCamera(ci).getDepthMap());
    if (showColors) {
      PointerTo<TextureStage> colorMap = new TextureStage("colormap");
      path.set_texture(colorMap, (Texture*)&sensor.getCamera(ci).getColorMap());
    }
    else if (showLabels) {
      PointerTo<TextureStage> labelMap = new TextureStage("labelmap");
      path.set_texture(labelMap, (Texture*)&sensor.getCamera(ci).getLabelMap());
    }
  }

  ostringstream stream;
  stream << "void vshader(uniform float4x4 mat_modelproj," << endl;
  stream << "    uniform float4 range_limits," << endl;
  stream << "    uniform sampler2D tex_0 : TEXUNIT0," << endl;
  if (showColors || showLabels)
    stream << "    uniform sampler2D tex_1 : TEXUNIT1," << endl;
  stream << "    in float4 vtx_position : POSITION," << endl;
  stream << "    in float4 vtx_color : COLOR," << endl;
  stream << "    in float2 vtx_texcoord0 : TEXCOORD0," << endl;
  stream << "    out float4 l_position : POSITION," << endl;
  stream << "    out float4 l_color : COLOR) {" << endl;
  stream << "  l_position = float4(0.0, 0.0, 0.0, 1.0);" << endl;
  stream << "  l_color = vtx_color;" << endl;
  stream << "  if (vtx_position[2] > 0.0) {" << endl;
  stream << "    float depth = tex2D(tex_0, vtx_texcoord0).r;" << endl;
  stream << "    float range = range_limits[1]*range_limits[0]/" << endl;
  stream << "      (range_limits[1]-depth*" << endl;
  stream << "      (range_limits[1]-range_limits[0]));" << endl;
  stream << "    if ((range > range_limits[0]) &&" << endl;
  stream << "        (range < range_limits[1])) {" <<endl;
  stream << "      l_position = float4(range*vtx_position[0]," << endl;
  stream << "         range, range*vtx_position[1], 1.0);" << endl;
  if (showColors || showLabels)
    stream << "      l_color = tex2D(tex_1, vtx_texcoord0);" << endl;
  stream << "      l_color[3] = 1.0-range/range_limits[1];" << endl;
  stream << "    }" << endl;
  stream << "    else l_color[3] = 0.0;" << endl;
  stream << "  }" << endl;
  stream << "  l_position = mul(mat_modelproj, l_position);" << endl;
  stream << "}" << endl;
  stream << "void fshader(in float4 l_color : COLOR," << endl;
  stream << "    out float4 o_color : COLOR) {" << endl;
  stream << "  o_color = l_color;" << endl;
  stream << "}" << endl;

  pointShader = Shader::make(stream.str(), Shader::SL_Cg);
  set_shader(pointShader);
  set_shader_input("range_limits", LVecBase4f(sensor.getRangeLimits()[0],
    sensor.getRangeLimits()[1], 0.0, 0.0));
}
