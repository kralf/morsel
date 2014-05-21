from panda3d import pandac as panda
from panda3d.direct.showbase.ShowBase import ShowBase

from morsel.config import Configuration

from scheduler import Scheduler
from event_manager import EventManager
from event_handler import EventHandler
from package import Package

from math import *
import sys
import os
from os.path import *
from optparse import OptionParser, OptionGroup
import re
import string
import traceback

import __builtin__
import inspect
import pkgutil

#-------------------------------------------------------------------------------

class Framework(object):
  def __init__(self, *argv):
    super(Framework, self).__init__()
    
    self.packages = {}
    self.paths = {}
    self.callbacks = {}
    self.layers = {}
    self.shortcuts = {}

    self.base = None
    self.window = None
    self.displayRegion = None
    self.camera = None
    self.cameraMask = 0x700000FF
    
    self.scheduler = None
    self.eventManager = None
    self.gui = None
    self.world = None
    
    self.activeLayer = None
    self.captureTask = None
    self.frame = 0

    self.configuration = Configuration()    
    
    self.parser = OptionParser(version = self.configuration.fullName,
      description = ("%s Copyright by %s. For additional help, contact "+
        "the authors at <%s> or visit the project homepage under %s.") % \
        (self.configuration.summary, self.configuration.authors,
        self.configuration.contact, self.configuration.home),
      usage = "usage: %prog [OPT1 [OPT2 [...]]] [FILE1 [FILE2 [...]]",
      add_help_option = False)

    self.parser.add_option("-h", "--help", dest = "help", default = False,
      action = "store_true", help = "show this help message and exit")
      
    group = OptionGroup(self.parser, "Options that control the simulation")
    group.add_option("--framerate", dest = "framerate", type = "float",
      metavar = "FPS", default = 60.0, action = "store",
      help = "maximum framerate in frames/s [%default]")
    group.add_option("-f", "--fullscreen", dest = "fullscreen", default = False,
      action = "store_true", help = "startup in fullscreen mode")
    group.add_option("-p", "--pause", dest = "pause", default = False,
      action = "store_true", help = "immediately pause simulation on startup")
    self.parser.add_option_group(group)

    group = OptionGroup(self.parser, "Framework configuration options")
    group.add_option("-i", "--include", dest = "include", metavar = "PACKAGE",
      action = "append", help = "include a list of packages")
    self.parser.add_option_group(group)

    group = OptionGroup(self.parser, "Output and debugging options")
    group.add_option("-v", "--verbose", dest = "verbose", default = False,
      action = "store_true", help = "enable verbose output")
    group.add_option("-d", "--debug", dest = "debug", default = False,
      action = "store_true", help = "enable debugging output")
    self.parser.add_option_group(group)
      
    group = OptionGroup(self.parser, "Options that provide information")
    group.add_option("--build", dest = "build", default = False,
      action = "store_true", help = "print build information and exit")
    group.add_option("--defaults", dest = "defaults", default = False,
      action = "store_true", help = "print default paths and exit")
    self.parser.add_option_group(group)
    
    (self.options, self.arguments) = self.parser.parse_args()

    self.verbose = self.options.verbose
    self.debug = self.options.debug

    self.include("morsel")
    self.addPath("conf", self.configuration.configurationPath)
    self.configFiles = ["defaults.conf"]
    self.windowTitle = self.configuration.fullName
        
    if self.options.include:
      for include in self.options.include:
        self.include(include)

    reparse = False
    for package in self.packages:
      if self.packages[package].options:
        group = OptionGroup(self.parser, "Options defined by "+package)
        group.add_options(self.packages[package].options)
        self.parser.add_option_group(group)
        reparse = True
    if reparse:
      (self.options, self.arguments) = self.parser.parse_args()

    if self.options.help:
      self.parser.print_help()
      exit(0)
    if self.options.build:
      print "Build system: %s" % self.configuration.buildSystem
      print "Build architecture: %s" % self.configuration.buildArchitecture
      print "Build type: %s" % self.configuration.buildType
      exit(0)
    if self.options.defaults:
      for package in self.packages:
        print "Package "+package+":"
        print "  System path: "+self.getSystemDir(package)
        print "  Configuration path: "+self.getConfigDir(package)
        print "  User path: "+self.getUserDir(package)
      exit(0)

    for argument in self.arguments:
      matched = False
      for package in self.packages:
        if self.packages[package].arguments:
          for dest in self.packages[package].arguments:
            match = re.match(self.packages[package].arguments[dest], argument)
            if match:
              if len(match.groups()) > 1:
                value = list(match.groups())
              else:
                value = match.group(1)
              setattr(self.packages[package].configuration, dest, value)
                
              matched = True
        
      if not matched:
        self.configFiles.append(argument)
      
#-------------------------------------------------------------------------------

  def getSystemDir(self, package = "morsel"):
    try:
      return os.environ[self.packages[package].homeVar]
    except KeyError:
      return self.packages[package].systemDir

  systemDir = property(getSystemDir)

#-------------------------------------------------------------------------------

  def getConfigDir(self, package = "morsel"):
    return self.packages[package].configDir

  configDir = property(getConfigDir)

#-------------------------------------------------------------------------------

  def getUserDir(self, package = "morsel"):
    return self.packages[package].userDir

  userDir = property(getUserDir)

#-------------------------------------------------------------------------------

  def getGUI(self):
    if hasattr(self, "_gui") and self._gui:
      return self._gui
    else:
      return None

  def setGUI(self, gui):
    if not hasattr(self, "_gui") or not self._gui:
      self._gui = gui
    else:
      self.error("GUI already initialized.")

  gui = property(getGUI, setGUI)
  
#-------------------------------------------------------------------------------

  def getWorld(self):
    if hasattr(self, "_world") and self._world:
      return self._world
    else:
      return None

  def setWorld(self, world):
    if not hasattr(self, "_world") or not self._world:
      self._world = world
    else:
      self.error("World already initialized.")
      
  world = property(getWorld, setWorld)
      
#-------------------------------------------------------------------------------

  def getConfigVariable(self, variable, types):
    variable = panda.ConfigVariable(variable)
    if not isinstance(types, list):
      types = [types]

    values = []
    for i in range(len(types)):
      if types[i] == bool:
        values.append(bool(variable.getBoolWord(i)))
      elif types[i] == float:
        values.append(float(variable.getDoubleWord(i)))
      elif types[i] == int:
        values.append(int(variable.getIntWord(i)))
      elif types[i] == str:
        values.append(str(variable.getStringWord(i)))

    if len(values) == 1:
      return values[i]
    elif not values:
      return None
    else:
      return values

  def setConfigVariable(self, variable, values):
    variable = panda.ConfigVariable(variable)
    if not isinstance(values, list):
      values = [values]
    
    for i in range(len(values)):
      if type(values[i]) == bool:
        variable.setBoolWord(i, values[i])
      elif type(values[i]) == float:
        variable.setDoubleWord(i, values[i])
      elif type(values[i]) == int:
        variable.setIntWord(i, values[i])
      elif type(values[i]) == str:
        variable.setStringWord(i, values[i])

#-------------------------------------------------------------------------------

  def getFullscreen(self):
    return self.getConfigVariable("fullscreen", bool)

  def setFullscreen(self, fullscreen):
    self.setConfigVariable("fullscreen", fullscreen)

    if self.window:
      properties = panda.WindowProperties(self.window.getProperties())
      properties.setFullscreen(fullscreen)
      self.window.requestProperties(properties)

  fullscreen = property(getFullscreen, setFullscreen)

#-------------------------------------------------------------------------------

  def getWindowPosition(self):
    return self.getConfigVariable("win-origin", [float, float])

  def setWindowPosition(self, position):
    self.setConfigVariable("win-origin", position)

    if self.window:
      properties = panda.WindowProperties(self.window.getProperties())
      properties.setOrigin(position[0], position[1])
      self.window.requestProperties(properties)

  windowPosition = property(getWindowPosition, setWindowPosition)

#-------------------------------------------------------------------------------

  def getWindowSize(self):
    return self.getConfigVariable("win-size", [float, float])

  def setWindowSize(self, size):
    self.setConfigVariable("win-size", size)

    if self.window:
      properties = panda.WindowProperties(self.window.getProperties())
      properties.setSize(size[0], size[1])
      self.window.requestProperties(properties)

  windowSize = property(getWindowSize, setWindowSize)

#-------------------------------------------------------------------------------

  def getWindowTitle(self):
    return self.getConfigVariable("window-title", str)

  def setWindowTitle(self, title):
    self.setConfigVariable("window-title", title)

    if self.window:
      properties = panda.WindowProperties(self.window.getProperties())
      properties.setTitle(title)
      self.window.requestProperties(properties)

  windowTitle = property(getWindowTitle, setWindowTitle)

#-------------------------------------------------------------------------------

  def getBackgroundColor(self):
    return self.getConfigVariable("background-color",
      [float, float, float, float])

  def setBackgroundColor(self, color):
    self.setConfigVariable("background-color", color)

    if self.displayRegion:
      self.displayRegion.setClearColorActive(True)
      self.displayRegion.setClearColor(panda.Vec4(*color))

  backgroundColor = property(getBackgroundColor, setBackgroundColor)

#-------------------------------------------------------------------------------

  def getShowFrameRate(self):
    return self.getConfigVariable("show-frame-rate-meter", bool)

  def setShowFrameRate(self, show):
    self.setConfigVariable("show-frame-rate-meter", show)

    if self.base:
      self.base.setFrameRateMeter(show)

  showFrameRate = property(getShowFrameRate, setShowFrameRate)

#-------------------------------------------------------------------------------

  def getMaxFrameRate(self):
    mode = self.getConfigVariable("clock-mode", str)
    if mode == "normal":
      return None
    else:
      return self.getConfigVariable("clock-frame-rate", float)

  def setMaxFrameRate(self, frameRate):
    if frameRate:
      self.setConfigVariable("clock-mode", "limited")
      self.setConfigVariable("clock-frame-rate", frameRate)
      if self.scheduler:
        self.scheduler.clock.setMode(panda.ClockObject.MLimited)
        self.scheduler.clock.setFrameRate(frameRate)
    else:
      self.setConfigVariable("clock-mode", "normal")
      if self.scheduler:
        self.scheduler.clock.setMode(panda.ClockObject.MNormal)

  maxFrameRate = property(getMaxFrameRate, setMaxFrameRate)

#-------------------------------------------------------------------------------
  
  def getCameraMask(self):
    return self._cameraMask

  def setCameraMask(self, cameraMask):
    self._cameraMask = cameraMask
    
    if self.camera:
      self.camera.setCameraMask(panda.BitMask32(self._cameraMask))
      
  cameraMask = property(getCameraMask, setCameraMask)
      
#-------------------------------------------------------------------------------

  def getActiveLayer(self):
    return self._activeLayer

  def setActiveLayer(self, layer):
    if not layer or self.layers.has_key(layer):
      self._activeLayer = layer
      if self.world and self.world.scene:
        self.world.scene.activeLayer = layer
    else:
      self.error("Layer '"+layer+"' is undefined.")

  activeLayer = property(getActiveLayer, setActiveLayer)

#-------------------------------------------------------------------------------

  def include(self, package, **kargs):
    package = package.replace("-", "_")
    if package in self.packages.keys():
      return
    
    self.info("Including package: "+package)
    try:
      self.packages[package] = Package(package, **kargs)
    except Exception as includeError:
      self.error("Failed to include package "+package+": "+str(includeError))
      
    if self.packages[package].requires:
      for required in self.packages[package].requires:
        self.include(required)
      
    packageModule = __import__(self.packages[package].module)
    packagePath = os.path.dirname(packageModule.__file__)
    modules = [name for _, name, _ in pkgutil.iter_modules([packagePath])]

    if "facade" in modules:      
      facade = __import__(self.packages[package].module+".facade",
        __builtin__.globals(), __builtin__.locals(), ["*"])
      for expression in dir(facade):
        if not __builtin__.__dict__.has_key(expression):
          __builtin__.__dict__[expression] = getattr(facade, expression)

#-------------------------------------------------------------------------------

  def addPath(self, extension, *args):
    if not self.paths.has_key(extension):
      self.paths[extension] = []

    for path in args:
      if not path in self.paths[extension]:
        self.paths[extension].append(path)

#-------------------------------------------------------------------------------

  def addLayer(self, layer, description):
    self.layers[layer] = description
    if len(self.layers) == 1:
      self.activeLayer = layer

#-------------------------------------------------------------------------------

  def addShortcut(self, key, function, description):
    if not key in self.shortcuts:
      self.shortcuts[key] = description

      handler = EventHandler(function)
      self.eventManager.addHandler(key, handler)
    else:
      self.error("Duplicate shortcut for '"+key+"' key.")

#-------------------------------------------------------------------------------

  def error(self, message):
    raise RuntimeError(message)

#-------------------------------------------------------------------------------

  def info(self, message):
    if self.verbose or self.debug:
      message = message.strip().split("\n")
      message = string.join(message, "\nInfo: ")
        
      print "Info: "+message

#-------------------------------------------------------------------------------

  def spam(self, message):
    if self.debug:
      message = message.strip().split("\n")
      message = string.join(message, "\nDebug: ")
        
      print "Debug: "+message

#-------------------------------------------------------------------------------

  def findConfigFile(self, filename, package = None):
    if os.path.exists(filename):
      return os.path.abspath(filename)

    if package:
      packages = [package]
    else:
      packages = self.packages.keys()
    
    for package in reversed(packages):
      resultPath = os.path.join(self.getConfigDir(package), filename)
      if os.path.exists(resultPath):
        return os.path.abspath(resultPath)

    return None

#-------------------------------------------------------------------------------

  def findFile(self, filename, package = None):
    if os.path.exists(filename):
      return os.path.abspath(filename)

    name, extension = os.path.splitext(filename)
    extension = extension[1:]

    if self.paths.has_key(extension):
      if package:
        packages = [package]
      else:
        packages = self.packages.keys()
      
      for path in self.paths[extension]:
        if not os.path.isabs(path):
          for package in reversed(packages):
            for dir in [self.getUserDir(package), self.getSystemDir(package)]:
              resultPath = os.path.join(dir, path, filename)
              if os.path.exists(resultPath):
                return os.path.abspath(resultPath)
        else:
          resultPath = os.path.join(path, filename)
          if os.path.exists(resultPath):
            return os.path.abspath(resultPath)

    return None

#-------------------------------------------------------------------------------

  def loadConfigFile(self, filename, package = None):
    configFile = self.findConfigFile(filename, package)
    
    if configFile:
      self.info("Loading configuration file: "+configFile)
      context = inspect.stack()[1][0].f_globals
      execfile(configFile, context)
    else:
      self.error("Configuration file '"+filename+"' not found.")
    
#-------------------------------------------------------------------------------

  def executeFile(self, filename, package = None, **kargs):
    filePath = self.findFile(filename, package)
    
    if filePath:
      context = inspect.stack()[1][0].f_globals
      parameters = {}
      execfile(filePath, context, parameters)
      parameters.update(kargs)

      return parameters
    else:
      self.error("File '"+filename+"' not found.")

#-------------------------------------------------------------------------------

  def createInstance(self, module, type, **kargs):
    for package in reversed(self.packages.keys()):
      try:
        imported = __import__(self.packages[package].module+"."+module,
          __builtin__.globals(), __builtin__.locals(), [type])
        instance = getattr(imported, type)
      except ImportError as importError:
        self.spam("Importing type "+type+" from "+
          self.packages[package].module+"."+module+" failed: "+
          str(importError))
        self.spam(traceback.format_exc())
      except AttributeError as attributeError:
        self.spam("Importing type "+type+" from "+
          self.packages[package].module+"."+module+" failed: "+
          str(attributeError))
        self.spam(traceback.format_exc())
      else:
        self.spam("Importing type "+type+" from "+
          self.packages[package].module+"."+module+" succeeded")
        return instance(**kargs)

    error = "Failed to import "+type+" from module "+module+"."
    if self.debug:
      error = error+" See debugging output for details."
    else:
      error = error+" Enable debugging output for details."
    self.error(error)
        
#-------------------------------------------------------------------------------

  def loadInstance(self, module, filename = None, **kargs):
    if filename:
      parameters = self.executeFile(filename, **kargs)
    else:
      parameters = kargs

    if parameters.has_key("type"):
      type = parameters["type"]
      del parameters["type"]

      return self.createInstance(module, type, **parameters)
    else:
      self.error("Missing type parameter.")

#-------------------------------------------------------------------------------

  def importPhysics(self, name, module = None):      
    if module:
      if not self.world:
        self.error("Failed to import physics class "+name+
          " from module "+module+": World not initialized.")
      
      submodules = name.split(".")
      if len(submodules) > 1:
        module = module+"."+self.world.physics+"."+string.join(
          submodules[0:len(submodules)-1], ".")
        name = submodules[-1]
      else:
        module = module+"."+self.world.physics
      
      module = __import__(module, fromlist=[name])
      return getattr(module, name)
    else:
      if not self.world:
        self.error("Failed to import physics module "+module+
          ": World not initialized.")
          
      return __import__(name+"."+self.world.physics)

#-------------------------------------------------------------------------------

  def run(self):
    if not self.base:
      self.base = ShowBase()
      self.window = self.base.win
      self.camera = self.base.camera.getChild(0).node()
      self.displayRegion = self.camera.getDisplayRegion(0)
      
      self.scheduler = Scheduler(pause = self.options.pause)
      self.eventManager = EventManager()

      for configFile in self.configFiles:
        self.loadConfigFile(configFile)
      self.locals = inspect.stack()[0][0].f_globals

      self.maxFrameRate = self.options.framerate
      self.fullscreen = self.options.fullscreen
      
      self.camera.setCameraMask(panda.BitMask32(self.cameraMask))
      self.camera.getDisplayRegion(0).setDrawCallback(
        panda.PythonCallbackObject(self.drawCallback))
        
      self.base.run()
    else:
      self.error("Framework already running.")

#-------------------------------------------------------------------------------

  def exit(self):
    sys.exit()

#-------------------------------------------------------------------------------

  def toggleLayer(self):
    layers = self.layers.keys()
    index = layers.index(self.activeLayer)

    self.activeLayer = layers[(index+1)%len(layers)]

#-------------------------------------------------------------------------------

  def saveScreen(self, filename = "frame-%.jpg"):
    if self.window:
      filename = filename.replace("%", "%06d" % (self.frame))
      self.window.saveScreenshot(filename)
      self.frame += 1

#-------------------------------------------------------------------------------

  def toggleCaptureScreen(self, framerate = 24):
    if not self.captureTask:
      self.captureTask = self.scheduler.addTask("CaptureScreen",
        self.captureScreen, period = 1.0/framerate)
    else:
      self.scheduler.removeTask(self.captureTask)

#-------------------------------------------------------------------------------

  def captureScreen(self, time):
    self.saveScreen()
    return True

#-------------------------------------------------------------------------------

  def addDrawCallback(self, name, callback):
    self.callbacks[name] = callback
  
#-------------------------------------------------------------------------------

  def drawCallback(self, data):
    for callback in self.callbacks.itervalues():
      callback()
    
    data.upcall()
