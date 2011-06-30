#ifndef MORSEL_H
#define MORSEL_H

#include <string.h>
#include <cstring>
#include <cstdlib>

#include <panda.h>

// Nasty patch needed for interrogate to work.
// #ifndef FD_SET
// typedef struct sockaddr_in AddressType;
// typedef long fd_mask;
// typedef struct fd_set {
//    fd_mask fds_bits[howmany(FD_SETSIZE, NFDBITS)];
// } fd_set;
// #endif

#include <graphicsEngine.h>

//------------------------------------------------------------------------------
// Functions to access global structures
//------------------------------------------------------------------------------

GraphicsStateGuardian * getGSG();
GraphicsEngine * getEngine();
GraphicsOutput * getWindow( int index );

#endif /*MORSEL_H*/
