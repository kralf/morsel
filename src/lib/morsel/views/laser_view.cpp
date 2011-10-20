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

//------------------------------------------------------------------------------

LaserView::LaserView(
  std::string name,
  NodePath & sensor,
  float r,
  float g,
  float b,
  float a,
  bool showPoints,
  bool showLines,
  bool showColors,
  bool showLabels                   
) : NodePath( name ),
    _name( name ),
    _sensor( static_cast<RangeSensor&>( sensor ) ),
    _color( r, g, b, a ),
    _showPoints( showPoints ),
    _showLines( showLines ),
    _showColors( showColors ),
    _showLabels( showLabels )
{
  set_two_sided( true );
  set_depth_write( false );
  set_transparency( TransparencyAttrib::M_alpha );
  setupRendering();
}

//------------------------------------------------------------------------------

LaserView::~LaserView()
{
}

//------------------------------------------------------------------------------

bool
LaserView::update( double time )
{
  return true;
}

//------------------------------------------------------------------------------
// Protected methods
//------------------------------------------------------------------------------

void
LaserView::setupRendering()
{
  for ( int ci = 0; ci < _sensor.cameraCount(); ci++ ) {
    stringstream s;
    s << get_name() << "GeomNode" << ci;
    
    _nodes.push_back( new GeomNode( s.str() ) );
    _nodes[ci]->adjust_draw_mask( PandaNode::get_all_camera_mask(),
      BitMask32( 1 ), BitMask32( 0 ) );
    NodePath path = attach_new_node( _nodes[ci] );
    path.set_hpr( _sensor.camera( ci ).get_hpr() );
    _geomData.push_back( new GeomVertexData( "geometry",
      GeomVertexFormat::get_v3c4t2(), Geom::UH_dynamic ) );

    GeomVertexWriter v( _geomData[ci], "vertex" );
    GeomVertexWriter c( _geomData[ci], "color" );
    GeomVertexWriter t( _geomData[ci], "texcoord" );

    double width = _sensor.camera( ci ).depthMap().get_x_size();
    double height = _sensor.camera( ci ).depthMap().get_y_size();
    
    v.add_data3f( 0.0, 0.0, 0.0 );
    c.add_data4f( 0.0, 0.0, 0.0, 0.0 );
    t.add_data2f( 0.0, 0.0 );
    for ( int ri = 0; ri < _sensor.camera( ci ).rayCount(); ri++ ) {
      v.add_data3f( _sensor.camera( ci ).rayInfo( ri ).hTan,
        _sensor.camera( ci ).rayInfo( ri ).vTan, 1.0 );
      c.add_data4f( _color );
      t.add_data2f( _sensor.camera( ci ).rayInfo( ri ).column / width,
        1.0 - _sensor.camera( ci ).rayInfo( ri ).row / height );
    }

    PT(Geom) geom;
    if ( _showLines ) {
      PT(GeomLines) line = new GeomLines( GeomLines( Geom::UH_static ) );
      for ( int ri = 0; ri < _sensor.rayCount(); ri++ ) {
        line->add_vertex( 0 );
        line->add_vertex( ri );
        line->close_primitive();
      }

      geom = new Geom( _geomData[ci] );
      geom->add_primitive( line );
      _nodes[ci]->add_geom( geom );
    }
    else if ( _showPoints ) {
      PT(GeomPoints) points = new GeomPoints( GeomPoints( Geom::UH_static ) );
      for ( int ri = 0; ri < _sensor.camera( ci ).rayCount(); ri++ ) {
        points->add_vertex( ri );
        points->close_primitive();
      }

      geom = new Geom( _geomData[ci] );
      geom->add_primitive( points );
      path.set_render_mode_thickness( 3 );
      _nodes[ci]->add_geom( geom );
    }
    geom->set_bounds( _sensor.camera( ci ).lens().make_bounds() );
    
    TextureStage * depthMap = new TextureStage( "depthmap" );
    path.set_texture( depthMap, &_sensor.camera( ci ).depthMap() );
    if ( _showColors ) {
      TextureStage * colorMap = new TextureStage( "colormap" );
      path.set_texture( colorMap, &_sensor.camera( ci ).colorMap() );
    }
    else if ( _showLabels ) {
      TextureStage * labelMap = new TextureStage( "labelmap" );
      path.set_texture( labelMap, &_sensor.camera( ci ).labelMap() );
    }
  }

  ostringstream stream;
  stream << "void vshader(uniform float4x4 mat_modelproj," << endl;
  stream << "    uniform float4 range_limits," << endl;
  stream << "    uniform sampler2D tex_0 : TEXUNIT0," << endl;
  if ( _showColors || _showLabels )
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
  if ( _showColors || _showLabels )
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
  
  _pointShader = Shader::make( stream.str(), Shader::SL_Cg );
  set_shader( _pointShader );
  set_shader_input( "range_limits", LVecBase4f( _sensor.minRange(),
    _sensor.maxRange(), 0.0, 0.0 ) );
}
