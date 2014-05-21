from node import Node
from iterator import Iterator
from mesh import Mesh
from object import Object
from static import Static
from sensor import Sensor
from platform import Platform
from actor import Actor
from view import View
from controller import Controller

#-------------------------------------------------------------------------------

class Scene(Node):
  def __init__(self, world = None, activeLayer = None, **kargs):
    self.world = world
    
    super(Scene, self).__init__(**kargs)

    if activeLayer:
      self.activeLayer = activeLayer
    else:
      self.activeLayer = framework.activeLayer
      
    framework.addShortcut("control-l", self.ls,
      "List the hierarchy at and below the scene")
      
    if self.world:
      self.world.scene = self

#-------------------------------------------------------------------------------

  def setParent(self, parent):
    if not parent:
      parent = render
      
    Node.setParent(self, parent)

  parent = property(Node.getParent, setParent)
  
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

  def getObjects(self):
    return Iterator(self, Object).generator

  objects = property(getObjects)

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
    