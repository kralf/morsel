#include "image_view.h"
#include "morsel/sensors/image_sensor.h"

#include <pandaFramework.h>
#include <orthographicLens.h>
#include <cardMaker.h>

using namespace std;

//------------------------------------------------------------------------------

ImageView::ImageView(
  std::string name,
  NodePath & sensor
) : NodePath( name ),
    _name( name ),
    _sensor( static_cast<ImageSensor&>( sensor ) )
{
  setupRendering();
}

//------------------------------------------------------------------------------

ImageView::~ImageView()
{
}

//------------------------------------------------------------------------------

bool
ImageView::update( double time )
{
  return true;
}

//------------------------------------------------------------------------------
// Protected methods
//------------------------------------------------------------------------------

void
ImageView::setupRendering()
{
  GraphicsStateGuardian * gsg = getGSG();
  GraphicsEngine * engine = getEngine();

  FrameBufferProperties fbProps = FrameBufferProperties::get_default();
  WindowProperties winProps = WindowProperties::get_default();
  winProps.set_size( _sensor.horizontalResolution(),
    _sensor.verticalResolution() );
  winProps.set_title( _sensor.name() );
  int flags = GraphicsPipe::BF_require_window |
    GraphicsPipe::BF_fb_props_optional;

  _window = engine->make_output( gsg->get_pipe(), "window", 0, fbProps,
      winProps, flags, gsg );

  _sceneNode = new PandaNode( "scene" );
  _scene = attach_new_node( _sceneNode );

  _cameraNode = new Camera( "cam" );
  _cameraNode->set_camera_mask( BitMask32( 1 ) );
  _cameraNode->set_scene( _scene );
  _camera = _scene.attach_new_node( _cameraNode );

  PT(Lens) lens = new OrthographicLens();
  lens->set_film_size(2.0, 2.0);
  lens->set_near_far(-1.0, 1.0);
  _cameraNode->set_lens( lens );

  _scene.set_depth_test( false );
  _scene.set_depth_write( false );

  PT(DisplayRegion) drc = _window->make_display_region();
  drc->set_camera( _camera );

  CardMaker cm( "card" );
  cm.set_frame( -1.0, 1.0, -1.0, 1.0 );
  _card = _scene.attach_new_node( cm.generate() );
  _card.set_texture( _sensor.colorMap() );
}
