from node import Node
from iterator import Iterator
from mesh import Mesh
from solid import Solid
from static import Static
from actor import Actor
from platform import Platform

#-------------------------------------------------------------------------------

class Scene(Node):
  def __init__(self, world, name, **kargs):
    Node.__init__(self, world, name, parent = render, **kargs)

    if not world.scene:
      world.scene = self
    else:
      raise RuntimeError("World already has a scene")

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

  def getPlatforms(self):
    return Iterator(self, Platform).generator

  platforms = property(getPlatforms)

#-------------------------------------------------------------------------------

  def __iter__(self):
    return Iterator(self)
