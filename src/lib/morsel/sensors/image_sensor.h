#ifndef IMAGE_SENSOR_H
#define IMAGE_SENSOR_H

#include "morsel/morsel.h"

#include <nodePath.h>
#include <pnmImage.h>
#include <texture.h>
#include <graphicsOutput.h>

#include <string>

class ImageSensor : public NodePath
{
PUBLISHED:
  ImageSensor(
    std::string name,
    int horizontalResolution,
    int verticalResolution,
    double minRange,
    double maxRange,
    double filmWidth,
    double filmHeight,
    double focalLength
  );
public:
  virtual ~ImageSensor();
PUBLISHED:
  const std::string & name();
  int horizontalResolution();
  int verticalResolution();
  PointerTo<Texture> colorMap();
  bool update( double time );
  void showFrustum();
  void hideFrustum();
protected:
  std::string _name;
  int         _horizontalResolution;
  int         _verticalResolution;
  double      _minRange;
  double      _maxRange;
  double      _filmWidth;
  double      _filmHeight;
  double      _focalLength;

  PointerTo<GraphicsOutput> _colorBuffer;
  PNMImage    _colorTexels;
  Texture     _colorMap;
  PT(Camera)  _cameraNode;
  NodePath    _camera;
  
  void setupCamera();
};

#endif /*IMAGE_SENSOR_H*/
