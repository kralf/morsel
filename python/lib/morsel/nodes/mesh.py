from morsel.panda import *
from node import Node
from animation import Animation

#-------------------------------------------------------------------------------

class Mesh(Node):
  def __init__(self, filename = None, model = None, exclude = None, twoSided =
      False, flatten = False, **kargs):
    self._activeLayer = None
        
    super(Mesh, self).__init__(**kargs)

    self.filename = None
    self.animation = None
    self.twoSided = twoSided

    if filename:
      if isinstance(filename, dict):
        for layer in filename.iterkeys():
          fileroot = filename[layer].rsplit(":", 1)
          
          if len(fileroot) > 1:
            model = panda.NodePath(loader.loadModel(fileroot[0])).find(
              fileroot[1])
          else:
            model = loader.loadModel(fileroot[0])

          self.setModel(model, layer)
      else:
        fileroot = filename.rsplit(":", 1)

        if len(fileroot) > 1:
          model = panda.NodePath(loader.loadModel(fileroot[0])).find(
            fileroot[1])
        else:
          model = loader.loadModel(fileroot[0])
          
        self.model = model
    elif model:
      if isinstance(model, dict):
        for layer in model.iterkeys():
          self.setModel(model, layer)
      else:
        self.model = model
    else:
      self.model = None
    
    if exclude:
      for model in self.models:
        if isinstance(exclude, list):
          for part in exclude:
            model.find("**/"+part).removeNode()
        else:
          model.find("**/"+exclude).removeNode()

    for model in self.models:
      character = model.find("*/+Character")
      if not character.isEmpty():
        self.animation = Animation(world = self.world, mesh = self)
        character.hide()
    
    if flatten:
      for model in self.models:
        model.flattenStrong()
    
    if self.world:
      self.activeLayer = self.world.scene.activeLayer

#-------------------------------------------------------------------------------

  def getModel(self, layer = None):
    if layer:
      return self._model[layer]
    else:
      return self._model

  def setModel(self, model, layer = None):
    if model:
      model.reparentTo(self)
      model.setTwoSided(self.twoSided)

      self.applyTransform(model)
      
    if layer:
      if not hasattr(self, "_model"):
        self._model = {}
      self._model[layer] = model
      
      if layer == self.activeLayer:
        model.unstash()
      else:
        model.stash()
    else:
      self._model = model

  model = property(getModel, setModel)

#-------------------------------------------------------------------------------

  def getModelName(self, layer = None):
    if layer:
      return self._model[layer].getName()
    else:
      return self._model.getName()

  modelName = property(getModelName)
  
#-------------------------------------------------------------------------------

  def getLayers(self):
    if isinstance(self._model, dict):
      return self._model.iterkeys()
    else:
      return [None]

  layers = property(getLayers)

#-------------------------------------------------------------------------------

  def getModels(self):
    if isinstance(self._model, dict):
      return self._model.itervalues()
    elif self._model:
      return [self._model]
    else:
      return []

  models = property(getModels)

#-------------------------------------------------------------------------------

  def getModelNames(self):
    if isinstance(self._model, dict):
      names = []
      for model in self.models:
        names.append(model.getName())
        
      return names
    elif self._model:
      return [self._model.getName()]
    else:
      return None

  modelNames = property(getModelNames)

#-------------------------------------------------------------------------------

  def getActiveLayer(self):
    return self._activeLayer

  def setActiveLayer(self, layer):
    self._activeLayer = layer

    for layer in self.layers:
      model = self.getModel(layer)
      
      if model:
        if not layer or layer == self._activeLayer:
          model.unstash()
        else:
          model.stash()

  activeLayer = property(getActiveLayer, setActiveLayer)

#-------------------------------------------------------------------------------

  def copyFrom(self, node, layer = None, flatten = False):
    model = node.copyTo(self)
    
    self.setModel(model, layer)

    model.clearTransform(node)
    if flatten:
      model.flattenStrong()
    