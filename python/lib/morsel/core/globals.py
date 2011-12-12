from sys import argv
from morsel.config import *

import __builtin__

#-------------------------------------------------------------------------------

if not __builtin__.__dict__.has_key("framework"):
  from framework import Framework
  __builtin__.__dict__["framework"] = Framework(argv)

#-------------------------------------------------------------------------------

framework.include("morsel")

framework.addPath("conf", MORSEL_CONFIGURATION_PATH)
framework.addPath("bam", "models")
framework.addPath("egg", "models")
framework.addPath("trk", "tracks")
framework.addPath("pth", "paths")
framework.addPath("tra", "trajectories")
framework.addPath("scm", "scenes")
framework.addPath("acm", "actuators")
framework.addPath("sem", "sensors")
framework.addPath("acm", "actors")
framework.addPath("pfm", "platforms")
framework.addPath("ctl", "control")
framework.addPath("cg", "shaders")
framework.addPath("glsl", "shaders")

framework.fullscreen = False
framework.windowPosition = [100, 100]
framework.windowSize = [800, 600]
framework.windowTitle = MORSEL_FULL_NAME

framework.setConfigVariable("background-color", [0.5, 0.5, 0.8])
framework.setConfigVariable("depth-bits", 16)
framework.setConfigVariable("direct-gui-edit", True)
framework.setConfigVariable("basic-shaders-only", False)

framework.addLayer("low_poly", "Low polygon meshes")
framework.addLayer("high_poly", "High polygon meshes")

framework.run()
