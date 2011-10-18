#include "image_sensor.h"

#include <perspectiveLens.h>
#include <numeric>
#include <sstream>

using namespace std;

//------------------------------------------------------------------------------

ImageSensor::ImageSensor(
  string name,
  int horizontalResolution,
  int verticalResolution,
  double minRange,
  double maxRange,
  double filmWidth,
  double filmHeight,
  double focalLength )
  : NodePath( name ),
    _name( name ),
    _horizontalResolution( horizontalResolution ),
    _verticalResolution( verticalResolution ),
    _minRange( minRange ),
    _maxRange( maxRange ),
    _filmWidth( filmWidth ),
    _filmHeight( filmHeight ),
    _focalLength( focalLength )
{
  setupCamera();
}

//------------------------------------------------------------------------------

ImageSensor::~ImageSensor()
{
}

//------------------------------------------------------------------------------

const string &
ImageSensor::name() {
  return _name;
}

//------------------------------------------------------------------------------

int
ImageSensor::horizontalResolution()
{
  return _horizontalResolution;
}

//------------------------------------------------------------------------------

int
ImageSensor::verticalResolution()
{
  return _verticalResolution;
}

//------------------------------------------------------------------------------

PointerTo<Texture>
ImageSensor::colorMap() {
  return & _colorMap;
}

//------------------------------------------------------------------------------

bool
ImageSensor::update( double time )
{
  _colorMap.store( _colorTexels );
  return true;
}

//------------------------------------------------------------------------------

void
ImageSensor::showFrustum()
{
  _cameraNode->show_frustum();
}

//------------------------------------------------------------------------------

void
ImageSensor::hideFrustum()
{
  _cameraNode->hide_frustum();
}

//------------------------------------------------------------------------------
// Protected methods
//------------------------------------------------------------------------------

void
ImageSensor::setupCamera()
{
  GraphicsOutput * window = getWindow( 0 );
  _colorBuffer = window->make_texture_buffer( "colormap", _horizontalResolution,
    _verticalResolution, &_colorMap, true );

  PT(Lens) lens = new PerspectiveLens();
  lens->set_near_far( _minRange, _maxRange );
  lens->set_view_vector( 1.0, 0.0, 0.0, 0.0, 0.0, 1.0 );
  lens->set_film_size( _filmWidth, _filmHeight );
  lens->set_focal_length( _focalLength );

  _cameraNode = new Camera( "cam" );
  _cameraNode->set_camera_mask( BitMask32( 1 ) );
  _cameraNode->set_scene( getGSG()->get_scene()->get_scene_root() );
  _camera = attach_new_node( _cameraNode );
  _cameraNode->set_lens( lens );

  PT(DisplayRegion) drc = _colorBuffer->make_display_region();
  drc->set_sort( 0 );
  drc->set_camera( _camera );
}
