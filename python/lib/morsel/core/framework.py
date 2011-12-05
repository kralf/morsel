from panda3d import pandac as panda
from panda3d.direct.showbase.ShowBase import ShowBase

from scheduler import Scheduler
from event_manager import EventManager
from package import Package

from morsel.console import interactive_console as Console
from morsel.gui.object_manager import ObjectManager
from morsel.config import *

from math import *
from os import *
from os.path import *

import __builtin__
import inspect

#-------------------------------------------------------------------------------

class Framework(object):
  def __init__(self, *argv):
    object.__init__(self)

    self.arguments = argv[0]
    self.packages = {}
    self.paths = {}
    self.configFiles = ["defaults.conf"];
    for argument in self.arguments[1:]:
      self.configFiles.append(argument)
      
    self.base = None
    self.scheduler = None
    self.eventManager = None
    self.objectManager = None
    self.console = None
    self.world = None

    self.debug = False
  
#-------------------------------------------------------------------------------

  def getSystemDir(self, package = "morsel"):
    try:
      return os.environ[self.packages[package].homeVar]
    except KeyError:
      return self.packages[package].systemDir

  systemDir = property(getSystemDir)

#-------------------------------------------------------------------------------

  def getUserDir(self, package = "morsel"):
    return self.packages[package].userDir

  userDir = property(getUserDir)

#-------------------------------------------------------------------------------

  def getWorld(self):
    return self._world

  def setWorld(self, world):
    if not self._world:
      self._world = world
    else:
      self.error("Word already initialized")
      
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

    if self.base:
      properties = panda.WindowProperties(self.base.win.getProperties())
      properties.setFullscreen(fullscreen)
      self.base.win.requestProperties(properties)

  fullscreen = property(getFullscreen, setFullscreen)

#-------------------------------------------------------------------------------

  def getWindowPosition(self):
    return self.getConfigVariable("win-origin", [float, float])

  def setWindowPosition(self, position):
    self.setConfigVariable("win-origin", position)

    if self.base:
      properties = panda.WindowProperties(self.base.win.getProperties())
      properties.setOrigin(position[0], position[1])
      self.base.win.requestProperties(properties)

  windowPosition = property(getWindowPosition, setWindowPosition)

#-------------------------------------------------------------------------------

  def getWindowSize(self):
    return self.getConfigVariable("win-size", [float, float])

  def setWindowSize(self, size):
    self.setConfigVariable("win-size", size)

    if self.base:
      properties = panda.WindowProperties(self.base.win.getProperties())
      properties.setSize(size[0], size[1])
      self.base.win.requestProperties(properties)

  windowSize = property(getWindowSize, setWindowSize)

#-------------------------------------------------------------------------------

  def getWindowTitle(self):
    return self.getConfigVariable("window-title", str)

  def setWindowTitle(self, title):
    self.setConfigVariable("window-title", title)

    if self.base:
      properties = panda.WindowProperties(self.base.win.getProperties())
      properties.setTitle(title)
      self.base.win.requestProperties(properties)

  windowTitle = property(getWindowTitle, setWindowTitle)

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

  def include(self, package, **kargs):
    self.packages[package] = Package(package, **kargs)
    
    try:
      facade = __import__(self.packages[package].module+".facade",
        __builtin__.globals(), __builtin__.locals(), ["*"])
    except ImportError:
      pass
    else:
      for expression in dir(facade):
        if not __builtin__.__dict__.has_key(expression):
          __builtin__.__dict__[expression] = getattr(facade, expression)

#-------------------------------------------------------------------------------

  def addPath(self, extension, path):
    if not self.paths.has_key(extension):
      self.paths[extension] = []

    if not path in self.paths[extension]:
      self.paths[extension].append(path)

#-------------------------------------------------------------------------------

  def error(self, message):
    raise RuntimeError("Error: "+message)

#-------------------------------------------------------------------------------

  def findFile(self, filename):
    if os.path.exists(filename):
      return os.path.abspath(filename)

    for package in self.packages:
      resultPath = self.findPackageFile(filename, package)
      if resultPath:
        return resultPath

    return None

#-------------------------------------------------------------------------------

  def findPackageFile(self, filename, package = "morsel"):
    if os.path.exists(filename):
      return os.path.abspath(filename)

    name, extension = os.path.splitext(filename)
    extension = extension[1:]

    if self.paths.has_key(extension):
      for path in self.paths[extension]:
        if not os.path.isabs(path):
          for dir in [self.getUserDir(package), self.getSystemDir(package)]:
            resultPath = os.path.join(dir, path, filename)
            if os.path.exists(resultPath):
              return os.path.abspath(resultPath)
        else:
          resultPath = os.path.join(path, package, filename)
          if os.path.exists(resultPath):
            return os.path.abspath(resultPath)

    return None

#-------------------------------------------------------------------------------

  def loadConfigFile(self, filename):
    configFile = self.findFile(filename)
    
    if configFile:
      context = inspect.stack()[1][0].f_globals
      execfile(configFile, context)
    else:
      self.error("Configuration file '" + filename + "' not found.")
    
#-------------------------------------------------------------------------------

  def executeFile(self, filename, **kargs):
    filePath = self.findFile(filename)
    
    if filePath:
      context = inspect.stack()[1][0].f_globals
      parameters = {}
      execfile(filePath, context, parameters)
      parameters.update(kargs)

      return parameters
    else:
      self.error("File '"+filename+"' not found")

#-------------------------------------------------------------------------------

  def createInstance(self, module, type, **kargs):
    for package in self.packages:
      try:
        imported = __import__(self.packages[package].module+"."+module,
          __builtin__.globals(), __builtin__.locals(), [type])
        instance = getattr(imported, type)
      except ImportError:
        pass
      except AttributeError:
        pass
      else:
        return instance(**kargs)

    self.error("Failed to import "+type+" from module "+module)

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
      self.error("Missing type parameter")

#-------------------------------------------------------------------------------

  def run(self):
    if not self.base:
      self.base = ShowBase()
      self.scheduler = Scheduler()
      self.eventManager = EventManager()

      for configFile in self.configFiles:
        self.loadConfigFile(configFile)

      self.console = Console.pandaConsole(Console.INPUT_GUI |
        Console.OUTPUT_PYTHON, inspect.stack()[2][0].f_globals)
      self.console.toggle()
      self.objectManager = ObjectManager()

      self.base.run()
    else:
      self.error("Framework.run() may only be called once.")

#-------------------------------------------------------------------------------

  def exitHandler(self, key):
    exit

#-------------------------------------------------------------------------------

  def pauseHandler(self, key):
    self.scheduler.togglePause()
    