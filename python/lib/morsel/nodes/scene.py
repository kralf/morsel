from node import Node
from iterator import Iterator
from mesh import Mesh
from solid import Solid
from static import Static
from actor import Actor
from sensor import Sensor
from platform import Platform
from view import View

#-------------------------------------------------------------------------------

class Scene(Node):
  def __init__(self, world, name, **kargs):
    Node.__init__(self, world, name, parent = render, **kargs)

    if not world.scene:
      world.scene = self
    else:
      framework.error("World already has a scene")

#-------------------------------------------------------------------------------

  def getMeshes(self):
    return Iterator(self, Mesh).generator

  meshes = property(getMeshes)

#-------------------------------------------------------------------------------

  def getSolids(self):
    return Iterator(self, Solid).generator

  solids = property(getSolids)

#-------------------------------------------------------------------------------

  def getStatics(self):
    return Iterator(self, Static).generator

  statics = property(getStatics)

#-------------------------------------------------------------------------------

  def getActors(self):
    return Iterator(self, Actor).generator

  actors = property(getActors)

#-------------------------------------------------------------------------------

  def getSensors(self):
    return Iterator(self, Sensor).generator

  sensors = property(getSensors)

#-------------------------------------------------------------------------------

  def getPlatforms(self):
    return Iterator(self, Platform).generator

  platforms = property(getPlatforms)

#-------------------------------------------------------------------------------

  def getViews(self):
    return Iterator(self, View).generator

  views = property(getViews)

#-------------------------------------------------------------------------------

  def __iter__(self):
    return Iterator(self)
