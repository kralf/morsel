from morsel.core import *
from morsel.nodes.solid import Solid as Base
from morsel.nodes.ode.collider import Collider
from morsel.nodes.ode.geometry import Geometry
from morsel.nodes.facade import Body

#-------------------------------------------------------------------------------

class Solid(Base):
  def __init__(self, world, name, mesh = None, geometry = None, body = None,
      mass = 0, massOffset = [0, 0, 0], display = None, position = [0, 0, 0],
      orientation = [0, 0, 0], scale = 1, **kargs):
    self.geometry = geometry
    self.body = None
    self.display = display
    self.positionOffset = [0, 0, 0]
    self.orientationOffset = [0, 0, 0]

    Base.__init__(self, world, name, mesh = mesh, **kargs)

    if body:
      self.body = Body(name+"Body", body, self, mass = mass,
        massOffset = massOffset, parent = self)

    if self.geometry:
      self.geometry.parent = self
      self.geometry.position = position
      self.geometry.orientation = orientation
      self.geometry.setCollisionMasks(self.collider.collisionMasks)
      if self.mesh:
        self.positionOffset = self.mesh.getPosition(self.geometry)
        self.orientationOffset = self.mesh.getOrientation(self.geometry)
      
    if self.display:
      self.display.parent = self
      self.display.scale = scale
      self.display.color = [1, 1, 1, 0.5]
      self.display.setTransparency(panda.TransparencyAttrib.MAlpha)

    self.position = position
    self.orientation = orientation

#-------------------------------------------------------------------------------

  def setPosition(self, position, node = None, recursive = True):
    Base.setPosition(self, position, node, recursive)

    if self.body:
      self.body.position = [0, 0, 0]
      self.body.orientation = [0, 0, 0]
    if self.geometry:
      self.geometry.position = [0, 0, 0]
      self.geometry.orientation = [0, 0, 0]
      if self.mesh:
        self.mesh.setPosition(self.positionOffset, self.geometry)
        self.mesh.setOrientation(self.orientationOffset, self)

  position = property(Base.getPosition, setPosition)

#-------------------------------------------------------------------------------

  def setOrientation(self, orientation, node = None, recursive = True):
    Base.setOrientation(self, orientation, node, recursive)

    if self.body:
      self.body.position = [0, 0, 0]
      self.body.orientation = [0, 0, 0]
    if self.geometry:
      self.geometry.position = [0, 0, 0]
      self.geometry.orientation = [0, 0, 0]
      if self.mesh:
        self.mesh.setPosition(self.positionOffset, self)
        self.mesh.setOrientation(self.orientationOffset, self.geometry)

  orientation = property(Base.getOrientation, setOrientation)

#-------------------------------------------------------------------------------

  def getCollisionMasks(self):
    if self.geometry:
      return self.geometry.getCollisionMasks()
    else:
      return []

  def setCollisionMasks(self, collisionMasks):
    if self.geometry:
      self.geometry.setCollisionMasks(collisionMasks)
      
    for child in self.getChildren(Solid):
      child.setCollisionMasks(collisionMasks)

  collisionMasks = property(getCollisionMasks, setCollisionMasks)

#-------------------------------------------------------------------------------

  def update(self):
    if self.geometry:
      quaternion = panda.Quat(self.geometry.geometry.getQuaternion())

      self.setPosition(self.geometry.geometry.getPosition(),
        self.world.scene, False)
      self.setOrientation(quaternion.getHpr(), self.world.scene, False)
    elif self.body:
      quaternion = panda.Quat(self.body.body.getQuaternion())
      
      self.setPosition(self.body.body.getPosition(), self.world.scene, False)
      self.setOrientation(quaternion.getHpr(), self.world.scene, False)
