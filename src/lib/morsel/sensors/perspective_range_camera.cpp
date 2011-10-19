#include "perspective_range_camera.h"

#include <perspectiveLens.h>
#include <graphicsEngine.h>
#include <cmath>
#include <string>

using namespace std;

//------------------------------------------------------------------------------

PerspectiveRangeCamera::PerspectiveRangeCamera(
  string name,
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
  bool acquireColor,
  string acquireLabel )
  : RangeCamera( name, horizontalAngle, verticalAngle, horizontalFOV,
                 verticalFOV, horizontalRays, verticalRays, minRange, maxRange,
                 horizontalResolution, verticalResolution, acquireColor,
                 acquireLabel )
{
  setupLens();
  setupRays();
}

//------------------------------------------------------------------------------

PerspectiveRangeCamera::~PerspectiveRangeCamera()
{
}

//------------------------------------------------------------------------------
// Protected methods
//------------------------------------------------------------------------------

void
PerspectiveRangeCamera::setupLens()
{
  PT(Lens) lens = new PerspectiveLens();
  lens->set_near_far( _minRange, _maxRange );
  lens->set_fov( _horizontalFOV * 180.0 / M_PI, _verticalFOV * 180.0 / M_PI );

  setupCamera( lens );

  set_hpr( _horizontalAngle * 180.0 / M_PI - 90.0,
    _verticalAngle * 180.0 / M_PI, 0.0 );
}

//------------------------------------------------------------------------------

void
PerspectiveRangeCamera::setupRays()
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
      LPoint3f point, dist;
      point[0] = _maxRange * tan( hAngle );
      point[1] = _maxRange;
      point[2] = _maxRange * tan( vAngle );
      _cameraNode->get_lens()->project( point, dist );

      double column = 0.5 * _width * ( 1.0 + dist[0] );
      double row = 0.5 * _height * ( 1.0 - dist[1] );

      RayInfo ri;
      ri.row    = row;
      ri.column = column;
      ri.hAngle = hAngle;
      ri.vAngle = vAngle;
      ri.hTan   = tan( ri.hAngle );
      ri.vTan   = tan( ri.vAngle );

      _rayInfo[index] = ri;
      ++index;

      vAngle += deltaVAngle;
    }
    hAngle += deltaHAngle;
  }
}
