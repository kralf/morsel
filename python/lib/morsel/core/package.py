from morsel.config import Configuration

import os
from os.path import *

import __builtin__

#-------------------------------------------------------------------------------

class Package(object):
  def __init__(self, name, homeVar = None, configDir = None, systemDir = None,
      userDir = None, module = None, requires = None, options = None,
      arguments = None):
    object.__init__(self)

    self.name = name
    self.module = module
    self.requires = requires
    self.options = options
    self.arguments = arguments
    
    self.homeVar = homeVar
    self.configDir = configDir
    self.systemDir = systemDir
    self.userDir = userDir

    if not self.module:
      self.module = self.name.replace("-", "_")

    imported = __import__(self.module+".config", __builtin__.globals(),
      __builtin__.locals(), ["config"])
    self.configuration = getattr(imported, "Configuration")()
      
    if not self.homeVar:
      self.homeVar = (self.name.replace("-", "_")+"_HOME").upper()
    if not self.configDir:
      self.configDir = self.configuration.configurationPath
    if not self.systemDir:
      self.systemDir = self.configuration.filePath
    if not self.userDir:
      self.userDir = os.path.join(os.environ["HOME"], "."+self.name)
    
    if not self.requires:
      if hasattr(self.configuration, "requires"):
        self.requires = self.configuration.requires
    if not self.options:
      if hasattr(self.configuration, "options"):
        self.options = self.configuration.options
    if not self.arguments:
      if hasattr(self.configuration, "arguments"):
        self.arguments = self.configuration.arguments
    