from node import Node
from animation import Animation

#-------------------------------------------------------------------------------

class Mesh(Node):
  def __init__(self, world, name, filename = None, model = None,
      exclude = [], twoSided = False, parent = None, **kargs):
    Node.__init__(self, world, name, **kargs)

    self.filename = filename
    self.twoSided = twoSided
    self.animation = None
    
    if self.filename:
      self.model = loader.loadModel(self.filename)
    else:
      self.clearTransform(model)
      model.clearTransform()
      self.model = model
    
    if exclude:
      for part in exclude:
        self.model.find("**/"+part).removeNode()

    self.parent = parent

    character = self.model.find("*/+Character")
    if not character.isEmpty():
      self.animation = Animation(self.world, name+"Animation", self)
      character.hide()

#-------------------------------------------------------------------------------

  def getModel(self):
    return self._model

  def setModel(self, model):
    self._model = model
    
    model.reparentTo(self)
    model.setTwoSided(self.twoSided)    

  model = property(getModel, setModel)
