from sys import argv
from morsel.config import *

import __builtin__

#-------------------------------------------------------------------------------

if not __builtin__.__dict__.has_key("framework"):
  from framework import Framework
  __builtin__.__dict__["framework"] = Framework(argv)

#-------------------------------------------------------------------------------

framework.addMorselPath("conf", MORSEL_CONFIGURATION_PATH)
framework.addMorselPath("bam", "models")
framework.addMorselPath("egg", "models")
framework.addMorselPath("trk", "tracks")
framework.addMorselPath("pth", "paths")
framework.addMorselPath("tra", "trajectories")
framework.addMorselPath("scm", "scenes")
framework.addMorselPath("acm", "actuators")
framework.addMorselPath("sem", "sensors")
framework.addMorselPath("acm", "actors")
framework.addMorselPath("pfm", "platforms")
framework.addMorselPath("ctl", "control")
framework.addMorselPath("cg", "shaders")
framework.addMorselPath("glsl", "shaders")

framework.fullscreen = False
framework.windowPosition = [100, 100]
framework.windowSize = [800, 600]
framework.windowTitle = "%s version %s.%s.%s" % (MORSEL_NAME,
  MORSEL_MAJOR_VISION, MORSEL_MINOR_VISION, MORSEL_PATCH)

framework.setConfigVariable("background-color", [0.5, 0.5, 0.8])
framework.setConfigVariable("depth-bits", 16)
framework.setConfigVariable("direct-gui-edit", True)
framework.setConfigVariable("basic-shaders-only", False)

framework.run()
