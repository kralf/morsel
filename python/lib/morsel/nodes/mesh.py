from node import Node

#-------------------------------------------------------------------------------

class Mesh(Node):
  def __init__(self, world, name, filename = None, twoSided = False, **kargs):
    Node.__init__(self, world, name, **kargs)

    self._model = None

    self.filename = filename
    self.twoSided = twoSided
    
    if self.filename:
      self.model = loader.loadModel(self.filename)

#-------------------------------------------------------------------------------

  def getModel(self):
    return self._model

  def setModel(self, model):
    self._model = model
    model.reparentTo(self)
    model.setTwoSided(self.twoSided)

  model = property(getModel, setModel)
