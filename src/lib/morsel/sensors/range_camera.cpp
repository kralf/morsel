#include "range_camera.h"

#include <cmath>
#include <string>
#include <limits>

using namespace std;

//------------------------------------------------------------------------------

RangeCamera::RangeCamera(
  string name,
  double horizontalAngle,
  double verticalAngle,
  double horizontalFOV,
  double verticalFOV,
  int horizontalRays,
  int verticalRays,
  double minRange,
  double maxRange,
  int horizontalResolution,
  int verticalResolution,
  bool acquireColor,
  string acquireLabel )
  : NodePath( name ),
    _name( name ),
    _horizontalAngle( horizontalAngle ),
    _verticalAngle( verticalAngle ),
    _horizontalFOV( horizontalFOV ),
    _verticalFOV( verticalFOV ),
    _horizontalRays( horizontalRays ),
    _verticalRays( verticalRays ),
    _minRange( minRange ),
    _maxRange( maxRange ),
    _width( horizontalResolution ),
    _height( verticalResolution ),
    _rayCount( horizontalRays * verticalRays ),
    _rayInfo( new RayInfo[_rayCount] ),
    _rays( new Ray[_rayCount] ),
    _acquireColor( acquireColor ),
    _acquireLabel( acquireLabel )
{
}

//------------------------------------------------------------------------------

RangeCamera::~RangeCamera()
{
  delete [] _rayInfo;
  delete [] _rays;
}

//------------------------------------------------------------------------------

int
RangeCamera::rayCount()
{
  return _rayCount;
}

//------------------------------------------------------------------------------

Ray &
RangeCamera::ray( int index ) {
  return _rays[index];
}


//------------------------------------------------------------------------------

double
RangeCamera::depth( int column, int row ) {
  if ( ( column >= 0 ) && ( column < _depthTexels.get_x_size() )  &&
      ( row >= 0 ) && ( row < _depthTexels.get_y_size() ) )
    return _maxRange * _minRange / ( _maxRange - _depthTexels.get_gray(
      column, row ) * ( _maxRange - _minRange ) );
  else
    return -1.0;
}

//------------------------------------------------------------------------------

bool
RangeCamera::update( double time )
{
  _depthMap.store( _depthTexels );
  if ( _acquireColor )
    _colorMap.store( _colorTexels );
  if ( !_acquireLabel.empty() )
    _labelMap.store( _labelTexels );
  updateRays();
  return true;
}

//------------------------------------------------------------------------------

bool
RangeCamera::inRange( NodePath & node )
{
  return true;
}

//------------------------------------------------------------------------------

void
RangeCamera::setActive( bool active )
{
  _depthCameraNode->set_active( active );
  _colorCameraNode->set_active( active );
  _labelCameraNode->set_active( active );
}

//------------------------------------------------------------------------------

void
RangeCamera::showFrustum()
{
  _depthCameraNode->show_frustum();
}

//------------------------------------------------------------------------------

void
RangeCamera::hideFrustum()
{
  _depthCameraNode->hide_frustum();
}

//------------------------------------------------------------------------------
// Protected methods
//------------------------------------------------------------------------------

void
RangeCamera::setupCamera( PT(Lens) lens )
{
  _depthMap.set_format( Texture::F_depth_component );
  _depthMap.set_component_type( Texture::T_unsigned_short );

  GraphicsOutput * window = getWindow( 0 );

  _depthBuffer = window->make_texture_buffer( "depthmap", _width, _height,
    &_depthMap, true );
  if ( _acquireColor )
    _colorBuffer = window->make_texture_buffer( "colormap", _width, _height,
      &_colorMap, true );
  if ( !_acquireLabel.empty() )
    _labelBuffer = window->make_texture_buffer( "labelmap", _width, _height,
      &_labelMap, true );

  _depthCameraNode = new Camera( "depthcam" );
  _depthCameraNode->set_camera_mask( BitMask32( 1 ) );
  _depthCameraNode->set_scene( getGSG()->get_scene()->get_scene_root() );
  _depthCameraNode->set_lens( lens );

  _depthCamera = attach_new_node( _depthCameraNode );
  _depthCamera.set_light_off( true );
  _depthCamera.set_material_off( true );
  _depthCamera.set_color_off( true );

  PT(DisplayRegion) drd = _depthBuffer->make_display_region();
  drd->set_sort( 0 );
  drd->set_camera( _depthCamera );

  if ( _acquireColor ) {
    _colorCameraNode = new Camera( "colorcam" );
    _colorCameraNode->set_camera_mask( BitMask32( 1 ) );
    _colorCameraNode->set_scene( getGSG()->get_scene()->get_scene_root() );
    _colorCameraNode->set_lens( lens );

    _colorCamera = attach_new_node( _colorCameraNode );
    
    PT(DisplayRegion) drc = _colorBuffer->make_display_region();
    drc->set_sort( 0 );
    drc->set_camera( _colorCamera );
  }

  if ( !_acquireLabel.empty() ) {
    _labelCameraNode = new Camera( "labelcam" );
    _labelCameraNode->set_camera_mask( BitMask32( 1 ) );
    _labelCameraNode->set_scene( getGSG()->get_scene()->get_scene_root() );
    _labelCameraNode->set_lens( lens );

    _labelCamera = attach_new_node( _labelCameraNode );

    PT(DisplayRegion) drc = _labelBuffer->make_display_region();
    drc->set_sort( 0 );
    drc->set_camera( _labelCamera );
    
    ostringstream stream;
    stream << "void vshader(uniform float4x4 mat_modelproj," << endl;
    stream << "    in float4 vtx_position : POSITION," << endl;
    stream << "    out float4 l_position : POSITION," << endl;
    stream << "    out float4 l_color : COLOR) {" << endl;
    stream << "  l_position = mul(mat_modelproj, vtx_position);" << endl;
    stream << "}" << endl;
    stream << "void fshader(uniform float4 " << _acquireLabel << "," << endl;
    stream << "    uniform float4 max_label," << endl;
    stream << "    out float4 o_color : COLOR) {" << endl;
    stream << "  o_color = float4(" << endl;
    stream << "    " << _acquireLabel << "[0]/max_label[0]," << endl;
    stream << "    " << _acquireLabel << "[1]/max_label[1]," << endl;
    stream << "    " << _acquireLabel << "[2]/max_label[2]," << endl;
    stream << "    " << _acquireLabel << "[3]/max_label[3]" << endl;
    stream << "  );" << endl;
    stream << "}" << endl;
    _labelShader = Shader::make( stream.str(), Shader::SL_Cg );
    
    NodePath shaderAttrib( "shader label" );
    shaderAttrib.set_shader( _labelShader );
    shaderAttrib.set_shader_input( _acquireLabel,
      LVecBase4f(0.0, 0.0, 0.0, 0.0) );
    shaderAttrib.set_shader_input( "max_label",
      LVecBase4f(255.0, 255.0, 255.0, 255.0) );
    _labelCameraNode->set_initial_state( shaderAttrib.get_state() );
    _labelBuffer->set_clear_color( LVecBase4f(0.0, 0.0, 0.0, 0.0) );
  }
}

void
RangeCamera::updateRays()
{
  for ( int i = 0; i < _rayCount; i++ ) {
    RayInfo & ri = _rayInfo[i];
    Ray & ray = _rays[i];

    ray.y = depth( round( ri.column ), round( ri.row ) );
    if ( ray.y < _minRange )
      ray.y = 0.0;
    ray.x = ray.y * ri.hTan;
    ray.z = ray.y * ri.vTan;
    ray.radius = sqrt( ray.x * ray.x + ray.y * ray.y + ray.z * ray.z );
    ray.hAngle = ri.hAngle;
    ray.vAngle = ri.vAngle;
    ray.column = ri.column;
    ray.row = ri.row;
    
    if ( _acquireColor ) {
      ray.red = _colorTexels.get_red( ri.column, ri.row );
      ray.green = _colorTexels.get_green( ri.column, ri.row );
      ray.blue = _colorTexels.get_blue( ri.column, ri.row );
    }

    if ( !_acquireLabel.empty() ) {
      ray.label = ( _labelTexels.get_alpha_val( ri.column, ri.row ) << 24 ) +
        ( _labelTexels.get_blue_val( ri.column, ri.row ) << 16 ) +
        ( _labelTexels.get_green_val( ri.column, ri.row ) << 8 ) +
        _labelTexels.get_red_val( ri.column, ri.row );
    }
  }
}
