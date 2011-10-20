#include "range_sensor.h"
#include "perspective_range_camera.h"
#include "spherical_range_camera.h"

#include <lpoint3.h>
#include <lvecBase3.h>
#include <numeric>
#include <sstream>

using namespace std;

//------------------------------------------------------------------------------

RangeSensor::RangeSensor(
  string name,
  double horizontalMinAngle,
  double horizontalMaxAngle,
  double verticalMinAngle,
  double verticalMaxAngle,
  double horizontalResolution,
  double verticalResolution,
  double minRange,
  double maxRange,
  double cameraMaxHorizontalFOV,
  double cameraMaxVerticalFOV,
  int cameraHorizontalResolution,
  int cameraVerticalResolution,
  bool spherical,
  bool acquireColor,
  string acquireLabel )
  : NodePath( name ),
    _name( name ),
    _horizontalMinAngle( horizontalMinAngle ),
    _horizontalMaxAngle( horizontalMaxAngle ),
    _verticalMinAngle( verticalMinAngle ),
    _verticalMaxAngle( verticalMaxAngle ),
    _horizontalResolution( horizontalResolution ),
    _verticalResolution( verticalResolution ),
    _minRange( minRange ),
    _maxRange( maxRange ),
    _horizontalFOV( horizontalMaxAngle-horizontalMinAngle ),
    _verticalFOV( verticalMaxAngle-verticalMinAngle ),
    _horizontalRays( floor( _horizontalFOV / horizontalResolution ) ),
    _verticalRays( floor( _verticalFOV / verticalResolution ) ),
    _rayCount( _horizontalRays * _verticalRays ),
    _rays( new RangeSensor::Ray[_rayCount] ),
    _cameraMaxHorizontalFOV( cameraMaxHorizontalFOV ),
    _cameraMaxVerticalFOV( cameraMaxVerticalFOV ),
    _cameraHorizontalResolution( cameraHorizontalResolution ),
    _cameraVerticalResolution( cameraVerticalResolution ),
    _spherical( spherical ),
    _acquireColor( acquireColor ),
    _acquireLabel( acquireLabel )
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

const string &
RangeSensor::name() {
  return _name;
}

//------------------------------------------------------------------------------

int
RangeSensor::cameraCount() {
  return _cameras.size();
}

//------------------------------------------------------------------------------

RangeCamera &
RangeSensor::camera( int index ) {
  return *_cameras[index];
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
      if ( _acquireColor ) {
        ray2._red   = ray1.red;
        ray2._green = ray1.green;
        ray2._blue  = ray1.blue;
      } else {
        ray2._red   = 0;
        ray2._green = 0;
        ray2._blue  = 0;
      }
      if ( !_acquireLabel.empty() )
        ray2._label = ray1.label;
      else
        ray2._label = 0;
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

void
RangeSensor::showFrustums()
{
  for ( int i = 0; i < _cameras.size(); ++i )
    _cameras[i]->showFrustum();
}

//------------------------------------------------------------------------------

void
RangeSensor::hideFrustums()
{
  for ( int i = 0; i < _cameras.size(); ++i )
    _cameras[i]->hideFrustum();
}

//------------------------------------------------------------------------------
// Private methods
//------------------------------------------------------------------------------

void
RangeSensor::computeParameters(
  double minAngle,
  double maxAngle,
  int rayCount,
  double cameraMaxFOV,
  deque<double> & fovs,
  deque<double> & angles,
  deque<int> & rayCounts
)
{
  fovs.clear();
  angles.clear();
  rayCounts.clear();
  
  double fov = maxAngle - minAngle;
  double rayFov = fov / rayCount;
  int camCount = ceil( fov / cameraMaxFOV );
  double camFOV = fov / camCount;

  for ( int i = rayCount; i > 0; ) {
    int camRayCount = fmin( round( camFOV / rayFov ), i );
    rayCounts.push_back( camRayCount );
    fovs.push_back( camRayCount * rayFov );
    i -= camRayCount;
  }

  double angle = minAngle;
  for ( int i = 0; i < rayCounts.size(); i++ ) {
    angles.push_back( angle + 0.5 * fovs[i] );
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
  computeParameters( _horizontalMinAngle, _horizontalMaxAngle, _horizontalRays,
    _cameraMaxHorizontalFOV, hFovs, hAngles, hRayCounts );

  deque<double> vFovs;
  deque<double> vAngles;
  deque<int> vRayCounts;
  computeParameters( _verticalMinAngle, _verticalMaxAngle, _verticalRays,
    _cameraMaxVerticalFOV, vFovs, vAngles, vRayCounts );

  for ( int i = 0; i < hFovs.size(); i++ ) {
    for ( int j = 0; j < vFovs.size(); j++ ) {
      stringstream s;
      s << get_name() << ":" << i << "," << j;

      RangeCamera * c;
      if ( _spherical )
        c = new SphericalRangeCamera(
          s.str(),
          hAngles[i],
          vAngles[j],
          hFovs[i],
          vFovs[j],
          hRayCounts[i],
          vRayCounts[j],
          _minRange,
          _maxRange,
          _cameraHorizontalResolution,
          _cameraVerticalResolution,
          _acquireColor,
          _acquireLabel
        );
      else
        c = new PerspectiveRangeCamera(
          s.str(),
          hAngles[i],
          vAngles[j],
          hFovs[i],
          vFovs[j],
          hRayCounts[i],
          vRayCounts[j],
          _minRange,
          _maxRange,
          _cameraHorizontalResolution,
          _cameraVerticalResolution,
          _acquireColor,
          _acquireLabel
        );        
      c->reparent_to( *this );
      _cameras.push_back( c );
    }
  }
}
