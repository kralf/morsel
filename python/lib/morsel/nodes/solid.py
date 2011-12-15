from object import Object
from iterator import Iterator
from facade import Collider

#-------------------------------------------------------------------------------

class Solid(Object):
  def __init__(self, world, name, mesh = None, parent = None, **kargs):
    if not isinstance(parent, Solid):
      if not parent.collider:
        parent.collider = Collider(name = parent.name+"Collider",
          parent = parent)
      Object.__init__(self, world, name, parent = parent.collider, **kargs)
    else:
      Object.__init__(self, world, name, parent = parent, **kargs)

    parent.collider.addSolid(self)
    
    self.mesh = mesh

#-------------------------------------------------------------------------------

  def setPosition(self, position, node = None):
    Object.setPosition(self, position, node)
    self.updateTransform()

  position = property(Object.getPosition, setPosition)

#-------------------------------------------------------------------------------

  def setOrientation(self, orientation, node = None):
    Object.setOrientation(self, orientation, node)
    self.updateTransform()

  orientation = property(Object.getOrientation, setOrientation)

#-------------------------------------------------------------------------------

  def updateTransform(self):
    pass
  