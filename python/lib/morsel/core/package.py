from morsel.config import *

from os import *
from os.path import *

#-------------------------------------------------------------------------------

class Package(object):
  def __init__(self, name, homeVar = None, configDir = None, systemDir = None,
      userDir = None, module = None):
    object.__init__(self)

    self.name = name
    self.homeVar = homeVar
    self.systemDir = systemDir
    self.userDir = userDir
    self.module = module
    
    if not self.homeVar:
      self.homeVar = (self.name.replace("-", "_")+"_HOME").upper()
    if not self.systemDir:
      self.systemDir = os.path.join(MORSEL_FILE_PATH, self.name)
    if not self.userDir:
      self.userDir = os.path.join(os.environ["HOME"], "."+self.name)
    if not self.module:
      self.module = self.name.replace("-", "_")
    