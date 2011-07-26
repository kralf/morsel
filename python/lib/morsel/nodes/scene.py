from node import Node
from iterator import Iterator
from mesh import Mesh
from solid import Solid
from actor import Actor
from platform import Platform

#-------------------------------------------------------------------------------

class Scene(Node):
  def __init__(self, world, name = "Scene", **kargs):
    Node.__init__(self, world, name, render, **kargs)

#-------------------------------------------------------------------------------

  def getMeshes(self):
    return Iterator(self, Mesh).generator

  meshes = property(getMeshes)

#-------------------------------------------------------------------------------

  def getSolids(self):
    return Iterator(self, Solid).generator

  solids = property(getSolids)

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
