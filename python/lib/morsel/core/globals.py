from sys import argv
from morsel.config import *

import __builtin__

#-------------------------------------------------------------------------------

if not __builtin__.__dict__.has_key("framework"):
  from framework import Framework
  __builtin__.__dict__["framework"] = Framework(argv)

#-------------------------------------------------------------------------------

framework.addMorselPath("cfg", MORSEL_CONFIGURATION_PATH)
framework.addMorselPath("bam", "models")
framework.addMorselPath("egg", "models")
framework.addMorselPath("trk", "tracks")
framework.addMorselPath("scm", "scenes")
framework.addMorselPath("acm", "actors")
framework.addMorselPath("sem", "sensors")
framework.addMorselPath("pfm", "platforms")
framework.addMorselPath("ctl", "control")

framework.setFullscreen(False)
framework.setWindowSize(800, 600)
framework.setWindowTitle("%s version %s.%s.%s" % (MORSEL_NAME,
  MORSEL_MAJOR_VISION, MORSEL_MINOR_VISION, MORSEL_PATCH))

framework.setConfigVariable("background-color", 0.5, 0.5, 0.8)
framework.setConfigVariable("depth-bits", 16)
framework.setConfigVariable("direct-gui-edit", True)

framework.run()
