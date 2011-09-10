#ifndef RANGE_SENSOR_H
#define RANGE_SENSOR_H

#include "morsel/morsel.h"
#include "morsel/sensors/range_camera.h"

#include <nodePath.h>

#include <string>
#include <deque>
#include <cstring>

class RangeSensor : public NodePath
{
public:
  class Ray {
  public:
    int column() { return _column; }
    int row() { return _row; }
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
    int _column;
    int _row;
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

  RangeSensor(
    std::string name,
    double horizontalFOV,
    double verticalFOV,
    int horizontalRays,
    int verticalRays,
    double minRange,
    double maxRange,
    double cameraMaxHorizontalFOV = 60,
    double cameraMaxVerticalFOV = 60,
    bool colorInfo = false
  );
  virtual ~RangeSensor();
  
  //accessors
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
private:
  std::string _name;
  double      _horizontalFOV;
  double      _verticalFOV;
  int         _horizontalRays;
  int         _verticalRays;
  double      _minRange;
  double      _maxRange;
  int         _rayCount;
  double      _cameraMaxHorizontalFOV;
  double      _cameraMaxVerticalFOV;
  bool        _colorInfo;

  Ray     *   _rays;
  std::vector<RangeCamera*> _cameras;

  void computeParameters(
    double fov,
    double cameraMaxFOV,
    int rayCount,
    std::deque<double> & fovs,
    std::deque<double> & angles,
    std::deque<int> & rayCounts
  );
  void setupCameras();
};

#endif /*RANGE_SENSOR_H*/
