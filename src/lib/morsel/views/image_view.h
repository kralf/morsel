#ifndef IMAGE_VIEW_H
#define IMAGE_VIEW_H

#include "morsel/morsel.h"

#include <nodePath.h>

class ImageSensor;

class ImageView : public NodePath
{
PUBLISHED:
  ImageView(
    std::string name,
    NodePath & sensor
  );
public:
  virtual ~ImageView();
PUBLISHED:
  bool update( double time );
protected:
  std::string _name;
  ImageSensor & _sensor;
  PointerTo<GraphicsOutput> _window;
  PointerTo<PandaNode> _sceneNode;
  PointerTo<Camera> _cameraNode;
  NodePath _scene;
  NodePath _camera;
  NodePath _card;
  Texture _texture;
  
  void setupRendering();
};

#endif /*IMAGE_VIEW_H*/
