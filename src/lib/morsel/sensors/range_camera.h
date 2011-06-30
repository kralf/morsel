#ifndef RANGE_CAMERA_H
#define RANGE_CAMERA_H

#include "morsel/morsel.h"

#include <nodePath.h>
#include <pnmImage.h>
#include <texture.h>
#include <graphicsOutput.h>

#include <string>

struct Ray {
  double x;
  double y;
  double z;
  double radius;
  int column;
  int row;
  double hAngle;
  double vAngle;
  double red;
  double green;
  double blue;
};

class RangeCamera : public NodePath
{
public:
  struct RayInfo;

  RangeCamera(
    std::string name,
    double horizontalFOV,
    double verticalFOV,
    int horizontalRays,
    int verticalRays,
    double minRange,
    double maxRange,
    bool colorInfo = false
  );
  virtual ~RangeCamera();
  int rayCount();
  Ray & ray( int index );
  bool update( double time );
  bool inRange( NodePath & node );
  void setActive( bool active );
private:
  std::string _name;
  double      _horizontalFOV;
  double      _verticalFOV;
  int         _horizontalRays;
  int         _verticalRays;
  double      _minRange;
  double      _maxRange;
  bool        _colorInfo;

  int         _width;
  int         _height;
  int         _rayCount;

  RayInfo *   _rayInfo;
  Ray     *   _rays;

  PointerTo<GraphicsOutput> _depthBuffer;
  PointerTo<GraphicsOutput> _colorBuffer;
  PNMImage    _depth_texels;
  PNMImage    _color_texels;
  Texture     _depthMap;
  Texture     _colorMap;
  PT(Camera)  _cameraNode;
  NodePath    _camera;

  void setupCamera();
  void setupRays();
  void updateRays();
};


#endif /*RANGE_CAMERA_H*/
