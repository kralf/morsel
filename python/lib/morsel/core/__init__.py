#===============================================================================
# Submodules
#===============================================================================

from _globals      import *
from framework     import *
from util          import *
import __builtin__
from panda3d.pandac import NodePath


if not __builtin__.__dict__.has_key( "scheduler" ):
  import scheduling
  __builtin__.__dict__["scheduler"] = scheduling.Scheduler()
if not __builtin__.__dict__.has_key( "eventManager" ):
  import  event_manager
  __builtin__.__dict__["eventManager"] = event_manager.EventManager()
scheduler.addTask( "updateActors", updateActors )
