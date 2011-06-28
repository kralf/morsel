from sys             import argv
from facade   import *

if len( argv ) > 1:
  includeConfig( "defaults.cfg" )
  includeConfig( argv[1] )
else:
  error( "You should specify a configuration file." )

run()
