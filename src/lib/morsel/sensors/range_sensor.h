#ifndef RANGE_SENSOR_H
#define RANGE_SENSOR_H

#include "morsel/morsel.h"
#include "morsel/sensors/range_camera.h"

#include <nodePath.h>

#include <string>
#include <deque>
#include <cstring>
#include <cmath>

class RangeSensor : public NodePath
{
public:
  class Ray {
  public:
    double column() { return _column; }
    double row() { return _row; }
    int index() { return _index; }
    double hAngle() { return _hAngle; }
    double vAngle() { return _vAngle; }
    double x() { return _x;}
    double y() { return _y;}
    double z() { return _z;}
    double radius() { return _radius;}
    double red() { return _red;}
    double green() { return _green;}
    double blue() { return _blue;}
    double _column;
    double _row;
    int _index;
    double _hAngle;
    double _vAngle;
    double _x;
    double _y;
    double _z;
    double _radius;
    double _red;
    double _green;
    double _blue;
  };
PUBLISHED:
  RangeSensor(
    std::string name,
    double horizontalMinAngle,
    double horizontalMaxAngle,
    double verticalMinAngle,
    double verticalMaxAngle,
    double horizontalResolution,
    double verticalResolution,
    double minRange,
    double maxRange,
    double cameraMaxHorizontalFOV = 60 * M_PI / 180.0,
    double cameraMaxVerticalFOV = 60 * M_PI / 180.0,
    int cameraHorizontalResolution = 128,
    int cameraVerticalResolution = 128,
    bool sphericalLens = false,
    bool colorInfo = false
  );
public:
  virtual ~RangeSensor();
PUBLISHED:
  const std::string & name();
  int rayCount();
  Ray & ray( int index );
  bool update( double time );
  double minRange();
  double maxRange();
  bool inRange( NodePath & node );
  double hFov();
  double vFov();
  int hRays();
  int vRays();
  double rayLength( int index );
  void showFrustums();
  void hideFrustums();
protected:
  std::string _name;
  double      _horizontalMinAngle;
  double      _horizontalMaxAngle;
  double      _verticalMinAngle;
  double      _verticalMaxAngle;
  double      _horizontalResolution;
  double      _verticalResolution;
  double      _minRange;
  double      _maxRange;
  double      _horizontalFOV;
  double      _verticalFOV;
  int         _horizontalRays;
  int         _verticalRays;
  int         _rayCount;
  double      _cameraMaxHorizontalFOV;
  double      _cameraMaxVerticalFOV;
  int         _cameraHorizontalResolution;
  int         _cameraVerticalResolution;
  bool        _spherical;
  bool        _colorInfo;

  Ray     *   _rays;
  std::vector<RangeCamera*> _cameras;

  void computeParameters(
    double minAngle,
    double maxAngle,
    int rayCount,
    double cameraMaxFOV,
    std::deque<double> & fovs,
    std::deque<double> & angles,
    std::deque<int> & rayCounts
  );
  void setupCameras();
};

#endif /*RANGE_SENSOR_H*/
