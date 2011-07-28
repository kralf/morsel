from morsel.core import *
from morsel.nodes.solid import Solid as Base
from morsel.nodes.ode.collider import Collider
from morsel.nodes.ode.geometry import Geometry
from morsel.nodes.facade import Body

#-------------------------------------------------------------------------------

class Solid(Base):
  def __init__(self, world, name, mesh, geometry = None, body = None,
      mass = 0, massOffset = [0, 0, 0], display = None, position = [0, 0, 0],
      orientation = [0, 0, 0], **kargs):
    self.geometry = None
    self.body = None
    self.display = display

    Base.__init__(self, world, name, mesh, **kargs)

    if not isinstance(self.parent, Collider):
      if not self.parent.collider:
        self.parent.collider = Collider(world, self.parent.name+"Collider",
          parent = self.parent)
      self.parent = self.parent.collider

    if geometry:
      self.geometry = Geometry(world, name+"Geometry", self, geometry,
        position = position, orientation = orientation, parent = self)

    if body:
      self.body = Body(name+"Body", body, self, mass = mass,
        massOffset = massOffset, parent = self)

    if self.display:
      self.display.parent = self
      self.display.setColor(1, 1, 1, 0.5)
      self.display.setTransparency(panda.TransparencyAttrib.MAlpha)

    if self.geometry:
      self.positionOffset = self.mesh.getPos(self.geometry)
      self.orientationOffset = self.mesh.getQuat(self.geometry)

#-------------------------------------------------------------------------------

  def setCollisionMasks(self, collisionsFrom, collisionsInto):
    if self.geometry:
      self.geometry.setCollisionMasks(collisionsFrom, collisionsInto)

#-------------------------------------------------------------------------------

  def update(self):
    if self.geometry:
      self.geometry.update()
    if self.body:
      self.body.update()
    if self.display:
      self.display.setPosQuat(self.geometry.getPos(), self.geometry.getQuat())
    if self.geometry:
      self.mesh.setPosQuat(self.geometry.getPos()+self.positionOffset,
        self.orientationOffset*self.geometry.getQuat())
