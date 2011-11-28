from morsel.world.globals import *
from node import Node
from iterator import Iterator
from mesh import Mesh
from solid import Solid
from static import Static
from actuator import Actuator
from sensor import Sensor
from platform import Platform
from actor import Actor
from view import View
from facade import Collider, Solid

#-------------------------------------------------------------------------------

class Scene(Node):
  def __init__(self, world, name, **kargs):
    Node.__init__(self, world, name, parent = render, **kargs)

    if not world.scene:
      world.scene = self
    else:
      framework.error("World already has a scene")

    self.collider = Collider(name+"Collider", parent = self,
      collisionMasks = [STATIC_COLLISIONS_FROM, STATIC_COLLISIONS_INTO])
    self.solid = Solid(name+"Solid", "Empty", self, parent = self)

#-------------------------------------------------------------------------------

  def getMeshes(self):
    return Iterator(self, Mesh).generator

  meshes = property(getMeshes)

#-------------------------------------------------------------------------------

  def getSolids(self):
    return Iterator(self, Solid).generator

  solids = property(getSolids)

#-------------------------------------------------------------------------------

  def getActuators(self):
    return Iterator(self, Actuator).generator

  actors = property(getActuators)

#-------------------------------------------------------------------------------

  def getSensors(self):
    return Iterator(self, Sensor).generator

  sensors = property(getSensors)

#-------------------------------------------------------------------------------

  def getPlatforms(self):
    return Iterator(self, Platform).generator

  platforms = property(getPlatforms)

#-------------------------------------------------------------------------------

  def getActors(self):
    return Iterator(self, Actor).generator

  actors = property(getActors)

#-------------------------------------------------------------------------------

  def getViews(self):
    return Iterator(self, View).generator

  views = property(getViews)

#-------------------------------------------------------------------------------

  def __iter__(self):
    return Iterator(self)
