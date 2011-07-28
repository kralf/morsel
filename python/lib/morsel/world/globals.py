from morsel.core import *

#-------------------------------------------------------------------------------

world = None

#-------------------------------------------------------------------------------

NO_COLLISIONS_FROM       = panda.BitMask32( 0x00000000 )
NO_COLLISIONS_INTO       = panda.BitMask32( 0x00000000 )
STATIC_COLLISIONS_FROM   = panda.BitMask32( 0x00000001 )
STATIC_COLLISIONS_INTO   = panda.BitMask32( 0x11111110 )
ACTOR_COLLISIONS_FROM    = panda.BitMask32( 0x00000010 )
ACTOR_COLLISIONS_INTO    = panda.BitMask32( 0x00000011 )
PLATFORM_COLLISIONS_FROM = panda.BitMask32( 0x00000100 )
PLATFORM_COLLISIONS_INTO = panda.BitMask32( 0x00000011 )
