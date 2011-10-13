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
  double column;
  double row;
  double hAngle;
  double vAngle;
  double red;
  double green;
  double blue;
};

class RangeCamera : public NodePath
{
public:
  struct RayInfo {
    double hAngle;
    double vAngle;
    double row;
    double column;
    double hTan;
    double vTan;
  };

  RangeCamera(
    std::string name,
    double horizontalAngle,
    double verticalAngle,
    double horizontalFOV,
    double verticalFOV,
    int horizontalRays,
    int verticalRays,
    double minRange,
    double maxRange,
    int horizontalResolution = 128,
    int verticalResolution = 128,
    bool colorInfo = false
  );
  virtual ~RangeCamera();

  int rayCount();
  Ray & ray( int index );
  double depth( int column, int row );
  bool update( double time );
  bool inRange( NodePath & node );
  void setActive( bool active );
  void showFrustum();
  void hideFrustum();
protected:
  std::string _name;
  double      _horizontalAngle;
  double      _verticalAngle;
  double      _horizontalFOV;
  double      _verticalFOV;
  int         _horizontalRays;
  int         _verticalRays;
  double      _minRange;
  double      _maxRange;
  int         _resolution;
  bool        _colorInfo;

  int         _width;
  int         _height;
  int         _rayCount;

  RayInfo *   _rayInfo;
  Ray     *   _rays;

  PointerTo<GraphicsOutput> _depthBuffer;
  PointerTo<GraphicsOutput> _colorBuffer;
  PNMImage    _depthTexels;
  PNMImage    _colorTexels;
  Texture     _depthMap;
  Texture     _colorMap;
  PT(Camera)  _cameraNode;
  NodePath    _camera;

  void setupCamera( PT(Lens) lens );
  void updateRays();

  virtual void setupLens() = 0;
};


#endif /*RANGE_CAMERA_H*/
