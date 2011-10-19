#include "laser_view.h"
#include "morsel/sensors/range_sensor.h"

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
    _node( new GeomNode( name + "GeomNode" ) ),
    _showPoints( showPoints ),
    _showLines( showLines ),
    _showColors( showColors ),
    _showLabels( showLabels )
{
  set_two_sided( true );
  set_depth_write( false );
  set_transparency( TransparencyAttrib::M_alpha );
  attach_new_node( _node );
  _node->adjust_draw_mask( PandaNode::get_all_camera_mask(), BitMask32( 1 ),
    BitMask32( 0 ) );
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
  if ( ! is_hidden() )
    updateRays();
  return true;
}

//------------------------------------------------------------------------------
// Protected methods
//------------------------------------------------------------------------------

double
LaserView::labelToHue( size_t label )
{
  size_t reverse = label;
  size_t shift = sizeof( size_t ) * CHAR_BIT - 1;

  for ( label >>= 1; label; label >>= 1 ) {
    reverse <<= 1;
    reverse |= label & 1;
    --shift;
  }
  reverse <<= shift;

  return (double)reverse / numeric_limits<size_t>::max() * 2.0 * M_PI;
}

Colorf
LaserView::hsvToRgb( double hue, double sat, double val )
{
  Colorf rgb;
  rgb[3] = 1.0;

  if ( sat > 0.0 ) {
    hue /= 60.0 * M_PI / 180.0;
    int i = floor( hue );
    double f = hue - i;
    double p = val * ( 1.0 - sat );
    double q = val * ( 1.0 - sat * f );
    double t = val * ( 1.0 - sat * ( 1.0 - f ) );

    switch( i ) {
      case 0:
        rgb[0] = val;
        rgb[1] = t;
        rgb[2] = p;
        break;
      case 1:
        rgb[0] = q;
        rgb[1] = val;
        rgb[2] = p;
        break;
      case 2:
        rgb[0] = p;
        rgb[1] = val;
        rgb[2] = t;
        break;
      case 3:
        rgb[0] = p;
        rgb[1] = q;
        rgb[2] = val;
        break;
      case 4:
        rgb[0] = t;
        rgb[1] = p;
        rgb[2] = val;
        break;
      default:
        rgb[0] = val;
        rgb[1] = p;
        rgb[2] = q;
        break;
    }
  }
  else {
    rgb[0] = val;
    rgb[1] = val;
    rgb[2] = val;
  }

  return rgb;
}
void
LaserView::setupRendering()
{
  _geomData = new GeomVertexData( "geometry", GeomVertexFormat::get_v3c4(),
    Geom::UH_dynamic );

  GeomVertexWriter v( _geomData, "vertex" );
  GeomVertexWriter c( _geomData, "color" );

  v.add_data3f( 0, 0, 0 );
  c.add_data4f( 0, 0, 0, 0 );
  for ( int i = 0; i < _sensor.rayCount(); i++ ) {
    v.add_data3f( 10, i - _sensor.rayCount() / 2.0, 0 );
    c.add_data4f( 0, 1, 1, 1 );
  }

  if ( _showLines ) {
    PT(GeomLines) line = new GeomLines( GeomLines( Geom::UH_static ) );
    for ( int i = 0; i < _sensor.rayCount(); i++ ) {
      line->add_vertex( 0 );
      line->add_vertex( i );
      line->close_primitive();
    }

    PT(Geom) geom = new Geom( _geomData );
    geom->add_primitive( line );
    _node->add_geom( geom );
  }

  if ( _showPoints ) {
    PT(GeomPoints) points = new GeomPoints( GeomPoints( Geom::UH_static ) );
    for ( int i = 0; i < _sensor.rayCount(); i++ ) {
      points->add_vertex( i );
      points->close_primitive();
    }

    PT(Geom) geom = new Geom( _geomData );
    geom->add_primitive( points );
    _node->add_geom( geom );
    set_render_mode_thickness( 3 );
  }
}

//------------------------------------------------------------------------------

void
LaserView::updateRays()
{
  GeomVertexWriter v( _geomData, "vertex" );
  v.set_row( 1 );
  GeomVertexWriter c( _geomData, "color" );
  c.set_row( 1 );

  for ( int i = 0; i < _sensor.rayCount(); i++ ) {
    RangeSensor::Ray & ray = _sensor.ray( i );
    double x = ray.x();
    double y = ray.y();
    double z = ray.z();
    double r = ray.radius();

    double red   = ray.red();
    double green = ray.green();
    double blue  = ray.blue();
    size_t label = ray.label();

    double val = 1.0 - r / _sensor.maxRange();
    if ( r <= 0 ) {
      val = 0;
      x   = 0;
      y   = 0;
    }
    v.set_data3f( x, y, z );
    if ( _showColors )
      c.set_data4f( red, green, blue, _color[3] );
    else if ( _showLabels ) {
      Colorf color = hsvToRgb( labelToHue( label ), 1.0, 1.0 );
      c.set_data4f( color[0], color[1], color[2], val );
    }
    else
      c.set_data4f( _color[0], _color[1], _color[2], val );
  }
}
