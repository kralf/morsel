from globals import *
from object import Object
from iterator import Iterator
from mesh import Mesh
from solid import Solid
from static import Static
from actuator import Actuator
from sensor import Sensor
from platform import Platform
from actor import Actor
from view import View
from controller import Controller
from facade import Collider, Solid

#-------------------------------------------------------------------------------

class Scene(Object):
  def __init__(self, world, name, activeLayer = None, collisionMasks =
      [STATIC_COLLISIONS_FROM, STATIC_COLLISIONS_INTO], **kargs):
    Object.__init__(self, world, name, parent = render, **kargs)

    if activeLayer:
      self.activeLayer = activeLayer
    else:
      self.activeLayer = framework.activeLayer

    self.collider = Collider(name = name+"Collider", parent = self,
      collisionMasks = collisionMasks)
    self.solid = Solid(name = name+"Solid", type = "Empty", mesh = self,
      parent = self)

#-------------------------------------------------------------------------------

  def getActiveLayer(self):
    return self._activeLayer

  def setActiveLayer(self, layer):
    self._activeLayer = layer

    for mesh in self.meshes:
      mesh.setActiveLayer(layer)

  activeLayer = property(getActiveLayer, setActiveLayer)

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

  def getControllers(self):
    return Iterator(self, Controller).generator

  controllers = property(getControllers)

#-------------------------------------------------------------------------------

  def __iter__(self):
    return Iterator(self)
