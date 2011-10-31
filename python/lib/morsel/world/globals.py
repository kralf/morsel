from morsel.panda import *

#-------------------------------------------------------------------------------

world = None

#-------------------------------------------------------------------------------

NO_COLLISIONS_FROM       = panda.BitMask32( 0x00000000 )
NO_COLLISIONS_INTO       = panda.BitMask32( 0x00000000 )
STATIC_COLLISIONS_FROM   = panda.BitMask32( 0x00000001 )
STATIC_COLLISIONS_INTO   = panda.BitMask32( 0x11111110 )
ACTUATOR_COLLISIONS_FROM = panda.BitMask32( 0x00000010 )
ACTUATOR_COLLISIONS_INTO = panda.BitMask32( 0x11111101 )
SENSOR_COLLISIONS_FROM   = panda.BitMask32( 0x00000100 )
SENSOR_COLLISIONS_INTO   = panda.BitMask32( 0x11100011 )
ACTOR_COLLISIONS_FROM    = panda.BitMask32( 0x00001000 )
ACTOR_COLLISIONS_INTO    = panda.BitMask32( 0x11110101 )
PLATFORM_COLLISIONS_FROM = panda.BitMask32( 0x00010000 )
PLATFORM_COLLISIONS_INTO = panda.BitMask32( 0x11101111 )
