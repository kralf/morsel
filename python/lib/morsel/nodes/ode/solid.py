from morsel.core import *
from morsel.nodes.solid import Solid as Base
from morsel.nodes.ode.collider import Collider
from morsel.nodes.ode.geometry import Geometry
from morsel.nodes.facade import Body

#-------------------------------------------------------------------------------

class Solid(Base):
  def __init__(self, world, name, mesh, geometry = None, body = None,
      mass = 0, massOffset = [0, 0, 0], display = None, position = [0, 0, 0],
      orientation = [0, 0, 0], scale = [0, 0, 0], **kargs):
    self.geometry = geometry
    self.body = None
    self.display = display

    Base.__init__(self, world, name, mesh, **kargs)

    if body:
      self.body = Body(name+"Body", body, self, mass = mass,
        massOffset = massOffset, parent = self)

    if self.geometry:
      self.geometry.parent = self
      self.geometry.position = position
      self.geometry.orientation = orientation
      self.positionOffset = self.mesh.getPos(self.geometry)
      self.orientationOffset = self.mesh.getQuat(self.geometry)
      self.geometry.setCollisionMasks(self.parent.collisionMasks)
      
    if self.display:
      self.display.parent = self
      self.display.scale = scale
      self.display.setColor(1, 1, 1, 0.5)
      self.display.setTransparency(panda.TransparencyAttrib.MAlpha)

#-------------------------------------------------------------------------------

  def update(self):
    if self.body:
      if self.geometry:
        self.geometry.update()
      self.body.update()
      if self.display:
        self.display.setPosQuat(self.geometry.getPos(), self.geometry.getQuat())
        
      self.mesh.setPosQuat(self.geometry, self.positionOffset,
        self.orientationOffset)
