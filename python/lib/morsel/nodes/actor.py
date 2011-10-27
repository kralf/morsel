from morsel.world.globals import *
from node import Node
from morsel.nodes.facade import Collider

#-------------------------------------------------------------------------------

class Actor(Node):
  def __init__(self, world, name, collisionMasks = [ACTOR_COLLISIONS_FROM,
      ACTOR_COLLISIONS_INTO], **kargs):
    self._translationalVelocity = [0, 0, 0]
    self._rotationalVelocity = [0, 0, 0]
    self._mesh = None
    self._solid = None
    
    Node.__init__(self, world, name, **kargs)

    self.collider = Collider(name+"Collider", parent = self,
      collisionMasks = collisionMasks)

#-------------------------------------------------------------------------------

  def getPosition(self, node = None):
    if self.solid:
      if not node:
        node = self.parent
      return self.solid.getPosition(node)
    else:
      return Node.getPosition(self, node)
    
  def setPosition(self, position, node = None):
    Node.setPosition(self, position, node)

    if self.solid:
      self.solid.position = self.solid.position

  position = property(getPosition, setPosition)

#-------------------------------------------------------------------------------

  def getOrientation(self, node = None):
    if self.solid:
      if not node:
        node = self.parent
      return self.solid.getOrientation(node)
    else:
      return Node.getOrientation(self, node)
      
  def setOrientation(self, orientation, node = None):
    Node.setOrientation(self, orientation, node)

    if self.solid:
      self.solid.orientation = self.solid.orientation

  orientation = property(getOrientation, setOrientation)

#-------------------------------------------------------------------------------

  def getTranslationalVelocity(self):
    return self._translationalVelocity

  def setTranslationalVelocity(self, translationalVelocity):
    self._translationalVelocity = translationalVelocity

  translationalVelocity = property(getTranslationalVelocity,
    setTranslationalVelocity)

#-------------------------------------------------------------------------------

  def getRotationalVelocity(self):
    return self._rotationalVelocity

  def setRotationalVelocity(self, rotationalVelocity):
    self._rotationalVelocity = rotationalVelocity

  rotationalVelocity = property(getRotationalVelocity, setRotationalVelocity)

#-------------------------------------------------------------------------------

  def getMesh(self):
    return self._mesh

  def setMesh(self, mesh):
    self._mesh = mesh
    self._mesh.parent = self

  mesh = property(getMesh, setMesh)

#-------------------------------------------------------------------------------

  def getSolid(self):
    return self._solid

  def setSolid(self, solid):
    self._solid = solid
    self._solid.parent = self.collider
    
    self.collider.addSolid(solid)

  solid = property(getSolid, setSolid)

#-------------------------------------------------------------------------------

  def updatePhysics(self, period):
    pass

#-------------------------------------------------------------------------------

  def updateGraphics(self):
    pass
