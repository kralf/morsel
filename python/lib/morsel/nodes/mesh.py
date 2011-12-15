from object import Object
from animation import Animation

#-------------------------------------------------------------------------------

class Mesh(Object):
  def __init__(self, world, name, filename = None, model = None,
      exclude = [], twoSided = False, parent = None, **kargs):
    Object.__init__(self, world, name, **kargs)

    self.filename = None
    self.animation = None
    self.twoSided = twoSided

    self._activeLayer = world.scene.activeLayer

    if filename:
      if isinstance(filename, dict):
        for layer in filename.iterkeys():
          self.setModel(loader.loadModel(filename[layer]), layer)
      else:
        self.model = loader.loadModel(filename)
    else:
      if isinstance(model, dict):
        self.clearTransform(model.itervalues().next())
        for layer in model.iterkeys():
          self.setModel(model, layer)
      else:
        self.clearTransform(model)
        self.model = model
      for model in self.models:
        model.clearTransform()
    
    if exclude:
      for model in self.models:
        for part in exclude:
          model.find("**/"+part).removeNode()

    self.parent = parent

    for model in self.models:
      character = model.find("*/+Character")
      if not character.isEmpty():
        self.animation = Animation(name+"Animation", self)
        character.hide()

#-------------------------------------------------------------------------------

  def getModel(self, layer = None):
    if layer:
      return self._model[layer]
    else:
      return self._model

  def setModel(self, model, layer = None):
    model.reparentTo(self)
    model.setTwoSided(self.twoSided)    

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
    else:
      return [self._model]

  models = property(getModels)

#-------------------------------------------------------------------------------

  def getActiveLayer(self):
    return self._activeLayer

  def setActiveLayer(self, layer):
    self._activeLayer = layer

    if self.layers:
      for layer in self.layers:
        if not layer or layer == self._activeLayer:
          self.getModel(layer).unstash()
        else:
          self.getModel(layer).stash()

  activeLayer = property(getActiveLayer, setActiveLayer)

#-------------------------------------------------------------------------------

  def updateGraphics(self):
    if self.animation:
      self.animation.step(self.world.time)
