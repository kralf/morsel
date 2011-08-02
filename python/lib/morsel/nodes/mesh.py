from node import Node

#-------------------------------------------------------------------------------

class Mesh(Node):
  def __init__(self, world, name, filename = None, model = None, exclude = [],
      twoSided = False, **kargs):
    Node.__init__(self, world, name, **kargs)

    self.filename = filename
    self.twoSided = twoSided
    
    if self.filename:
      self.model = loader.loadModel(self.filename)
    else:
      self.setTransformFromPath(model)
      self.model = model
      self.model.clearTransform()
      
    if exclude:
      for part in exclude:
        self.model.find("**/"+part).removeNode()

#-------------------------------------------------------------------------------

  def getModel(self):
    return self._model

  def setModel(self, model):
    self._model = model
    
    model.reparentTo(self)
    model.setTwoSided(self.twoSided)    

  model = property(getModel, setModel)
