#ifndef LASER_VIEWER_H
#define LASER_VIEWER_H

#include "morsel/morsel.h"
#include "morsel/sensors/range_sensor.h"

#include <nodePath.h>

class LaserViewer : public NodePath
{
public:
  LaserViewer(
    std::string name,
    RangeSensor & laser,
    float r,
    float g,
    float b,
    float a,
    bool points = false,
    bool colorInfo = false
  );
  virtual ~LaserViewer();
  bool update( double time );
private:
  std::string         _name;
  RangeSensor &       _laser;
  Colorf              _color;
  bool                _points;
  bool                _colorInfo;
  PointerTo<GeomNode>        _node;
  PointerTo<GeomVertexData>  _geomData;
  void setupRendering();
  void updateRays();
};

#endif /*LASER_VIEWER_H*/
