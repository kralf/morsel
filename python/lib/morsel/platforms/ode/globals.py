from morsel.core import *

#-------------------------------------------------------------------------------

STATIC_CATEGORY       = panda.BitMask32( "001" )
STATIC_COLLIDE_BITS   = panda.BitMask32( "110" )
CHASSIS_CATEGORY      = panda.BitMask32( "010" )
CHASSIS_COLLIDE_BITS  = panda.BitMask32( "011" )
ACTUATOR_CATEGORY     = panda.BitMask32( "100" )
ACTUATOR_COLLIDE_BITS = panda.BitMask32( "001" )

