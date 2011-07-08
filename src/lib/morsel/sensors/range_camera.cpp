#include "range_camera.h"

#include <perspectiveLens.h>
#include <graphicsEngine.h>
#include <cmath>
#include <string>

using namespace std;

//------------------------------------------------------------------------------

struct RangeCamera::RayInfo {
  double hAngle;
  double vAngle;
  int row;
  int column;
  double hTan;
  double vTan;
};

//------------------------------------------------------------------------------

RangeCamera::RangeCamera(
  std::string name,
  double horizontalFOV,
  double verticalFOV,
  int horizontalRays,
  int verticalRays,
  double minRange,
  double maxRange,
  bool colorInfo )
  : NodePath( name ),
    _name( name ),
    _horizontalFOV( horizontalFOV ),
    _verticalFOV( verticalFOV ),
    _horizontalRays( horizontalRays ),
    _verticalRays( verticalRays ),
    _minRange( minRange ),
    _maxRange( maxRange ),
    _width( 128 ),
    _height( 128 ),
    _rayCount( horizontalRays * verticalRays ),
    _rayInfo( new RayInfo[_rayCount] ),
    _rays( new Ray[_rayCount] ),
    _colorInfo( colorInfo )
{
  setupCamera();
  setupRays();
}

//------------------------------------------------------------------------------

RangeCamera::~RangeCamera()
{
  delete [] _rayInfo;
  delete [] _rays;
}

//------------------------------------------------------------------------------

int
RangeCamera::rayCount()
{
  return _rayCount;
}

//------------------------------------------------------------------------------

Ray &
RangeCamera::ray( int index ) {
  return _rays[index];
}

//------------------------------------------------------------------------------

bool
RangeCamera::update( double time )
{
  _depthMap.store( _depth_texels );
  if ( _colorInfo )
    _colorMap.store( _color_texels );
  updateRays();
  return true;
}

//------------------------------------------------------------------------------

bool
RangeCamera::inRange( NodePath & node )
{
  return true;
}

//------------------------------------------------------------------------------

void RangeCamera::setActive( bool active )
{
  _cameraNode->set_active( active );
}

//------------------------------------------------------------------------------
// Private methods
//------------------------------------------------------------------------------

void
RangeCamera::setupCamera()
{
  _depthMap.set_format( Texture::F_depth_component );
  _depthMap.set_component_type( Texture::T_unsigned_short );

  GraphicsOutput * window = getWindow( 0 );

  _depthBuffer = window->make_texture_buffer( "depthmap", _width, _height,
    &_depthMap, true );
  if ( _colorInfo )
    _colorBuffer = window->make_texture_buffer( "colormap", _width, _height,
      &_colorMap, true );

  _cameraNode = new Camera( "cam" );
  _cameraNode->set_camera_mask( BitMask32( 1 ) );
  _cameraNode->set_scene( getGSG()->get_scene()->get_scene_root() );

  PT(PerspectiveLens) lens = new PerspectiveLens();
  lens->set_near_far( _minRange, _maxRange );
  lens->set_fov( _horizontalFOV );
  lens->set_aspect_ratio( _horizontalFOV / _verticalFOV );
  _cameraNode->set_lens( lens );

  _camera = attach_new_node( _cameraNode );

  _camera.set_hpr( -90, 0, 180 );
  _camera.set_light_off( true );
  _camera.set_material_off( true );
  _camera.set_color_off( true );

  PT(DisplayRegion) drd = _depthBuffer->make_display_region();
  drd->set_sort( 0 );
  drd->set_camera( _camera );

  if ( _colorInfo ) {
    PT(DisplayRegion) drc = _colorBuffer->make_display_region();
    drc->set_sort( 0 );
    drc->set_camera( _camera );
  }
}

//------------------------------------------------------------------------------

void
RangeCamera::setupRays()
{
  double hFov = _horizontalFOV * M_PI / 180;
  double vFov = _verticalFOV * M_PI / 180;
  double deltaHAngle = -hFov;
  double hAngle = 0;
  if ( _horizontalRays  > 1 ) {
    deltaHAngle = -hFov / ( _horizontalRays - 1 );
    hAngle = hFov / 2;
  }
  double deltaVAngle = -vFov;
  if ( _verticalRays > 1 )
    deltaVAngle = -vFov / ( _verticalRays - 1 );
  double hFocal = ( _width / 2.0 - 0.5 ) / tan( hFov / 2.0 );
  double vFocal = ( _height / 2.0 - 0.5 ) / tan( vFov / 2.0 );
  int index = _rayCount;
  while ( hAngle + hFov / 2.0 > -2e-10 ) {
    double hDist = hFocal * tan( hAngle );
    int column = static_cast<int>( _width / 2.0 + hDist );
    double vAngle = 0;
    if ( _verticalRays > 1 )
      vAngle = vFov / 2.0;
    while ( vAngle + vFov / 2.0 > -2e-10 ) {
      double vDist = vFocal * tan( vAngle );
      int row = static_cast<int>( _height / 2.0 + vDist );
      RayInfo ri;
      ri.row    = row;
      ri.column = column;
      ri.hAngle = hAngle;
      ri.vAngle = vAngle;
      ri.hTan   = tan( hAngle );
      ri.vTan   = tan( vAngle );
      _rayInfo[--index] = ri;
      vAngle += deltaVAngle;
    }
    hAngle += deltaHAngle;
  }
}

//------------------------------------------------------------------------------

void
RangeCamera::updateRays()
{
  for ( int i = 0; i < _rayCount; i++ ) {
    RayInfo & ri = _rayInfo[i];
    Ray & ray    = _rays[i];
    double depth = _depth_texels.get_gray( ri.column, ri.row );
    ray.x = _maxRange * _minRange /
      ( _maxRange - depth * ( _maxRange - _minRange ) );
    ray.column = ri.column;
    ray.row    = ri.row;
    if ( ray.x < 0 )
      ray.x = 0;
    ray.y = ray.x * ri.hTan;
    ray.z = ray.x * ri.vTan;
    ray.radius = sqrt( ray.x * ray.x + ray.y * ray.y + ray.z * ray.z );
    ray.hAngle = ri.hAngle;
    ray.vAngle = ri.vAngle;

    if ( _colorInfo ) {
      ray.red   = _color_texels.get_red( ri.column, ri.row );
      ray.green = _color_texels.get_green( ri.column, ri.row );
      ray.blue  = _color_texels.get_blue( ri.column, ri.row );
    }
  }
}
