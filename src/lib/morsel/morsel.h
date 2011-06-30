#ifndef MORSEL_H
#define MORSEL_H

#include <string.h>
#include <cstring>
#include <cstdlib>

#include <panda.h>

#include <graphicsEngine.h>

//------------------------------------------------------------------------------
// Functions to access global structures
//------------------------------------------------------------------------------

GraphicsStateGuardian * getGSG();
GraphicsEngine * getEngine();
GraphicsOutput * getWindow( int index );

#endif /*MORSEL_H*/
