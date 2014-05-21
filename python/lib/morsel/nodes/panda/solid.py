from morsel.nodes.panda.object import Object
from morsel.nodes.geometry import Geometry

#-------------------------------------------------------------------------------

class Solid(Geometry):
  def __init__(self, name = "Solid", geometry = None, **kargs):
    self._geometry = None
    
    super(Solid, self).__init__(name = name, **kargs)
      
    self.geometry = geometry

#-------------------------------------------------------------------------------

  def getObject(self):
    if isinstance(self.parent, Object):
      return self.parent
    else:
      return None
      
  def setObject(self, object):
    if self.parent != object:
      self.parent = object
    
    self.fit(object)
    
  object = property(getObject, setObject)
  
#-------------------------------------------------------------------------------

  def getGeometry(self):
    return self._geometry
    
  def setGeometry(self, geometry):
    self._geometry = geometry
    
    if self.object:
      self.object.collider.node().clearSolids()
      self.object.collider.node().addSolid(self._geometry)
  
  geometry = property(getGeometry, setGeometry)
  