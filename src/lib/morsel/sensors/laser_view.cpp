#include "laser_view.h"

#include <geomVertexWriter.h>
#include <geomVertexFormat.h>
#include <geomVertexData.h>
#include <geomNode.h>
#include <geom.h>
#include <geomLines.h>
#include <geomPoints.h>

using namespace std;

//------------------------------------------------------------------------------

LaserView::LaserView(
  std::string name,
  RangeSensor & laser,
  float r,
  float g,
  float b,
  float a,
  bool points,
  bool lines,
  bool colorInfo
) : NodePath( name ),
    _name( name ),
    _laser( laser ),
    _color( r, g, b, a ),
    _node( new GeomNode( name + "GeomNode" ) ),
    _points( points ),
    _lines( lines ),
    _colorInfo( colorInfo )
{
  set_two_sided( true );
  set_depth_write( false );
  set_transparency( TransparencyAttrib::M_alpha );
  attach_new_node( _node );
  _node->adjust_draw_mask( PandaNode::get_all_camera_mask(), BitMask32( 1 ), BitMask32( 0 ) );
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
// Private methods
//------------------------------------------------------------------------------

void
LaserView::setupRendering()
{
  _geomData = new GeomVertexData( "geometry", GeomVertexFormat::get_v3c4(), Geom::UH_dynamic );

  GeomVertexWriter v( _geomData, "vertex" );
  GeomVertexWriter c( _geomData, "color" );

  v.add_data3f( 0, 0, 0 );
  c.add_data4f( 0, 0, 0, 0 );
  for ( int i = 0; i < _laser.rayCount(); i++ ) {
    v.add_data3f( 10, i - _laser.rayCount() / 2.0, 0 );
    c.add_data4f( 0, 1, 1, 1 );
  }

  if ( _lines ) {
    PT(GeomLines) line = new GeomLines( GeomLines( Geom::UH_static ) );
    for ( int i = 0; i < _laser.rayCount(); i++ ) {
      line->add_vertex( 0 );
      line->add_vertex( i );
      line->close_primitive();
    }

    PT(Geom) geom = new Geom( _geomData );
    geom->add_primitive( line );
    _node->add_geom( geom );
  }

  if ( _points ) {
    PT(GeomPoints) points = new GeomPoints( GeomPoints( Geom::UH_static ) );
    for ( int i = 0; i < _laser.rayCount(); i++ ) {
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

  for ( int i = 0; i < _laser.rayCount(); i++ ) {
    RangeSensor::Ray & ray = _laser.ray( i );
    double x = ray.x();
    double y = ray.y();
    double z = ray.z();
    double r = ray.radius();

    double red   = ray.red();
    double green = ray.green();
    double blue  = ray.blue();

    double val = 1.0 - r / _laser.maxRange();
    if ( r <= 0 ) {
      val = 0;
      x   = 0;
      y   = 0;
    }
    v.set_data3f( x, y, z );
    if ( _colorInfo )
      c.set_data4f( red, green, blue, _color[3] );
    else
      c.set_data4f( _color[0], _color[1], _color[2], val );
  }
}
