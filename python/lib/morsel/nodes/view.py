from object import Object

#-------------------------------------------------------------------------------

class View(Object):
  def __init__(self, world, name, **kargs):
    Object.__init__(self, world, name, **kargs)

#-------------------------------------------------------------------------------

  def updateGraphics(self):
    pass
