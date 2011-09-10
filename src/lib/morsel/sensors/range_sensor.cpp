#include "range_sensor.h"

#include <lpoint3.h>
#include <lvecBase3.h>
#include <numeric>
#include <cmath>
#include <sstream>

using namespace std;

//------------------------------------------------------------------------------

RangeSensor::RangeSensor(
  std::string name,
  double horizontalFOV,
  double verticalFOV,
  int horizontalRays,
  int verticalRays,
  double minRange,
  double maxRange,
  double cameraMaxHorizontalFOV,
  double cameraMaxVerticalFOV,
  bool colorInfo )
  : NodePath( name ),
    _name( name ),
    _horizontalFOV( horizontalFOV ),
    _verticalFOV( verticalFOV ),
    _horizontalRays( horizontalRays ),
    _verticalRays( verticalRays ),
    _minRange( minRange ),
    _maxRange( maxRange ),
    _rayCount( horizontalRays * verticalRays ),
    _rays( new RangeSensor::Ray[_rayCount] ),
    _cameraMaxHorizontalFOV( cameraMaxHorizontalFOV ),
    _cameraMaxVerticalFOV( cameraMaxVerticalFOV ),
    _colorInfo( colorInfo )
{
  setupCameras();
  getEngine()->render_frame();
}

//------------------------------------------------------------------------------

RangeSensor::~RangeSensor()
{
  delete [] _rays;
  for ( int i = 0; i < _cameras.size(); i++ )
    delete _cameras[i];
}

//------------------------------------------------------------------------------

int
RangeSensor::rayCount()
{
  return _rayCount;
}

//------------------------------------------------------------------------------

RangeSensor::Ray &
RangeSensor::ray( int index ) {
  return _rays[index];
}

//------------------------------------------------------------------------------

bool
RangeSensor::update( double time )
{
  for ( int ci = 0; ci < _cameras.size(); ci++ )
    RangeCamera * c = _cameras[ci];
  int rayIndex = 0;
  for ( int ci = 0; ci < _cameras.size(); ci++ ) {
    RangeCamera * c = _cameras[ci];
    c->update( time );
    for ( int ri = 0; ri < c->rayCount(); ri++ ) {
      ::Ray & ray1 = c->ray( ri );
      LPoint3f p = get_relative_point( *c,
        LVecBase3f( ray1.x, ray1.y, ray1.z ) );
      double r = ray1.radius;
      if ( r >= _maxRange )
        r = -1;
      if ( r <= _minRange )
        r = -2;
      RangeSensor::Ray & ray2 = _rays[rayIndex++];

      ray2._row    = ray1.row;
      ray2._column = ray1.column;
      ray2._index  = rayIndex;
      ray2._hAngle = atan2( p[1], p[0] );
      ray2._vAngle = atan2( p[2], sqrt( p[0] * p[0] + p[1] * p[1] ) );
      ray2._x      = p[0];
      ray2._y      = p[1];
      ray2._z      = p[2];
      ray2._radius = r;
      if ( _colorInfo ) {
        ray2._red   = ray1.red;
        ray2._green = ray1.green;
        ray2._blue  = ray1.blue;
      } else {
        ray2._red   = 0;
        ray2._green = 0;
        ray2._blue  = 0;
      }
    }
  }
  return true;
}

//------------------------------------------------------------------------------

double
RangeSensor::minRange()
{
  return _minRange;
}

//------------------------------------------------------------------------------

double
RangeSensor::maxRange()
{
  return _maxRange;
}

//------------------------------------------------------------------------------

bool
RangeSensor::inRange( NodePath & node )
{
  return true;
}

//------------------------------------------------------------------------------

double
RangeSensor::hFov()
{
  return _horizontalFOV;
}

//------------------------------------------------------------------------------

double
RangeSensor::vFov()
{
  return _verticalFOV;
}

//------------------------------------------------------------------------------

int
RangeSensor::hRays()
{
  return _horizontalRays;
}

//------------------------------------------------------------------------------

int
RangeSensor::vRays()
{
  return _verticalRays;
}

//------------------------------------------------------------------------------

double
RangeSensor::rayLength( int index )
{
  if(index >= _rayCount) {
    fprintf(stderr, "morsel->range_sensor->rayLength(...) "
      "index out of range: %d >= %d. Aborting...\n", index, _rayCount);
    exit(1);
  }
  return _rays[index]._radius;
}




//------------------------------------------------------------------------------
// Private methods
//------------------------------------------------------------------------------

void
RangeSensor::computeParameters(
  double fov,
  double cameraMaxFOV,
  int rayCount,
  deque<double> & fovs,
  deque<double> & angles,
  deque<int> & rayCounts
)
{
  fovs.clear();
  angles.clear();
  rayCounts.clear();
  double rayFov   = fov / rayCount;

  int camRayCount = min( static_cast<int>( cameraMaxFOV / rayFov ), rayCount );
  if ( (rayCount - camRayCount) % 2 )
    camRayCount -= 1;
  rayCounts.push_front( camRayCount );
  fovs.push_front( camRayCount * rayFov );

  for ( int i = (rayCount - camRayCount ) / 2; i > 0; ) {
    camRayCount = min( static_cast<int>( cameraMaxFOV / rayFov ), i );
    rayCounts.push_front( camRayCount );
    fovs.push_front( camRayCount * rayFov );
    rayCounts.push_back( camRayCount );
    fovs.push_back( camRayCount * rayFov );
    i -= camRayCount;
  }

  double angle = -fov / 2;
  for ( int i = 0; i < rayCounts.size(); i++ ) {
    angles.push_back( angle + fovs[i] / 2 );
    angle += fovs[i];
  }
}

//------------------------------------------------------------------------------

void
RangeSensor::setupCameras()
{
  deque<double> hFovs;
  deque<double> hAngles;
  deque<int> hRayCounts;
  computeParameters( _horizontalFOV, _cameraMaxHorizontalFOV, _horizontalRays,
    hFovs, hAngles, hRayCounts );

  deque<double> vFovs;
  deque<double> vAngles;
  deque<int> vRayCounts;
  computeParameters( _verticalFOV, _cameraMaxVerticalFOV, _verticalRays,
    vFovs, vAngles, vRayCounts );

  for ( int i = 0; i < hFovs.size(); i++ ) {
    for ( int j = 0; j < vFovs.size(); j++ ) {
      stringstream s;
      s << get_name() << ":" << i << "," << j;
      RangeCamera * c = new RangeCamera(
        s.str(),
        hFovs[i],
        vFovs[j],
        hRayCounts[i],
        vRayCounts[j],
        _minRange,
        _maxRange,
        _colorInfo
      );
      c->reparent_to( *this );
      c->set_hpr( hAngles[i], vAngles[j], 0 );
      _cameras.push_back( c );
    }
  }
}
