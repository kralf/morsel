from morsel.config  import *
from morsel.core    import *
from morsel.gui     import *
from morsel.console import interactiveConsole as Console

#-------------------------------------------------------------------------------

camera           = base.camera

objectProperties = ObjectProperties()

console_context  = inspect.stack()[2][0].f_globals
console          = Console.pandaConsole(
                     Console.INPUT_GUI | Console.OUTPUT_PYTHON,
                     console_context )
console.toggle()

paths = {}

addMorselPath( "cfg", MORSEL_CONFIGURATION_PATH )
addMorselPath( "bam", "models" )
addMorselPath( "egg", "models" )
addMorselPath( "trk", "tracks")
addMorselPath( "acm", "actors")
addMorselPath( "pfm", "platforms")
