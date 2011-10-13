#ifndef LASER_VIEW_H
#define LASER_VIEW_H

#include "morsel/morsel.h"

#include <nodePath.h>

class RangeSensor;

class LaserView : public NodePath
{
PUBLISHED:
  LaserView(
    std::string name,
    NodePath & sensor,
    float r,
    float g,
    float b,
    float a,
    bool points = true,
    bool lines = false,
    bool colorInfo = false
  );
public:
  virtual ~LaserView();
PUBLISHED:
  bool update( double time );
protected:
  std::string                _name;
  RangeSensor &              _sensor;
  Colorf                     _color;
  bool                       _points;
  bool                       _lines;
  bool                       _colorInfo;
  PointerTo<GeomNode>        _node;
  PointerTo<GeomVertexData>  _geomData;
  void setupRendering();
  void updateRays();
};

#endif /*LASER_VIEW_H*/
