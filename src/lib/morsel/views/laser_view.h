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
    bool showPoints = true,
    bool showLines = false,
    bool showColors = false,
    bool showLabels = false
  );
public:
  virtual ~LaserView();
PUBLISHED:
  bool update( double time );
protected:
  std::string   _name;
  RangeSensor & _sensor;
  Colorf        _color;
  bool          _showPoints;
  bool          _showLines;
  bool          _showColors;
  bool          _showLabels;
  PointerTo<GeomNode> _node;
  PointerTo<GeomVertexData> _geomData;

  double labelToHue( size_t label );
  Colorf hsvToRgb( double hue, double sat, double val );
  void setupRendering();
  void updateRays();
};

#endif /*LASER_VIEW_H*/
