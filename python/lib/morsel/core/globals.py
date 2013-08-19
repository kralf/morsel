from sys import argv
from morsel.config import *

import __builtin__

#-------------------------------------------------------------------------------

if not __builtin__.__dict__.has_key("framework"):
  from framework import Framework
  __builtin__.__dict__["framework"] = Framework(*argv)

#-------------------------------------------------------------------------------

framework.setConfigVariable("depth-bits", 16)
framework.setConfigVariable("basic-shaders-only", False)

framework.run()
