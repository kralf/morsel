from morsel.panda import *
from morsel.nodes.solid import Solid as Base
from morsel.nodes.ode.facade import Body, Geometry

#-------------------------------------------------------------------------------

class Solid(Base):
  def __init__(self, world, name, mesh = None, geometry = None,
      body = None, mass = 0, massOffset = [0, 0, 0], **kargs):
    self.geometry = None
    self.body = None

    Base.__init__(self, world, name, mesh = mesh, **kargs)

    if mesh:
      self.clearTransform(mesh)
      p_min, p_max = mesh.getBounds(self)
      x = 0.5*(p_min[0]+p_max[0])
      y = 0.5*(p_min[1]+p_max[1])
      z = 0.5*(p_min[2]+p_max[2])
      dx = abs(p_max[0]-p_min[0])
      dy = abs(p_max[1]-p_min[1])
      dz = abs(p_max[2]-p_min[2])
      
      position = [x, y, z]
      scale = [dx, dy, dz]
    else:
      position = [0, 0, 0]
      scale = [0, 0, 0]

    if body:
      self.body = Body(name+"Body", body, self, mass = mass,
        position = [position[0]+massOffset[0], position[1]+massOffset[1],
        position[2]+massOffset[2]], scale = scale, parent = self)

    if geometry:
      self.geometry = Geometry(name+"Geometry", geometry, self,
        position = position, scale = scale, parent = self)
      self.geometry.collisionMasks = self.collider.collisionMasks

    if self.geometry and self.body:
      self.geometry.body = self.body

#-------------------------------------------------------------------------------

  def setPosition(self, position, node = None):
    Base.setPosition(self, position, node)

    if self.body:
      self.body.position = self.body.position
    elif self.geometry:
      self.geometry.position = self.geometry.position
    if self.mesh:
      self.mesh.setPos(self, self.getPos())

  position = property(Base.getPosition, setPosition)

#-------------------------------------------------------------------------------

  def setOrientation(self, orientation, node = None):
    Base.setOrientation(self, orientation, node)

    if self.body:
      self.body.orientation = self.body.orientation
    elif self.geometry:
      self.geometry.orientation = self.geometry.orientation
    if self.mesh:
      self.mesh.setQuat(self, self.getQuat())

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

  def updateTransform(self):
    if self.body:
      self.body.updateTransform()
    elif self.geometry:
      self.geometry.updateTransform()
    if self.mesh:
      self.mesh.setPosQuat(self, self.getPos(), self.getQuat())
      
    for child in self.getChildren(Solid):
      child.updateTransform()

#-------------------------------------------------------------------------------

  def updateGraphics(self):
    if self.body:
      transform = panda.TransformState.makePos(self.body.body.getPosition())
      transform = transform.setQuat(panda.Quat(self.body.body.getQuaternion()))
      bodyTransform = panda.TransformState.makePos(self.body.getPos())
      bodyTransform = bodyTransform.setQuat(self.body.getQuaternion())
      transform = transform.compose(bodyTransform.getInverse())
      
      if self.mesh:
        self.mesh.setTransform(self.world.scene, transform)
      self.setTransform(self.world.scene, transform)

      panda.TransformState.clearCache()
      