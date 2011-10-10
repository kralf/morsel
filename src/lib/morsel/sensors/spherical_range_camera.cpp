#include "spherical_range_camera.h"

#include <perspectiveLens.h>
#include <graphicsEngine.h>
#include <cmath>
#include <string>

using namespace std;

//------------------------------------------------------------------------------

SphericalRangeCamera::SphericalRangeCamera(
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
  : RangeCamera( name, horizontalAngle, verticalAngle, horizontalFOV,
                 verticalFOV, horizontalRays, verticalRays, minRange, maxRange,
                 horizontalResolution, verticalResolution, colorInfo )
{
  setupLens();
  setupRays();
}

//------------------------------------------------------------------------------

SphericalRangeCamera::~SphericalRangeCamera()
{
}

//------------------------------------------------------------------------------
// Protected methods
//------------------------------------------------------------------------------

void
SphericalRangeCamera::setupLens()
{
  PT(Lens) lens = new PerspectiveLens();
  lens->set_near_far( _minRange, _maxRange );
  setupCamera( lens );
  
  double minHAngle = _horizontalAngle - 0.5 * _horizontalFOV;
  double maxHAngle = _horizontalAngle + 0.5 * _horizontalFOV;
  double minVAngle = _verticalAngle - 0.5 * _verticalFOV;
  double maxVAngle = _verticalAngle + 0.5 * _verticalFOV;

  LPoint3f ll(
    cos( maxHAngle ) * cos( minVAngle ),
    sin( maxHAngle ) * cos( minVAngle ),
    sin( minVAngle ) );
  LPoint3f lr(
    cos( minHAngle ) * cos( minVAngle ),
    sin( minHAngle ) * cos( minVAngle ),
    sin( minVAngle ) );
  LPoint3f ul(
    cos( maxHAngle ) * cos( maxVAngle ),
    sin( maxHAngle ) * cos( maxVAngle ),
    sin( maxVAngle ) );
  LPoint3f ur(
    cos( minHAngle ) * cos( maxVAngle ),
    sin( minHAngle ) * cos( maxVAngle ),
    sin( maxVAngle ) );

  lens->set_frustum_from_corners(
    _camera.get_relative_point( get_parent(), ul ),
    _camera.get_relative_point( get_parent(), ur ),
    _camera.get_relative_point( get_parent(), ll ),
    _camera.get_relative_point( get_parent(), lr ),
    Lens::FC_aspect_ratio | Lens::FC_off_axis );
  set_hpr( lens->get_view_hpr() );
  lens->set_view_hpr( 0.0, 0.0, 0.0 );
}

//------------------------------------------------------------------------------

void
SphericalRangeCamera::setupRays()
{
  double deltaHAngle = _horizontalFOV;
  double hAngle = 0.0;
  if ( _horizontalRays  > 1 ) {
    deltaHAngle = _horizontalFOV / _horizontalRays;
    hAngle = 0.5 * ( -_horizontalFOV + deltaHAngle ) ;
  }

  double deltaVAngle = _verticalFOV;
  if ( _verticalRays > 1 )
    deltaVAngle = _verticalFOV / _verticalRays;

  int index = 0;
  while ( hAngle < 0.5 * _horizontalFOV ) {
    double vAngle = 0.0;
    if ( _verticalRays > 1 )
      vAngle = 0.5 * ( -_verticalFOV + deltaVAngle );

    while ( vAngle < 0.5 * _verticalFOV ) {
      LPoint3f point = _camera.get_relative_point( get_parent(), LPoint3f(
        cos( _horizontalAngle + hAngle ) * cos( _verticalAngle + vAngle ),
        sin( _horizontalAngle + hAngle ) * cos( _verticalAngle + vAngle ),
        sin( _verticalAngle + vAngle ) ) );
      LPoint2f dist;
      _cameraNode->get_lens()->project( point, dist );

      double column = 0.5 * _width * ( 1.0 + dist[0] );
      double row = 0.5 * _height * ( 1.0 - dist[1] );
      
      RayInfo ri;
      ri.row    = row;
      ri.column = column;
      ri.hAngle = atan2( point[0], point[1] );
      ri.vAngle = atan2( point[2], point[1] );
      ri.hTan   = tan( ri.hAngle );
      ri.vTan   = tan( ri.vAngle );

      _rayInfo[index] = ri;
      ++index;

      vAngle += deltaVAngle;
    }
    hAngle += deltaHAngle;
  }
}
