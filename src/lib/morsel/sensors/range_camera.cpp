#include "range_camera.h"

#include <cmath>
#include <string>

using namespace std;

//------------------------------------------------------------------------------

RangeCamera::RangeCamera(
  std::string name,
  double horizontalAngle,
  double verticalAngle,
  double horizontalFOV,
  double verticalFOV,
  int horizontalRays,
  int verticalRays,
  double minRange,
  double maxRange,
  int horizontalResolution,
  int verticalResolution,
  bool colorInfo )
  : NodePath( name ),
    _name( name ),
    _horizontalAngle( horizontalAngle ),
    _verticalAngle( verticalAngle ),
    _horizontalFOV( horizontalFOV ),
    _verticalFOV( verticalFOV ),
    _horizontalRays( horizontalRays ),
    _verticalRays( verticalRays ),
    _minRange( minRange ),
    _maxRange( maxRange ),
    _width( horizontalResolution ),
    _height( verticalResolution ),
    _rayCount( horizontalRays * verticalRays ),
    _rayInfo( new RayInfo[_rayCount] ),
    _rays( new Ray[_rayCount] ),
    _colorInfo( colorInfo )
{
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

void
RangeCamera::setActive( bool active )
{
  _cameraNode->set_active( active );
}

//------------------------------------------------------------------------------

void
RangeCamera::showFrustum()
{
  _cameraNode->show_frustum();
}

//------------------------------------------------------------------------------

void
RangeCamera::hideFrustum()
{
  _cameraNode->hide_frustum();
}

//------------------------------------------------------------------------------
// Protected methods
//------------------------------------------------------------------------------

void
RangeCamera::setupCamera( PT(Lens) lens )
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
  _cameraNode->set_lens( lens );

  _camera = attach_new_node( _cameraNode );
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

void
RangeCamera::updateRays()
{
  for ( int i = 0; i < _rayCount; i++ ) {
    RayInfo & ri = _rayInfo[i];
    Ray & ray = _rays[i];

    double depth = 0.0;
    if ( ( ri.column >= 0 ) && ( ri.column < _depth_texels.get_x_size() )  &&
         ( ri.row >= 0 ) && ( ri.row < _depth_texels.get_y_size() ) )
      depth = _depth_texels.get_gray( ri.column, ri.row );

    ray.y = _maxRange * _minRange /
      ( _maxRange - depth * ( _maxRange - _minRange ) );
    if ( ray.y < _minRange )
      ray.y = 0.0;
    ray.x = ray.y * ri.hTan;
    ray.z = ray.y * ri.vTan;
    ray.radius = sqrt( ray.x * ray.x + ray.y * ray.y + ray.z * ray.z );
    ray.hAngle = ri.hAngle;
    ray.vAngle = ri.vAngle;
    ray.column = ri.column;
    ray.row    = ri.row;
    
    if ( _colorInfo ) {
      ray.red   = _color_texels.get_red( ri.column, ri.row );
      ray.green = _color_texels.get_green( ri.column, ri.row );
      ray.blue  = _color_texels.get_blue( ri.column, ri.row );
    }
  }
}
