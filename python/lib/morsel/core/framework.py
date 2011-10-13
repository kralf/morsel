from panda3d import pandac as panda
from panda3d.direct.showbase.ShowBase import ShowBase

from scheduler import Scheduler
from event_manager import EventManager
from morsel.console import interactive_console as Console
from morsel.gui.object_manager import ObjectManager

from morsel.config import *
from morsel.facade import *
from math import *
from os import *
from os.path import *

import inspect

#-------------------------------------------------------------------------------

class Framework:
  def __init__(self, *argv):
    self.arguments = argv[0]
    self.paths = {}
    self.configFiles = ["defaults.cfg"];
    for argument in self.arguments[1:]:
      self.configFiles.append(argument)
      
    self.base = None
    self.scheduler = None
    self.eventManager = None
    self.objectManager = None
    self.console = None
  
#-------------------------------------------------------------------------------

  def getHomeDir(self):
    return os.environ["HOME"]

  homeDir = property(getHomeDir)

#-------------------------------------------------------------------------------

  def getMorselSystem(self):
    try:
      return os.environ["MORSEL_HOME"]
    except KeyError:
      return MORSEL_FILE_PATH

  morselSystem = property(getMorselSystem)

#-------------------------------------------------------------------------------

  def getMorselUser(self):
    return self.homeDir+"/.morsel"

  morselUser = property(getMorselUser)

#-------------------------------------------------------------------------------

  def setConfigVariable(self, variable, *values):
    prc = variable

    for value in values:
      if isinstance(value, bool):
        if value:
          value = "#t"
        else:
          value = "#f"
      prc += " %s" % (value)

    panda.loadPrcFileData("", prc)

#-------------------------------------------------------------------------------

  def setFullscreen(self, value):
    self.setConfigVariable("fullscreen", value)

#-------------------------------------------------------------------------------

  def setWindowSize(self, width, height):
    self.setConfigVariable("win-size", "%s %s" % (width, height))

#-------------------------------------------------------------------------------

  def setWindowTitle(self, title):
    self.setConfigVariable("window-title", title)

#-------------------------------------------------------------------------------

  def addPath(self, extension, path):
    if not self.paths.has_key(extension):
      self.paths[extension] = []

    if not path in self.paths[extension]:
      self.paths[extension].append(path)

#-------------------------------------------------------------------------------

  def addMorselPath(self, extension, path):
    self.addPath(extension, os.path.join(".", path))
    self.addPath(extension, os.path.join(self.morselUser, path))
    self.addPath(extension, os.path.join(self.morselSystem, path))

#-------------------------------------------------------------------------------

  def error(self, message):
    raise RuntimeError("Error: "+message)

#-------------------------------------------------------------------------------

  def findFile(self, filename):
    if os.path.exists(filename):
      return os.path.abspath(filename)

    name, extension = os.path.splitext(filename)
    extension = extension[1:]

    if self.paths.has_key(extension):
      for path in self.paths[extension]:
        resultPath = os.path.join(path, filename)
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

  def run(self):
    if not self.base:
      self.base = ShowBase()
      self.scheduler = Scheduler()
      self.eventManager = EventManager()
      self.console = Console.pandaConsole(Console.INPUT_GUI |
        Console.OUTPUT_PYTHON, inspect.stack()[2][0].f_globals)
      self.console.toggle()
      self.objectManager = ObjectManager()

      for configFile in self.configFiles:
        self.loadConfigFile(configFile)

      self.base.run()
    else:
      self.error("Framework.run() may only be called once.")
