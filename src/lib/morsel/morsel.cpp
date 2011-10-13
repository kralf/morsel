#include "morsel.h"

#include <pandaFramework.h>

//------------------------------------------------------------------------------

GraphicsStateGuardian * 
getGSG() 
{
  return static_cast<GraphicsStateGuardian*>(
    GraphicsStateGuardianBase::get_default_gsg() );
}

//------------------------------------------------------------------------------

GraphicsEngine * 
getEngine() 
{
  return getGSG()->get_engine();
}

//------------------------------------------------------------------------------

GraphicsOutput * 
getWindow( int index )
{
  return getEngine()->get_window( index );
}
